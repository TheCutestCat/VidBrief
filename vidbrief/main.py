from utils import extract_segments_from_vtt,\
    download_video_with_subtitles,\
    extract_frames,\
    combine_vtt_and_frames,\
    openai_wrapper,\
    chunk_text
from PromptsAndClass.writing import SummaryResponseFromat,SummaryPrompts

from ImageKmeans import get_representative_images_path,group_and_process_frames
from test_image_gen import create_movie_layout
if __name__ == "__main__":

    vtt_result = extract_segments_from_vtt(file_path='./videos/DQacCB9tDaw.en.vtt')

    # Usage Example
    # video_file_path = "./videos/DQacCB9tDaw.mp4"  # Path to downloaded video
    # frame_output_folder = "./cache/video_frames/akeytNVcIy4/"  # Folder for storing extracted frames
    # frames = extract_frames(video_file_path, frame_output_folder)

    # key_frame_result = group_and_process_frames(frame_output_folder)

    # key_frame_result = ['./cache/video_frames/akeytNVcIy4/frame_695.jpg', './cache/video_frames/akeytNVcIy4/frame_1161.jpg', './cache/video_frames/akeytNVcIy4/frame_728.jpg', './cache/video_frames/akeytNVcIy4/frame_292.jpg', './cache/video_frames/akeytNVcIy4/frame_594.jpg', './cache/video_frames/akeytNVcIy4/frame_1459.jpg', './cache/video_frames/akeytNVcIy4/frame_1393.jpg', './cache/video_frames/akeytNVcIy4/frame_1557.jpg', './cache/video_frames/akeytNVcIy4/frame_243.jpg', './cache/video_frames/akeytNVcIy4/frame_230.jpg']

    # combined_result = combine_vtt_and_frames(vtt_result, key_frame_result) # [{picture_path : ['text_1','text_2']}]

    # all is the text result
    total_word_count = 0
    total_text = ""
    for segment in vtt_result.values():
        text_content = segment['text']
        end_time = segment['end_time']
        total_text += f"{end_time} : {text_content}"
        total_word_count += len(text_content.split())

    # At this point, `total_word_count` is the total number of words across all text segments.
    # You can either use this value later or print it out to verify the results.
    print(total_word_count)

    # ans = openai_wrapper(system_messages = SummaryPrompts,input_messages = total_text,response_format = SummaryResponseFromat)

    # highlights_list = [{"text": item.text, "end_time": item.end_time} for item in ans.highlits]

    highlights_list = [{'text': "Introduction of CHBT's desktop version and new flagship model GBT-4, making advanced AI tools freely available.", 'end_time': '00:02:03.270'}, {'text': 'GBT-4, faster and more efficient, integrates voice, text, and vision for enhanced interaction and is available to free users.', 'end_time': '00:06:01.430'}, {'text': 'Introduction of real-time conversational speech capabilities and efforts for safety with GBT-4.', 'end_time': '00:10:00.389'}, {'text': "Live demo showcasing GBT-4's emotional and voice modulation capabilities.", 'end_time': '00:13:01.670'}, {'text': 'Demo of vision and coding capabilities, supporting interaction with video and solving code-related tasks.', 'end_time': '00:19:00.029'}]

    canava_list = []
    # time to picture_path
    for item in highlights_list:
        end_time = item['end_time']
        hours, minutes, seconds = end_time.split(':')
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(float(seconds))

        text = item['text']
        image_path = f'./cache/video_frames/akeytNVcIy4/frame_{total_seconds}.jpg'

        temp = (text,image_path)
        canava_list.append(temp)
        canava_list.append(temp)

    output_image = create_movie_layout(canava_list)
    output_image.save('output.png')