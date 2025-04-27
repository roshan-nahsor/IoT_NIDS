import pyshark
import csv

def capture_traffic_to_csv(output_file='live_dataset.csv'):
    capture = pyshark.LiveCapture(interface='wlan0', display_filter='not tcp.port == 22')
    print("> wlan0 selected")

    capture.set_debug()
    capture.sniff(timeout=5)
    capture.close()
    print("Capturing traffic... Writing to CSV...")

    # Define the header
    headers = [
        'frame.time', 'ip.src_host', 'ip.dst_host', 'arp.dst.proto_ipv4', 'arp.opcode', 'arp.hw.size',
        'arp.src.proto_ipv4', 'icmp.checksum', 'icmp.seq_le', 'icmp.transmit_timestamp', 'icmp.unused',
        'http.file_data', 'http.content_length', 'http.request.uri.query', 'http.request.method', 'http.referer',
        'http.request.full_uri', 'http.request.version', 'http.response', 'http.tls_port', 'tcp.ack', 'tcp.ack_raw',
        'tcp.checksum', 'tcp.connection.fin', 'tcp.connection.rst', 'tcp.connection.syn', 'tcp.connection.synack',
        'tcp.dstport', 'tcp.flags', 'tcp.flags.ack', 'tcp.len', 'tcp.options', 'tcp.payload', 'tcp.seq', 'tcp.srcport',
        'udp.port', 'udp.stream', 'udp.time_delta', 'dns.qry.name', 'dns.qry.name.len', 'dns.qry.qu', 'dns.qry.type',
        'dns.retransmission', 'dns.retransmit_request', 'dns.retransmit_request_in', 'mqtt.conack.flags',
        'mqtt.conflag.cleansess', 'mqtt.conflags', 'mqtt.hdrflags', 'mqtt.len', 'mqtt.msg_decoded_as', 'mqtt.msg',
        'mqtt.msgtype', 'mqtt.proto_len', 'mqtt.protoname', 'mqtt.topic', 'mqtt.topic_len', 'mqtt.ver',
        'mbtcp.len', 'mbtcp.trans_id', 'mbtcp.unit_id'
    ]

    # Open CSV file for writing
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for packet in capture:
            data = {}

            # Basic fields
            data['frame.time'] = getattr(packet.frame_info, 'time', None)

            # IP Layer
            data['ip.src_host'] = getattr(packet.ip, 'src', 0) if hasattr(packet, 'ip') else 0
            data['ip.dst_host'] = getattr(packet.ip, 'dst', 0) if hasattr(packet, 'ip') else 0

            # ARP Layer
            data['arp.dst.proto_ipv4'] = 0
            data['arp.opcode'] = 0
            data['arp.hw.size'] = 0.0
            data['arp.src.proto_ipv4'] = 0
            
            if hasattr(packet, 'arp'):
                # data['arp.dst.proto_ipv4'] = getattr(packet.arp, 'dst.proto_ipv4', 0)
                # data['arp.opcode'] = getattr(packet.arp, 'opcode', 0)
                # data['arp.hw.size'] = getattr(packet.arp, 'hw.size', 0.0)
                # data['arp.src.proto_ipv4'] = getattr(packet.arp, 'src.proto.ipv4', 0)
                # data['arp.dst.proto_ipv4'] = getattr(packet.arp.dst.proto_ipv4, '', 0)
                # data['arp.opcode'] = getattr(packet.arp.opcode, '', 0)
                # data['arp.hw.size'] = getattr(packet.arp.hw.size, '', 0.0)
                # data['arp.src.proto_ipv4'] = getattr(packet.arp.src.proto.ipv4, '', 0)
                data['arp.dst.proto_ipv4'] = 0
                data['arp.opcode'] = 0
                # data['arp.hw.size'] = 0.0 if packet.arp.hw.size is None else packet.arp.hw.size
                data['arp.hw.size'] = getattr(packet.arp, 'hw.size', 0.0)
                data['arp.src.proto_ipv4'] = getattr(packet.arp, 'src.proto.ipv4', 0)
                # data['arp.src.proto_ipv4'] = 0 if packet.arp.src.proto.ipv4 is None else packet.arp.src.proto.ipv4
                

            # ICMP Layer
            if hasattr(packet, 'icmp'):
                data['icmp.checksum'] = getattr(packet.icmp, 'checksum', 0)
                data['icmp.seq_le'] = getattr(packet.icmp, 'seq_le', 0.0)
                data['icmp.transmit_timestamp'] = getattr(packet.icmp, 'transmit_timestamp', 0)
                data['icmp.unused'] = getattr(packet.icmp, 'unused', 0.0)
            else:
                data['icmp.checksum'] = 0
                data['icmp.seq_le'] = 0.0
                data['icmp.transmit_timestamp'] = 0
                data['icmp.unused'] = 0.0




            # HTTP Layer
            data['http.file_data'] = 0.0
            data['http.content_length'] = 0.0
            data['http.request.uri.query'] = 0.0
            data['http.request.method'] = 0.0
            data['http.referer'] = 0.0
            data['http.request.full_uri'] = 0.0
            data['http.request.version'] = 0.0
            data['http.response'] = 0.0
            data['http.tls_port'] = 0.0

            if hasattr(packet, 'http'):
                # data['http.file_data'] = getattr(packet.http, 'file_data', 0.0)
                data['http.content_length'] = getattr(packet.http, 'content_length', 0.0)
                # data['http.request.uri.query'] = getattr(packet.http, 'request.uri.query', 0.0)
                # data['http.request.method'] = getattr(packet.http, 'request.method', 0.0)
                # data['http.referer'] = getattr(packet.http, 'referer', 0.0)
                # data['http.request.full_uri'] = getattr(packet.http, 'request.full_uri', 0.0)
                # data['http.request.version'] = getattr(packet.http, 'request.version', 0.0)
                data['http.response'] = getattr(packet.http, 'response', 0.0)
                # data['http.tls_port'] = getattr(packet.http, 'tls_port', 0.0)
    

            # TLS (inside TCP sometimes)
            # data['http.tls_port'] = 0.0  # Needs special handling, leave as None for now


            # TCP Layer
            data['tcp.ack'] = 0.0
            data['tcp.ack_raw'] = 0
            data['tcp.checksum'] = 0
            data['tcp.connection.fin'] = 0
            data['tcp.connection.rst'] = 0
            data['tcp.connection.syn'] = 0
            data['tcp.connection.synack'] = 0
            data['tcp.dstport'] = 0
            data['tcp.flags'] = 0
            data['tcp.flags.ack'] = 0
            data['tcp.len'] = 0
            data['tcp.options'] = 0.0
            data['tcp.payload'] = 0.0
            data['tcp.seq'] = 0
            data['tcp.srcport'] = 0.0
            
            if hasattr(packet, 'tcp'):
                data['tcp.ack'] = getattr(packet.tcp, 'ack', 0.0)
                data['tcp.ack_raw'] = getattr(packet.tcp, 'ack_raw', 0)
                data['tcp.checksum'] = getattr(packet.tcp, 'checksum', 0)
                data['tcp.connection.fin'] = getattr(packet.tcp, 'connection.fin', 0)
                data['tcp.connection.rst'] = getattr(packet.tcp, 'connection_rst', 0)
                data['tcp.connection.syn'] = getattr(packet.tcp, 'connection_syn', 0)
                data['tcp.connection.synack'] = getattr(packet.tcp, 'connection_synack', 0)
                data['tcp.dstport'] = getattr(packet.tcp, 'dstport', 0)
                data['tcp.flags'] = getattr(packet.tcp, 'flags', 0)
                data['tcp.flags.ack'] = getattr(packet.tcp, 'flags_ack', 0)
                data['tcp.len'] = getattr(packet.tcp, 'len', 0)
                data['tcp.options'] = getattr(packet.tcp, 'options', 0.0)
                data['tcp.payload'] = getattr(packet.tcp, 'payload', 0.0)
                data['tcp.seq'] = getattr(packet.tcp, 'seq', 0)
                data['tcp.srcport'] = getattr(packet.tcp, 'srcport', 0.0)
                
            # UDP Layer
            data['udp.port'] = 0
            data['udp.stream'] = 0
            data['udp.time_delta'] = 0
            
            if hasattr(packet, 'udp'):
                data['udp.port'] = getattr(packet.udp, 'port', 0)
                data['udp.stream'] = getattr(packet.udp, 'stream', 0)
                data['udp.time_delta'] = getattr(packet.udp, 'time_delta', 0)

            # DNS Layer
            data['dns.qry.name'] = 0
            data['dns.qry.name.len'] = 0.0
            data['dns.qry.qu'] = 0
            data['dns.qry.type'] = 0
            data['dns.retransmission'] = 0
            data['dns.retransmit_request'] = 0
            data['dns.retransmit_request_in'] = 0
            
            if hasattr(packet, 'dns'):
                data['dns.qry.name'] = getattr(packet.dns, 'qry.name', 0)
                data['dns.qry.name.len'] = getattr(packet.dns, 'qry.name.len', 0.0)
                data['dns.qry.qu'] = getattr(packet.dns, 'qry.qu', 0)
                data['dns.qry.type'] = getattr(packet.dns, 'qry.type', 0)
                data['dns.retransmission'] = getattr(packet.dns, 'retransmission', 0)
                data['dns.retransmit_request'] = getattr(packet.dns, 'retransmit_request', 0)
                data['dns.retransmit_request_in'] = getattr(packet.dns, 'retransmit_request_in', 0)

            # MQTT Layer
            data['mqtt.conack.flags'] = 0
            data['mqtt.conflag.cleansess'] = 0
            data['mqtt.conflags'] = 0
            data['mqtt.hdrflags'] = 0
            data['mqtt.len'] = 0
            data['mqtt.msg_decoded_as'] = 0
            data['mqtt.msg'] = 0.0
            data['mqtt.msgtype'] = 0
            data['mqtt.proto_len'] = 0
            data['mqtt.protoname'] = 0.0
            data['mqtt.topic'] = 0.0
            data['mqtt.topic_len'] = 0
            data['mqtt.ver'] = 0
            
            if hasattr(packet, 'mqtt'):
                data['mqtt.conack.flags'] = getattr(packet.mqtt, 'conack.flags', 0)
                data['mqtt.conflag.cleansess'] = getattr(packet.mqtt, 'con.flag.cleansess', 0)
                data['mqtt.conflags'] = getattr(packet.mqtt, 'conflags', 0)
                data['mqtt.hdrflags'] = getattr(packet.mqtt, 'hdrflags', 0)
                data['mqtt.len'] = getattr(packet.mqtt, 'len', 0)
                data['mqtt.msg_decoded_as'] = getattr(packet.mqtt, 'msg_decoded_as', 0)
                data['mqtt.msg'] = getattr(packet.mqtt, 'msg', 0.0)
                data['mqtt.msgtype'] = getattr(packet.mqtt, 'msgtype', 0)
                data['mqtt.proto_len'] = getattr(packet.mqtt, 'proto_len', 0)
                data['mqtt.protoname'] = getattr(packet.mqtt, 'protoname', 0.0)
                data['mqtt.topic'] = getattr(packet.mqtt, 'topic', 0.0)
                data['mqtt.topic_len'] = getattr(packet.mqtt, 'topic_len', 0)
                data['mqtt.ver'] = getattr(packet.mqtt, 'ver', 0)

            # Modbus TCP Layer (MBTCP)
            data['mbtcp.len'] = 0
            data['mbtcp.trans_id'] = 0
            data['mbtcp.unit_id'] = 0
                
            if hasattr(packet, 'mbtcp'):
                data['mbtcp.len'] = getattr(packet.mbtcp, 'len', 0)
                data['mbtcp.trans_id'] = getattr(packet.mbtcp, 'trans_id', 0)
                data['mbtcp.unit_id'] = getattr(packet.mbtcp, 'unit_id', 0)

            writer.writerow(data)

    print(f"CSV file '{output_file}' saved successfully.")

if __name__ == "__main__":
    print("> Main started")
    capture_traffic_to_csv()
    print("> Main ended")
