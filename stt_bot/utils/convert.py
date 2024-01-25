import asyncio
import datetime
import subprocess
import logging
from os import remove

from .text_responses import Response
from .queue import q


FMT_SEPARATOR = "///---***???"


def try_remove(filename) -> bool:
    try:
        remove(filename)
    except Exception as e:
        logging.info(f"failed to remove {filename}. {e}")
        return False
    logging.info(f"{filename} removed")
    return True


class Converter():
    def __init__(self, file_path, whisper_model,
                 msg_id, is_video: bool = False):
        self.file_path = file_path
        self.whisper_model = whisper_model
        self.msg_id = msg_id
        self.is_video = is_video
        self.converted = False
        self.result = None

    def speech_to_text(self) -> tuple[str, str]:
        """
        get transcription and detected language
        + save transcripts to file named *msg_id*.txt
        """
        if self.is_video:
            new_path = self.file_path.replace(".mp4", ".wav")
            subprocess.run(
                ["ffmpeg", "-i", self.file_path, new_path,
                 "-loglevel", "quiet"]
            )
            logging.info(f"video {self.file_path} converted to .wav")
            self.cleanup()
            self.file_path = new_path
        res = self.whisper_model.model.transcribe(self.file_path)
        logging.info(f"audio {self.file_path} transcribed")
        self.cleanup()

        with open(f"tmp/{self.msg_id}.txt", 'w') as f:
            fmted_res = Response.stt_response(
                res["text"], res["language"], self.whisper_model.mdl
            )
            f.write(fmted_res + FMT_SEPARATOR + self.parse_timings(res))
        self.converted = True
        self.result = res["text"], res["language"]

    def cleanup(self):
        """remove file associated with the converter"""
        try_remove(self.file_path)

    def parse_timings(self, dict_: str) -> str:
        """parse timings from res"""
        segments = dict_["segments"]

        res = ""
        for segment in segments:
            s, e = segment['start'], segment['end']
            s_fmted = str(datetime.timedelta(seconds=int(s)))
            e_fmted = str(datetime.timedelta(seconds=int(e)))
            res += f"( {s_fmted} -> {e_fmted} ): {segment['text']}\n"

        return Response.stt_response(
            res, dict_['language'], self.whisper_model.mdl
        )


def read_from_file(filename: str, fmt: str) -> str:
    with open(filename, 'r') as f:
        res = "".join(f.readlines())
    if fmt == "text":
        return res.split(FMT_SEPARATOR)[0]
    elif fmt == "timings":
        return res.split(FMT_SEPARATOR)[1]


async def add_to_q_and_convert(cnv: Converter):
    """
    Call cnv.speech_to_text and await for answer.
    This method puts cnv in queue.Queue and waits
    for it to be processed.
    """
    # complete shit but it works, not blocking the main event

    q.put(cnv)
    logging.info(f"{cnv.file_path} added to q")
    while not cnv.result:
        await asyncio.sleep(1)
    logging.info(f"{cnv.file_path} awaited and returned")
    return cnv.result
