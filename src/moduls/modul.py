from moviepy.editor import VideoFileClip, AudioFileClip


#1. Videófájl beolvasása
video_path = "video.mp4"
video = VideoFileClip(video_path)

#2. A hangsáv kinyerése és mentése
audio_path = "hangsav.mp3"
video.audio.write_audiofile(audio_path)

#3. A hangsáv cenzurálása


#4. A hang nélküli videó mentése
video.write_videofile("hang_nelkul_video.mp4", codec="libx264", audio=False)

#5. A hang hozzárendelése a videóhoz
video_clip = VideoFileClip("hang_nelkul_video.mp4")
audio_clip = AudioFileClip(audio_path)
final_clip = video_clip.set_audio(audio_clip)

#6. Az új videó mentése hanggal együtt
final_clip.write_videofile("kesz_video.mp4", codec="libx264", audio_codec="aac")

video_clip.close()
audio_clip.close()
final_clip.close()