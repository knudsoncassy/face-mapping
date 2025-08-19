import os
import cv2
import librosa
import pandas as pd
import subprocess
from moviepy.editor import VideoFileClip

# === CONFIG ===
VIDEO_PATH = 'input.mp4'
FRAME_DIR = 'frames'
AUDIO_DIR = 'audio_chunks'
EXCEL_OUT = 'video_data.xlsx'
FPS = 24
SR = 16000  # audio sample rate
N_MFCC = 13

os.makedirs(FRAME_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# === STEP 1: Extract Frames ===
def extract_frames(video_path, frame_dir, fps):
    subprocess.run([
        'ffmpeg', '-i', video_path,
        '-vf', f'fps={fps}',
        f'{frame_dir}/frame_%04d.png'
    ])

# === STEP 2: Extract Audio and Chunk ===
def extract_audio_chunks(video_path, audio_dir, fps):
    subprocess.run([
        'ffmpeg', '-i', video_path,
        '-ar', str(SR),
        '-f', 'segment',
        '-segment_time', f'{1/fps:.5f}',
        '-c', 'copy',
        f'{audio_dir}/frame_%04d.wav'
    ])

# === STEP 3: Extract MFCCs ===
def extract_mfcc(path, sr=SR, n_mfcc=N_MFCC):
    y, sr = librosa.load(path, sr=sr)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc.mean(axis=1)

# === STEP 4: Build Excel Sheet ===
def build_excel(frame_dir, audio_dir):
    rows = []
    frame_files = sorted(os.listdir(frame_dir))
    audio_files = sorted(os.listdir(audio_dir))

    for i, (f_img, f_audio) in enumerate(zip(frame_files, audio_files)):
        mfcc = extract_mfcc(os.path.join(audio_dir, f_audio))
        row = {
            'frame_number': i,
            'filename': f_img,
            'audio_chunk_path': f_audio,
        }
        for j, val in enumerate(mfcc):
            row[f'mfcc_{j}'] = val
        # Placeholder for landmarks and word label
        row['word'] = ''
        row['mouth_corner_left'] = ''
        row['mouth_corner_right'] = ''
        row['lip_top_center'] = ''
        row['lip_bottom_center'] = ''
        row['jaw_left'] = ''
        row['jaw_right'] = ''
        row['nose_tip'] = ''
        row['eye_corner_left'] = ''
        row['eye_corner_right'] = ''
        row['mouth_open'] = ''
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(EXCEL_OUT, index=False)
    print(f"✅ Excel sheet saved to {EXCEL_OUT}")

# === RUN ALL ===
extract_frames(VIDEO_PATH, FRAME_DIR, FPS)
extract_audio_chunks(VIDEO_PATH, AUDIO_DIR, FPS)
build_excel(FRAME_DIR, AUDIO_DIR)