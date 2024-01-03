# Speech-to-text (STT) bot for Telegram

This is a simple speech to text Telegram bot for a single user. Convert voice, video and video notes to text in any language with or without timings locally. Powered by [OpenAI Whisper](https://openai.com/research/whisper) STT model.

The app requires **FFmpeg** to convert videos.

### Quick start
1. Clone the repository: `git clone https://github.com/lindy2076/whisper_telegram_bot`
2. Install all dependencies: `pip install -r requirements.txt`
    
    (~5 GB)
    (and install FFmpeg to convert videos)
3. Create `.env` and provide credentials: `cp .env.sample .env`
4. Run the app: `python3 -m stt_bot`
5. Wait for small Whisper model to be downloaded ( ~460 MB, models are stored in `~/.cache/whisper/`)
6. Forward a voice message or a video note to transcribe.


> Note that this bot is for single use only. Whisper takes some time to convert audios and it requires a lot of computing power.

Transcripts are stored in `tmp/` folder. Filename contains chat_id and message_id so they can be removed by clicking the cleanup button.

### Screenshots

![Screenshot from 2024-01-03 18-42-11](https://github.com/lindy2076/whisper_telegram_bot/assets/67479681/96112da5-8efe-4495-b08a-3a6327b8991a)
![Screenshot from 2024-01-03 18-42-00](https://github.com/lindy2076/whisper_telegram_bot/assets/67479681/6d1e718f-c6b8-44b4-a608-0634721cc338)
![Screenshot from 2024-01-03 18-52-04](https://github.com/lindy2076/whisper_telegram_bot/assets/67479681/c47ae500-4151-444a-9735-c5f4b13be326)
![Screenshot from 2024-01-03 18-51-55](https://github.com/lindy2076/whisper_telegram_bot/assets/67479681/5918bad6-4c20-4120-9869-406f3e258432)
