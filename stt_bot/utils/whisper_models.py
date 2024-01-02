import whisper


class WhiModel():
    def __init__(self, mdl: str):
        self.mdl = mdl
        self.model = whisper.load_model(mdl)

    def change_model(self, new_mdl):
        self.model = whisper.load_model(new_mdl)
        self.mdl = new_mdl


model = WhiModel("small")
