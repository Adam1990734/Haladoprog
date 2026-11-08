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