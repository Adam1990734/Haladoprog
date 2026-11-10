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
