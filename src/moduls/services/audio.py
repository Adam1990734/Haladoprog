import shutil
import numpy as np
import wave;
import os;

from config import Config as cf
from utils.ffmpeg import run_ffmpeg

class AudioService:
    def __init__(
        self,
        vad_pipeline,
        whisper_pipeline,
        profanity_service,
        censorship_service
    ):
        self.vad = vad_pipeline
        self.whisper = whisper_pipeline

        self.profanity_service = (
            profanity_service
        )

        self.censorship_service = (
            censorship_service
        )

    def _read_wav(self, input_wav):
            with wave.open(input_wav) as w:
                channels = w.getnchannels()
                rate = w.getframerate()
    
                samps = np.frombuffer(
                    w.readframes(w.getnframes()),
                    dtype=np.int16
                )
    
            return samps.reshape(-1, channels), rate, channels

    def extract_speech_segments(
        self,
        audio: np.ndarray
    ):
        timestamps = self.vad(audio)

        if not timestamps:
            return np.array([], dtype=np.float32), []

        audio_chunks = []
        offsets = []

        current_position = 0

        for segment in timestamps:

            start = segment["start"]
            end = segment["end"]

            chunk = audio[start:end]

            audio_chunks.append(chunk)

            offsets.append({
                "new_start": current_position,
                "new_end": current_position + len(chunk),
                "original_start": start
            })

            current_position += len(chunk)

        return (
            np.concatenate(audio_chunks),
            offsets
        )

    def restore_timestamp(
        self,
        sample_index,
        offsets
    ):
        for item in offsets:

            if (
                item["new_start"]
                <= sample_index
                < item["new_end"]
            ):

                return (
                    item["original_start"]
                    + (
                        sample_index
                        - item["new_start"]
                    )
                )

        return None

    def transcribe(
        self,
        speech_audio
    ):
        return self.whisper.transcribe(
            {
                "raw": speech_audio,
                "sampling_rate": 16000
            }
        )

    def remap_word_timestamps(
        self,
        words,
        offsets
    ):
        for word in words:
            start, end = word["timestamp"]

            if start is None:
                continue

            start_sample = int(
                start * 16000
            )

            new_start = (
                self.restore_timestamp(
                    start_sample,
                    offsets
                )
            )

            if new_start is None:
                continue

            if end is not None:

                end_sample = int(
                    end * 16000
                )

                new_end = (
                    self.restore_timestamp(
                        end_sample,
                        offsets
                    )
                )

                if new_end is None:
                    new_end = new_start + 4800

            else:
                new_end = new_start + 4800

            word["timestamp"] = (
                new_start / 16000,
                new_end / 16000
            )
        return words

    def process_audio(
        self,
        original_wav,
        censored_wav,
        mode="beep"
    ):
        speech_wav = os.path.join(cf.TEMP_DIR, "speech.wav")
        run_ffmpeg(
            "-i",
            original_wav,
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            speech_wav
        )

        audio, _, _ = self._read_wav(
            speech_wav
        )

        audio = (
            audio[:, 0] .astype(np.float32) / 32768.0
        )

        speech_audio, offsets = (
            self.extract_speech_segments(
                audio
            )
        )

        if len(speech_audio) == 0:
            return []

        result = self.transcribe(
            speech_audio
        )

        words = result["chunks"]

        words = self.remap_word_timestamps(
            words,
            offsets
        )

        matches = (
            self.profanity_service.detect(
                words
            )
        )

        if not matches:
            shutil.copyfile(
                original_wav,
                censored_wav
            )
            return []

        print(f"Words detected: {len(words)}")
        print(f"Profanity matches: {len(matches)}")

        self.censorship_service.censor(
            original_wav,
            censored_wav,
            [
                (
                    match.start,
                    match.end
                )
                for match in matches
            ],
            mode
        )
        return matches