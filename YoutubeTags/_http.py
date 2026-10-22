"""HTTP layer: one place for headers, consent cookies, timeouts and retries."""
import time

import requests

from .exceptions import RequestFailed

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# Skips the EU cookie-consent interstitial, which otherwise hides every meta tag.
CONSENT_COOKIES = {"CONSENT": "YES+1", "SOCS": "CAI"}

_RETRY_STATUS = {429, 500, 502, 503, 504}

_config = {
    "timeout": 15,
    "retries": 2,
    "user_agent": DEFAULT_USER_AGENT,
    "language": None,
    "proxies": None,
}


def configure(timeout=None, retries=None, user_agent=None, language=None, proxies=None):
    """Change global request settings. Only the arguments you pass are updated.

    timeout    -- seconds to wait for YouTube (default 15)
    retries    -- extra attempts on network errors / 429 / 5xx (default 2)
    user_agent -- User-Agent header to send
    language   -- Accept-Language value, e.g. "en-US" (default: let YouTube decide)
    proxies    -- requests-style proxies dict, e.g. {"https": "http://host:port"}
    """
    for key, value in (
        ("timeout", timeout),
        ("retries", retries),
        ("user_agent", user_agent),
        ("language", language),
        ("proxies", proxies),
    ):
        if value is not None:
            _config[key] = value
    return dict(_config)


def _headers():
    headers = {"User-Agent": _config["user_agent"]}
    if _config["language"]:
        headers["Accept-Language"] = _config["language"]
    return headers


def get(url, params=None):
    """GET a URL with retries. Returns a requests.Response."""
    attempts = max(0, int(_config["retries"])) + 1
    last_error = None
    for attempt in range(attempts):
        try:
            response = requests.get(
                url,
                params=params,
                headers=_headers(),
                cookies=CONSENT_COOKIES,
                timeout=_config["timeout"],
                proxies=_config["proxies"],
            )
        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = e
        else:
            if response.status_code not in _RETRY_STATUS:
                return response
            last_error = RequestFailed(
                "HTTP %s for %s" % (response.status_code, url)
            )
        if attempt < attempts - 1:
            time.sleep(0.5 * (2 ** attempt))
    if isinstance(last_error, RequestFailed):
        raise last_error
    raise RequestFailed("Request to %s failed: %s" % (url, last_error))


def get_html(url, params=None):
    response = get(url, params=params)
    # requests falls back to ISO-8859-1 when the header has no charset; YouTube is UTF-8.
    if "charset" not in response.headers.get("Content-Type", "").lower():
        response.encoding = "utf-8"
    return response.text
