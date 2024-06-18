import src.reencoder.vp8_reencoder as vp8
import src.reencoder.vp9_reencoder as vp9
import src.reencoder.av1_reencoder as av1

import src.validator.PSNR_validator as PSNR
import src.validator.SSIM_validator as SSIM

import os
from pathlib import Path
import sys
import time
import pandas as pd

# Running radom test with the 3 codecs, changing bitrate, crf and speed parameters
if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    data_dir = sys.argv[3]
    # Setting test data structre
    tests_data = []
    # Each test will be treated as a solo line, identifying the test by the 'src codec' and 'dst codec'
    test_i = 0
    # Choosing bitrate
    for bitrate in {'8k' : 8000, '64k' : 64000, '750K' : 750000, '1M' : 1000000}.items():
        bitrate_str, bitrate_value = bitrate

        # Choosing crf
        for crf in range(0, 100, 10):
            
            # Choosing speed / quality
            for speed in ('quality', 'balanced', 'realtime'):
                print(f'Test {test_i} -> bitrate: {bitrate_str}, crf (%): {crf}, speed/quality: {speed}')
                test_i += 1

                # Creating folder to store the videos
                dir = f'{output_dir}/test_{bitrate}_{crf}_{speed}'
                Path.mkdir(dir)

                # building reencoders
                vp8_codec = vp8.Vp8_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, quiet=True)
                vp9_codec = vp9.Vp9_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, quiet=True)
                av1_codec = av1.Av1_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, quiet=True)
                
                # choosing video to compress
                for src_codec in ('h264', 'h264+', 'h265'):
                    video = src_codec + '_short.mp4'
                    original_video_size = os.path.getsize(f'{input_dir}/{video}.mp4')
                    print(f'Video original = {video}, tamanho: {original_video_size}')
                    
                    # VP8
                    time_i = time.time()
                    vp8_codec.reencode(f'{input_dir}/{video}.mp4', dir + '_vp8.webm')
                    time_f = time.time()
                    psnr_score, _, _, _ = PSNR.PSNR_validator().compare(f'{input_dir}/{video}.mp4',dir + '_vp8.webm')
                    ssim_score, _, _, _ = SSIM.SSIM_validator().compare(f'{input_dir}/{video}.mp4',dir + '_vp8.webm')
                    video_size = os.path.getsize(dir + '_vp8.webm')
                    size_gain = video_size / original_video_size
                    print(f'vp8 time: {time_f - time_i}, PSNR score: {psnr_score}, SSIM score: {ssim_score}, compacted video size: {video_size}, % original : {size_gain}\n')
                    tests_data.append([src_codec, 'vp8', bitrate_value, crf, speed, size_gain])

                    # VP9
                    time_i = time.time()
                    vp9_codec.reencode(f'{input_dir}/{video}.mp4', dir + '_vp9.webm')
                    time_f = time.time()
                    psnr_score, _, _, _ = PSNR.PSNR_validator().compare(f'{input_dir}/{video}.mp4',dir + '_vp9.webm')
                    ssim_score, _, _, _ = SSIM.SSIM_validator().compare(f'{input_dir}/{video}.mp4',dir + '_vp9.webm')
                    video_size = os.path.getsize(dir + '_vp9.webm')
                    size_gain = video_size / original_video_size
                    print(f'vp9 time: {time_f - time_i}, PSNR score: {psnr_score}, SSIM score: {ssim_score}, compacted video size: {video_size}, % original : {size_gain}\n')
                    tests_data.append([src_codec, 'vp9', bitrate_value, crf, speed, size_gain])

                    # AV1
                    time_i = time.time()
                    av1_codec.reencode(f'{input_dir}/{video}.mp4', dir + '_av1.webm')
                    time_f = time.time()
                    psnr_score, _, _, _ = PSNR.PSNR_validator().compare(f'{input_dir}/{video}.mp4',dir + '_av1.webm')
                    ssim_score, _, _, _ = SSIM.SSIM_validator().compare(f'{input_dir}/{video}.mp4',dir + '_av1.webm')
                    video_size = os.path.getsize(dir + '_av1.webm')
                    size_gain = video_size / original_video_size
                    print(f'av1 time: {time_f - time_i}, PSNR score: {psnr_score}, SSIM score: {ssim_score}, compacted video size: {video_size}, % original : {size_gain}\n')
                    tests_data.append([src_codec, 'av1', bitrate_value, crf, speed, size_gain])
    
    df = pd.DataFrame(data=tests_data, columns=['src codec', 'dst codec', 'bitrate (b)', 'crf (%)', 'speed(s)', 'size_gain (%)'])
    df.to_csv(data_dir + '/tests_data.csv')