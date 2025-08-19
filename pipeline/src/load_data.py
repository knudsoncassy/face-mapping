import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import torch

def load_dataset(csv_path):
    df = pd.read_csv(csv_path)

    # Word encoding
    le = LabelEncoder()
    df['word_encoded'] = le.fit_transform(df['word_label'])

    # MFCCs
    mfcc_cols = [f'mfcc_{i}' for i in range(13)]
    mfccs = df[mfcc_cols].values

    # Normalize MFCCs
    mfcc_scaler = MinMaxScaler()
    mfccs = mfcc_scaler.fit_transform(mfccs)

    # Landmarks
    landmark_cols = [f'{axis}{i}' for i in range(1, 10) for axis in ['x', 'y']]
    landmarks = df[landmark_cols].values
    landmark_scaler = MinMaxScaler()
    landmarks = landmark_scaler.fit_transform(landmarks)

    # Inputs: word + mfccs
    word_encoded = df['word_encoded'].values.reshape(-1, 1)
    inputs = np.hstack([word_encoded, mfccs])

    return torch.tensor(inputs, dtype=torch.float32), torch.tensor(landmarks, dtype=torch.float32), le