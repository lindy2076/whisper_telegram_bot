import queue
import threading
import logging

q = queue.Queue()


def worker():
    while True:
        cnv = q.get()
        logging.info(f"Q: found {cnv.file_path}, getting. Q size:{q.qsize()}")
        cnv.speech_to_text()
        q.task_done()


threading.Thread(target=worker, daemon=True).start()
