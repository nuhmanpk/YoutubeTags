import requests
import logging
from bs4 import BeautifulSoup


def videotags(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        tags = ', '.join([meta.attrs.get("content") for meta in soup.find_all(
            "meta", {"property": "og:video:tag"})])
        return tags
    except Exception as e:
        logging.error(e)
        return False


def channeltags(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        tags = ', '.join([meta.attrs.get("content") for meta in soup.find_all(
            "meta", {"property": "og:video:tag"})])
        return tags
    except Exception as e:
        logging.error(e)
        return False


def videotitle(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        title = soup.find("title").text.strip()
        return title
    except Exception as e:
        logging.error(e)
        return False


def videodescription(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        description = soup.find("meta", {"name": "description"}).attrs.get("content")
        return description
    except Exception as e:
        logging.error(e)
        return False


def channeldescription(url):
    try:
        request = requests.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        description = soup.find("meta", {"name": "description"}).attrs.get("content")
        return description
    except Exception as e:
        logging.error(e)
        return False
