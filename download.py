# coding: utf-8
 
import urllib, urllib2, cookielib, re, json, eyeD3, os

songs_dir = 'songs'
base_url = 'http://douban.fm/j/mine/playlist?type=n&sid=&pt=0.0&channel=0&from=mainsite&kbps=%d'
invalid = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

def valid_filename(s):
    return filter(lambda x:x not in invalid, s)

def get_songs_information(sid, ssid, kbps=64, cookie=None):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    prereq = urllib2.Request('http://douban.fm?start=%sg%sg' % (sid, ssid))
    prereq.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    urllib2.urlopen(prereq, timeout=60).read()
    req = urllib2.Request(base_url % kbps)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    if cookie is not None:
        for c in cj:
            cookie += '; ' + c.name + '=' + c.value
        req.add_header('Cookie', cookie)
    ret = json.loads(urllib2.urlopen(req, timeout=60).read())
    return ret['song']

def download(song):
    try:
        os.mkdir(songs_dir)
    except:
        pass
    filename = '%s-%s.mp3' % (valid_filename(song['artist']) , valid_filename(song['title']))
    filepath = os.path.join(songs_dir, filename)
    if os.path.exists(filepath):
        return
    urllib.urlretrieve(song['url'], filepath)
    picname = song['picture'][1+song['picture'].rindex('/'):]
    picpath = os.path.join(songs_dir, picname)
    urllib.urlretrieve(song['picture'].replace('mpic','lpic'), picpath)
    tag = eyeD3.Tag()
    tag.link(filepath)
    tag.header.setVersion(eyeD3.ID3_V2_3)
    tag.encoding = '\x01'
    tag.setTitle(song['title'])
    tag.setAlbum(song['albumtitle'])
    tag.setArtist(song['artist'])
    tag.setDate(song['public_time'])
    tag.addImage(3, picpath)
    os.remove(picpath)
    tag.update()	

def handle(sid, ssid, kbps=64, cookie=None):
    try:
        songs = get_songs_information(sid, ssid, int(kbps), cookie)
        for song in songs:
            if sid == song['sid']:
                download(song)
                return True
    except:
        pass
    return False
