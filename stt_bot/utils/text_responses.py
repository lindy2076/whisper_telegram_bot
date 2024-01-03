class Response(str):
    NO_ADMIN = "Sorry, my owner said i shouldn't talk to anyone except him..."
    ADMIN_START = "Hello Mr. Admin!"
    UNKNOWN_FORMAT = "I can't convert this message type. " + \
                     "It is not a voice message, video or video note."
    NO_ADMIN_CALLBACK = "You have absolutely no rights to click these buttons"
    MODEL_LOADING = "Downloading model. Please wait..."
    HELP = "Type /model to select (and download) Whisper model.\n\n" + \
        "Type /help to see this message.\n\n" + \
        "Forward any voice or video note message here. " + \
        "Then wait and select text formatting.\n" + \
        "Github: github.com/lindy2076/whisper_telegram_bot"
    SOMETHING_WRONG = "Something went wrong..."

    @classmethod
    def select_curr_model(cls, mdl: str) -> str:
        return f"Select model!\nCurrent model is *{mdl}*"

    @classmethod
    def new_model_selected(cls, mdl: str) -> str:
        return f"{mdl} model selected!\n" + \
                "This message will disappear in 5 seconds"

    @classmethod
    def stt_response(cls, result, lang: str = None, mdl: str = None) -> str:
        if lang is None and mdl is None:
            return f"{result}"
        return f"{result}\n\nDetected language: {lang}\nModel: {mdl}"
