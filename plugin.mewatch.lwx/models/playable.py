class Playable:
    def __init__(self, **kwargs) -> None:
        self.url = kwargs['url']
        # is an array of .srts

        _subs = kwargs['subtitles']
        if type(_subs) == list:
            self.subtitles = kwargs['subtitles']
        else:
            self.subtitles = [kwargs['subtitles']]