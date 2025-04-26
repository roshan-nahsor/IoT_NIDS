# import pyshark
# import csv
# import os
# import sys
# import time

# def capture_traffic_to_csv():
#     capture = pyshark.LiveCapture(interface='wlan0', display_filter='not tcp.port == 22')
#     print(">wlan0 selected")
#     capture.set_debug()

#     capture.sniff(timeout=5)
#     capture.close()
#     print("Capturing traffic... Writing to CSV...\n")

#     # Define your fields and which ones need 0.0 (float) instead of 0
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

#     # Fields that should be considered floats (time_delta, etc.)
#     float_fields = ['UDP Time Delta']

#     filename = "captured_headers.csv"

#     # Open CSV file
#     with open(filename, mode='w', newline='') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=list(fields.keys()))
#         writer.writeheader()

#         try:
#             for packet in capture:
#                 row = {}
#                 for label, (layer_name, attr_name) in fields.items():
#                     value = None
#                     if hasattr(packet, layer_name):
#                         layer = getattr(packet, layer_name)
#                         if attr_name:
#                             value = getattr(layer, attr_name, None)
#                         else:
#                             # If attr_name is empty, take whole layer (for MQTT clean session, etc.)
#                             value = str(layer)
                    
#                     if value is None:
#                         # Default values if missing
#                         if label in float_fields:
#                             row[label] = 0.0
#                         else:
#                             row[label] = 0
#                     else:
#                         row[label] = str(value)
                
#                 writer.writerow(row)
#                 print(f"Packet captured and saved at {time.strftime('%H:%M:%S')}")
                
#         except KeyboardInterrupt:
#             print("\n\n>Interrupted by user. Exiting and closing CSV file.")
#         except Exception as e:
#             print(f"Error occurred: {e}")

#     print("\n>Capture session ended. File saved as", filename)

# if __name__ == "__main__":
#     print(">main started\n")
#     capture_traffic_to_csv()
#     print("\n>main ended")


import pyshark
import csv
import time

def capture_traffic_to_csv():
    capture = pyshark.LiveCapture(interface='wlan0', display_filter='not tcp.port == 22')
    print("> wlan0 selected")

    # New Headers as you specified
    fields = {
        'frame.time': ('frame_info', 'time'),
        'ip.src_host': ('ip', 'src_host'),
        'ip.dst_host': ('ip', 'dst_host'),
        'arp.dst.proto_ipv4': ('arp', 'dst_proto_ipv4'),
        'arp.opcode': ('arp', 'opcode'),
        'arp.hw.size': ('arp', 'hw_size'),
        'arp.src.proto_ipv4': ('arp', 'src_proto_ipv4'),
        'icmp.checksum': ('icmp', 'checksum'),
        'icmp.seq_le': ('icmp', 'seq_le'),
        'icmp.transmit_timestamp': ('icmp', 'transmit_timestamp'),
        'icmp.unused': ('icmp', 'unused'),
        'http.file_data': ('http', 'file_data'),
        'http.content_length': ('http', 'content_length'),
        'http.request.uri.query': ('http', 'request_uri_query'),
        'http.request.method': ('http', 'request_method'),
        'http.referer': ('http', 'referer'),
        'http.request.full_uri': ('http', 'request_full_uri'),
        'http.request.version': ('http', 'request_version'),
        'http.response': ('http', 'response'),
        'http.tls_port': ('http', 'tls_port'),
        'tcp.ack': ('tcp', 'ack'),
        'tcp.ack_raw': ('tcp', 'ack_raw'),
        'tcp.checksum': ('tcp', 'checksum'),
        'tcp.connection.fin': ('tcp', 'connection_fin'),
        'tcp.connection.rst': ('tcp', 'connection_rst'),
        'tcp.connection.syn': ('tcp', 'connection_syn'),
        'tcp.connection.synack': ('tcp', 'connection_synack'),
        'tcp.dstport': ('tcp', 'dstport'),
        'tcp.flags': ('tcp', 'flags'),
        'tcp.flags.ack': ('tcp', 'flags_ack'),
        'tcp.len': ('tcp', 'len'),
        'tcp.options': ('tcp', 'options'),
        'tcp.payload': ('tcp', 'payload'),
        'tcp.seq': ('tcp', 'seq'),
        'tcp.srcport': ('tcp', 'srcport'),
        'udp.port': ('udp', 'port'),
        'udp.stream': ('udp', 'stream'),
        'udp.time_delta': ('udp', 'time_delta'),
        'dns.qry.name': ('dns', 'qry_name'),
        'dns.qry.name.len': ('dns', 'qry_name_len'),
        'dns.qry.qu': ('dns', 'qry_qu'),
        'dns.qry.type': ('dns', 'qry_type'),
        'dns.retransmission': ('dns', 'retransmission'),
        'dns.retransmit_request': ('dns', 'retransmit_request'),
        'dns.retransmit_request_in': ('dns', 'retransmit_request_in'),
        'mqtt.conack.flags': ('mqtt', 'conack_flags'),
        'mqtt.conflag.cleansess': ('mqtt', 'conflag_cleansess'),
        'mqtt.conflags': ('mqtt', 'conflags'),
        'mqtt.hdrflags': ('mqtt', 'hdrflags'),
        'mqtt.len': ('mqtt', 'len'),
        'mqtt.msg_decoded_as': ('mqtt', 'msg_decoded_as'),
        'mqtt.msg': ('mqtt', 'msg'),
        'mqtt.msgtype': ('mqtt', 'msgtype'),
        'mqtt.proto_len': ('mqtt', 'proto_len'),
        'mqtt.protoname': ('mqtt', 'protoname'),
        'mqtt.topic': ('mqtt', 'topic'),
        'mqtt.topic_len': ('mqtt', 'topic_len'),
        'mqtt.ver': ('mqtt', 'ver'),
        'mbtcp.len': ('mbtcp', 'len'),
        'mbtcp.trans_id': ('mbtcp', 'trans_id'),
        'mbtcp.unit_id': ('mbtcp', 'unit_id'),
    }

    # List of fields to be treated as floats
    float_fields = ['udp.time_delta']

    filename = "saturdaycapture_headers.csv"

    print("> Capturing packets for 1 minute... Please wait.")

    # Capture for 60 seconds
    capture.sniff(timeout=60)

    print("\n> 1 minute completed. Writing captured data to CSV...")

    # Open CSV file
    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(fields.keys()))
        writer.writeheader()

        for packet in capture:
            row = {}
            for label, (layer_name, attr_name) in fields.items():
                value = None
                if hasattr(packet, layer_name):
                    layer = getattr(packet, layer_name)
                    if attr_name:
                        value = getattr(layer, attr_name, None)
                    else:
                        value = str(layer)
                
                if value is None:
                    # Default values if missing
                    if label in float_fields:
                        row[label] = 0.0
                    else:
                        row[label] = 0
                else:
                    row[label] = str(value)
            
            writer.writerow(row)
            print(f"Packet captured at {time.strftime('%H:%M:%S')}")

    print("\n> Capture session ended. File saved as", filename)

if __name__ == "__main__":
    print("> Main started\n")
    capture_traffic_to_csv()
    print("\n> Main ended")
