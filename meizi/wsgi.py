import os
from flask import Flask, render_template, request
from os.path import dirname as d, join
from pathlib import Path


def list_albums(data_dir: Path):
    if not data_dir.exists():
        return []
    albums = os.listdir(data_dir)
    if 'ok.txt' in albums:
        albums.remove('ok.txt')
    return albums


def create_app(data_dir: Path):
    app = Flask(__name__, static_folder=data_dir, static_url_path='/static')

    @app.route('/')
    def list():
        titles = list_albums(data_dir)
        return render_template('list.html', titles=titles)

    @app.route('/album/<title>')
    def album(title):
        path = data_dir / title
        images = os.listdir(path)
        images = [join('/static', title, image) for image in images]
        return render_template('detail.html', images=images)

    @app.route('/search')
    def search():
        keyword = request.args.get('keyword', '')
        titles = list_albums(data_dir)
        results = [title for title in titles if keyword in title]
        return render_template('list.html', titles=results)

    return app
