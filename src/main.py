import src.vp8_reencoder as vp8
import src.vp9_reencoder as vp9
import src.av1_reencoder as av1
import os

def main(): 
    if 'INPUT_FILE_PATH' in os.environ:
       input_file_path = os.environ['INPUT_FILE_PATH'] 
    else:
        input_file_path = "videos/h264_short.mp4"
    
    if 'OUTPUT_FILE_PATH' in os.environ:
       output_file_name = os.environ['OUTPUT_FILE_PATH'] 
    else:
        output_file_name = None

    # input_file_name = file_path.split('/')[-1]
    
    if 'CODEC_DST' in os.environ:
       codec_dst = os.environ['CODEC_DST'] 
    else:
        raise Exception('No codec provided!')

    if codec_dst == 'VP8':
        reencoder = vp8.Vp8_reencoder(variable_bitrate=True)
    elif codec_dst == 'VP9':
        reencoder = vp9.Vp9_reencoder(variable_bitrate=True)    
    elif codec_dst == 'AV1':
        reencoder = av1.Av1_reencoder(variable_bitrate=True)
    else:
        raise Exception(f'Codec /"{codec_dst}/" inválido!')
    
    reencoder.reencode(input_file_path, output_file_name)
        

if __name__ == '__main__':
    main()