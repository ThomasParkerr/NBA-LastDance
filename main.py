from utils import read_video, save_video
from trackers import Tracker
import cv2

def main():
    # Read Video
    video_frames = read_video('input videos/1.mp4')

    tracker = Tracker('models/yolov8_trained_best_model.pt')
    tracks = tracker.get_object_tracks(video_frames,
                                       read_from_stub=True,
                                       stub_path='stubs/track_stubs.pkl')

    #for track_id, player in tracks['players'][0].items():
       # bbox = player['bbox']
        #frame = video_frames[0]
        
        #cropped bbox from frame
        #cropped_image = frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

        #cv2.imwrite(f'output_videos/cropped_img.jpg', cropped_image)

    output_videos_frames = tracker.draw_annotations(video_frames, tracks)
    
    # Save video
    save_video(video_frames, 'output_videos/output_video.avi')

if __name__ == '__main__':
    main()
