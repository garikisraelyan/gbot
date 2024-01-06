from pytube import YouTube


SAVE_PATH = "videos/"

def yt_validation_check(string: str) -> bool:
    if "https://www.youtube.com/watch?" or \
        "https://youtube.com/watch?" or \
        "https://youtu.be/" or \
        "https://m.youtube.com/watch" in string:
        return True
    return False

def yt_download(link: str, resolution: str = None):
    yt = YouTube(link).streams
    if resolution:
        yt = yt.filter(res=resolution).first()
    else:
        yt = yt.get_highest_resolution()
    filename = f"{yt.title}_{resolution}.mp4".replace(" ", "_")
    file = yt.download(output_path=SAVE_PATH, filename=filename)
    return file

def process_yt_video(message: str):
    splitted_message = message.split(" ")
    for word in splitted_message:
        if yt_validation_check(word):
            yt_link = word
            break
    file = yt_download(yt_link)
    return file