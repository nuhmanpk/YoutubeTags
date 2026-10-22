"""Pure parsing helpers. Nothing in here touches the network."""
import json
import re

from bs4 import BeautifulSoup

from .exceptions import InvalidURL

_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_VIDEO_ID_IN_URL_RE = re.compile(
    r"(?:v=|vi=|youtu\.be/|/shorts/|/embed/|/live/|/v/|/e/)([A-Za-z0-9_-]{11})"
)
_YOUTUBE_HOST_RE = re.compile(
    r"^(?:www\.|m\.|music\.)?(?:youtube\.com|youtu\.be|youtube-nocookie\.com)(?:/|$)",
    re.IGNORECASE,
)
_HASHTAG_RE = re.compile(r"(?:^|(?<=\s))#(\w+)", re.UNICODE)
_KEYWORD_TOKEN_RE = re.compile(r'"([^"]+)"|(\S+)')


def normalize_url(url):
    """Make common link shapes fetchable; anything unrecognised is returned unchanged.

    "RTbrXiIzUt4"              -> https://www.youtube.com/watch?v=RTbrXiIzUt4
    "youtube.com/watch?v=..."  -> https://youtube.com/watch?v=...
    "@mkbhd"                   -> https://www.youtube.com/@mkbhd
    """
    if not isinstance(url, str):
        return url
    url = url.strip()
    if _VIDEO_ID_RE.match(url):
        return "https://www.youtube.com/watch?v=" + url
    if url.startswith("@") and "/" not in url:
        return "https://www.youtube.com/" + url
    if url.startswith("//"):
        return "https:" + url
    if _YOUTUBE_HOST_RE.match(url):
        return "https://" + url
    return url


def extract_video_id(url):
    """Return the 11-character video id from a link (watch, youtu.be, shorts, embed, live) or id."""
    if not isinstance(url, str):
        raise InvalidURL("Expected a string, got %r" % (url,))
    candidate = url.strip()
    if _VIDEO_ID_RE.match(candidate):
        return candidate
    match = _VIDEO_ID_IN_URL_RE.search(candidate)
    if not match:
        raise InvalidURL("Could not find a YouTube video id in %r" % (url,))
    return match.group(1)


def soup_of(markup):
    return BeautifulSoup(markup, "html.parser")


def og_video_tags(soup):
    return [
        meta.attrs.get("content")
        for meta in soup.find_all("meta", {"property": "og:video:tag"})
        if meta.attrs.get("content")
    ]


def meta_content(soup, **attrs):
    tag = soup.find("meta", attrs)
    if tag is None:
        return None
    return tag.attrs.get("content")


def split_keywords(value):
    """Split a channel keywords string: words separated by spaces, phrases in double quotes."""
    if not value:
        return []
    return [quoted or bare for quoted, bare in _KEYWORD_TOKEN_RE.findall(value)]


def find_json_object(html, variable):
    """Decode the JSON object assigned to a JS variable such as ytInitialPlayerResponse."""
    pattern = re.compile(r"\b%s\s*=\s*(?=\{)" % re.escape(variable))
    decoder = json.JSONDecoder()
    for match in pattern.finditer(html):
        try:
            value, _ = decoder.raw_decode(html, match.end())
        except ValueError:
            continue
        if isinstance(value, dict):
            return value
    return None


def player_response(html):
    return find_json_object(html, "ytInitialPlayerResponse") or {}


def hashtags_from_text(text):
    seen = set()
    result = []
    for tag in _HASHTAG_RE.findall(text or ""):
        key = tag.lower()
        if key not in seen:
            seen.add(key)
            result.append("#" + tag)
    return result


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def best_thumbnail(thumbnail_block):
    thumbs = (thumbnail_block or {}).get("thumbnails") or []
    if not thumbs:
        return None
    best = max(thumbs, key=lambda t: (t.get("width") or 0) * (t.get("height") or 0))
    return best.get("url")


def subscriber_text(html):
    match = re.search(r'"subscriberCountText":\{.*?"simpleText":"([^"]+)"', html)
    return match.group(1) if match else None
