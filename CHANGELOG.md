# Changelog

## 1.5

Backward compatible: `videotags`, `channeltags`, `videotitle`, `videodescription` and
`channeldescription` keep the same signature and return values.

### Added
- `get_video_info`, `get_channel_info`, `videotags_list`, `channeltags_list`, `hashtags`
- `tag_suggestions` (YouTube autocomplete), `analyze_tags` (500-char limit, duplicates)
- `bulk_videotags` for concurrent extraction
- `configure` for timeout, retries, Accept-Language and proxies
- `extract_video_id`, `normalize_url`
- Exceptions: `YoutubeTagsError`, `InvalidURL`, `RequestFailed`, `VideoUnavailable`
- `youtubetags` command line tool / `python -m YoutubeTags`
- Offline test suite and GitHub Actions test workflow

### Fixed
- Requests had no timeout and could hang forever; now 15s with retries on 429 / 5xx
- EU cookie-consent page made every function return empty results
- A tag meta element with no `content` crashed the join and returned `False`
- Links without `https://`, bare video ids and `@handles` failed
- `videotags` now falls back to the player data when the page has no tag meta elements;
  `channeltags` falls back to the channel keywords meta
- Dependency `bs4===0.0.1` (a placeholder package) replaced with `beautifulsoup4`
- Read the Docs build (added `.readthedocs.yaml`, `docs/conf.py`)
- CodeQL and PyPI workflows used deprecated action versions
- README example 4 printed an undefined variable
