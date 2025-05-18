# /path/to/your_project/run.py
from flask import Flask, render_template, Response, jsonify
from scapy.all import sniff, IP, TCP, UDP, Raw
import threading
import queue
import json
import time
import psutil
import math
import hashlib  # <-- Added for hashing

app = Flask(__name__)
packet_queue = queue.Queue()
all_packets = []
infected_packets = []
sniff_thread = None
stop_sniffing = False

def get_interfaces():
    stats = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()
    interfaces = []
    for iface in stats:
        is_up = stats[iface].isup
        has_ip = any(addr.family.name == 'AF_INET' for addr in addrs.get(iface, []))
        interfaces.append({
            "name": iface,
            "active": is_up and has_ip
        })
    return interfaces

def calc_entropy(data):
    if not data:
        return 0
    byte_counts = [0] * 256
    for b in data:
        byte_counts[b] += 1
    entropy = 0
    for count in byte_counts:
        if count:
            p = count / len(data)
            entropy -= p * math.log2(p)
    return entropy

def parse_packet(pkt):
    try:
        layers = []
        proto_name = "Other"
        sport = dport = None
        payload_size = 0
        payload = ""
        app_data = b""

        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            proto = pkt[IP].proto
            layers.append("IP")
            if TCP in pkt:
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
                layers.append("TCP")
                proto_name = "TCP"
                if Raw in pkt:
                    app_data = pkt[Raw].load
                    payload_size = len(app_data)
                    try:
                        payload = app_data.decode(errors='replace')
                        if payload.startswith("GET") or payload.startswith("POST") or "HTTP" in payload:
                            layers.append("HTTP")
                            proto_name = "HTTP"
                    except:
                        pass
            elif UDP in pkt:
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
                layers.append("UDP")
                proto_name = "UDP"
                if Raw in pkt:
                    app_data = pkt[Raw].load
                    payload_size = len(app_data)
                    try:
                        payload = app_data.decode(errors='replace')
                    except:
                        pass
            else:
                proto_name = str(proto)

            hex_payload = bytes(pkt).hex()
            entropy = calc_entropy(app_data)
            malicious_signatures = [
                "malware", "exploit", "cmd.exe", "powershell", "wget",
                "curl", "<script>", "eval(", "base64", "reverse shell"
            ]
            is_malicious = any(sig in payload.lower() for sig in malicious_signatures) or entropy > 7.5

            # Calculate hashes if malicious and payload exists
            md5_hash = sha1_hash = sha256_hash = None
            if is_malicious and app_data:
                md5_hash = hashlib.md5(app_data).hexdigest()
                sha1_hash = hashlib.sha1(app_data).hexdigest()
                sha256_hash = hashlib.sha256(app_data).hexdigest()

            packet_info = {
                "time": time.strftime('%I:%M:%S %p', time.localtime(pkt.time)),
                "src_ip": src_ip,
                "sport": sport,
                "dst_ip": dst_ip,
                "dport": dport,
                "proto": proto_name,
                "layers": ", ".join(layers),
                "payload": payload,
                "payload_size": payload_size,
                "hex_payload": hex_payload,
                "entropy": round(entropy, 2),
                "malicious": is_malicious,
                "md5": md5_hash,
                "sha1": sha1_hash,
                "sha256": sha256_hash
            }
            return packet_info
    except Exception as e:
        print(f"Error parsing packet: {e}")
        return None

def packet_handler(pkt):
    global stop_sniffing
    if stop_sniffing:
        return False
    info = parse_packet(pkt)
    if info:
        packet_queue.put(json.dumps(info))
        all_packets.insert(0, info)
        if info["malicious"]:
            infected_packets.insert(0, info)
            if len(infected_packets) > 1000:
                infected_packets.pop()
        if len(all_packets) > 1000:
            all_packets.pop()

def start_sniff(interface):
    global stop_sniffing
    stop_sniffing = False
    sniff(iface=interface, prn=packet_handler, store=False, stop_filter=lambda x: stop_sniffing)

@app.route('/')
def index():
    interfaces = get_interfaces()
    return render_template('index.html', interfaces=interfaces)

@app.route('/start_capture/<iface>')
def start_capture(iface):
    global sniff_thread, stop_sniffing
    if sniff_thread and sniff_thread.is_alive():
        return jsonify({"status": "Already capturing"})
    stop_sniffing = False
    sniff_thread = threading.Thread(target=start_sniff, args=(iface,), daemon=True)
    sniff_thread.start()
    return jsonify({"status": "Started capture on " + iface})

@app.route('/stop_capture')
def stop_capture():
    global stop_sniffing
    stop_sniffing = True
    return jsonify({"status": "Stopping capture..."})

@app.route('/stream')
def stream():
    def event_stream():
        while True:
            try:
                pkt = packet_queue.get(timeout=1)
                yield f"data: {pkt}\n\n"
            except queue.Empty:
                yield "data: {}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/packet/<int:index>')
def packet_detail(index):
    if 0 <= index < len(all_packets):
        return jsonify(all_packets[index])
    return jsonify({"error": "Packet not found"}), 404

@app.route('/infected')
def infected():
    return render_template('infected.html', infected_count=len(infected_packets))

@app.route('/api/infected_packets')
def get_infected_packets():
    return jsonify(infected_packets)

@app.route('/infected_packet/<int:index>')
def infected_packet_detail(index):
    if 0 <= index < len(infected_packets):
        return jsonify(infected_packets[index])
    return jsonify({"error": "Packet not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
