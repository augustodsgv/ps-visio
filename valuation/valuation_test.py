import src.reencoder.vp8_reencoder as vp8
import src.reencoder.vp9_reencoder as vp9
import src.reencoder.av1_reencoder as av1
import src.reencoder.video_reencoder as vr

import src.validator.PSNR_validator as PSNR
import src.validator.SSIM_validator as SSIM

import os
from pathlib import Path
import sys
import time
import pandas as pd
import threading

# Consts
timeout_period = 5

# def run_test(code_name : str, input_file : str, output_file : str, reencoder : vr) -> list[str, str, int, float, str, float]:
#     time_i = time.time()
#     reencoder.reencode(input_file, output_file)
#     time_f = time.time()
#     psnr_score, _, _, _ = PSNR.PSNR_validator().compare(input_file, output_file)
#     ssim_score, _, _, _ = SSIM.SSIM_validator().compare(input_file, output_file)
#     video_size = os.path.getsize(output_file)
#     size_gain = video_size / original_video_size
#     print(f'{code_name} time: {time_f - time_i}, PSNR score: {psnr_score}, SSIM score: {ssim_score}, compacted video size: {video_size}, % original : {size_gain}\n')
#     return [src_codec, code_name, bitrate_value, crf, speed, size_gain]

def run_test(code_name : str, input_file : str, output_file : str, reencoder : vr) -> list[str, str, int, float, str, float]:
    time.sleep(10)
    return 'banana'

def run_test_1(code_name : str, input_file : str, output_file : str, reencoder : vr) -> list[str, str, int, float, str, float]:
    time.sleep(2)
    return 'pineaple'

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

                # # Creating folder to store the videos
                # dir = f'{output_dir}/test_{bitrate}_{crf}_{speed}'
                # Path.mkdir(dir)

                # building reencoders
                vp8_codec = vp8.Vp8_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, quiet=True)
                vp9_codec = vp9.Vp9_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, quiet=True)
                av1_codec = av1.Av1_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, quiet=True)
                
                # choosing video to compress
                for src_codec in ('h264', 'h264+', 'h265'):
                    video = src_codec + '_short.mp4'
                    # original_video_size = os.path.getsize(f'{input_dir}/{video}.mp4')
                    # print(f'Video original = {video}, tamanho: {original_video_size}')
                    
                    # VP8
                    input_file = f'{input_dir}/{video}.mp4'
                    output_file = output_dir + '/' + src_codec + '_vp8.webm'
                    t = threading.Thread(target=run_test, args=('vp8', input_file, output_file, vp8_codec))
                    t.start()
                    test_results = t.join(timeout=timeout_period)
                    # Thread time_outed
                    if t.is_alive():
                        print('Test vp8 timeout! Saving no data')
                    else:
                        tests_data.append(test_results)

                    # # VP9
                    # input_file = f'{input_dir}/{video}.mp4'
                    # output_file = dir + '_vp9.webm'
                    # test_results = run_test('vp9', input_file, output_file, vp8_codec)
                    # tests_data.append(test_results)
                    # VP8
                    input_file = f'{input_dir}/{video}.mp4'
                    output_file = output_dir + '/' + src_codec + '_vp8.webm'
                    t1 = threading.Thread(target=run_test_1, args=('vp8', input_file, output_file, vp8_codec))
                    t1.start()
                    test_results = t.join(timeout=timeout_period)
                    # Thread time_outed
                    if t1.is_alive():
                        print('Test vp9 timeout! Saving no data')
                    else:
                        print('não deu timeout!')
                        tests_data.append(test_results)
                    # # AV1
                    # input_file = f'{input_dir}/{video}.mp4'
                    # output_file = dir + '_av1.mkv'
                    # test_results = run_test('vp9', input_file, output_file, vp8_codec)
                    # tests_data.append(test_results)

    df = pd.DataFrame(data=tests_data, columns=['src codec', 'dst codec', 'bitrate (b)', 'crf (%)', 'speed(s)', 'size_gain (%)'])
    df.to_csv(data_dir + '/tests_data.csv')