from utils import read_video, save_video

def main():
    # Read Video
    video_frames = read_video('input_videos/08fd33_4.mp4')

    # Save video
    save_video(output_video_frames, 'output_videos/output_video.avi')

if __name__ == '__main__':
    main()
