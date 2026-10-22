"""Richer API added in 1.5. These functions raise YoutubeTagsError subclasses on failure
instead of returning False, and return Python lists / dicts instead of joined strings."""
import json
import re
from concurrent.futures import ThreadPoolExecutor

from . import _extract, _http
from .exceptions import RequestFailed, VideoUnavailable

# YouTube Studio rejects a tag list longer than this many characters.
TAGS_CHAR_LIMIT = 500

_SUGGEST_URL = "https://suggestqueries-clients6.youtube.com/complete/search"


def _watch_url(url):
    return "https://www.youtube.com/watch?v=" + _extract.extract_video_id(url)


def get_video_info(url):
    """Everything YouTube exposes publicly about a video, as a dict.

    Accepts watch / youtu.be / shorts / embed / live links or a bare 11-character id.
    """
    html = _http.get_html(_watch_url(url))
    player = _extract.player_response(html)
    details = player.get("videoDetails")
    if not details:
        status = player.get("playabilityStatus") or {}
        reason = status.get("reason") or status.get("status") or "no video details on page"
        raise VideoUnavailable("Video %s is unavailable: %s" % (_extract.extract_video_id(url), reason))

    micro = (player.get("microformat") or {}).get("playerMicroformatRenderer") or {}
    soup = _extract.soup_of(html)
    tags = details.get("keywords") or _extract.og_video_tags(soup)
    description = details.get("shortDescription") or ""

    video_id = details.get("videoId")
    return {
        "video_id": video_id,
        "url": "https://www.youtube.com/watch?v=%s" % video_id,
        "title": details.get("title"),
        "description": description,
        "tags": list(tags),
        "hashtags": _extract.hashtags_from_text(description),
        "channel_name": details.get("author") or micro.get("ownerChannelName"),
        "channel_id": details.get("channelId") or micro.get("externalChannelId"),
        "channel_url": micro.get("ownerProfileUrl"),
        "views": _extract.to_int(details.get("viewCount") or micro.get("viewCount")),
        "likes": _extract.to_int(micro.get("likeCount")),
        "length_seconds": _extract.to_int(details.get("lengthSeconds")),
        "category": micro.get("category"),
        "publish_date": micro.get("publishDate"),
        "upload_date": micro.get("uploadDate"),
        "thumbnail": _extract.best_thumbnail(details.get("thumbnail")),
        "is_live": bool(details.get("isLiveContent")),
        "is_family_safe": micro.get("isFamilySafe"),
        "is_unlisted": micro.get("isUnlisted"),
        "is_private": details.get("isPrivate"),
    }


def get_channel_info(url):
    """Public metadata for a channel page (/@handle, /c/name, /channel/UC..., /user/name)."""
    html = _http.get_html(_extract.normalize_url(url))
    soup = _extract.soup_of(html)
    channel_id = _extract.meta_content(soup, itemprop="identifier")
    if not channel_id:
        match = re.search(r"/channel/(UC[\w-]{22})", _extract.meta_content(soup, property="og:url") or "")
        channel_id = match.group(1) if match else None
    tags = _extract.og_video_tags(soup) or _extract.split_keywords(
        _extract.meta_content(soup, name="keywords")
    )
    return {
        "channel_id": channel_id,
        "name": _extract.meta_content(soup, property="og:title"),
        "url": _extract.meta_content(soup, property="og:url"),
        "description": _extract.meta_content(soup, property="og:description")
        or _extract.meta_content(soup, name="description"),
        "tags": tags,
        "avatar": _extract.meta_content(soup, property="og:image"),
        "subscribers": _extract.subscriber_text(html),
        "is_family_safe": _extract.meta_content(soup, itemprop="isFamilyFriendly"),
    }


def videotags_list(url):
    """Video tags as a list of strings (empty list when the video has none)."""
    return get_video_info(url)["tags"]


def channeltags_list(url):
    """Channel tags as a list of strings."""
    return get_channel_info(url)["tags"]


def hashtags(url):
    """Hashtags (#like #this) used in a video's description."""
    return get_video_info(url)["hashtags"]


def tag_suggestions(query, language="en", region=None):
    """YouTube search autocomplete for a keyword -- handy for finding new tag ideas."""
    params = {"client": "youtube", "ds": "yt", "q": query, "hl": language}
    if region:
        params["gl"] = region
    text = _http.get_html(_SUGGEST_URL, params=params)
    start, end = text.find("("), text.rfind(")")
    if start == -1 or end <= start:
        raise RequestFailed("Unexpected suggestion response for %r" % (query,))
    try:
        payload = json.loads(text[start + 1:end])
    except ValueError:
        raise RequestFailed("Could not decode suggestion response for %r" % (query,))
    return [item[0] for item in payload[1] if isinstance(item, list) and item]


def analyze_tags(tags):
    """SEO checks for a tag list (list, or the comma-separated string videotags() returns).

    Character count follows YouTube Studio: commas between tags count, and tags that
    contain a space are wrapped in quotes (+2 characters each).
    """
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    tags = [t for t in (tags or []) if t]

    seen, duplicates = set(), []
    for tag in tags:
        key = tag.lower()
        if key in seen and key not in duplicates:
            duplicates.append(key)
        seen.add(key)

    total = sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0)
    return {
        "count": len(tags),
        "unique_count": len(seen),
        "total_characters": total,
        "character_limit": TAGS_CHAR_LIMIT,
        "within_limit": total <= TAGS_CHAR_LIMIT,
        "duplicates": duplicates,
        "longest": max(tags, key=len) if tags else None,
        "average_length": round(sum(len(t) for t in tags) / float(len(tags)), 2) if tags else 0,
    }


def bulk_videotags(urls, max_workers=4):
    """Fetch tags for many videos concurrently. Returns {url: [tags]}; failed urls map to None."""
    urls = list(urls)

    def one(u):
        try:
            return videotags_list(u)
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=max(1, max_workers)) as pool:
        return dict(zip(urls, pool.map(one, urls)))
