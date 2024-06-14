import video_downloader
import src.video_reencoder as vr

if __name__ == '__main__':
    # for encode_type in ('h264', 'h264+', 'h265'):
    #     vd = video_downloader.Video_downloader()
    #     vd.download_video(encode_type + '.mp4', 'videos')
    reencoder = vr.Video_reencoder()
    reencoder.reencode()