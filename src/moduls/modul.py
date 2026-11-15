<<<<<<< HEAD
import os
import subprocess
import tempfile
import wave

import imageio_ffmpeg          # a moviepy-val együtt települ, ez adja az ffmpeg-et
import numpy as np
from moviepy import VideoFileClip, AudioFileClip
from transformers import pipeline

# ======================== A CENZÚRA-PIPELINE BEÁLLÍTÁSAI ========================
TILTOTT_SZAVAK = ["fuck", "fucking", "fucker", "shit", "bitch", "asshole", "bastard", "dick", "cunt", "stupid"]
TRAGAR_CIMKE = "LABEL_1"       # a trágárság-modell "trágár" osztálya (a futáskor kiírja a címkéket)
KUSZOB_SZOVEG = 0.30           # AI-érzékenység a szavaknál (0..1)

ASR_MODELL = "openai/whisper-small.en"           #Beszédfelismerés
TRAGAR_MODELL = "tarekziade/pardonmyai"          #Trágárság-felismerés


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
# ================================================================================


def ffmpeg(*argumentumok):
    """Lefuttat egy ffmpeg parancsot, hiba esetén leáll."""
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *argumentumok], check=True)


def wav_beolvas(fajl):
    """WAV fájl -> (hangminták táblázata, mintavételi frekvencia, csatornák száma)."""
    with wave.open(fajl) as w:
        csatornak, frekvencia = w.getnchannels(), w.getframerate()
        mintak = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return mintak.reshape(-1, csatornak), frekvencia, csatornak


def hang_cenzural(be, ki, idopontok, mod):
    """A megadott (kezdet, vég) időpontoknál csipog ('beep') vagy elnémít ('mute')."""
    hang, frekvencia, csatornak = wav_beolvas(be)
    hang = hang.copy()
    for kezdet, veg in idopontok:
        a = int(max(0, kezdet - 0.05) * frekvencia)       # kis ráhagyás a szó körül
        b = min(len(hang), int((veg + 0.05) * frekvencia))
        if mod == "mute":
            hang[a:b] = 0
        else:
            t = np.arange(b - a) / frekvencia
            hang[a:b] = (0.25 * 32767 * np.sin(2 * np.pi * 1000 * t)).astype(np.int16)[:, None]
    with wave.open(ki, "wb") as w:
        w.setnchannels(csatornak)
        w.setsampwidth(2)
        w.setframerate(frekvencia)
        w.writeframes(hang.tobytes())
=======
from moviepy import VideoFileClip, AudioFileClip


#1. Videófájl beolvasása
video_path = "C:/Users/didki/Videos/wow.mp4"
video = VideoFileClip(video_path)

#2. A hangsáv kinyerése és mentése
audio_path = "C:/Users/didki/Videos/hangsav.mp3"
video.audio.write_audiofile(audio_path)

#3. A hangsáv cenzurálása


#4. A hang nélküli videó mentése
video.write_videofile("C:/Users/didki/Videos/hang_nelkul_video.mp4", codec="libx264", audio=False)

#5. A hang hozzárendelése a videóhoz
video_clip = VideoFileClip("C:/Users/didki/Videos/hang_nelkul_video.mp4")
audio_clip = AudioFileClip(audio_path)
final_clip = video_clip.with_audio(audio_clip)

#6. Az új videó mentése hanggal együtt
final_clip.write_videofile("C:/Users/didki/Videos/kesz_video.mp4", codec="libx264", audio_codec="aac")

video_clip.close()
audio_clip.close()
final_clip.close()
>>>>>>> Balázs
