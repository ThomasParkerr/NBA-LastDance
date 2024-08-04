import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
import supervision as sv
import pickle
import os
from sklearn.cluster import KMeans

def read_video(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return []
    
    frames = []
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)
    
    video.release()
    
    if not frames:
        print(f"Warning: No frames were read from {video_path}")
    
    return frames

def save_video(output_video_frames, output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)
    out.release()
