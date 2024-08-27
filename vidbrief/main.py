from utils import extract_segments_from_vtt,\
    download_video_with_subtitles,\
    extract_frames,\
    combine_vtt_and_frames,\
    openai_wrapper,\
    chunk_text
from PromptsAndClass.writing import HighlitsResponseFromat,HighlitsPrompts

from ImageKmeans import get_representative_images_path,group_and_process_frames
import argparse

from CanavaGen import create_layout

if __name__ == "__main__":

    # # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Process a YouTube video URL.')
    parser.add_argument('--url', type=str, required=True, help='Enter the YouTube video URL')
    
    args = parser.parse_args()
    
    # Validate the YouTube URL format
    if 'https://www.youtube.com/watch?v=' not in args.url:
        raise ValueError("Invalid YouTube URL format. It should be like: https://www.youtube.com/watch?v={youtube_id}")
    elif len(args.url) == 11:
        youtube_id = args.url
    else:
        raise ValueError("Invalid input. Please provide a valid YouTube video URL or a YouTube video ID like DQacCB9tDaw.")
    
    # Extract YouTube ID from the given URL
    youtube_id = args.url.split('v=')[1]

    youtube_id = 'DQacCB9tDaw' # example id here

    # youtube video download
    download_video_with_subtitles(youtube_id)

    vtt_result = extract_segments_from_vtt(file_path=f'./videos/{youtube_id}.en.vtt')

    # Usage Example
    video_file_path = f"./videos/{youtube_id}.mp4"  # Path to downloaded video
    frame_output_folder = f"./cache/video_frames/{youtube_id}/"  # Folder for storing extracted frames

    # all is the text result
    total_word_count = 0
    total_text = ""
    for segment in vtt_result.values():
        text_content = segment['text']
        end_time = segment['end_time']
        total_text += f"{end_time} : {text_content}"
        total_word_count += len(text_content.split())
    print(f"input text length : {total_word_count}")


    openai_highlights_result = openai_wrapper(system_messages = HighlitsPrompts,input_messages = total_text,response_format = HighlitsResponseFromat)
    highlights_list = [{"text": item.text, "end_time": item.end_time} for item in openai_highlights_result.highlits]
    print('openai analyse done')

    canava_list = []
    image_target_second_list = []
    # time to picture_path
    for item in highlights_list:
        end_time = item['end_time']
        hours, minutes, seconds = end_time.split(':')
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(float(seconds))

        text = item['text']
        image_path = f'./cache/video_frames/{youtube_id}/frame_{total_seconds}.jpg'
        image_target_second_list.append(total_seconds)
        temp = (text,image_path)
        canava_list.append(temp)
    print(f'we will use the image of {image_target_second_list} second')
    extract_frames(video_file_path, frame_output_folder, target_list = image_target_second_list)
    print('the image extracted')
    output_image = create_layout(canava_list)
    output_image.save(f'./image_gen_{youtube_id}.png')
    print(f'image generated at : ./image_gen_{youtube_id}.png')