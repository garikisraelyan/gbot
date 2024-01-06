from pytube import YouTube

SAVE_PATH = ""


class InvalidRequestException(Exception):
    def __init__(
            self, 
            message: str = "Invalid request. Please provide a YouTube video link."
        ):
        self.message = message
        super().__init__(self.message)


def download(link: str, resolution: str = None):
    yt = YouTube(link).streams
    if resolution:
        yt = yt.filter(res=resolution).first()
        print(yt)
    else:
        yt = yt.get_highest_resolution()
        print(yt)
    filename = f"{yt.title}_{resolution}.mp4".replace(" ", "_")
    file = yt.download(output_path=SAVE_PATH, filename=filename)
    return file

def message_processer(message: str):
    if "https://www.youtube.com/watch?" or \
        "https://youtube.com/watch?" or \
        "https://youtu.be/" or \
        "https://m.youtube.com/watch" in message:
        splitted_message = message.split(" ")
        for word in splitted_message:
            if "https://www.youtube.com/watch?" or \
            "https://youtube.com/watch?" or \
            "https://youtu.be/" or \
            "https://m.youtube.com/watch" in word:
                yt_link = word
                break
        file = download(yt_link)
        return file
    # TODO: Exception
    # else:
    #     raise InvalidRequestException
