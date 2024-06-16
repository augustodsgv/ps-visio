from src.video_reencoder import Video_reencoder
import subprocess

class Vp9_reencoder(Video_reencoder):
    def reencode(self, input_file : str, output_file : str = None):
        if output_file == None:
            output_file = input_file.split('.mp4')[0] + '.webm'

        ffmpeg_call = [
            "ffmpeg",
            "-i", input_file,           # input file
            "-c", "libvpx-vp9",         # codec
            "-y",                       # Sobrescrever arquivo de output, se existir
        ]
        
        if not self.variable_bitrate:
            ffmpeg_call.extend(["-b:v", self.bit_rate, "-minrate", self.bit_rate, "-maxrate", self.bit_rate])
        
        if self.crf != None:
            ffmpeg_call.extend(["-crf", self.crf])
        
        if self.speed != None:
            ffmpeg_call.extend(["-deadline", self.speed])

        if self.n_threads != None:
            ffmpeg_call.extend(["-threads", self.n_threads])
        
        if self.t_duration != None:
            ffmpeg_call.extend(["-t", self.t_duration])

        if self.quiet:
            ffmpeg_call.extend(["-hide_banner", "-loglevel", "error"])


        ffmpeg_call.append(output_file)
        subprocess.run(ffmpeg_call)
