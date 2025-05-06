# === 1. Import Libraries ===
import pandas as pd
import numpy as np
import torch
import pickle
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import torch.nn.functional as F

# === 2. Define CNN model class ===
class CNN(torch.nn.Module):
    def __init__(self, num_class=15):
        super(CNN, self).__init__()
        self.conv1 = torch.nn.Conv1d(1, 64, kernel_size=3, padding=1)
        self.conv2 = torch.nn.Conv1d(64, 32, kernel_size=3, padding=1)
        self.conv3 = torch.nn.Conv1d(32, 16, kernel_size=3, padding=1)        
        self.fc1 = torch.nn.Linear(960, 30)
        self.out_layer = torch.nn.Linear(30, num_class)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.max_pool1d(x, kernel_size=1)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return F.log_softmax(self.out_layer(x), dim=1)

# === 3. Load Trained Model ===
from torch.serialization import add_safe_globals
add_safe_globals({"CNN": CNN})  # Allow unpickling CNN class

model = torch.load("cnn_nids_model.pth", weights_only=False)
model.eval()

# === 4. Load Scaler and LabelEncoders (fitted during training) ===
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

# === 5. Dataset class for torch ===
class NIDS_Dataset(Dataset):
    def __init__(self, X):
        self.X = X

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        sample = torch.tensor(self.X[idx], dtype=torch.float).unsqueeze(0)
        return sample

# === 6. Prediction Setup ===
attack_file_path = "F:/Documents/CRCE/Project/NIDS/dataset/Edge-IIoT/Edge-IIoTset dataset/Attack traffic/DDoS_UDP_Flood_attack.csv"
chunk_size = 50000

training_columns = ['ip.src_host', 'ip.dst_host', 'arp.dst.proto_ipv4', 'arp.opcode', 'arp.hw.size', 'arp.src.proto_ipv4', 'icmp.checksum', 'icmp.seq_le', 'icmp.transmit_timestamp', 'icmp.unused', 'http.file_data', 'http.content_length', 'http.request.uri.query', 'http.request.method', 'http.referer', 'http.request.full_uri', 'http.request.version', 'http.response', 'http.tls_port', 'tcp.ack', 'tcp.ack_raw', 'tcp.checksum', 'tcp.connection.fin', 'tcp.connection.rst', 'tcp.connection.syn', 'tcp.connection.synack', 'tcp.dstport', 'tcp.flags', 'tcp.flags.ack', 'tcp.len', 'tcp.options', 'tcp.payload', 'tcp.seq', 'tcp.srcport', 'udp.port', 'udp.stream', 'udp.time_delta', 'dns.qry.name', 'dns.qry.name.len', 'dns.qry.qu', 'dns.qry.type', 'dns.retransmission', 'dns.retransmit_request', 'dns.retransmit_request_in', 'mqtt.conack.flags', 'mqtt.conflag.cleansess', 'mqtt.conflags', 'mqtt.hdrflags', 'mqtt.len', 'mqtt.msg_decoded_as', 'mqtt.msg', 'mqtt.msgtype', 'mqtt.proto_len', 'mqtt.protoname', 'mqtt.topic', 'mqtt.topic_len', 'mqtt.ver', 'mbtcp.len', 'mbtcp.trans_id', 'mbtcp.unit_id']
categorical_cols = ['ip.src_host', 'ip.dst_host']

all_preds = []

# === 7. Process Chunks (the fixed chunk loop from earlier) ===
for chunk in pd.read_csv(attack_file_path, chunksize=chunk_size, low_memory=False):
    print("Processing a new chunk...")

    # Drop unnecessary columns
    chunk = chunk.drop(columns=[col for col in ["Attack_label", "Attack_type", "frame.time"] if col in chunk.columns])
    chunk = chunk[training_columns]

    # Encode categorical columns safely
    for col in categorical_cols:
        chunk[col] = chunk[col].astype(str)

        le = label_encoders[col]  # use pre-loaded encoder
        class_to_index = {label: idx for idx, label in enumerate(le.classes_)}
        chunk[col] = chunk[col].map(lambda s: class_to_index.get(s, -1))

    # Drop any remaining object columns
    chunk = chunk.select_dtypes(exclude=["object"])

    # Apply fitted scaler
    X_chunk = scaler.transform(chunk)

    # Dataset + Dataloader
    dataset = NIDS_Dataset(X_chunk)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=False)

    # Predict
    preds = []
    with torch.no_grad():
        for inputs in dataloader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            preds.extend(predicted.numpy())

    all_preds.extend(preds)

# === 8. Show Result Summary ===
print("\nTotal Predictions:", len(all_preds))
unique, counts = np.unique(all_preds, return_counts=True)
for cls, count in zip(unique, counts):
    print(f"Class {cls}: {count} instances")











import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import torch.nn.functional as F

# === 1. Load Pretrained Model (define your CNN model again) ===
class CNN(torch.nn.Module):
    def __init__(self, num_class=15):
        super(CNN, self).__init__()
        self.conv1 = torch.nn.Conv1d(1, 64, kernel_size=3, padding=1)
        self.conv2 = torch.nn.Conv1d(64, 32, kernel_size=3, padding=1)
        self.conv3 = torch.nn.Conv1d(32, 16, kernel_size=3, padding=1)        
        self.fc1 = torch.nn.Linear(960, 30)
        self.out_layer = torch.nn.Linear(30, num_class)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.max_pool1d(x, kernel_size=1)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return F.log_softmax(self.out_layer(x), dim=1)

import torch
from torch.serialization import add_safe_globals

add_safe_globals({"CNN": CNN})  # allow CNN class to be unpickled

model = torch.load("cnn_nids_model.pth", weights_only=False)
model.eval()

# === 2. Setup Encoder & Scaler ===
# You must fit these on your original training data first
# For now, we assume they are already available
label_encoders = {}
scaler = StandardScaler()

# === 3. Setup custom Dataset class ===
class NIDS_Dataset(Dataset):
    def __init__(self, X):
        self.X = X

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        sample = torch.tensor(self.X[idx], dtype=torch.float).unsqueeze(0)
        return sample

# === 4. Predict on chunks ===
attack_file_path = "F:/Documents/CRCE/Project/NIDS/dataset/Edge-IIoT/Edge-IIoTset dataset/Attack traffic/DDoS_UDP_Flood_attack.csv"
chunk_size = 50000

all_preds = []

training_columns = ['ip.src_host', 'ip.dst_host', 'arp.dst.proto_ipv4', 'arp.opcode', 'arp.hw.size', 'arp.src.proto_ipv4', 'icmp.checksum', 'icmp.seq_le', 'icmp.transmit_timestamp', 'icmp.unused', 'http.file_data', 'http.content_length', 'http.request.uri.query', 'http.request.method', 'http.referer', 'http.request.full_uri', 'http.request.version', 'http.response', 'http.tls_port', 'tcp.ack', 'tcp.ack_raw', 'tcp.checksum', 'tcp.connection.fin', 'tcp.connection.rst', 'tcp.connection.syn', 'tcp.connection.synack', 'tcp.dstport', 'tcp.flags', 'tcp.flags.ack', 'tcp.len', 'tcp.options', 'tcp.payload', 'tcp.seq', 'tcp.srcport', 'udp.port', 'udp.stream', 'udp.time_delta', 'dns.qry.name', 'dns.qry.name.len', 'dns.qry.qu', 'dns.qry.type', 'dns.retransmission', 'dns.retransmit_request', 'dns.retransmit_request_in', 'mqtt.conack.flags', 'mqtt.conflag.cleansess', 'mqtt.conflags', 'mqtt.hdrflags', 'mqtt.len', 'mqtt.msg_decoded_as', 'mqtt.msg', 'mqtt.msgtype', 'mqtt.proto_len', 'mqtt.protoname', 'mqtt.topic', 'mqtt.topic_len', 'mqtt.ver', 'mbtcp.len', 'mbtcp.trans_id', 'mbtcp.unit_id']
categorical_cols = ['ip.src_host', 'ip.dst_host']

# Fit encoders and scaler once using training data
# --- Assume you've done this before and saved them ---
# --- For real-time, you should load them via pickle ---

for chunk in pd.read_csv(attack_file_path, chunksize=chunk_size, low_memory=False):
    print("Processing a new chunk...")

    # Drop columns not used for inference
    if "Attack_label" in chunk.columns:
        y_chunk = chunk["Attack_label"]
        chunk = chunk.drop(columns=["Attack_label"])
    if "Attack_type" in chunk.columns:
        chunk = chunk.drop(columns=["Attack_type"])
    if "frame.time" in chunk.columns:
        chunk = chunk.drop(columns=["frame.time"])

    # Keep only training columns
    chunk = chunk[training_columns]

    from sklearn.preprocessing import LabelEncoder

    label_encoders = {}  # Dictionary to store fitted encoders for each column

    for col in categorical_cols:
        chunk[col] = chunk[col].astype(str)

        # If encoder for the column doesn't exist yet
        if col not in label_encoders:
            le = LabelEncoder()
            le.fit(chunk[col])
            label_encoders[col] = le
        else:
            le = label_encoders[col]

        # Ensure the encoder has been fitted
        if not hasattr(le, "classes_"):
            le.fit(chunk[col])
            label_encoders[col] = le

        # Create a lookup dictionary for safe mapping
        class_to_index = {label: idx for idx, label in enumerate(le.classes_)}

        # Apply safe transformation
        chunk[col] = chunk[col].map(lambda s: class_to_index.get(s, -1))



    # Encode remaining object columns
    other_cats = chunk.select_dtypes(include=["object"]).columns
    for col in other_cats:
        le = LabelEncoder()
        chunk[col] = chunk[col].astype(str).map(
            lambda s: le.transform([s])[0] if s in le.classes_ else -1
        )


    # Scale numeric features
    X_chunk = scaler.fit_transform(chunk)

    # Create dataset and dataloader
    dataset = NIDS_Dataset(X_chunk)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=False)

    # Predict
    preds = []
    with torch.no_grad():
        for inputs in dataloader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            preds.extend(predicted.numpy())

    all_preds.extend(preds)

# === 5. Display results ===
print("\nTotal Predictions:", len(all_preds))
unique, counts = np.unique(all_preds, return_counts=True)
for cls, count in zip(unique, counts):
    print(f"Class {cls}: {count} instances")
