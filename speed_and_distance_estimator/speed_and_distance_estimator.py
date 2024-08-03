import cv2
import sys
import math
sys.path.append('../')
from utils import measure_distance, get_foot_position

class SpeedAndDistanceEstimator:
    def __init__(self, frame_rate=24, frame_window=5):
        self.frame_rate = frame_rate
        self.frame_window = frame_window
        self.total_distance = {}

    def add_speed_and_distance_to_tracks(self, tracks):
        for object, object_tracks in tracks.items():
            if object in ["ball", "referees"]:
                continue
            
            number_of_frames = len(object_tracks)
            for frame_num in range(0, number_of_frames, self.frame_window):
                last_frame = min(frame_num + self.frame_window, number_of_frames - 1)
                for track_id in object_tracks[frame_num]:
                    if track_id not in object_tracks[last_frame]:
                        continue
                    
                    start_position = object_tracks[frame_num][track_id].get('position_transformed')
                    end_position = object_tracks[last_frame][track_id].get('position_transformed')
                    if start_position is None or end_position is None:
                        continue
                    
                    distance_covered = measure_distance(start_position, end_position)
                    time_elapsed = (last_frame - frame_num) / self.frame_rate
                    speed_meters_per_second = distance_covered / time_elapsed
                    speed_km_per_hour = speed_meters_per_second * 3.6
                    
                    if object not in self.total_distance:
                        self.total_distance[object] = {}
                    
                    if track_id not in self.total_distance[object]:
                        self.total_distance[object][track_id] = 0
                    
                    self.total_distance[object][track_id] += distance_covered
                    
                    for frame_num_batch in range(frame_num, last_frame):
                        if track_id not in tracks[object][frame_num_batch]:
                            continue
                        tracks[object][frame_num_batch][track_id]['speed'] = speed_km_per_hour
                        tracks[object][frame_num_batch][track_id]['distance'] = self.total_distance[object][track_id]

    def draw_speed_and_distance(self, frames, tracks):
        output_frames = []
        for frame_num, frame in enumerate(frames):
            for object, object_tracks in tracks.items():
                if object in ["ball", "referees"]:
                    continue 
                for track_id, track_info in object_tracks[frame_num].items():
                    speed = track_info.get('speed')
                    distance = track_info.get('distance')
                    if speed is None or distance is None:
                        continue
                    
                    bbox = track_info['bbox']
                    position = get_foot_position(bbox)
                    position = list(position)
                    position[1] += 40
                    position = tuple(map(int, position))
                    cv2.putText(frame, f"{speed:.2f} km/h", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    cv2.putText(frame, f"{distance:.2f} m", (position[0], position[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            output_frames.append(frame)
        
        return output_frames
