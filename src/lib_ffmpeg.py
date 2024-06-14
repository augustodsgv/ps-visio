# from ffmpeg import FFmpeg
import subprocess

def vp8_reencode(input_file : str, output_file : str = None):
    if output_file == None:
        output_file = input_file.split('.mp4')[0] + '.webm'
    subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libvpx-vp9", "-b:v", "2M", output_file])