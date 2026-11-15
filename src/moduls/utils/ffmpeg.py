import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

def run_ffmpeg(*args):
    subprocess.run(
        [FFMPEG, "-y", *args],
        check=True
    )