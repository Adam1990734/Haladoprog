from factory import VideoCensoreFactory


def main():
    video_service = VideoCensoreFactory.create_video_service()

    video_service.process_video(
        "input/test.mp4",
        mode="beep"
    )

main()