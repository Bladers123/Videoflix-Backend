# video_app/api/tasks.py
import subprocess



def convert_to_480p(source):
    target_file = source + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target_file)
    run = subprocess.run(cmd, capture_output=True)
