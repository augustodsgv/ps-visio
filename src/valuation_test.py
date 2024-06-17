import src.reencoder.vp8_reencoder as vp8
import src.reencoder.vp9_reencoder as vp9
import src.reencoder.av1_reencoder as av1

import src.validator.PSNR_validator as PSNR
import src.validator.SSIM_validator as SSIM

import sys
import random

# Running radom test with the 3 codecs, changing bitrate, crf and speed parameters
if __name__ == '__main__':
    n_tests = 10
    # Choosing random bitrate
    for _ in range(n_tests):
        bitrate_options = {'8k' : 8000, '64k' : 64000, '750K' : 750000, '1M' : 1000000}
        bitrate_str, bitrate_value = random.choice(list(bitrate_options.items()))
    
        # Choosing random crf
        crf = random.randint(0, 100)
        av1_

        # Choosing random speed / quality
        speed = {
            'av1' : ('speed', 'balanced', 'speed'),
            'vp9' : ('realtime', 'good', 'best')
        }