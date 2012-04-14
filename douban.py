# coding: utf-8
 
from BeautifulSoup import BeautifulSoup
import urllib,urllib2,cookielib,re
 
def handle(s):
    return s.replace("&lt;","<").replace("&gt;",">").replace("\\","")
   
def fhandle(s):
    return s.replace("/","and").replace(" ","")
 
def get(myurl,cookie):
    url2="http://douban.fm/j/mine/playlist?type=n&h=&channel=0&context=channel:0|subject_id:%d"
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
    urllib2.install_opener(opener)
    req=urllib2.Request(myurl)
    req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    req.add_header('Cookie',cookie)
    content=urllib2.urlopen(req).read()
    soup=BeautifulSoup(str(content))
    soup=soup.find("div", { "id" : "record_viewer" })
    for div in soup.findAll("div", { "class" : "info_wrapper" }):
      div=div.find("div",{ "class" : "song_info" })
      a=div.contents[1]
      p1,p2,p3=div.contents[3].findAll("p")
      print a["href"]+"\nsong:"+handle(p1.string)+"\nsinger:"+handle(p2.string)+"\nalbum:"+handle(p3.a.string)
      p=re.compile(r'(\d+)')
      m=p.search(a["href"])
      num=int(m.groups()[0])
      url3=url2%num
      print url3
      mark=False
      try:
          for j in range(100):
              content=urllib2.urlopen(url3).read()
              c=eval(content)
              c=c['song']
              for i in c:
                  if unicode(str(i['title']),'utf-8')==handle(p1.string):
                      urllib.urlretrieve(i['url'].replace('\\',''), fhandle(handle(p1.string))+"-"+fhandle(handle(p2.string))+".mp3")
                      mark=True
                      break
              if mark:
                  break
          if mark:
              print "succeed!\n"
          else: print "fail!\n"
      except Exception as e:
          print e.message
 
def main():
    url="http://douban.fm/mine?start=%d&type=liked"
    cookie=raw_input('cookie:')
    print "you should enter the pages you want to download"
    page0=int(raw_input('page from:'))
    page1=int(raw_input('page to:'))
    for i in range(page1-page0+1):
        get(url%((i+page0-1)*15),cookie)
 
if __name__ == "__main__":
    main()
