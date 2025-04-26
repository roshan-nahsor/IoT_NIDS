import pyshark
import time
import os
import sys

def print_traffic():
    capture = pyshark.LiveCapture(interface='wlan0', display_filter='not tcp.port == 22')
    print(">wlan0 selected")
    capture.set_debug()

    capture.sniff(timeout=5)
    capture.close()
    print("Capturing traffic... Updating headers live...\n")

    fields = {
        'ARP Opcode': ('arp', 'opcode'),
        'ARP HW Size': ('arp', 'hw_size'),
        'ICMP Checksum': ('icmp', 'checksum'),
        'ICMP Seq LE': ('icmp', 'seq_le'),
        'ICMP Unused': ('icmp', 'unused'),
        'HTTP Content-Length': ('http', 'content_length'),
        'HTTP Response': ('http', 'response'),
        'HTTP TLS Port': ('http', 'tls_port'),
        'TCP ACK': ('tcp', 'ack'),
        'TCP ACK Raw': ('tcp', 'ack_raw'),
        'TCP Checksum': ('tcp', 'checksum'),
        'TCP FIN': ('tcp', 'connection_fin'),
        'TCP RST': ('tcp', 'connection_rst'),
        'TCP SYN': ('tcp', 'connection_syn'),
        'TCP SYNACK': ('tcp', 'connection_synack'),
        'TCP Flags': ('tcp', 'flags'),
        'TCP Flags ACK': ('tcp', 'flags_ack'),
        'TCP Length': ('tcp', 'len'),
        'TCP Seq': ('tcp', 'seq'),
        'UDP Stream': ('udp', 'stream'),
        'UDP Time Delta': ('udp', 'time_delta'),
        'DNS Query Name': ('dns', 'qry_name'),
        'DNS Query QU': ('dns', 'qry_qu'),
        'DNS Query Type': ('dns', 'qry_type'),
        'DNS Retransmission': ('dns', 'retransmission'),
        'DNS Retransmit Req': ('dns', 'retransmit_request'),
        'DNS Retransmit Req In': ('dns', 'retransmit_request_in'),
        'MQTT Clean Session': ('mqtt', ''),
        'MQTT Flags': ('mqtt', 'conflags'),
        'MQTT HDR Flags': ('mqtt', 'hdrflags'),
        'MQTT Length': ('mqtt', 'len'),
        'MQTT Decoded As': ('mqtt', 'msg_decoded_as'),
        'MQTT Msg Type': ('mqtt', 'msgtype'),
        'MQTT Proto Len': ('mqtt', 'proto_len'),
        'MQTT Topic Len': ('mqtt', 'topic_len'),
        'MQTT Version': ('mqtt', 'ver'),
        'Modbus TCP Length': ('mbtcp', 'len'),
        'Modbus Trans ID': ('mbtcp', 'trans_id'),
        'Modbus Unit ID': ('mbtcp', 'unit_id'),
    }

    missing_fields = list(fields.keys())
    received_fields = {}

    def print_live_table():
        os.system('clear' if os.name == 'posix' else 'cls')
        print("======== LIVE PACKET HEADER STATUS ========")
        print(f"{'Received Fields (with Values)':<50} | {'Missing Fields'}")
        print("-" * 100)
        all_received = list(received_fields.items())
        max_len = max(len(all_received), len(missing_fields))

        for i in range(max_len):
            left = f"{all_received[i][0]}: {all_received[i][1]}" if i < len(all_received) else ""
            right = missing_fields[i] if i < len(missing_fields) else ""
            print(f"{left:<50} | {right}")
        print("===========================================\n")
        print("Listening... press Ctrl+C to stop.")

    for packet in capture:
        for label, (layer_name, attr) in fields.items():
            value = None
            if hasattr(packet, layer_name):
                layer = getattr(packet, layer_name)
                if attr and hasattr(layer, attr):
                    value = getattr(layer, attr)
                elif not attr:  # Some fields like MQTT Clean Session had empty attr
                    value = str(layer)  # fallback to raw layer

            if value is not None:
                if label in missing_fields:
                    missing_fields.remove(label)
                received_fields[label] = str(value)
            else:
                if label in received_fields:
                    del received_fields[label]
                if label not in missing_fields:
                    missing_fields.append(label)

        print_live_table()
        time.sleep(1)

if __name__ == "__main__":
    print(">main started\n")
    try:
        print_traffic()
    except KeyboardInterrupt:
        print("\n\n>Interrupted by user. Exiting gracefully.")
    print("\n>main ended")


