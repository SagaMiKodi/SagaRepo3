  # -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
Addon = xbmcaddon.Addon()
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
import HTMLParser
html_parser = HTMLParser.HTMLParser()
Domain='serethd.net'
class MyHTTPHandler (urllib2.HTTPHandler):

    def http_open (self, req):
        return self.do_open (MyHTTPConnection, req)

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

def addNolink( name, url,mode,isFolder, iconimage="DefaultFolder.png"):
 

          
         
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name)   })

          liz.setProperty("IsPlayable","false")
          liz.setProperty( "Fanart_Image", iconimage )
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################        

def addDir3(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok



def addLink( name, url,mode,isFolder, iconimage,fanart,description,title,data=''):

          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+(name)+"&data="+str(data)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+(description)+"&title="+(title)
 

          
         
         
          #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name) , "Plot": description  })

          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)

def Crypt(value):
  import hashlib
  
  m = hashlib.md5()
  m.update(value)
  md5_1 = m.hexdigest()
  return((md5_1))
def dictToQuery(d):
  query = ''
  for key in d.keys():
    query += str(key) + '=' + str(d[key]) + "&"
  return query
def read_site_html(url_link):
    global Domain
    import requests,cookielib
    #check redirect

    
    headers = {
        'Host': Domain,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    handlers = [MyHTTPHandler]
    cookjar = cookielib.CookieJar()
    handlers += [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookjar)]
    opener = urllib2.build_opener(*handlers)
    request = urllib2.Request(url_link,  headers=headers)
    try:
      html = opener.open(request).read()
    except:
      #xbmcgui.Dialog().ok("בא לי פרק","בעיה בחיבור לאתר\n החלף כתובת בהגדרות")
  
        r = requests.get(url_link)
        regex_domain='//(.+?)/'
        mathc_domain=re.compile(regex_domain).findall(r.url)

        new_domain=mathc_domain[0]
        if new_domain!=Domain:
          Addon.setSetting("domain",new_domain)
          Domain=Addon.getSetting("domain")
        xbmcgui.Dialog().ok("סרט HD"," כתובת האתר הוחלפה ועודכנה פתח שנית "+ '\n[COLOR aqua]'+Domain+'[/COLOR]')
        sys.exit()
    #html = urllib2.urlopen(request, timeout=int(30)).read()
    
    #html=requests.get(url_link,headers=headers)
    cookies={}
    for item in cookjar:
       cookies[item.name]=item.value

    #a=a+1
    try:
    
        first=Crypt('protect_own'+Domain)
        second=Crypt('protect_up'+Domain)
        third=Crypt('js'+Domain)

        oc1=str(cookies[first])
        oc2=str(cookies[second])
        
        co3=Crypt(oc1+oc2)+Crypt(oc2+oc1)
        


        cookies = {
        third: (co3),
        first:oc1,
        second:oc2,
        'expires': "14400",
        '__cfduid':cookies['__cfduid'],
        'path':'/'
        }
      

        
        html = requests.get(url_link, headers=headers, cookies=cookies).content
        request = urllib2.Request(url_link,  headers=headers)
        #html=requests.get(url_link,headers=headers,cookies=cookies)
        #html = opener.open(request, timeout=int(30)).read()
        
        return html#.encode('utf8')
    except:
      return html#.encode('utf8')

def main_menu():
    html=read_site_html('https://serethd.net/')
    addDir3('[COLOR aqua]סרטים אחרונים[/COLOR]','https://serethd.net/',2,' ',' ','latest movies')
    addDir3('[COLOR aqua]סדרות אחרונות[/COLOR]','https://serethd.net/',2,' ',' ','latest episodes')
    addDir3('[COLOR aqua]רשימת סדרות[/COLOR]','https://serethd.net/genre/%d7%a1%d7%93%d7%a8%d7%95%d7%aa',2,' ',' ','רשימת סדרות')
    addDir3('[COLOR aqua]חיפוש[/COLOR]','https://serethd.net/search/p=/s=%s',5,' ',' ','search')
    
    regex='class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-.+?"><a href="(.+?)">(.+?)</a>'
    match=re.compile(regex).findall(html)

    for link,name in match:
      if '<b>' not in name:
        addDir3(name,link,2,' ',' ',name)

def scrpae_site(name,url,plot_o):
   html=read_site_html(url)
   if plot_o=='latest movies' or plot_o=='latest episodes':
       regex_pre='<!--%s-->(.+?)<!--/%s-->'%(plot_o,plot_o)
       match_pre=re.compile(regex_pre,re.DOTALL).findall(html)
   else:
     match_pre=[html]
   regex='div data-movie-id=.+?<a href="(.+?)"(.+?)<img data-original="(.+?)".+?"mli-info"><h2>(.+?)</h2>.+?<div class="jt-info">(.+?)<.+?<div class="jt-info">(.+?)<.+?<p>(.+?)</p>'
   match=re.compile(regex,re.DOTALL).findall(match_pre[0])
   for link,quality,image,name,year,times_l,plot in match:
     if times_l=='N/A':
       times_l=''
     else:
       times_l='\n[COLOR lightblue]'+times_l+'[/COLOR]\n'
     if year=='N/A':
       year=''
     else:
       regex_y='<a href=".+?" rel="tag">(.+?)$'
    
       year=re.compile(regex_y).findall(year)[0]
     if 'mli-quality' in quality:
       regex_q='"mli-quality">(.+?)<'
       quality='[COLOR aqua]'+re.compile(regex_q).findall(quality)[0]+'[/COLOR]'
     else:
       quality=''
     addDir3(html_parser.unescape(name.decode('utf-8')).encode('utf-8'),link,3,image.strip(),image.strip(),quality+' ' +year+' '+times_l+html_parser.unescape(plot.decode('utf-8')).encode('utf-8'))
     regex_page='<link rel="next" href="(.+?)" />'
     match_page=re.compile(regex_page).findall(html)
   for next in match_page:
       addDir3('[COLOR aqua][I]עמוד הבא[/I][/COLOR]',next,2,' ',' ',plot_o)
def get_links(name,url,image,plot):


   html=read_site_html(url)
   regex='<strong>(.+?)</strong>.+?<div class="les-content"><a href="#(.+?)">(.+?)</a></div>'
   match=re.compile(regex,re.DOTALL).findall(html)
   if len(match)==0:
    regex='<p>(.+?)</p>(.+?)<hr />'
    match=re.compile(regex,re.DOTALL).findall(html)
    if len(match)==0:
        regex='<p><(.+?)>(.+?)</a>'
        match=re.compile(regex,re.DOTALL).findall(html)
        for links,name_l in match:
          regex_link='a href="(.+?)"'
          match_link=re.compile(regex_link,re.DOTALL).findall(links)
          for link in match_link:
              data={}
              data['title']=name
              data['plot']=plot

              addLink( name_l, link,4,False, image,image,plot,name,data=data)
    else:
    
        for name_l,links in match:
          regex_link='a href="(.+?)".+?>(.+?)</a>'
          match_link=re.compile(regex_link,re.DOTALL).findall(links)
          for link,name_pre in match_link:
              data={}
              data['title']=name
              data['plot']=plot

              addLink( name_l+' ' +name_pre, link,4,False, image,image,plot,name,data=data)
      
   else:
    for name_l,link,link_name in match:
     regex_link='<div id="%s".+?<iframe src="(.+?)"'%link
     match_link=re.compile(regex_link,re.DOTALL).findall(html)
     data={}
     data['title']=name
     data['plot']=plot
     addLink( name_l+' ' +link_name, match_link[0],4,False, image,image,plot,name,data=data)

def resolve(name,title,url,plot,data):
    import urlresolver,json
 
    videoPlayListUrl = urlresolver.HostedMediaFile(url=url).resolve()

def search():
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered = keyboard.getText()
                html=read_site_html('https://serethd.net/?s='+urllib.quote_plus(search_entered.replace(" ","+")))
              
                regex_pre='class="ml-item"(.+?)</p'
                match_pre=re.compile(regex_pre,re.DOTALL).findall(html)
                for item in match_pre:
                    regex='<a href="(.+?)".+?img data-original="(.+?)".+?<h2>(.+?)</h2>'
                    match=re.compile(regex,re.DOTALL).findall(item)
                    regex='-quality">(.+?)<'
                    quality_p=re.compile(regex).findall(item)
                    if len(quality_p)>0:
                      quality=quality_p[0]
                    else:
                      quality=' '
                    regex='"jt-info"><a href=".+?" rel="tag">(.+?)</a>'
                    year_p=re.compile(regex).findall(item)
                    if len(year_p)>0:
                      year=year_p[0]
                    else:
                      year=' '
                    regex='^<div class="jt-info">(.+?)<'
                    times_l_p=re.compile(regex).findall(item)
                    if len(times_l_p)>0:
                      times_l=times_l_p[0]
                    else:
                      times_l=' '
                    regex='<p>(.+?)$'
                    plot_p=re.compile(regex).findall(item)
                    if len(plot_p)>0:
                      plot=plot_p[0]
                    else:
                      plot=' '
               
                    for link,image,name in match:
   
                       addDir3(html_parser.unescape(name.decode('utf-8')).encode('utf-8'),link,3,image.strip(),image.strip(),quality+' ' +year+' '+times_l+html_parser.unescape(plot.decode('utf-8')).encode('utf-8'))
                
               
        else:
          sys.exit()
params=get_params()
        

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
data=None
title=None
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
    data=urllib.unquote_plus(params["data"])
except:
        pass
try:
    title=urllib.unquote_plus(params["title"])
except:
        pass



if mode==None or url==None or len(url)<1:
        main_menu()
elif mode==2:
        scrpae_site(name,url,description)
elif mode==3:
        get_links(name,url,iconimage,description)
elif mode==4:
        resolve(name,title,url,description,data)
elif mode==5:
        search()

xbmcplugin.setContent(int(sys.argv[1]), 'movies')


xbmcplugin.endOfDirectory(int(sys.argv[1]))

