import re
import requests
from pathlib import Path
from functools import partial
from parsel import Selector
from urllib.parse import urljoin
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

logger.add('error.log', level='ERROR')

BASE_URL = 'https://www.mmm131.com/'

ALBUM_RE = re.compile(rf'^{BASE_URL}[a-z]+/[0-9]+.html$')
LIST_RE = re.compile(rf'^{BASE_URL}[a-z]+/(list_.*)?$')

session = requests.Session()
session.headers = {'Referer': BASE_URL}


def get_bytes(url):
    b = session.get(url).content
    return b


def get_selector(url):
    html = get_bytes(url).decode('gbk')
    return Selector(html)


def download_image(url, album_dir):
    filename = url.split('/')[-1]
    filepath = album_dir / filename
    b = get_bytes(url)
    with open(filepath, 'wb') as f:
        f.write(b)


def is_downloaded(data_dir, url):
    ok_list = data_dir / 'ok.txt'
    if not ok_list.exists():
        return False
    with open(ok_list) as f:
        urls = f.read().split('\n')
    return url in urls


def mark_downloaded(data_dir, url):
    ok_list = data_dir / 'ok.txt'
    with open(ok_list, 'a') as f:
        f.write(url + '\n')


def download_album(data_dir, album_url) -> Path:
    if is_downloaded(data_dir, album_url):
        logger.info(f'{album_url} is already downloaded.')
    sel = get_selector(album_url)
    album_name = sel.css('h5::text').get()
    count = int(re.search(r'共(\d+)页', sel.get()).group(1))
    image_url = sel.css('.content-pic img::attr(src)').get()
    prefix = image_url.rsplit('/', maxsplit=1)[0]
    image_urls = [f'{prefix}/{i}.jpg' for i in range(1, count + 1)]
    album_dir = data_dir / album_name
    album_dir.mkdir(parents=True, exist_ok=True)
    ok_count = 0
    for image_url in image_urls:
        try:
            download_image(image_url, album_dir)
            ok_count += 1
        except Exception as e:
            logger.error(f'{e} - {image_url} - {album_url}')
    msg = f'[{ok_count}/{count}] {album_name} - {album_url}'
    if ok_count == count:
        mark_downloaded(data_dir, album_url)
        logger.info(msg)
    else:
        logger.error(msg)
    return album_dir


def extract_links(page_url: str):
    sel = get_selector(page_url)
    links = sel.css('a::attr(href)').getall()
    links = [urljoin(page_url, link) for link in links]
    links = [link for link in links if link.startswith(BASE_URL)]
    album_links = [link for link in links if ALBUM_RE.match(link)]
    list_links = [link for link in links if LIST_RE.match(link)]
    return album_links, list_links


def bfs():
    seen_albums = set()
    seen_lists = set()
    deq = deque([BASE_URL])
    while deq:
        url = deq.pop()
        albums, lists = extract_links(url)
        albums = set(albums) - seen_albums
        seen_albums |= albums
        yield from albums
        lists = set(lists) - seen_lists
        seen_lists |= lists
        deq.extend(lists)


def main(max_workers, data_dir):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(partial(download_album, data_dir), bfs())
