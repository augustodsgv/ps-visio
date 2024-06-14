from src.video_reencoder import Video_reencoder
import subprocess
    
class Av1_reencoder(Video_reencoder):
    def reencode(self, input_file : str, output_file : str = None):
        if output_file == None:
            output_file = input_file.split('.mp4')[0] + '.mkv'
        if self.variable_bitrate:
            subprocess.run([
                "ffmpeg", 
                "-i", input_file,           # input file
                "-c", "libaom-av1",         # codec
                "-crf", self.crf,           # crf
                "-t", self.n_threads,       # threads
                "-y",                       # Sobrescrever arquivo de output, se existir
                output_file
            ])
        else:
            subprocess.run([
                "ffmpeg", 
                "-i", input_file,           # input file
                "-c", "libaom-av1",         # codec
                "-b", self.bit_rate,        # bit-rate
                "-crf", self.crf,           # crf
                "-t", self.n_threads,       # threads
                "-y",                       # Sobrescrever arquivo de output, se existir
                output_file
            ])
    