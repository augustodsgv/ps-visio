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

# Consts
timeout_period = 5

def run_test(src_codec : str, dst_codec : str, input_file : str, output_file : str, reencoder : vr) -> list[str, str, int, float, str, int, int, float]:
    print(output_file)
    time_i = time.time()
    succeded = reencoder.reencode(input_file, output_file)
    time_f = time.time()
    # Timeout
    if not succeded:
        print('test timed out!')
        return [src_codec, dst_codec, bitrate_value, crf, speed, None, None, None, None, None]
    psnr_score, _, _, _ = PSNR.PSNR_validator().compare(input_file, output_file)
    ssim_score, _, _, _ = SSIM.SSIM_validator().compare(input_file, output_file)
    reencoded_size = os.path.getsize(output_file)
    original_video_size = os.path.getsize(input_file)
    size_gain = reencoded_size / original_video_size
    print(f'{dst_codec}, PSNR score: {psnr_score}, SSIM score: {ssim_score}, time: {time_f - time_i}, compacted video size: {reencoded_size}, % original : {size_gain}\n')
    return [src_codec, dst_codec, bitrate_value, crf, speed, time_f - time_i, reencoded_size, size_gain, psnr_score, ssim_score]
    



# Running radom test with the 3 codecs, changing bitrate, crf and speed parameters
if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    data_dir = sys.argv[3]


    # Setting test data structre
    df = pd.DataFrame(columns=['src codec', 'dst codec', 'bitrate (b)', 'crf (%)', 'speed', 'time(s)','compacted size(b)', 'size_gain (%)', 'psnr score', 'ssim_score'])
    df.to_csv(data_dir + '/test_data_2.csv')

    # Each test will be treated as a solo line, identifying the test by the 'src codec' and 'dst codec'
    test_i = 0
    # Choosing bitrate
    for speed in ('good', 'best', 'realtime'):

        # Choosing crf
        for crf in (25, 50, 75):

            for bitrate in {'64k' : 64000, '1M' : 1000000}.items():
                bitrate_str, bitrate_value = bitrate
            
            # Choosing speed / quality
                print(f'Test {test_i} -> bitrate: {bitrate_str}, crf (%): {crf}, speed/quality: {speed}')
                test_i += 1

                # Creating folder to store the videos
                dir = f'{output_dir}/test_{bitrate_str}_{crf}_{speed}'
                Path(dir).mkdir(parents=True, exist_ok=True)

                # building reencoders
                vp8_codec = vp8.Vp8_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, time_out=100, quiet=True, n_threads=4)
                vp9_codec = vp9.Vp9_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=speed, time_out=100, quiet=True, n_threads=4)
                av1_speed_translate = {'realtime' : 'speed', 'good' : 'balanced', 'best' : 'quality'}
                av1_codec = av1.Av1_reencoder(bit_rate=bitrate_str, crf_range=crf, speed=av1_speed_translate[speed], time_out=100, quiet=True, n_threads=4)
                
                # choosing video to compress
                for src_codec in ('h264', 'h264+', 'h265'):
                    curr_test_data = []
                    video = src_codec + '_short.mp4'
                    original_video_size = os.path.getsize(f'{input_dir}/{video}')
                    print(f'Video original = {video}, tamanho: {original_video_size}')

                    # VP8
                    print('vp8')
                    input_file = f'{input_dir}/{video}'
                    output_file = dir + '/' + src_codec + '_vp8.webm'
                    vp8_result = run_test(src_codec, 'vp8', input_file, output_file, vp8_codec)
                    curr_test_data.append(vp8_result)

                    # VP9
                    print('vp9')
                    input_file = f'{input_dir}/{video}'
                    output_file = dir + '/' + src_codec + '_vp9.webm'
                    vp9_result = run_test(src_codec, 'vp9', input_file, output_file, vp9_codec)
                    curr_test_data.append(vp9_result)
                        
                    # AV1
                    print('av1')
                    input_file = f'{input_dir}/{video}'
                    output_file = dir + '/' + src_codec + '_av1.mkv'
                    av1_result = run_test(src_codec, 'av1', input_file, output_file, av1_codec)
                    curr_test_data.append(av1_result)

                    new_df = pd.DataFrame(curr_test_data, columns=['src codec', 'dst codec', 'bitrate (b)', 'crf (%)', 'speed', 'time(s)','compacted size(b)', 'size_gain (%)', 'psnr score', 'ssim_score'])
                    df = pd.concat([df, new_df], ignore_index=True)
                    df.to_csv(data_dir + '/test_data2.csv')

