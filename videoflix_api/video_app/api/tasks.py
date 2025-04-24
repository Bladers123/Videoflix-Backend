# video_app/api/tasks.py
import os
import subprocess
import ftplib
from core.ftp_client import FTPClient
 


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


def upload_hls_files(directory, video_folder, video_type):
    ftp_client = FTPClient()
    base_remote_dir = "/" + video_type + "s"

    try:
        ftp_client.connection.cwd(base_remote_dir)
    except ftplib.error_perm:
        try:
            ftp_client.connection.mkd(base_remote_dir)
            ftp_client.connection.cwd(base_remote_dir)
        except Exception as e:
            print(f"Fehler beim Wechseln in {base_remote_dir}: {e}")
            ftp_client.close()
            return

    try:
        ftp_client.connection.mkd(video_folder)
        print(f"Ordner '{video_folder}' erstellt.")
    except ftplib.error_perm:
        print(f"Ordner '{video_folder}' existiert bereits.")

    try:
        ftp_client.connection.cwd(video_folder)
    except Exception as e:
        print(f"Fehler beim Wechseln in {video_folder}: {e}")
        ftp_client.close()
        return

    for filename in os.listdir(directory):
        if (filename.endswith(".m3u8") or filename.endswith(".ts")) and filename.startswith(video_folder):
            local_path = os.path.join(directory, filename)
            remote_filename = os.path.basename(filename)
            ftp_client.upload_file(local_path, remote_filename)
            print(f"{filename} hochgeladen in /movies/{video_folder}/{remote_filename}")

    ftp_client.close()



def generate_master_playlist(directory, base_name):
    master_playlist_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
    
    variants = [
        {"suffix": "_120p", "bandwidth": 800000, "resolution": "160x120"},
        {"suffix": "_360p", "bandwidth": 1400000, "resolution": "640x360"},
        {"suffix": "_720p", "bandwidth": 2800000, "resolution": "1280x720"},
        {"suffix": "_1080p", "bandwidth": 5000000, "resolution": "1920x1080"},
    ]
    
    for variant in variants:
        playlist_filename = f"{base_name}{variant['suffix']}.m3u8"
        master_playlist_content += (
            f"#EXT-X-STREAM-INF:BANDWIDTH={variant['bandwidth']},RESOLUTION={variant['resolution']}\n"
            f"{playlist_filename}\n"
        )
    
    master_playlist_path = os.path.join(directory, "master.m3u8")
    with open(master_playlist_path, "w") as f:
        f.write(master_playlist_content)
    
    print(f"Master-Playlist erstellt: {master_playlist_path}")
    return master_playlist_path



def generate_and_upload_master_playlist(directory, video_folder, base_name, video_type):
    master_playlist_path = generate_master_playlist(directory, base_name)
    
    ftp_client = FTPClient()
    base_remote_dir = "/" + video_type + "s"
    
    try:
        ftp_client.connection.cwd(base_remote_dir)
    except ftplib.error_perm:
        try:
            ftp_client.connection.mkd(base_remote_dir)
            ftp_client.connection.cwd(base_remote_dir)
        except Exception as e:
            print(f"Fehler beim Wechseln in {base_remote_dir}: {e}")
            ftp_client.close()
            return
    
    try:
        ftp_client.connection.mkd(video_folder)
        print(f"Ordner '{video_folder}' erstellt.")
    except ftplib.error_perm:
        print(f"Ordner '{video_folder}' existiert bereits.")
    
    try:
        ftp_client.connection.cwd(video_folder)
    except Exception as e:
        print(f"Fehler beim Wechseln in {video_folder}: {e}")
        ftp_client.close()
        return
    
    try:
        ftp_client.upload_file(master_playlist_path, "master.m3u8")
        print(f"Master-Playlist erfolgreich hochgeladen in {base_remote_dir}/{video_folder}/master.m3u8")
    except Exception as e:
        print(f"Fehler beim Hochladen der Master-Playlist: {e}")
    
    ftp_client.close()


def upload_thumbnail(source, video_folder, video_type, remote_filename=None):
    base_remote_dir = f"/{video_type}s"
    ftp_client = FTPClient()

    try:
        try:
            ftp_client.connection.cwd(base_remote_dir)
        except ftplib.error_perm:
            ftp_client.connection.mkd(base_remote_dir)
            ftp_client.connection.cwd(base_remote_dir)

        try:
            ftp_client.connection.mkd(video_folder)
        except ftplib.error_perm:
            pass 
        ftp_client.connection.cwd(video_folder)

        if remote_filename is None:
            remote_filename = os.path.basename(source)

        ftp_client.upload_file(source, remote_filename)
        print(f"Thumbnail '{source}' erfolgreich hochgeladen als {base_remote_dir}/{video_folder}/{remote_filename}")

    except Exception as e:
        print(f"Fehler beim Hochladen des Thumbnails: {e}")
    finally:
        ftp_client.close()
