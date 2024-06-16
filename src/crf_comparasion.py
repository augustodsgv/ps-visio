import src.vp8_reencoder as vp8
import src.vp9_reencoder as vp9
import src.av1_reencoder as av1
import time

def main():
    CRFs_infos = {}
    for CRF in range(0, 51, 13):
        print(f'reencoding with CRF {CRF}')
        CRFs_infos[CRF] = {}
        reencoder = vp9.Vp9_reencoder(crf=CRF, quiet=True, variable_bitrate=True)
        i_time = time.time()
        reencoder.reencode('videos/h264_short.mp4', output_file=f'output_videos/h264_vp9_CRF_{CRF}.mp4')
        f_time = time.time()
        CRFs_infos[CRF]['time_stemp'] = f_time - i_time

    for CRF in CRFs_infos.keys():
        print(f'CRF {CRF} : infos: {CRFs_infos[CRF]}')

if __name__ == '__main__':
    main()