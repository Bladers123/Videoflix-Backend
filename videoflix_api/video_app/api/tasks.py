# video_app/api/tasks.py
import os
import subprocess
 
""" 
Zerlege den Pfad in Verzeichnis und Dateiname
Erzeuge neue Dateinamen
MP4-Konvertierung für Auflösung X 
HLS-Konvertierung basierend auf der erstellten MP4-Datei
"""

def convert_to_120p(source):
    directory, filename = os.path.split(source)
    name, ext = os.path.splitext(filename)
    
    mp4_target = os.path.join(directory, f"{name}_120p{ext}")
    hls_target = os.path.join(directory, f"{name}_120p.m3u8")
    
    cmd_mp4 = 'ffmpeg -i "{}" -s 160x120 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, mp4_target)
    subprocess.run(cmd_mp4, capture_output=True)
    print('120p: in mp4 umgewandelt')
    
    cmd_hls = 'ffmpeg -i "{}" -c:v copy -c:a aac -ac 2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(mp4_target, hls_target)
    subprocess.run(cmd_hls, capture_output=True)
    print('120p: in hls umgewandelt')


def convert_to_360p(source):
    directory, filename = os.path.split(source)
    name, ext = os.path.splitext(filename)
    
    mp4_target = os.path.join(directory, f"{name}_360p{ext}")
    hls_target = os.path.join(directory, f"{name}_360p.m3u8")
    
    cmd_mp4 = 'ffmpeg -i "{}" -s 640x360 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, mp4_target)
    subprocess.run(cmd_mp4, capture_output=True)
    print('360p: in mp4 umgewandelt')
    
    cmd_hls = 'ffmpeg -i "{}" -c:v copy -c:a aac -ac 2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(mp4_target, hls_target)
    subprocess.run(cmd_hls, capture_output=True)
    print('360p: in hls umgewandelt')


def convert_to_720p(source):
    directory, filename = os.path.split(source)
    name, ext = os.path.splitext(filename)
    
    mp4_target = os.path.join(directory, f"{name}_720p{ext}")
    hls_target = os.path.join(directory, f"{name}_720p.m3u8")
    
    cmd_mp4 = 'ffmpeg -i "{}" -s 1280x720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, mp4_target)
    subprocess.run(cmd_mp4, capture_output=True)
    print('720p: in mp4 umgewandelt')
    
    cmd_hls = 'ffmpeg -i "{}" -c:v copy -c:a aac -ac 2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(mp4_target, hls_target)
    subprocess.run(cmd_hls, capture_output=True)
    print('720p: in hls umgewandelt')


def convert_to_1080p(source):
    directory, filename = os.path.split(source)
    name, ext = os.path.splitext(filename)
    
    mp4_target = os.path.join(directory, f"{name}_1080p{ext}")
    hls_target = os.path.join(directory, f"{name}_1080p.m3u8")
    
    cmd_mp4 = 'ffmpeg -i "{}" -s 1920x1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, mp4_target)
    subprocess.run(cmd_mp4, capture_output=True)
    print('1080p: in mp4 umgewandelt')
    
    cmd_hls = 'ffmpeg -i "{}" -c:v copy -c:a aac -ac 2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{}"'.format(mp4_target, hls_target)
    subprocess.run(cmd_hls, capture_output=True)
    print('1080p: in hls umgewandelt')


