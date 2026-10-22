"""Command line interface: `youtubetags <link>` or `python -m YoutubeTags <link>`."""
import argparse
import json
import sys

from . import __version__, api
from .exceptions import YoutubeTagsError


def _parser():
    parser = argparse.ArgumentParser(
        prog="youtubetags",
        description="Extract YouTube video / channel tags without the YouTube API.",
    )
    parser.add_argument("target", nargs="*", help="video link(s), video id(s), or channel link with --channel")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-c", "--channel", action="store_true", help="treat targets as channel links")
    mode.add_argument("-i", "--info", action="store_true", help="print full video metadata")
    mode.add_argument("-a", "--analyze", action="store_true", help="print SEO analysis of the video's tags")
    mode.add_argument("-s", "--suggest", metavar="QUERY", help="YouTube autocomplete suggestions for a keyword")
    parser.add_argument("--json", action="store_true", help="output JSON")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    return parser


def _emit(value, as_json):
    if as_json or isinstance(value, dict):
        print(json.dumps(value, indent=2, ensure_ascii=False))
    elif isinstance(value, list):
        print(", ".join(value))
    else:
        print(value)


def main(argv=None):
    parser = _parser()
    args = parser.parse_args(argv)

    if args.suggest:
        try:
            _emit(api.tag_suggestions(args.suggest), args.json)
        except YoutubeTagsError as e:
            print("error: %s" % e, file=sys.stderr)
            return 1
        return 0

    if not args.target:
        parser.error("give at least one link (or use --suggest QUERY)")

    status = 0
    results = {}
    for target in args.target:
        try:
            if args.channel:
                value = api.get_channel_info(target) if args.json else api.channeltags_list(target)
            elif args.info:
                value = api.get_video_info(target)
            elif args.analyze:
                value = api.analyze_tags(api.videotags_list(target))
            else:
                value = api.videotags_list(target)
        except YoutubeTagsError as e:
            print("error: %s: %s" % (target, e), file=sys.stderr)
            status = 1
            continue
        if args.json and len(args.target) > 1:
            results[target] = value
        else:
            _emit(value, args.json)
    if results:
        _emit(results, True)
    return status


if __name__ == "__main__":
    sys.exit(main())
