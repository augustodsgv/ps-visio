import src.video_reencoder as vr
import os

def main(): 
    if 'INPUT_FILE_PATH' in os.environ:
       file_path = os.environ['INPUT_FILE_PATH'] 
    else:
        file_path = "videos/h264_short.mp4"
        print(f'WARNING: no file provided, using default: /"{file_path}/"')
    file_name = file_path.split('/')[-1]

    encode_dst = os.environ['ENCODE_DST']
    reencoder = vr.Video_reencoder()
    if encode_dst == 'VP8':
        print(f'Encoding {file_name} to VP8')
        reencoder.vp8_reencode(file_path)
    elif encode_dst == 'VP9':
        print(f'Encoding {file_name} to VP9')
        reencoder.vp9_reencode(file_path)
    elif encode_dst == 'AV1':
        print(f'Encoding {file_name} to AV1')
        reencoder.av1_reencode(file_path)


if __name__ == '__main__':
    main()