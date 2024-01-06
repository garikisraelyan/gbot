from .yt_video_downloader import process_yt_video
from .ig_video_downloader import process_ig_link
from .checkers import (
    yt_validation_check,
    ig_validation_check,
)

class InvalidRequestException(Exception):
    def __init__(
            self, 
            message: str = "Invalid request. Please provide a valid YouTube/Instagram video/reel link."
        ):
        self.message = message
        super().__init__(self.message)


def message_processer(message: str) -> str:
    if yt_validation_check(message):
        file = process_yt_video(message)
        return file
    if ig_validation_check(message):
        dd_link = process_ig_link(message)
        return dd_link
    # TODO: Exception
    # else:
    #     raise InvalidRequestException
