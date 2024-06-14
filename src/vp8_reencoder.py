from src.video_reencoder import Video_reencoder
import subprocess

class Vp8_reencoder(Video_reencoder):
    def reencode(self, input_file : str, output_file : str = None):
        if output_file == None:                                     # se nenhum nome de output for indicado, o arquivo somente mudará de extensão
            output_file = input_file.split('.mp4')[0] + '.webm'
        if self.variable_bitrate:
            subprocess.run([
                "ffmpeg",
                "-i", input_file,           # input file
                "-c", "libvpx",             # codec
                "-crf", self.crf,           # crf
                "-t", self.n_threads,       # threads
                "-y",                       # Sobrescrever arquivo de output, se existir
                output_file
            ])
        else:
            subprocess.run([
            "ffmpeg",
            "-i", input_file,           # input file
            "-c", "libvpx-vp9",         # codec
            "-b", self.bit_rate,        # bit rate
            "-crf", self.crf,           # crf
            "-t", self.n_threads,       # threads
            "-y",                       # Sobrescrever arquivo de output, se existir
            output_file
        ])