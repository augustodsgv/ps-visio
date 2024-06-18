from src.reencoder.video_reencoder import Video_reencoder
import subprocess
import math

class Vp8_reencoder(Video_reencoder):

    def __init__(
        self,
        bit_rate : str = None,
        variable_bitrate : bool = False,
        crf_range : float = None,
        crf : float = None,           # crf. 10 is the recomended standart 
        speed : str = None,         # realtime, good or best
        n_threads : int = None,
        t_duration : int = None,
        quiet : bool = False
        ):
        super().__init__(bit_rate, variable_bitrate, crf_range, speed, n_threads, t_duration, quiet)
        
    @property
    def crf(self):
        # libpx-vp9 accepts crf from 0 to 63. 0 means 63, 100 means 0
        if self.crf_range != None:
            return 63 - math.ceil(59 * (self.crf_range / 100))
        else:
            return None

    @property
    def _speed(self):
        # Speed accepts very delimited inputs
        if self.speed != None:
            # speed_modes = {
            #     'realtime' : 'rt',
            #     'balanced' : 'good',
            #     'quality' : 'best'
            #     }

            speed_modes = {
                'realtime' : 'realtime',
                'balanced' : 'good',
                'quality' : 'best'
            }

            return speed_modes[self.speed]
        else:
            return None
    


    def _set_reencode_call(self, input_file : str, output_file : str = None):
        if output_file == None:                                     # se nenhum nome de output for indicado, o arquivo somente mudará de extensão
            output_file = input_file.split('.mp4')[0] + '.webm'
        
        ffmpeg_call = [
            "ffmpeg",
            "-i", input_file,           # input file
            "-c", "libvpx",             # codec
            "-y",
        ]
        
        if self.bit_rate != None:
            ffmpeg_call.extend(["-b", self.bit_rate])
        
        if self.crf != None:
            ffmpeg_call.extend(["-crf", str(self.crf)])
        
        # speed options: --best, --good, --rt
        if self.speed != None:
            # ffmpeg_call.extend([f"--{self._speed}"])
            ffmpeg_call.extend(["-deadline", self._speed])
        
        if self.n_threads != None:
            ffmpeg_call.extend(["-threads", self.n_threads])
        
        if self.t_duration != None:
            ffmpeg_call.extend(["-t", self.t_duration])
        
        if self.quiet:
            ffmpeg_call.extend(["-hide_banner", "-loglevel", "error"])
        
        ffmpeg_call.append(output_file)
        return ffmpeg_call