from src.reencoder.video_reencoder import Video_reencoder
import subprocess
import math

class Vp9_reencoder(Video_reencoder):
    def __init__(
        self,
        bit_rate : str = None,
        variable_bitrate : bool = False,
        crf_range : float = None,           # crf. 10 is the recomended standart 
        speed : str = None,         # realtime, good or best
        n_threads : int = None,
        t_duration : int = None,
        quiet : bool = False,
        time_out : bool = False
        ):
        super().__init__(bit_rate, variable_bitrate, crf_range, speed, n_threads, t_duration, quiet, time_out)

    @property
    def crf(self):
        # libpx-vp9 accepts crf from 0 to 63. 0 means 63, 100 means 0
        if self.crf_range != None:
            return 63 - math.ceil(63 * (self.crf_range / 100))
        else:
            return None
        
    @property
    def _speed(self):
        # Speed accepts very delimited inputs
        if self.speed != None:
            speed_modes = {
                'realtime' : 'realtime',
                'balanced' : 'good',
                'quality' : 'best'
            }
            return speed_modes[self.speed]
        else:
            return None
    
    def _set_reencode_call(self, input_file : str, output_file : str = None):
        if output_file == None:
            output_file = input_file.split('.mp4')[0] + '.webm'

        ffmpeg_call = [
            "ffmpeg",
            "-i", input_file,           # input file
            "-c:v", "libvpx-vp9",       # video codec
            "-c:a", "libopus",          # audio codec
            "-y",                       # Sobrescrever arquivo de output, se existir
        ]
        
        if self.bit_rate != None:
            # WARN: this is hardcoded
            ffmpeg_call.extend(["-b:v", self.bit_rate, "-minrate", self.bit_rate, "-maxrate", self.bit_rate])
        
        if self.crf != None:
            ffmpeg_call.extend(["-crf", str(self.crf)])
        
        # -deadline realtime, -deadline good, -deadline best
        if self.speed != None:
            ffmpeg_call.extend(["-deadline", self._speed])

        if self.n_threads != None:
            ffmpeg_call.extend(["-threads", self.n_threads])
        
        if self.t_duration != None:
            ffmpeg_call.extend(["-t", self.t_duration])

        if self.quiet:
            ffmpeg_call.extend(["-hide_banner", "-loglevel", "error"])

        ffmpeg_call.append(output_file)
        return ffmpeg_call
