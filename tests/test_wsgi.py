from meizi.wsgi import create_app
from meizi.download import download_album
import httpx


def test_wsgi(tmp_path):
    app = create_app(data_dir=tmp_path)
    with httpx.Client(app=app, base_url="http://testserver") as client:
        r = client.get("/")
        assert r.status_code == 200
        assert '共0结果' in r.text

        url = 'https://www.mmm131.com/qingchun/1319.html'
        download_album(tmp_path, url)

        r = client.get("/")
        assert r.status_code == 200
        assert '共1结果' in r.text
        assert 'You are my sister' in r.text
