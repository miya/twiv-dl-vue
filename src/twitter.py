import re
from datetime import datetime
from twython import TwythonAuthError, TwythonRateLimitError, TwythonError

from src import twitter, jst


def get_tweet_id(url):
    """フロントで入力されたURLから正規表現を用いてツイートIDを抽出する"""
    tweet_id = re.findall('https://twitter\.com/.+?/status/(\d+)', url)
    if len(tweet_id) > 0:
        return tweet_id[0]


def get_rate_limit():
    """残りのAPI利用可能回数を取得する"""
    rate_limit_data = twitter.get_application_rate_limit_status()['resources']['statuses']['/statuses/lookup']
    reset_time = str(datetime.fromtimestamp(rate_limit_data['reset'], jst))
    limit = rate_limit_data['remaining']
    return {'remaining': limit, 'reset_time': reset_time}


def get_video_urls(video):
    """
    ビットレートの高さでソートする
    フロントで表示させる動画URLとダウンロードできる動画サイズを返す
    """
    sorted_bitrate = sorted(video)
    video_urls = {}
    count = 1
    for i in range(len(video)):
        video_url = video[sorted_bitrate[i]]
        video_urls.update({
            count: {
                'size': re.findall('vid/(.+)/', video_url)[0],
                'url': video[sorted_bitrate[i]]
            }
        })
        count += 1
    return video_urls, video[sorted_bitrate[-1]]


def get_video_data(tweet_id):
    """TwitterAPIを利用して動画のURLを取得する"""
    try:
        tweet_data = twitter.lookup_status(id=tweet_id, include_entities=True)
        rate_limit = get_rate_limit()
    except TwythonAuthError as e:
        print(e)
        return {'status': False, 'message': 'アプリケーションの認証に何らかの問題があります。'}
    except TwythonRateLimitError as e:
        print(e)
        return {'status': False, 'message': 'APIの呼び出し回数制限を超えました。時間をおいてからやり直してください。'}
    except TwythonError as e:
        print(e)
        return {'status': False, 'message': 'エラーが発生しました'}

    # ツイートが存在しているかどうか
    if len(tweet_data) > 0:

        # 動画、画像を含むメディア付きツイートかどうか
        if 'extended_entities' in tweet_data[0]:
            media = tweet_data[0]['extended_entities']['media'][0]

            # 動画付きツイートかどうか
            if media['type'] == 'video':

                # ビットレートとURLを取り出して辞書に追加
                video = {}
                for i in media['video_info']['variants']:
                    if i['content_type'] == 'video/mp4':
                        video.update({i['bitrate']: i['url']})
                download_video_urls, display_video_url = get_video_urls(video)

                return {
                    'status': True,
                    'message': '動画のURLを取得しました。',
                    'download_video_urls': download_video_urls,
                    'display_video_url': display_video_url,
                    'media_url': media['media_url'],
                    'rate_limit': rate_limit,
                    'tweet_info': {
                        'name': tweet_data[0]['user']['name'],
                        'screen_name': tweet_data[0]['user']['screen_name'],
                        'profile_image_url': tweet_data[0]['user']['profile_image_url'],
                        'tweet_text': tweet_data[0]['text'],
                        'created_at': tweet_data[0]['created_at']
                    }
                }

            else:
                return {'status': False, 'message': '動画付きツイートではありません。', 'rate_limit': rate_limit}

        else:
            return {'status': False, 'message': '動画付きツイートではありません。', 'rate_limit': rate_limit}

    else:
        return {'status': False, 'message': 'ツイートが見つかりませんでした。', 'rate_limit': rate_limit}
