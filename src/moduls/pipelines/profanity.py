from transformers import pipeline

class ProfanityClassifier:
    def __init__(self, model_name):
        self.pipeline = pipeline(
            "text-classification",
            model=model_name
        )

    def predict(self, texts):
        return self.pipeline(texts)