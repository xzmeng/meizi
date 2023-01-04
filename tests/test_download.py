import os
import pytest
from meizi.download import download_album

def test_download(tmp_path):
    path = download_album(tmp_path, 'https://www.mmm131.com/qingchun/1319.html')
    files = os.listdir(path)
    assert len(files) == 7
    assert 'You are my sister' in path.name
