import subprocess
import logging
from os import remove

import whisper


# class Converter():
#     def __init__(self, file_path, whisper_model: str = "small", language: str = 'ru', output_formats: list[str] = ["txt"]):
#         self.file_path = file_path
#         self.language = language
#         self.whisper_model = whisper_model
#         self.output_formats = output_formats
    
#     def speech_to_text(self) -> str:
#         # res = self.whisper_model.transcribe(self.file_path)
#         r = subprocess.run(
#             ["whisper", self.file_path, 
#              "--model", self.whisper_model, 
#              "--output_format", f"{' '.join(self.output_formats)}", 
#              "--language", self.language,
#              "--output_dir", "tmp/"
#              ]
#         )
#         with open(self.file_path.replace(".ogg", ".txt"), 'r') as f:
#             return "".join(f.readlines())

#     def cleanup(self):
#         remove(self.file_path)
#         for fmt in self.output_formats:
#             remove(self.file_path.replace(".ogg", f".{fmt}"))


class Converter():
    def __init__(self, file_path, whisper_model, is_video: bool = False):
        self.file_path = file_path
        self.whisper_model = whisper_model
        self.is_video = is_video

    def speech_to_text(self) -> tuple[str, str]:
        if self.is_video:
            new_path = self.file_path.replace(".mp4", ".wav")
            subprocess.run(
                ["ffmpeg", "-i", self.file_path, new_path, "-loglevel", "quiet"]
            )
            logging.info(f"video {self.file_path} converted to .wav")
            self.cleanup()
            self.file_path = new_path
        res = self.whisper_model.transcribe(self.file_path)
        logging.info(f"audio {self.file_path} transcribed")
        return res["text"], res["language"]
        
    def cleanup(self):
        remove(self.file_path)
