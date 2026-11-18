import os
import subprocess
import tempfile
import wave

import imageio_ffmpeg         
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


def audio_pipeline(audio_path):
    """
    HANG-PIPELINE: az audio_path (mp3) fájlt veszi át, és a cenzúrázott hang elérési útját adja vissza.

      audio_path ─► [a] átalakítás ─► [b] AI #1 Whisper (szavak időponttal)
                 ─► [c] AI #2 trágárság-modell ─► [d] futtató döntése
                 ─► [e] csipogás / némítás ─► cenzúrázott mp3
    """
    mappa = tempfile.mkdtemp()
    hang_wav = os.path.join(mappa, "hang.wav")         # jó minőségű hang (ezt cenzúrázzuk)
    beszed_wav = os.path.join(mappa, "beszed.wav")     # 16 kHz mono (ezt kapja az AI)
    cenz_wav = os.path.join(mappa, "cenzuralt.wav")
    kimenet = os.path.splitext(audio_path)[0] + "_cenzuralt.mp3"

    # [a] az mp3 átalakítása WAV-vá (így könnyű számokkal dolgozni)
    ffmpeg("-i", audio_path, "-c:a", "pcm_s16le", hang_wav)
    ffmpeg("-i", audio_path, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", beszed_wav)

    # [b] AI #1 – beszédfelismerés: minden szó + mikor hangzik el
    print("AI #1 – beszédfelismerés (Whisper)...")
    beszed, _, _ = wav_beolvas(beszed_wav)
    beszed = beszed[:, 0].astype(np.float32) / 32768.0
    asr = pipeline("automatic-speech-recognition", model=ASR_MODELL, chunk_length_s=30)
    szavak = asr({"raw": beszed, "sampling_rate": 16000}, return_timestamps="word")["chunks"]
    print(f"  {len(szavak)} szót ismert fel.")
    for sz in szavak:
        szo = sz["text"].strip()
        kezdet, veg = sz["timestamp"]
        print(f"{kezdet:7.2f} mp - {veg:7.2f} mp | {szo}")

    # [c] AI #2 – melyik szó trágár? (tiltólista + AI-modell)
    print("AI #2 – trágárság-felismerés...")
    trago_ai = pipeline("text-classification", model=TRAGAR_MODELL)
    print("  A modell osztálycímkéi:", trago_ai.model.config.id2label)
    lista = [sz["text"].strip() for sz in szavak]
    ai_eredmenyek = trago_ai(lista) if lista else []
    talalatok = []                                     # (kezdet, vég, szó)
    for sz, szo, ai in zip(szavak, lista, ai_eredmenyek):
        listas = szo.lower().strip(".,!?\"'") in TILTOTT_SZAVAK or "*" in szo
        ai_szerint = ai["label"] == TRAGAR_CIMKE and ai["score"] >= KUSZOB_SZOVEG
        if listas or ai_szerint:
            kezdet, veg = sz["timestamp"]
            talalatok.append((kezdet, veg if veg is not None else kezdet + 0.3, szo))

    # [d] A futtató értesítése és döntése
    if not talalatok:
        print("  Nem találtam trágár szót – a hang változatlan marad.")
        ffmpeg("-i", hang_wav, kimenet)
        return kimenet
    print(f"\nFIGYELEM: {len(talalatok)} trágár szót találtam a hangban:")
    for kezdet, veg, szo in talalatok:
        print(f"   {kezdet:7.2f} mp – {veg:7.2f} mp   {szo}")
    valasz = input("Mit tegyek? [b] csipogás / [m] némítás / [k] marad: ").strip().lower()
    mod = {"b": "beep", "m": "mute"}.get(valasz, "none")

    # [e] Cenzúrázás és mentés mp3-ba
    if mod == "none":
        ffmpeg("-i", hang_wav, kimenet)
    else:
        hang_cenzural(hang_wav, cenz_wav, [(k, v) for k, v, _ in talalatok], mod)
        ffmpeg("-i", cenz_wav, kimenet)
    return kimenet


# ============================ A TÁRS EREDETI PROGRAMJA ============================

#1. Videófájl beolvasása
video_path = "C:/Users/local_user/Videos/wow.mp4"
video = VideoFileClip(video_path)

#2. A hangsáv kinyerése és mentése
audio_path = "C:/Users/local_user/Videos/hangsav.mp3"
video.audio.write_audiofile(audio_path)

#3. A hangsáv cenzurálása
audio_path = audio_pipeline(audio_path)      # a pipeline az audio_path-ot veszi át, és a cenzúrázott hang útvonalát adja vissza

#4. A hang nélküli videó mentése
video.write_videofile("C:/Users/local_user/Videos/hang_nelkul_video.mp4", codec="libx264", audio=False)

#5. A hang hozzárendelése a videóhoz
video_clip = VideoFileClip("C:/Users/local_user/Videos/hang_nelkul_video.mp4")
audio_clip = AudioFileClip(audio_path)       # ez már a cenzúrázott hang
final_clip = video_clip.with_audio(audio_clip)

#6. Az új videó mentése hanggal együtt
final_clip.write_videofile("C:/Users/local_user/Videos/kesz_video.mp4", codec="libx264", audio_codec="aac")

video_clip.close()
audio_clip.close()
final_clip.close()
