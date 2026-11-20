from models.profanity_match import ProfanityMatch as pm


class ProfanityService:
    def __init__(
        self,
        classifier,
        forbidden_words,
        threshold,
        label
    ):
        self.classifier = classifier
        self.forbidden_words = {
            w.lower()
            for w in forbidden_words
        }

        self.threshold = threshold
        self.label = label

    def detect(self, words):
        texts = [
            w["text"].strip()
            for w in words
        ]

        predictions = (
            self.classifier.predict(texts)
            if texts
            else []
        )

        matches = []

        for word_info, text, prediction in zip(
            words,
            texts,
            predictions
        ):

            clean = (
                text.lower()
                .strip(".,!?\"'")
            )

            listed = clean in self.forbidden_words

            ai_match = (
                prediction["label"] == self.label
                and prediction["score"] >= self.threshold
            )

            if listed or ai_match:

                start, end = word_info["timestamp"]

                if end is None:
                    end = start + 0.3

                matches.append(
                    pm(
                        word=text,
                        start=start,
                        end=end
                    )
                )

        return matches