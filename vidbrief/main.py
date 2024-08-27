from utils import extract_segments_from_vtt,download_video_with_subtitles

import cv2
import os

def extract_frames(video_path, frame_folder):
    # Ensure the frame folder exists
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    frames_dict = {}
    start_time = 0
    frames_sub_dict = {}
    
    success, image = cap.read()
    frame_count = 0

    while success:
        frame_time = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
        
        # Capture the frame every second
        if frame_count % int(fps) == 0:
            image_file = f"{frame_folder}/frame_{frame_time}.jpg"
            cv2.imwrite(image_file, image)  # Save frame as JPEG file
            frames_sub_dict[frame_time] = image_file

            # Every 60 seconds, store the sub-dict into the main dict
            if frame_time > 0 and frame_time % 60 == 0:
                frames_dict[start_time] = frames_sub_dict
                start_time = frame_time + 1
                frames_sub_dict = {}

        success, image = cap.read()
        frame_count += 1

    # Add the remaining frames if they exist
    if frames_sub_dict:
        frames_dict[start_time] = frames_sub_dict

    cap.release()
    return frames_dict

if __name__ == "__main__":
    # Usage Example
    video_file_path = "./video/akeytNVcIy4.mp4"  # Path to downloaded video
    frame_output_folder = "./cache/video_frames/akeytNVcIy4/"  # Folder for storing extracted frames
    frames = extract_frames(video_file_path, frame_output_folder)
    print(frames)

