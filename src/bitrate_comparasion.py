import src.vp8_reencoder as vp8
import src.vp9_reencoder as vp9
import src.av1_reencoder as av1
import time

def main():
    bitrates_infos = {}
    for bitrate in ('8', '64', '1024', '2048', '4096', '8192'):
        print(f'reencoding with bitrate {bitrate}')
        bitrates_infos[bitrate] = {}
        reencoder = vp9.Vp9_reencoder(bit_rate=bitrate, quiet=True)
        i_time = time.time()
        reencoder.reencode('videos/h264_short.mp4', output_file=f'output_videos/h264_vp8_bitrate_{bitrate}.mp4')
        f_time = time.time()
        bitrates_infos[bitrate]['time_stemp'] = f_time - i_time

    for bitrate in bitrates_infos.keys():
        print(f'bitrate {bitrate} : infos: {bitrates_infos[bitrate]}')

if __name__ == '__main__':
    main()