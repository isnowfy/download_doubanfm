# coding: utf-8
 
import urllib, urllib2, cookielib, re, json, eyeD3, os

import download
import download_album

RE_ALBUM = re.compile(r'/subject/\d+/')

def html_decode(html):
    #return html.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    import HTMLParser
    return HTMLParser.HTMLParser().unescape(html)
 
def get(myurl, cookie):
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    req = urllib2.Request(myurl)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    req.add_header('Cookie', cookie)
    content = urllib2.urlopen(req, timeout=20).read()
    for s in json.loads(content)['songs']:
        sid = s['id']
        album = RE_ALBUM.search(s['path']).group(0)
        try:
            print "song:" + html_decode(s['title']) + "\nsinger:" + html_decode(s['artist']) + "\nalbum:" + s['path']
        except:
            print 'song...'
        try:
            ssid = download_album.get_ssid(album, sid)
            if download.handle(sid, ssid):
                print 'succeed!\n\n'
            else:
                print 'fail!\n\n'
        except:
            print 'fail!\n\n'
 
def main():
    url = 'http://douban.fm/j/play_record?type=liked&start=%d'
    cookie = raw_input('cookie:')
    print 'you should enter the pages you want to download'
    page0 = int(raw_input('page from:'))
    page1 = int(raw_input('page to:'))
    for i in range(page1-page0+1):
        get(url%((i+page0-1)*15), cookie)
 
if __name__ == '__main__':
    main()
