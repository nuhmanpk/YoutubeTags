# YoutubeTags
**YouTube SEO tool for extracting video tags without the need for the official YouTube API**

[![Downloads](https://static.pepy.tech/personalized-badge/youtubetags?period=total&units=abbreviation&left_color=grey&right_color=yellow&left_text=Total-Downloads)](https://pepy.tech/project/youtubetags)
[![CodeQL](https://github.com/nuhmanpk/YoutubeTags/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/nuhmanpk/YoutubeTags/actions/workflows/codeql-analysis.yml)
[![Supported Versions](https://img.shields.io/pypi/pyversions/Youtubetags.svg)](https://pypi.org/project/YoutubeTags)
![GitHub](https://img.shields.io/github/license/nuhmanpk/YoutubeTags)
![PyPI](https://img.shields.io/pypi/v/youtubetags)
[![Documentation Status](https://readthedocs.org/projects/youtubetags/badge/?version=latest)](https://youtubetags.readthedocs.io/en/latest/?badge=latest)
![PyPI - Downloads](https://img.shields.io/pypi/dm/YoutubeTags)
[![Downloads](https://static.pepy.tech/personalized-badge/youtubetags?period=week&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads/Week)](https://pepy.tech/project/youtubetags)
[![Upload to PIP](https://github.com/nuhmanpk/YoutubeTags/actions/workflows/Pypi-uploads.yml/badge.svg?branch=main&event=workflow_dispatch)](https://github.com/nuhmanpk/YoutubeTags/actions/workflows/Pypi-uploads.yml)
![PyPI - Format](https://img.shields.io/pypi/format/YoutubeTags)


[![Tests](https://github.com/nuhmanpk/YoutubeTags/actions/workflows/tests.yml/badge.svg)](https://github.com/nuhmanpk/YoutubeTags/actions/workflows/tests.yml)

> **New in Version 1.5** — fully backward compatible, existing code keeps working unchanged.
> - Full video metadata (`get_video_info`), channel metadata (`get_channel_info`)
> - Tags as Python lists, hashtags, YouTube autocomplete tag suggestions, tag SEO analysis (500-char limit check)
> - Bulk/concurrent tag extraction, `youtubetags` command line tool
> - Accepts `youtu.be`, Shorts, embed, live links, bare video ids and `@handles`
> - Timeouts, retries and EU cookie-consent handling so requests no longer hang or come back empty
>
> **Version 1.4** Added Functions for videotitle,videodescription,channeldescription

# Installation

```python
pip install YoutubeTags

```
# Video Tags

## How to Use It

```python
import YoutubeTags
from YoutubeTags import videotags
link = "Add Your Youtube Link Here" # Use https / http Links
variable_name = videotags(link)
print(variable_name)
```

> **_NOTE:_** ONLY SUPPORTS HTTP(S) , use HTTP(S) links to get the results 

## Example 1
```python
import YoutubeTags
from YoutubeTags import videotags
findtags = videotags("https://www.youtube.com/watch?v=RTbrXiIzUt4") # Mkbhd's Video
print(findtags)
```
### Output of Example 1

```
Right To Repair, right to repair, MKBHD, right to repair movement, Apple, Apple vs, 
repairing iPhone, iPhone 12, Tesla right to repair, Apple right to repair

```

## Example 2
```python
import YoutubeTags
from YoutubeTags import videotags
tags = videotags("https://www.youtube.com/watch?v=Kbe3FKeCd1A") # Karikku star Episode
print(tags)
```
### Output of Example 2

```
karikku, malayalam, funny, comedy, webseries, lolan,
george, karikk, karikke, film, trending, sketch, vine, flowerstv

```
## Example 3
```python
import YoutubeTags
from YoutubeTags import videotags
gettag = videotags("https://www.youtube.com/watch?v=nvjILgpf6tc") # Video From Technical Guruji
print(gettag)
```
### Output of Example 3
```
iPhone 14, iPhone 14 Unboxing, iPhone 14 exclusive 1st look, iPhone 14 first look,
iPhone 14 no notch, iPhone 14 punch hole camera, iPhone 14 titanium sides, iPhone 14 look, 
iPhone 14 leaks, iPhone 14 design, iPhone 14 india, iPhone 14 launch date, iPhone 14 no camera bump,
iPhone 14 features, iPhone 14 price, iPhone 14 vs iPhone 13, iPhone 14 launch event, iPhone 14 india 1st look, 
iPhone 14 first look in hindi, Technical Guruji, Technicalguruji, Gaurav Chaudhary, 13
```
## Example 4 (If Video Has no tags)
```python
import YoutubeTags
from YoutubeTags import videotags
tag = videotags("https://www.youtube.com/watch?v=Mlk888FiI8A") # Google Keynote video 2021 
if tag:
   print (tag)
else:
   print("No Tags Found")
```
### Output of Example 4
```
No Tags Found
```
# Channel Tags

## How to Use It

```python
import YoutubeTags
from YoutubeTags import channeltags
link = "Add Your Channel Link Here" # Use https / http Links
variable_name = channeltags(link)
print(variable_name)
```

> **_NOTE:_** ONLY SUPPORTS HTTP(S) , use HTTP(S) links to get the results 

## Example 1
```python
import YoutubeTags
from YoutubeTags import channeltags
findtags = channeltags("https://youtube.com/c/mkbhd") # Mkbhd's channel Link
print(findtags)
```
### Output of Example 1

```
 MKBHD, MarquesBrownlee, Marques, Brownlee 
```

## Example 2
```python
import YoutubeTags
from YoutubeTags import channeltags
tags = channeltags("https://youtube.com/c/Karikku_Fresh") # Karikku channel Link
print(tags)
```
### Output of Example 2

```
 karikku, media, digital, malayalam 
```
## Example 3
```python
import YoutubeTags
from YoutubeTags import channeltags
gettag = channeltags("https://youtube.com/c/TechnicalGuruji") # Technical Guruji channel Link
print(gettag)
```
### Output of Example 3
```
 Hindi Technology, Technology in Hindi, Hindi Tech Guru, Technical Guruji, Hindi Tech Tips, Tech Reviews, Mobile Tips and Tricks, Technology Explained,
 Hindi Tech, Hindi Tech Reviews, Tech Hindi, hindi, Technology, Mobile, tech, Reviews, TechnicalGuruji, Gaurav Chaudhary, Smartphones, Mobile Phones,
 Tech, latest Tech,Cool Technology, Tech News, Latest Tech News 
```
## Example 4
```python
import YoutubeTags
from YoutubeTags import channeltags
tag = channeltags("https://youtube.com/user/PewDiePie") # PewDiePie channel Link
print(tag)
```
### Output of Example 4
```
  pewdiepie, pewds, gaming, felix arvid ulf, felix, kjellberg 
```

# What's New in 1.5

Everything above still works exactly as before. The functions below are new; they return
Python lists / dicts and raise `YoutubeTags.YoutubeTagsError` (or a subclass) on failure
instead of returning `False`.

## Flexible links

Every function now also accepts `youtu.be/...`, `/shorts/...`, `/embed/...`, `/live/...` links,
bare 11-character video ids, links without `https://`, and channel `@handles`.

```python
from YoutubeTags import videotags, channeltags
print(videotags("RTbrXiIzUt4"))
print(videotags("https://youtu.be/RTbrXiIzUt4"))
print(channeltags("@mkbhd"))
```

## Full video info

```python
from YoutubeTags import get_video_info
info = get_video_info("https://www.youtube.com/watch?v=RTbrXiIzUt4")
print(info["title"], info["views"], info["tags"])
```

```
{
 "video_id": "RTbrXiIzUt4",
 "url": "https://www.youtube.com/watch?v=RTbrXiIzUt4",
 "title": "What Is Right To Repair?",
 "description": "Do you really own what you buy? ...",   # full description, not truncated
 "tags": ["Right To Repair", "right to repair", "MKBHD", ...],
 "hashtags": [],
 "channel_name": "Marques Brownlee",
 "channel_id": "UCBJycsmduvYEL83R_U4JriQ",
 "channel_url": "http://www.youtube.com/@mkbhd",
 "views": 4679645,
 "likes": 250306,
 "length_seconds": 1215,
 "category": "Science & Technology",
 "publish_date": "2021-05-07T18:03:28-07:00",
 "upload_date": "2021-05-07T18:03:28-07:00",
 "thumbnail": "https://i.ytimg.com/vi/RTbrXiIzUt4/maxresdefault.jpg",
 "is_live": false,
 "is_family_safe": true,
 "is_unlisted": false,
 "is_private": false
}
```

## Channel info

```python
from YoutubeTags import get_channel_info
print(get_channel_info("https://www.youtube.com/@mkbhd"))
```

```
{'channel_id': 'UCBJycsmduvYEL83R_U4JriQ', 'name': 'Marques Brownlee',
 'url': 'https://www.youtube.com/channel/UCBJycsmduvYEL83R_U4JriQ',
 'description': 'MKBHD: Quality Tech Videos | ...', 'tags': ['MKBHD', 'MarquesBrownlee', 'Marques', 'Brownlee'],
 'avatar': 'https://yt3.googleusercontent.com/...', 'subscribers': '1.17M subscribers', 'is_family_safe': 'true'}
```

## Tags as lists, hashtags

```python
from YoutubeTags import videotags_list, channeltags_list, hashtags
videotags_list("RTbrXiIzUt4")      # ['Right To Repair', 'right to repair', 'MKBHD', ...]
channeltags_list("@mkbhd")         # ['MKBHD', 'MarquesBrownlee', 'Marques', 'Brownlee']
hashtags("https://youtu.be/...")   # ['#shorts', '#tech']
```

## Tag ideas from YouTube search autocomplete

```python
from YoutubeTags import tag_suggestions
tag_suggestions("right to repair")              # ['right to repair', 'right to repair india', ...]
tag_suggestions("cricket", language="hi", region="IN")
```

## Tag SEO analysis

Checks your tags against YouTube Studio's 500-character limit and finds duplicates.
Accepts a list or the string returned by `videotags()`.

```python
from YoutubeTags import videotags, analyze_tags
analyze_tags(videotags("RTbrXiIzUt4"))
```

```
{'count': 10, 'unique_count': 9, 'total_characters': 164, 'character_limit': 500,
 'within_limit': True, 'duplicates': ['right to repair'], 'longest': 'right to repair movement',
 'average_length': 13.9}
```

## Many videos at once

```python
from YoutubeTags import bulk_videotags
bulk_videotags(["RTbrXiIzUt4", "Kbe3FKeCd1A"], max_workers=4)
# {'RTbrXiIzUt4': [...], 'Kbe3FKeCd1A': [...]}   failed links map to None
```

## Error handling

```python
from YoutubeTags import get_video_info, VideoUnavailable, InvalidURL, RequestFailed
try:
    get_video_info("https://www.youtube.com/watch?v=xxxxxxxxxxx")
except VideoUnavailable as e:
    print(e)   # Video xxxxxxxxxxx is unavailable: This video is unavailable
```

## Settings (timeout, retries, language, proxies)

```python
import YoutubeTags
YoutubeTags.configure(timeout=10, retries=3, language="en-US",
                      proxies={"https": "http://127.0.0.1:8080"})
```

Defaults: 15 second timeout, 2 retries on network errors / HTTP 429 / 5xx, YouTube picks the language.

## Command line

```
youtubetags https://www.youtube.com/watch?v=RTbrXiIzUt4       # tags
youtubetags RTbrXiIzUt4 Kbe3FKeCd1A --json                     # several videos, JSON
youtubetags --info RTbrXiIzUt4                                 # full metadata
youtubetags --analyze RTbrXiIzUt4                              # tag SEO analysis
youtubetags --channel @mkbhd                                   # channel tags
youtubetags --suggest "right to repair"                        # tag ideas
python -m YoutubeTags RTbrXiIzUt4                              # same, without the script
```

## Running the tests

```
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

The tests use saved HTML, so they never hit YouTube.

# License

<b>© 2021 Nuhman Pk , LICENSED under [MIT License](https://github.com/nuhmanpk/YoutubeTags/blob/main/LICENSE)</b>

## Github

Follow me on [Github](https://www.github.com/nuhmanpk) and if you find this [library](https://github.com/nuhmanpk/YoutubeTags) useful don't forget to add Your star

## Sponsor this project
[ko-fi](https://ko-fi.com/nuhmanpk)<br>
[paypal](https://www.paypal.me/nuhmanpk)<br>
[Buy me a Coffee](https://www.buymeacoffee.com/nuhmanpk)


## Credits : [thepythoncode](https://www.thepythoncode.com/)
This Project is based on small Snippet from [thepythoncode.com](https://www.thepythoncode.com/) as part of their Web Scrapping Modules. Do check their web site [here](https://www.thepythoncode.com/). 
