import pyshark
import csv

def save_csv():
    # Capture live traffic on the default interface
    capture = pyshark.LiveCapture(interface='wlan0', display_filter='not tcp.port == 22')
    print(">wlan0 selected")
    capture.set_debug()
    
    capture.sniff(timeout=5)
    # capture
    capture.close()
    print("Capturing traffic... Press Ctrl+C to stop.")
    
    # Open a CSV file to write the captured data
    with open('captured_traffic.csv', mode='w', newline='') as csv_file:
        fieldnames = ['frame_num', 'frame_time', 'frame_len', 'src_eth', 'src_ip', 'src_port', 
                      'dst_eth', 'dst_ip', 'dst_port', 'proto', 'p_length', 'inter_packet_time']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write header row
        writer.writeheader()
        
        # Iterate through captured packets and extract information
        for packet in capture:
            p_length = packet.length
            frame_num = packet.frame_info.number
            frame_time = packet.frame_info.time
            frame_len = packet.frame_info.len
            
            # Default values for layers
            src_ip = "None"
            dst_ip = "None"
            proto = "None"
            src_eth = "None"
            dst_eth = "None"
            src_port = "None"
            dst_port = "None"
            inter_packet_time = "None"
            
            # Extract IP layer details if available
            if 'IP' in packet:
                src_ip = packet.ip.src
                dst_ip = packet.ip.dst
                proto = packet.ip.proto
            
            # Extract Ethernet layer details if available
            if 'ETH' in packet:
                src_eth = packet.eth.src
                dst_eth = packet.eth.dst
            
            # Extract TCP layer details if available
            if 'TCP' in packet:
                src_port = packet.tcp.srcport
                dst_port = packet.tcp.dstport
                inter_packet_time = packet.tcp.time_delta
            
            # Prepare row for CSV
            row = {
                'frame_num': frame_num,
                'frame_time': frame_time,
                'frame_len': frame_len,
                'src_eth': src_eth,
                'src_ip': src_ip,
                'src_port': src_port,
                'dst_eth': dst_eth,
                'dst_ip': dst_ip,
                'dst_port': dst_port,
                'proto': proto,
                'p_length': p_length,
                'inter_packet_time': inter_packet_time
            }
            
            # Write the packet data row to CSV
            writer.writerow(row)
        

if __name__ == "__main__":
    print(">main started")
    save_csv()
    print(">main ended")