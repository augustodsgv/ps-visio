import subprocess
import pathlib

class Video_reencoder:
    def __init__(self):
        self.reencode_formats = ('VP8', 'VP9', 'AV1')

    def reencode(self, file_name : str, dest_encode : str):
        if not pathlib.Path(file_name).is_file():
            raise Exception(f'File {file_name} does not exists')
        
        if dest_encode not in self.reencode_formats:
            raise Exception(f'Invalide reencode format {dest_encode}\n Available formats: {self.reencode_formats}')
        subprocess.run(['ls', '-l'])