import json
import unittest
from unittest import mock

import requests

import YoutubeTags
from YoutubeTags import _extract, cli

PLAYER = {
    "playabilityStatus": {"status": "OK"},
    "videoDetails": {
        "videoId": "RTbrXiIzUt4",
        "title": "What Is Right To Repair?",
        "lengthSeconds": "1215",
        "keywords": ["Right To Repair", "MKBHD", "Apple"],
        "channelId": "UCBJycsmduvYEL83R_U4JriQ",
        "shortDescription": "Own what you buy? #RightToRepair #tech #Tech",
        "viewCount": "4679645",
        "author": "Marques Brownlee",
        "isLiveContent": False,
        "isPrivate": False,
        "thumbnail": {"thumbnails": [
            {"url": "small.jpg", "width": 120, "height": 90},
            {"url": "big.jpg", "width": 1280, "height": 720},
        ]},
    },
    "microformat": {"playerMicroformatRenderer": {
        "category": "Science & Technology",
        "publishDate": "2021-05-07T18:03:28-07:00",
        "uploadDate": "2021-05-07T18:03:28-07:00",
        "likeCount": "250306",
        "ownerProfileUrl": "http://www.youtube.com/@mkbhd",
        "isFamilySafe": True,
        "isUnlisted": False,
    }},
}

VIDEO_HTML = """<html><head><title>What Is Right To Repair? - YouTube</title>
<meta name="description" content="Do you really own what you buy?">
<meta property="og:video:tag" content="Right To Repair">
<meta property="og:video:tag" content="MKBHD">
<meta property="og:video:tag" content="Apple">
</head><body><script>var ytInitialPlayerResponse = %s;var meta = {};</script></body></html>
""" % json.dumps(PLAYER)

# Same page without og:video:tag metas -- tags must come from the player JSON.
VIDEO_HTML_NO_META = VIDEO_HTML.replace('property="og:video:tag"', 'property="x"')

CHANNEL_HTML = """<html><head><title>Marques Brownlee - YouTube</title>
<meta name="description" content="MKBHD: Quality Tech Videos">
<meta name="keywords" content="MKBHD &quot;Marques Brownlee&quot; tech">
<meta property="og:title" content="Marques Brownlee">
<meta property="og:url" content="https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ">
<meta property="og:image" content="https://yt3.example/avatar.jpg">
<meta property="og:description" content="MKBHD: Quality Tech Videos">
<meta itemprop="identifier" content="UCBJycsmduvYEL83R_U4JriQ">
</head><body><script>{"subscriberCountText":{"simpleText":"1.17M subscribers"}}</script></body></html>
"""

UNAVAILABLE_HTML = '<html><script>var ytInitialPlayerResponse = {"playabilityStatus":{"status":"ERROR","reason":"This video is unavailable"}};</script></html>'


def fake_response(html, status=200):
    response = requests.Response()
    response.status_code = status
    response._content = html.encode("utf-8")
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.encoding = "utf-8"
    return response


def serve(html, status=200):
    return mock.patch("requests.get", return_value=fake_response(html, status))


class LegacyApiTests(unittest.TestCase):
    """The original 1.x functions must keep their exact contract."""

    def test_videotags_returns_comma_string(self):
        with serve(VIDEO_HTML):
            self.assertEqual(YoutubeTags.videotags("https://www.youtube.com/watch?v=RTbrXiIzUt4"),
                             "Right To Repair, MKBHD, Apple")

    def test_videotags_falls_back_to_player_keywords(self):
        with serve(VIDEO_HTML_NO_META):
            self.assertEqual(YoutubeTags.videotags("https://youtu.be/RTbrXiIzUt4"),
                             "Right To Repair, MKBHD, Apple")

    def test_videotags_no_tags_is_empty_string(self):
        with serve("<html><head><title>x</title></head></html>"):
            self.assertEqual(YoutubeTags.videotags("https://www.youtube.com/watch?v=Mlk888FiI8A"), "")

    def test_errors_return_false(self):
        with mock.patch("requests.get", side_effect=requests.ConnectionError("boom")), \
                mock.patch("time.sleep"), mock.patch("logging.error"):
            for fn in (YoutubeTags.videotags, YoutubeTags.channeltags, YoutubeTags.videotitle,
                       YoutubeTags.videodescription, YoutubeTags.channeldescription):
                self.assertIs(fn("https://www.youtube.com/watch?v=RTbrXiIzUt4"), False)

    def test_invalid_url_returns_false(self):
        with mock.patch("logging.error"):
            self.assertIs(YoutubeTags.videotags("not a url"), False)

    def test_videotitle_keeps_youtube_suffix(self):
        with serve(VIDEO_HTML):
            self.assertEqual(YoutubeTags.videotitle("https://www.youtube.com/watch?v=RTbrXiIzUt4"),
                             "What Is Right To Repair? - YouTube")

    def test_descriptions(self):
        with serve(VIDEO_HTML):
            self.assertEqual(YoutubeTags.videodescription("https://www.youtube.com/watch?v=RTbrXiIzUt4"),
                             "Do you really own what you buy?")
        with serve(CHANNEL_HTML):
            self.assertEqual(YoutubeTags.channeldescription("https://youtube.com/c/mkbhd"),
                             "MKBHD: Quality Tech Videos")

    def test_channeltags_falls_back_to_keywords_meta(self):
        with serve(CHANNEL_HTML):
            self.assertEqual(YoutubeTags.channeltags("https://youtube.com/c/mkbhd"),
                             "MKBHD, Marques Brownlee, tech")

    def test_meta_without_content_is_skipped(self):
        html = '<meta property="og:video:tag"><meta property="og:video:tag" content="ok">'
        with serve(html):
            self.assertEqual(YoutubeTags.videotags("https://www.youtube.com/watch?v=RTbrXiIzUt4"), "ok")

    def test_sends_timeout_and_consent_cookie(self):
        with serve(VIDEO_HTML) as get:
            YoutubeTags.videotags("RTbrXiIzUt4")
        args, kwargs = get.call_args
        self.assertEqual(args[0], "https://www.youtube.com/watch?v=RTbrXiIzUt4")
        self.assertTrue(kwargs["timeout"])
        self.assertIn("SOCS", kwargs["cookies"])

    def test_retries_on_server_error(self):
        responses = [fake_response("", 503), fake_response(VIDEO_HTML)]
        with mock.patch("requests.get", side_effect=responses) as get, mock.patch("time.sleep"):
            self.assertEqual(YoutubeTags.videotags("RTbrXiIzUt4"), "Right To Repair, MKBHD, Apple")
        self.assertEqual(get.call_count, 2)


class NewApiTests(unittest.TestCase):
    def test_get_video_info(self):
        with serve(VIDEO_HTML):
            info = YoutubeTags.get_video_info("https://www.youtube.com/shorts/RTbrXiIzUt4")
        self.assertEqual(info["video_id"], "RTbrXiIzUt4")
        self.assertEqual(info["title"], "What Is Right To Repair?")
        self.assertEqual(info["tags"], ["Right To Repair", "MKBHD", "Apple"])
        self.assertEqual(info["hashtags"], ["#RightToRepair", "#tech"])
        self.assertEqual(info["views"], 4679645)
        self.assertEqual(info["likes"], 250306)
        self.assertEqual(info["length_seconds"], 1215)
        self.assertEqual(info["thumbnail"], "big.jpg")
        self.assertEqual(info["category"], "Science & Technology")

    def test_unavailable_video_raises(self):
        with serve(UNAVAILABLE_HTML):
            with self.assertRaises(YoutubeTags.VideoUnavailable):
                YoutubeTags.get_video_info("xxxxxxxxxxx")

    def test_get_channel_info(self):
        with serve(CHANNEL_HTML):
            info = YoutubeTags.get_channel_info("@mkbhd")
        self.assertEqual(info["channel_id"], "UCBJycsmduvYEL83R_U4JriQ")
        self.assertEqual(info["name"], "Marques Brownlee")
        self.assertEqual(info["tags"], ["MKBHD", "Marques Brownlee", "tech"])
        self.assertEqual(info["subscribers"], "1.17M subscribers")

    def test_list_helpers(self):
        with serve(VIDEO_HTML):
            self.assertEqual(YoutubeTags.videotags_list("RTbrXiIzUt4"), ["Right To Repair", "MKBHD", "Apple"])
            self.assertEqual(YoutubeTags.hashtags("RTbrXiIzUt4"), ["#RightToRepair", "#tech"])
        with serve(CHANNEL_HTML):
            self.assertEqual(YoutubeTags.channeltags_list("@mkbhd"), ["MKBHD", "Marques Brownlee", "tech"])

    def test_tag_suggestions(self):
        body = 'window.google.ac.h(["repair",[["repair phone",0,[512]],["repair car",0,[512]]],{"k":1}])'
        with serve(body) as get:
            self.assertEqual(YoutubeTags.tag_suggestions("repair", region="IN"), ["repair phone", "repair car"])
        self.assertEqual(get.call_args[1]["params"]["gl"], "IN")

    def test_analyze_tags(self):
        result = YoutubeTags.analyze_tags("Right To Repair, right to repair, MKBHD")
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["unique_count"], 2)
        self.assertEqual(result["duplicates"], ["right to repair"])
        # 2 quoted multi-word tags (15+2 each) + MKBHD (5) + 2 commas
        self.assertEqual(result["total_characters"], 41)
        self.assertTrue(result["within_limit"])
        self.assertEqual(YoutubeTags.analyze_tags("")["count"], 0)
        self.assertEqual(YoutubeTags.analyze_tags(False)["count"], 0)

    def test_bulk_videotags(self):
        with serve(VIDEO_HTML):
            result = YoutubeTags.bulk_videotags(["RTbrXiIzUt4", "bad-link"])
        self.assertEqual(result["RTbrXiIzUt4"], ["Right To Repair", "MKBHD", "Apple"])
        self.assertIsNone(result["bad-link"])

    def test_configure(self):
        original = YoutubeTags.configure()
        try:
            YoutubeTags.configure(timeout=3, language="en-US")
            with serve(VIDEO_HTML) as get:
                YoutubeTags.videotags("RTbrXiIzUt4")
            self.assertEqual(get.call_args[1]["timeout"], 3)
            self.assertEqual(get.call_args[1]["headers"]["Accept-Language"], "en-US")
        finally:
            YoutubeTags._http._config.update(original)


class ExtractTests(unittest.TestCase):
    def test_extract_video_id(self):
        for link in ("RTbrXiIzUt4",
                     "https://www.youtube.com/watch?v=RTbrXiIzUt4&t=10",
                     "https://youtu.be/RTbrXiIzUt4?si=abc",
                     "https://www.youtube.com/shorts/RTbrXiIzUt4",
                     "https://www.youtube.com/embed/RTbrXiIzUt4",
                     "https://www.youtube.com/live/RTbrXiIzUt4",
                     "https://m.youtube.com/watch?feature=share&v=RTbrXiIzUt4"):
            self.assertEqual(YoutubeTags.extract_video_id(link), "RTbrXiIzUt4", link)
        with self.assertRaises(YoutubeTags.InvalidURL):
            YoutubeTags.extract_video_id("https://example.com")

    def test_normalize_url(self):
        n = YoutubeTags.normalize_url
        self.assertEqual(n("https://www.youtube.com/watch?v=RTbrXiIzUt4"), "https://www.youtube.com/watch?v=RTbrXiIzUt4")
        self.assertEqual(n("RTbrXiIzUt4"), "https://www.youtube.com/watch?v=RTbrXiIzUt4")
        self.assertEqual(n("youtube.com/c/mkbhd"), "https://youtube.com/c/mkbhd")
        self.assertEqual(n("@mkbhd"), "https://www.youtube.com/@mkbhd")
        self.assertEqual(n("not a url"), "not a url")
        self.assertIsNone(n(None))

    def test_split_keywords(self):
        self.assertEqual(_extract.split_keywords('a "b c" d'), ["a", "b c", "d"])
        self.assertEqual(_extract.split_keywords(None), [])


class CliTests(unittest.TestCase):
    def test_default_prints_tags(self):
        with serve(VIDEO_HTML), mock.patch("builtins.print") as out:
            self.assertEqual(cli.main(["RTbrXiIzUt4"]), 0)
        out.assert_called_with("Right To Repair, MKBHD, Apple")

    def test_error_exit_code(self):
        with mock.patch("sys.stderr"):
            self.assertEqual(cli.main(["bad-link"]), 1)


if __name__ == "__main__":
    unittest.main()
