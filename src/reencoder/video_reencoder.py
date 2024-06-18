from abc import ABC, abstractmethod
import subprocess
import time

class Video_reencoder(ABC):
    def __init__(
        self,
        bit_rate : str = None,
        variable_bitrate : bool = False,
        crf_range : float = None,          # 0 - 100, meaning 100 being best quality, 0 worst quality
        speed : str = None,             # realtime, balanced or quality
        n_threads : int = None,
        t_duration : int = None,
        quiet : bool = False,
        time_out : int = None
        ):

        if crf_range != None:
            if (crf_range < 0 or crf_range > 100):
                raise ValueError('Provide an integer crf value between 0 and 100, 0 being worst quality and 100 best')
        self.crf_range = crf_range

        # Checking for ambiguous configuration
        if bit_rate != None and variable_bitrate == True:
            raise Exception('You can\'t set a fixed "bit_rate" and set a variable bitrate')
        
        # speed treatment
        speed_modes = ('realtime', 'balanced', 'quality')
        if speed != None and speed not in speed_modes:
            raise ValueError(f'Invalid speed mode "{speed}". Available values: {speed_modes}')
        
        self.speed = speed

        self.bit_rate = bit_rate if bit_rate != None else None
        self.variable_bitrate = variable_bitrate

        self.n_threads = str(n_threads) if n_threads != None else None
        self.t_duration = str(t_duration) if t_duration != None else None
        self.timeout = time_out

        self.quiet = quiet

    @abstractmethod
    def reencode(
        self,
        input_file : str,
        output_file : str = None
        ):
        pass

    @property
    @abstractmethod
    def crf(self):
        pass

    @property
    @abstractmethod
    def _speed(self):
        pass

    # Calls ffmpeg and returns if it could be finished
    def reencode(self, input_file : str, output_file : str = None) -> bool:
        ffmpeg_call = self._set_reencode_call(input_file, output_file)
        if not self.quiet:
            print(f'ffmpeg call: {ffmpeg_call}')
        process = subprocess.Popen(ffmpeg_call, shell=True)
        if self.timeout != None:
            try:
                process.wait(self.timeout)
                return True
            except:
                return False
        else:
            return True

    @abstractmethod
    def _set_reencode_call(self, input_file : str, output_file : str = None):
        pass