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
