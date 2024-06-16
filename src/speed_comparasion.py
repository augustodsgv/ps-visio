import src.vp8_reencoder as vp8
import src.vp9_reencoder as vp9
import src.av1_reencoder as av1
import time

def main():
    speeds_infos = {}

    for speed in ('realtime', 'good', 'best'):
        print(f'reencoding with speed {speed}')
        speeds_infos[speed] = {}
        reencoder = vp9.Vp9_reencoder(speed=speed, quiet=True, variable_bitrate=True, t_duration=60)
        i_time = time.time()
        reencoder.reencode('videos/h264_short.mp4', output_file=f'output_videos/h264_vp9_speed_{speed}.mp4')
        f_time = time.time()
        speeds_infos[speed]['time_stemp'] = f_time - i_time

    for speed in speeds_infos.keys():
        print(f'speed {speed} : infos: {speeds_infos[speed]}')

if __name__ == '__main__':
    for i in range(3):
        main()