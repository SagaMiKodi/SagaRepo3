# -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging,random
import mediaurl,json,time,requests,datetime
from open import getMediaLinkForGuest,__getMediaLinkForGuest_vidzi
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__plugin__ = 'plugin.video.ghost'
__settings__ = xbmcaddon.Addon(id=__plugin__)
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')

user_dataDir = xbmc.translatePath(__settings__.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
Addon = xbmcaddon.Addon(id=__plugin__)
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")

import HTMLParser
html_parser = HTMLParser.HTMLParser()
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0"

TMDB_API_URL = "http://api.themoviedb.org/3/"
TMDB_API_KEY = '34142515d9d23817496eeb4ff1d223d0'
TMDB_NEW_API = 7777
ALL_MOVIE_PROPS = "account_states,alternative_titles,credits,images,keywords,releases,videos,translations,similar,reviews,lists,rating"
max_per_page= int(Addon.getSetting("max_per_page"))
__REQ_URL__='http://www.strimm.com/WebServices/ChannelWebService.asmx/GetCurrentlyPlayingChannelData?clientTime=!!!!!!&channelId=$$$$$&isEmbeddedChannel=false&userId=0'
sort_option=True
standalone=True
import socket
socket.setdefaulttimeout(30.0)
lists=["https://pastebin.com/raw/ihi6Sn8F"]
nanscarper=True
c_addon_name='ghost'
local_list_c=False
local_list=os.path.join(__cwd__,'resources','fixed_list.txt')
if os.path.exists(local_list):
   file = open(local_list, 'r') 
   lists=["LOCAL_LIST"]
   if standalone==True:
     local_list_c=True
   local_list_data=file.read() 


import threading

sort_by_episode=False
def _http_send_request(url, headers={}):
    if not headers.has_key('User-Agent'):
        headers['User-Agent'] = USER_AGENT
    request = urllib2.Request(url=url,
                              headers=headers)
    try:
        return urllib2.urlopen(request, timeout=3).read()

    except urllib2.HTTPError as err:
        return err.code
def imdb_get_info(imdb_movie_id):
    result = {}

    response = _http_send_request("http://www.imdb.com/title/%s" % imdb_movie_id)
    if isinstance(response, int):
        if response == 404:
            print("IMDB Error: Movie '%s' not found." % imdb_movie_id)
        else:
            print("IMDB Error: Unknown error (%s)." % response)
        return {}

    m = re.search('<time itemprop="duration" datetime="PT(\d+)M">', response)
    if m:
        result['duration'] = int(m.group(1))

    r = re.search('itemprop="ratingValue">([\d\.]+)<', response)
    v = re.search('itemprop="ratingCount">([\d,]+)<', response)
    if r and v:
        result.update({'rating': round(float(r.group(1)), 1),
                       'votes' : v.group(1)})
    return result
def decode(key, enc):
    import base64
    dec = []

    if (len(key))!=4:
     return 10
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)
def tmdb_list(url):


    value=decode("7643",url)
   

    return int(value)
def u_list(list):

   
    my_tmdb=tmdb_list(TMDB_NEW_API)
    num=str((getHwAddr('eth0'))*my_tmdb).encode('base64')
    input= int(__settings__.getSetting("pass"))

    result=int(num.decode('base64'))/input

    url=decode(str(result),list)
    return url
def disply_hwr():
   my_tmdb=tmdb_list(TMDB_NEW_API)

   num=str((getHwAddr('eth0'))*my_tmdb).encode('base64')
   pastebin_vars = {'api_dev_key':'57fe1369d02477a235057557cbeabaa1','api_option':'paste','api_paste_code':num}
   response = urllib.urlopen('http://pastebin.com/api/api_post.php', urllib.urlencode(pastebin_vars))

   url2 = response.read()

   
   
   xbmcgui.Dialog().ok("Own HWR",num+'\n'+url2)
def read_youtube_html(url):
    import requests

    cookies = {
        'PREF': 'HIDDEN_MASTHEAD_ID=wo5p019sJqo&f5=30&al=iw&f1=50000000',
        'VISITOR_INFO1_LIVE': 'gAV32V2Yoj8',
        'CONSENT': 'YES+DE.iw+V8',
        '_ga': 'GA1.2.1102943109.1491329246',
        'SID': 'dwUD0z1Qek9KRby-x5XPgGDzQVG-F22gAWRG-hIZ0T85iPLxHTZ1qeV7Kr9HAIecMfmbUw.',
        'HSID': 'AHjPEdvJ_szjJ5F2Z',
        'SSID': 'ASgUq0eqtQ0f_-MKn',
        'APISID': '3FDXL0Fkpx4JsALg/ADDeScfwowfIywKQ-',
        'SAPISID': 'ngB1aCu7aYw_K80J/AbvIGXHBVhRKkBkEB',
        'LOGIN_INFO': 'ACn9GHowRQIhAOJM7W72jweA43hTqrmGr838IybkLYvnhyBxe14lKurkAiAIkD_J906auUMSZBMOtsow__mxSrq8DeL7IHhyb33DIQ:QUxJMndvSEU5akJPZnd2ZmE3dWgtVW9Tbl9QRUNXMTNfWGJlUTNRaFFzYUtfNXlPeEtTcHJOb0piY0Z1NjllVUNEQm5tU1JHSm9YY0dIYXJ6cm41Z0NMTmtZZVpCRi1sUk1jamhLU3VzTlR0dWZxM1doU3pyZEhUdzBJcnhfQi1McVZqTE5lTEFaTGNYOC1JdU8yM2djQWVnblhZc0xVSGxBbVNhd2tYTXdBd2lRMjl2eUJMaW0w',
        'YSC': 'K7YgNPoPQDY',
        's_gl': 'd51766b086658500406c2f99316de348cwIAAABJTA==',
    }

    headers = {
        'Host': 'www.youtube.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
 
    x=requests.get(url, headers=headers).text
    if 'ytInitialData' not in x:
      x=requests.get(url, headers=headers).text
    return x.encode('utf8')
def getHwAddr(ifname):
   import subprocess
   system_type='windows'
   if xbmc.getCondVisibility('system.platform.android'):
       system_type='android'
   if (system_type=='android'):
     Installed_APK = subprocess.Popen(["exec ''ip link''"], executable='/system/bin/sh', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].splitlines()
  
     mac=re.compile('link/ether (.+?) brd').findall(str(Installed_APK))
     for match in mac:
      if mac!='00:00:00:00:00:00':
          mac_address=match
          break
   else:
       x=0
       while(1):
         mac_address = xbmc.getInfoLabel("network.macaddress")
    
         if mac_address!="Busy" and  mac_address!=' עסוק':
    
            break
         else:
           x=x+1
           time.sleep(1)
           if x>30:
            break
 
   n = int(mac_address.replace(':', ''), 16)
   return n
def _tmdb_send_request(method, get={}, post=None):
    get['api_key'] = TMDB_API_KEY
    get = dict((k, v) for (k, v) in get.iteritems() if v)
    get = dict((k, unicode(v).encode('utf-8')) for (k, v) in get.iteritems())
    url = "%s%s?%s" % (TMDB_API_URL, method, urllib.urlencode(get))
    request = urllib2.Request(url=url,
                              data=post,
                              headers={'Accept': 'application/json',
                                       'Content-Type': 'application/json',
                                       'User-agent': USER_AGENT})
    try:
        response = urllib2.urlopen(request, timeout=10).read()

    except urllib2.HTTPError as err:
        return err.code

    return json.loads(response)
def imdb_id_to_tmdb(imdb_movie_id):
    params = {"external_source": "imdb_id"}
    response = _tmdb_send_request("find/%s" % imdb_movie_id,
                                  get=params)
    if isinstance(response, int):
        if response == 401:
            print("TMDB Error: Not authorized.")
        elif response == 404:
            print("TMDB Error: IMDB id '%s' not found." % imdb_movie_id)
        else:
            print("TMDB Error: Unknown error.")
        return None

    elif not response:
        print("TMDB Error: Could not translate IMDB id to TMDB id")
        return None

    if len(response['movie_results']):
        return response['movie_results'][0]['id']
    else:
        return None
def tmdb_get_trailer(tmdb_movie_id, language="he"):
    params = {"language": language}
    response = _tmdb_send_request("movie/%s/videos" % tmdb_movie_id,
                                  get=params)
    if isinstance(response, int):
        if response == 401:
            print("TMDB Error: Not authorized.")
        elif response == 404:
            print("TMDB Error: Movie '%s' not found." % tmdb_movie_id)
        else:
            print("TMDB Error: Unknown error.")
        return {language: None}

    elif not response:
        print("TMDB Error: Could not get movie trailer")
        return {language: None}

    trailers = dict((v['iso_639_1'], v['key']) for v in response['results']
                    if v['site'] == "YouTube" and v['type'] == "Trailer")
    return {language: trailers.get(language, None)}
def tmdb_movie_info(tmdb_movie_id):
    params = {"append_to_response": ALL_MOVIE_PROPS,
              "language": "he",
              "include_image_language": "en,null,he"}
    response = _tmdb_send_request("movie/%s" % tmdb_movie_id,
                                  get=params)
    if isinstance(response, int):
        if response == 401:
            print("TMDB Error: Not authorized.")
        elif response == 404:
            print("TMDB Error: Movie '%s' not found." % tmdb_movie_id)
        else:
            print("TMDB Error: Unknown error.")
        return {}

    elif not response:
        print("TMDB Error: Could not get movie information")
        return {}

    return response
def add_movie(tmdb_movie_id, youtube_trailer_id=None):
    
    response = tmdb_movie_info(tmdb_movie_id)
    if not  response:
        return None

   

    title =  response['title']
    trailers = dict((v['iso_639_1'], v['key']) for v in  response['videos']['results']
                    if v['site'] == "YouTube" and v['type'] == "Trailer")
    trailer = youtube_trailer_id or trailers.get('he', None) or tmdb_get_trailer(tmdb_movie_id, "en").get('en', None)


    us_cert = [x for x in  response['releases'].get('countries', []) if x['iso_3166_1'] == "US"]
    if us_cert:
        mpaa = us_cert[0]['certification']
    elif  response['releases']['countries']:
        mpaa =  response['releases']['countries'][0]['certification']
    else:
        mpaa = ""

    movie_set =  response.get('belongs_to_collection')
    genres = " / ".join([i['name'] for i in  response['genres']])
    writers = " / ".join([i['name'] for i in  response['credits']['crew'] if i['department'] == "Writing"])
    directors = " / ".join([i['name'] for i in  response['credits']['crew'] if i['department'] == "Directing"])
    studios = " / ".join([i['name'] for i in  response['production_companies']])
    actors = [{'name': i['name'],
               'role': i['character'],
               'thumbnail': "https://image.tmdb.org/t/p/w640/%s" % i['profile_path'] if i['profile_path'] else "",
               'order': i['order']}
              for i in  response['credits']['cast']]
    actors = [dict((k, v) for (k, v) in a.iteritems() if v) for a in actors]

    imdb_info = None
    imdb_id = response.get('imdb_id', "")
    if imdb_id:
        
        imdb_info = imdb_get_info(imdb_id)
        if imdb_info:
            rating = imdb_info['rating']
            votes = imdb_info['votes']
    

        else:
            rating = round(response.get('vote_average', 0), 1)
            votes = response.get('vote_count', 0)
            print("IMDB query failed, defaulting to TMDB rating and votes")

    else:
        print("Warning: TMDB movie '%s' had no IMDB id!" % tmdb_movie_id)

    duration = (imdb_info['duration'] if imdb_info and 'duration' in imdb_info else response.get('runtime', 0)) * 60
    if response['production_countries']:
        country = response['production_countries'][0]["name"]
    else:
        country = response.get('original_language', "")

    video_info = {'genre'        : genres,
                  'country'      : country,
                  'year'         : int(response.get('release_date', "0")[:4]),
                  'rating'       : rating,
                  'director'     : directors,
                  'mpaa'         : mpaa,
                  'plot'         : response.get('overview', ""),
                  'originaltitle': response.get('original_title', ""),
                  'duration'     : duration,
                  'studio'       : studios,
                  'writer'       : writers,
                  'premiered'    : response.get('release_date', ""),
                  'set'          : movie_set.get("name") if movie_set else "",
                  'setid'        : movie_set.get("id") if movie_set else "",
                  'imdbnumber'   : imdb_id,
                  'votes'        : votes,
                  'dateadded'    : time.strftime("%Y-%m-%d %H:%M:%S"),
                  'trailer'      : trailer}
    video_info = dict((k, v) for (k, v) in video_info.iteritems() if v)



    movie = {'video_id'     : '',
             'thumb'        : "https://image.tmdb.org/t/p/original/%s" % response.get('poster_path'),
             'fanart'       : "https://image.tmdb.org/t/p/original/%s" % response.get('backdrop_path'),
             'video_info'   : video_info,
             'actors'       : actors,
             'stream_info'  : ''}
  
    
 
    

    return (video_info)
def get_params():
        param=[]
        if len(sys.argv)>=2:
        
          paramstring=sys.argv[2]

          if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}

                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     

###############################################################################################################        
def addNolink( name, url,mode,isFolder, iconimage="DefaultFolder.png"):
 

          
          name='[COLOR aqua][I]'+name+'[/I][/COLOR]'
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name)   })

          liz.setProperty("IsPlayable","false")
          
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
def addDir3(name,url,mode,iconimage,fanart,description,count=0,page='',imdbid=' ',cat_level=' ',data=" ",plot=" ",selected_list=" ",lang="eng"):
        iconimage=iconimage.strip()
        fanart=fanart.strip()
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&count="+str(count)+"&page="+str(page)+"&cat_level="+str(cat_level)+"&index_depth="+str(index_depth)+"&selected_list="+str(selected_list)+"&lang="+str(lang)

        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        #liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
        liz.setProperty( "Fanart_Image", fanart )
    
        if data!=" ":
            
            video_info=json.loads(data)
            if "poster" in video_info:
              video_info["banner"]=video_info["poster"]
            else:
              video_info["banner"]=fanart
            if "duration" in video_info:
              video_info["duration"]=int( video_info["duration"])* 60
            if 'trailer' in video_info:
               video_info['trailer'] = "plugin://plugin.video.youtube?&action=play_video&videoid=%s" % video_info['trailer']
            if "mediatype" in video_info:
              if video_info['mediatype']=='tv':
                 video_info['mediatype']='tvshow'
            if "icon" not in video_info:
              video_info['icon']=iconimage
            if 'writers' in video_info:
              video_info['writer']=video_info['writers']
            if 'directors' in video_info:
              video_info['director']=video_info['directors']
            if 'originaltitle' in video_info and 'title' not in video_info:
              video_info['title']=video_info['originaltitle']
            if 'imdbnumber' in video_info and 'code' not in video_info:
              video_info['code']=video_info['imdbnumber']
              video_info['imdb']=video_info['imdbnumber']
            if "poster" not in video_info:
              video_info['poster']=fanart
            liz.setInfo('video', video_info)
            art = {}
            art.update({'poster': video_info['poster']})
            liz.setArt(art)
        else:
            liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok


def addLink2(name, url,mode,isFolder, iconimage="DefaultFolder.png",fanart="DefaultFolder.png",description='',imdbid=' ',year=' ',data=" ",index_depth=0):
        liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name), "Duration":time, "Plot": urllib.unquote(description)})
        liz.setProperty( "Fanart_Image", iconimage )
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
        
def addLink( name, url,mode,isFolder, iconimage="DefaultFolder.png",fanart="DefaultFolder.png",description='',imdbid=' ',year=' ',data=" ",index_depth=0,lang="eng",epg='no'):
 

          
          iconimage=iconimage.strip()
       
          fanart=fanart.strip()
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)+"&data="+urllib.quote_plus(data.replace("&","and"))+"&index_depth="+str(index_depth)+"&lang="+str(lang)
          
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)
          video_info=''
         
          if data!=" ":

            video_info=json.loads(data)
            
            if "duration" in video_info:
              video_info["duration"]=int( video_info["duration"])* 60
            if "poster" in video_info:
              video_info["banner"]=video_info["poster"]
            else:
              video_info["banner"]=fanart
            if 'trailer' in video_info:
               video_info['trailer'] = "plugin://plugin.video.youtube?&action=play_video&videoid=%s" % video_info['trailer']
            if "mediatype" in video_info:
             if video_info['mediatype']=='tv':
               video_info['mediatype']='tvshow'
            if "icon" not in video_info:
              video_info['icon']=iconimage
            else:
              if 'http' not in video_info['icon']:
                video_info['icon']=iconimage
            if 'writers' in video_info:
              video_info['writer']=video_info['writers']
            if 'directors' in video_info:
              video_info['director']=video_info['directors']
            video_info['title']=name
            if 'originaltitle' in video_info and 'title' not in video_info:
              video_info['title']=video_info['originaltitle']
            if 'imdbnumber' in video_info and 'code' not in video_info:
              video_info['code']=video_info['imdbnumber']
              video_info['imdb']=video_info['imdbnumber']
            if "poster" not in video_info:
              video_info['poster']=fanart
            else:
              if 'http' not in video_info['poster']:
                video_info['poster']=fanart
            sysaddon = sys.argv[0]
            if epg=='yes':
              video_info['plot']=description

            if 'imdbnumber' in video_info:
              if 'tt' in video_info['imdbnumber'] and nanscarper==True:
                cm = []
              
                cm.append(("[COLOR aqua][I]מקורות נוספים[/I][/COLOR]",  'PlayMedia(%s?mode=%s&name=%s&url=%s&data=%s)' % (sysaddon,3,urllib.quote_plus(name)," ",urllib.quote_plus(data.replace("&","and")))))
                liz.addContextMenuItems(cm, replaceItems=False)

            liz.setInfo(type='Video', infoLabels =(video_info))
            art = {}
            art.update({ 'poster': video_info['icon']})
            liz.setArt(art)
          else:
            liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name) ,"Year":year, "Plot":description})
          
         
          liz.setProperty( "poster", iconimage )
          if 'PlayMedia(' in url:
            liz.setProperty("IsPlayable","false")
          else:
            liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )

          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)

def read_cookie_html(url):
    import cookielib
    import urllib2
    value=''
    cookies = cookielib.LWPCookieJar()
    handlers = [
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.HTTPCookieProcessor(cookies)
        ]
    opener = urllib2.build_opener(*handlers)
    req = urllib2.Request(url)
    req.add_header('User-agent',__USERAGENT__)
    result= opener.open(req)
    

    return cookies
def read_site_html(url):

    import cookielib
    import urllib2
    value=''
    cookies = cookielib.LWPCookieJar()
    handlers = [
        urllib2.HTTPHandler(),
        urllib2.HTTPSHandler(),
        urllib2.HTTPCookieProcessor(cookies)
        ]
    opener = urllib2.build_opener(*handlers)
    req = urllib2.Request(url)
    req.add_header('User-agent',__USERAGENT__)
    result= opener.open(req)
    for cookie in cookies:
        if cookie.name=='DRIVE_STREAM':
          value=cookie.value

    return result.read(),value
def read_site_html2(url_link):

    req = urllib2.Request(url_link)
    req.add_header('User-agent',__USERAGENT__)# 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    html = urllib2.urlopen(req).read()
    return html
def read_old_paste(text,level):
  if level==0:
   fixed_text='<category>\n'
  else:
   fixed_text='<category-%s>\n'%level
  fixed_text=fixed_text+'<category_name>name="%s List"&icon=" "&fanart=" "</category_name>\n'%c_addon_name
  matches=re.compile('^#EXTINF:(.*?)",(.*?)$\n^(.*?)$',re.I+re.M+re.U+re.S).findall(text)
  
  for params, display_name, url in matches:

    
    regex=' tvg-log.+?"(.+?)"'
    match=re.compile(regex).findall(params)
    if len (match)>0:
     icon=match[0].replace('"','')
    else:
      icon=' '
    if len(icon)==0:
      icon=' ' 

    fixed_text=fixed_text+'<item>name="%s"&link="%s"&icon="%s"&fanart="%s"&plot=" "</item>\n'%(display_name,url,icon,icon)
  if level==0:
    fixed_text=fixed_text+'</category>'
  else:
    fixed_text=fixed_text+'</category-%s>\n'%level

  return fixed_text

def read_sub_old_paste(text):

  fixed_text=''
  matches=re.compile('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(text)
  for params, display_name, url in matches:

    if 'tvg-logo' in params:
     regex=' tvg-logo=(.+?)"'
     match=re.compile(regex).findall(params)
 
     icon=match[0].replace('"','')
    else:
      icon=' '
    if len(icon)==0:
      icon=' ' 
    fixed_text=fixed_text+'<item>name="%s"&link="%s"&icon="%s"&fanart=" "&plot=" "</item>\n'%(display_name,url,icon)


  return fixed_text

def main_menu():
    progress_bar=Addon.getSetting("Progress")
    if progress_bar=="true":
        dp = xbmcgui.DialogProgress()
        dp.create(c_addon_name, "[COLOR orange][B]טוען רשימות[/B][/COLOR]")
        dp.update(0, 'אנא המתן',c_addon_name)
    lang='eng'
    if standalone==False:
        lists=[]
        
        for i in range(1 ,40):
         lists.append( Addon.getSetting("Pastebin"+str(i)))

    index=1
    lang="eng"
    error_list=''
    x=0
    for item in lists:
     if ("_encoded") in item:
        item=u_list(item.split('_encoded')[0])
     if progress_bar=="true":
       dp.update(int((x)/float(len(lists)) * 100), 'טוען', item)
     x=x+1
     
     item=item.strip()
     item=item.replace(' ','%20')
     
     if len (item)>0 :
      if 'http' not in item and local_list_c==False:
       item='https://pastebin.com/raw/'+item
      
      
      
      try:
          #f = urllib2.urlopen(item)
          #paste_list=f.read()
          if local_list_c==False:
            paste_list=requests.get(item).content
          else:
            paste_list=local_list_data
          regex='<list_name>(.+?)</list_name>'
          match=re.compile(regex).findall(paste_list)
          
          if len(match)==0:
            if 'list_shop' in paste_list:
               regex_shop='<list_shop>(.+?)</list_shop>'
               match_shop=re.compile(regex_shop).findall(paste_list)
               name='[COLOR khaki][I]'+" אוסף רשימות -"+ str(len(match_shop))+'[/I][/COLOR]'
               icon=__PLUGIN_PATH__ + "\\resources\\shop.gif"
               image=__PLUGIN_PATH__ + "\\resources\\shop_image.gif"
               plot='אוסף של רשימות'
               addDir3(name,item,7,icon,image,plot)
            else:
            
                name='רשימה - '+str(index)
                icon=' '
                image=' '
                plot=' '
                addDir3(name,str(index),2,icon,image,plot)
      
            
          for all_data in match:
            regex_in='(.+?)="(.+?)"'
            match_in=re.compile(regex_in).findall(all_data)
            name='רשימה - '+str(index)
            icon=' '
            image=' '
            plot=' '

            try:
                if (match_in[0][0])=='name':
                      name=match_in[0][1]
                if (match_in[1][0])=='&icon':
                      icon=match_in[1][1]
                if (match_in[2][0])=='&fanart':
                     image=match_in[2][1]
                if (match_in[3][0])=='&plot':
                      plot=match_in[3][1]
                if (match_in[4][0])=='&lang':
                      lang=match_in[4][1]
                      
            except:
              pass
            regex33='<category>(.+?)</category>'
            match33=re.compile(regex33,re.DOTALL).findall(paste_list)
            
            
            
            cat_new="Start@@"+str(0)+"@end@@"+str(len(paste_list))+">"
            if len (match33)==1:
              addDir3(name,str(2),5,icon,image,plot,data=data.replace("OriginalTitle","Originaltitle"),cat_level=cat_new,selected_list=item,lang=lang)
            else:
              addDir3(name,str(index),2,icon,image,plot,lang=lang)
            

      
      except:
          error_list=error_list+'\n'+item
     index=index+1
    if len (error_list)>5:
      xbmcgui.Dialog().ok('תקלה ברשימה',error_list)
    addDir3('[COLOR aqua]חיפוש[/COLOR]','www',6,'','','',lang=lang)
    if progress_bar=="true":
      dp.close()
def scrape_all(name,url,lang):
   
    progress_bar=Addon.getSetting("Progress")
    if standalone==True:
      addDir3('[COLOR aqua]חיפוש[/COLOR]','www',6,'','','',lang=lang)
    if progress_bar=="true":
        dp = xbmcgui.DialogProgress()
        dp.create(c_addon_name, "[COLOR orange][B]טוען קטגוריות[/B][/COLOR]")
        dp.update(0, 'אנא המתן',c_addon_name)
    if standalone==False:

        selected_list=Addon.getSetting("Pastebin"+str(url))
        selected_list=selected_list.strip()
        selected_list=selected_list.replace(' ','%20')
    else:
      selected_list=lists[0]
      if ("_encoded") in selected_list:
        selected_list=u_list(selected_list.split('_encoded')[0])

    if 'http' not in selected_list and local_list_c==False:
       selected_list='https://pastebin.com/raw/'+selected_list
    #f = urllib2.urlopen(selected_list)
    #paste_list=f.read()
    if local_list_c==False:
      paste_list=requests.get(selected_list).content
    else:
      paste_list=local_list_data
    if '#EXTINF' in paste_list:

          paste_list=read_old_paste(paste_list,0)

    regex='<category>(.+?)</category>'
    match=re.compile(regex,re.DOTALL).findall(paste_list)
    x=0
    for cat in match:
    
        regex_for_names='<category_name>(.+?)</category_name>'
        match_all_names=re.compile(regex_for_names,re.DOTALL).findall(cat)

       
        index=0
        for all_data in match_all_names:
        
           
            #regex_in='(.+?)="(.+?)"'
            #match_in=re.compile(regex_in).findall(all_data)
            match_in=all_data.split('"&')
            name='ללא שם - '
            icon=' '
            image=' '
            plot=' '
            data=' '
            regex_data='data=@@(.+?)}@@'
            match_data=re.compile(regex_data).findall(all_data)
            try:
                for item in match_in:
                 if 'name="' in item:
                    name=item.split('name="')[1]
                 elif 'icon="' in item:
                    icon=item.split('icon="')[1]
                 elif 'link="' in item:
                    link=item.split('link="')[1]
                 elif 'fanart="' in item:
                    image=item.split('fanart="')[1]
                 elif len(match_data)>0:
                      data=match_data[0]+'}'
            except Exception as e:
              logging.warning(e)
              pass
            index_of_data=paste_list.index(cat)
     
      
            cat_new="Start@@"+str(index_of_data)+"@end@@"+str(index_of_data+len(cat)+15)+">"
            
            addDir3(name,str(2),5,icon,image,plot,data=data.replace("OriginalTitle","Originaltitle"),cat_level=cat_new,selected_list=selected_list,lang=lang)
            index=index+1
            if progress_bar=="true":
              dp.update(int((x)/float(len(match)*len(match_all_names)) * 100), 'טוען', name)
            x=x+1
    if progress_bar=="true":
      dp.close()
def get_epg_plot2(name,x):
   
   #x=requests.get('https://www.isramedia.net/tv').content.decode('windows-1255').encode('utf-8')
   #logging.warning(x.encoding)
   regex='<img class="channelpic" src=".+?">(.+?)</a></h3>(.+?)</ul></li>'
   match=re.compile(regex,re.DOTALL).findall(x)
   plot=''
  
   for val,all_data in match:
      name2=name.strip().split(" ")
      name3=name2[0]+name2[1]
      val2=val.split(" ")
      val3=val2[0]+val2[1]

      if len (val2)>2:
          
          if name2[1]=='11':
            name2[1]='1'
         


          if name2[1] == val2[2]:


            regex2='<time datetime=.+?>(.+?)<.+?<li class="info">(.+?)</li>'
            match2=re.compile(regex2,re.DOTALL).findall(all_data)
            plot=''

            for times,plots in match2:
               plot=plot+times+': '+plots+'\n'
            return plot
   return plot
def deep_scrape(name,url,cat_data2,items_count,selected_list,lang):
    global sort_option,sort_by_episode
    progress_bar=Addon.getSetting("Progress")
    if progress_bar=="true":
        dp = xbmcgui.DialogProgress()
        dp.create(c_addon_name, "[COLOR orange][B]טוען קטגוריות[/B][/COLOR]")
        dp.update(0, 'אנא המתן',c_addon_name)
    #f = urllib2.urlopen(selected_list)
 
    #paste_list=f.read()
    if local_list_c==False:
       paste_list=requests.get(selected_list).content
    else:
       paste_list=local_list_data
    if progress_bar=="true":
      dp.update(0, 'סיים הורדה',c_addon_name)
    regex_cats="Start@@(.+?)@end@@(.+?)>"
    match_cats=re.compile(regex_cats,re.DOTALL).findall(cat_data2)
    paste_list=paste_list.replace('...','&')
    cat_data=paste_list[int(match_cats[0][0]):int(match_cats[0][1])].replace('...','&')
    
    sort_option=True
    if '#EXTINF' in cat_data:
        
        cat_data=read_old_paste(cat_data,int(url))
        sort_option=False

    if 'ערוץ 12' in cat_data or 'ערוץ 13' in cat_data or 'ערוץ 14' in cat_data  or 'ערוץ 11' in cat_data or 'ערוץ 1' in cat_data  or 'ערוץ 24' in cat_data or 'ערוץ 9' in cat_data:
       filedata2=requests.get('https://www.isramedia.net/tv').content.decode('windows-1255').encode('utf-8')
    if 'EPG' in cat_data:
      
       filedata = open(user_dataDir+'/guide.xml', 'r').read()
    regex_cat='<category_name-%s>(.+?)</category_name-%s>'%(url,url)

    match_cat=re.compile(regex_cat,re.DOTALL).findall(cat_data)
    
    z=0
    for all_data in match_cat:

            #regex_in='(.+?)="(.+?)"'
            #match_in=re.compile(regex_in).findall(all_data)
            match_in=all_data.split('"&')
            name='ללא שם'
            icon=' '
            image=' '
            plot=' '
            data=' '
            regex_data='data=@@(.+?)}@@'
            match_data=re.compile(regex_data).findall(all_data)
            try:
                for item in match_in:
                 if 'name="' in item:
                    name=item.split('name="')[1]
                 elif 'icon="' in item:
                    icon=item.split('icon="')[1]
                 elif 'link="' in item:
                    link=item.split('link="')[1]
                 elif 'fanart="' in item:
                    image=item.split('fanart="')[1]
                 elif len(match_data)>0:
                      data=match_data[0]+'}'
            except Exception as e:
              logging.warning(e)
              pass
            
     

            
            regex_next_data='<category_name-%s>name="%s"&(.+?)</category-%s>'%(url,name,url)
            
            match_next_data=re.compile(regex_next_data,re.DOTALL).findall(cat_data.replace('...','&'))
            #match_next_data=cat_data.replace('...','&').split('<category_name-%s>name="%s"&'%(url,name))
            
            
            #regex_counter='...'
            #match_counter=re.compile(regex_counter,re.DOTALL).findall(paste_list)
        
            index_of_data=paste_list.index(match_next_data[0])
      
    
            cat_new="Start@@"+str(index_of_data-len('<category_name-%s>name="%s"'%(url,name)))+"@end@@"+str(index_of_data+len(match_next_data[0])+len('</category-%s>'%url))+">"
            
            addDir3(name,str(int(url)+1),5,icon,image,plot,data=data,cat_level=cat_new,selected_list=selected_list,lang=lang)
            if progress_bar=="true":
               dp.update(int((z)/float(len(match_cat)) * 100), 'טוען', name)
            z=z+1
    if url=='2':
      item_num='m'
    else:
      item_num='m-'+url
    
    regex_items='<ite%s>(.+?)</ite%s>'%(item_num,item_num)
    match_in_up=re.compile(regex_items,re.DOTALL).findall(cat_data.replace('...','&'))
    regex_in='(.+?)="(.+?)"'
    if len (match_in_up)>0:
     match_in=re.compile(regex_in).findall(match_in_up[0])
            
     if 'pastebin' in match_in[1][1]:
              
                #f = urllib2.urlopen(match_in[1][1])
                #paste_list_old=f.read()
                paste_list=requests.get(match_in[1][1]).content

                match_data_old=read_sub_old_paste(paste_list)
                regex_items='<item>(.+?)</item>'
                match_in_up=re.compile(regex_items,re.DOTALL).findall(match_data_old)
                

    x=int(items_count)
    y=0
    if  sort_option==True:
      match_in_up=sorted(match_in_up)
    for all_data in match_in_up:
        

        if y>=int(items_count):
            
            if (x>(int(items_count)+max_per_page)):
                
                addDir3('[COLOR aqua][I]עמוד הבא[/I][/COLOR]',url,5,__PLUGIN_PATH__ + "\\resources\\next_icon.gif",__PLUGIN_PATH__ + "\\resources\\next.gif",'Next page',count=x,cat_level=cat_data2,data=" ",selected_list=selected_list,lang=lang)
                
                break
            x=x+1
            #regex_in='(.+?)="(.+?)"'
            #match_in=re.compile(regex_in).findall(all_data)
            #match_in=all_data.split('=')
            match_in=all_data.split('"&')
            
            regex_data='data=@@(.+?)}@@'
            match_data=re.compile(regex_data).findall(all_data)
 
            name='ללא שם - '
            link=' '
            icon=' '
            image=' '
            plot=' '
            data=' '

            try:
                for item in match_in:
                 if 'name="' in item:
                    name=item.split('name="')[1]
                 elif 'icon="' in item:
                    icon=item.split('icon="')[1]
                 elif 'link="' in item:
                    link=item.split('link="')[1]
                 elif 'fanart="' in item:
                    image=item.split('fanart="')[1]
                 elif len(match_data)>0:
                      data=match_data[0]+'}'
            except Exception as e:
              logging.warning(e)
              pass
          

            
            #link='ActivateWindow(10025,&quot;plugin://plugin.video.MakoTV/?iconimage=http%3a%2f%2fnow.tufts.edu%2fsites%2fdefault%2ffiles%2f111116_kids_TV_illo_L.JPG&amp;mode=0&amp;name=%d7%aa%d7%9b%d7%a0%d7%99%d7%95%d7%aa%20%d7%99%d7%9c%d7%93%d7%99%d7%9d&amp;url=http%3a%2f%2fwww.mako.co.il%2fmako-vod-kids&quot;,return)'
            temp_link=link
     
            
            
      
              
              #temp_link=link.split('/?')[0]+'/?'+urllib.quote_plus(link.split('/?')[1])
            epg_display='no'
            if 'ערוץ 12' in name or 'ערוץ 13' in name or 'ערוץ 14' in name  or 'ערוץ 11' in name or 'ערוץ 1' in name  or 'ערוץ 24' in name or 'ערוץ 9' in name :
              epg_display='yes'
              plot=get_epg_plot2(name,filedata2)
            elif 'EPG' in plot:
              epg_display='yes'
              plot=get_epg_plot(plot.split("$$$")[1],filedata)
            try:
              data_jason=json.loads(data)
            except:
              data_jason={}

            if 'Episode' in data_jason :

                if len(data_jason['Episode'])!=0 and (data_jason['Episode']!=' '):
                  sort_by_episode=True
            
            addLink(name,temp_link,3,False,icon,image,plot,data=data.replace("OriginalTitle","originaltitle"),lang=lang,epg=epg_display)
            if progress_bar=="true":
              dp.update(int((z)/float((max_per_page)) * 100), 'טוען', name)
            z=z+1
        y=y+1
    if progress_bar=="true":
      dp.close()
def play_myfile(url):
    #import requests

    r,cookie = read_site_html(url)
    regex="window.location='(.+?)'"

    
    match4=re.compile(regex).findall(r)
    
    path=match4[1]
    
   
    return (path)
def get_upfile_det(url):
    
    html,cookie=read_site_html(url)
    regex='<title>(.+?)</title>.+?<input type="hidden" value="(.+?)" name="hash">'
    match=re.compile(regex,re.DOTALL).findall(html)
    for name,link in match:
      id=url.split('/')[-1]
      id=id.replace('.html','').replace('.htm','')
      
      playlink='http://down.upfile.co.il/downloadnew/file/%s/%s'%(id,link)
    return name,playlink

      
def get_q(html):
    regex_q='"fmt_list","(.+?)"'
    match_q=re.compile(regex_q).findall(html)

    match_q2=match_q[0].split(',')
    return match_q2
def getPublicStream(url):
        import cookielib


        pquality=-1
        pformat=-1
        acodec=-1

        mediaURLs = []
  
       
        cookies = cookielib.LWPCookieJar()
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(cookies)
            ]
        opener = urllib2.build_opener(*handlers)
        req = urllib2.Request(url)

        req.add_header('User-agent',__USERAGENT__)
        result= opener.open(req)
        for cookie in cookies:
            if cookie.name=='DRIVE_STREAM':
              value=cookie.value

        #response = urllib2.urlopen(req)
        
        response_data = result.read()
        #response.close()





        for r in re.finditer('\"fmt_list\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            fmtlist = r.group(1)

        title = ''
        for r in re.finditer('\"title\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            title = r.group(1)



        itagDB={}
        containerDB = {'x-flv':'flv', 'webm': 'WebM', 'mp4;+codecs="avc1.42001E,+mp4a.40.2"': 'MP4'}
        for r in re.finditer('(\d+)/(\d+)x(\d+)/(\d+/\d+/\d+)\&?\,?' ,
                               fmtlist, re.DOTALL):
              (itag,resolution1,resolution2,codec) = r.groups()

              if codec == '9/0/115':
                itagDB[itag] = {'resolution': resolution2, 'codec': 'h.264/aac'}
              elif codec == '99/0/0':
                itagDB[itag] = {'resolution': resolution2, 'codec': 'VP8/vorbis'}
              else:
                itagDB[itag] = {'resolution': resolution2}

        for r in re.finditer('\"url_encoded_fmt_stream_map\"\,\"([^\"]+)\"' ,
                             response_data, re.DOTALL):
            urls = r.group(1)


        
        urls = urllib.unquote(urllib.unquote(urllib.unquote(urllib.unquote(urllib.unquote(urls)))))
        urls = re.sub('\\\\u003d', '=', urls)
        urls = re.sub('\\\\u0026', '&', urls)


#        urls = re.sub('\d+\&url\='+self.PROTOCOL, '\@', urls)
        urls = re.sub('\&url\='+ 'https://', '\@', urls)

#        for r in re.finditer('\@([^\@]+)' ,urls):
#          videoURL = r.group(0)
#        videoURL1 = self.PROTOCOL + videoURL


        # fetch format type and quality for each stream
        count=0
        for r in re.finditer('\@([^\@]+)' ,urls):
                videoURL = r.group(1)
                for q in re.finditer('itag\=(\d+).*?type\=video\/([^\&]+)\&quality\=(\w+)' ,
                             videoURL, re.DOTALL):
                    (itag,container,quality) = q.groups()
                    count = count + 1
                    order=0
                    if pquality > -1 or pformat > -1 or acodec > -1:
                        if int(itagDB[itag]['resolution']) == 1080:
                            if pquality == 0:
                                order = order + 1000
                            elif pquality == 1:
                                order = order + 3000
                            elif pquality == 3:
                                order = order + 9000
                        elif int(itagDB[itag]['resolution']) == 720:
                            if pquality == 0:
                                order = order + 2000
                            elif pquality == 1:
                                order = order + 1000
                            elif pquality == 3:
                                order = order + 9000
                        elif int(itagDB[itag]['resolution']) == 480:
                            if pquality == 0:
                                order = order + 3000
                            elif pquality == 1:
                                order = order + 2000
                            elif pquality == 3:
                                order = order + 1000
                        elif int(itagDB[itag]['resolution']) < 480:
                            if pquality == 0:
                                order = order + 4000
                            elif pquality == 1:
                                order = order + 3000
                            elif pquality == 3:
                                order = order + 2000
                    try:
                        if itagDB[itag]['codec'] == 'VP8/vorbis':
                            if acodec == 1:
                                order = order + 90000
                            else:
                                order = order + 10000
                    except :
                        order = order + 30000

                    try:
                        if containerDB[container] == 'MP4':
                            if pformat == 0 or pformat == 1:
                                order = order + 100
                            elif pformat == 3 or pformat == 4:
                                order = order + 200
                            else:
                                order = order + 300
                        elif containerDB[container] == 'flv':
                            if pformat == 2 or pformat == 3:
                                order = order + 100
                            elif pformat == 1 or pformat == 5:
                                order = order + 200
                            else:
                                order = order + 300
                        elif containerDB[container] == 'WebM':
                            if pformat == 4 or pformat == 5:
                                order = order + 100
                            elif pformat == 0 or pformat == 1:
                                order = order + 200
                            else:
                                order = order + 300
                        else:
                            order = order + 100
                    except :
                        pass

                    try:
                        mediaURLs.append( mediaurl.mediaurl('https://' + videoURL, itagDB[itag]['resolution'] + ' - ' + containerDB[container] + ' - ' + itagDB[itag]['codec'], str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
                    except KeyError:
                        mediaURLs.append(mediaurl.mediaurl('https://'+ videoURL, itagDB[itag]['resolution'] + ' - ' + container, str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
        
        return mediaURLs,value
        
def googledrive_resolve(id):


    #html,cookie=read_site_html('https://drive.google.com/file/d/'+id+'/view')
    #regex='"fmt_stream_map".+?http(.+?)"'
    #match=re.compile(regex).findall(html)
    #link=('http'+match[0]).decode('unicode_escape')
    links_data,cookie=getPublicStream('https://drive.google.com/file/d/'+id+'/view')

    mediaURLs = sorted(links_data)
    options = []
    for mediaURL in mediaURLs:
        options.append(mediaURL.qualityDesc)

    
    ret = xbmcgui.Dialog().select("בחר איכות", options)
    
    
    playbackURL = mediaURLs[ret].url


    final_link=playbackURL
    
    
    return (final_link+'||Cookie=DRIVE_STREAM%3D'+cookie) 
def get_epg_plot(num,filedata):
    import _strptime
    

    regex_pre='<programme start=(.+?)</programme>'
    match_pre=re.compile(regex_pre,re.DOTALL).findall(filedata)


    today=(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    last_week=((datetime.datetime.now()-datetime.timedelta(minutes=10080)).strftime("%Y%m%d%H%M%S"))

    today_date=(datetime.datetime.now().strftime("%Y%m%d"))
    last_week_date=((datetime.datetime.now()-datetime.timedelta(minutes=10080)).strftime("%Y%m%d"))
    prev=''
    plot=''
    disc=''
    for all in match_pre:

      regex='"(.+?)" stop="(.+?)" channel="%s">.+?<desc lang="he">(.+?)</desc>'%num
      match=re.compile(regex,re.DOTALL).findall(all)

      for start,end,disc in match:
       start_date=start.split(" ")[0]
       if today_date in start:
         check_date=today
       else:
         check_date=last_week
       if int(check_date)<=int(start_date):

          if prev!='':

            try:
                first=datetime.datetime.strptime(prev, "%Y%m%d%H%M%S")
            except TypeError:
                first=datetime.datetime(*(time.strptime(prev, "%Y%m%d%H%M%S")[0:6]))
    
 
            try:
                second=datetime.datetime.strftime(first,"%H:%M")
            except TypeError:
                second=datetime.datetime(*(time.strftime(first,"%H:%M")[0:6]))

            #second=first.strftime("%H:%M")
            plot=plot+second+': '+disc +'\n'
            prev=''
          else:
            try:
                first=datetime.datetime.strptime(start_date, "%Y%m%d%H%M%S")
            except TypeError:
                first=datetime.datetime(*(time.strptime(start_date, "%Y%m%d%H%M%S")[0:6]))
    
 
            try:
                second=datetime.datetime.strftime(first,"%H:%M")
            except TypeError:
                second=datetime.datetime(*(time.strftime(first,"%H:%M")[0:6]))
               
            plot=plot+ second+': '+disc+'\n'
         
       else:
         prev=start_date
    
    return plot
def get_strimm_link(ch):
    ch=ch.strip("")
    
    html=read_site_html2(ch)
    date_time_now=time.strftime("%m-%d-%Y-%H-%M")
    regex='channelTubeId = "(.+?)"'
    match=re.compile(regex).findall(html)
    html=read_site_html2(__REQ_URL__.replace("$$$$$",match[0]).replace('!!!!!!',str(date_time_now)))
    link=__REQ_URL__.replace("$$$$$",match[0]).replace('!!!!!!',str(date_time_now))
    html=read_site_html2(link)
    regex='<Playlist>(.+?)</Playlist>'
    match=re.compile(regex,re.DOTALL).findall(html)
    
    regex='<VideoTubeTitle>(.+?)</VideoTubeTitle>.+?<ProviderVideoId>(.+?)</ProviderVideoId>.+?<Thumbnail>(.+?)</Thumbnail>'
    match2=re.compile(regex,re.DOTALL).findall(match[0])
    playlist =xbmc.PlayList (xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    x=0
    for name,id,image in match2:
        
        
        
        if Addon.getSetting("youtube")=="0":
        
          link='plugin://plugin.video.youtube/play/?video_id='+id
        else:
         video_id='/watch?v=%s'%id
         video_id = 'videoid@@@@'+video_id.replace("=","@@@@@@").replace("&","*****").replace("?","!!!!!!")
         link='plugin://plugin.video.MyYoutube/?mode=3&name=%s&url=%s' % (name, video_id)
        
        
        listitem =xbmcgui.ListItem (name, thumbnailImage=image)
        listitem.setInfo('video', {'Title': name})
        playlist.add(url=link, listitem=listitem, index=x)
        x=x+1
    playlist.shuffle()
    #change_aspect()
    #xbmc.Player().play(playlist,windowed=False)

    #mode=99
    #sys.exit()
    return 'DONE'
def change_aspect():
    import glob, sqlite3
    files = glob.glob(xbmc.translatePath('special://Database') + '/MyVideos*.db')
    if len(files):
        conn = sqlite3.connect(files[0])
        c = conn.cursor()

      
        xbmc.Player().stop()

        

        # Change the information registered
        while True:
            c.execute("SELECT idFile FROM files WHERE strFilename LIKE ? ESCAPE '$'", (file,))
            row = c.fetchone()
            if row != None:
                print row[0]
                c.execute("UPDATE settings SET ViewMode = 6, PixelRatio = 0.5 WHERE idFile = ?", (row[0],))
                conn.commit()
                break
            xbmc.sleep(100)

        # play again
        
        c.close()
def get_auro_link(link):
   html,cookie=read_site_html(link)
   regex="<source src=\"(.+?)\" type="
   match=re.compile(regex).findall(html)
   ret = xbmcgui.Dialog().select("בחר מקור", match)
   return match[0].strip(" \n") +'|User-Agent=%s'%__USERAGENT__

def get_whole_link(link):
    
    html,cookie=read_site_html(link)
    regex='<input type="hidden" name="stepkey" value="(.+?)"><Br>'
    match=re.compile(regex).findall(html)
   
    
   
   
   
   
    



    headers = {
        'Host': 'www.wholecloud.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': link,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    data = [
      ('stepkey', match[0]),
      ('submit', 'submit'),
      ('ab', '1'),
    ]
    
    x=requests.post(link, headers=headers, data=data).text

   
    regex="<source src=\"(.+?)\" type="
    match=re.compile(regex).findall(x)
    ret = xbmcgui.Dialog().select("בחר מקור", match)
    return match[ret].strip(" \n") +'|User-Agent=%s'%__USERAGENT__
def get_vidlox(link):
   html,cookie=read_site_html(link)

   regex="sources:(.+?)]"
   match=re.compile(regex).findall(html)
   regex_links='"(.+?)"'
   match_links=re.compile(regex_links).findall(match[0])
   
   ret = xbmcgui.Dialog().select("בחר מקור", match_links)

   
           
   return match_links[ret].strip(" \n") +'|User-Agent=%s'%__USERAGENT__
def get_vidi(link):
   ok,link=__getMediaLinkForGuest_vidzi(link)
  
   return link
   html,cookie=read_site_html(link)
  
   regex="sources:(.+?)]"
   match=re.compile(regex).findall(html)
   regex_links='file: "(.+?)"'
   match_links=re.compile(regex_links).findall(match[0])
   
   ret = xbmcgui.Dialog().select("בחר מקור", match_links)

   
           
   return match_links[ret].strip(" \n") +'|User-Agent=%s'%__USERAGENT__
def dailymotion(link):
   html,cookie=read_site_html(link)

   regex="var __PLAYER_CONFIG__ = (.+?);\n"
   match=re.compile(regex).findall(html)

   json_data=json.loads(match[0])
   q_name=[]
   links=[]
   all_data=[]
   for items in json_data['metadata']['qualities']:
       
       
       for ques in json_data['metadata']['qualities'][items]:

         all_data.append((ques['type'],items,ques['url']))
   all_data.sort(key=lambda x: x[1], reverse=True)
   for items in all_data:
         q_name.append('[COLOR aqua]'+items[0]+'[/COLOR]'+" - "+items[1]+'p')
  
         links.append(items[2])
         
   dialog = xbmcgui.Dialog()
   ret = dialog.select("Choose quality to play", q_name)
   if ret != -1:
        link_new = links[ret]
   else:
     sys.exit()
   return link_new
def resolve_bitpor(url):
    import cloudflare
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        #'Host': 'www.bitporno.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
   
    x,token=cloudflare.request(url)
    regex='<source src="(.+?)" type="video/mp4" data-res="(.+?)"'
   
    match=re.compile(regex).findall(x)
    if len (match)==0:
       regex="<source src=\"(.+?)\" type='video/mp4'.+?res='(.+?)'"
           
       match=re.compile(regex).findall(x)
    
    
    all_names=[]
    all_links=[]
    for link,res in match:
       if len(res)>1:
         if 'x' in res:
           res=res.split('x')[1]
         all_names.append(res)
         all_links.append(link)
         
    ret = xbmcgui.Dialog().select("Choose quality to play", all_names)
    if ret != -1:
        return all_links[ret]
    else:
     sys.exit()
def resolver(link):

  #link='https://www.wholecloud.net/video/3c589d3f55442'
  link=link.strip()
  link=link.replace(' ','%20')
  if 'rtmp' not in link and 'estream' not in link:
    #cookie=read_cookie_html(link)
    #logging.warning(cookie)
    a=1
  if 'upfile' in link or 'www.upf.co.il' in link:
   name2,link=get_upfile_det(link)
  elif 'https://vidzi.tv/' in link  :
    link=get_vidi(link)
  elif 'vidlox.tv' in link:
    link=get_vidlox(link)
  elif 'https://www.wholecloud.net' in link:
    link=get_whole_link(link)
  elif 'www.strimm.com' in link:
    link=get_strimm_link(link)
  elif 'http://www.auroravid.to' in link:
    link=get_auro_link(link)
  elif 'myfile' in link:

     link=(play_myfile(link))
  elif 'dailymotion.com' in link:

     link=(dailymotion(link))
  elif 'rapidvideo' in link:
      from raptu import resolve
      dialog = xbmcgui.Dialog()
      video_data = resolve(link)
      videos = video_data['videos']
      qualities = sorted([_x.encode("UTF8") for _x in videos.keys()], key=lambda _q: int(filter(str.isdigit, _q)))
      ret = dialog.select("Choose quality to play", qualities)
      if ret != -1:
        link = videos[qualities[ret]]
  elif 'google' in link:
      #https://drive.google.com/file/d/0B7x6bLX-Xu4RTUMyV05lRTAxVlk/view?usp=sharing
      if '=' in link:
        id=link.split('=')[-1]

      else:
       regex='/d/(.+?)/view'
       match=re.compile(regex).findall(link)
       if len(match)>0:
         id=match[0]
       else:
         regex='/d/(.+?)/preview'
         match=re.compile(regex).findall(link)
         id=match[0]
      link=googledrive_resolve(id)
  elif 'www.you' in link:
   
    if 'list' in link:

      if Addon.getSetting("youtube")=="0":
          playlist =xbmc.PlayList (xbmc.PLAYLIST_VIDEO)
          playlist.clear()
          video_id = link.split('list=')[1]
          link =get_all_youtube_items(name,link,playlist)
          #link = 'plugin://plugin.video.youtube/play/?playlist_id=%s&mode=shuffle&order=shuffle' % video_id
      else:
          video_id = 'playlistId@@@@'+link.replace('https://www.youtube.com',"").replace("=","@@@@@@").replace("&","*****").replace("?","!!!!!!")
          link= 'plugin://plugin.video.MyYoutube/?mode=3&name=%s&url=%s' % (name, video_id)
     
    else:
       if Addon.getSetting("youtube")=="0":
          video_id = link.split('v=')[1]
          link = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
       else:
          video_id = 'videoid@@@@'+link.replace('https://www.youtube.com',"").replace("=","@@@@@@").replace("&","*****").replace("?","!!!!!!")
          link= 'plugin://plugin.video.MyYoutube/?mode=3&name=%s&url=%s' % (name, video_id)
  elif 'openload' in link:
       xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'Vimoo Source')).encode('utf-8'))
       streamurl=getMediaLinkForGuest(url)
     
       link=streamurl
       xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', '[COLOR lighgreen]Vimoo OK[/COLOR]')).encode('utf-8'))
       '''
       import requests
       Domain=Addon.getSetting("server")
       En_Domain=Addon.getSetting("serveroption")
       if 'openload' in url and  len(Domain)>0 and En_Domain=='true':
           if 'http' not in Domain:
                  Domain='http://'+Domain
           new_serv=Domain+":8080/GetVideoUrl?url="+(url)
           new_serv=new_serv.replace("openload.co",'oload.stream').replace("embed",'f')

           try:
             
               x=requests.get(new_serv, timeout=70).content
               regex='>(.+?)<'
               link=re.compile(regex).findall(x)[0]
               
         
                       
           except:
                import resolveurl
                try:

                    videoPlayListUrl = resolveurl.HostedMediaFile(url=link).resolve()
                    match=videoPlayListUrl.split("/")[-1]
                    link=videoPlayListUrl.replace(match,urllib.quote_plus(match))
                    
                except:
               
                 link=link
       '''
  elif 'bitporno' in link or 'estream' in link:
    
     link=resolve_bitpor(link)
  elif 'm3u8' not in url and 'rtmp' not in link :

    import resolveurl
    try:

        videoPlayListUrl = resolveurl.HostedMediaFile(url=link).resolve()
        match=videoPlayListUrl.split("/")[-1]
        link=videoPlayListUrl.replace(match,urllib.quote_plus(match))
        
    except:
   
     link=link


  return link.replace(' ','%20')
def update_view(url):

    ok=True        
    xbmc.executebuiltin('XBMC.Container.Update(%s)' % url )
    return ok

def get_links(name,url,data):
    import nanscrapers,resolveurl
    
    video_info=json.loads(data)

    def sort_function(item):
            quality = item[1][0]["quality"]
            if quality == "1080": quality = "HDa"
            if quality == "720": quality = "HDb"
            if quality == "560": quality = "HDc"
            if quality == "HD": quality = "HDd"
            if quality == "480": quality = "SDa"
            if quality == "360": quality = "SDb"
            if quality == "SD": quality = "SDc"

            return quality
    if 'tvshow'  in data:
      
  
      link = nanscrapers.scrape_episode_with_dialog(video_info['originaltitle'],video_info['year'],int(  video_info['year']), int( video_info['Season']), int( video_info['Episode']), video_info['imdbnumber'], None)
   
    else:
      link = nanscrapers.scrape_movie_with_dialog(video_info['originaltitle'], video_info['year'], video_info['imdbnumber'], timeout=600, sort_function=sort_function)
    if link is False:
        xbmcgui.Dialog().ok("Movie not found", "No Links Found for " + name + " (" + year + ")")
    else:
        if link:
            url = link['url']
            return url
def dis_or_enable_addon(addon_id, enable="true"):
    import json
    addon = '"%s"' % addon_id
    if xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "true":
        
        return xbmc.log("### Skipped %s, reason = allready enabled" % addon_id)
    elif not xbmc.getCondVisibility("System.HasAddon(%s)" % addon_id) and enable == "false":
        return xbmc.log("### Skipped %s, reason = not installed" % addon_id)
    else:
        do_json = '{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":%s,"enabled":%s}}' % (addon, enable)
        query = xbmc.executeJSONRPC(do_json)
        response = json.loads(query)
        if enable == "true":
            xbmc.log("### Enabled %s, response = %s" % (addon_id, response))
        else:
            xbmc.log("### Disabled %s, response = %s" % (addon_id, response))
    return xbmc.executebuiltin('Container.Update(%s)' % xbmc.getInfoLabel('Container.FolderPath'))
def downloader_is (url,name,with_massage ) :
 import downloader,extract   
 i1iIIII = xbmc . getInfoLabel ( "System.ProfileName" )
 I1 = xbmc . translatePath ( os . path . join ( 'special://home' , '' ) )
 O0OoOoo00o = xbmcgui . Dialog ( )
 if name.find('repo')< 0 and with_massage=='yes':
     choice = O0OoOoo00o . yesno ( "XBMC ISRAEL" , "Yes to install" ,name)
 else:
     choice=True
 if    choice :
  iiI1iIiI = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
  iiiI11 = xbmcgui . DialogProgress ( )
  iiiI11 . create ( "XBMC ISRAEL" , "Downloading " +name, '' , 'Please Wait' )
  OOooO = os . path . join ( iiI1iIiI , 'isr.zip' )
  try :
     os . remove ( OOooO )
  except :
      pass
  downloader . download ( url , OOooO ,name, iiiI11 )
  II111iiii = xbmc . translatePath ( os . path . join ( 'special://home' , 'addons' ) )
  iiiI11 . update ( 0 , name , "Extracting Zip Please Wait" )

  extract . all ( OOooO , II111iiii , iiiI11 )
  iiiI11 . update ( 0 , name , "Downloading" )
  iiiI11 . update ( 0 , name , "Extracting Zip Please Wait" )
  xbmc . executebuiltin ( 'UpdateLocalAddons ' )
  xbmc . executebuiltin ( "UpdateAddonRepos" )
  
def install_package(name,url):
    dialog = xbmcgui.Dialog()
    choice=dialog.yesno(c_addon_name, '','[B][COLOR red]Install %s[/COLOR][/B]'%name)
    if    choice :
      downloader_is(url,name,"No")
      addon_name=url.split('/')
  
      if '-' in addon_name:
        addon_name=addon_name[len(addon_name)-1].split("-")[0]
      else:
        addon_name=addon_name.replace('.zip','')

      dis_or_enable_addon(addon_name)
    
    


      
      
      
      

      dis_or_enable_addon(name.rstrip('\r\n'))
      time.sleep(10)
      xbmc.executebuiltin('SendClick(yesnodialog,11)')
      
   
      
def unshorten_url(url):
    import urlparse,httplib
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url
def getall_youtube(html,playlist,video_id):
     in_token=0
     x=0
     while(in_token==0):
          if 'items' not in html:
            return None
          for item in html['items']:
         
                 listitem =xbmcgui.ListItem (item['snippet']['title'], thumbnailImage=' ')
                 listitem.setInfo('video', {'Title': item['snippet']['title']})
                 url_2='plugin://plugin.video.youtube/play/?video_id=%s' % ( item['snippet']['resourceId']['videoId'])
                 
                 playlist.add(url=url_2, listitem=listitem, index=x)

                 x=x+1
          if 'nextPageToken' in html:
           
             url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=50&pageToken=%s&key=AIzaSyClvQA4Zjs3ZwWBkjVG4hlMrT98JnINDII'%(video_id,html['nextPageToken'])
             html=requests.get(url).json()

          else:
             in_token=1
     playlist.shuffle()
    
def get_all_youtube_items2(name,link,playlist):
     
     video_id = link.split('list=')[1]
 
     url='https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s&maxResults=50&key=AIzaSyClvQA4Zjs3ZwWBkjVG4hlMrT98JnINDII'%video_id

     html=requests.get(url).json()
    
     threading.Thread(target=getall_youtube, args=(html,playlist ,video_id)).start()
     if 'items' in html:
       return('plugin://plugin.video.youtube/play/?video_id=%s' % ( html['items'][0]['snippet']['resourceId']['videoId']))
     else:
       return 'playlist_all'
def getPlaylistUrlID(url):
    if 'list=' in url:
        eq_idx = url.index('=') + 1
        pl_id = url[eq_idx:]
        if '&' in url:
            amp = url.index('&')
            pl_id = url[eq_idx:amp]
    return pl_id 
    
def getFinalVideoUrl(vid_urls):
    final_urls = []
    for vid_url in vid_urls:
        url_amp = len(vid_url)
        if '&' in vid_url:
            url_amp = vid_url.index('&')
        final_urls.append('http://www.youtube.com/' + vid_url[:url_amp])
    return final_urls
    
def get_all_youtube_items(name,link,playlist):
        import random
        page_content=read_youtube_html(link)
      
        playlist_id = getPlaylistUrlID(url)
  
        vid_url_pat = re.compile(r'watch\?v=\S+?list=' + playlist_id)
        vid_url_matches = list(set(re.findall(vid_url_pat, page_content)))
        x=0
        all_data=[]
        if vid_url_matches:
             #final_vid_urls = getFinalVideoUrl(vid_url_matches)
             
             for vid_url in vid_url_matches:
                url_amp = len(vid_url)
                if '&' in vid_url:
                    url_amp = vid_url.index('&')
                final_urls=('http://www.youtube.com/' + vid_url[:url_amp])
                
                  
                regex='"videoId":"%s".+?"label":"(.+?)"'%vid_url[:url_amp].split('\\')[0].split('=')[1]
                match=re.compile(regex,re.DOTALL).findall(page_content)
      
                video_data={}
                video_data['title']=match[0]
                name=match[0]
                all_data.append((urllib.quote_plus(final_urls),name))
    
                listitem =xbmcgui.ListItem (match[0], thumbnailImage=' ')
                listitem.setInfo('video', video_data)
                url_2='plugin://%s/?mode=10&url=%s&name=%s' % (__plugin__,urllib.quote_plus(final_urls),urllib.quote_plus(match[0]))
                 
                playlist.add(url=url_2, listitem=listitem, index=x)
                x=x+1
      
        playlist.shuffle()
        value=random.choice(all_data)
        return('plugin://%s/?mode=10&url=%s&name=%s' % (__plugin__,value[0],value[1]))
def play_link(name,url,data,lang,plot):
    play_option=True
    #url='http://server2.sratim-il.com/%D7%90%D7%99%D7%A9_%D7%94%D7%97%D7%95%D7%9C.mp4'

    

    if 'goo.gl' in url:
     try:
      url=unshorten_url(url)
     except:
      pass
    links_list=0
    if '.zip' in url:
      install_package(name,url)
      sys.exit()

    try:

    
        video_info=json.loads(data)
        
        if 'tt' in video_info['imdbnumber'] and nanscarper==True and len(url)<5:
         
         options=[]
         options.append("ניגון ישיר")
         options.append("חפש מקורות ניגון")
         if len(url)<5:
           import resolveurl
           original_url=get_links(name,url,data)
           links_list=1
           
           url= resolveurl.HostedMediaFile(url=url).resolve()
           
           #url=resolver(url).strip().replace('\\r','').replace('\\n','')
           
           if url==False:
            url=original_url
           #url=resolver(url).strip().replace('\\r','').replace('\\n','')
         else:
             ret = xbmcgui.Dialog().select("בחר מקור", options)

             if ret==1:
                   url=get_links(name,url,data)
                   links_list=1
             if ret==-1:
                   return

    except:
      pass

    if '$$$' in url and ('playlist_all' not in url or 'playlist_all=True' in url):
       options=[]
       mediaURLs=url.split('$$$')
       x=1
       for mediaURL in mediaURLs:
        if '//' in mediaURL:
            regex_media='//(.+?)/'
            match_media=re.compile(regex_media).findall(mediaURL)
            if 'pluggin' in mediaURL:
              options.append(' מקור ')+str(x)
              x=x+1
            else:
              options.append(match_media[0])

    
       ret = xbmcgui.Dialog().select("בחר מקור", options)
       if ret == -1:
         play_option=False
       url = mediaURLs[ret]
    if 'server2.sratim-il.com' in url:
        regex='/(.+?).mp4'
        match=re.compile(regex).findall(url)
        
        headers={'Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                'Accept-Language':'en-US,en;q=0.5',
                'Cache-Control':'no-cache',
                'Connection':'keep-alive',
                'Host':'server2.sratim-il.com',
                'Pragma':'no-cache',

                'Referer':'http://www.sratim-il.cf/newsite/%s/'%match[0],
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/59.0'}
        head=urllib.urlencode(headers)
        url=url+"|"+head
    if not 'plugin://' in url or ('plugin://' in url and 'PlayMedia' in url):
      if play_option==True:
       if not 'plugin://' in url:
        if links_list==0:
          
          if '$$$' in url:
                
                mediaURLs=url.split('$$$')
                
                playlist =xbmc.PlayList (xbmc.PLAYLIST_VIDEO)
                playlist.clear()
                x=0
                
                for link in mediaURLs:
         
                  if 'www.you' in link and 'list' in link :
                    
                    url=get_all_youtube_items(name,link,playlist)
                    
                    #playlist.add(url=url, listitem=listitem, index=x)
                  if link!="playnext=1" and link!='playlist_all' and link!='playlist_all=True':

                      if 'www.you' not in link and 'list' not in link :
                        url=resolver(link).strip().replace('\\r','').replace('\\n','')
                      
                      listitem =xbmcgui.ListItem (name, thumbnailImage=' ')
                      try:
                        
                          video_data=json.loads(data)
                          if lang=='heb' and links_list==0:
                             video_data[u'mpaa']=unicode(lang)
                          if 'title' not in video_data and 'originaltitle' in video_data:
                             video_data['title']=video_data['originaltitle']
                          if video_data['plot']=='':
                            video_data['plot']=plot
                          
                          listitem.setInfo(type='Video', infoLabels=video_data)
                          listitem.setInfo( type="Music", infoLabels=video_data )
                      except:
                          listitem.setInfo(type='Video', infoLabels={"Title": name})
                          listitem.setInfo( type="Music", infoLabels={"Title": name} )
                      #listitem.setInfo('video', {'Title': name})

                      if 'www.you' not in link and 'list=' not in link :

                        playlist.add(url=url, listitem=listitem, index=x)
                      if x==0:
                        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listitem)
                      x=x+1


                #playlist.shuffle()
                #for items in playlist:
         
                url="DONE"
          else:
            url=resolver(url).strip().replace('\\r','').replace('\\n','')
        
        if url!="DONE":

            listItem = xbmcgui.ListItem(name, path=url) 
            try:
            
              video_data=json.loads(data)
              if lang=='heb' and links_list==0:
                 video_data[u'mpaa']=unicode(lang)
              if 'title' not in video_data and 'originaltitle' in video_data:
                 video_data['title']=video_data['originaltitle']
              if video_data['plot']=='':
                video_data['plot']=plot
       
              listItem.setInfo(type='Video', infoLabels=video_data)
              listItem.setInfo( type="Music", infoLabels=video_data )
            except:
              listItem.setInfo(type='Video', infoLabels={"Title": name})
              listItem.setInfo( type="Music", infoLabels={"Title": name} )
            listItem.setProperty('IsPlayable', 'true')
     
            xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)

       else:
        
        
        #regexss='&quot;(.+?)&quot;'
        #matchss_up=re.compile(regexss).findall(url)
        #regexss='url=(.+?)&'
        #matchss=re.compile(regexss).findall(url)
        #if len(matchss)>0:
        #    url=url.replace(matchss[0],urllib.quote_plus(matchss[0]))
            

        #xbmc.executebuiltin('PlayMedia(plugin://plugin.video.vipsecret/?url=plugin%3A%2F%2Fplugin.video.f4mTester%2F%3Furl%3Dhttp%253A%252F%252Fclientportal.link%253A8080%252Flive%252Fabc123%252F321cba%252F13464.ts%26amp%3Bstreamtype%3DTSDOWNLOADER%26name%3DBEN%2520NG&amp;mode=12)')
        #xbmc.executebuiltin( "PlayMedia(plugin://plugin.video.vipsecret/?url=plugin%3A%2F%2Fplugin.video.f4mTester%2F%3Furl%3Dhttp%253A%252F%252Fclientportal.link%253A8080%252Flive%252Fabc123%252F321cba%252F13464.ts%26amp%3Bstreamtype%3DTSDOWNLOADER%26name%3DBEN%2520NG&mode=12)" )
        xbmc.executebuiltin(url.replace('&amp;mode','&mode').replace('&quot;',""))
    
        
        '''
        regexss='name=(.+?)&'
        matchss=re.compile(regexss).findall(matchss_up[0])
        if len(matchss)>0:
            url=matchss_up[0].replace(matchss[0],urllib.quote_plus(matchss[0])).replace('amp;','')
        regexss='url=(.+?)&'
        matchss=re.compile(regexss).findall(matchss_up[0])
        if len(matchss)>0:
            url=matchss_up[0].replace(matchss[0],urllib.unquote(matchss[0]))
        
        '''

        
    else:
      regexss='&quot;(.+?)&quot;'
      matchss_up=re.compile(regexss).findall(url)
      if len(matchss_up)>0:
        update_view(matchss_up[0])
      else:
        update_view(url)
   
    

def run_addon(url):

  xbmc.executebuiltin(html_parser.unescape(url))
  xbmc.executebuiltin('xbmc.PlayerControl(RepeatOff)')
  mode=99
  sys.exit()
  return '0'
def search_all(lists):
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
    keyboard.doModal()
    if keyboard.isConfirmed():
                search_entered = keyboard.getText()
    if standalone==False:
        lists=[]
        
        for i in range(1 ,40):
         lists.append( Addon.getSetting("Pastebin"+str(i)))
    all_links=[]
    if search_entered !='' :
     for item in lists:
      if ("_encoded") in item:
        item=u_list(item.split('_encoded')[0])
      if len (item)>0:
       if 'http' not in item:
         item='https://pastebin.com/raw/'+item
       #f = urllib2.urlopen(item)
       #paste_list=f.read()
       paste_list=requests.get(item).content
       if '#EXTINF' in paste_list:
           paste_list=read_old_paste(paste_list,0)

       
      
       regex='<it.+?>(.+?)</it'
       match_in_up=re.compile(regex).findall(paste_list)
          
       
       for all_data in match_in_up:
           
            #regex_in='(.+?)="(.+?)"'
            #match_in=re.compile(regex_in).findall(all_data)
            match_in=all_data.split('"&')
            
            regex_data='data=@@(.+?)}@@'
            match_data=re.compile(regex_data).findall(all_data)
 
            name='ללא שם - '
            link=' '
            icon=' '
            image=' '
            plot=' '
            data=' '

            try:
                for item in match_in:
                 if 'name="' in item:
                    name=item.split('name="')[1]
                 elif 'icon="' in item:
                    icon=item.split('icon="')[1]
                 elif 'link="' in item:
                    link=item.split('link="')[1]
                 elif 'fanart="' in item:
                    image=item.split('fanart="')[1]
                 elif len(match_data)>0:
                      data=match_data[0]+'}'
            except Exception as e:
              logging.warning(e)
              pass
          
            if search_entered in name or search_entered in data:
                temp_link=link
                
                if temp_link.strip() not in all_links:
                  all_links.append(temp_link.strip())
              
                  
                  addLink(name,temp_link.strip(),3,False,icon,image,plot,data=data.replace("OriginalTitle","originaltitle"))
            
def display_shop(url):
          lists=[]
          for i in range(1 ,40):
             lists.append( Addon.getSetting("Pastebin"+str(i)))
          #f = urllib2.urlopen(url)
          #paste_list=f.read()
          paste_list=requests.get(url).content
          regex='<list_shop>name="(.+?)"&link="(.+?)"</list_shop>'
          match=re.compile(regex).findall(paste_list)
          
          for name1,shopes in match:
          
           
          
           #f = urllib2.urlopen(shopes)
           #paste_list=f.read()
           paste_list=requests.get(shopes).content
          
           regex_list='<list_name>(.+?)</list_name>'
           match_list=re.compile(regex_list).findall(paste_list)
           index=0
           for all_data in match_list:
            regex_in='(.+?)="(.+?)"'
            match_in=re.compile(regex_in).findall(all_data)
            
            name='רשימה - '+str(index)
            icon=' '
            image=' '
            plot=' '
            index=index+1
            try:
                if (match_in[0][0])=='name':
                  name=match_in[0][1]
                if (match_in[1][0])=='&icon':
                  icon=match_in[1][1]
                if (match_in[2][0])=='&fanart':
                  image=match_in[2][1]
                if (match_in[3][0])=='&plot':
                  plot=match_in[3][1]
            except:
              pass
            if shopes in lists:
              color='aqua'
            else:
              color='red'
            addLink('[COLOR %s]'%color+name+'[/COLOR]','PlayMedia('+shopes,8,False)
           if len(match_list)==0:
             name='רשימה - '+str(index)
             icon=' '
             image=' '
             plot=' '
             if shopes in lists:
               color='aqua'
             else:
               color='red'
             addLink('[COLOR %s]'%color+name1+'[/COLOR]','PlayMedia('+shopes,8,False)
           
             index=index+1
def install_list(url):
   all_lists=[]
   for i in range(1 ,41):
     all_lists.append(Addon.getSetting("Pastebin"+str(i)))
   if url.replace('PlayMedia(','') not in all_lists:
       lists=[]
       for i in range(1 ,41):
          setting=Addon.getSetting("Pastebin"+str(i))
          if len (setting)<3:
            Addon.setSetting("Pastebin"+str(i),url.replace('PlayMedia(',''))
            #xbmc.executebuiltin('Container.Refresh')
            xbmcgui.Dialog().ok('התווסף להרחבה',url.replace('PlayMedia(',''))
            break
   else:
       xbmcgui.Dialog().ok('[COLOR red][I]כבר קיים[/I][/COLOR]',url.replace('PlayMedia(','')+' [COLOR red][I]כבר קיים[/I][/COLOR]')
         
        
def play_youtube(url,name):
    from pytube import YouTube

    playback_url = YouTube(url).streams.first().download()
     
   
    
    #playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
    item = xbmcgui.ListItem(path=playback_url)
    item.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name)   })
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
count=0
cat_level=" "
index_depth=0
page=None
data=" "
selected_list=""
lang=" "
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        count=urllib.unquote_plus(params["count"])
except:
        pass
try:        
        page=urllib.unquote_plus(params["page"])
except:
        pass
try:        
        cat_level=urllib.unquote_plus(params["cat_level"])
except:
        pass
try:        
        index_depth=urllib.unquote_plus(params["index_depth"])
except:
        pass
try:        
        data=urllib.unquote_plus(params["data"])
except:
        pass
try:        
        selected_list=urllib.unquote_plus(params["selected_list"])
except:
        pass
try:        
        lang=urllib.unquote_plus(params["lang"])
except:
        pass

def check_jump_stage(name,url,lang):
   
    progress_bar=Addon.getSetting("Progress")

    if standalone==False:

        selected_list=Addon.getSetting("Pastebin"+str(url))
        selected_list=selected_list.strip()
        selected_list=selected_list.replace(' ','%20')
    else:
      selected_list=lists[0]
      if ("_encoded") in selected_list:
        selected_list=u_list(selected_list.split('_encoded')[0])

    if 'http' not in selected_list and local_list_c==False:
       selected_list='https://pastebin.com/raw/'+selected_list
    #f = urllib2.urlopen(selected_list)
    #paste_list=f.read()
    if local_list_c==False:
      paste_list=requests.get(selected_list).content
    else:
      paste_list=local_list_data
    if '#EXTINF' in paste_list:

          paste_list=read_old_paste(paste_list,0)

    regex='<category>(.+?)</category>'
    match=re.compile(regex,re.DOTALL).findall(paste_list)
    x=0
    cat_counter=0
    for cat in match:
    
        regex_for_names='<category_name>(.+?)</category_name>'
        match_all_names=re.compile(regex_for_names,re.DOTALL).findall(cat)

       
        index=0
        for all_data in match_all_names:
        
           
            #regex_in='(.+?)="(.+?)"'
            #match_in=re.compile(regex_in).findall(all_data)
            match_in=all_data.split('"&')
            name='ללא שם - '
            icon=' '
            image=' '
            plot=' '
            data=' '
            regex_data='data=@@(.+?)}@@'
            match_data=re.compile(regex_data).findall(all_data)
            try:
                for item in match_in:
                 if 'name="' in item:
                    name=item.split('name="')[1]
                 elif 'icon="' in item:
                    icon=item.split('icon="')[1]
                 elif 'link="' in item:
                    link=item.split('link="')[1]
                 elif 'fanart="' in item:
                    image=item.split('fanart="')[1]
                 elif len(match_data)>0:
                      data=match_data[0]+'}'
            except Exception as e:
              logging.warning(e)
              pass
            index_of_data=paste_list.index(cat)
            
            cat_new="Start@@"+str(index_of_data)+"@end@@"+str(index_of_data+len(cat)+15)+">"
            
            #addDir3(name,str(2),5,icon,image,plot,data=data.replace("OriginalTitle","Originaltitle"),cat_level=cat_new,selected_list=selected_list,lang=lang)
            index=index+1

            x=x+1
        cat_counter=cat_counter+1

    
    if cat_counter==1:
       
      addDir3('[COLOR aqua]חיפוש[/COLOR]','www',6,'','','',lang=lang)
      all_data=((name,str(2),5,icon,image,plot,data.replace("OriginalTitle","Originaltitle"),cat_new,selected_list,lang))
      return True,all_data
    else:
      return False,all_data

if standalone==True:
    if mode==None:
       check,a_data=check_jump_stage(name,url,lang)
       if check:
         
         name,url,mode,iconimage,fanart,description,data,cat_level,selected_list,lang=a_data
logging.warning(mode)

if mode==None or url==None or len(url)<1:
      if standalone==False:
        main_menu()
      else:
        scrape_all(name,url,"eng")
elif mode==2:
     scrape_all(name,url,lang)
elif mode==3:
     play_link(name,url,data,lang,description)
elif mode==4:
     ok=run_addon(url)
elif mode==5:
  deep_scrape(name,url,cat_level,count,selected_list,lang)
elif mode==6:
    search_all(lists)
elif mode==7:
    display_shop(url)
elif mode==8:
    install_list(url)
elif mode==9:
    disply_hwr()
elif mode==10:
    logging.warning('ININI')
    play_youtube(url,name)
xbmcplugin.setContent(int(sys.argv[1]), "movies")

if  sort_option==True and sort_by_episode==False:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATEADDED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
#xbmc.executebuiltin('Container.SetViewMode(500)')
elif sort_by_episode==True and sort_option==True:

    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
xbmcplugin.endOfDirectory(int(sys.argv[1]),succeeded =True,cacheToDisc =True)

