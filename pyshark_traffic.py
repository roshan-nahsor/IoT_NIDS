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
        p_length=packet.length

        if('IP' in packet):
        # IP layer
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            proto = packet.ip.proto

        else:
            src_ip = None
            dst_ip = None
            proto = None            
        
        if('ETH' in packet):
        # Ethernet layer
            src_eth = packet.eth.src
            dst_eth = packet.eth.dst
        else:
            src_eth = None
            dst_eth = None

        
        if('TCP' in packet):
        # TCP layer (if available)
            src_port = packet.tcp.srcport
            dst_port = packet.tcp.dstport
            inter_packet_time = packet.tcp.time_delta
        else:
            src_port = None
            dst_port = None
            inter_packet_time = None
            
        # if('MQTT' in packet):
        #     # client_id=packet.mqtt.client_id
        #     topic=packet.mqtt.topic
        #     topic_len=packet.mqtt.topic_len
        #     message=packet.mqtt.msg
        #     message_len=packet.mqtt.len
            
        # else:
        #     # client_id=None
        #     topic=None
        #     topic_len=None
        #     message=None
        #     message_len=None
            
        frame_num=packet.frame_info.number
        frame_time=packet.frame_info.time
        frame_len=packet.frame_info.len
        # frame_time_delta=packet.frame_info.time_delta
        
            
        
        # Print the extracted values, or empty string if the field doesn't exist
        # print(f"{src_ip:<15} {src_eth:<20} {src_port:<5} {dst_ip:<15} {dst_eth:<20} {dst_port:<5}")
        # print(f"{packet.layers} {src_ip} {src_eth} {src_port} {dst_ip} {dst_eth} {dst_port}")
        # print(f"{src_ip} {src_eth} {src_port} {dst_ip} {dst_eth} {dst_port} {proto} {p_length} {intit_time} {topic} {topic_len} {message} {message_len}")
        # print(f"{src_ip} {src_eth} {src_port} {dst_ip} {dst_eth} {dst_port} {proto} {p_length} {inter_packet_time}")
        # print(dir(packet))
        print(f"{frame_num} {frame_time} {frame_len} {src_eth} {src_ip} {src_port} {dst_eth} {dst_ip} {dst_port} {proto} {p_length} {inter_packet_time}")
        

        

if __name__ == "__main__":
    print(">main started")
    print_traffic()
    print(">main ended")