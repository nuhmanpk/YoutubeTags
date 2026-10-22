class YoutubeTagsError(Exception):
    """Base class for every error raised by YoutubeTags."""


class InvalidURL(YoutubeTagsError, ValueError):
    """The input is not a recognisable YouTube link or video id."""


class RequestFailed(YoutubeTagsError):
    """YouTube could not be reached or kept returning errors."""


class VideoUnavailable(YoutubeTagsError):
    """The video is private, removed, age-gated or otherwise not viewable."""
