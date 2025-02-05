import ffmpeg

async def get_video_info(video_path):
    probe = ffmpeg.probe(video_path)
    video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
    
    width = int(video_info['width'])
    height = int(video_info['height'])
    duration = int(float(video_info['duration']))
    
    return width, height, duration
