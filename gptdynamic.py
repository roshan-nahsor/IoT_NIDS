# import pyshark
# import time
# import os
# import sys

# def print_traffic():
#     capture = pyshark.LiveCapture(interface='wlan0', display_filter='not tcp.port == 22')
#     print(">wlan0 selected")
#     capture.set_debug()

#     capture.sniff(timeout=5)
#     capture.close()
#     print("Capturing traffic... Updating headers live...\n")

#     fields = {
#         'ARP Opcode': ('arp', 'opcode'),
#         'ARP HW Size': ('arp', 'hw_size'),
#         'ICMP Checksum': ('icmp', 'checksum'),
#         'ICMP Seq LE': ('icmp', 'seq_le'),
#         'ICMP Unused': ('icmp', 'unused'),
#         'HTTP Content-Length': ('http', 'content_length'),
#         'HTTP Response': ('http', 'response'),
#         'HTTP TLS Port': ('http', 'tls_port'),
#         'TCP ACK': ('tcp', 'ack'),
#         'TCP ACK Raw': ('tcp', 'ack_raw'),
#         'TCP Checksum': ('tcp', 'checksum'),
#         'TCP FIN': ('tcp', 'connection_fin'),
#         'TCP RST': ('tcp', 'connection_rst'),
#         'TCP SYN': ('tcp', 'connection_syn'),
#         'TCP SYNACK': ('tcp', 'connection_synack'),
#         'TCP Flags': ('tcp', 'flags'),
#         'TCP Flags ACK': ('tcp', 'flags_ack'),
#         'TCP Length': ('tcp', 'len'),
#         'TCP Seq': ('tcp', 'seq'),
#         'UDP Stream': ('udp', 'stream'),
#         'UDP Time Delta': ('udp', 'time_delta'),
#         'DNS Query Name': ('dns', 'qry_name'),
#         'DNS Query QU': ('dns', 'qry_qu'),
#         'DNS Query Type': ('dns', 'qry_type'),
#         'DNS Retransmission': ('dns', 'retransmission'),
#         'DNS Retransmit Req': ('dns', 'retransmit_request'),
#         'DNS Retransmit Req In': ('dns', 'retransmit_request_in'),
#         'MQTT Clean Session': ('mqtt', ''),
#         'MQTT Flags': ('mqtt', 'conflags'),
#         'MQTT HDR Flags': ('mqtt', 'hdrflags'),
#         'MQTT Length': ('mqtt', 'len'),
#         'MQTT Decoded As': ('mqtt', 'msg_decoded_as'),
#         'MQTT Msg Type': ('mqtt', 'msgtype'),
#         'MQTT Proto Len': ('mqtt', 'proto_len'),
#         'MQTT Topic Len': ('mqtt', 'topic_len'),
#         'MQTT Version': ('mqtt', 'ver'),
#         'Modbus TCP Length': ('mbtcp', 'len'),
#         'Modbus Trans ID': ('mbtcp', 'trans_id'),
#         'Modbus Unit ID': ('mbtcp', 'unit_id'),
#     }

#     # Initially, all fields are considered "missing"
#     missing_fields = list(fields.keys())
#     received_fields = []

#     def print_live_table():
#         os.system('clear' if os.name == 'posix' else 'cls')
#         print("======== LIVE PACKET HEADER STATUS ========")
#         print(f"{'Received Fields':<40} | {'Missing Fields'}")
#         print("-" * 80)
#         for i in range(max(len(received_fields), len(missing_fields))):
#             left = received_fields[i] if i < len(received_fields) else ""
#             right = missing_fields[i] if i < len(missing_fields) else ""
#             print(f"{left:<40} | {right}")
#         print("===========================================\n")
#         print("Listening... press Ctrl+C to stop.")

#     for packet in capture:
#         for label, (layer_name, attr) in fields.items():
#             present = False
#             if hasattr(packet, layer_name):
#                 layer = getattr(packet, layer_name)
#                 if hasattr(layer, attr):
#                     present = True

#             if present and label in missing_fields:
#                 missing_fields.remove(label)
#                 received_fields.append(label)
#             elif not present and label in received_fields:
#                 received_fields.remove(label)
#                 missing_fields.append(label)

#         print_live_table()
#         time.sleep(1)

# if __name__ == "__main__":
#     print(">main started\n")
#     try:
#         print_traffic()
#     except KeyboardInterrupt:
#         print("\n\n>Interrupted by user. Exiting gracefully.")
#     print("\n>main ended")