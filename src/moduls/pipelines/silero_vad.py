import numpy as np
import torch

from silero_vad import load_silero_vad, get_speech_timestamps

class SileroVADPipeline:
    def __init__(self):
        super().__init__(
            model=load_silero_vad(),
            tokenizer=None,
            feature_extractor=None
        )

    def __init__(self):
        self.model = load_silero_vad()

    def __call__(
        self,
        audio: np.ndarray
    ):
        audio_tensor = (
            torch.from_numpy(audio)
            if isinstance(audio, np.ndarray)
            else audio
        )

        return get_speech_timestamps(
            audio_tensor,
            self.model,
            sampling_rate=16000
        )