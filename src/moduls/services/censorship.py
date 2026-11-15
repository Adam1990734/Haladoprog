import wave
import numpy as np


class CensorshipService:
    def _write_wav(
        self,
        file_path,
        audio,
        sample_rate,
        channels
    ):
        with wave.open(file_path, "wb") as wav:
            wav.setnchannels(channels)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)

            wav.writeframes(audio.tobytes())

    def _read_wav(self, input_wav):
        with wave.open(input_wav) as w:
            channels = w.getnchannels()
            rate = w.getframerate()

            samps = np.frombuffer(
                w.readframes(w.getnframes()),
                dtype=np.int16
            )

        return samps.reshape(-1, channels), rate, channels

    def _apply_beep(
        self,
        audio,
        a,
        b,
        rate,
        channels
    ):
        t = np.arange(b - a) / rate
        beep = (
            0.25
            * 32767
            * np.sin(2 * np.pi * 1000 * t)
        ).astype(np.int16)

        beep = np.repeat(
            beep[:, np.newaxis],
            channels,
            axis=1
        )

        audio[a:b] = beep

    def censor(
        self,
        input_wav,
        output_wav,
        ranges,
        mode="beep"
    ):
        audio, rate, channels = self._read_wav(
            input_wav
        )

        audio = audio.copy()

        for start, end in ranges:

            a = int(
                max(0, start - 0.05)
                * rate
            )

            b = min(
                len(audio),
                int((end + 0.05) * rate)
            )

            if b <= a:
                continue

            if mode == "mute":
                audio[a:b] = 0

            else:
                self._apply_beep(
                    audio,
                    a,
                    b,
                    rate,
                    channels
                )

        self._write_wav(
            output_wav,
            audio,
            rate,
            channels
        )