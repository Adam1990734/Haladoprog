from config import Config as cf

from utils.folder import create_base

from pipelines.silero_vad import SileroVADPipeline
from pipelines.whisper import WhisperPipeline
from pipelines.profanity import ProfanityClassifier

from services.profanity import ProfanityService
from services.censorship import CensorshipService
from services.audio import AudioService
from services.video import VideoService

class VideoCensoreFactory:
    @staticmethod
    def create_video_service():
        vad = SileroVADPipeline()

        whisper = WhisperPipeline(
            cf.ASR_MODEL
        )

        classifier = ProfanityClassifier(
            cf.PROFANITY_MODEL
        )

        profanity_service = ProfanityService(
            classifier= classifier,
            forbidden_words= cf.FORBIDDEN_WORDS,
            threshold= cf.PROFANITY_THRESHOLD,
            label= cf.PROFANITY_LABEL
        )

        censorship_service = CensorshipService()

        audio_service = AudioService(
            vad_pipeline= vad,
            whisper_pipeline= whisper,
            profanity_service= profanity_service,
            censorship_service= censorship_service
        )

        return VideoService(
            audio_service= audio_service
        )