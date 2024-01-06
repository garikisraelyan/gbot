from .checkers import ig_validation_check

def process_ig_link(message):
    if ig_validation_check(message):
        splitted_message = message.split(" ")
        for word in splitted_message:
            if ig_validation_check(word):
                ig_link = word
                break
        splitted_link = ig_link.split(".")
        try:
            splitted_link.remove("dd")
        except ValueError:
            pass
        splitted_link[splitted_link.index("instagram")] = "ddinstagram"
        dd_link = ".".join(splitted_link)
        return dd_link
    