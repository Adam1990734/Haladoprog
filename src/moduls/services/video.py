import os

from utils.ffmpeg import run_ffmpeg
from config import Config as cf

class VideoService:
    def __init__(
        self,
        audio_service
    ):
        self.audio_service = audio_service

    def _extract_audio(
        self,
        video_path,
        audio_path
    ):
        run_ffmpeg(
            "-i",
            video_path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            audio_path
        )

    def _replace_audio(
        self,
        video_path,
        audio_path,
        output_path
    ):
        run_ffmpeg(
            "-i",
            video_path,
            "-i",
            audio_path,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            output_path
        )

    def _build_output_path(
        self,
        video_path
    ):
        filename = os.path.splitext(
            os.path.basename(video_path)
        )[0]

        return os.path.join(
            cf.OUTPUT_DIR,
            f"{filename}_censored.mp4"
        )


    def process_video(
        self,
        video_path,
        mode="beep"
    ):
        extracted_audio = os.path.join(
            cf.TEMP_DIR,
            "audio.wav"
        )

        censored_audio = os.path.join(
            cf.TEMP_DIR,
            "censored.wav"
        )

        self._extract_audio(
            video_path,
            extracted_audio
        )

        matches = self.audio_service.process_audio(
            original_wav=extracted_audio,
            censored_wav=censored_audio,
            mode=mode
        )

        output_video = self._build_output_path(
            video_path
        )

        self._replace_audio(
            video_path,
            censored_audio,
            output_video
        )
        return output_video, matches