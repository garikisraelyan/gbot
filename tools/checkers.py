import os
import urllib.parse


def get_link_type(string: str) -> str:
    parsed = urllib.parse.urlparse(string)
    if parsed.scheme and parsed.netloc:
        return "URL"
    if os.path.exists(string):
        return "Path"
    return "Unknown"

def yt_validation_check(string: str) -> bool:
    return "https://www.youtube.com/watch?" in string or \
            "https://youtube.com/watch?" in string or \
            "https://youtu.be/" in string or \
            "https://m.youtube.com/watch" in string

def ig_validation_check(string: str) -> bool:
    return "https://www.instagram.com/reels/" in string or \
            "https://instagram.com/reels/" in string or \
            "https://www.dd.instagram.com/reels/" in string or \
            "https://dd.instagram.com/reels/" in string
