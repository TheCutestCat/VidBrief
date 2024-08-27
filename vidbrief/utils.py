import os
import yt_dlp
import cv2
import base64
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.duckagi.com/v1/")

def openai_wrapper(system_messages,input_messages,response_format):
    system_messages = {"role": "system", "content": f"{system_messages}"}
    input_messages = {"role": "user", "content": f"{input_messages}"}
    
    messages = [system_messages]
    messages.append(input_messages)
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=response_format,
    )
    completion_result = completion.choices[0].message

    if completion_result.parsed:
        result = completion_result.parsed
        return result
    else:
        print(completion_result.refusal)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def chunk_text(text, chunk_size=600, overlap=100):
    words = text.split()  # 将文本分割成单词列表
    chunks = []  # 用于存储chunk的列表
    start = 0  # 起始位置

    while start < len(words):
        end = start + chunk_size  # 计算chunk的结束位置
        chunk = words[start:end]  # 取出当前的chunk
        chunks.append(" ".join(chunk))  # 将chunk重新组合成字符串并添加到chunks列表
        start = end - overlap  # 为下一个chunk计算新的起始位置

        # 如果剩余单词不足一个chunk，但又大于overlap时，确保不会跳过
        if start + chunk_size > len(words) and start < len(words):
            chunk = words[start:]  # 获取剩余的所有单词
            chunks.append(" ".join(chunk))
            break

    return chunks


def download_video_with_subtitles(video_url, output_path="./videos/%(id)s.%(ext)s"):
    # 解析视频URL以获取视频ID
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_id = info_dict.get("id", "default_id")
    
    # 生成文件名和路径
    output_path = output_path.replace("%(id)s", video_id)
    output_path = output_path.replace("%(ext)s", "mp4")
    
    # 检查文件是否已存在
    if os.path.exists(output_path):
        print(f"File '{output_path}' already exists. Skipping download.")
        return
    
    # 设置yt_dlp的下载选项
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',  # 下载最佳视频和音频，并合并
        'merge_output_format': 'mp4',  # 合并输出格式设置为mp4
        'subtitleslangs': ['en'],  # 下载英语字幕，如果需要其他语言可以修改这里
        'writesubtitles': True,  # 下载字幕
        'writeautomaticsub': True  # 下载自动生成的字幕
    }
    
    # 执行下载
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def extract_segments_from_vtt(file_path):
    import re

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    segments = {}
    current_minute = None
    segment_text = []
    timestamp_pattern = re.compile(r'<\d{2}:\d{2}:\d{2}\.\d{3}><c>|\</c>')

    previous_text = ""

    for line in lines:
        line = line.strip()
        if '-->' in line:
            time_range = line.split(' --> ')
            end_time = time_range[0].strip()
            minute = int(end_time.split(':')[1])  # Extract the minute part

            if current_minute is None:
                current_minute = minute

            # Only store the segment if it matches the specific structure
            if minute != current_minute:
                if segment_text:
                    merged_text = ' '.join(segment_text).strip()
                    if merged_text != previous_text:
                        segments[current_minute] = {
                            'end_time': end_time,
                            'text': merged_text
                        }
                        previous_text = merged_text
                current_minute = minute
                segment_text = []

        elif line and not line.startswith(('WEBVTT', 'Kind:', 'Language:', 'NOTE')):  # Skip metadata
            # Only process lines that match the specific structure format
            if re.search(timestamp_pattern, line):
                cleaned_line = re.sub(timestamp_pattern, '', line).strip()
                segment_text.append(cleaned_line)

    # Add the last segment if there's any leftover text
    if segment_text:
        merged_text = ' '.join(segment_text).strip()
        if merged_text != previous_text:
            segments[current_minute] = {
                'end_time': end_time,
                'text': merged_text
            }

    return segments


def extract_frames(video_path, frame_folder):
    # Ensure the frame folder exists
    if not os.path.exists(frame_folder):
        os.makedirs(frame_folder)

    # Return the list of all files in the frame folder
    if os.listdir(frame_folder):
        return os.listdir(frame_folder)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    saved_image_files = []
    
    success, image = cap.read()
    frame_count = 0

    while success:
        frame_time = int(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)
        
        # Capture the frame every second
        if frame_count % int(fps) == 0:
            image_file = f"{frame_folder}/frame_{frame_time}.jpg"
            cv2.imwrite(image_file, image)  # Save frame as JPEG file
            saved_image_files.append(image_file)

        success, image = cap.read()
        frame_count += 1

    cap.release()
    return saved_image_files

def combine_vtt_and_frames(vtt_result, key_frame_result):
    # Extract the frame index from each key_frame_result path and sort the key_frame_result
    sorted_key_frames = sorted(key_frame_result, key=lambda path: int(path.split('_')[-1].split('.')[0]))

    combined_result = []

    # Initialize the previous index
    prev_index = None

    for frame_path in sorted_key_frames:
        # Extract the current frame index
        current_index = int(frame_path.split('_')[-1].split('.')[0])

        # Determine the start of the current segment in vtt_result
        if prev_index is not None:
            start_time = prev_index // 60
        else:
            start_time = 0

        # Determine the end of the current segment in vtt_result
        end_time = current_index // 60

        # Create a tuple consisting of frame path and the corresponding vtt_result segment(s)
        segment = [vtt_result.get(i, '') for i in range(start_time, end_time + 1)] # this should get improved here
        combined_result.append((frame_path, segment))

        # Update the previous index
        prev_index = current_index

    return combined_result




# 示例使用
if __name__ == "__main__":
    # video_url = "https://www.youtube.com/watch?v=DQacCB9tDaw"  
    # download_video_with_subtitles(video_url)
    ans = extract_segments_from_vtt(file_path='./videos/DQacCB9tDaw.en.vtt')
    total_words = sum(len(text.split()) for text in ans.values())
    print("Total number of words:", total_words)