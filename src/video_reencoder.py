import subprocess
import pathlib

class Video_reencoder:
    def __init__(self):
        self.reencode_formats = ('VP8', 'VP9', 'AV1')

    def vp8_reencode(self, input_file : str, output_file : str = None):
        if output_file == None:
            output_file = input_file.split('.mp4')[0] + '.webm'
        subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libvpx", "-b:v", "1M", "-c:a", "libvorbis", output_file])

    def vp9_reencode(self, input_file : str, output_file : str = None):
        if output_file == None:
            output_file = input_file.split('.mp4')[0] + '.webm'
        subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libvpx-vp9", "-b:v", "2M", output_file])

    def av1_reencode(self, input_file : str, output_file : str = None):
        if output_file == None:
            output_file = input_file.split('.mp4')[0] + '.mkv'
        subprocess.run(["ffmpeg", "-i", input_file, "-c:v", "libaom-av1", "-crf", "30", output_file])