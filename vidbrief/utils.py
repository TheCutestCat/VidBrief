import os
import yt_dlp

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
    # we make text processed into 1 min text files dict {0 : '...', .... , 23 : '...'}
    import re

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    segments = {}
    current_minute = None
    segment_text = []

    timestamp_pattern = re.compile(r'<\d{2}:\d{2}:\d{2}\.\d{3}><c>|\</c>')
    
    for line in lines:
        line = line.strip()
        if '-->' in line:
            time_range = line.split(' --> ')
            start_time = time_range[0]
            minute = int(start_time.split(':')[1])  # Extract the minute part

            if current_minute is None:
                current_minute = minute

            # If the minute changes, store the current segment and reset
            if minute != current_minute:
                if segment_text:
                    segments[current_minute] = ' '.join(segment_text)
                current_minute = minute
                segment_text = []

        elif line and not line.startswith(('WEBVTT', 'Kind:', 'Language:', 'NOTE')):  # Skip metadata
            # Remove timestamp cues and add cleaned line to segment text
            cleaned_line = re.sub(timestamp_pattern, '', line)
            segment_text.append(cleaned_line)
    # Add the last segment if there's any leftover text
    if segment_text:
        segments[current_minute] = ' '.join(segment_text)
    
    return segments

# 示例使用
if __name__ == "__main__":
    # video_url = "https://www.youtube.com/watch?v=DQacCB9tDaw"  
    # download_video_with_subtitles(video_url)
    ans = extract_segments_from_vtt(file_path='./videos/DQacCB9tDaw.en.vtt')
    total_words = sum(len(text.split()) for text in ans.values())
    print("Total number of words:", total_words)