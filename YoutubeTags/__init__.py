"""YoutubeTags -- YouTube SEO tool for extracting video tags without the official YouTube API.

The original functions (videotags, channeltags, videotitle, videodescription,
channeldescription) keep their exact behaviour: they take a link, return a string,
and return False (after logging the error) if anything goes wrong.

Newer functions (get_video_info, get_channel_info, videotags_list, tag_suggestions, ...)
return lists / dicts and raise YoutubeTagsError subclasses instead.
"""
import logging

import requests  # noqa: F401  (kept importable as YoutubeTags.requests for existing code)
from bs4 import BeautifulSoup

from . import _extract, _http
from ._extract import extract_video_id, normalize_url
from ._http import configure
from .api import (
    TAGS_CHAR_LIMIT,
    analyze_tags,
    bulk_videotags,
    channeltags_list,
    get_channel_info,
    get_video_info,
    hashtags,
    tag_suggestions,
    videotags_list,
)
from .exceptions import InvalidURL, RequestFailed, VideoUnavailable, YoutubeTagsError

__version__ = "1.5"

__all__ = [
    # original API
    "videotags",
    "channeltags",
    "videotitle",
    "videodescription",
    "channeldescription",
    # added in 1.5
    "get_video_info",
    "get_channel_info",
    "videotags_list",
    "channeltags_list",
    "hashtags",
    "tag_suggestions",
    "analyze_tags",
    "bulk_videotags",
    "extract_video_id",
    "normalize_url",
    "configure",
    "TAGS_CHAR_LIMIT",
    "YoutubeTagsError",
    "InvalidURL",
    "RequestFailed",
    "VideoUnavailable",
]


def _fetch(url):
    return _http.get(normalize_url(url))


def videotags(url):
    try:
        request = _fetch(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        tags = _extract.og_video_tags(soup)
        if not tags:
            details = _extract.player_response(request.text).get("videoDetails") or {}
            tags = details.get("keywords") or []
        return ', '.join(tags)
    except Exception as e:
        logging.error(e)
        return False


def channeltags(url):
    try:
        request = _fetch(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        tags = _extract.og_video_tags(soup)
        if not tags:
            tags = _extract.split_keywords(_extract.meta_content(soup, name="keywords"))
        return ', '.join(tags)
    except Exception as e:
        logging.error(e)
        return False


def videotitle(url):
    try:
        request = _fetch(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        title = soup.find("title").text.strip()
        return title
    except Exception as e:
        logging.error(e)
        return False


def videodescription(url):
    try:
        request = _fetch(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        description = soup.find("meta", {"name": "description"}).attrs.get("content")
        return description
    except Exception as e:
        logging.error(e)
        return False


def channeldescription(url):
    try:
        request = _fetch(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        description = soup.find("meta", {"name": "description"}).attrs.get("content")
        return description
    except Exception as e:
        logging.error(e)
        return False
