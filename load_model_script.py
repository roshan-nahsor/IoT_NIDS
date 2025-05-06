import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import sys


num_class = 15

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv1d(1, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(64, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv1d(32, 16, kernel_size=3, padding=1)        
        self.fc1 = nn.Linear(39 * 16, 30)
        self.out_layer = nn.Linear(30, num_class)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.max_pool1d(x, kernel_size=1)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return F.log_softmax(self.out_layer(x), dim=1)


saved_model=CNN()
saved_model.load_state_dict(torch.load('tuesday_model.pth'))

saved_model.eval()


# data_path = 'F:/Documents/CRCE/Project/NIDS/dataset/Edge-IIoT/Edge-IIoTset dataset/Attack traffic/DDoS_UDP_Flood_attack.csv'  # Replace with your actual path
# data_path = 'live_dataset_1.csv'  # Replace with your actual path
data_path = 'presentation_dataset.csv'  # Replace with your actual path
df = pd.read_csv(data_path, low_memory=False)
df.head()


# Drop unnecessary columns
drop_columns = [
    "frame.time", "ip.src_host", "ip.dst_host", "arp.src.proto_ipv4", "arp.dst.proto_ipv4",
    "http.file_data", "http.request.full_uri", "icmp.transmit_timestamp", "http.request.uri.query",
    "tcp.options", "tcp.payload", "tcp.srcport", "tcp.dstport", "udp.port", "mqtt.msg"
]
df.drop(drop_columns, axis=1, inplace=True, errors='ignore')

# Remove NaNs and duplicates
# df.dropna(axis=0, how='any', inplace=True)
# df.drop_duplicates(subset=None, keep="first", inplace=True)

# Strip strings
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# DO NOT shuffle here (this is for training only)
# df = shuffle(df)

# One-hot encode categorical columns
def encode_text_dummy(df, name):
    dummies = pd.get_dummies(df[name], prefix=name)
    df = pd.concat([df, dummies], axis=1)
    return df.drop(name, axis=1)

for col in ['http.request.method', 'http.referer', 'http.request.version',
            'dns.qry.name.len', 'mqtt.conack.flags', 'mqtt.protoname', 'mqtt.topic']:
    if col in df.columns:
        df = encode_text_dummy(df, col)

# Save 'Attack_type' if present
if 'Attack_type' in df.columns:
    labels = df['Attack_type']
else:
    labels = None

# Keep only numeric columns
df = df.select_dtypes(include=[np.number]).copy()

# Add back label for later comparison
if labels is not None:
    df['Attack_type'] = labels



import joblib
import torch

# Load training-time artifacts
feature_columns = joblib.load("feature_columns.pkl")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# Align current dataframe's columns to match training
df = df.reindex(columns=feature_columns, fill_value=0)

# Apply scaling (again)
features_scaled = scaler.transform(df)

# Convert to tensor
X_attack = torch.tensor(features_scaled, dtype=torch.float32).unsqueeze(1)  # (batch_size, 1, num_features)

# Load the model architecture and weights
saved_model=CNN()
saved_model.load_state_dict(torch.load('tuesday_model.pth'))
saved_model.eval()  # Put model in evaluation mode




with torch.no_grad():
    outputs = saved_model(X_attack)
    _, predicted = torch.max(outputs, 1)
    predicted_labels = label_encoder.inverse_transform(predicted.numpy())

print(predicted_labels)
len(predicted_labels)




# data_path = 'F:/Documents/CRCE/Project/NIDS/dataset/Edge-IIoT/Edge-IIoTset dataset/Attack traffic/DDoS_UDP_Flood_attack.csv'  # Replace with your actual path
# data_path = 'live_dataset_1.csv'  # Replace with your actual path
data_path = 'presentation_dataset.csv'  # Replace with your actual path
df = pd.read_csv(data_path, low_memory=False)
df.head()


df['predicted_type']=predicted_labels


df['Attack_label'] = (df['predicted_type'] != 'Normal').astype(int)
# df



# df.to_csv('CNN_predictions.csv', index=False)  # Save predictions to a new CSV file
df.to_csv('presentation_CNN_predictions.csv', index=False)  # Save predictions to a new CSV file