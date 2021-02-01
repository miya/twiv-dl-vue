import requests
from io import BytesIO
from flask import request, jsonify, send_file, render_template

from src import app
from src.twitter import get_tweet_id, get_video_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    if request.headers['Content-Type'] == 'application/json':
        input_url = request.json['inputUrl']
        tweet_id = get_tweet_id(input_url)
        if not tweet_id:
            return jsonify({'status': False, 'message': 'Twitterの動画付きツイートではありません。'})
        video_data = get_video_data(tweet_id)
        print(video_data)
        return jsonify(video_data)


@app.route('/download', methods=['POST'])
def download():
    if request.headers['Content-Type'] == 'application/json':
        download_url = request.json['downloadUrl']
        req = requests.get(download_url)
        if req.status_code == 200:
            video_obj = BytesIO(req.content)
            return send_file(video_obj, mimetype='video/mp4', attachment_filename='video.mp4', as_attachment=True)
