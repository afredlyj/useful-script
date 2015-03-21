__author__ = 'winnie'

import datetime
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict

import weibo


APP_KEY = '3810030607'
APP_SECRET = '46dc1f8f9a1c48a03d0c04eaa8734fc4'
ACCESS_TOKEN = '2.00BB3ovBZAVqJEfbdc317513YXwMUC'
client = weibo.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri="http://afredlyj.github.io/")
client.set_access_token(ACCESS_TOKEN, 157679999)
COUNT = 50

def getfavorites(page, count):

    response = client.favorites.get(page=page, count=count)
    ids = []
    # kv = OrderedDict()
    print 'get favorites ids response : %s' % response.favorites

    for id in response.favorites:
        ids.append(id.status)

    print 'favorites list size : %d' % len(ids)
    return ids


def getfavoritestotalcount():
    response = client.favorites.ids.get()
    return response.total_number

def dumpToEvernote(text = {}):
    file = 'weibo_favorite%s.txt' % datetime.datetime.now().strftime("%Y-%m-%d")
    # for detail in text:
    with open(file, 'aw') as f:
        for id in text.iterkeys():
            f.writelines(((str(id) + ' ' + text[id]).encode('utf-8').strip(), '\n'))


def start():

    total_number = getfavoritestotalcount()
    total_page = total_number / COUNT + 1
    print 'total number : %d, total page : %d' % (total_number, total_page)

    for page in range(1, total_page + 1):
        # get my favorites detail by page
        favorites = getfavorites(page, COUNT)
        text = _parse_favorites(favorites)
        dumpToEvernote(text)

'''
key : id
value : text
'''
def _parse_favorites(favorites):
    # text = []
    id2text = OrderedDict()
    for favorite in favorites:
        if hasattr(favorite, 'retweeted_status'):
            retweeted_status = favorite.retweeted_status
            if hasattr(retweeted_status, 'deleted'):
                continue
            print 'retweeted_status text : %s' % retweeted_status.text
            # text.append(retweeted_status.text)
            id2text[retweeted_status.id] = retweeted_status.text
        else:
            if hasattr(favorite, 'deleted'):
                continue
            print 'status text : %s' % favorite.text
            # text.append(favorite.text)
            id2text[favorite.id] = favorite.text
    return id2text


if __name__ == '__main__':
    start()