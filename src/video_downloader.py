from google.cloud import storage
from pathlib import Path

class Video_downloader:
    def __init__(self):
        pass

    # Baixa um vídeo do bucket
    def download_video(self, video_name : str, download_path = ''):
        storage.Client.create_anonymous_client()
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(bucket_name='psel_video_samples')
        blob = bucket.blob(video_name)

        # Criando path, caso não exista
        if Path != '':
            Path(download_path).mkdir(parents=True, exist_ok=True)

        blob.download_to_filename(download_path + '/' + video_name)

    def check_downloaded(file_name : str):
        pass
        