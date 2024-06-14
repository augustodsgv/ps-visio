from abc import ABC, abstractmethod


class Video_reencoder(ABC):
    
    def __init__(
        self,
        bit_rate : str = None,
        variable_bitrate : bool = False,
        crf : int = 10,         # crf. 10 is the recomended standart 
        # speed : int = None,     # ??/
        n_threads : int = 2
        ):
        if bit_rate == None and variable_bitrate == False:
            raise Exception('You either have to set "variable_bitrate" to True or set and fixed "bit_rate"')
        self.bit_rate = bit_rate
        self.variable_bitrate = variable_bitrate
        self.crf = str(crf)
        # self.speed = speed
        self.n_threads = str(n_threads)


    @abstractmethod
    def reencode(
        self,
        input_file : str,
        output_file : str = None
        ):
        pass