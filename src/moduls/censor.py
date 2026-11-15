from sys import argv
from utils.args import get_mode, get_video_source

from factory import VideoCensoreFactory
    

def main():
    video_service = VideoCensoreFactory.create_video_service()

    video_service.process_video(
        video_path= get_video_source(argv),
        mode= get_mode(argv)
    )

main()