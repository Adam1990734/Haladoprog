from transformers import pipeline

class WhisperPipeline:
    def __init__(self, model_name):
        self.pipeline = pipeline(
            "automatic-speech-recognition",
            model=model_name,
            chunk_length_s=30
        )

    def transcribe(self, audio):
        print(audio)
        return self.pipeline(
            audio,
            return_timestamps="word"
        )