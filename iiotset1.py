# import pyshark
# import time
# from tabulate import tabulate
# import sys

# # Define fields to monitor
# FIELDS = [
#     "arp.opcode", "arp.hw.size", "icmp.checksum", "icmp.seq_le", "icmp.unused",
#     "http.content_length", "http.response", "http.tls_port",
#     "tcp.ack", "tcp.ack_raw", "tcp.checksum", "tcp.connection.fin", "tcp.connection.rst",
#     "tcp.connection.syn", "tcp.connection.synack", "tcp.flags", "tcp.flags.ack", "tcp.len", "tcp.seq",
#     "udp.stream", "udp.time_delta",
#     "dns.qry.name", "dns.qry.qu", "dns.qry.type", "dns.retransmission",
#     "dns.retransmit_request", "dns.retransmit_request_in",
#     "mqtt.conflag.cleansess", "mqtt.conflags", "mqtt.hdrflags", "mqtt.len",
#     "mqtt.msg_decoded_as", "mqtt.msgtype", "mqtt.proto_len", "mqtt.topic_len", "mqtt.ver",
#     "mbtcp.len", "mbtcp.trans_id", "mbtcp.unit_id"
# ]

# def get_field(packet, field):
#     """Try to extract a value from a dotted protocol.field string."""
#     try:
#         proto, attr = field.split('.', 1)
#         if hasattr(packet, proto):
#             return getattr(getattr(packet, proto), attr)
#     except Exception:
#         return None

# def print_live_capture(interface='wlan0'):
#     print(f"> Starting live capture on {interface}...\n(Press Ctrl+C to stop)")
#     capture = pyshark.LiveCapture(interface=interface, display_filter='not tcp.port == 22')

#     for packet in capture.sniff_continuously():
#         # Divide fields into two groups based on presence
#         present_fields = []
#         missing_fields = []

#         for field in FIELDS:
#             val = get_field(packet, field)
#             if val is not None:
#                 present_fields.append((field, str(val)))
#             else:
#                 missing_fields.append((field, "-"))

#         # Clear the screen
#         sys.stdout.write("\033[H\033[J")  # ANSI escape to clear screen and move cursor to top
#         print("Live Packet Field Monitor")
#         print("=" * 80)

#         # Print in two side-by-side columns
#         max_len = max(len(present_fields), len(missing_fields))
#         present_fields += [("", "")] * (max_len - len(present_fields))
#         missing_fields += [("", "")] * (max_len - len(missing_fields))

#         table = []
#         for left, right in zip(present_fields, missing_fields):
#             table.append([
#                 left[0], left[1], "│", right[0], right[1]
#             ])

#         print(tabulate(table, headers=["Present Field", "Value", "", "Missing Field", "Value"], tablefmt="fancy_grid"))

#         time.sleep(0.5)  # Slow down updates just a bit for readability

# if __name__ == "__main__":
#     try:
#         print_live_capture()
#     except KeyboardInterrupt:
#         print("\n> Capture stopped by user.")


import pyshark
import time
from tabulate import tabulate
import sys

# Only focus on MQTT fields
MQTT_FIELDS = [
    "mqtt.conflag.cleansess", "mqtt.conflags", "mqtt.hdrflags", "mqtt.len",
    "mqtt.msg_decoded_as", "mqtt.msgtype", "mqtt.proto_len", "mqtt.topic_len", "mqtt.ver"
]

def get_field(packet, field):
    """Try to extract a value from a dotted protocol.field string."""
    try:
        proto, attr = field.split('.', 1)
        if hasattr(packet, proto):
            return getattr(getattr(packet, proto), attr)
    except Exception:
        return None

def print_live_capture(interface='wlan0'):
    print(f"> Starting live MQTT capture on {interface}...\n(Press Ctrl+C to stop)")
    capture = pyshark.LiveCapture(interface=interface, display_filter='mqtt')

    # Preprint enough lines to "reserve" screen space
    print("\n" * (len(MQTT_FIELDS) + 6))  # leave space for header and buffer

    for packet in capture.sniff_continuously():
        present_fields = []
        missing_fields = []

        for field in MQTT_FIELDS:
            val = get_field(packet, field)
            if val is not None:
                present_fields.append((field, str(val)))
            else:
                missing_fields.append((field, "-"))

        # Move cursor to top-left without clearing whole screen
        sys.stdout.write("\033[H")
        sys.stdout.flush()

        print("📡 Live MQTT Packet Field Monitor")
        print("=" * 50)

        max_len = max(len(present_fields), len(missing_fields))
        present_fields += [("", "")] * (max_len - len(present_fields))
        missing_fields += [("", "")] * (max_len - len(missing_fields))

        table = []
        for left, right in zip(present_fields, missing_fields):
            table.append([
                left[0], left[1], "│", right[0], right[1]
            ])

        print(tabulate(table, headers=["Present Field", "Value", "", "Missing Field", "Value"], tablefmt="simple"))
        time.sleep(0.3)  # adjust refresh rate

if __name__ == "__main__":
    try:
        print_live_capture()
    except KeyboardInterrupt:
        print("\n> Capture stopped by user.")
