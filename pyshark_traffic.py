import pyshark

def print_traffic():
    # Capture live traffic on the default interface
    capture = pyshark.LiveCapture(interface='wlan0', display_filter='not tcp.port == 22')
    print(">wlan0 selected")
    capture.set_debug()
    
    capture.sniff(timeout=5)
    # capture
    capture.close()
    print("Capturing traffic... Press Ctrl+C to stop.")
    
    # for packet in capture.sniff_continuously(packet_count=None):  # Change packet_count to None for continuous capture
    for packet in capture:
        # print(">inside for")
        # print(packet)
        # print(
        #     packet.ip.src,
        #     packet.eth.src,
        #     # packet.tcp.srcport,
        #     # packet.ip.dst,
        #     # packet.eth.dst,
        #     # packet.ip.proto,
        #     # packet.tcp.dstport
        # )

        if('IP' in packet):
        # IP layer
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
        else:
            src_ip = ''
            dst_ip = ''
        
        if('ETH' in packet):
        # Ethernet layer
            src_eth = packet.eth.src
            dst_eth = packet.eth.dst
        else:
            src_eth = ''
            dst_eth = ''

        
        if('TCP' in packet):
        # TCP layer (if available)
            src_port = packet.tcp.srcport
            dst_port = packet.tcp.dstport
        else:
            src_port = ''
            dst_port = ''
        
        # Print the extracted values, or empty string if the field doesn't exist
        # print(f"{src_ip:<15} {src_eth:<20} {src_port:<5} {dst_ip:<15} {dst_eth:<20} {dst_port:<5}")
        print(f"{packet.layers} {src_ip} {src_eth} {src_port} {dst_ip} {dst_eth} {dst_port}")

        

if __name__ == "__main__":
    print(">main started")
    print_traffic()
    print(">main ended")