def main(video_path, model_path, output_video_path):
    tracker = Tracker(model_path)
    video_frames = read_video(video_path)
    
    if not video_frames:
        print("Error: No frames were read from the video.")
        return

    tracks = tracker.get_object_tracks(video_frames)
    tracker.add_position_to_tracks(tracks)
    
    # Assign team colors
    tracker.team_assigner.assign_team_color(video_frames[0], tracks["players"][0])
    
    annotated_frames = tracker.draw_annotations(video_frames, tracks)
    save_video(annotated_frames, output_video_path)

if __name__ == "__main__":
    video_path = "input videos/1.mp4"
    model_path = "models/yolov8_trained_best_model.pt"
    output_video_path = "output_videos/video.mp4"
    main(video_path, model_path, output_video_path)
