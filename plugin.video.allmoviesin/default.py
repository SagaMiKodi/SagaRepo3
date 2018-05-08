# -*- coding: utf-8 -*-
import xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging,time
import requests,json,mediaurl,ssl,gzip,linecache
ADDON=xbmcaddon.Addon(id='plugin.video.allmoviesin')
import cache,zlib,HTMLParser,xbmcvfs
from open import getMediaLinkForGuest
from thevideo import getMediaLinkForGuest_thevid,getMediaLinkForGuest_vshare,getMediaLinkForGuest_vidlox,getMediaLinkForGuest_vidup
import PTN,StringIO
import resolveurl
import textwrap
__settings__ = ADDON
try:
    import StorageServer
except ImportError:
    import storageserverdummy as StorageServer
import socket
try:
    import StorageServer
except ImportError:
    import storageserverdummy as StorageServer
BASE_URL = "http://www.cinemast.org/he/cinemast/api/"
socket.setdefaulttimeout(10.0)
__PLUGIN_PATH__ = __settings__.getAddonInfo('path')
servers_db=__PLUGIN_PATH__ + "\\resources\\servers.db"
store = StorageServer.StorageServer('plugin.video.allmoviesin', int(24))  # 24hr
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
Addon = xbmcaddon.Addon()
addonPath = xbmc.translatePath(Addon.getAddonInfo("path")).decode("utf-8")
Domain_sparo=Addon.getSetting("domain_sp")
libDir = os.path.join(addonPath, 'resources', 'lib')
sys.path.insert(0, libDir)
libDir = os.path.join(addonPath, 'resources', 'lib2')
sys.path.insert(0, libDir)
libDir = os.path.join(addonPath, 'resources', 'plugins')
sys.path.insert(0, libDir)
__scriptname__ = Addon.getAddonInfo('name')
store = StorageServer.StorageServer(__scriptname__, int(24 * 364 / 2))  # 6 months
time_to_save=int(Addon.getSetting("save_time"))
import js2py,urlparse
import  cloudflare,threading
global links_scn,links_bmovie,links_kizi,links_shu,links_gona,links_moviesak,links_reqzone,links_ftp,links_tvl,link_onitube,link_filepursuit,link_2ddl,links_jksp,links_uni,links_linkia,links_sdarot,link_ct,imdb_global,all_magnet,links_m4u,rd_tvr,link_dlt,links_pf,all_subs,link_afdah,link_seehd,sources_a,link_cin,links_list2,links_list,links_sno,links_fun,links_mx,link_upto,link_direct,stop_all,links_we,links_dwatch,links_cmovies,links_flix,link_showbox,link_daily,link_source1,match_a,match,link_hdonline,link_dl20,cooltvzion,link_ava,link_tmp,links_1movie,next_p_all,link_goo,links_sc,links_seil,links_put
global pr_lv,pr_sv,pr_tv,pr_dl,pr_ho
global pr_sb,pr_dai,pr_au,pr_sp
global search_done,silent_mode,close_all
from vidtodo import VidToDoResolver
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
level_images=['http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Cherry.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Strawberry.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Orange.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Apple.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Pear.ico','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Banana.ico','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTaOe61sWWiQLqgknayKHvVfPtb59o_acSgPLMLhnxZEqHwuymWYQ','http://files.softicons.com/download/food-drinks-icons/paradise-fruit-icon-set-by-artbees/ico/Mango.ico','https://cdn.iconscout.com/public/images/icon/premium/png-512/pretzel-breakfast-appetizer-pastry-37ebe79fde250ac4-512x512.png','https://i.ytimg.com/vi/vPa45_0ozqE/maxresdefault.jpg']
level_fanart=['https://i0.wp.com/cidadegamer.com.br/wp-content/uploads/2012/02/Pac-man-the-adventure-begins-estreia-no-disney-XD-em-2013.jpg?fit=298%2C298','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-sj9LxuMDN64yD2GqxiUXpbJwstVmq4rZbOJJlNtX9q5twNqR','https://vignette.wikia.nocookie.net/fantendo/images/2/25/Mario_Artwork_-_Super_Mario_3D_World.png/revision/20131025223057','https://cdn.thisiswhyimbroke.com/images/iron-man-lamp.jpg','https://www.avforums.com/image.php?imageparameters=editorial/products/a197b-thor-2-the-dark-world-photos-2.jpg|909','https://i.pinimg.com/originals/99/27/aa/9927aab09a32ff610086758078fe792e.jpg','https://news.marvel.com/wp-content/uploads/2016/09/57852a5335bb6.jpg','http://cdn-static.denofgeek.com/sites/denofgeek/files/styles/main_wide/public/0/04//batman-v-superman-dawn-of-justice.jpg?itok=SwDBZWJJ','https://www.sideshowtoy.com/wp-content/uploads/2014/01/902174-product-feature1.jpg','https://vignette.wikia.nocookie.net/emporea/images/d/d9/Black_dragon_preloader.jpg/revision/latest?cb=20160216171424']
level_movies=['https://www.youtube.com/watch?v=nRCTMwgBGxM','https://www.youtube.com/watch?v=M0Es2B7aUHo','https://www.youtube.com/watch?v=mSolF3QBVBY','https://www.youtube.com/watch?v=QgRyng9w38g','https://www.youtube.com/watch?v=NlfoaCVHP0s','https://www.youtube.com/watch?v=KMR-6-YizZQ','https://www.youtube.com/watch?v=pBbsvavno8I','https://www.youtube.com/watch?v=lUIDCuYszqI','https://www.youtube.com/watch?v=opji5DgE_nQ']
addonInfo = xbmcaddon.Addon().getAddonInfo
dataPath = xbmc.translatePath(addonInfo('profile')).decode('utf-8')
cacheFile = os.path.join(dataPath, 'cache_play.db')
xbmcvfs.mkdir(dataPath)
dbcon = database.connect(cacheFile)
dbcur = dbcon.cursor()

dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'AllData')
dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""url TEXT, ""icon TEXT, ""image TEXT, ""plot TEXT, ""year TEXT, ""original_title TEXT, ""season TEXT, ""episode TEXT, ""id TEXT, ""eng_name TEXT, ""show_original_year TEXT, ""heb_name TEXT , ""isr TEXT, ""type TEXT);" % 'Lastepisode')
dbcur.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""speed TEXT);" % 'servers')
try:
    dbcur.execute("VACUUM 'AllData';")
    dbcur.execute("PRAGMA auto_vacuum;")
    dbcur.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
    dbcur.execute("PRAGMA temp_store=MEMORY ;")
except:
 pass
dbcon.commit()






pr_sb=0
pr_dai=0
stop_all=0
pr_au=0
pr_lv=0
pr_sv=0
pr_tv=0
pr_dl=0
pr_ho=0
pr_sp=0

silent_mode=False
links_scn=[]
links_bmovie=[]
links_kizi=[]
links_shu=[]
links_gona=[]
links_moviesak=[]
links_reqzone=[]
links_ftp=[]
links_tvl=[]
link_onitube=[]
link_filepursuit=[]
link_2ddl=[]
links_jksp=[]
links_uni=[]
links_linkia=[]
links_sdarot=[]
link_ct=[]
imdb_global=''
all_magnet=[]
links_m4u=[]
rd_tvr=[]
link_dlt=[]
links_pf=[]
all_subs=[]
link_afdah=[]
link_seehd=[]
sources_a=[]
link_cin=[]
links_list2=[]
links_list=[]
links_sno=[]
links_fun=[]
links_mx=[]
link_upto=[]
link_direct=[]
links_we=[]
links_dwatch=[]
links_cmovies=[]
links_flix=[]
links_seil=[]
links_sc=[]
links_put=[]
next_p_all=[]
links_1movie=[]
link_goo=[]
link_showbox=[]
link_daily=[]
link_source1=[]
link_tmp=[]
match_a=[]
link_ava=[]
link_dl20=[]
match=[]
cooltvzion=[]
API =('aHR0cHM6Ly9hcGkuc2Rhcm90Lndvcmxk'.decode('base64'))
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 Sdarot/2.5.3'
}

all_servers=['scn','1movie','bmovie','kizi','shuid','getgona','moviesak','reqzone','ftp','tvl','Onitube','filep','Magnet','M4u','Rd_tvr','Dlt','Pf','Afdah','Seehd','Cin','Upto','Direct','We','Dwatch','Cmovies','Flix','Put','Seil','Sc','Goo','Tmp','Ava','Cooltvzion','Dl20','Hdonline','Showbox','Sp','List','List2','Sno','fun','mx','daily','Ct','Sdarot','Linkia','Uni','2ddl']
link_hdonline=[]

KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])



reload(sys)  
sys.setdefaultencoding('utf8')
#PYTHONIOENCODING="UTF-8" 



rd_sources=Addon.getSetting("rdsource")
allow_debrid = rd_sources == "true" 

if KODI_VERSION>=17:
  ssl._create_default_https_context = ssl._create_unverified_context
  domain_s='https://'
elif KODI_VERSION<17:
  domain_s='http://'


#search


def get_upfile_det(url):
    name=''
  
    html,cook=cloudflare.request(url)
    regex='<title>(.+?)</title>.+?<input type="hidden" value="(.+?)" name="hash">'
    match=re.compile(regex,re.DOTALL).findall(html)

    for name,link in match:
      id=url.split('/')[-1]
      id=id.replace('.html','').replace('.htm','')
      
      playlink='http://down.upfile.co.il/downloadnew/file/%s/%s'%(id,link)
    return name,playlink
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
   
    return ( 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

def clean_name(name,option):

    if option==1:
      return name.replace('%20',' ').replace('%3a',':').replace('%27',"'")
    else:
      return name.replace('%20',' ').replace('%3a',':').replace('%27'," ")

def server_data(f_link,original_title,direct='NO',c_head={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}):
       try:
        
        
         
        if 'nowvideo.sx' in f_link:
          return original_title,' ',' ',False
        resolvable=resolveurl.HostedMediaFile(f_link).valid_url()
        
        if 'http' not in f_link:
           return original_title,' ',' ',False
        if 'estream' in f_link or resolvable==False:
          return original_title,' ',' ',True
        direct='yes'
        
        if direct=='yes':
        
          
         
          html2=requests.get(f_link,headers=c_head,timeout=10).content
        else:
          html2,cook=cloudflare.request(f_link,timeout=5)

        regex='"og:title" content="(.+?)"'
        match4=re.compile(regex).findall(html2)
        
        if len( match4)==0:
            regex='<Title>(.+?)</Title>'
            match4=re.compile(regex,re.DOTALL).findall(html2)
        if len(match4)==0:
             regex='name="fname" value="(.+?)"'
             match4=re.compile(regex,re.DOTALL).findall(html2)
        if len(match4)==0:
             regex='<title>(.+?)</title>'
             match4=re.compile(regex,re.DOTALL).findall(html2)
        if len(match4)==0:
             regex="title: '(.+?)',"
             match4=re.compile(regex,re.DOTALL).findall(html2)
        if len(match4)==0:
             regex='><span title="(.+?)"'
             match4=re.compile(regex,re.DOTALL).findall(html2)
        if len(match4)==0:
             regex=name='description" content="(.+?)"'
             match4=re.compile(regex,re.DOTALL).findall(html2)
       
        if len(match4)>0:
              name1=match4[0]
              try:
                  info=(PTN.parse(match4[0]))
                  
                  if 'resolution' in info:
                     res=info['resolution']
                  else:
                     if "HD" in match4[0]:
                      res="HD"
                     elif "720" in match4[0]:
                      res="720"
                     elif "1080" in match4[0]:
                       res="1080"
                     else:
                       res=' '
              except:
                res=' '
                pass
        else: 
            name1=original_title.replace('%20',' ')
            res=' '
   
        regex_s="//(.+?)/"
        match_s=re.compile(regex_s).findall(f_link)
        check=check_link(html2,full_data=True)
        return name1,match_s[0],res,check
       except Exception as e:
          logging.warning(e)
          logging.warning(f_link)
          return original_title,' ',' ',False
def ClearCache():
    from storage import Storage
    cache.clear(['cookies', 'pages'])
    Storage.open("parsers").clear()
    storage_path = os.path.join(xbmc.translatePath("special://temp"), ".storage")
    if os.path.isdir(storage_path):
        for f in os.listdir(storage_path):
            if re.search('.cache', f):
                os.remove(os.path.join(storage_path, f))

    cookies_path = xbmc.translatePath("special://temp")
    if os.path.isdir(cookies_path):
        for f in os.listdir(cookies_path):
            if re.search('.jar', f):
                os.remove(os.path.join(cookies_path, f))
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'נוקה'.decode('utf8'))).encode('utf-8'))
def base_convert(x,b,alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
    'convert an integer to its string representation in a given base'
    if b<2 or b>len(alphabet):
        if b==64: # assume base64 rather than raise error
            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        else:
            raise AssertionError("int2base base out of range")
    if isinstance(x,complex): # return a tuple
        return ( int2base(x.real,b,alphabet) , int2base(x.imag,b,alphabet) )
    if x<=0:
        if x==0:
            return alphabet[0]
        else:
            return  '-' + int2base(-x,b,alphabet)
    # else x is non-negative real
    rets=''
    while x>0:
        x,idx = divmod(x,b)
        rets = alphabet[idx] + rets
    return rets

    




from source1 import get_sources_source1

user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
save_file=os.path.join(user_dataDir,"fav.txt")
headers = {
    'Host': 'www.alluc.ee',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
cookies = {
'cf_clearance': '539f58668bbe6136468ce261e69ab811003732de-1518381700-7200',

}
class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)
        
tv_images={u'\u05d0\u05e7\u05e9\u05df \u05d5\u05d4\u05e8\u05e4\u05ea\u05e7\u05d0\u05d5\u05ea': 'http://stavarts.com/wp-content/uploads/2017/10/%D7%A9%D7%99%D7%A9%D7%99-%D7%94%D7%A8%D7%A4%D7%AA%D7%A7%D7%90%D7%95%D7%AA-%D7%AA%D7%A9%D7%A2%D7%B4%D7%97-%D7%A8%D7%90%D7%92%D7%A0%D7%90%D7%A8%D7%95%D7%A7_Page_1.jpg', u'\u05de\u05e1\u05ea\u05d5\u05e8\u05d9\u05df': 'http://avi-goldberg.com/wp-content/uploads/5008202002.jpg', u'\u05d9\u05dc\u05d3\u05d9\u05dd': domain_s+'i.ytimg.com/vi/sN4xfdDwjHk/maxresdefault.jpg', u'\u05de\u05e2\u05e8\u05d1\u05d5\u05df': domain_s+'i.ytimg.com/vi/Jw1iuGaNuy0/hqdefault.jpg', u'\u05e4\u05e9\u05e2': 'http://www.mapah.co.il/wp-content/uploads/2012/09/DSC_1210.jpg', u'\u05e8\u05d9\u05d0\u05dc\u05d9\u05d8\u05d9': 'http://blog.tapuz.co.il/oferD/images/%7B2D0A8A8A-7F57-4C8F-9290-D5DB72F06509%7D.jpg', u'\u05de\u05e9\u05e4\u05d7\u05d4': 'http://kaye7.school.org.il/photos/family.jpg', u'\u05e1\u05d1\u05d5\u05df': 'http://www.myliberty.co.il/media/com_hikashop/upload/2-1.jpg', u'\u05d7\u05d3\u05e9\u05d5\u05ea': domain_s+'shaza10.files.wordpress.com/2010/11/d790d795d79cd7a4d79f-d797d793d7a9-d797d793d7a9d795d7aa-10-d7a6d799d79cd795d79d-d7aad795d79ed7a8-d7a4d795d79cd798d799d79f03.jpg', u'\u05e7\u05d5\u05de\u05d3\u05d9\u05d4': domain_s+'upload.wikimedia.org/wikipedia/he/e/ef/Le_Tout_Nouveau_Testament.jpg', u'\u05d0\u05e0\u05d9\u05de\u05e6\u05d9\u05d4': 'http://www.printime.co.il/image/users/16584/ftp/my_files/smileynumbers1we.jpg', u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9 \u05d5\u05e4\u05e0\u05d8\u05d6\u05d9\u05d4': domain_s+'media.getbooks.co.il/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/s/h/shemharuach_getbooks-copy.jpg', u'\u05d3\u05e8\u05de\u05d4': 'http://www.yorav.co.il/images/moshe+erela/2007/dram.JPG', u'\u05d3\u05d5\u05e7\u05d5\u05de\u05e0\u05d8\u05e8\u05d9': 'http://img.mako.co.il/2017/03/28/704104_I.jpg', u'\u05de\u05dc\u05d7\u05de\u05d4 \u05d5\u05e4\u05d5\u05dc\u05d9\u05d8\u05d9\u05e7\u05d4': domain_s+'dannyorbach.files.wordpress.com/2013/05/berlinsynagoge.jpg', u'\u05d3\u05d9\u05d1\u05d5\u05e8\u05d9\u05dd': 'http://www.news1.co.il/uploadimages/NEWS1-556713283061982.jpg'}
movie_images={u'\u05de\u05d5\u05e1\u05d9\u05e7\u05d4': 'http://www.blich.ramat-gan.k12.il/sites/default/files/files/music.jpg', u'\u05e1\u05e8\u05d8 \u05d8\u05dc\u05d5\u05d9\u05d6\u05d9\u05d4': domain_s+'i.ytimg.com/vi/hFc1821MSoA/hqdefault.jpg', u'\u05d4\u05e8\u05e4\u05ea\u05e7\u05d0\u05d5\u05ea': domain_s+'upload.wikimedia.org/wikipedia/he/3/38/%D7%94%D7%A8%D7%A4%D7%AA%D7%A7%D7%90%D7%95%D7%AA_%D7%91%D7%A8%D7%A0%D7%A8%D7%93_%D7%95%D7%91%D7%99%D7%90%D7%A0%D7%A7%D7%94_%D7%9B%D7%A8%D7%96%D7%94_%D7%A2%D7%91%D7%A8%D7%99%D7%AA.png', u'\u05de\u05e1\u05ea\u05d5\u05e8\u05d9\u05df': 'http://avi-goldberg.com/wp-content/uploads/5008202002.jpg', u'\u05de\u05e2\u05e8\u05d1\u05d5\u05df': domain_s+'i.ytimg.com/vi/Jw1iuGaNuy0/hqdefault.jpg', u'\u05de\u05dc\u05d7\u05de\u05d4': 'http://images.nana10.co.il/upload/mediastock/img/16/0/208/208383.jpg', u'\u05e4\u05e9\u05e2': 'http://www.mapah.co.il/wp-content/uploads/2012/09/DSC_1210.jpg', u'\u05e4\u05e0\u05d8\u05d6\u05d9\u05d4': 'http://blog.tapuz.co.il/beinhashurot/images/1943392_142.jpg', u'\u05de\u05e9\u05e4\u05d7\u05d4': 'http://kaye7.school.org.il/photos/family.jpg', u'\u05e7\u05d5\u05de\u05d3\u05d9\u05d4': domain_s+'upload.wikimedia.org/wikipedia/he/e/ef/Le_Tout_Nouveau_Testament.jpg', u'\u05d0\u05e0\u05d9\u05de\u05e6\u05d9\u05d4': 'http://www.printime.co.il/image/users/16584/ftp/my_files/smileynumbers1we.jpg', u'\u05d3\u05e8\u05de\u05d4': 'http://www.yorav.co.il/images/moshe+erela/2007/dram.JPG', u'\u05d4\u05e1\u05d8\u05d5\u05e8\u05d9\u05d4': domain_s+'medicine.ekmd.huji.ac.il/schools/occupationaltherapy/He/about/PublishingImages/%d7%aa%d7%9e%d7%95%d7%a0%d7%94%207.jpg', u'\u05e8\u05d5\u05de\u05e0\u05d8\u05d9': domain_s+'i.ytimg.com/vi/oUon62EIInc/maxresdefault.jpg', u'\u05d3\u05d5\u05e7\u05d5\u05de\u05e0\u05d8\u05e8\u05d9': 'http://img.mako.co.il/2017/03/28/704104_I.jpg', u'\u05d0\u05d9\u05de\u05d4': 'http://up203.siz.co.il/up2/y12o20immdyw.jpg', u'\u05de\u05d5\u05ea\u05d7\u05df': 'http://www.brz.co.il/wp-content/uploads/2014/06/11-350x350.jpg', u'\u05de\u05d3\u05e2 \u05d1\u05d3\u05d9\u05d5\u05e0\u05d9': domain_s+'upload.wikimedia.org/wikipedia/commons/c/cc/4pen.jpg', u'\u05d0\u05e7\u05e9\u05df': domain_s+'www.renne.co.il/wp-content/uploads/2017/07/actionsign.jpg'}
def get_allu_links(url):
    import requests,binascii,math
    html,cook=cloudflare.request(url)#requests.get(url,headers=headers,cookies=cookies).content
 
    regex='var aaa = (.+?);'
    match_a=re.compile(regex).findall(html)

    regex='var bbb = (.+?);'
    match_b=re.compile(regex).findall(html)

    regex='var ccc = (.+?);'
    match_c=re.compile(regex).findall(html)

    regex='var ddd = (.+?);'
    match_d=re.compile(regex).findall(html)

    regex="document.write\(decrypt\('(.+?)', '(.+?)'"
    match_links=re.compile(regex).findall(html)

    for code,key in match_links:
        r=code
        t=key
        aaa = match_a[0].replace("'",'')
        bbb = match_b[0].replace("'",'')
        ccc = match_c[0].replace("'",'')
        ddd = match_d[0].replace("'",'')

        e = ""


        o = r[0: 3]
        r = r[3:]

        
        '''
        def a2b(a):
          b, c, d, e = {}, f = 0, g = 0, h = "", i = ' ', j = len(a)
          for (b = 0; 64 > b; b++) 
             e["ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charAt(b)] = b
          for (c = 0; j > c; c++) for (b = e[a.charAt(c)], f = (f << 6) + b, g += 6; g >= 8; ) ((d = 255 & f >>> (g -= 8)) || j - 2 > c) && (h += i(d));
          return h;
        '''

        def hta(r):
            t = str(r)
            e=""
           
            for o in range(0, len(t)-1,2):
             
               
               
               e += chr(int(t[o: o+2], 16))
            return e

        def strswpcs(r):
            t=""
           
            t=''.join(c.lower() if c.isupper() else c.upper() for c in r)

              
              #t += r[e].match('/^[A-Za-z]$/') ? r[e] === r[e].toLowerCase() ? r[e].toUpperCase() : r[e].toLowerCase() : r[e];
            return t



        def ord2(r):
            t = r + ""

            e = ord(t[0])
            if (e >= 55296 and 56319 >= e) :
                o = e
                if len(t)==1:
                  return e
                else:
                  return  1024 * (o - 55296) + (ord(t[1]) - 56320) + 65536
                
            
            return e


        if ("3" + aaa + "f" == o ):

          r = (binascii.a2b_base64(r))[::-1]

        elif ("f" + bbb + "0" == o):

          r = hta((r)[::-1]) 

        elif ("6" + ccc + "3" == o):

          r = (binascii.a2b_base64(r[::-1]))

        elif ("5" + ddd + "a" == o):
 
          r = binascii.a2b_base64(strswpcs(r))
          

        s = 0;
   
   
        for s in range (0,len(r)-1):
            n = r[s]

            a = t[s % len(t) - 1: 1]

            n = math.floor(ord2(n) - ord2(a))

            n = chr(int(n))
          
            e += n

        regex='"(.*?)"'
        match=re.compile(regex).findall(e)
       
        if len (match)>0:
         
          if 'pron.' in match[0]:
              
       
              html2,cook=cloudflare.request(url)#requests.get(match[0],headers=headers,cookies=cookies).content
              regex2='<a href="(.+?)"'
              match2=re.compile(regex2).findall(html2)
         
              return match2[0]
         
          else:
            
            if 'src="' in e.lower():
              regex2='iframe.+?src=(?:"|\')(.+?)(?:"|\')'
              match2=re.compile(regex2).findall(e)
          
              return match2[0]
            else:
              return match[0]
        else:
          
          return e
def get_custom_params(item):
        param=[]
        item=item.split("?")
        if len(item)>=2:
          paramstring=item[1]
          
          if len(paramstring)>=2:
                params=item[1]
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

def addNolink( name, url,mode,isFolder, iconimage="DefaultFolder.png",fanart="DefaultFolder.png",description=' '):
 

          
         
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name),'plot':description   })
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","false")
          liz.setProperty( "Fanart_Image", fanart )
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################        

def addDir3(name,url,mode,iconimage,fanart,description,data=' ',original_title=' ',id=' ',season=' ',episode=' ',tmdbid=' ',eng_name=' ',show_original_year=' ',rating=0,heb_name=' ',isr=0,generes=' ',trailer=' ',dates=' '):
        te1=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        
        te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description.encode('utf8'))+"&heb_name="+(heb_name)+"&dates="+(dates)
        te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
        te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)+"&isr="+str(isr)
        
        
        
        
        u=te1 + te2 + te3 + te4.decode('utf8')
 
        ok=True
        video_data={}
        video_data['title']=original_title
        if episode!=' ':
          video_data['mediatype']='tvshow'
          video_data['TVshowtitle']=original_title
          video_data['Season']=int(str(season).replace('%20','0'))
          video_data['Episode']=int(str(episode).replace('%20','0'))
        else:
           video_data['mediatype']='movies'
           video_data['TVshowtitle']=''
           video_data['tvshow']=''
           video_data['season']=0
           video_data['episode']=0
        video_data['OriginalTitle']=original_title
        video_data['year']=data
        video_data['genre']=generes
        video_data['rating']=str(rating)
    
        video_data['poster']=fanart
        video_data['plot']=description
        video_data['trailer']=trailer
        menu_items=[]

        
        str_e1=list(u.encode('utf8'))
        for i in range(0,len(str_e1)):
           str_e1[i]=str(ord(str_e1[i]))
        str_e='$$'.join(str_e1)
        file_data=[]
        change=0

        if os.path.exists(save_file):
            f = open(save_file, 'r')
            file_data = f.readlines()
            f.close()
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s'"%(original_title.replace("'"," ").replace(" ","%20").replace(':','%3a').replace("'",'%27')))

        match = dbcur.fetchone()
        if match!=None:
        
          menu_items.append(('[COLOR peru][I]הסר ממעקב סדרות[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode=34&name=%s&id=0')%(sys.argv[0],original_title,name)))
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s'  AND season='%s' AND episode = '%s'"%(original_title.replace("'"," ").replace(" ","%20").replace(':','%3a').replace("'",'%27'),season,episode))
     
        match = dbcur.fetchone()
        if match!=None:
        
          menu_items.append(('[COLOR pink][I]הסר סימון נצפה[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&original_title=%s&mode=34&name=%s&id=1&season=%s&episode=%s')%(sys.argv[0],original_title,name,season,episode))) 
          
        if str_e+'\n' not in file_data:
           menu_items.append(('[COLOR lightblue][I]הוספה למועדפים שלי[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&description=%s&mode=17')%(sys.argv[0],str_e)))
           
        else:
           
           menu_items.append(('[COLOR red][I]הסרה מהמועדפים שלי[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&description=%s&mode=19')%(sys.argv[0],str_e)))
        menu_items.append(('פרטים', 'Action(Info)'))
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(menu_items, replaceItems=False)
        
        liz.setInfo( type="Video", infoLabels=video_data)
        liz.setProperty( "Fanart_Image", fanart )
        art = {}
        art.update({'poster': iconimage})
        liz.setArt(art)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok



def addLink( name, url,mode,isFolder, iconimage,fanart,description,data='',original_title=' ',id=' ',season=' ',episode=' ',rating=0,saved_name=' ',prev_name=' ',eng_name=' ',heb_name=' ',show_original_year=' ',num_in_list=None):
          url=url.encode('utf8')
          try:
            name=urllib.unquote(name)
          except:
            pass
          name=name.replace("openload","vumoo").replace("Openload","vumoo")
          description=description.replace("openload","vumoo").replace("Openload","vumoo")
          name=name.replace("thevideo","tvumoo.li")
          description=description.replace("thevideo","tvumoo.li")
          te1=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
          te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+(description)+"&heb_name="+(heb_name)
          te3="&data="+str(data)+"&original_title="+(original_title)+"&id="+(id)+"&season="+str(season)
          te4="&episode="+str(episode)
        
       
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+(name)+"&data="+str(data)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+(description)+"&original_title="+(original_title)+"&id="+str(id)+"&season="+str(season)+"&episode="+str(episode)+"&saved_name="+str(saved_name)+"&prev_name="+str(prev_name)+"&eng_name="+str(eng_name)+"&heb_name="+str(heb_name)+"&show_original_year="+str(show_original_year)
 

          
          menu_items=[]
          video_data={}
          video_data['title']=name
          video_data['season']=season
          video_data['episode']=episode
          video_data['poster']=fanart
          video_data['plot']=description
          video_data['rating']=str(rating)
          #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels=video_data)
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )
          if num_in_list!=None:
             menu_items.append(('[COLOR red][I]הסרה מהמועדפים שלי[/I][/COLOR]', 'XBMC.RunPlugin(%s)' % ('%s?url=www&description=%s&mode=20')%(sys.argv[0],num_in_list)))
          liz.addContextMenuItems(menu_items, replaceItems=False)
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)

def save_to_fav(plot):

    
    

    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
    
    if plot+'\n' not in file_data:
      file_data.append(plot)
      change=1
    for i in range (len(file_data)-1,0,-1):
         file_data[i]=file_data[i].replace('\n','')
         if len(file_data[i])<3:
          
          file_data.pop(i)
          change=1
    if change>0:
       
          file = open(save_file, 'w')
          file.write('\n'.join(file_data))
          file.close()
          xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'נשמר')).encode('utf-8'))
def read_site_html(url_link):
    import requests
    '''
    req = urllib2.Request(url_link)
    req.add_header('User-agent',__USERAGENT__)# 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    html = urllib2.urlopen(req).read()
    '''
    html=requests.get(url_link)
    return html
def get_tv_poster():


      import random
      all_img=[]
      url=domain_s+'api.themoviedb.org/3/tv/top_rated?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US'
      x=requests.get(url).json()
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
             else:
              fan=domain_s+'image.tmdb.org/t/p/original/'+items['backdrop_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img
def get_movie_poster():


      import random
      all_img=[]
      url=domain_s+'api.themoviedb.org/3/movie/top_rated?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US'
      x=requests.get(url).json()
      for items in x['results']:
          if 'backdrop_path' in items:
             if items['backdrop_path']==None:
              fan=' '
             else:
              fan=domain_s+'image.tmdb.org/t/p/original/'+items['backdrop_path']
              all_img.append(fan)
      random.shuffle(all_img)
      return all_img
def main_menu():


      dbcur.execute("SELECT COUNT(*) FROM AllData")

      match = dbcur.fetchone()
      level_index=(match[0]/100)
      if level_index>9:
        level_index=9
      addDir3('סרטים'.decode('utf8'),'www',13,domain_s+'vignette.wikia.nocookie.net/survivor-org/images/f/f7/13432033-movie-theme-design.jpg/revision/latest?cb=20140512163942',domain_s+'images.fandango.com/ImageRenderer/0/0/redesign/static/img/default_poster.png/0/images/masterrepository/other/INTRO_AvengersAgeUltron_FINAL.jpg','סרטים'.decode('utf8'))
      addDir3('סדרות'.decode('utf8'),'www',14,'http://hd.wallpaperswide.com/thumbs/vikings_tv_show-t2.jpg',domain_s+'vignette.wikia.nocookie.net/grimm/images/1/19/Season_6_Poster_v2_wide.jpg/revision/latest?cb=20161010171057','סדרות'.decode('utf8'))
      addDir3('חיפוש'.decode('utf8'),'www',15,'http://3.bp.blogspot.com/-rAHeVUsvB6g/VE_XmOm6AXI/AAAAAAAAATg/DiwHrv72DmM/s1600/searcher.gif','http://significnet.com/wp-content/uploads/search-engins.jpg','חיפוש'.decode('utf8'))
      addDir3('מועדפים'.decode('utf8'),'all',18,domain_s+'cdn0.iconfinder.com/data/icons/sharp_folder_icons_by_folksnet/256/favorites.png','http://4.bp.blogspot.com/-8q4ops3bX_0/T0TWUOu5ETI/AAAAAAAAA1A/AQMDv0Sv4Cs/s1600/logo1.gif','מועדפים'.decode('utf8'))
      addDir3('רשימות Trakt'.decode('utf8'),'www',29,'http://koditips.com/wp-content/uploads/trakt-api-key.png',domain_s+'www.mjdtech.net/content/images/2016/02/traktfeat.jpg','רשימות Trakt')
      addDir3('ערוצי סרטים וסדרות'.decode('utf8'),'www',38,'https://lh3.googleusercontent.com/XYa0sUr3lFYPwJWmc3SJsQLb8Be2EY8RuSZ72uaWscNx3oz_OgDey6BRPvOjbt1vDHo','https://digitalcontentguide.com.au/wp-content/uploads/2014/07/moviestv_banner.png','ערוצי סרטים וסדרות')
      
      addNolink('ניקוי מטמון','www',16,False,iconimage=domain_s+'encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQPFxfTBe7pS6M_C2EOKzjgC3Sx1IdMP8A-dMfYxSkPHMo0APcM_w',fanart=domain_s+'dahliasavage.files.wordpress.com/2014/11/despicable-me-2-animation-cleaning-home-4084.jpg')
      addDir3('[COLOR yellow][I]בדיקת שרתים[/I][/COLOR]'.decode('utf8'),'www',98,'http://www.bandwidthplace.com/wp/wp-content/uploads/2014/10/servers_and_speed_tests.png',domain_s+'sqlundercover.files.wordpress.com/2018/01/eniac_.jpg?w=736','בדיקת שרתים'.decode('utf8'))
      addNolink('פתח הגדרות','www',24,False,iconimage='http://www.endlessicons.com/wp-content/uploads/2012/11/setting-icon.png',fanart=domain_s+'www.wanderlustworker.com/wp-content/uploads/2014/05/setting-smarter-goals.jpg')
      plot='[COLOR gold]'+'אתה כרגע בשלב '+str(level_index+1)+'\n'+'עד עכשיו צפית ב '+str(match[0]) +' סרטים ופרקים '+' תמשיך ככה.... '+'[/COLOR]'+'\nעוד ' +str((100*(level_index+1))-int(match[0]))+' כדי לעבור לשלב הבא :-)'
      addLink('[COLOR khaki][I]'+'הדירוג שלי'+'[/I][/COLOR]',level_movies[level_index],35,False,iconimage=level_images[level_index],fanart=level_fanart[level_index],description=plot)
def movies_menu():
      #all_img=get_movie_poster()
      all_img=cache.get(get_movie_poster,24, table='posters')

      addDir3('סגנונות'.decode('utf8'),'http://api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&page=1',2,'http://blog.tapuz.co.il/MoviesAndSeries/images/3737266_2.jpg',all_img[0],'סרטים'.decode('utf8'))
      addDir3('סרטים פופולרים'.decode('utf8'),'http://api.themoviedb.org/3/movie/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&page=1',3,domain_s+'cdn.xl.thumbs.canstockphoto.co.il/%D7%A1%D7%A8%D7%98%D7%99%D7%9D-%D7%9E%D7%95%D7%A9%D7%92-%D7%A7%D7%95%D7%9C%D7%A0%D7%95%D7%A2-%D7%90%D7%99%D7%95%D7%A8-%D7%A1%D7%98%D7%95%D7%A7_csp41044564.jpg',all_img[1],'סרטים פופולרים'.decode('utf8'))
      addDir3('סרטים לפי שנים'.decode('utf8'),'movie_years&page=1',3,'http://www.greenmancreations.com/images/logo-design/movieworld-logo.jpg',all_img[2],'סרטים לפי שנים'.decode('utf8'))
      addDir3('סרטים ישראלים'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&sort_by=popularity.desc&include_adult=false&include_video=false&with_original_language=he&page=1',3,domain_s+'s-media-cache-ak0.pinimg.com/236x/da/b0/9e/dab09e9a53a39abf8ef1246b3fd605e6--israel-youth.jpg',all_img[3],'סרטים ישראלים'.decode('utf8'),isr=1)
      addDir3('סרטים ישראלים לפי שנים'.decode('utf8'),'movie_years&page=1',3,domain_s+'hautevitrine.files.wordpress.com/2011/10/1974-united-israel-appeal-poster-by-paul-kor-tel-aviv-2011.jpg',all_img[6],'סרטים ישראלים לפי שנים'.decode('utf8'),isr=1)
      addDir3('סרטים מועדפים'.decode('utf8'),'movies',18,domain_s+'cdn0.iconfinder.com/data/icons/sharp_folder_icons_by_folksnet/256/favorites.png','http://4.bp.blogspot.com/-8q4ops3bX_0/T0TWUOu5ETI/AAAAAAAAA1A/AQMDv0Sv4Cs/s1600/logo1.gif','מועדפים'.decode('utf8'))
      addDir3('נצפה לאחרונה'.decode('utf8'),'movie',32,domain_s+'images.gr-assets.com/books/1485469752l/33260180.jpg',all_img[7],'סרטים אחרונים שנצפו'.decode('utf8'),isr=0)
      addDir3('חפש סרט'.decode('utf8'),'http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&append_to_response=origin_country&page=1',3,domain_s+'cellcomtv.cellcom.co.il/globalassets/cellcomtv/content/sratim/pets-secret-life/480x543-template.jpg','http://www.videomotion.co.il/wp-content/uploads/whatwedo-Pic-small.jpg','חפש סרט'.decode('utf8'))
      addDir3('[I]מומלצים עבורך[/I]'.decode('utf8'),'www',26,domain_s+'i.pinimg.com/564x/fc/79/15/fc79150482303ac1d7e4d7133c8c5d6e--candida-overgrowth-candida-diet.jpg',all_img[4],'סרטים מומלצים עבורך לפי הסטוריית הצפייה שלך'.decode('utf8'),isr=0)
      addDir3('[I]שחרורי HD אחרונים[/I]'.decode('utf8'),domain_s+'www.dvdsreleasedates.com/movies/',28,domain_s+'seeklogo.com/images/F/Full_HD_1080-logo-EF7336DA95-seeklogo.com.png',all_img[5],'סרטים מומלצים עבורך לפי הסטוריית הצפייה שלך'.decode('utf8'),isr=0)
      addDir3('[COLOR yellow][I]סרטים מדובבים[/I][/COLOR]'.decode('utf8'),'0',11,domain_s+'www.flatpanelshd.com/pictures/despicableme2-1l.jpg','http://4k.com/wp-content/uploads/2014/11/toystory3_img10_720-790x442.jpg','סרטים ישראלים'.decode('utf8'))
      addDir3('[COLOR gold]תן לי באיכות[/COLOR]'.decode('utf8'),domain_s+'www.mehlizmovieshd.com/genre/4k-2160p-movies/',10,'http://cdn.techgyd.com/150-Most-Amazing-4K-Wallpaper-for-your-Devices-42.jpg',domain_s+'i.ytimg.com/vi/vrbaJ1_FPq0/maxresdefault.jpg','סרטי 4K'.decode('utf8'))

def tv_menu():
      import datetime
      now = datetime.datetime.now()
      all_img=cache.get(get_tv_poster,24, table='posters')

      addDir3('[COLOR lightblue]סגנונות[/COLOR]'.decode('utf8'),'http://api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&page=1',2,'http://img0.liveinternet.ru/images/attach/c/1//49/86/49086845_14270296_1.jpg',all_img[0],'סדרות'.decode('utf8'))
      addDir3('[COLOR lightblue]סדרות פופולריות[/COLOR]'.decode('utf8'),'http://api.themoviedb.org/3/tv/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&page=1',3,'http://culture.bestoneonline.co.il/wp-content/uploads/sites/11/2016/07/%D7%A1%D7%93%D7%A8%D7%95%D7%AA.jpg',all_img[1],'סדרות פופולריות'.decode('utf8'))
      addDir3('[COLOR lightblue]סדרות לפי שנים[/COLOR]'.decode('utf8'),'tv_years&page=1',3,domain_s+'lh5.ggpht.com/cr6L4oleXlecZQBbM1EfxtGggxpRK0Q1cQ8JBtLjJdeUrqDnXAeBHU30trRRnMUFfSo=w300',all_img[2],'סדרות לפי שנים'.decode('utf8'))
      addDir3('[COLOR lightblue]סדרות חדשות[/COLOR]'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US&sort_by=popularity.desc&first_air_date_year='+str(now.year)+'&timezone=America%2FNew_York&include_null_first_air_dates=false&language=he&page=1',3,domain_s+'lh5.ggpht.com/cr6L4oleXlecZQBbM1EfxtGggxpRK0Q1cQ8JBtLjJdeUrqDnXAeBHU30trRRnMUFfSo=w300',all_img[3],'סדרות לפי שנים'.decode('utf8'))
      addDir3('[COLOR lightblue]סדרות ישראליות[/COLOR]'.decode('utf8'),domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&sort_by=popularity.desc&timezone=America%2FNew_York&include_null_first_air_dates=false&with_original_language=he&page=1',3,'http://escapism.co.il/wp-content/uploads/2018/01/fauda-768x671.jpg',all_img[4],'סדרות ישראליות'.decode('utf8'),isr=1)
      addDir3('[COLOR lightblue]סדרות מועדפות[/COLOR]'.decode('utf8'),'tv',18,domain_s+'cdn0.iconfinder.com/data/icons/sharp_folder_icons_by_folksnet/256/favorites.png','http://4.bp.blogspot.com/-8q4ops3bX_0/T0TWUOu5ETI/AAAAAAAAA1A/AQMDv0Sv4Cs/s1600/logo1.gif','מועדפים'.decode('utf8'))
      addDir3('[COLOR lightblue][I]מומלצים עבורך[/I][/COLOR]'.decode('utf8'),'www',27,domain_s+'www.maxrealestateexposure.com/wp-content/uploads/2011/10/Recommendation.jpg',all_img[5],'סדרות מומלצות עבורך על פי היסטוריית הצפייה שלך'.decode('utf8'),isr=0)
      addDir3('[COLOR deeppink][I]מעקב סדרות[/I][/COLOR]'.decode('utf8'),'tv',32,domain_s+'pbs.twimg.com/profile_images/873323586622078976/Z0BfwrYm.jpg',all_img[6],'פרקים אחרונים שנצפו'.decode('utf8'),isr=0)
      
      addDir3('[COLOR lightblue]חפש סידרה[/COLOR]'.decode('utf8'),'http://api.themoviedb.org/3/search/tv?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&page=1',3,domain_s+'img.wcdn.co.il/f_auto,w_700,t_18/1/0/7/2/1072572-46.jpg',domain_s+'f.frogi.co.il/news/640x300/010170efc8f.jpg','חפש סידרה'.decode('utf8'))

def search_menu():

      addDir3('חפש סרט'.decode('utf8'),'http://api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&append_to_response=origin_country&page=1',3,domain_s+'cellcomtv.cellcom.co.il/globalassets/cellcomtv/content/sratim/pets-secret-life/480x543-template.jpg','http://www.videomotion.co.il/wp-content/uploads/whatwedo-Pic-small.jpg','חפש סרט'.decode('utf8'))
      addDir3('[COLOR yellow][I]חיפוש סרטים מדובבים[/I][/COLOR]'.decode('utf8'),'search',11,'http://2.bp.blogspot.com/-vDRXO2qGAFc/UyCAFd2LAPI/AAAAAAAAEco/pIfXWlRJG6Q/s1600/images+(9).jpg',domain_s+'i.pinimg.com/originals/c1/cb/ed/c1cbede7238494e7878f7107ed478d79.jpg','סרטים ישראלים'.decode('utf8'))
      addDir3('[COLOR lightblue]חפש סידרה[/COLOR]'.decode('utf8'),'http://api.themoviedb.org/3/search/tv?api_key=34142515d9d23817496eeb4ff1d223d0&query=%s&language=he&page=1',3,domain_s+'img.wcdn.co.il/f_auto,w_700,t_18/1/0/7/2/1072572-46.jpg',domain_s+'f.frogi.co.il/news/640x300/010170efc8f.jpg','חפש סידרה'.decode('utf8'))
def get_genere(link):
   images={}
   html=requests.get(link).json()
   for data in html['genres']:
     if '/movie' in link:
       new_link='http://api.themoviedb.org/3/genre/%s/movies?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&page=1'%str(data['id'])
     else:
       new_link='http://api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&sort_by=popularity.desc&with_genres=%s&language=he&page=1'%str(data['id'])
     if data['name'] in tv_images:
       image=tv_images[data['name']]
     elif data['name'] in movie_images:
       image=movie_images[data['name']]
     addDir3(data['name'],new_link,3,image,image,data['name'])
def movies_channel():
    addLink('ערוץ הסרטים של הנוקם'.decode('utf8'),domain_s+'raw.githubusercontent.com/shimonar/sh/master/%D7%94%D7%A0%D7%95%D7%A7%D7%9D%20%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%9F%20.txt',36,False,'https://imgcs.artprintimages.com/img/print/print/the-avengers-age-of-ultron-captain-america-black-widow-hulk-hawkeye-vision-iron-man-thor_a-l-14824548-11969363.jpg?w=550&h=550','https://i.kinja-img.com/gawker-media/image/upload/s--fWBQap3Z--/c_scale,f_auto,fl_progressive,q_80,w_800/1234660079547003496.jpg','ערוץ הסרטים של הנוקם')
    addLink("ערוץ המדובבים".decode('utf8'),domain_s+'goo.gl/vCA3Mq',36,False,'http://icons.iconarchive.com/icons/3xhumed/mega-games-pack-31/256/Cars-pixar-4-icon.png','https://www.filminquiry.com/wp-content/uploads/2015/10/Pixar.jpg',"ערוץ המדובבים")
    addLink("הערוץ של ONI".decode('utf8'),'www',37,False,'https://upload.wikimedia.org/wikipedia/en/thumb/2/2e/Oni_Coverart.jpg/220px-Oni_Coverart.jpg','http://nerdtrek.com/wp-content/uploads/2011/07/streaming-tv-movies.jpg',"הערוץ של ONI")
    addLink("הערוץ של 1M".decode('utf8'),'www',39,False,'https://thehaletelescope.com/wp-content/uploads/2017/08/war-movies.jpg','https://lumiere-a.akamaihd.net/v1/images/h_blackpanther_intheaters_61ff73b4.jpeg?region=0,0,2048,832',"הערוץ של 1M")
def get_movies(url,isr,reco=0,new_name_array=[]):
   all_years=[]
   import datetime
   now = datetime.datetime.now()
   for year in range(now.year,1970,-1):
         all_years.append(str(year))
   if url=='movie_years&page=1':
     
      
      ret=ret = xbmcgui.Dialog().select("בחר שנה", all_years)
      if ret!=-1:
        if isr==1:
          url=domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=he&page=1'%all_years[ret]
          
        else:
          url=domain_s+'api.themoviedb.org/3/discover/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&sort_by=popularity.desc&include_adult=false&include_video=false&primary_release_year=%s&with_original_language=he|en&page=1'%all_years[ret]
        
      else:
        sys.exit()
   if url=='tv_years&page=1' and 'page=1' in url:
      
      ret=ret = xbmcgui.Dialog().select("בחר שנה", all_years)
      if ret!=-1:
        url=domain_s+'api.themoviedb.org/3/discover/tv?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&sort_by=popularity.desc&first_air_date_year=%s&include_null_first_air_dates=false&with_original_language=en|he&page=1'%all_years[ret]
       
      else:
        sys.exit()
   if '/search' in url and 'page=1' in url:
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
        keyboard.doModal()
        if keyboard.isConfirmed():
               search_entered = keyboard.getText()
               url=url%urllib.quote_plus(search_entered)
        else:
          sys.exit()

   html=requests.get(url).json()
   
   if '/tv/' in url:
     url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
     
   else:
     url_g=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
   html_g=requests.get(url_g).json()
   
   if Addon.getSetting("dp")=='true' and (Addon.getSetting("disapear")=='true' or Addon.getSetting("check_subs")=='true'):
            dp = xbmcgui.DialogProgress()
            dp.create("טוען סרטים", "אנא המתן", '')
            dp.update(0)
   xxx=0
   start_time = time.time()
   
   for data in html['results']:
     if 'vote_average' in data:
       rating=data['vote_average']
     else:
      rating=0
     if 'first_air_date' in data:
       year=str(data['first_air_date'].split("-")[0])
     else:
        year=str(data['release_date'].split("-")[0])
     if data['overview']==None:
       plot=' '
     else:
       plot=data['overview']
     if 'title' not in data:
       new_name=data['name']
     else:
       new_name=data['title']
     f_subs=[]
     if 'original_title' in data:
       original_name=data['original_title']
       mode=4
       
       id=str(data['id'])
       if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
         f_subs=cache.get(get_subs,9999,'movie',original_name,'0','0',id,year,True, table='pages')
       
       
     else:
       original_name=data['original_name']
       id=str(data['id'])
       mode=7
     if data['poster_path']==None:
      icon=' '
     else:
       icon=data['poster_path']
     if 'backdrop_path' in data:
         if data['backdrop_path']==None:
          fan=' '
         else:
          fan=data['backdrop_path']
     else:
        fan=html['backdrop_path']
     if plot==None:
       plot=' '
     if 'http' not in fan:
       fan=domain_s+'image.tmdb.org/t/p/original/'+fan
     if 'http' not in icon:
       icon=domain_s+'image.tmdb.org/t/p/original/'+icon
     genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
            if i['name'] is not None])
     try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
     except:genere=''

     trailer = "plugin://plugin.video.allmoviesin?mode=25&url=www&id=%s" % id
     if new_name not in new_name_array:
      new_name_array.append(new_name)
      if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
          if len(f_subs)>0:
            color='white'
          else:
            color='red'
            
      else:
         color='white'

      dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' "%(original_name.replace("'"," ").replace(" ","%20").replace(':','%3a').replace("'",'%27'),'movie'))

      match = dbcur.fetchone()

      if match!=None:
        
        color='magenta'
      elapsed_time = time.time() - start_time
      if (Addon.getSetting("check_subs")=='true'  or Addon.getSetting("disapear")=='true') and Addon.getSetting("dp")=='true':
        dp.update(int(((xxx* 100.0)/(len(html['results']))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
      xxx=xxx+1
      if  Addon.getSetting("disapear")=='true' and color=='red' and mode!=7:
        a=1
      else:
        if mode==7:
          color='white'
          dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s'"%(urllib.quote_plus(original_name.encode('utf8')).replace("+","%20")))
         
          match = dbcur.fetchone()

          if match!=None:
            color='orange'
        addDir3('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer)
   regex='page=(.+?)$'
   match=re.compile(regex).findall(url)
   link=url.split('page=')[0]
   
   if reco==0:
     addDir3('[COLOR aqua][I]עוד תוצאות[/I][/COLOR]'.decode('utf8'),link+'page='+str(int(match[0])+1),3,' ',' ','עוד תוצאות'.decode('utf8'),isr=isr)
   xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
   xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

   xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
   return new_name_array
def get_daily(url2,original_title,season_n,episode_n,season,episode):
    global link_daily,pr_dai,stop_all
    
    html=requests.get(url2).json()
  
    all_links=[]
    zz=0
    for data in html['list']:
      #try:
       if stop_all==1:
         break
       if len(data['title'])>1 and data['title']!=None:
           info=(PTN.parse(data['title']))
           info['season']="0"
           info['episode']="0"
           zz=zz+1
           regex_s_e=' s(.+?)e(.+?)(?: |])'
           match_s_e=re.compile(regex_s_e,re.IGNORECASE).findall(data['title'].lower())
     
           if len(match_s_e)>0:
             data['title']=data['title']+' season '+match_s_e[0][0]+' episode '+match_s_e[0][1]
         
           if 'season' in data['title'].lower() and 'episode' in data['title'].lower():
             re_s='season (.+?) episode (.+?) '
             match=re.compile(re_s,re.IGNORECASE).findall(data['title'].lower())
             if len (match)>0:
             
               info['season']=match[0][0]
               info['episode']=match[0][1]
             else:
               info['season']="0"
               info['episode']="0"

           
           if season!=None and season!="%20":
               if "עונה" in data['title'].encode('utf8') or  "פרק" in data['title'].encode('utf8'):
                 syntex="עונה %s פרק %s "%(season,episode)
                 syntex2="S%sE%s"%(season_n,episode_n)
                 syntex3="S%s E%s"%(season_n,episode_n)
                 syntex4="עונה %s פרק %s"%(season,episode)
                
                 if syntex in data['title'] or syntex2.lower()+'@@@@@@' in data['title'].lower()+'@@@@@@' or syntex3.lower()+'@@@@@@' in data['title'].lower()+'@@@@@@' or syntex4.lower()+'@@@@@@' in data['title'].lower()+'@@@@@@':
                   quality=' '
                   if 'available_formats' in data:
                        for qu in data['available_formats']:
                          quality=qu.upper().replace("HD720","720p").replace("HD480","480p").replace("HD360","360p").replace("HD240","240p").replace("HD1080","1080p")

                   all_links.append((('http://www.dailymotion.com/video/'+data['id']),data['title'],'Daily',quality))
               else:
             
                  try:
                    if (int(data['duration'])>900) and original_title.lower().replace("%20"," ") in data['title'].lower() and int(season) == int(info['season']) and int(episode_n)==int( info['episode']): #15 min minimum
                      quality=' '
                
                      if 'available_formats' in data:
                        for qu in data['available_formats']:
                          quality=qu.upper().replace("HD720","720p").replace("HD480","480p").replace("HD360","360p").replace("HD240","240p").replace("HD1080","1080p")
                      all_links.append((('http://www.dailymotion.com/video/'+data['id']),data['title'],'Daily',quality))
                  except:
                   pass
              
           else:
             
             if (int(data['duration'])>900) and original_title.lower() in data['title'].lower(): #15 min minimum
                quality=' '
                if 'available_formats' in data:
                        for qu in data['available_formats']:
                          quality=qu.upper().replace("HD720","720p").replace("HD480","480p").replace("HD360","360p").replace("HD240","240p").replace("HD1080","1080p")
                all_links.append((('http://www.dailymotion.com/video/'+data['id']),data['title'],'Daily',quality))
           link_daily=all_links
      #except:
      # pass
       
    return all_links
def similar(w1, w2):
    from difflib import SequenceMatcher
    
    s = SequenceMatcher(None, w1, w2)
    return int(round(s.ratio()*100))
    
def get_dlt(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
    global link_dlt
   

    all_links=[]
    import HTMLParser
    html_parser = HTMLParser.HTMLParser()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'vexmovies.org',
        'Pragma': 'no-cache',
        #'Referer': domain_s+'vexmovies.org/?s=the+matrix',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }

    params = (
        ('s', clean_name(original_title,1)+' '+show_original_year),
    )

    response = requests.get(domain_s+'vexmovies.org/', headers=headers, params=params).content
    regex='<h1>Results: (.+?)</h1>.+?<a href="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(response)
    
    for name,link in match:
      if clean_name(original_title,1).lower() in name.lower() and show_original_year in name.lower():
        yy=requests.get(link,headers=headers).content
        regex='<iframe src="(.+?)"'
        match2=re.compile(regex).findall(yy)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'consistent.stream',
            'Pragma': 'no-cache',
            'Referer': link,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
        zz=requests.get(match2[0],headers=headers).content
 
        regex='player.+?title="(.+?)"'
        match3=re.compile(regex).findall(zz)
        
        link_results=json.loads(html_parser.unescape(match3[0]))
        for sources_o in link_results['servers']:
          for sources in sources_o['sources']:
              
              if 'Openload' in sources_o['name'] or 'SE' in sources_o['name']:
                  name1,match_s,res,check=server_data(sources['src'],original_title)
                  if check :
                    all_links.append((name1,sources['src'],match_s,res))
                    link_dlt=all_links
              else:
                  if "1080" in sources['src']:
                    res="1080"
                  elif "720" in sources['src']:
                    res="720"
                  elif "480" in sources['src']:
                    res="720"
                  elif "hd" in sources['src'].lower():
                    res="HD"
                  else:
                   res=' '
                  link=sources['src']
                  if 'mentor' in link:
                   headers = {
                        'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Host': 'mentor.dfcdn.net',
                        'Pragma': 'no-cache',
                        'Range': 'bytes=0-',
                        'Referer': match2[0],
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                   }
                   head=urllib.urlencode(headers)
            
                   link=link+"|"+head
                  all_links.append((original_title,link,sources_o['name'],res))
                  link_dlt=all_links
    return all_links
def get_showbox(tv_movie,original_title,season_n,episode_n,season,episode,year):
    global link_showbox,pr_sb,stop_all
    all_links=[]
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'my-project-free.tv',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }

    response = requests.get(domain_s+'my-project-free.tv/episode/%s-season-%s-episode-%s/'%(original_title.lower().replace('%20','-').replace('%3a','').replace(' ','-'),season,episode), headers=headers).content
    regex="callvalue\('.+?','.+?','(.+?)'"
    
    match=re.compile(regex).findall(response)
    

    for link in match:
        if stop_all==1:
          break
        name1,match_s,res,check=server_data(link,original_title)
        if check:
          all_links.append((name1.replace("%20"," "),link,match_s,res))
          link_showbox=all_links
    return all_links
def get_showbox_old(tv_movie,original_title,season_n,episode_n,season,episode,year):
    global link_showbox,pr_sb
    from   showbox  import source
    import requests
    blank=[]
    try:
        url2='http://www.omdbapi.com/?apikey=8e4dcdac&t=%s&year=%s'%(original_title,year)

        imdb_id="0"
        try:
           imdb_id=requests.get(url2).json()['imdbID']
        except:
          pass
        if tv_movie=='movie':
          x=source().movie(imdb_id, original_title, original_title, original_title, year)
        else:
          x=source().tvshow(imdb_id,' ', original_title, original_title, original_title, year) 
          x=source().episode(x, imdb_id, ' ', original_title, year, season, episode)
        y=source().sources(x)
      
        
        sources = [json.loads(t) for t in set(json.dumps(d, sort_keys=True) for d in y)]
        all_links=[]
        zz=0
        for su in sources:
          pr_sb=(zz*100)/len(sources)
          zz=zz+1
          all_links.append((original_title.replace("%20"," "),su['url'],su['source'],su['quality']))
          link_showbox=all_links
        return all_links
    except:
      return blank
def fix_q(quality):
    f_q=100
    if '2160' in quality:
      f_q=1
    if '1080' in quality:
      f_q=2
    elif '720' in quality:
      f_q=3
    elif '480' in quality:
      f_q=4
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q=5
    elif '360' in quality or 'sd' in quality.lower():
      f_q=6
    elif '240' in quality:
      f_q=7
    return f_q


def get_c(url):
    import js2py_o
    regex=",S='(.+?)'"
    s_val=re.compile(regex,re.DOTALL).findall(url)[0]

    regex="var A='(.+?)'"
    a_val=re.compile(regex,re.DOTALL).findall(url)[0]
    s={}
    L=len(s_val)
    U=0
    l=0
    a=0
    r=''
  
    for i in range(0,len(a_val)):
      s[a_val[i]]=i
    for i in range(0,len(s_val)):
     if s_val[i]!='=':
      c=s[s_val[i]]
      U=(U<<6)+c
      
      l+=6
      while (l>=8):
        l=l-8
        
        f=(U>>l)&255
        
         
        a=f;
       
        r+=chr(a);
    result2=js2py_o.eval_js(r.replace('location.reload();','').replace('document.cookie','document'))

    return result2,s_val
def get_c_old(url):
        import js2py_o
        
        regex=",S='(.+?)'"
        match=re.compile(regex,re.DOTALL).findall(url)
        
        jscode=\
        '''
        var s={},u,c,U,r,l=0,a,e=eval,w=String.fromCharCode,sucuri_cloudproxy_js='',
        S='$$$$$$';L=S.length;U=0;r='';var A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
        for(u=0;u<64;u++)
        {
            s[A.charAt(u)]=u;
            }
        var k=0,h=0;
        for(k=0;k<L;k++)
        {
        h=k
        c=s[S.charAt(h)];
        U=(U<<6)+c;
        l+=6;
        
        while(l>=8)
        {
        ((a=(U>>>(l-=8))&0xff)||(h<(L-2)))&&(r+=w(a));
        }}; r;
        
        
        '''
        
        jscode=jscode.replace('$$$$$$',match[0])
        
        jcode2=\
        '''
        var j,document
        j="4" + 'UxF9'.substr(3, 1) +String.fromCharCode(49) + '>a'.slice(1,2)+'51'.slice(1,2)+"3" + String.fromCharCode(56) + "fsu".slice(0,1) + "5" + "9" + '46'.slice(1,2)+"4sucur".charAt(0)+"5su".slice(0,1) +  '' +String.fromCharCode(48) + 'e' +  "" +"d".slice(0,1) +  '' +"dsucur".charAt(0)+"1" + "f" + 'RyKb'.substr(3, 1) + '' +"d" + "3" + "6su".slice(0,1) + String.fromCharCode(53) + '>tHc'.substr(3, 1) + '' +'6rL5'.substr(3, 1) +'d' +  "bsucur".charAt(0)+ '' +''+"f" +  '' +''+'pT4'.charAt(2)+ '' +''+String.fromCharCode(49) +  '' +''+"0sucur".charAt(0)+ '' +'';
        document='s'+'u'+'c'+'u'+'rsuc'.charAt(0)+ 'i'+'_'+'c'+'l'+'osuc'.charAt(0)+ 'sucuriu'.charAt(6)+'sucurd'.charAt(5) + 'p'+'r'+'sucuo'.charAt(4)+ 'x'+'ysucu'.charAt(0)  +'_'+'sucuu'.charAt(4)+ 'u'+''+'i'.charAt(0)+'dsucu'.charAt(0)  +'sucur_'.charAt(5) + '9'+'3'+'8'.charAt(0)+'su2'.charAt(2)+'asuc'.charAt(0)+'7'+'asuc'.charAt(0)+ '8'+'8'+''+"=" + j + ';path=/;max-age=86400'; 
        '''
        
 
        result=js2py_o.eval_js(jscode)
  
        result2=js2py_o.eval_js(result.replace('location.reload();','').replace('document.cookie','document'))
  
        return result2,match[0]
def check_cookies(url):
    from Cookie import SimpleCookie
    coockie={}
    headers = {
    'Host': Domain_sparo,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
        
    }
    x=requests.get(url, headers=headers).content
    
    if 'var s={}' in x:
      
      coockie2,token=(get_c(x))
      cookie = SimpleCookie()
      cookie.load(str(coockie2))

      # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
      # which is incompatible with requests. Manually construct a dictionary instead.
      cookies = {}
      for key, morsel in cookie.items():
            cookies[key] = morsel.value
      cookies['XSRF-TOKEN']=str(token)
      cookies['max-age']='86400'
    return cookies
def read_sparo_html(url):
    

    



    headers = {
    'Host': Domain_sparo,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
        
    }

    cookies=cache.get(check_cookies,3,'http://'+Domain_sparo, table='cookies_sp')
    
    x=requests.get(url, headers=headers,cookies=cookies).content
    
    if 'var s={}' in x:
      
      cookies=cache.get(check_cookies,0,url, table='cookies_sp')
      #cookies=check_cookies(url)
   
      x=requests.get(url, headers=headers, cookies=cookies)
      
      x.encoding = 'utf-8'
      x=x.content
   
    return x

def get_sp(title,name,season,episode):
          global link_source1
          link_source1=[]
         
          html=read_sparo_html('http://%s/searchlike?search='%Domain_sparo+title)
          
          all_links=[]
          all_links_only=[]
          try:

            results_json=json.loads(html)
          except Exception as e:
            logging.warning(e)
            results_json=[]
            html=read_sparo_html('http://%s/searchlike?search='%Domain_sparo+name)
            try:
              results_json=json.loads(html)
            except Exception as e:
              logging.warning(e)
              results_json=[]
          
          saved_name=' '


          for record in results_json:
            saved_name=record['title']
            o_link='http://%s/'%Domain_sparo+record['categoria_name'].replace(' ','%20').encode('utf-8')+'/'+str(record['id'])+'/'+record['title'].replace(' ','%20').encode('utf-8')
            
            if (('series' in o_link) or ('סדרות' in o_link)) :
                new_mode=6

            else:
                new_mode=3

            season_title='עונה-%s'%season
            episode_title='פרק-%s'%episode
            if season!=None and season!='%20':
    
               html=read_sparo_html(o_link)
          
               regex1='<article>(.+?)</article>'
               match2=re.compile(regex1,re.DOTALL).findall(html)
               
               for m in match2:
                  regex='<a href="(.+?)">.+?src="(.+?)".+?<h.+?>(.+?)</h1>.+?<span .+?>(.+?)</span>.+?<span .+?>(.+?)</span>.+?<span .+?>(.+?)</span>.+?<br><br>(.+?)</p>'
                  match=re.compile(regex,re.DOTALL).findall(m)
                  for link,image,name,plot1,plot2,plot3,plot4 in match:
                    descrp=str(plot1.strip(' \n')+'\n'+plot2.strip(' \n')+'\n[COLOR aqua]'+plot3.strip(' \n')+'[/COLOR]\n'+plot4.strip(' \n'))
                    name_new=" ".join(name.split())
                    name_new=name_new.replace('|'," ")
                  
                    if season_title in link :
 
                      saved_link=link
                      break
   
               html=read_sparo_html(saved_link)
               regex1='<article>(.+?)</article>'
               match2=re.compile(regex1,re.DOTALL).findall(html)
  
               for m in match2:
                    regex='<a href="(.+?)">.+?src="(.+?)".+?<h.+?>(.+?)</h1>.+?<p .+?>(.+?)</p>'
                    match=re.compile(regex,re.DOTALL).findall(m)
                    for link,image,name,plot in match:
                      name=name.replace('\n','').replace('        ','')
             
                      if episode_title+" @@@@@@@@" in link+"@@@@@@@@" :
                      
                        saved_link=link
                        break
            else:
                saved_link=o_link
            
      
            html=read_sparo_html(saved_link)
            regex='<div class="nowdanlad">.+?href="(.+?)".+?"qualityinfo">(.+?)</p>.+?<div.+?>(.+?)</div>.+?</i>(.+?)</div>'
            match2=re.compile(regex,re.DOTALL).findall(html)
            
            for link,quality,name,date in match2:

                    html_source=read_sparo_html(link)
                    regex_source='class="btn btn-(.+?)" href="(.+?)"'
                    match_s=re.compile(regex_source).findall(html_source)
                    
                    xxx=0
                    for type,links_dip in match_s:
                        match_more=[]
                    
                        
                        if Domain_sparo in links_dip:
                          try:
                              html_source_dip=read_sparo_html(links_dip)
                             
                              
                              regex_source_dip='<iframe src="(.+?)"'
                              match_s_dip=re.compile(regex_source_dip).findall(html_source_dip)
                              regex_more='<source src="(.+?)" type="video/mp4">'
                              match_more=re.compile(regex_more,re.DOTALL).findall(html_source_dip)
                          except:
                            pass
                        else:
                          
                            regex_source_dip='class="btn btn-success" href="(.+?)"'
                            match_s_dip=re.compile(regex_source_dip).findall(html_source)
                        for in_link in match_s_dip:
                          if 'http' in in_link:
                              
                              names=re.compile('//(.+?)/',re.DOTALL).findall(in_link)[0]
                              if in_link not in all_links_only:
                                all_links_only.append(in_link)
                                all_links.append((saved_name,in_link,names,quality))
                                link_source1=all_links
                        for links2 in match_more:
                           
                           if 'http' in links2:
                            if 'http' in links2:
                              if 'href' in links2:
                                regex_l2='href=&quot;(.+?)&quot'
                                match_le=re.compile(regex_l2).findall(links2)
                                links2=match_le[0]
                          
                              try:
                                names=re.compile('//(.+?)/',re.DOTALL).findall(links2)[0]
                              except:
                                names='Direct'
                        
                              if links2 not in all_links_only:
                                all_links_only.append(links2)
                                all_links.append((saved_name,links2,names,quality))
                                link_source1=all_links
   
          return (all_links)

def get_allu(url):
    
    global match_a,next_p_all,match,pr_au
    html, cookie = cloudflare.request(url)


    
    
    regex='class="resblock".+?href="(.+?)".+?title="(.+?)".+?<.+?class="for.+?">(.+?)<.+?div class="sourcetitle(.+?)/div>\n</div>'
    #regex='onclick="window.location.href=\'(.+?)\'<a title="(.+?)".+?<a title=.+?>(.+?)<.+?<div class="tagged">(.+?)<'
    match_a=re.compile(regex,re.DOTALL).findall(html)

    video_data={}
    regex='href="(.+?)" rel=\'next\'>Next'
    match=re.compile(regex).findall(html)

    next_p_all=match
    return match_a,next_p_all
    
def get_strgo(url,original_url):
    url=domain_s+'streamgo.me/player/'+url
    
    headers = {
        'Host': 'streamgo.me',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': original_url,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    x=requests.get(url, headers=headers).content
    regex='sources.+?"file":"(.+?)"'
    match=re.compile(regex).findall(x)

    headers = {
    'Host': 'mango.fruity.pw',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept': '*/*',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': url,
    'Origin': domain_s+'streamgo.me',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }
    head=urllib.urlencode(headers)
    
    link=match[0]+"|"+head
    regex='<title>(.+?)</title>'
    match=re.compile(regex).findall(x)
    return link,match[0]

def get_hdonline_old(tv_movie,original_title,season_n,episode_n,season,episode,year):
    global link_hdonline,pr_ho,stop_all
    all_links=[]
    if tv_movie=='movie':
        x=requests.get(domain_s+'hdonline.eu/search-query/%s+%s/'%(original_title.replace('%20','+'),year)).content
       
        regex='<li class="movie-item" data-hasqtip=.+?<a href="(.+?)" title="(.+?)"'
        match=re.compile(regex,re.DOTALL).findall(x)
        zz=0
        for link,name in match:
          if stop_all==1:
            break
          pr_ho=(zz*100)/len(match)
          zz=zz+1
          y=requests.get(link).content
     
          regex2='data-openload="(.+?)"'
          match2=re.compile(regex2).findall(y)
          
          regex3='data-strgo="(.+?)"'
          match3=re.compile(regex3).findall(y)
          
          regex_q='Quality: <span class="badge">(.+?)<'
          match_q=re.compile(regex_q).findall(y)
          if len(match2)>0:
            name1,match_s,res,check=server_data(domain_s+'openload.co/embed/'+match2[0],original_title)
 
            if check:
              if res==' ':
                 res=match_q[0]
              all_links.append((name1.replace("%20"," "),domain_s+'openload.co/embed/'+match2[0],'Vimuoo',res))
          if len(match3)>0 and '.srt' not in match3[0] :
            link2,name2=get_strgo(match3[0],link)
            all_links.append((name2.replace("%20"," "),link2,'-VIP-',match_q[0]))
          link_hdonline=all_links
    else:
        x=requests.get(domain_s+'hdonline.eu/search-query/%s/'%(original_title.replace('%20','+')+'+S'+season_n)).content
     
        regex='<li class="movie-item" data-hasqtip=.+?<a href="(.+?)" title="(.+?)"'
        match=re.compile(regex,re.DOTALL).findall(x)
        zz=0
        for link,name in match:
          if stop_all==1:
            break
          pr_ho=(zz*100)/len(match)
          zz=zz+1
          y=requests.get(link).content
          regex_q='Quality: <span class="badge">(.+?)<'
          match_q=re.compile(regex_q).findall(y)
          regex_pre='<li class="ep-item " id="episode-(.+?)</li>'
          match_pre=re.compile(regex_pre,re.DOTALL).findall(y)
          
          for epis_data in match_pre:
              if stop_all==1:
                 break
              regex2='data-openload="(.+?)">\n<div class="sli-name"><a href="javascript:.+?" title="Episode (.+?):'
              
              match2=re.compile(regex2).findall(epis_data)
     
              
              for link_in,ep in match2:
                 if stop_all==1:
                      break
                 if episode_n==ep:
                     name1,match_s,res,check=server_data(domain_s+'openload.co/embed/'+link_in,original_title)
 
                     if check:
                      if res==' ':
                        res=match_q[0]
                      all_links.append((name1.replace("%20"," "),domain_s+'openload.co/embed/'+link_in,'Vumoo',res))
              regex2='data-strgo="(.+?)">\n<div class="sli-name"><a href="javascript:.+?" title="Episode (.+?):'
              
              match2=re.compile(regex2).findall(epis_data)
     
              
              for link_in,ep in match2:
          
                 if episode_n==ep:
                      link2,name2=get_strgo(link_in,link)
                      all_links.append((name2.replace("%20"," "),link2,'-VIP-',match_q[0]))
              link_hdonline=all_links
    return all_links
def decode_link(code):
    import js2py_o

    code=code.decode('base64')
    code_d='FileID=(\'%s\').replace(/[a-zA-Z]/g,function(c){return String.fromCharCode((c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26)});'%code
   
    result=js2py_o.eval_js(code_d)
    #FileID=atob(FileID).replace(/[a-zA-Z]/g,function(c){return String.fromCharCode((c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26)});
    '''
    d_code=list(code)
    fileid=''
  
    for c in d_code:
      if not c.isdigit():
          c=ord(c)

          if (c <= ord("Z")):
            temp=90
          else:
            temp=122
   
          temp2=c + 13
          c=temp2

          if ((temp) >=temp2 ):
           c=c
          else:  
           c=c - 26

          fileid=fileid+chr(c)
      else:
        fileid=fileid+str(c)
    '''
    
    return domain_s+'openload.co/embed/'+result
def get_cooltvzion(tv_movie,original_title,season_n,episode_n,season,episode,year):
    global cooltvzion,pr_tv
    all_links=[]
    if tv_movie=='tv':
        headers = {
            'Host': 'www.cooltvzion.pro',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': '*/*',
            'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Referer': domain_s+'www.cooltvzion.pro/watch-tv-series-online/keyword-streamable/arrow-0/1',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = {'prefixText':original_title.replace("%20"," ").replace("%27","'"),'count':'100'}
        
        response,cook = cloudflare.request(domain_s+'www.cooltvzion.pro/WebServices/WebService.asmx/GetShowCompletionList?'+urllib.urlencode(data), headers=headers)

        regex='<string>(.+?)</string>'
        match=re.compile(regex).findall(response)
        #response=json.loads(match)
        res={'results':[]}
        
        for result in (match):
          info=(PTN.parse(json.loads(result)['First']))
     
          if original_title.replace("%27","'").replace("%20"," ").lower() in info['title'].lower():

            if tv_movie=='tv':
              
                res['results'].append(json.loads(result))
            else:
              if str(info['year'])==str(year):
                  res['results'].append(json.loads(result))
        if len(res['results'])>0:
            data = {'ShowID':res['results'][0]['Second']}
           
            y,cook=cloudflare.request(domain_s+'www.cooltvzion.pro/WebServices/WebService.asmx/GetUrl?'+urllib.urlencode(data), headers=headers)

            regex='<string xmlns=".+?">(.+?)</string>'
            match2=re.compile(regex,re.DOTALL).findall(y)
          

            z,cook=cloudflare.request(match2[0].replace(" ",""))
            
           
            regex='<a itemprop="url" href="(.+?)"'
            match=re.compile(regex).findall(z)
            zy=0
            for links in match:
              
                if tv_movie=='tv':
                  pr_tv=(zy*100)/len(match)
                  zy=zy+1
  
                  if 'season-%s-episode-%s-'%(str(season),str(episode)) in links:
                   
                     zz,cook=cloudflare.request(links)
                   
                     regex_in="var FileID = '(.+?)'"
                     match_in=re.compile(regex_in).findall(zz)
    
                     
                     f_link=decode_link(match_in[0])
                     name1,match_s,res,check=server_data(f_link,original_title)
                                
                     if check:
                          all_links.append((name1.replace("%20"," "),f_link,match_s,res))
                    
                          cooltvzion=all_links

    return all_links
def search_site(search_q,base_url):
    import requests

    headers = {
        'Host': 'www.startpage.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': domain_s+'www.startpage.com/do/search',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    data = [
      ('cmd', 'process_search'),
      ('language', 'english'),
      ('enginecount', '1'),
      ('pl', ''),
      ('abp', '-1'),
      ('hmb', '1'),
      ('ff', ''),
      ('theme', ''),
      ('flag_ac', '0'),
      ('cat', 'web'),
      ('ycc', '0'),
      ('t', 'air'),
      ('nj', '0'),
      ('query', '%s site:%s'%(search_q,(base_url))),
      ('pg', '0'),
    ]

    response = requests.post(domain_s+'www.startpage.com/do/search', headers=headers, data=data).content
    regex="<h3 class='clk'><a href='(.+?')'"
    match=re.compile(regex).findall(response)

    
    return match
def get_dl20(tv_movie,original_title,season_n,episode_n,season,episode,year):
        global link_dl20



        all_links=[]
        headers = {
            'Host': 'watchmoviestream.me',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': domain_s+'watchmoviestream.me/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        params = (
            ('s', original_title.replace('%20','+').replace(' ','+').replace('%3a',':').replace('%27','+')),
        )
        
        response = requests.get(domain_s+'watchmoviestream.me/', headers=headers, params=params).content
        regex='<div class="title"><a href="(.+?)">(.+?)<'
        match=re.compile(regex).findall(response)

        for link,name in match:
    
          if name.replace("&#8217;","'").lower()==original_title.lower().replace('%20',' ').replace('3a',':').replace('%27',"'"):
            yy=requests.get(link, headers=headers).content

            if tv_movie=='tv':
              regex='div class="numerando">%s - %s</div><div class="episodiotitle"><a href="(.+?)">'%(season,episode)
            
              match2=re.compile(regex).findall(yy)
              zz=requests.get(match2[0], headers=headers).content
            else:
              zz=yy
              
            regex='<iframe class=".+?" src="(.+?)"'
            match3=re.compile(regex).findall(zz)

            if len (match3)>0:
                xx=requests.get(match3[0]).content
                regex='"og:title" content="(.+?)"'
                match4=re.compile(regex).findall(xx)
                if len(match4)>0:
                      name1=match4[0]
                      try:
                          info=(PTN.parse(match4[0]))
                          
                          if 'resolution' in info:
                             res=info['resolution']
                          else:
                             if "HD" in match4[0]:
                              res="HD"
                             elif "720" in match4[0]:
                              res="720"
                             elif "1080" in match4[0]:
                               res="1080"
                             else:
                               res=' '
                      except:
                        res=' '
                        pass
                else: 
                    name1=original_title
                    res=' '
                regex_s="//(.+?)/"
                match_s=re.compile(regex_s).findall(match3[0])
                all_links.append((name1.replace("%20"," "),match3[0],match_s[0],res))
                  
                link_dl20=all_links
        return all_links
def get_dl20_old(tv_movie,original_title,season_n,episode_n,season,episode,year):

    global link_dl20,pr_dl
    
    base_url='http://dl20.mihanpix.com/'
    
    
  


    if tv_movie=='tv':
        search_q='%s.s%se%s'%(original_title,season_n,episode_n)
        
        #x=requests.get("https://www.google.co.il/search?source=hp&q="+search_q+"+site%3A"+urllib.quote_plus(base_url)).content
        #regex='q=%s(.+?)&'%base_url
        #match=re.compile(regex).findall(x)
        match=search_site(search_q,base_url)
        all_links=[]
        zz=0
        for mat in match:

          y=requests.get(base_url+mat).content
          regex=re.compile('<a href="(.+?)"')
          match_l=re.compile(regex).findall(y)
          
          for link in match_l:
           link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
           if len(link_t)>0:
               info=(PTN.parse(link_t))
               pr_dl=(zz*100)/(len(match_l)*len(match))
               zz=zz+1
               if 'resolution' in info:
                 res=info['resolution']
               else:
                 res=' '
               if info['title']==original_title and str(info['season'])==str(season) and str(info['episode'])==str(episode):
               
                  all_links.append((link.replace("%20"," "),base_url+mat+link,'DL20',res))
               link_dl20=all_links
    else:
        search_q=original_title
       
        #x=requests.get("https://www.google.co.il/search?source=hp&q="+search_q+"+site%3A"+urllib.quote_plus(base_url)).content
        #regex='q=%s(.+?)&'%base_url
        #match=re.compile(regex).findall(x)
        match=search_site(search_q,base_url)
        all_links=[]
        zz=0
        for mat in match:
         
          headers = {
                'Host': 'dl20.mihanpix.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
          }
          y=requests.get(base_url+mat,headers=headers).content
          regex=re.compile('<a href="(.+?)"')
          match_l=re.compile(regex).findall(y)

          for link in match_l:
           try:
               link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
               if len(link_t)>2 and link_t!=None:
          
                   info=(PTN.parse(link_t))
                   if 'season' not in info:
                       pr_dl=(zz*100)/(len(match_l)*len(match))
                       zz=zz+1
                       
                       if 'resolution' in info:
                         res=info['resolution']
                       else:
                         res=' '
                       if 'title' in info:
                           if info['title']==original_title.replace("%20"," "):
                             
                              if 'year' in info:
                                if str(info['year'])==str(year):
                                  all_links.append((link.replace("%20"," "),base_url+mat+link,'DL20',res))
                              else:
                                 all_links.append((link.replace("%20"," "),base_url+mat+link,'DL20',res))
                           link_dl20=all_links
           except:
            pass
    return all_links
def get_ava(tv_movie,original_title,season_n,episode_n,season,episode,year):
        global link_ava
        
        all_links=[]
        headers = {
            #'Host': 'putlockermovies.eu',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            #'Referer': 'putlockermovies.eu',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        response = requests.get('http://www.putlockers.lc/?s='+original_title.replace('%20','+').replace(' ','+').replace('%3a',':').replace('%27','+'), headers=headers).content
        regex='<div class="title">.+?<a href="(.+?)">(.+?)<'
        match=re.compile(regex,re.DOTALL).findall(response)
    
        for link,name in match:
  
          if  (original_title.lower().replace('%20',' ').replace('3a',':').replace('%27',"'")+' '+year) == name.replace("&#8217;","'").lower():

            
            
            if tv_movie=='tv':
              yy=requests.get(link+'?season='+season, headers=headers).content
            
              #regex='div class="numerando">%s - %s</div>.+?<div class="episodiotitle">.+?<a href="(.+?)">'%(season,episode)
              regex='Season %s Episode %s .+?"  href="(.+?)"'%(season,episode)
                    
              
              match2=re.compile(regex).findall(yy)
       
        
              zz=requests.get(match2[0]+'?watching', headers=headers).content
            else:
              yy=requests.get(link+'?watching', headers=headers).content
              zz=yy
     
            regex='class="metaframe rptss" src="(.+?)"'
            match3=re.compile(regex).findall(zz)
            
            '''
            xx=requests.get(domain_s+'putlockermovies.eu'+match3[0]).content
            regex='src="(.+?)"'
            match5=re.compile(regex).findall(xx)
            '''
            link=requests.get(match3[0])
            name1,match_s,res,check=server_data(link.url,original_title)
                        
            if check:
                  all_links.append((name1.replace("%20"," "),link.url,match_s,res))
                  link_ava=all_links
        return all_links
def get_ava_old(tv_movie,original_title,season_n,episode_n,season,episode,year):

    global link_ava,pr_sv
    base_url='http://avadl.uploadt.com/DL7/'
    if tv_movie=='tv':
        search_q='%s.s%se%s'%(original_title,season_n,episode_n)
        zz=0
        x=requests.get("https://www.google.co.il/search?source=hp&q="+search_q+"+site%3A"+urllib.quote_plus(base_url)).content
        regex='q=%s(.+?)&'%base_url
        match=re.compile(regex).findall(x)
        all_links=[]
        for mat in match:

          y=requests.get(base_url+mat).content
          regex=re.compile('<a href="(.+?)"')
          
          match_l=re.compile(regex).findall(y)
          
          
          for link in match_l:
           link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
           if len(link_t)>0:
               info=(PTN.parse(link_t))
               pr_sv=(zz*100)/(len(match_l)*len(match))
               zz=zz+1
               if 'title' in info and 'season' in info and 'episode' in info:
                   if 'resolution' in info:
                     res=info['resolution']
                   else:
                     res=' '
                   if info['title']==original_title and str(info['season'])==str(season) and str(info['episode'])==str(episode):
                   
                      all_links.append((link.replace("%20"," "),base_url+mat+link,'ava',res))
                   link_ava=all_links
    else:
        search_q=original_title
       
        x=requests.get("https://www.google.co.il/search?source=hp&q="+search_q+"+site%3A"+urllib.quote_plus(base_url)).content
        regex='q=%s(.+?)&'%base_url
        match=re.compile(regex).findall(x)
        all_links=[]
        zz=0
        for mat in match:
         
          y=requests.get(base_url+mat).content
          regex=re.compile('<a href="(.+?)"')
          match_l=re.compile(regex).findall(y)
          
          for link in match_l:
           link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
           if len(link_t)>2 and link_t!=None:
        
               info=(PTN.parse(link_t))
            
               if 'title' in info:
                   title=info['title']
                   if 'season' not in info:
                       pr_sv=(zz*100)/(len(match_l)*len(match))
                       zz=zz+1
                       if 'resolution' in info:
                         res=info['resolution']
                       else:
                         res=' '
                       
                       
                       if title==original_title.replace("%20"," "):
                        
                          if 'year' in info:
                            if str(info['year'])==str(year):
                              all_links.append((link.replace("%20"," "),base_url+mat+link,'ava',res))
                          else:
                             all_links.append((link.replace("%20"," "),base_url+mat+link,'ava',res))
                       link_ava=all_links
    return all_links
def get_tmp(tv_movie,original_title,season_n,episode_n,season,episode,year):
    global link_tmp,stop_all
    all_links=[]
    if tv_movie=='movie':
      headers = {
        'Host': 'watchfilms.me',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
      }   
      html=requests.get("https://watchfilms.me/all",headers=headers).content
      regex='<a href="(.+?)" title="(.+?)"'
      match=re.compile(regex).findall(html)
      for link,name in match:
        if stop_all==1:
          break
        if name.lower()==original_title.lower().replace('%20',' ').replace('3a',':'):
         yy=requests.get("https://watchfilms.me"+link,headers=headers).content
         regex='<li class="playlist_entr.+?" id="(.+?)"'
         match2=re.compile(regex).findall(yy)
         for id in match2:
            if stop_all==1:
               break
            data={'d':"embed",'id':id}

            response = requests.post(domain_s+'watchfilms.me/api', data=data).content
            regex='<a href="(.+?)"'
            match_l=re.compile(regex).findall(response)
            match_l[0]=match_l[0]#.replace("vidtodo.com","vidtudu.com")
            
           
            
            if 1:
                
                headers={#'Host': 'vidtudu.com',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'utf8',
                        'Referer': "https://watchfilms.me"+link,

                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1'}
            
                f_link=match_l[0]
                name1,match_s,res,check=server_data(f_link,original_title,direct='yes',c_head=headers)
             

                
                if check:
                 
                  if match_s=='vidtodo.com':
                    f_link=VidToDoResolver(f_link,c_head=headers)[1]
   
                  all_links.append((name1.replace("%20"," "),f_link,match_s,res))
                
                  link_tmp=all_links
    else:
              headers = {
                'Host': 'newepisodes.co',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
              }   
              html=requests.get("https://newepisodes.co/all",headers=headers).content
              regex='<a href="//newepisodes.co(.+?)">(.+?)<'
              match=re.compile(regex).findall(html)
              
              for link,name in match:
                if stop_all==1:
                    break
                if name.lower().strip()==original_title.lower().replace('%20',' ').replace('3a',':'):
   
                 yy=requests.get("https://newepisodes.co"+link,headers=headers).content
                 regex_pre='<div data-type="show" class="list-item  season_%s">(.+?)</a>'%season
                 match_pre=re.compile(regex_pre,re.DOTALL).findall(yy)
             
                 for data in match_pre:
                   
                  
                   regex_in='<a href="(.+?)".+?<span class="mini".+?S%sE%s	'%(season,episode)
                   match_in=re.compile(regex_in,re.DOTALL).findall(data)
                   if len(match_in)>0:
                    break
                   
            
                 yy=requests.get("https:"+match_in[0],headers=headers).content
                 
                 regex='<li class="playlist_entr.+?" id="(.+?)"'
                 match2=re.compile(regex).findall(yy)
                 for id in match2:
                    if stop_all==1:
                        break
                    data={'d':"embed",'id':id}

                    response = requests.post(domain_s+'newepisodes.co/api', data=data).content
                    regex='<a href="(.+?)"'
                    match_l=re.compile(regex).findall(response)
                    match_l[0]=match_l[0].replace("vidtodo.com","vidtod.me")
                    
                    
                    
                    if 1:
                   
                        
                        headers={#'Host': 'vidtudu.com',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                'Accept-Language': 'en-US,en;q=0.5',
                                'Accept-Encoding': 'utf8',
                                'Referer': "https://newepisodes.co"+link,

                                'Connection': 'keep-alive',
                                'Upgrade-Insecure-Requests': '1'}
                    
                        
                        name1,match_s,res,check=server_data(match_l[0],original_title,direct='yes',c_head=headers)

                        
                        if check:
                          if match_s=='vidtodo.com':
                                f_link=VidToDoResolver(f_link,c_head=headers)[1]
                               
                          all_links.append((name1.replace("%20"," "),match_l[0],match_s,res))
                       
                          link_tmp=all_links
    return all_links
def get_tmp_old(tv_movie,original_title,season_n,episode_n,season,episode,year):



    global link_tmp,pr_lv
    base_url='http://server1.timepassbd.com/ftpdata1/'
    if tv_movie=='tv':
        search_q='%s.s%se%s'%(original_title,season_n,episode_n)
       
        x=requests.get("https://www.google.co.il/search?source=hp&q="+search_q+"+site%3A"+urllib.quote_plus(base_url)).content
        regex='q=%s(.+?)&'%base_url
        match=re.compile(regex).findall(x)
        all_links=[]
        zz=0
        for mat in match:
          
          mat=urllib.unquote(mat).replace(" ",'%20')
          y=requests.get(base_url+mat).content
          regex=re.compile('<a href="(.+?)"')
          
          match_l=re.compile(regex).findall(y)
          
          
    
          for link in match_l:
           link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
           if len(link_t)>0:
               info=(PTN.parse(link_t))
             
               pr_lv=(zz*100)/(len(match_l)*len(match))
               zz=zz+1
               if 'title' in info and 'season' in info and 'episode' in info:
                   if 'resolution' in info:
                     res=info['resolution']
                   else:
                     res=' '
                   if info['title']==original_title and str(info['season'])==str(season) and str(info['episode'])==str(episode):
                      
                      all_links.append((link.replace("%20"," "),base_url+mat+link,'tmp',res))
                      link_tmp=all_links
    else:
        search_q=original_title
       
        x=requests.get("https://www.google.co.il/search?source=hp&q="+search_q+"+site%3A"+urllib.quote_plus(base_url)).content
        regex='q=%s(.+?)&'%base_url
        match=re.compile(regex).findall(x)
        zz=0
        all_links=[]
       
        
        for mat in match:
       
          mat= urllib.unquote(mat).replace(" ",'%20')
          y=requests.get(base_url+mat).content
          regex=re.compile('<a href="(.+?)"')
          match_l=re.compile(regex).findall(y)
     
          
          for link in match_l:
           link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
           if len(link_t)>2 and link_t!=None:           
               info=(PTN.parse(link_t))
               if 'title' in info:
                   title=info['title']
                   
                   if 'season' not in info:
                       pr_lv=(zz*100)/(len(match_l)*len(match))
                       zz=zz+1
                       if 'resolution' in info:
                         res=info['resolution']
                       else:
                         res=' '
                       
                       if title==original_title.replace("%20"," "):
                         
                          if 'year' in info:
                            year_in=info['year']
                            if str(year_in)==str(year):
                              all_links.append((link.replace("%20"," "),base_url+mat+link,'tmp',res))
                          else:
                             all_links.append((link.replace("%20"," "),base_url+mat+link,'tmp',res))
                          link_tmp=all_links
    
    return all_links
def get_putvid(url):
    z=requests.get(url).content

    regex="return p.+?'(.+?)'\.split"
    str_new=re.compile(regex).findall(z)[0]
    pre=''
    x=0
    for ch in str_new:
       if ch=="'" and pre!='\\':
         loc=x
         break
       else:
        pre=ch
        x=x+1
    p=(str_new[0:x])
    rest=(str_new.replace(p,""))
    a=int(rest.split(',')[1])
    c=int(rest.split(',')[2])-1
    k=rest.split(',')[3].split('|')
    p=p.replace('\\','')


    while (c>0):
        
        if (k[c]):
          temp=(base_convert(c,a))
          p=re.sub("\\b"+(base_convert(c,a))+"\\b", k[c], p)
          
        c=c-1
    regex='http(.+?)"'
    match=re.compile(regex).findall(p)
 
    return 'http'+match[0]
def get_goo(tv_movie,original_title,season_n,episode_n,season,episode,year):
    global link_goo
    if tv_movie=="tv":
    
       name_search=original_title.lower().replace(" ","-").replace("%20","-").replace("%3a","").replace("%27","-")+"/"+season_n+"-"+episode_n
       htm=requests.get("http://gomostream.com/show/"+name_search).content
    else:
       name_search=original_title.lower().replace(" ","-").replace("%20","-").replace("%3a","").replace("%27","-")
       htm=requests.get("http://gomostream.com/movie/"+name_search).content

    regex="var tc = '(.+?)'"
    match2=re.compile(regex,re.DOTALL).findall(htm)
    regex='function _tsd_tsd_ds(.+?)</script>'
    match=re.compile(regex).findall(htm)
    jscode="var s = '%s';tc=_tsd_tsd_ds(s);"%match2[0]+'function _tsd_tsd_ds'+match[0]



    result=js2py.eval_js(jscode)

    regex='"_token": "(.+?)"'
    match3=re.compile(regex).findall(htm)

    headers= { 'x-token': result}
    data= {
      'tokenCode': match2[0],
      "_token": match3[0],
    }
    
    x=requests.post("https://gomostream.com/decoding_v3.php",headers=headers,data=data).json()
    
    all_links=[]

    for link in x:
    
    
      if 'putvid' in link:
        link=get_putvid(link)
        all_links.append((original_title.replace("%20"," "),link,"PUTVID","1080"))
          
        link_goo=all_links
      elif 'vidushare.com' not in link and len(link)>5:#try:
          html2=requests.get(link).content
          regex='"og:title" content="(.+?)"'
          match=re.compile(regex).findall(html2)
          if len(match)>0:
              name1=match[0]
              info=(PTN.parse(match[0]))
              
              if 'resolution' in info:
                 res=info['resolution']
              else:
                 if "HD" in match[0]:
                  res="HD"
                 elif "720" in match[0]:
                  res="720"
                 elif "1080" in match[0]:
                   res="1080"
                 else:
                   res=' '
          else: 
            name1=original_title
            res=' '
          regex_s="//(.+?)/"
          match_s=re.compile(regex_s).findall(link)
          all_links.append((name1.replace("%20"," "),link,match_s[0],res))
          
          link_goo=all_links
 
    
    
    return all_links
def get_1movie_old(tv_movie,original_title,season_n,episode_n,season,episode,year):
        global links_1movie
        
        if tv_movie=='tv':
            search_string='http://search.1movies.im/?q='+(original_title+"%20season%20"+season)
            z=requests.get(search_string).content
            
            regex='<a class="thumb" href="(.+?)"'
            match=re.compile(regex).findall(z)
            
            y=requests.get('http:'+match[0]).content
            
            regex_ep='<a href="(.+?)" class="">Episode (.+?)<'
            match_ep=re.compile(regex_ep).findall(y)
            for link,ep in match_ep:
              if ep==episode:
                o_link=link
                y=requests.get(link).content
                break
        
        
        
        regex='load_player\((.+?)\)'
        match=re.compile(regex).findall(y)
        x=requests.get("http://1movies.im/ajax/movie/load_player_v3?id="+match[0]).json()


        headers = {
            'Host': 'xplay.1movies.im',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'http:'+match[0],
            'Origin': 'http://1movies.im',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        params = (
            ('k', 'c2d47c576561ac70ccad3750edee8477'),
            ('li', '0'),
            ('tham', '1519741483'),
            ('lt', 'os'),
            ('st', 'b025550974ae4e50db6dfc21bc04c482'),
            ('qlt', '720p'),
            ('spq', 'p'),
            ('prv', ''),
            ('key', '93c26993ad479f0e305fdbc7d6bb4ee3'),
            ('h', '1519741483'),
            #('_', '1519742825829'),
        )


         
        response = requests.get('http:'+x['value'], headers=headers).json()
        regex_n='slug: "(.+?)"'
        match_n=re.compile(regex_n).findall(y)
 
        all_links=[]
        for link in response['playlist']:
          f_link=link['file']
          if "1080" in o_link:
            res="1080"
          elif "720" in o_link:
            res="720"
          elif "480" in o_link:
            res="720"
          elif "hd" in o_link.lower():
            res="HD"
          else:
           res=' '
          
          headers = {
                'Host': 's5.6krnpl.men',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
          }
          head=urllib.urlencode(headers)
          f_link=f_link+"|"+head
          all_links.append((match_n[0].replace("%20"," "),f_link,"1Movie",res))
          links_1movie=all_links
        return all_links
def get_sc(tv_movie,original_title,name,season_n,episode_n,season,episode,year):
        #search is down need to check later.... :-((((
        
        global links_sc,stop_all
        all_links=[]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.gowatchfreemovies.to',
            'Referer': domain_s+'www.gowatchfreemovies.to/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
        if tv_movie=='tv':
          type="2"
        else:
          type="1"
        params = (
            ('keyword', original_title.replace("%20","+").replace(" ","+")),
            ('search_section', type),
        )
        data = {
            'keyword': original_title.replace("%20","+").replace(" ","+"),
            'search_section': type,
        }
        
        response = requests.get(domain_s+'www.gowatchfreemovies.to/?keyword=%s&search_section=1'%original_title.replace("%20","+").replace(" ","+"), headers=headers).content
        regex='<div class="item"><a href="(.+?)" title="(.+?)"'
        match=re.compile(regex).findall(response)
       
        for link,name in match:
          if stop_all==1:
            break
  
          if original_title.replace("%20"," ").replace("%27","'").lower() in name.lower() and year in  name.lower():
            if tv_movie=='tv':
              link=link.replace('watch','tv')+'/season-%s-episode-%s'%(season,episode)
         
            
            yy=requests.get(domain_s+'www.gowatchfreemovies.to'+link,headers=headers).content
            regex='gtfo=(.+?)&'
            match2=re.compile(regex).findall(yy)
            for links2 in match2:
              try:
                if stop_all==1:
                  break
                f_link=links2.decode('base64')
        
                nam1,srv,res,check=server_data(f_link,original_title)
              
                if check:
                  all_links.append((nam1.replace("%20"," "),src,srv,res))
                  
                  links_sc=all_links
              except:
               pass
        return all_links
def get_sc_old(tv_movie,original_title,name,season_n,episode_n,season,episode,year):
      global links_sc
        
      all_links=[]
      link2=''
      if tv_movie=='tv':
          if season!='1':
           url='http://www.seret.club/'+original_title+'-%d7%a2%d7%95%d7%a0%d7%94-'+season+'-%d7%a4%d7%a8%d7%a7-'+episode
          else:
            url='http://www.seret.club/'+original_title+'-%d7%a4%d7%a8%d7%a7-'+episode
      else:
           url='http://www.seret.club/'+name.replace('%20','-').replace(' ','-')
      
      html=requests.get(url).content
      regex_n='"og:title" content="(.+?)"'
      match_n=re.compile(regex_n).findall(html)
      regex='<iframe.+?src="(.+?)"'
      match_pre=re.compile(regex,re.IGNORECASE).findall(html)

      try:
        link=(match_pre[0])
      except:
       link=' '

      if 'recaptcha' in link or len(match_pre)==0 or 'לצפייה בטלפון נייד לחצו כאן' in html:
         regex='href="(.+?)".+?לצפייה בטלפון נייד לחצו כאן'
         match=re.compile(regex).findall(html)
         if len (match)>0:
           link2=match[0]
         
     
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
         
          links=googledrive_resolve(id)
          
          for li,que in links:
           
           all_links.append((match_n[0],li,'-Gdrive-',que))
           links_sc=all_links
          
      else:

         link=match_pre[0]


      regex_s="//(.+?)/"
      match_s=re.compile(regex_s).findall(link)
      if len (match_s)>0 and len (match_s)>0:
        all_links.append((match_n[0],link,match_s[0],' '))
      if link2!='':
             regex_s="//(.+?)/"
             match_s=re.compile(regex_s).findall(link2)
             all_links.append((match_n[0],link2,match_s[0],' '))
      links_sc=all_links
      return links_sc
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
        urls = re.sub('\&url\='+ domain_s+'', '\@', urls)

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
                        mediaURLs.append( mediaurl.mediaurl(domain_s+'' + videoURL, itagDB[itag]['resolution'] + ' - ' + containerDB[container] + ' - ' + itagDB[itag]['codec'], str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
                    except KeyError:
                        mediaURLs.append(mediaurl.mediaurl(domain_s+''+ videoURL, itagDB[itag]['resolution'] + ' - ' + container, str(itagDB[itag]['resolution'])+ '_' + str(order+count), order+count, title=title))
        
        return mediaURLs,value
def googledrive_resolve(id):


    #html,cookie=read_site_html(domain_s+'drive.google.com/file/d/'+id+'/view')
    #regex='"fmt_stream_map".+?http(.+?)"'
    #match=re.compile(regex).findall(html)
    #link=('http'+match[0]).decode('unicode_escape')
    links_data,cookie=getPublicStream(domain_s+'drive.google.com/file/d/'+id+'/view')

    mediaURLs = sorted(links_data)
    options = []
 

    
    #ret = xbmcgui.Dialog().select("בחר איכות", options)
    final_link=[]
    que=[]
    for links in mediaURLs:
      playbackURL = links.url
   

      final_link.append((playbackURL+'||Cookie=DRIVE_STREAM%3D'+cookie,links.qualityDesc))
    
  
    return final_link
def get_seretil(tv_movie,original_title,name,season_n,episode_n,season,episode,year):
    global links_seil

    if tv_movie=='movie':
        all_links=[]
        headers = {
            'Host': 'www.sratim-il.ga',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
            #'Referer': domain_s+'www.sratim-il.ga/sratim/2018/03/03/%D7%94%D7%A6%D7%9C%D7%A6%D7%95%D7%9C-3/',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = [
          ('action', 'ajaxsearchlite_search'),
          ('aslp', name),
          ('asid', '1'),
          ('options', 'qtranslate_lang=0&set_exactonly=checked&set_intitle=None&set_inposts=None&categoryset%5B%5D=4&categoryset%5B%5D=5&categoryset%5B%5D=7&categoryset%5B%5D=383&categoryset%5B%5D=8&categoryset%5B%5D=9&categoryset%5B%5D=620&categoryset%5B%5D=11&categoryset%5B%5D=580&categoryset%5B%5D=12&categoryset%5B%5D=13&categoryset%5B%5D=565&categoryset%5B%5D=14&categoryset%5B%5D=15&categoryset%5B%5D=583&categoryset%5B%5D=6&categoryset%5B%5D=18&categoryset%5B%5D=19&categoryset%5B%5D=20'),
        ]
     
        response = requests.post('http://www.sratim-il.ga/sratim/wp-admin/admin-ajax.php', headers=headers,  data=data).content
        regex='"asl_res_url" href=\'(.+?)\''
        

        match=re.compile(regex).findall(response)

        
        if len(match)>0:
            html=requests.get(match[0]).content

            regex='svq_playlist_data.push\((.+?)\)'
            match=re.compile(regex).findall(html)
            if len (match)==0:
              regex='<source type="video/mp4" src="(.+?)"'
              match=re.compile(regex).findall(html)
              regex_t='/(.+?).mp4'
              match_t=re.compile(regex_t).findall(match[0])
              headers={'Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                    'Accept-Language':'en-US,en;q=0.5',
                    'Cache-Control':'no-cache',
                    'Connection':'keep-alive',
                    'Host':'server2.sratim-il.com',
                    'Pragma':'no-cache',

                    'Referer':'http://www.sratim-il.cf/newsite/%s/'%match_t[0],
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/59.0'}
              head=urllib.urlencode(headers)

              all_links.append((name.decode('utf8') + ' תרגום מובנה'.decode('utf8'),match[0]+"|"+head,'SERETIL','1080'))
              links_seil=all_links
            else:
                for m in json.loads(match[0]):
                  
                  for data in m['svq_video']:
              
                    regex_t='/(.+?).mp4'
                    match_t=re.compile(regex_t).findall(data['svq_url'])
                    headers={'Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                            'Accept-Language':'en-US,en;q=0.5',
                            'Cache-Control':'no-cache',
                            'Connection':'keep-alive',
                            'Host':'server2.sratim-il.com',
                            'Pragma':'no-cache',

                            'Referer':'http://www.sratim-il.cf/newsite/%s/'%match_t[0],
                            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/59.0'}
                    head=urllib.urlencode(headers)

                    all_links.append((name + ' תרגום מובנה',data['svq_url']+"|"+head,'SERETIL',data['svq_label']))
                    links_seil=all_links
        
    return links_seil
def get_flix(tv_mode,original_title,name,season_n,episode_n,season,episode,year_w):
        global links_flix
        title=original_title
       
        base_url=domain_s+'flixanity.mobi'
        headers = {
            'Host': 'api.flixanity.mobi',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': domain_s+'flixanity.mobi/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': domain_s+'flixanity.mobi',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = [
          ('q', title),
          ('limit', '100'),
          ('timestamp', '1520344292692'),
          ('verifiedCheck', 'eCNBuxFGpRmFlWjUJjmjguCJI'),
          ('set', 'ISWUIMkRkmWaoQrxnoiRrviDs'),#random
          ('rt', 'rPAOhkSTcEzSyJwHWwzwthPWVVFJHVZxExzJnbDekabvEeivQf'),
          ('sl', '9fc895fbb0b23f1c0fb8e5a5fe02f7b5'),
        ]
        '''
        example:
        rt:"rPAOhkSTcEzSyJwHWwzwthPWVHnTwUIKOugeuRCoozUooDLkQn"
        set:"UaGjHVXBhtrhEPbbmHbbQYxDa"
        sl:"9fc895fbb0b23f1c0fb8e5a5fe02f7b5"
        verifiedCheck:"eCNBuxFGpRmFlWjUJjmjguCJI"


        https://flixanity.mobi/templates/FliXanity/assets/scripts/plugins/foxycomplete.js?version=2.471518469393:formatted
        set:
              function l() {
                        for (var t = "", e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", r = 0; 25 > r; r++)
                            t += e.charAt(Math.floor(Math.random() * e.length))
                        return t
                        
        SShRpZKNDxeaxrhlMqUupRrsg

        rt:


            String.prototype.rflix = function(set) {
                var curr = token ,rfl = curr+set.toString();
                return flix(rfl);
                
            function flix(ain){
                return ain.replace(/[a-zA-Z]/g, function(c){
                    return String.fromCharCode((c <= "Z" ? 90 : 122) >= (c = c.charCodeAt(0) + 13) ? c : c - 26);
                });
        sl:
        input=evokjaqbb3
        return md5(enc('0A6ru35yyi5yn4THYpJqy0X82tE95bta')+input);
        function enc (data) {
            var b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
            var o1, o2, o3, h1, h2, h3, h4, bits, i = 0,
                ac = 0,
                enc = "",
                tmp_arr = [];

            if (!data) {
                return data;
            }


            do { // pack three octets into four hexets
                o1 = data.charCodeAt(i++);
                o2 = data.charCodeAt(i++);
                o3 = data.charCodeAt(i++);

                bits = o1 << 16 | o2 << 8 | o3;

                h1 = bits >> 18 & 0x3f;
                h2 = bits >> 12 & 0x3f;
                h3 = bits >> 6 & 0x3f;
                h4 = bits & 0x3f;

                // use hexets to index into b64, and append result to encoded string
                tmp_arr[ac++] = b64.charAt(h1) + b64.charAt(h2) + b64.charAt(h3) + b64.charAt(h4);
            } while (i < data.length);

            enc = tmp_arr.join('');

            var r = data.length % 3;

            return (r ? enc.slice(0, r - 3) : enc) + '==='.slice(r || 3);
        }
        '''
        #response = requests.post(domain_s+'api.flixanity.mobi/api/v1/0A6ru35yevokjaqbb3', headers=headers, data=data).json()


        #for items in response:
          #if 'TV Show' in items['meta']:
              
              #type=items['meta'].split('|')[0].strip()
              #year=items['meta'].split('|')[1].strip()
              
              
                #if title.lower()==items['title'].lower() and type=='TV Show' and year==year_w:
                #link=base_url+items['permalink'].replace('show','tv-show')+'/season/'+season+'/episode/'+episode
        if tv_mode=='tv':
          link=domain_s+'flixanity.mobi/tv-show/%s/season/%s/episode/%s'%(title.lower().replace('%20','-').replace('%3a','').replace(' ','-'),season,episode)
         
          action='getEpisodeEmb'
        else:
          link=domain_s+'flixanity.mobi/movie/%s/'%title.lower().replace('%20','-').replace(' ','-')
          action='getMovieEmb'
      
        x=requests.get(link).content
        if "var tok    = '" not in x :
          if tv_mode=='tv':
            link=domain_s+'flixanity.mobi/tv-show/%s-%s/season/%s/episode/%s'%(title.lower().replace('%20','-').replace('%3a','').replace(' ','-'),year_w,season,episode)
            x=requests.get(link).content
          else:
            link=domain_s+'flixanity.mobi/movie/%s-%s/'%(title.lower().replace('%20','-').replace(' ','-'),year_w)
            x=requests.get(link).content
       
        token=re.findall("var tok    = '(.+?)'",x)[0]
        lid=re.findall('elid = "(.+?)"',x)[0]


        import base64
        elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

        headers = {
            'Host': 'flixanity.mobi',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': link,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer false',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = [
          ('action', action),
          ('idEl', lid),
          ('token', token),
          ('nopop', ''),
          ('elid',elid),
        ]

        response2 = requests.post(domain_s+'flixanity.mobi/ajax/gonlflhyad.php', headers=headers, data=data).json()

        all_links=[]
        for links in response2:
          
          server=response2[links]['type']

          regex='SRC="(.+?)"'
          match=re.compile(regex,re.IGNORECASE).findall(response2[links]['embed'])
          
          src=match[0]
          if 'openload.co' in server or 'streamango' in server:
              yy=requests.get(src).content
              regex='og:title" content="(.+?)"'
              match_n=re.compile(regex).findall(yy)
              regex_l='//(.+?)/'
              match_l=re.compile(regex_l).findall(src)
              srv=match_l[0]
              if len(match_n)>0:
                  info=(PTN.parse(match_n[0]))
                  nam1=match_n[0].replace('%20',' ')
                  if 'resolution' in info:
                      res=info['resolution']
                  else:
                      res=' '
              else:
                 nam1=original_title.replace('%20',' ')
                 res=' '
          else:
            if '1080' in server:
              res='1080'
            elif '720' in server:
              res='720'
            elif '480' in server:
              res='480'
            elif '360' in server:
              res='360'
            else:
              res='HD'
            nam1=original_title.replace('%20',' ')
            srv=server
          all_links.append((nam1,src,srv,res))
          links_flix=all_links
        return links_flix
def get_put(tv_movie,original_title,name,season_n,episode_n,season,episode,year):
    global links_put,stop_all
    all_links=[]
    
    url2='http://www.omdbapi.com/?apikey=8e4dcdac&t=%s&year=%s'%(original_title,year)



    imdb_id="0"
    try:
       imdb_id=requests.get(url2).json()['imdbID']
    except:
      pass
  


    headers = {
        #'Host': 'putlocker.ninja',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        #'Referer': domain_s+'putlocker.ninja/tv-show/watch-the-flash-2014-season-4-episode-13-online-free.html',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }


    if tv_movie=='movie':
        response = requests.get(domain_s+'putlocker.ninja/embed/'+imdb_id+'/', headers=headers).content
    else:
       response = requests.get(domain_s+'putlocker.ninja/embed/'+imdb_id+'/'+season+'-'+episode+'/', headers=headers).content

    regex='<iframe src="(.+?)"'
    match=re.compile(regex).findall(response)
    for links in match:
        if stop_all==1:
            break
        yy=requests.get(links).content
        regex='og:title" content="(.+?)"'
        match=re.compile(regex).findall(yy)
        regex_l='//(.+?)/'
        match_l=re.compile(regex_l).findall(links)
        info=(PTN.parse(match[0]))
        if 'resolution' in info:
          res=info['resolution']
        else:
          res=' '
        all_links.append((match[0],links,match_l[0],res))
        links_put=all_links
    return links_put
def resolve_flix(link,action,season,episode):
        global link_hdonline,stop_all
        all_links=[]
        x=requests.get(link).content
        
        if action=='getEpisodeEmb':
          regex='<a href="(.+?)" class="season.+?>%s</'%season
          match=re.compile(regex).findall(x)
        
          
          x=requests.get(match[0]).content
          
          regex='<h5 class="episode-title"><a href="(.+?)episode/%s"'%episode
          match=re.compile(regex).findall(x)
          
          link=match[0]+'episode/'+episode
          x=requests.get(match[0]+'episode/'+episode).content
        token=re.findall("var tok    = '(.+?)'",x)[0]
        lid=re.findall('elid = "(.+?)"',x)[0]


        import base64
        elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())

        headers = {
            'Host': 'flixanity.mobi',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': link,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Authorization': 'Bearer false',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        data = [
          ('action', action),
          ('idEl', lid),
          ('token', token),
          ('nopop', ''),
          ('elid',elid),
        ]

        response2 = requests.post(domain_s+'flixanity.mobi/ajax/gonlflhyad.php', headers=headers, data=data).json()

        all_links=[]

        for links in response2:
          if stop_all==1:
            break
          server=response2[links]['type']

          regex='SRC="(.+?)"'
          match=re.compile(regex,re.IGNORECASE).findall(response2[links]['embed'])
          
          src=match[0]
        
          if 'openload.co' in server or 'streamango' in server:
              
              
              nam1,srv,res,check=server_data(src,original_title)
              
              if check:
                all_links.append((nam1.replace("%20"," "),src,srv,res))
          else:
            if '1080' in server:
              res='1080'
            elif '720' in server:
              res='720'
            elif '480' in server:
              res='480'
            elif '360' in server:
              res='360'
            else:
              res='HD'
            nam1=original_title.replace('%20',' ')
            srv=server
            all_links.append((nam1,src,srv,res))
            link_hdonline=all_links
        return all_links
def resolve_hdo(url,action,season,episode,original_title):
    global link_hdonline,stop_all
    ids=url.split('-')
    id=ids[len(ids)-1]
    all_links=[]
    url=domain_s+'hdonline.is/ajax/movie/episodes/'+id
    x=requests.get(url).content
    x=x.replace("\\","")
    if action=='getEpisodeEmb':
      regex_pre='<li class="ep-item"(.+?)</li'
      match=re.compile(regex_pre).findall(x)
      x=''
      for ep in match:
        if 'Episode '+episode in ep:
          x=x+' '+ep
          
      regex='data-server=".+?" data-id="(.+?)"'
    else:
      regex='data-server=".+?" data-id="(.+?)"'
    
    match=re.compile(regex).findall(x)
    
    for eid in match:
      if stop_all==1:
            break
      url=domain_s+'hdonline.is/ajax/movie/get_embed/'+eid
      x=requests.get(url).json()

      if x['status']==True:
        name1,match_s,res,check=server_data(x['src'],original_title)
        
        if check:
          all_links.append((name1.replace("%20"," "),x['src'],match_s,res))
      
      url=domain_s+'hdo.to/ajax/movie/token?eid=%s&mid=%s'%(eid,id)
      
      x=requests.get(url).content
      regex="_x='(.+?)', _y='(.+?)'"
      match=re.compile(regex).findall(x)
      for x,y in match:
        if stop_all==1:
            break
        url=domain_s+'hdonline.is/ajax/movie/get_sources/%s?x=%s&y=%s'%(eid,x,y)
        
        x=requests.get(url).content
        if len(x)>5:
         x=json.loads(x)
         if 'playlist' in x:
             for item in  x['playlist'][0]['sources']:
                   if stop_all==1:
                    break
                  
                   if 'file' in x['playlist'][0]['tracks'][0]:
                      nam1_a=x['playlist'][0]['tracks'][0]['file'].split('/')
                      nam1=nam1_a[len(nam1_a)-1].replace('.srt','')
                      if '1080' in nam1:
                          res='1080'
                      elif '720' in nam1:
                          res='720'
                      elif '480' in nam1:
                          res='480'
                      elif '360' in nam1:
                          res='360'
                      else:
                          res='HD'
                      all_links.append((nam1.replace("%20"," "),item['file'],'VIP',res))
         else:
           if 'src' in x:
            name1,match_s,res,check=server_data(x['src'],original_title)
      
            if check:
              all_links.append((name1.replace("%20"," "),x['src'],match_s,res))
              link_hdonline=all_links
    return all_links


def get_hdonline(tv_mode,original_title,season_n,episode_n,season,episode,year_w):
                
        global link_hdonline,stop_all
        title=original_title

        if tv_mode=='movie':
           
         
          
       
          action='getMovieEmb'
          url='http://212.227.203.133/api_v2/code/main/movie_search_all_servers_v2.php?server=hdo_movies&q=%s&year=%s'%(original_title.lower().replace('%20','+').replace('%3a','').replace(' ','+'),year_w)
        else:
          action='getEpisodeEmb'
          url='http://212.227.203.133/api_v2/code/main/movie_search_all_servers_series_v2.php?server=is_series&q=%s&season=%s'%(original_title.lower().replace('%20','+').replace('%3a','').replace(' ','+'),season)
        headers={'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; S16 Build/NRD90M)',
                'Host': '212.227.203.133',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'utf8'}

        x=requests.get(url,headers=headers).json()
        
        links=[]
        links2=[]
        for item in x:
          if stop_all==1:
            break
          if action=='getEpisodeEmb' and 'flixanity' not in item['url']:
            year_w=item['title_with_year']
          if  clean_name(original_title,1) in item['title_with_year'] and year_w in item['title_with_year']:
             
             if 'flixanity' in item['url']:
               links=resolve_flix(item['url'],action,season,episode)
             
             if 'hdo.' in item['url']:
       
               links2=resolve_hdo(item['url'],action,season,episode_n,original_title)

        mergedlist = []
        mergedlist.extend(links)
        mergedlist.extend(links2)
        link_hdonline=mergedlist
        return link_hdonline
def get_put(tv_movie,original_title,name,season_n,episode_n,season,episode,year):
    global links_put
    all_links=[]
    
    url2='http://www.omdbapi.com/?apikey=8e4dcdac&t=%s&year=%s'%(original_title,year)



    imdb_id="0"
    try:
       imdb_id=requests.get(url2).json()['imdbID']
    except:
      pass
  


    headers = {
        'Host': 'putlocker.ninja',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        #'Referer': domain_s+'putlocker.ninja/tv-show/watch-the-flash-2014-season-4-episode-13-online-free.html',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }


    if tv_movie=='movie':
        response = requests.get(domain_s+'putlocker.ninja/embed/'+imdb_id+'/', headers=headers).content
    else:
       response = requests.get(domain_s+'putlocker.ninja/embed/'+imdb_id+'/'+season+'-'+episode+'/', headers=headers).content
    regex='<iframe src="(.+?)"'
    match=re.compile(regex).findall(response)
    for links in match:
        yy=requests.get(links).content
        regex='og:title" content="(.+?)"'
        match=re.compile(regex).findall(yy)
        regex_l='//(.+?)/'
        match_l=re.compile(regex_l).findall(links)
        if len(match)>0:
            if len(match[0])>0:
                nam1=match[0]
                try:
                  info=(PTN.parse(match[0]))
                except:
                  info={}
                if 'resolution' in info:
                  res=info['resolution']
                else:
                  res=' '
            else:
             nam1=original_title.replace('%20',' ')
             res=' '
        else:
             nam1=original_title.replace('%20',' ')
             res=' '
        all_links.append((nam1,links,match_l[0],res))
        links_put=all_links
    return links_put
def get_cin(tv_mode,original_title,name,season_n,episode_n,season,episode,year_w):
        global link_cin,stop_all
         
        title=urllib.unquote_plus(original_title)
        all_links=[]
        headers = {
            'Host': 'dwatchseries.to',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': domain_s+'dwatchseries.to/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        if tv_mode=='tv':
            html = requests.get(domain_s+'dwatchseries.to/search/%s'%urllib.quote_plus(title), headers=headers).content
  
            regex='<a href="(.+?)" title="(.+?)" target="_blank"><strong>'
            match=re.compile(regex).findall(html)

      
            for link,name in match:
              if stop_all==1:
                break
              precent=similar(list(name.lower()),list(title.lower()))
          
              if int(precent)>90:
         
                yy=requests.get(link, headers=headers).content
                regex_p='span itemprop="name">Season %s</span>(.+?)</ul>'%season
                match_p=re.compile(regex_p,re.DOTALL).findall(yy)
        

                for item in match_p:
                  if stop_all==1:
                    break
                  regex='itemprop="episode".+?"episodenumber" content="%s".+?content="(.+?)"'%episode
                  match2=re.compile(regex,re.DOTALL).findall(item)
                  zz=requests.get(match2[0], headers=headers).content
                  regex_3=domain_s+'dwatchseries.to/.+?.html\?r=(.+?)"'
              
                  match3=re.compile(regex_3).findall(zz)
             
                  for all_l in match3:
                    if stop_all==1:
                        break
                    f_link=all_l.decode('base64')
                    name1,match_s,res,check=server_data(f_link,original_title)
                    if check:
                      all_links.append((name1.replace("%20"," "),f_link,match_s,res))
                      
                   
                      link_cin=all_links
                  
        return all_links
def get_cmovies(tv_mode,original_title,name,season_n,episode_n,season,episode,year_w):
        global links_cmovies,stop_all
        title=original_title

        if tv_mode=='tv':
          link=domain_s+'cmovies.io/film/%s-season-%s/watching.html?ep=%s'%(title.lower().replace('%20','-').replace('%3a','').replace(' ','-'),season,episode)
         
          
        else:
         
          headers = {
                'Host': 'cmovies.io',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
                'Referer': domain_s+'cmovies.io/film/the-maze-runner-nbb',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                }

          params = (
                ('keyword', title.lower().replace('%3a','').replace('%20','+').replace(' ','+')),
                   )

          response = requests.get(domain_s+'cmovies.io/ajax/suggest_search', headers=headers, params=params).json()

          
          
          
          regex='href="(.+?)"'
          match_l=re.compile(regex).findall(response['content'])
          
          tt=requests.get(domain_s+'cmovies.io'+match_l[0]+'/watching.html').content
         
          regex_l="var page_url = '(.+?)'"
          match_ll=re.compile(regex_l).findall(tt)
          episode=match_ll[0].split('=')[1]
          link=domain_s+'cmovies.io'+match_l[0]+'/watching.html'+match_ll[0]
          
        
        x=requests.get(link).content
        
        regex='title="Episode %s" class="btn-eps.+?player-data="(.+?)"'%episode
        response2=re.compile(regex).findall(x)

        all_links=[]
        all_links_in=[]
        import resolveurl
        for links in response2:
          if stop_all==1:
               break
          try:
              if 'vidnode.net' in links:
      
               zz=requests.get('https:'+links).content
         
               regex_l="sources.+?file.+?'(.+?)'"
               match_l=re.compile(regex_l).findall(zz)
               
               for ll in match_l:
                 if 'google' not in ll:
            
                  #regex_l='//(.+?)/'
                  #match_l=re.compile(regex_l).findall(ll)
   
                  link_n=get_redirect(ll)
           
                  links_name=link_n.split('/')
                  
                  name1=links_name[len(links_name)-1].replace('.mp4','').replace('.mkv','').replace('.avi','')
                  if clean_name(original_title,1).replace(" ",".") not in name1:
                    name1=clean_name(original_title,1)
                  all_links.append((name1,link_n,'CMOVIES','HD'))
                  links_cmovies=all_links
               
               regex_l='window.location = "(.+?)"'
               match_l22=re.compile(regex_l).findall(zz)
              
               
               for ll in match_l22:
                resolvable=resolveurl.HostedMediaFile(ll).valid_url()
                if stop_all==1:
                       break
                if resolvable:
                   
                   yy=requests.get(ll)
                   link_ok=check_link(yy)
                   if link_ok:
                   
                       regex='og:title" content="(.+?)"'
                       match_n=re.compile(regex).findall(yy.content)
                       if len( match_n)==0:
                            regex='<Title>(.+?)</Title>'
                            match_n=re.compile(regex,re.IGNORECASE).findall(yy.content)
                       if len(match_n)==0:
                         regex='name="fname" value="(.+?)"'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                       if len(match_n)==0:
                         regex='<title>(.+?)</title>'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                       regex_l='//(.+?)/'
                       match_l=re.compile(regex_l).findall(ll)
                       srv=match_l[0]
                       if len(match_n)>0 and 'thevideo' not in ll:
                           match_n[0]=match_n[0].replace('\n','').replace('  ',' ').replace('\t','').replace('\r','')
                           info=(PTN.parse(match_n[0]))
                           nam1=match_n[0].replace('%20',' ')
                           if 'resolution' in info:
                              res=info['resolution']
                           else:
                              res=' '
                       else:
                         nam1=original_title.replace('%20',' ')
                         res=' '
                       if ll not in all_links_in:
                         all_links_in.append(ll)
                         all_links.append((nam1,ll,match_l[0],res))
                         links_cmovies=all_links
               regex_l=' "Download Video",.+?"(.+?)"'
               match_l=re.compile(regex_l,re.DOTALL).findall(zz)
               if len(match_l)==0:
                   regex_l='id="embedvideo" src="(.+?)"'
                   match_l=re.compile(regex_l,re.DOTALL).findall(zz)
               tt=requests.get(match_l[0]).content
               
               regex_l='href="(.+?)" target=\'_blank\''
               match_l22=re.compile(regex_l).findall(tt)
           
    
               for ll in match_l22:

                resolvable=resolveurl.HostedMediaFile(ll).valid_url()

                if resolvable:
               
           
                   
                   yy=requests.get(ll,timeout=10)
                   link_ok=check_link(yy)
                   if link_ok:
                     
                       regex='og:title" content="(.+?)"'
                       match_n=re.compile(regex).findall(yy.content)
                       if len( match_n)==0:
                            regex='<Title>(.+?)</Title>'
                            match_n=re.compile(regex,re.IGNORECASE).findall(yy.content)
                       if len(match_n)==0:
                         regex='name="fname" value="(.+?)"'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                       if len(match_n)==0:
                         regex='<title>(.+?)</title>'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                       regex_l='//(.+?)/'
                       match_l=re.compile(regex_l).findall(ll)
                       srv=match_l[0]
                       if len(match_n)>0 and 'thevideo' not in ll:
                           match_n[0]=match_n[0].replace('\n','').replace('  ',' ').replace('\t','').replace('\r','')
                           info=(PTN.parse(match_n[0]))
                           nam1=match_n[0].replace('%20',' ')
                           if 'resolution' in info:
                              res=info['resolution']
                           else:
                              res=' '
                       else:
                         nam1=original_title.replace('%20',' ')
                         res=' '
                       
                       if ll not in all_links_in:
                         all_links_in.append(ll)
                         all_links.append((nam1,ll,match_l[0],res))
                         links_cmovies=all_links
                        
              else:
               
               resolvable=resolveurl.HostedMediaFile(links).valid_url()
          
               if resolvable:
                   
                   yy=requests.get(links)
                   link_ok=check_link(yy)
                   if link_ok:
                   
                       regex='og:title" content="(.+?)"'
                       match_n=re.compile(regex).findall(yy.content)
                       if len( match_n)==0:
                            regex='<Title>(.+?)</Title>'
                            match_n=re.compile(regex,re.IGNORECASE).findall(yy.content)
                       if len(match_n)==0:
                         regex='name="fname" value="(.+?)"'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                       if len(match_n)==0:
                         regex='<title>(.+?)</title>'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                       regex_l='//(.+?)/'
                       match_l=re.compile(regex_l).findall(links)
                       srv=match_l[0]
                       if len(match_n)>0 and 'thevideo' not in links:
                           match_n[0]=match_n[0].replace('\n','').replace('  ',' ').replace('\t','').replace('\r','')
                           info=(PTN.parse(match_n[0]))
                           nam1=match_n[0].replace('%20',' ')
                           if 'resolution' in info:
                              res=info['resolution']
                           else:
                              res=' '
                       else:
                         nam1=original_title.replace('%20',' ')
                         res=' '
                       if links not in all_links_in:
                         all_links_in.append(links)
                         all_links.append((nam1,links,match_l[0],res))
                         links_cmovies=all_links
          except:
            pass
        return links_cmovies
def get_dwatch(tv_mode,original_title,name,season_n,episode_n,season,episode,year_w):
        global links_dwatch,stop_all
        all_links=[]
        title=original_title.replace('%20',' ')
        headers = {
            'Host': 'moviegrabber.tv',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': domain_s+'moviegrabber.tv/',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        params = (
            ('q', title),
            ('format', 'json'),
        )

        response = requests.get(domain_s+'moviegrabber.tv/backend/media/search', headers=headers, params=params).json()
       
        
        for item in response['shows']:
      
          if title.lower() in item['showname'].lower().replace(':','') and str(year_w) in item['showname']:
            
            data = {'epid':'0',
            'showid':item['showid'],
            'data':'web'
            }

            headers = {
                'Host': 'moviegrabber.tv',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': domain_s+'moviegrabber.tv/videos/%s/0'%item['showid'],
                'content-type': 'application/json',
                'X-CSRFTOKEN': '',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }
            xx = requests.post(domain_s+'moviegrabber.tv/backend/media/getLinks', headers=headers, json=data).json()
        
            for l_data in xx['links']:
               l_data=l_data['url']
               n_link=l_data.split('http://stream.moviegrabber.tv/resolve/')
               if len(n_link)>1:
                       yy=requests.get(n_link[1])
             
                       regex='og:title" content="(.+?)"'
                       match_n=re.compile(regex).findall(yy.content)
       
                       if len( match_n)==0:
                            regex='<Title>(.+?)</Title>'
                            match_n=re.compile(regex,re.IGNORECASE).findall(yy.content)
                       if len(match_n)==0:
                         regex='name="fname" value="(.+?)"'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                       if len(match_n)==0:
                         regex='<title>(.+?)</title>'
                         match_n=re.compile(regex,re.DOTALL).findall(yy.content)
                
                       if len(match_n)>0:
                           match_n[0]=match_n[0].replace('\n','').replace('  ',' ').replace('\t','').replace('\r','')
                           info=(PTN.parse(match_n[0]))
                           nam1=match_n[0].replace('%20',' ')
                           if 'resolution' in info:
                              res=info['resolution']
                           else:
                              res=' '
                       else:
                         nam1=original_title.replace('%20',' ')
                         res=' '
               else:
                         nam1=original_title.replace('%20',' ')
                         res=' '
               regex='//(.+?)/'
               match=re.compile(regex).findall(l_data)
               if 'http://stream.moviegrabber.tv/resolve/' in l_data:
                  l_data=l_data.split('http://stream.moviegrabber.tv/resolve/')[1]
               all_links.append((nam1,l_data,match[0],res))
               links_dwatch=all_links
        return links_dwatch
def get_we(tv_mode,original_title,name,season_n,episode_n,season,episode,year_w):
        global links_we,stop_all
        title=original_title
        f_link=''
        if tv_mode=='tv':
            link=domain_s+'www.watchepisodes4.com/'+(title.lower().replace('%20','-').replace('%3a','').replace(' ','-'))
            
              
           
              
            
            x=requests.get(link).content
            regex='href="(.+?)"'
            
            response2=re.compile(regex).findall(x)
            for li in response2:
             
              if 'season-%s-episode-%s-'%(season,episode) in li:
                f_link=li
                break
            if len(f_link)>0:
                x=requests.get(f_link).content
                regex='class="watch-button" data-actuallink="(.+?)"'
                response2=re.compile(regex).findall(x)
                all_links=[]
                import resolveurl
                for links in response2:
                  if stop_all==1:
                    break
                  if 1:#try:
                       resolvable=resolveurl.HostedMediaFile(links).valid_url()
                       if resolvable:
                          
                            name1,match_s,res,check=server_data(links,original_title)
                            if check:
                              all_links.append((name1.replace("%20"," "),links,match_s,res))
                              links_we=all_links
              #except:
              #  pass
        return links_we
def get_direct_links(tv_mode,original_title,name,season_n,episode_n,season,episode,year):
        global link_direct
        all_links=[]
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': '123netflix.pro',
            'Pragma': 'no-cache',
            'Referer': domain_s+'123netflix.pro/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
        
        if tv_mode=='movie':
            params = (
                ('s', clean_name(original_title,1)),
            )
        else:
            params = (
                ('s', clean_name(original_title,1)+' season '+season),
            )

        response = requests.get(domain_s+'123netflix.pro/', headers=headers, params=params).content
        
        regex='class="ml-item"><a href="(.+?)".+?title="(.+?)"'
        match=re.compile(regex).findall(response)
        f_link=''
        if tv_mode=='movie':
          string_check=year
        else:
          string_check=' season '+ season
          
        for link,name in match:
          name=name.replace('&#8217;',"'").replace(':',"")

          if clean_name(original_title,1).lower() in name.lower() and string_check.lower() in name.lower():
             f_link=link
             break
   
        if f_link!='':

            headers = {
                'accept-encoding': 'utf8',
                'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'referer': f_link,
                'authority': 'dvideos.me',
            }
            html=requests.get(f_link).content
            if tv_mode=='tv':
             regex='<a href="#(.+?)">Episode - (.+?)</a>'
             match=re.compile(regex).findall(html)
             for l_name,ep in match:
     
               if ep==episode:
                 f_name=l_name
                 break
            
             regex='<div id="%s" ><div class="movieplay"><iframe src="(.+?)"'%f_name
             match=re.compile(regex).findall(html)
            else:
                regex='<div class="movieplay"><iframe src="(.+?)"'
                match=re.compile(regex).findall(html)
            yy=requests.get(match[0].replace("\/","/"),headers=headers).content
            regex='<iframe  src="(.+?)"'
            match=re.compile(regex).findall(yy)
            for link in match:
               name1,match_s,res,check=server_data(link,original_title)
               if check:
                  all_links.append((name1.replace("%20"," "),link,match_s,res))
                  link_direct=all_links
        return all_links
def get_direct_links_old(tv_mode,original_title,name,season_n,episode_n,season,episode,year):
  global link_direct
  url='http://dl.bi-seda.ir/Films/'
  html=requests.get(url).content
  regex=re.compile('<a href="(.+?)"')
  match_l=re.compile(regex).findall(html)
  zz=0
  all_links=[]
  url='http://103.67.198.6/uploaded-videos/'
  html=requests.get(url).content
  regex=re.compile('<a href="(.+?)"')
  match_l2=(re.compile(regex).findall(html))
  base_url='http://dl.bi-seda.ir/Films/'
  for link in match_l:
   link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
   if len(link_t)>2 and link!=None:
   
       info=(PTN.parse(link_t))


       if 'title' in info:
           title=info['title']
           if 'year' in info:
             year_in=info['year']
           if 'season' not in info:
              
               zz=zz+1
               if 'resolution' in info:
                 res=info['resolution']
               else:
                 res=' '
               

                 
               if title==original_title.replace("%20"," "):
                
                  if 'year' in info:
                    if str(year_in)==str(year):
                      all_links.append((link.replace("%20"," "),base_url+link,'ava',res))
                  else:
                     all_links.append((link.replace("%20"," "),base_url+link,'ava',res))
                  link_direct=all_links
  base_url='http://103.67.198.6/uploaded-videos/'
  for link in match_l2:
      link_t=link.replace('%20','.').replace('%28','.').replace('%29','.').replace('...','.').replace('..','.')
      if len(link_t)>2 and link!=None:  
     
       info=(PTN.parse(link_t))


       if 'title' in info:
           title=info['title']
           if 'year' in info:
             year_in=info['year']
           if 'season' not in info:
              
               zz=zz+1
               if 'resolution' in info:
                 res=info['resolution']
               else:
                 res=' '
               
                       
            
               if title==original_title.replace("%20"," "):
              
                  if 'year' in info:
                    if str(year_in)==str(year):
                      all_links.append((link.replace("%20"," "),base_url+link,'ava',res))
                  else:
                     all_links.append((link.replace("%20"," "),base_url+link,'ava',res))
                  
                  link_direct=all_links
                  
             
  return all_links
def get_upto(tv_movie,original_title,name,season_n,episode_n,season,episode,year):
  global link_upto
  all_links=[]

  x=requests.get('http://uptoboxsearch.com/').content
  regex="var cx = '(.+?)'"
  match=re.compile(regex).findall(x)
  cx=match[0]
  
  x=requests.get(domain_s+'cse.google.com/cse.js?cx='+cx).content
  regex='"cse_token": "(.+?)"'
  match=re.compile(regex).findall(x)
  cse=match[0]
  if tv_movie=='movie':
    q=(original_title.replace('%20',' ')+' '+year)
  else:
    q=(original_title.replace('%20',' ').replace('%27','')+' s'+season_n+' e'+episode_n)

  headers = {
        'Host': 'www.googleapis.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://uptoboxsearch.com/',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
  }
  params = (
        ('key', 'AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY'),
        ('rsz', 'filtered_cse'),
        ('num', '15'),
        ('hl', 'en'),
        ('prettyPrint', 'false'),
        ('source', 'gcsc'),
        ('gss', '.com'),
        
        ('cx', cx),
        ('q', q),
        ('cse_tok', cse),
        ('sort', ''),
        ('googlehost', 'www.google.com'),
        ('oq', q),
       
        ('callback', 'google.search.Search.apiary11806'),
  )

  html = requests.get(domain_s+'www.googleapis.com/customsearch/v1element', headers=headers, params=params).content
  
    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.get(domain_s+'www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=45e50696e04f15ce6310843f10a3a8fb&cx=004238030042834740991:-46442tgrgu&q=justice%20league%202017&cse_tok=AOdTmaC-ij38dzKkMq3QK2HyVv31W5gTHw:1520722941794&sort=&googlehost=www.google.com&oq=justice%20league%202017&gs_l=partner-generic.12...0.0.3.1622277.0.0.0.0.0.0.0.0..0.0.gsnos%2Cn%3D13...0.0jj1..1ac..25.partner-generic..36.5.239.zlYYXWhpZYw&callback=google.search.Search.apiary11806', headers=headers)

 
  regex='\((.+?)\);'
  match=re.compile(regex).findall(html)

  all_results=json.loads(match[0])
  for data in all_results['results']:
   if 'upto' in data['url']:
    title=data['titleNoFormatting']
 
    info=(PTN.parse(title.replace('..','.')))

    if 'resolution' in info:
      res=info['resolution']
    else:
      res=' '
    if 'http' not in data['url']:
      link_f='http://'+data['url']
    else:
      link_f=data['url']
    x=requests.get(link_f).content
    regex='<a href="https://uptostream.com/(.+?)"'
    match=re.compile(regex).findall(x)

    if len (match)>0:
        url=domain_s+'uptostream.com/'+match[0]

        all_links.append((title.replace("%20"," "),link_f,'Upto',res))
        link_upto=all_links
  return all_links
  
def get_seehd(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
  global link_seehd,stop_all
  all_links=[]
  url=domain_s+'www.seehd.pl/?s=%s+s%se%s'%(original_title.lower().replace('%20','+').replace('%3a','').replace(' ','+'),season_n,episode_n)
  if tv_movie=='tv':

    x,cook=cloudflare.request(url.strip())
  
   
    
  else:
    url=domain_s+'www.seehd.pl/?s=%s'%(original_title.lower().replace('%20','+').replace('%3a','').replace(' ','+'))

    x,cook=cloudflare.request(url.strip())
  regex='<a href="(.+?)"><h2 class="thumb_title">(.+?)</h2>'
  
  
  match=re.compile(regex).findall(x)
  
  for link,name in match:
    if stop_all==1:
      break
    if tv_movie=='tv':
      s_title='s%se%s '% (season_n,episode_n)
    else:
      s_title=name
  
    if original_title.lower().replace('%20',' ').replace('%3a','').replace('the','').strip() in name.lower() and s_title.lower() in name.lower():

      x,cook=cloudflare.request(link)
      regex='<iframe.+?src=(?:"|\')(.+?)(?:"|\')'
      match=re.compile(regex).findall(x)

      for link in match:
        if stop_all==1:
          break
    
        name1,match_s,res,check=server_data(link,original_title)
      
        if check:
          all_links.append((name1.replace("%20"," "),link,match_s,res))
          link_seehd=all_links
  return all_links
def get_afdah(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
  global link_afdah
  all_links=[]
  
  headers={'api_key': 'MWFkkDQzNDNxyzNkQEAjY29tLmFrYS5tb3ZpZXM=',
            'versionName': '1.0.0',
            'versioncode': '1',
            'Host': '35.198.246.6:3001',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'utf8',
            'User-Agent': 'okhttp/2.3.0'}
  search_t_a=original_title.split('%20')
  if len(search_t_a)>1:
    search_t=search_t_a[1]
  else:
    search_t=search_t_a[0]
  url='http://35.198.246.6:3001/movie/search?query='+search_t
  yy=requests.get(url,headers=headers).json()

  for item in yy['results']:

    if clean_name(original_title,1) in item['title'] and show_original_year in item['release_date']:
       url='http://35.198.246.6:3001/movie/%s/videos'%item['id']
       
       yy=requests.get(url,headers=headers).json()
       
       for item in yy['results']:
         if item['site']!='YouTube':
           all_links.append((original_title.replace("%20"," "),item['site'],'Gdrive',str(item['size'])))
           link_afdah=all_links

  url='http://104.251.215.154/auratik/api.php?kod=nonok2018&search='+original_title
  yy=requests.get(url).json()

  for item in yy['LIVETV']:

     if 'channel_title' in item:
      
      
      if clean_name(original_title,1).lower() in item['channel_title'].lower() and show_original_year in item['channel_title']:
        #all_links.append((item['channel_url'],item['channel_url'],'GDrive',item['channel_quality']))
        
       
        all_links.append((original_title.replace("%20"," "),item['channel_url'],'Direct',item['channel_quality']))
          
        link_afdah=all_links
  headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'palolak.xyz',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
  }

  url='http://apaapa.tk/malolak/api.php?kod=com.hdmoviesfree.app&search='+(original_title)

  yy=requests.get(url,headers=headers).json()
  
  for item in yy['LIVETV']:

     if 'channel_title' in item:
      if clean_name(original_title,1) in item['channel_title'] and show_original_year in item['channel_title']:
        #all_links.append((item['channel_url'],item['channel_url'],'GDrive',item['channel_quality']))
        
        name1,match_s,res,check=server_data(item['channel_director'],item['channel_title'])

        if check:
          all_links.append((name1.replace("%20"," "),item['channel_director'],match_s,res))
          
        link_afdah=all_links
  headers={'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; S16 Build/NRD90M)',
           'Host': 'manamana.xyz',
           'Connection': 'Keep-Alive',
           'Accept-Encoding': 'utf8'}

  url='http://manamana.xyz/mov/allahuakbar.php?search=%s&muveehd=hottest.moviered'%original_title
  
  yy=requests.get(url,headers=headers).json()

  for item in yy['HOTMOV']:
    if 'channel_title' in item:
     if clean_name(original_title,1).lower() in item['channel_title'].lower() and show_original_year in item['channel_title']:
       url='http://manamana.xyz/mov/allahuakbar.php?channel_id=%s&muveehd=hottest.moviered'%item['id']
  
       yy=requests.get(url,headers=headers).json()
     
       for item in yy['HOTMOV']:
           
           all_links.append((original_title.replace("%20"," "),item['channel_trailer'],'Openload',str(item['quality'])))
           all_links.append((original_title.replace("%20"," "),item['channel_url'],'Gdrive',str(item['quality'])))
           link_afdah=all_links
  url='http://newapps.mobodragon.com/appservice/AppSearch?PackageID=com.vivoapps.watchmoviesandtvseriesfree&Keyword='+original_title
  headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'newapps.mobodragon.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
  }
  yy=requests.get(url,headers=headers).content
  regex='a href="(.+?)&amp;MovieName=(.+?)"'
  match=re.compile(regex).findall(yy)
  for link,name in match:

    if clean_name(original_title,1).lower() in name.lower() and show_original_year in name:
      yy=requests.get(link,headers=headers).content
      break
  regex='<a href="(.+?)" class="slate_button"'
  match=re.compile(regex).findall(yy)
  if len(match)>0:
      yy=requests.get(match[0].replace("&amp;","&"),headers=headers).content
      
      regex='id="myVideo" src="(.+?)"'
      match=re.compile(regex).findall(yy)
     
      names=match[0].split('/')
      name1=names[len(names)-1]
      if "1080" in name1:
            res="1080"
      elif "720" in name1:
            res="720"
      elif "480" in name1:
            res="720"
      elif "hd" in name1.lower():
            res="HD"
      else:
           res=' '
      all_links.append((name1.replace("%20"," "),match[0],'Direct',res))
      link_afdah=all_links

  headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'dadodidu.xyz',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
  }

  params = (
    ('kod', 'com.muzzmoviesfree.app'),
    ('search', clean_name(original_title,1)),
  )

  yy = requests.get('http://dadodidu.xyz/muzzfree/api.php', headers=headers, params=params).content
  
  yy=yy[yy.index('{'):]
  


  yy=json.loads(yy.strip())
  for item in yy['LIVETV']:

     if 'channel_title' in item:
      if clean_name(original_title,1) in item['channel_title'] and show_original_year in item['channel_title']:
        all_links.append((item['channel_url'],item['channel_url'],'GDrive',item['channel_quality']))
        
        link_afdah=all_links
  headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'palolak.xyz',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
  }

  params = (
        ('kod', 'com.app.manggate'),
        ('search', clean_name(original_title,1)),
  )

  yy = requests.get('http://palolak.xyz/premium/api.php', headers=headers, params=params, cookies=cookies).content
  yy=yy[yy.index('{'):]
  


  yy=json.loads(yy.strip())
  for item in yy['LIVETV']:

     if 'channel_title' in item:
      if clean_name(original_title,1) in item['channel_title'] and show_original_year in item['channel_title']:
        if 'openload' in item['channel_url'].lower():
          name1,match_s,res,check=server_data(item['channel_director'],item['channel_title'])

          if check:
            all_links.append((name1,item['channel_url'],'GDrive',item['channel_quality']))
        else:
           all_links.append((item['channel_title'],item['channel_url'],'GDrive',item['channel_quality']))
        if 'openload' in item['channel_director'].lower():
          name1,match_s,res,check=server_data(item['channel_director'],item['channel_title'])
          
          if check:
            all_links.append((name1,item['channel_director'],'OP',item['channel_quality']))
          else:
            all_links.append((item['channel_title'],item['channel_director'],'OP',item['channel_quality']))
        link_afdah=all_links
  return all_links

class URLHandler():
    def __init__(self):
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('Accept-Encoding', 'gzip'),
                                  ('Accept-Language', 'en-us,en;q=0.5'),
                                  ('Pragma', 'no-cache'),
                                  ('Cache-Control', 'no-cache'),
                                  ('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 Kodi/17.2 (KHTML, like Gecko) Chrome/49.0.2526.111 Safari/537.36')]

    def request(self, url, data=None, query_string=None, ajax=False, referrer=None, cookie=None):
        if data is not None:
            data = urllib.urlencode(data)
        if query_string is not None:
            url += '?' + urllib.urlencode(query_string)
        if ajax:
            self.opener.addheaders += [('X-Requested-With', 'XMLHttpRequest')]
        if referrer is not None:
            self.opener.addheaders += [('Referrer', referrer)]
        if cookie is not None:
            self.opener.addheaders += [('Cookie', cookie)]

        content = None
  
        if data is not None and 'password' not in data:
            logging.warning("Post Data: %s" % (data))
        try:
            response = self.opener.open(url, data)
            content = None if response.code != 200 else response.read()

            if response.headers.get('content-encoding', '') == 'gzip':
                try:
                    content = zlib.decompress(content, 16 + zlib.MAX_WBITS)
                except zlib.error:
                    pass

            if response.headers.get('content-type', '') == 'application/json':
                content = json.loads(content, encoding="utf-8")

            response.close()
        except Exception as e:
            logging.warning("Failed to get url: %s\n%s" % (url, e))
            # Second parameter is the filename
        return content
urlHandler = URLHandler()
def login( notify_success=True):
        
        
        email = Addon.getSetting("Email")
        password = Addon.getSetting("Password")
        if email=='' or password=='':
          __settings__.openSettings()
          email = Addon.getSetting("Email")
          password = Addon.getSetting("Password")
        post_data = {'username': email, 'password': password}
        content = urlHandler.request(BASE_URL + "login/", post_data)

        if content['result'] == 'success':
            if notify_success:
                notify(32010)

            del content["result"]
            return content
        else:
            notify(32009)
            return None
def get_user_token( force_update=False):
        results =cache.get(login, 24, False, table='pages')
        '''
        if force_update:
            store.delete('credentials')
        
        results = store.get('credentials')
        if results:
            results = json.loads(results)
        else:
            results = login(False)
            if results:
                store.set('credentials', json.dumps(results))
        '''
        return results
def subcenter_search(item,mode_subtitle,subtitle_list,check_one):
        import re
        results = []
        
        id_collection=[]
    
        search_string = re.split(r'\s\(\w+\)$', item["tvshow"])[0] if item["tvshow"] else item["title"]

        
        user_token =  get_user_token()
        
        if user_token:
            query = {"q": search_string.encode("utf-8"), "user": user_token["user"], "token": user_token["token"]}
            if item["tvshow"]:
                query["type"] = "series"
                query["season"] = item["season"]
                query["episode"] = item["episode"]
            else:
                query["type"] = "movies"
                if item["year"]:
                    query["year_start"] = int(item["year"]) 
                    query["year_end"] = int(item["year"])

            search_result =  urlHandler.request( BASE_URL + "search/", query)
   
            if search_result is not None and search_result["result"] == "failed":
                # Update cached token
                user_token =  get_user_token(True)
                query["token"] = user_token["token"]
                search_result =  urlHandler.request( BASE_URL + "search/", query)

            if search_result is not None and search_result["result"] == "failed":
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('טייפון', 'בעיה בנתוני התחברות')).encode('utf-8'))
  
                return results



            if search_result is None or search_result["result"] != "success" or search_result["count"] < 1:
                
                    return results

            results = search_result# _filter_results(search_result["data"], search_string, item)
            
          

        else:
            xbmc.executebuiltin((u'Notification(%s,%s)' % ('טייפון', 'בעיה בנתוני התחברות')).encode('utf-8'))
        ret = []
        ok=True
        lang=[]
        lang.append('he')
        results2=[]
        for result in results['data']:
            total_downloads = 0
            counter = 0
            
            subs_list = result
            
              
            if subs_list is not None:
               

                for language in subs_list['subtitles']:
                        
                        
                       if language in lang:
                    #if xbmc.convertLanguage(language, xbmc.ISO_639_2) in item["3let_language"]:
                        for current in subs_list['subtitles'][language]:
                            

                            counter += 1
                            title = current["version"]
                            subtitle_list.append(title)
                            if check_one==True:
                              break
        return subtitle_list
def FirstPlace_Search(item,imdb_id,subtitle_list,check_one=False):
   
   import requests
   if item["tvshow"]:
       if 'tt' in imdb_id:
         query={"request":
            {
                "SearchPhrase": imdb_id,
                "SearchType": "ImdbID",
                "Version":"1.0",
                "Season":item["season"],
                "Episode":item["episode"]
            }
            }
       else:
         query={"request":
            {
                "SearchPhrase": item["tvshow"],
                "SearchType": "FilmName",
                "Version":"1.0",
                "Season":item["season"],
                "Episode":item["episode"]
            }
            }
       url_n='http://api.screwzira.com/FindSeries'
   else:
       if 'tt' in imdb_id:
         query={"request":
            {
                "SearchPhrase": imdb_id,
                "SearchType": "ImdbID",
                "Version":"1.0",
                "Season":item["season"],
                "Episode":item["episode"]
            }
            }
       else:
         query={"request":
            {
                "SearchPhrase": item["title"],
                "SearchType": "FilmName",
                "Version":"1.0",
                "year":int(item['year'])
            }
            }
            
       url_n='http://api.screwzira.com/FindFilm'

   subtitle=' '
   

   x=requests.post(url_n,json=query).json()
   z=0

   responce=json.loads(x)
   
   #subtitle_list=[]
   if responce['Results']!=None:
       for item_data in responce['Results']:
           


           if item_data["SubtitleName"] not in subtitle_list:
             subtitle_list.append(item_data["SubtitleName"])
             if check_one==True:
               break
              #addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listitem,isFolder=False)
           z=z+1
      

   return subtitle_list


def get_subs(tv_movie,original_title,season,episode,id,year,check_one=False):
    global all_subs
    item={}
 

    
    if tv_movie=='movie':
      item["tvshow"]=''
    else:
      item["tvshow"]=original_title.replace("%20"," ").replace("%27","'")
    if tv_movie=='tv':
      imdbid_data=domain_s+'api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&append_to_response=external_ids'%id
    else:
      imdbid_data=domain_s+'api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0&append_to_response=external_ids'%id

    x=requests.get(imdbid_data).json()
   
    try:
        imdbid=x['external_ids']['imdb_id']
        if imdbid==None:
          imdbid=''
    except:
      mdbid=''
    item['title']=original_title.replace("%20"," ").replace("%27","'")
  
    item["season"]=season.replace('%20','0')
    item["episode"]=episode.replace('%20','0')
    item["year"]=year
    subtitle_list=[]
 
    all_subs=(subcenter_search(item,'1',subtitle_list,check_one))
 
    if check_one==True:
      if len (all_subs)>0:
        return all_subs
    
    all_subs=(FirstPlace_Search(item,imdbid,all_subs,check_one))
    return all_subs
def get_pf(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
    
    global links_pf
    all_links=[]
    response,ok=cloudflare.request('http://pubfilmonline.net/?s='+original_title.replace("%20","+").replace(" ","+"))

    regex='<div class="result-item">.+?a href="(.+?)".+?alt="(.+?)" '
    match=re.compile(regex,re.DOTALL).findall(response)
    f_link=' '
    
    for link,name in match:
      name=name.replace("&#8217;","'")

 
      if tv_movie=='tv':
        show_original_year=name
      if clean_name(original_title,1) in name and show_original_year in name:
        f_link=link
        break

    
    
    if f_link!=' ':
        headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',

        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',

        'Host': 'pubfilmonline.net',
        'Pragma': 'no-cache',
        'Referer': f_link,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        'X-Requested-With': 'XMLHttpRequest'}
        
        z,ok=cloudflare.request(f_link)
        if tv_movie=='tv':
          regex='<div class="imagen"><a href="(.+?)">.+?<div class="numerando">(.+?) - (.+?)</div>'
          match_tv=re.compile(regex,re.DOTALL).findall(z)
          
          for link,season_in,episode_in in match_tv:
            if season==season_in and episode==episode_in:
              f_link2=link
              break
          z,ok=cloudflare.request(f_link2)

        regex='data-ids="(.+?)"'
        match=re.compile(regex).findall(z)
        regex_2='ajax_get_video_info":"(.+?)"'
        match_2=re.compile(regex_2).findall(z)
        data={
        'action':'ajax_get_video_info',
        'ids':match[0],
        'nonce':match_2[0],
        'server':'1'}
  
        x=requests.post('http://pubfilmonline.net/wp-admin/admin-ajax.php',headers=ok[1],cookies=ok[0],data=data).content
   
        for items in json.loads(x):

          all_links.append((clean_name(original_title,1),items['file'],'Direct',items['label']))
          links_pf=all_links
    return all_links
def get_rd_tvr(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
    global rd_tvr,stop_all
   
    all_links=[]
    if tv_movie=='tv':
      url='http://tv-release.pw/?s=%s+s%se%s'%(original_title.replace('%20',"+").replace('%27',"+").replace('.',"+"),season_n,episode_n)
    else:
      url='http://tv-release.pw/?s=%s+%s'%(original_title.replace('%20',"+").replace('%27',"+").replace('.',"+"),show_original_year)

    html,cook=cloudflare.request(url)

    regex="<h2><a hre.+?'(.+?)'>(.+?)</a>"
    match=re.compile(regex).findall(html)
    debrid_resolver = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()][0]
     
    debrid_resolver.login()
                
    for link,name in match:
   
      if stop_all==1:
        break
      if tv_movie=='tv':
        str_chk=('S%sE%s'%(season_n,episode_n)).lower()
      else:
        str_chk=show_original_year
      if clean_name(original_title,0).lower() in name.lower() and str_chk in name.lower():
   
        yy,ok=cloudflare.request(link)
     
        regex2="class=\"td_cols\"><a target='_blank' href='(.+?)'"
        match2=re.compile(regex2).findall(yy)
        for links in match2:
            if stop_all==1:
              break
            host = url.replace("\\", "")
            host2 = host.strip('"')
            host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(host2.strip().lower()).netloc)[0]
            host = replaceHTMLCodes(host)
            host = host.encode('utf-8')
            name2,match_s,res,check=server_data(links,original_title)
            resolvable= debrid_resolver.valid_url(links,host)
            
            if check and '.rar' not in links and resolvable:
                regex='//(.+?)/'
                match_s=re.compile(regex).findall(links)[0]
                name1s=links.split('/')
                name1=name1s[len(name1s)-1].replace('.html','').replace('TwoDDL_','')
      
                if clean_name(original_title,1).lower() not in name1.replace('.',' ').lower():
                  if clean_name(original_title,1).lower() not in name2.replace('.',' ').lower():
   
                    name1=clean_name(original_title,1)
                  else:
                    name1=name2
                 
                if "1080" in links:
                  res="1080"
                elif "720" in links:
                  res="720"
                elif "480" in links:
                  res="720"
                elif "hd" in links.lower():
                  res="HD"
                else:
                 res=' '
                all_links.append((name1.replace("%20"," "),links,match_s,res))
             
     
                rd_tvr=all_links
          
    return all_links
def get_m4u(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
        global links_m4u
        title=original_title
        title=title.replace("%20",' ').replace('%3a',':').replace('%27',"'").replace("'",'').replace(".",'')
        year=show_original_year
        all_links=[]
        if tv_movie=='movies':
          search_string=title+' '+year
        else:
          search_string=title


        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': domain_s+'m4ufree.com/',
            'Connection': 'keep-alive',
        }

        params = (
            ('keyword', search_string),
            ('search_section', '1'),
        )

        response = requests.get(domain_s+'m4ufree.com/', headers=headers, params=params).content



        regex='<div class="item">.+?a href="(.+?)" title="(.+?)"'
        match=re.compile(regex,re.DOTALL).findall(response)

        for link,name in match:

          if tv_movie=='tv':

             if title.lower()==name.lower():
               f_link=link
               break
          elif title.lower() in name.lower() and year in name:
            f_link=link
            break

        
        headers = {
            'Origin': domain_s+'m4ufree.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Referer': f_link,
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
     
        response = requests.get(f_link.replace("./",domain_s+'m4ufree.com/'), headers=headers).content

        if tv_movie=='tv':
          regex='idepisode="(.+?)" >S%s-E%s<'%(season_n,episode_n)
          match=re.compile(regex).findall(response)
          params = (
                ('idepisode', match[0]),
          )
          response = requests.get(domain_s+'m4ufree.com/ajax-tvshow.php', headers=headers, params=params).content
        
        regex='data="(.+?)"'
        match=re.compile(regex).findall(response)

        for servers in match:
            data = [
              ('m4u', servers),
            ]

            response = requests.post(domain_s+'m4ufree.com/ajax_new.php', headers=headers, data=data).content
            
            regex='<iframe src="(.+?)"'
            match2=re.compile(regex).findall(response)
            
            for links in match2:

               name1,match_s,res,check=server_data(links,original_title)

               if check:
                  all_links.append((name1.replace("%20"," "),links,match_s,res))
             
     
                  links_m4u=all_links
        return all_links
def get_ct(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
   global link_ct
   all_links=[]
   url='http://couchtuner.unblocked.lol/tv-shows/'
   headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'couchtuner.unblocked.lol',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
   }
   html=requests.get(url,headers=headers).content
   regex='<li><a href="(.+?)"><strong>(.+?)<'
   match=re.compile(regex).findall(html)
   
   for link,name in match:
     
     if clean_name(original_title,1).lower() in name.lower():
       
       yy=requests.get(link,headers=headers).content
       regex='strong><a href="(.+?)">.+?Season %s Episode %s<'%(season,episode)
       match2=re.compile(regex).findall(yy)
       
       for links in match2:
         zz=requests.get(links,headers=headers).content
         regex='Watch it here :</span> <a href="(.+?)"'
         match3=re.compile(regex).findall(zz)
         for links_in in match3:
           
           headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': 'mycouchtuner.nu',
                'Pragma': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
           }
           vv=requests.get(links_in,headers=headers).content
    
           regex='<iframe src="(.+?)"'
           match4=re.compile(regex).findall(vv)
           
           for f_link in match4:
             
              name1,match_s,res,check=server_data(f_link,original_title)
              if check :
                all_links.append((name1,f_link,match_s,res))
                link_ct=all_links
   return all_links
def get_magnet(tv_movie,original_title,season,episode,id,year):
    global all_magnet,imdb_global
    from play import search

    if tv_movie=='movie':
      
      imdbid_data=domain_s+'api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id
      
      x=requests.get(imdbid_data).json()
      imdbid=x['imdb_id']
      info={'search': 'movie', 'title': clean_name(original_title,1).replace("'",''), 'year': year, 'imdb_id':imdbid}
    else:
       imdbid_data=domain_s+'api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&append_to_response=external_ids'%id
      
       x=requests.get(imdbid_data).json()
       imdbid=x['external_ids']['imdb_id']
       info={'season': season, 'search': 'episode', 'title': clean_name(original_title,1).replace("'",''), 'episode': episode, 'imdb_id': imdbid}

    imdb_global=imdbid

    results=(search(info))

    all_magnet=results
    return all_magnet

def get_user_cookie():
    username = Addon.getSetting('username')
    password = Addon.getSetting('Password_sdr')

    if username and password:

        data = {
            'username': username,
            'password': password
        }

        req = requests.post(API + '/login', data=data, headers=HEADERS)
        res = req.json()

        if res['success']:
            return req.cookies.get_dict()

        else:
            xbmcgui.Dialog().ok('נסיון התחברות נכשל, סיסמא אופסה', ', '.join(res['errors']).encode('utf-8'))
            Addon.setSetting('password', '')

    return {}
def build_final_url(url, cookie):
    return 'https:' + url + '|Cookie=Sdarot={0}&User-Agent={1}'.format(urllib.quote(cookie.get('Sdarot'), safe=''), HEADERS.get('User-Agent'))

def get_final_video_and_cookie(sid, season, episode, choose_quality=False, download=False):

    cookie = get_user_cookie()
    req = requests.post(API + '/episode/preWatch', data={'SID': sid, 'season': season, 'episode': episode},
                        cookies=cookie, headers=HEADERS)
    token = req.text
    if not cookie:
        cookie = req.cookies.get_dict()

    if token == 'donor':
        vid = get_video_url(sid, season, episode, token, cookie, choose_quality)

    else:
        if download:
            plugin.notify('התחבר כמנוי כדי להוריד פרק זה', image=ICON)
            return None, None
        else:
            dp = xbmcgui.DialogProgress()
            dp.create("לצפייה באיכות HD וללא המתנה ניתן לרכוש מנוי", "אנא המתן 30 שניות", '',
                      "[COLOR orange][B]לרכישת מנוי להיכנס בדפדפן - www.sdarot.tv/donate[/B][/COLOR]")
            dp.update(0)
            for s in range(30, -1, -1):
                time.sleep(1)
                dp.update(int((30 - s) / 30.0 * 100), "אנא המתן 30 שניות", 'עוד {0} שניות'.format(s), '')
                if dp.iscanceled():
                    dp.close()
                    return None, None

        vid = get_video_url(sid, season, episode, token, cookie, choose_quality)

    if vid:
            return vid, cookie
def get_video_url(sid, season, episode, token, cookie, choose_quality):

    req = requests.post(API + '/episode/watch/sid/{0}/se/{1}/ep/{2}'.format(sid, season, episode),
                        data={'token': token}, cookies=cookie, headers=HEADERS).json()
    if req['success']:
        qualities = req['watch']
        if choose_quality:
            return qualities
        else:
            qualities_list = qualities.keys()
            max_quality = int('1080')
            quality = '480'

            if max_quality >= 720:
                quality = '1080' if '1080' in qualities_list and max_quality == 1080 else '720'
                if quality == '720' and '720' not in qualities_list:
                    quality = '480'

            return build_final_url(qualities[quality], cookie)
def get_sdarot(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year):
            global links_sdarot

            s = requests.Session()
            req = requests.Request(method='GET', url=API, headers=HEADERS)
            prep = req.prepare()
            prep.url = API + '/series/search/{0}/page/{1}/perPage/100'.format(name, '1')
            
            req = s.send(prep)
            all_links=[]
            results = req.json()['series']
            if results:
                items = []
                for s in results:
                
                    req = requests.get(API + '/series/info/{0}'.format(s['id']), headers=HEADERS).json()
                    serie = req['serie']
                    ep_found=0
                    se_found=0
                    episodes = serie['episodes']
               
                    for sen in episodes:
                      if sen==season:
                        se_found=1
                    
                    if se_found==1:
                        if (len(episodes)>=int(season)):
                          for items_in in episodes[season]:
                            ep=items_in['episode']
                     
                            if episode==ep:
                              ep_found=1
                              break
                       
                        if ep_found==1:
                            sd_link=json.dumps((s['id'], season, episode))
                          
                            if not episodes:
                                return []
                            #f_links=get_final_video_and_cookie(s['id'], season, episode, False, False)
                            all_links.append((s['heb'],sd_link,'Sdarot','480'))
                            links_sdarot=all_links
            return all_links
def get_linkia(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,dub='no'):
     global links_linkia,stop_all
     name=name.replace("%3a","")
     
     url=domain_s+'thelinkia.blogspot.co.il/'
     all_links=[]
     headers = {
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Language': 'en-US,en;q=0.5',
     'Cache-Control': 'no-cache',
     'Connection': 'keep-alive',
     'Host': 'thelinkia.blogspot.co.il',
     'Pragma': 'no-cache',
     'Upgrade-Insecure-Requests': '1',
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
     }
     html=requests.get(url,headers=headers).content
     regex="'post-count-link' href='(.+?)'"
     match=re.compile(regex).findall(html)
     found=0
     
       
       
     if tv_movie=='tv':
       url=domain_s+'thelinkia.blogspot.co.il/search/label/'+name+'%20%D7%A2%D7%95%D7%A0%D7%94%20'+(season)
     else:
       url=domain_s+'thelinkia.blogspot.co.il/search/label/'+name.replace('+',"%20")
     yy=requests.get(url,headers=headers).content

     regex="h3 class='post-title entry-title'.+?a href='(.+?)'>(.+?)</a>"
     match=re.compile(regex,re.DOTALL).findall(yy)
     for link,name_in in match:
         
         if tv_movie=='movie':
           if dub=='yes':
             second_con='מדובב'
           else:
             second_con=name_in
           string_for_check=show_original_year
         else:
           string_for_check='עונה %s, פרק %s'%(season,episode)+"$$$$$"
           second_con=name_in
         if urllib.unquote_plus(name) in name_in and string_for_check in name_in+"$$$$$" and second_con in name_in:
           f_link=link
           f_name=name_in
      
           break

     zz=requests.get(f_link,headers=headers).content
     regex='<b><a href="(.+?)" target="_blank">'
     match=re.compile(regex).findall(zz)
     for links_f in match:
          name1,match_s,res,check=server_data(links_f,f_name)
          if check :
            all_links.append((f_name,links_f,match_s,res))
            links_linkia=all_links
     return links_linkia
def get_uni(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    import universalscrapers
    global links_uni,stop_all
    if tv_movie=='movie':
      imdbid_data=domain_s+'api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id
      x=requests.get(imdbid_data).json()
      imdbid=x['imdb_id']
    else:
     imdbid_data=domain_s+'api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&append_to_response=external_ids'%id
     x=requests.get(imdbid_data).json()

     imdbid=x['external_ids']['imdb_id']
    all_links=[]
    
    if tv_movie=='movie':
        scraper = universalscrapers.scrape_movie
        links_scraper = scraper(
            clean_name(original_title,1),
            show_original_year,
            imdbid,
            timeout=1000,
            exclude=None,
            enable_debrid=allow_debrid)
    else:
     
                scraper = universalscrapers.scrape_episode
                links_scraper = scraper(
                    clean_name(original_title,1),
                    show_original_year,
                    show_original_year,
                    season,
                    episode,
                    imdbid,
                    '',
                    timeout=1000,
                    exclude=None,
                    enable_debrid=allow_debrid)
    for scraper_links in links_scraper():

       if stop_all==1:
         break
       for scraper_link in scraper_links:
        if stop_all==1:
         break
        
        name1,match_s,res,check=server_data(scraper_link['url'],original_title)
        
        if len(res)<2:
          res=scraper_link['quality']
        
        if check :
            all_links.append((name1,scraper_link['url'],match_s,res))
            links_uni=all_links
    return links_uni
def parseDOM(html, name='', attrs=None, ret=False):
    import dom_parser
    if attrs: attrs = dict((key, re.compile(value + ('$' if value else ''))) for key, value in attrs.iteritems())
    results = dom_parser.parse_dom(html, name, attrs, ret)
    if ret:
        results = [result.attrs[ret.lower()] for result in results]
    else:
        results = [result.content for result in results]
    return results
def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    txt = txt.strip()
    return txt
def get_2ddl(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global link_2ddl,stop_all
    
    imdbid_data=domain_s+'api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id
    x=requests.get(imdbid_data).json()
    imdb=x['imdb_id']
    search_link = '/lib/search526049.php?phrase=%s&pindex=1&content=true'
    base_link = 'http://rlsbb.ru'
    all_links=[]
    if tv_movie=='movie':
    
            url = {'imdb': imdb, 'title': original_title, 'year': show_original_year}
            url = urllib.urlencode(url)
    else:
            url = {'imdb': imdb,  'tvshowtitle': clean_name(original_title,1), 'year': show_original_year}
            url = urllib.urlencode(url)
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = clean_name(original_title,1), show_original_year, season, episode
            url = urllib.urlencode(url)
            
    sources = []



    data = urlparse.parse_qs(url)
    data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

    title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
    hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

    query = '%s S%02dE%02d' % (
    data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
    data['title'], data['year'])
    query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

    query = query.replace("&", "and")
    query = query.replace("  ", " ")
    query = query.replace(" ", "-")

    url = search_link % urllib.quote_plus(query)
    
    url = urlparse.urljoin(base_link, url)
    
    url = "http://rlsbb.ru/" + query

    import js2py_o
    x=requests.get('http://search.rlsbb.ru/js/light_script.js').content
    regex="basePage  \+ (.+?);"
    match=re.compile(regex,re.DOTALL).findall(x)

    r=js2py_o.eval_js("var locationtest_mode = '';"+match[0])
    if 'tvshowtitle' not in data: 
      #url = url + "-1080p"
      url='http://search.rlsbb.ru'+r+'?phrase=%s&pindex=1&content=true&rand=0.9575226837560482'%(clean_name(original_title,1).replace(' ','+')+'+'+show_original_year)
    else:
      url='http://search.rlsbb.ru'+r+'?phrase=%s&pindex=1&content=true&rand=0.9575226837560482'%(clean_name(original_title,1).replace(' ','+')+'+s'+season_n+'e'+episode_n)
    
    
    r = requests.get(url).content
    for u_in in json.loads(r)['results']:
        if stop_all==1:
          break
        u="http://rlsbb.ru/" +u_in['post_name']
        r = requests.get(u).content
        
  

        posts =parseDOM(r, "div", attrs={"class": "content"})
        if len(posts)==0:
          u='http://old.rlsbb.com/'+u_in['post_name']
          r = requests.get(u).content
          posts =parseDOM(r, "div", attrs={"class": "postContent"})
          
          
        items = []

       
        for post in posts:
            try:
                u = parseDOM(post, 'a', ret='href')
                
                for i in u:
                    try:
                        name = str(i)
                        if hdlr in name.upper(): items.append(name)
                    except:
                        pass
            except:
                pass

        seen_urls = set()
        
        debrid_resolver = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()][0]
     
        debrid_resolver.login()
        all_links_sum=[]
        for item in items:
            if stop_all==1:
                 break
            try:
                if 0:#'tvshowtitle'  in data:
                  
                  if 'torrent' in item[1].lower() or 'protected' in item[0] or 'tv.com' in item[0] or 'img.rls' in item[0]:
                  
                   continue
                  else:
                    item='http'+item[0]
                
                info = []

                url = str(item)
                url = replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if url in seen_urls: continue
                seen_urls.add(url)

                host = url.replace("\\", "")
                host2 = host.strip('"')
                host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(host2.strip().lower()).netloc)[0]

         
                if any(x in host2 for x in ['.rar', '.zip', '.iso']): continue

                if '720p' in host2:
                    quality = 'HD'
                elif '1080p' in host2:
                    quality = '1080p'
                else:
                    quality = 'SD'

           
                host = replaceHTMLCodes(host)
                host = host.encode('utf-8')
                
                resolvable= debrid_resolver.valid_url(url,host)
                
                #sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': host2, 'info': info, 'direct': False, 'debridonly': True})
                #name1,match_s,res,check=server_data(vid_url,original_title)
             
                if resolvable:
                    name2,match_s,res,check=server_data(host2,original_title)
                    
                   
                    
                    if check:
                        regex='//(.+?)/'
                        match_s=re.compile(regex).findall(host2)[0]
                        name1s=host2.split('/')
                        name1=name1s[len(name1s)-1].replace('.html','').replace('TwoDDL_','')
                        if clean_name(original_title,1).lower() not in name1.replace('.',' ').lower():
                          if clean_name(original_title,1) not in name2.replace('.',' '):
                           
                            name1=clean_name(original_title,1)
                          else:
                            name1=name1
 
                         
                        if "1080" in host2:
                          res="1080"
                        elif "720" in host2:
                          res="720"
                        elif "480" in host2:
                          res="720"
                        elif "hd" in host2.lower():
                          res="HD"
                        else:
                         res=' '
                        
                        all_links_sum.append(host2)
                        all_links.append((name1,host2,match_s,res))
                        
                        link_2ddl=all_links
            
            except Exception as e:
              logging.warning(e)
              pass
              
    return all_links
def get_onitube(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global link_onitube
    all_links=[]
    if tv_movie=='tv':
      search_string=clean_name(original_title,1).replace(' ','+')+'+'+'s'+season_n+'e'+episode_n
    else:
      search_string=clean_name(original_title,1).replace(' ','+')+'+'+show_original_year
    url=domain_s+'www.onitube.com/search/videos?search_query='+search_string
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.onitube.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    html=requests.get(url,headers=headers).content
    regex='<a href="https://www.onitube.com/video/(.+?)/.+?title="(.+?)".+?"hd-text-icon">(.+?)<'
    match=re.compile(regex,re.DOTALL).findall(html)
    for link,name,quality in match:
       ok=0
       if tv_movie=='tv':
        show_original_year=name
        if clean_name(original_title,1).lower() in name.lower() and 's'+season_n+'e'+episode_n in name.lower():
         ok=1
       else:
         if clean_name(original_title,1).lower() in name.lower() and show_original_year in name:
           ok=1
       if ok==1:
       
            if "1080" in quality:
              res="1080"
            elif "720" in quality:
              res="720"
            elif "480" in quality:
              res="480"
            elif "hd" in quality.lower():
              res="HD"
            else:
             res=' '
             
            
            match_s='Direct'
            name1=clean_name(original_title,1)
            
            f_link=domain_s+'ont-assets-1.finalservers.net/mp4sd.php?id='+link
           
            
            all_links.append((name1,f_link,match_s,res))
            link_onitube=all_links
    return link_onitube
def get_tvl(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_tvl
    all_links=[]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.tvil.me',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    
    html=requests.get('http://www.tvil.me/?page=search&key='+original_title,headers=headers).content
   
    regex='<div id="page-right">.+?<span style=".+?">(.+?)<.+?<a href="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(html)

    for title_o,link in match:
       #if clean_name(original_title,1) in name:
            x=requests.get(link,headers=headers).content
            regex='<div id="change-season-%s".+?<a href="(.+?)"'%season
            match2=re.compile(regex,re.DOTALL).findall(x)[0]

            
            html2=requests.get('http://www.tvil.me/'+match2).content
            regex='<div id="change-episode-%s".+?<a href="(.+?)"'%episode
            
            match4=re.compile(regex,re.DOTALL).findall(html2)[0]
            html2=requests.get('http://www.tvil.me/'+match4).content
            
            regex='(?:<div class="view-watch-button">|<div class="view-download-button">)<a href="(.+?)" target="_blank">(.+?)</a>'
            match3=re.compile(regex,re.DOTALL).findall(html2)
            
            regex2="'src','(.+?)'"
            match4=re.compile(regex2,re.DOTALL).findall(html2)
            for links,title in match3:
              links=links.replace("\n","").strip()
         
              resolvable=resolveurl.HostedMediaFile(links).valid_url()
              
              if resolvable:
                  #name1,match_s,res,check=server_data(links,original_title)
                  regex='//(.+?)/'
                  match_s=re.compile(regex).findall(links)[0]
                  res=' '
                  all_links.append((title_o,links,match_s,res))
                  links_tvl=all_links

            for links in match4:
              links=links.replace("\n","").strip()
   
              resolvable=resolveurl.HostedMediaFile(links).valid_url()
              
              if resolvable:
                  #name1,match_s,res,check=server_data(links,original_title)
                  regex='//(.+?)/'
                  match_s=re.compile(regex).findall(links)[0]
                  res=' '
                  all_links.append((title_o,links,match_s,res))
                  links_tvl=all_links
        
    return links_tvl
def get_filepursuit(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global link_filepursuit
    all_links=[]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'filepursuit.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    
    if tv_movie=='tv':
      search_string=clean_name(original_title,1).replace(' ','+')+'+'+'s'+season_n+'e'+episode_n
    else:
      search_string=clean_name(original_title,1).replace(' ','+')+'+'+show_original_year
    match_next=['0']
    dbconserver = database.connect(servers_db)
    dbcurserver = dbconserver.cursor()


    dbcurserver.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""speed TEXT);" % 'servers')
    dbcurserver.execute("VACUUM 'AllData';")
    dbcurserver.execute("PRAGMA auto_vacuum;")
    dbcurserver.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
    dbcurserver.execute("PRAGMA temp_store=MEMORY ;")
    dbconserver.commit()
    while len(match_next)>0:
    
        html=requests.get(domain_s+'filepursuit.com/search4/%s/type/videos/startrow/%s'%(search_string,match_next[0]),headers=headers).content
        logging.warning(domain_s+'filepursuit.com/search4/%s/type/videos/startrow/%s'%(search_string,match_next[0]))
        regex='data-clipboard-text="(.+?)"'
        match=re.compile(regex).findall(html)

        for link in match:
            split_link=link.split('/')
            name1=split_link[len(split_link)-1].replace('.mp4','').replace('.mkv','').replace('.avi','')
            regex='//(.+?)/'
            match_s=re.compile(regex).findall(link)[0]
            dbcurserver.execute("SELECT speed FROM servers WHERE name = '%s'"%(match_s))

            match = dbcurserver.fetchone()
            ok=0
            if match!=None:
       
              if match[0]!='TIMEOUT' and float(match[0])<0.6:
                ok=1
            if 'trailer' in name1.lower():
              ok=0
            if Addon.getSetting("filter_fp")=='false':
              ok=1
            if ok==1:
                if "1080" in link:
                  res="1080"
                elif "720" in link:
                  res="720"
                elif "480" in link:
                  res="720"
                elif "hd" in link.lower():
                  res="HD"
                else:
                 res=' '
                all_links.append((name1,link,match_s,res))
                link_filepursuit=all_links
        regex='type/videos/startrow/(.+?)"><strong>Next<'
        match_next=re.compile(regex).findall(html)
    return link_filepursuit
def get_ftp(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_ftp
    all_links=[]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.searchftps.net',
        'Pragma': 'no-cache',
        'Referer': domain_s+'www.searchftps.net/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    if tv_movie=='tv':
      search_s=clean_name(original_title,1).replace(' ','+')+'+s'+season_n+'e'+episode_n
    else:
      search_s=clean_name(original_title,1).replace(' ','+')+'+'+show_original_year
    data={'action':'result','args':'k=%s&t=and&o=size-desc&s=0'%(search_s)}
                                   
    response = requests.post(domain_s+'www.searchftps.net/', headers=headers,data=data).content

    regex="javascript:go\('content', \{'type':'f', 'hash':'(.+?)'\}\)\" title=\"(.+?)\".+?dn-size.+?<b>(.+?)<"
    match=re.compile(regex,re.DOTALL).findall(response)
    for hash,title,size in match:
      acc_size=size.split(" ")
      max_size=int(Addon.getSetting("ftp_size"))
      if float(acc_size[0])<max_size and acc_size[1]=='GB':
          data={'action':'content','args':'type=f&hash=%s'%hash}
          response2 = requests.post(domain_s+'www.searchftps.net/', headers=headers,data=data).content
          
          regex="ct2_t = decodeURIComponent\(escape\(decode\('(.+?)'"
          match2=re.compile(regex).findall(response2)[0].decode('base64')
          if '.srt' not in match2:
              links_name=match2.split('/')
                          
              name1=urllib.unquote(links_name[len(links_name)-1].replace('.mp4','').replace('.mkv','').replace('.avi',''))
              if "1080" in match2:
                res="1080"
              elif "720" in match2:
                res="720"
              elif "480" in match2:
                res="720"
              elif "hd" in match2.lower():
                res="HD"
              else:
               res=' '
              all_links.append((name1,match2,'FTP - '+size,res))
              links_ftp=all_links
    return links_ftp
def get_raqlink(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_reqzone
    search_link='http://reqzone.com/?s='+clean_name(original_title,1).replace(' ','+')
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'reqzone.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    all_links=[]
    html=requests.get(search_link,headers=headers).content
    regex='h3 class="entry-title">.+?<a href="(.+?)" title=".+?" rel="bookmark">(.+?)<'
    match=re.compile(regex,re.DOTALL).findall(html)

    for link,name in match:
        if tv_movie=='tv':

          clean_name_t=name.split(' &#8211; ')[0]
          show_original_year=name
        else:
          if '&#8211;' in name:
            clean_name_t=name.split(' &#8211; ')[0]
            trilogy_flag=1
          else:
             clean_name_t=name.split(' (')[0]
             trilogy_flag=0
     
        if clean_name(original_title,1).lower()==clean_name_t.lower():
             x=requests.get(link,headers=headers).content
             if tv_movie=='tv':
               regex='<span class="vc_tta-title-text">Season %s (.+?)<.+?<h3 style="text-align: center;">Episode %s<.+?<a href="(.+?)"'%(season,episode)
               match=re.compile(regex,re.DOTALL).findall(x)
               for quality,link in match:
                  if "1080" in quality:
                    res="1080"
                  elif "720" in quality:
                    res="720"
                  elif "480" in quality:
                    res="480"
                  elif "hd" in quality.lower():
                    res="HD"
                  else:
                   res=' '
                  all_links.append((original_title,link,quality.split('/')[2],res))
                  links_reqzone=all_links
             else:
               if '<h1 style="text-align: center;">'+clean_name(original_title,1) in x:
                 regex='<div class="wpb_wrapper">.+?<h1 style="text-align: center;">%s \(.+?<div class="wpb_wrapper">(.+?)</div>'%clean_name(original_title,1)
               else:
                 regex='<div class="wpb_wrapper">(.+?)</div>'
               match=re.compile(regex,re.DOTALL).findall(x)
               quality_save=''

               for links in match:
                 regex_in='<h1 style="text-align: center;"><span style="color: .+?;">(.+?)<|Server (.+?)</h3>.+?<h3 style=.+?href="(.+?)"'
                 match_in=re.compile(regex_in,re.DOTALL).findall(links)
                 for quality,server,link in match_in:
                     
                     if len(link)>0:
             
                      if "1080" in quality_save:
                        res="1080"
                      elif "720" in quality_save:
                        res="720"
                      elif "480" in quality_save:
                        res="480"
                      elif "hd" in quality_save.lower():
                        res="HD"
                      else:
                       res=' '
                      all_links.append((original_title,link,'Server '+server,res))
                      links_reqzone=all_links
                     else:
                       quality_save=quality
            
    return links_reqzone
def get_links_moviesak(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_moviesak
    all_links=[]
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.moviesak47.net',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    html=requests.get('https://www.moviesak47.net/complete-list-of-tv-series/',headers=headers).content
    regex='<li class="cat-item cat-item-.+?">.+?a href="(.+?)" data-wpel-link="internal">(.+?)<'
    match=re.compile(regex,re.DOTALL).findall(html)

    for link,title in match:
      
      
      if clean_name(original_title,1)==title.strip():
        x=requests.get(link,headers=headers).content
        regex='<article>.+?a href="(.+?)" title="%s Season %s .+?</article>'%(clean_name(original_title,1),season)
        match2=re.compile(regex).findall(x)
        if len (match2)>0:
           
              y=requests.get(match2[0],headers=headers).content
            
              regex='a href="(.+?)" data-wpel-link="external" target="_blank" rel="nofollow external noopener noreferrer"(.+?)</'
              match4=re.compile(regex).findall(y)
  
              for links,quality_save in match4:
               
                if len(links)>0 and '%20S{0}E{1}%20'.format(season_n,episode_n) in links:
             
                      if "1080" in quality_save:
                        res="1080"
                      elif "720" in quality_save:
                        res="720"
                      elif "480" in quality_save:
                        res="480"
                      elif "hd" in quality_save.lower():
                        res="HD"
                      else:
                       res=' '
                      regex='//(.+?)/'
                      match=re.compile(regex).findall(links)
                      names=links.split('/')
                      name1=names[len(names)-1].replace('.mkv','').replace('.mp4','').replace('.avi','')
                      all_links.append((name1,links,match[0],res))
                      links_moviesak=all_links
    return links_moviesak
def get_gonaw_try(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_gona
    from Cookie import SimpleCookie
    import js2py_o
    all_links=[]
    
    xy,cook1=cloudflare.request('https://www1.mehlizmovieshd.com/wp-content/plugins/bots-protect/token.php')
    y,cook=cloudflare.request('https://www1.mehlizmovieshd.com/wp-content/plugins/bots-protecthd/js/botProtect.js')
    regex='var stringLength =(.+?)alert\("Thank '
    match=re.compile(regex,re.DOTALL).findall(y)
    
    result=js2py_o.eval_js('var stringLength ='+match[0].replace('var token = response;','').replace('token',"'"+xy+"'").replace('document.cookie','document'))
    
    cookie = SimpleCookie()
    cookie.load(str(result))

      # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
      # which is incompatible with requests. Manually construct a dictionary instead.
    cookies = {}
    for key, morsel in cookie.items():
            cookies[key] = morsel.value
            
    cookies['__cfduid']=cook[0]['__cfduid']
    cookies['cf_clearance']=cook[0]['cf_clearance']
    cookies['google-adsenses']=key
    


    html=requests.get('https://www1.mehlizmovieshd.com/?custom7HDmehliz='+clean_name(original_title,1),cookies=cookies,headers=cook[1]).content

    regex='<div class="result-item"><article>.+?<div class="title"><a href="(.+?)">(.+?)<.+?"year">(.+?)<'
    match=re.compile(regex).findall(html)
    
    for link,title,year in match:

      if clean_name(original_title,1)==title and show_original_year==year:
         x=requests.get(link,cookies=cookies,headers=cook[1]).content
         regex='<div class="numerando">%s - %s</div><div class="episodiotitle"><a href="(.+?)"'%(season,episode)
         match2=re.compile(regex).findall(x)
 
         y=requests.get(match2[0],cookies=cookies,headers=cook[1]).content
         regex='<iframe.+?src="(.+?)"'
         match3=re.compile(regex).findall(y)
         for links in match3:
     
           if 'mehlizmovieshd.co' in links:
           
             z=requests.get(links,cookies=cookies,headers=cook[1]).content
             
             regex='file: "(.+?)",label: "(.+?)"'
             match4=re.compile(regex).findall(z)
             if len (match4)>0:
               all_links.append((original_title,match4[0][0],'Direct',match4[0][1]))
               links_gona=all_links
              
           else: 
               
                name1,match_s,res,check=server_data(links,original_title)
                
                if check :
                  all_links.append((name1,links,match_s,res))
                  links_gona=all_links
    return links_gona
def get_gonaw(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_gona
    if 'Agents Of S.h.i.e.l.d'.lower() in clean_name(original_title,1).lower():
         original_title='Agents%20Of%20S.h.i.e.l.d.'
                         
    all_links=[]
    if tv_movie=='tv':
      url='http://gonnawatch.com/search-movies/%s.html'%(original_title+'%20season%20'+season)
    else:
      url='http://gonnawatch.com/search-movies/%s.html'%original_title
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    #'Host': 'gonnawatch.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    html=requests.get(url,headers=headers).content
    if tv_movie=='tv':
        regex='<div class="titl(.+?)"><a href="(.+?)">(.+?): Season'
    else:
      regex='year">(.+?)<.+?div class="title"><a href="(.+?)">(.+?)<'
    match=re.compile(regex,re.DOTALL).findall(html)
    
   
    for year,link,title in match:
       if tv_movie=='tv':
         year=show_original_year

       if title.lower()==clean_name(original_title,1).lower() and year==show_original_year:
         
         x=requests.get(link,headers=headers).content
         if tv_movie=='tv':
           regex='a class="episode episode_series_link" href="(.+?)">(.+?)</a>'
           
           
           match6=re.compile(regex).findall(x)
           for link,episode_in in match6:
             if episode_in==episode:
            
               x=requests.get(link,headers=headers).content
         regex='class="server_play"><a href="(.+?)"'
         match4=re.compile(regex).findall(x)
         for links2 in match4:
          x=requests.get(links2,headers=headers).content
          regex='Base64.decode\("(.+?)"'
          match2=re.compile(regex).findall(x)
          if len(match2)>0:
            link1=match2[0].decode('base64')
            regex='src="(.+?)"'
            match3=re.compile(regex).findall(link1)
     
            try:
                
          
                if 'entervideo' in match3[0]:
                    y=requests.get(match3[0],headers=headers).content
                    regex='source src="(.+?)"'
                    f_link=re.compile(regex).findall(y)
                    
                    
                    names=f_link[0].split('/')
     
                    name1=names[len(names)-1]
                    if "1080" in name1:
                        res="1080"
                    elif "720" in name1:
                        res="720"
                    elif "480" in name1:
                        res="720"
                    elif "hd" in name1.lower():
                        res="HD"
                    else:
                       res=' '
                    headers2 = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Host': 'entervideo.net',
                    'Pragma': 'no-cache',
                    'Referer':match3[0],
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                    }
                    head=urllib.urlencode(headers2)
                    all_links.append((name1,f_link[0]+"|"+head,'Direct',res))
                    links_gona=all_links
                else:
                  
               
                        name1,match_s,res,check=server_data(match3[0],original_title)
                        if check :
                          all_links.append((name1,match3[0],match_s,res))
                          links_gona=all_links
            except:
             pass

          
          regex='<a title="Click here to Play on .+?" href="(.+?)"'
          match5=re.compile(regex).findall(x)

          if len(match5)>0:
                name1,match_s,res,check=server_data(match5[0],original_title)
                if check:
                  all_links.append((name1,match5[0],match_s,res))
                  links_gona=all_links
    return links_gona
def get_shuid(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_shu
    all_links=[]
    if tv_movie=='tv':
      url='http://shahid4u.tv/?s='+clean_name(original_title,1).replace(' ','+')+'+s'+season_n
    else:
      url='http://shahid4u.tv/?s='+clean_name(original_title,1).replace(' ','+')+'+'+show_original_year
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'shahid4u.tv',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    html=requests.get(url,headers=headers).content
    regex='"movief"><a href="(.+?)">(.+?)<'
    match=re.compile(regex).findall(html)
 

    for link,title in match:
      check=False
      if tv_movie=='movie':
       
        if show_original_year in title:
          check=True
 
      else:
      
        parts=title.split(" ")
        se=parts[len(parts)-1]
        if season==se:
          check=True
         

      if clean_name(original_title,1).lower() in title.lower().replace(':','') and check:
         x=requests.get(link+'?watch=1',headers=headers).content
  
         regex="data: '(.+?)'"
         match_q=re.compile(regex).findall(x)
         
         regex="url: '(.+?)'"
         match_ur=re.compile(regex).findall(x)
         for i in range (0,10):
            
            url=match_ur[0]+'?'+match_q[0]+str(i)

            y=requests.get(url,headers=headers).content
            regex='src="(.+?)"'
            match_f=re.compile(regex).findall(y)
            check=False
            name1,match_s,res,check=server_data(match_f[0],original_title)

            if check :
     
               all_links.append((name1,match_f[0],match_s,res))
               links_shu=all_links
    return links_shu
def get_kizi(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_kizi
    all_links=[]
    if tv_movie=='tv':
      url='https://www.kizi.video/search.php?keywords='+clean_name(original_title,1).replace(' ','+')+'+s'+season_n+'e'+episode_n
    else:
      url='https://www.kizi.video/search.php?keywords='+clean_name(original_title,1).replace(' ','+')+'+'+show_original_year
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    #'Host': 'www.kizi.video',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    html=requests.get(url,headers=headers).content
    regex='<div class="pm-video-thumb">.+?<a href="(.+?)" title="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(html)

    
    for link,title in match:
       check=False
       if tv_movie=='movie':
         if clean_name(original_title,1).lower() in title.lower().replace(':','') and show_original_year in title:
           check=True
       else:
         if clean_name(original_title,1).lower() in title.lower().replace(':','') and ('s%se%s'%(season_n,episode_n) in title.lower() or 'season %s episode %s'%(season_n,episode_n) in title.lower()):
           check=True

       if check:
         x=requests.get(link.replace('watch.php','view.php'),headers=headers).content
  
         regex='<iframe src="(.+?)"'
         match2=re.compile(regex).findall(x)
         y=requests.get(match2[0],headers=headers).content

         regex='file:"(.+?)"'
         match_l=re.compile(regex).findall(y)
         for links in match_l:
           all_links.append((original_title,links,'Direct',' '))
           links_kizi=all_links
           
         x=requests.get(link.replace('watch.php','download.php'),headers=headers).content
         regex='<iframe.+?src="(.+?)"'
         match3=re.compile(regex).findall(x)

         resolvable=resolveurl.HostedMediaFile(match3[0]).valid_url()
         name1,match_s,res,check=server_data(match3[0],original_title)
         
         if check and resolvable:
            all_links.append((name1,match3[0],match_s,res))
            links_kizi=all_links
    return links_kizi
def get_bmlink_str(new_link,match_id):
                 headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Host': 'streamvid.co',
                    'Pragma': 'no-cache',
                    'Referer': new_link,
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                 }
                 url=match_id
                 html=requests.get(url,headers=headers).content
              
                 from jsunpack import unpack
                 regex='JuicyCodes.Run\((.+?)\)'
                 match=re.compile(regex).findall(html)
                 regex='"(.+?)"'
                 match2=re.compile(regex).findall(match[0])
                 links_f=''
                 for items in match2:
                   links_f=links_f+items
                 final=links_f.decode('base64')
                 result2=unpack(final)
                 
                 regex='"src":"(.+?)"'
                 headers = {
                    'Accept': '*/*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Host': 'sirius.streamvid.co',
                    'Origin': 'https://streamvid.co',
                    'Pragma': 'no-cache',
                    'Referer': match_id,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                 }
                 url=re.compile(regex).findall(result2)[0]#.replace('video','720')
                 head=urllib.urlencode(headers)
                 #ht=requests.get(url,headers=headers).content

                 url=url+"|"+head
                 
                 if '1080' in result2:
                      res='1080'
                 elif '720' in result2:
                      res='720'
                 elif '480' in result2:
                      res='480'
                 elif '360' in result2:
                      res='360'
                 else:
                      res='HD'
                      
                 return url,res
def get_bmlink_drive(new_link,match_id):
                 headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Host': 'api-mov.com',
                    'Pragma': 'no-cache',
                    'Referer': new_link,
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                 }
                 url=match_id
                 html=requests.get(url,headers=headers).content
              
                 from jsunpack import unpack
                 regex='JuicyCodes.Run\((.+?)\)'
                 match=re.compile(regex).findall(html)
                 regex='"(.+?)"'
                 match2=re.compile(regex).findall(match[0])
                 links_f=''
                 for items in match2:
                   links_f=links_f+items
                 final=links_f.decode('base64')
                 result2=unpack(final)
         
                 regex='"file":"(.+?)","label":"(.+?)"'
                 match=re.compile(regex).findall(result2)
                 all_links_in=[]
                 for link,res in match:
                     headers = {
                        'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Host': 'express.api-mov.com',
                        
                        'Pragma': 'no-cache',
                        'Referer': match_id,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                     }
                    
                     head=urllib.urlencode(headers)
                     #ht=requests.get(url,headers=headers).content

                     link=link+"|"+head
                     all_links_in.append((link,res))
                 return all_links_in
def get_bmovie(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_bmovie
    all_links=[]
    if tv_movie=='tv':
      url='https://bmovies.film/ajaxsearch/search_suggestions/%s.html'%(clean_name(original_title,1)+'+season+'+season)
    else:
      url='https://bmovies.film/ajaxsearch/search_suggestions/%s.html'%(clean_name(original_title,1)+'+'+show_original_year)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'bmovies.film',
        'Pragma': 'no-cache',
        #'Referer': 'https://bmovies.film/search-query/the+matrix/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    
    

    response = requests.get(url, headers=headers).json()
    regex="<a href='(.+?)' class='ss-title'>(.+?)<"
    match=re.compile(regex).findall(response['content'])

    for link,name in match:
   
        if clean_name(original_title,1).lower() in name.lower().replace('&#039;',"'"):
             new_link=link+'watching.html/'
             x=requests.get(link+'watching.html/', headers=headers).content
    
             if tv_movie=='tv':
               regex='<a title="Episode %s: .+?" data-(.+?)="(.+?)"'%episode
               match_id_pre=re.compile(regex).findall(x)
               for type,link in match_id_pre:
   
                 if type.strip()=='strvid':
                   match_id=link
                   f_link,res=get_bmlink_str(new_link,match_id)
                   
                   all_links.append((original_title,f_link,'Direct',res))
                   links_bmovie=all_links
                 elif type.strip()=='drive':
                   match_id=link
                   f_links=get_bmlink_drive(new_link,match_id)
                   
                   for link,res in f_links:
                     all_links.append((original_title,link,'Direct',res.replace('P','')))
                     links_bmovie=all_links
                 else:
                   match_id=None
              
             else:
               regex=' data-(.+?)="(.+?)"'
               match_id_pre=re.compile(regex).findall(x)
               for type,link in match_id_pre:
                 
                 if type.strip()=='strvid':
                   match_id=link
                   f_link,res=get_bmlink_str(new_link,match_id)
                   
                   all_links.append((original_title,f_link,'Direct',res))
                   links_bmovie=all_links
                 elif type.strip()=='drive':
                   match_id=link
                   f_links=get_bmlink_drive(new_link,match_id)
                   
                   for link,res in f_links:
                     all_links.append((original_title,link,'Direct',res.replace('P','')))
                     links_bmovie=all_links
                 else:
                   match_id=None
             
             
                 
 
             if tv_movie=='tv':
               regex='<a title="Episode %s: .+?" data-.+?="(.+?)"'%episode
             else:
               regex=' data-.+?="(.+?)"'
             match2=re.compile(regex).findall(x)
             for links in match2:
               if 'streamvid' not in links and 'api-mov.com' not in links:
                     name1,match_s,res,check=server_data(links,original_title)
                     
                     resolvable=resolveurl.HostedMediaFile(links).valid_url()
                     if check and resolvable:
                        all_links.append((name1,links,match_s,res))
                        links_bmovie=all_links
    return links_bmovie
def get_1movie(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_1movie
    all_links=[]
    if tv_movie=='tv':
      url='http://1movies.biz/movies/search?s='+(clean_name(original_title,1).replace("Marvel's ",'')+'+season+'+season)
    else:
      url='http://1movies.biz/movies/search?s='+(clean_name(original_title,1)+'+'+show_original_year)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': '1movies.biz',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }

    html=requests.get(url,headers=headers).content
    regex='<div class="item_movie">.+?href="(.+?)" title="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(html)
    for link,name in match:
        check=False
        if tv_movie=='tv':
          if 'Season '+season in name:
            check=True
        else:
          if show_original_year in name:
            check=True

        if clean_name(original_title,1).lower().replace("marvel's ",'') in name.lower().replace('&#039;',"'") and check:
            x=requests.get(link,headers=headers).content
            if tv_movie=='tv':
                regex='<a href=".+?episode_id=(.+?)" class="">Episode %s</a>'%episode
      
                id=re.compile(regex).findall(x)[0]
            else:
                regex='load_player\((.+?)\);'
                id=re.compile(regex).findall(x)[0]
            headers1 = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': '1movies.biz',
                'Pragma': 'no-cache',
                'Referer': link,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'X-Requested-With': 'XMLHttpRequest',
            }
            url='http://1movies.biz/ajax/movie/load_player_v3?id='+id
            x=requests.get(url,headers=headers1).json()
            headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'play.1movies.biz',
            'Origin': 'http://1movies.biz',
            'Pragma': 'no-cache',
            'Referer': link,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            }

            y=requests.get('http:'+x['value'],headers=headers).json()
            if 'playlist' not in y:
                url='http://1movies.biz/ajax/movie/load_player_v3?retry=2&id='+id
                x=requests.get(url,headers=headers1).json()
                y=requests.get('http:'+x['value'],headers=headers).json() 
            url=y['playlist'][0]['file']
            name1=original_title
            res=' '
            if 'tracks' in y:
               if len(y['tracks'])>0:
                 if 'file' in y['tracks'][0]:
                  names=y['tracks'][0]['file'].split('/')
                  name1=names[len(names)-1].replace('.vtt','')
                  if '1080' in name1:
                      res='1080'
                  elif '720' in name1:
                      res='720'
                  elif '480' in name1:
                      res='480'
                  elif '360' in name1:
                      res='360'
                  else:
                      res='HD'
                      

            new_file=url
            if '.m3u8' in url:
              responce,cook=cloudflare.request(url)
  
              subfixs=url.rsplit('/', 1)[1]
             
              subflix=url.replace(subfixs,'')
            
              regex='URI="(.+?)"'
              match=re.compile(regex).findall(responce)
              responce,cook=cloudflare.request(match[0])
              f_data=responce.replace("BYTERANGE",'TARGETDURATION')
              f_data=f_data.replace("seg-",subflix+'seg-')
              new_file=os.path.join(user_dataDir ,'new.m3u8')
              try:
                xbmcvfs.delete(new_file)
              except:
               pass
              with open(new_file, "w") as text_file:
                    text_file.write(f_data)
            all_links.append((name1,new_file,'Direct',res))
            links_1movie=all_links
    return links_1movie
def get_scnsrc(tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id):
    global links_scn,stop_all
    all_links=[]
    if tv_movie=='tv':
      url='http://www.scnsrc.me/?s=%s'%(original_title.replace("Marvel's ",'').replace("%20","+")+'%20s'+season_n+'e'+episode_n)
    else:
      url='http://www.scnsrc.me/?s=%s'%(original_title.replace("%20","+")+'+'+show_original_year)
    import cfscrape
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.scnsrc.me',
    'Pragma': 'no-cache',
    'Referer': 'http://www.scnsrc.me/author/fatslave/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    #tk,cook,html=cfscrape.get_content(url,headers=headers)

    tk,cook=cache.get(cfscrape.get_content,3,'http://www.scnsrc.me/?s=The+Flash%20s04e04',30,headers, table='cookies')
 
    html=requests.get(url,headers=headers,cookies=tk).content
    if 'jschl-answer' in html:
      tk,cook=cache.get(cfscrape.get_content,0,'http://www.scnsrc.me/?s=The+Flash%20s04e04',30,headers, table='cookies')
      html=requests.get(url,headers=headers,cookies=tk).content
    #html,cook=cloudflare.request(url,headers=headers)
    regex='<h2> <a href="(.+?)" rel="bookmark" title="(.+?)"><u>'
    match=re.compile(regex).findall(html)


    
    for link,title in match:
      if stop_all==1:
        break
      title=title.replace("</u>",'').replace("<u>",'').replace("  ",' ').replace("."," ").replace("'","")
     
      if tv_movie=='tv':
        if 'S%sE%s '%(season_n,episode_n) in title:
         check=True
      else:
         if show_original_year in title :
           check=True
      if clean_name(original_title,1) in title and check==True:
  
          x=requests.get(link,headers=headers,cookies=tk).content
          regex="<div class='comm_content'><p><strong>(.+?)</p><p>(.+?)</div>"
          match_pre=re.compile(regex).findall(x)
          for name,cont in match_pre:
              regex='<a href="(.+?)" rel="nofollow"'
              match2=re.compile(regex).findall(cont)
              if stop_all==1:
                break
              for links in match2:
                  if 'imgur.com' not in links:
                    name1,match_s,res,check=server_data(links,original_title)
                    names2=links.split('/')
                    name2=names2[len(names2)-1].replace('.mkv','').replace('.mp4','').replace('.avi','').replace('.html','')
                    if stop_all==1:
                      break
                    resolvable=resolveurl.HostedMediaFile(links).valid_url()
               
                    if check and resolvable:
                        all_links.append((name2,links,match_s,res))
                        links_scn=all_links
                    
    return links_scn
def c_get_sources(name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,get_local=False):
    global links_reqzone,links_ftp,links_tvl,silent_mode,link_onitube,link_filepursuit,link_2ddl,links_jksp,links_uni,links_linkia,links_sdarot,link_ct,imdb_global,all_magnet,links_m4u,rd_tvr,link_dlt,links_pf,all_subs,link_afdah,link_seehd,sources_a,link_cin,links_list2,links_list,links_sno,links_fun,links_mx,link_upto,link_direct,stop_all,links_we,links_dwatch,links_cmovies,links_flix,link_showbox,link_daily,link_source1,match_a,match,link_hdonline,link_dl20,cooltvzion,link_ava,link_tmp,links_1movie,next_p_all,link_goo,links_sc,links_seil,links_put
    
    if Addon.getSetting("trailer_dp")=="true":
      pDialog = xbmcgui.DialogProgressBG()
      pDialog.create('אוסף מקורות')
      #pDialog.update(0, message=' אנא המתן ')

    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
   
    if Addon.getSetting("lang")=="1":
      lang='en'
    else:
      lang='he'
    url2=None
    if season!=None and season!="%20":
          tv_movie='tv'
      
          url=domain_s+'pron.tv/stream/%s'%(urllib.quote_plus(original_title)+"%20S"+season_n+'E'+episode_n)+"%20"+'lang%3A'+lang
          url2=domain_s+'api.dailymotion.com//videos?fields=available_formats,description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search=%s&sort=relevance&limit=100&family_filter=1'%((original_title.replace(" ","%20"))+"%20S"+season_n+'E'+episode_n)
    else:
          tv_movie='movie'
        
          url=domain_s+'pron.tv/stream/%s'%(urllib.quote_plus(original_title)+"%20"+year)+"%20"+'lang%3A'+lang
          url2=domain_s+'api.dailymotion.com//videos?fields=available_formats,description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search=%s&sort=relevance&limit=100&family_filter=1'%(original_title.replace(" ","%20")+"%20"+year)
    
    
    
    
    thread=[]
    tv_mode=tv_movie
    
    original_title=original_title.replace('%3a','')
    if Addon.getSetting("trailer_dp")=="true":
      thread.append(Thread(play_trailer_f(id,tv_mode)))
    if Addon.getSetting("2ddl")=='true'  and isr==0 and rd_sources=='true' :
        thread.append(Thread(get_2ddl,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("afdah")=='true'  and url2!=None and isr==0 and  tv_mode=='movie':
       thread.append(Thread(get_afdah,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("seehd")=='true'  and url2!=None and isr==0:
       thread.append(Thread(get_seehd,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("upto")=='true'  and url2!=None and isr==0:
       thread.append(Thread(get_upto,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("dire")=='true'  and url2!=None and isr==0 :
       thread.append(Thread(get_direct_links,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("we")=='true'  and url2!=None and isr==0 and  tv_mode=='tv':
       thread.append(Thread(get_we,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("cmovies")=='true'  and url2!=None and isr==0:
       thread.append(Thread(get_cmovies,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
       
    if Addon.getSetting("DW")=='true'  and url2!=None and isr==0  and  tv_mode=='movie':
       thread.append(Thread(get_dwatch,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
   
    if Addon.getSetting("flix")=='true'  and url2!=None and isr==0:
       thread.append(Thread(get_flix,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("put")=='true'  and url2!=None and isr==0:
       thread.append(Thread(get_put,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("sil")=='true'  and url2!=None  and  tv_mode=='movie':
       thread.append(Thread(get_seretil,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("sc")=='true'  and url2!=None :
      thread.append(Thread(get_sc,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("tmp")=='true'  and url2!=None and isr==0:
      thread.append(Thread(get_tmp,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("ava")=='true'  and url2!=None and isr==0:
      thread.append(Thread(get_ava,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("cooltvzion")=='true'  and url2!=None and isr==0  and  tv_mode=='tv':
      thread.append(Thread(get_cooltvzion,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("dl20")=='true'  and url2!=None and isr==0:
      thread.append(Thread(get_dl20,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("hdonline")=='true'  and url2!=None and isr==0:
      thread.append(Thread(get_hdonline,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("showbox")=='true'  and url2!=None and isr==0 and  tv_mode=='tv':
      thread.append(Thread(get_showbox,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("daily")=='true' and url2!=None:
      thread.append(Thread(get_daily,url2,original_title,season_n,episode_n,season,episode))
    if Addon.getSetting("sp")=='true' and url2!=None:
      thread.append(Thread(get_sp,original_title,heb_name,season,episode))
    if Addon.getSetting("gos")=='true' and url2!=None and isr==0:
      thread.append(Thread(get_goo,tv_movie,original_title,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("cin")=='true' and isr==0  and  tv_mode=='tv':
      thread.append(Thread(get_cin,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("pf")=='true' and isr==0  :
      thread.append(Thread(get_pf,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("dlt")=='true' and isr==0 and  tv_mode=='movie' :
      thread.append(Thread(get_dlt,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("rd_tvr")=='true' and isr==0  and rd_sources=='true':
      thread.append(Thread(get_rd_tvr,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("m4u")=='true' and isr==0  :
      thread.append(Thread(get_m4u,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    
    if Addon.getSetting("magnet")=='true' and isr==0 :
       thread.append(Thread(get_magnet,tv_movie,original_title,season,episode,id,show_original_year))
       
    if Addon.getSetting("movix")=='true' and  tv_mode=='movie':
       thread.append(Thread(get_movix,original_title,name,show_original_year,'no'))
    if Addon.getSetting("fun")=='true' and  tv_mode=='movie':
       thread.append(Thread(get_funlopy,original_title,name,show_original_year,'no'))
    if Addon.getSetting("snow")=='true' and  tv_mode=='movie':
       thread.append(Thread(get_serno,original_title,name,show_original_year,'no'))
    if isr==0 :
      thread.append(Thread(get_subs,tv_movie,original_title,season,episode,id,show_original_year))
      
    if Addon.getSetting("ct")=='true' and  tv_mode=='tv':
       thread.append(Thread(get_ct,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("sd")=='true' and  tv_mode=='tv':
       thread.append(Thread(get_sdarot,tv_movie,original_title,heb_name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("lk")=='true'  and isr==1:
       thread.append(Thread(get_linkia,tv_movie,original_title,heb_name,season_n,episode_n,season,episode,show_original_year))
    if Addon.getSetting("uni")=='true'  and isr==0:
        thread.append(Thread(get_uni,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id)) 
    if Addon.getSetting("filep")=='true'  and isr==0:
        thread.append(Thread(get_filepursuit,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id)) 
    if Addon.getSetting("onitube")=='true'  and isr==0:
        thread.append(Thread(get_onitube,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id)) 
    if Addon.getSetting("list")=='true' and  tv_mode=='movie':
       thread.append(Thread(search_lists,original_title,heb_name,show_original_year,id))
    if Addon.getSetting("tvl")=='true'  and  tv_mode=='tv' and isr==0:
        thread.append(Thread(get_tvl,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id)) 
    if Addon.getSetting("ftp")=='true'  and isr==0:
        thread.append(Thread(get_ftp,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("req")=='true'  and isr==0:
        thread.append(Thread(get_raqlink,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("movisk")=='true'  and isr==0 and  tv_mode=='tv':
        thread.append(Thread(get_links_moviesak,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("get")=='true'  and isr==0 :
        thread.append(Thread(get_gonaw,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("su")=='true'  and isr==0 :
        thread.append(Thread(get_shuid,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("kizi")=='true'  and isr==0 :
        thread.append(Thread(get_kizi,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("bmovie")=='true'  and isr==0 :
        thread.append(Thread(get_bmovie,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("1movie")=='true'  and isr==0 :
        thread.append(Thread(get_1movie,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if Addon.getSetting("scn")=='true'  and isr==0 and rd_sources=='true' :
        thread.append(Thread(get_scnsrc,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
        
    title_size=0
    start_time = time.time()
    stop_all=0
    
    for td in thread:
      td.start()
      #td.join()
    max_time=int(Addon.getSetting("time_s"))
    if Addon.getSetting("dp")=='true' and silent_mode==False:
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','מחפש מקורות', '','')
        dp.update(0, 'אנא המתן','מחפש מקורות', '' )
    num_live=0
    tt={}
    for i in range (0,40): 
      tt[i]="red"

    
    string_dp=''
    string_dp2=''
    still_alive=0
    while 1:
         num_live=0
         
          
         
         elapsed_time = time.time() - start_time
         if Addon.getSetting("dp")=='true' and silent_mode==False:
             dp.update(int(((num_live* 100.0)/(len(thread))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),string_dp, string_dp2)
         for threads in thread:
              num_live=0
              string_dp=''
              string_dp2=''
              still_alive=0
              count_1080=0
              count_720=0
              count_480=0
              count_rest=0
              for yy in range(0,len(thread)):
                if not thread[yy].is_alive():
                  num_live=num_live+1
                  tt[yy]="lightgreen"
                else:
                  still_alive=1
                  tt[yy]="red"
              all_links_togther=links_scn+links_bmovie+links_kizi+links_shu+links_gona+links_moviesak+links_reqzone+links_ftp+links_tvl+link_onitube+link_filepursuit+link_2ddl+links_jksp+links_uni+links_linkia+links_sdarot+link_ct+links_m4u+rd_tvr+link_dlt+links_pf+link_afdah+link_seehd+sources_a
              all_links_togther+=link_cin+links_list2+links_list+links_sno+links_fun+links_mx+link_upto+link_direct+links_we+links_dwatch
              all_links_togther+=links_cmovies+links_flix+link_showbox+link_daily+link_source1+link_hdonline+link_dl20+cooltvzion+link_ava+link_tmp+links_1movie+next_p_all+link_goo+links_sc+links_seil+links_put
     
              for data in all_links_togther:
                 
                 name1,links,server,res=data
                 
                 if res=='1080':
                   count_1080+=1
                 elif res=='720':
                   count_720+=1
                 elif res=='480':
                   count_480+=1
                 else:
                   count_rest+=1
              if Addon.getSetting("trailer_dp")=="true":
                string_dp="1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]"%(count_1080,count_720,count_480,count_rest)
                pDialog.update(int(((num_live* 100.0)/(len(thread))) ), message=time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+' '+string_dp)
              if Addon.getSetting("dp")=='true' and silent_mode==False:
                  zz=0
                  if isr==0:
                    string_dp=string_dp+('[COLOR gold]SUBS:%s[/COLOR]-'%(len( all_subs)))
                  if Addon.getSetting("2ddl")=='true' and isr==0 and rd_sources=='true' :
                  
                     string_dp=string_dp+('2DL:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_2ddl)))
                     zz=zz+1
                  if Addon.getSetting("afdah")=='true' and isr==0 and  tv_mode=='movie':
                  
                     string_dp=string_dp+('Af:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_afdah)))
                     zz=zz+1
                  
             
                  if Addon.getSetting("seehd")=='true' and isr==0:
                  
                     string_dp=string_dp+('SH:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_seehd)))
                     zz=zz+1
                  if Addon.getSetting("upto")=='true' and isr==0:
                  
                     string_dp=string_dp+('UP:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_upto)))
                     zz=zz+1
                  if Addon.getSetting("dire")=='true' and isr==0:
                  
                     string_dp=string_dp+('DI:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_direct)))
                     zz=zz+1
                  
                  
                  if Addon.getSetting("we")=='true' and isr==0 and  tv_mode=='tv':
                  
                     string_dp=string_dp+('WE:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_we)))
                     zz=zz+1
                  
                  
                  if Addon.getSetting("DW")=='true' and isr==0 and  tv_mode=='movie':
                  
                     string_dp=string_dp+('DW:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_dwatch)))
                     zz=zz+1
                  
                  
                  if Addon.getSetting("cmovies")=='true' and isr==0 and  tv_mode=='movie':
                  
                     string_dp=string_dp+('CM:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_cmovies)))
                     zz=zz+1
                  if Addon.getSetting("flix")=='true' and isr==0:
                  
                     string_dp=string_dp+('FL:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_flix)))
                     zz=zz+1
                  if Addon.getSetting("put")=='true' and isr==0:
                  
                     string_dp=string_dp+('PU:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_put)))
                     zz=zz+1
                  if Addon.getSetting("sil")=='true' and  tv_mode=='movie':
                     string_dp=string_dp+('SI:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_seil)))
                     zz=zz+1
                     
                  if Addon.getSetting("sc")=='true':
                     string_dp=string_dp+('SC:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_sc)))
                     zz=zz+1
                  if Addon.getSetting("tmp")=='true' and isr==0:
                     string_dp=string_dp+('LV:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_tmp)))
                     zz=zz+1
                  if Addon.getSetting("cooltvzion")=='true' and isr==0 and  tv_mode=='tv':
                    string_dp=string_dp+('TV:[COLOR %s]%s[/COLOR]'%(tt[zz],len( cooltvzion)))
                    zz=zz+1
                  if Addon.getSetting("ava")=='true' and isr==0:
                    string_dp=string_dp+('AV:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_ava)))
                    zz=zz+1
                  if Addon.getSetting("dl20")=='true' and isr==0:
                    string_dp=string_dp+('DL:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_dl20)))
                    zz=zz+1
                  if Addon.getSetting("hdonline")=='true' and isr==0:
                    string_dp=string_dp+('HO:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_hdonline)))
                    zz=zz+1
                  if Addon.getSetting("showbox")=='true' and isr==0 and  tv_mode=='tv':
                    string_dp2=string_dp2+('SB:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_showbox)))
                    zz=zz+1
                  if Addon.getSetting("daily")=='true':
                    string_dp2=string_dp2+('DA:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_daily)))
                    zz=zz+1
                  if Addon.getSetting("sp")=='true':
                    string_dp2=string_dp2+('SP:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_source1)))
                    zz=zz+1
                  if Addon.getSetting("gos")=='true' and isr==0:
                    string_dp2=string_dp2+('GO:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_goo)))
                    zz=zz+1
                  if Addon.getSetting("cin")=='true' and isr==0 and  tv_mode=='tv':
                   string_dp2=string_dp2+('CI:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_cin)))
                   zz=zz+1
                   
                  if Addon.getSetting("pf")=='true' and isr==0 :
                   string_dp2=string_dp2+('PF:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_pf)))
                   zz=zz+1
                  
                  if Addon.getSetting("dlt")=='true' and isr==0 :
                   string_dp2=string_dp2+('DLT:[COLOR %s]%s[/COLOR]'%(tt[zz],len( link_dlt)))
                   zz=zz+1
                   
                  
                  if Addon.getSetting("rd_tvr")=='true' and isr==0 and rd_sources=='true' :
                   string_dp2=string_dp2+('RD:[COLOR %s]%s[/COLOR]'%(tt[zz],len( rd_tvr)))
                   zz=zz+1

                  if Addon.getSetting("m4u")=='true' and isr==0  :
                   string_dp2=string_dp2+('M4:[COLOR %s]%s[/COLOR]'%(tt[zz],str(len( links_m4u))))
                   zz=zz+1
                   
                  if Addon.getSetting("movix")=='true' and  tv_mode=='movie' :
                       string_dp2=string_dp2+('MX:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_mx)))
                       zz=zz+1
                  if Addon.getSetting("fun")=='true' and  tv_mode=='movie'  and isr==1:
                       string_dp2=string_dp2+('Fu:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_fun)))
                       zz=zz+1

                  if Addon.getSetting("snow")=='true' and  tv_mode=='movie'  and isr==1:
                       string_dp2=string_dp2+('Sn:[COLOR %s]%s[/COLOR]'%(tt[zz],len( links_sno)))
                       zz=zz+1
                  if Addon.getSetting("ct")=='true' and  tv_mode=='tv' :
                       
                       string_dp2=string_dp2+('Ct:[COLOR %s]'%tt[zz]+str(len( link_ct))+'[/COLOR]')
                       zz=zz+1
                  if Addon.getSetting("sd")=='true' and  tv_mode=='tv' :
                       
                       string_dp2=string_dp2+('Sd:[COLOR %s]'%tt[zz]+str(len( links_sdarot))+'[/COLOR]')
                       zz=zz+1
                  if Addon.getSetting("lk")=='true'  and isr==1:
                       
                       string_dp2=string_dp2+('Lk:[COLOR %s]'%tt[zz]+str(len( links_linkia))+'[/COLOR]')
                       zz=zz+1
                  if Addon.getSetting("uni")=='true'  and isr==0:
                       
                       string_dp2=string_dp2+('Uni:[COLOR %s]'%tt[zz]+str(len( links_uni))+'[/COLOR]')
                       zz=zz+1
                  if Addon.getSetting("filep")=='true'  and isr==0:
                       
                       string_dp2=string_dp2+('FP:[COLOR %s]'%tt[zz]+str(len( link_filepursuit))+'[/COLOR]')
                       zz=zz+1
                  if Addon.getSetting("onitube")=='true'  and isr==0:
                       
                       string_dp2=string_dp2+('ONI:[COLOR %s]'%tt[zz]+str(len( link_onitube))+'[/COLOR]')
                       zz=zz+1
                  if Addon.getSetting("list")=='true' and  tv_mode=='movie':
                     string_dp2=string_dp2+('FA:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_list)))
                     zz=zz+1
                  if Addon.getSetting("tvl")=='true' and  tv_mode=='tv':
                     string_dp2=string_dp2+('TL:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_tvl)))
                     zz=zz+1
                  if Addon.getSetting("ftp")=='true':
                     string_dp2=string_dp2+('FT:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_ftp)))
                     zz=zz+1
                  if Addon.getSetting("req")=='true':
                     string_dp2=string_dp2+('RE:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_reqzone)))
                     zz=zz+1
                  if Addon.getSetting("movisk")=='true' and  tv_mode=='tv':
                     string_dp2=string_dp2+('MK:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_moviesak)))
                     zz=zz+1
                  if Addon.getSetting("get")=='true':
                     string_dp2=string_dp2+('GE:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_gona)))
                     zz=zz+1
                  if Addon.getSetting("su")=='true':
                     string_dp2=string_dp2+('SU:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_shu)))
                     zz=zz+1
                  if Addon.getSetting("kizi")=='true':
                     string_dp2=string_dp2+('KZ:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_kizi)))
                     zz=zz+1
                  if Addon.getSetting("bmovie")=='true':
                     string_dp2=string_dp2+('BV:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_bmovie)))
                     zz=zz+1
                  if Addon.getSetting("1movie")=='true':
                     string_dp2=string_dp2+('1M:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_1movie)))
                     zz=zz+1
                  
                  if Addon.getSetting("scn")=='true' and rd_sources=='true' :
                     string_dp2=string_dp2+('1M:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_scn)))
                     zz=zz+1
                  
                  if Addon.getSetting("simple_d")=='true':
                    string_dp2=('[COLOR gold]SUBS:%s[/COLOR]-'%(len( all_subs)))
                    string_dp="1080: [COLOR khaki]%s[/COLOR] 720: [COLOR gold]%s[/COLOR] 480: [COLOR silver]%s[/COLOR] Rest: [COLOR burlywood]%s[/COLOR]"%(count_1080,count_720,count_480,count_rest)
                  if Addon.getSetting("dp")=='true' and silent_mode==False:
                      dp.update(int(((num_live* 100.0)/(len(thread))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),string_dp, string_dp2)
                  xbmc.sleep(100)
                  
         if still_alive==0:
           break
         if Addon.getSetting("dp")=='true' and silent_mode==False:
           if dp.iscanceled():
             dp_c=True
           else:
             dp_c=False
         else:
           dp_c=False
         if dp_c or elapsed_time>max_time: 
           for threads in thread:
             if threads.is_alive():
                 stop_all=1
                 threads._Thread__stop()
         xbmc.sleep(1000)
    if Addon.getSetting("trailer_dp")=="true":
      xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'חיפוש מקורות הסתיים')).encode('utf-8'))
      pDialog.close()
    if Addon.getSetting("dp")=='true' and silent_mode==False:
      dp.close()
    all_1=[link_cin,link_upto,link_direct,links_we,links_dwatch,links_cmovies,links_flix,links_put,links_seil,links_sc,links_1movie,link_goo,link_tmp,link_ava,cooltvzion,link_dl20,link_hdonline,link_showbox,link_source1,match_a]
    
    return links_scn,links_bmovie,links_kizi,links_shu,links_gona,links_moviesak,links_reqzone,links_ftp,links_tvl,link_onitube,link_filepursuit,link_2ddl,links_jksp,links_uni,links_linkia,links_sdarot,link_ct,imdb_global,all_magnet,links_m4u,rd_tvr,link_dlt,links_pf,all_subs,link_afdah,link_seehd,sources_a,link_cin,links_list2,links_list,links_sno,links_fun,links_mx,link_upto,link_direct,stop_all,links_we,links_dwatch,links_cmovies,links_flix,link_showbox,link_daily,link_source1,match_a,match,link_hdonline,link_dl20,cooltvzion,link_ava,link_tmp,links_1movie,next_p_all,link_goo,links_sc,links_seil,links_put
def check_pre(saved_name,all_subs):
       release_names=['bluray','hdtv','dvdrip','bdrip','web-dl']
       array_original=list(saved_name)
       array_original=[line.strip().lower() for line in array_original]
       array_original=[(x) for x in array_original if x != '']
       highest=0
       for items in all_subs:
           array_subs=list(items)
          
           array_subs=[line.strip().lower() for line in array_subs]
           array_subs=[str(x).lower() for x in array_subs if x != '']
           
     
           for item_2 in release_names:
           
            if item_2 in array_original and item_2 in array_subs:
              array_original.append(item_2)
              array_original.append(item_2)
              array_original.append(item_2)
              array_subs.append(item_2)
              array_subs.append(item_2)
              array_subs.append(item_2)
    
     
           precent=similar(array_original,array_subs)
          
           if precent>=highest:
             highest=precent
       return highest
def save_fav(id,tv_movie):
   if tv_movie=='tv':
     save_file=os.path.join(user_dataDir,"fav_tv.txt")
   else:
     save_file=os.path.join(user_dataDir,"fav_movie.txt")
   file_data=[]
   change=0

   
   if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
   if len(file_data)>150:
       for i in range (len(file_data)-1,0,-1):
         if (i<(len(file_data)-100)) and len(file_data[i])>0:
          file_data.pop(i)
          change=1
       for i in range (len(file_data)-1,0,-1):
         
         if len(file_data[i])<3:
          
          file_data.pop(i)
          change=1

   if id not in file_data or change==1:
      for i in range (len(file_data)-1,0,-1):
         file_data[i]=file_data[i].replace('\n','')
         if len(file_data[i])<3:
          
          file_data.pop(i)
       
      if id not in file_data:
        file_data.append(id)
      file = open(save_file, 'w')
      file.write('\n'.join(file_data))
      file.close()
def get_sources(name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates='',get_local=False):
    name=name.replace('[COLOR red]','').replace('[COLOR white]','').replace('[/COLOR]','')
    o_year=year
    
    if plot==None:
      plot=' '
    if '-פרק ' in plot:
        
        all_d=json.loads(urllib.unquote_plus(dates))
        if all_d[0]==0:
          choise=['נגן את הפרק הבא - '+all_d[2],'נגן פרק נוכחי - '+all_d[1],'פתח את פרקי העונה','פתח את בחירת העונה']
        elif all_d[2]==0:
          choise=['נגן פרק נוכחי - '+all_d[1],'נגן פרק קודם - '+all_d[0],'פתח את פרקי העונה','פתח את בחירת העונה']
        else:
          if 'magenta' not in all_d[2]:
             choise=['נגן את הפרק הבא - '+all_d[2],'נגן פרק נוכחי - '+all_d[1],'נגן פרק קודם - '+all_d[0],'פתח את פרקי העונה','פתח את בחירת העונה']
          else:
             choise=['[COLOR magenta]'+'נגן את הפרק הבא - '+'[/COLOR]'+all_d[2],'נגן פרק נוכחי - '+all_d[1],'נגן פרק קודם - '+all_d[0],'פתח את פרקי העונה','פתח את בחירת העונה']
        ret = xbmcgui.Dialog().select("בחר פרק", choise)
        if ret!=-1:
         
            if all_d[2]==0:
              prev_index=1
            else:
              prev_index=2
            if ret==0 and all_d[2]!=0:
              episode=str(int(episode)+1)
            if ret==prev_index:
              if int(episode)>1:
                episode=str(int(episode)-1)
            if ret==(prev_index+1):
                get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr)
                return 0
            if ret==(prev_index+2):
                get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr)
                return 0
        else:
          sys.exit()
    
    global links_scn,links_bmovie,links_kizi,links_shu,links_gona,search_done,links_moviesak,links_reqzone,links_ftp,links_tvl,link_onitube,link_filepursuit,link_2ddl,links_jksp,links_uni,links_linkia,links_sdarot,link_ct,imdb_global,all_magnet,links_m4u,rd_tvr,link_dlt,links_pf,all_subs,link_afdah,link_seehd,sources_a,link_cin,links_list2,links_list,links_sno,links_fun,links_mx,link_upto,link_direct,stop_all,links_we,links_dwatch,links_cmovies,links_flix,link_showbox,link_daily,link_source1,match_a,match,link_hdonline,link_dl20,cooltvzion,link_ava,link_tmp,links_1movie,next_p_all,link_goo,links_sc,links_seil,links_put
    time_to_save=int(Addon.getSetting("save_time"))
    search_done=0
    #c_get_sources(name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr)
    o_name=name
    
    try:
      if season!=None and season!="%20":
        name=original_title
      data1=((name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr))
  
      links_scn,links_bmovie,links_kizi,links_shu,links_gona,links_moviesak,links_reqzone,links_ftp,links_tvl,link_onitube,link_filepursuit,link_2ddl,links_jksp,links_uni,links_linkia,links_sdarot,link_ct,imdb_global,all_magnet,links_m4u,rd_tvr,link_dlt,links_pf,all_subs,link_afdah,link_seehd,sources_a,link_cin,links_list2,links_list,links_sno,links_fun,links_mx,link_upto,link_direct,stop_all,links_we,links_dwatch,links_cmovies,links_flix,link_showbox,link_daily,link_source1,match_a,match,link_hdonline,link_dl20,cooltvzion,link_ava,link_tmp,links_1movie,next_p_all,link_goo,links_sc,links_seil,links_put= cache.get(c_get_sources, time_to_save, name,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr, table='pages')
      a=1
    except Exception as e:
      ClearCache()
      logging.warning(e)
      xbmcgui.Dialog().ok('Error occurred','קאש נוקה נסה שוב')
      
      sys.exit()
    #xbmc.Player().stop()
    all_data=[]
    video_data={}
    video_data['title']=name
    video_data['poster']=image
    video_data['plot']=plot
    video_data['icon']=icon
    video_data['year']=year
    if plot==None:
      plot=' '
    if len(episode)==1:
      episode_n="0"+episode
    else:
       episode_n=episode
    if len(season)==1:
      season_n="0"+season
    else:
      season_n=season
   
    if Addon.getSetting("lang")=="1":
      lang='en'
    else:
      lang='he'
    url2=None
    if season!=None and season!="%20":
       tv_movie='tv'
       if 'page=' not in url or 'www.alluc.ee' not in url:
          url=domain_s+'pron.tv/stream/%s'%(urllib.quote_plus(original_title)+"%20S"+season_n+'E'+episode_n)+"%20"+'lang%3A'+lang
          url2=domain_s+'api.dailymotion.com//videos?fields=available_formats,description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search=%s&sort=relevance&limit=100&family_filter=1'%((original_title.replace(" ","%20"))+"%20S"+season_n+'E'+episode_n)
    else:
        tv_movie='movie'
        if 'page=' not in url or 'www.alluc.ee' not in url:
          url=domain_s+'pron.tv/stream/%s'%(urllib.quote_plus(original_title)+"%20"+video_data['year'])+"%20"+'lang%3A'+lang
          url2=domain_s+'api.dailymotion.com//videos?fields=available_formats,description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search=%s&sort=relevance&limit=100&family_filter=1'%(original_title.replace(" ","%20")+"%20"+video_data['year'])
    save_fav(id,tv_movie)
    if tv_movie=='tv':
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' and type='%s' and season='%s' and episode='%s'"%(original_title.replace("'"," "),tv_movie,season,episode))

        match = dbcur.fetchone()
        if match==None:
          
          dbcur.execute("INSERT INTO AllData Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),url,icon,image,plot.replace("'"," "),year,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,heb_name.replace("'"," "),isr,tv_movie))
          dbcon.commit()
          
        dbcur.execute("SELECT * FROM Lastepisode WHERE original_title = '%s' and type='%s'"%(original_title.replace("'"," "),tv_movie))

        match = dbcur.fetchone()
        if match==None:
          
          dbcur.execute("INSERT INTO Lastepisode Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),url,icon,image,plot.replace("'"," "),year,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,heb_name.replace("'"," "),isr,tv_movie))
          dbcon.commit()
         
        else:
          
          dbcur.execute("UPDATE Lastepisode SET season='%s',episode='%s',image='%s' WHERE original_title = '%s' and type='%s'"%(season,episode,image,original_title.replace("'"," "),tv_movie))
          dbcon.commit()
        
    else:
        dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' and type='%s'"%(original_title.replace("'"," "),tv_movie))

        match = dbcur.fetchone()
        if match==None:
          
          dbcur.execute("INSERT INTO AllData Values ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s','%s','%s');" %  (name.replace("'"," "),url,icon,image,plot.replace("'"," "),year,original_title.replace("'"," "),season,episode,id,eng_name.replace("'"," "),show_original_year,heb_name.replace("'"," "),isr,tv_movie))
          dbcon.commit()
        #else:
          
        #  dbcur.execute("UPDATE AllData SET season='%s',episode='%s' WHERE original_title = '%s' and type='%s'"%(season,episode,original_title,tv_movie))
        #  dbcon.commit()
        links_scn
    for name,link,server,quality in links_scn:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-SCN-'
           all_data.append(('[COLOR grey][BV] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_bmovie:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-BV-'
           all_data.append(('[COLOR blue][BV] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_kizi:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-KIZI-'
           all_data.append(('[COLOR lightcoral][KZ] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
        
    for name,link,server,quality in links_shu:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-SHU-'
           all_data.append(('[COLOR palegreen][SU] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_gona:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-GE-'
           all_data.append(('[COLOR teal][GE] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_moviesak:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-MK-'
           all_data.append(('[COLOR orchid][MK] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_reqzone:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-REQ-'
           all_data.append(('[COLOR olivedab][REQ] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_ftp:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
           se='-FTP-'
           all_data.append(('[COLOR sandybrown][FTP] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_tvl:
           fixed_q=fix_q(quality)
           pre='101'
           se='-TVL-'
           all_data.append(('[COLOR magenta][TVL] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in links_list:
           fixed_q=fix_q(quality)
           pre='101'
           se='-FA-'
           all_data.append(('[COLOR khaki][FA] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
           
    for name,link,server,quality in link_onitube:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-ONI-'
           all_data.append(('[COLOR darkgray][ONI] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in link_filepursuit:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-FP-'
           all_data.append(('[COLOR olive][FP] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in link_2ddl:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-2Dl-'
           all_data.append(('[COLOR olive][2Dl] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in links_uni:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-UNI-'
           all_data.append(('[COLOR seagreen][Uni] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in links_linkia:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-LK-'
           all_data.append(('[COLOR dodgerblue][Lk] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in links_sdarot:
           fixed_q=fix_q(quality)
           #pre=check_pre(name,all_subs)
           pre=101
           se='-Sdarot-'
           all_data.append(('[COLOR cadetblue][Sd] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in link_ct:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-Ct-'
           all_data.append(('[COLOR gainsboro][Ct] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in links_mx:
           fixed_q=fix_q(quality)
           #pre=check_pre(name,all_subs)
           pre=101
           se='-Mx-'
           all_data.append(('[COLOR burlywood][Mx] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
  
    for name,link,server,quality in links_sno:
           fixed_q=fix_q(quality)
           #pre=check_pre(name,all_subs)
           pre=101
           se='-Sno-'
           all_data.append(('[COLOR dodgerblue][Sno] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))

    
    for name,link,server,quality in links_m4u:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-M4U-'
           all_data.append(('[COLOR darkgreen][M4U] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))

    for name,link,server,quality in rd_tvr:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-RD-TVR-'
           all_data.append(('[COLOR darkviolet][RD-TVR] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))

    for name,link,server,quality in link_afdah:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-AFa-'
           all_data.append(('[COLOR tomato][AFa] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))

    for name,link,server,quality in link_dlt:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-DLT-'
           all_data.append(('[COLOR tan][DLT] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
    
    for name,link,server,quality in links_pf:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-PF-'
           all_data.append(('[COLOR thistle][PF] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
    
    for name,link,server,quality in link_seehd:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)
 
           se='-SHD-'
           all_data.append(('[COLOR yellowgreen][SHD] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
    
    
    
    for name,link,server,quality in links_fun:
           fixed_q=fix_q(quality)
           pre=check_pre(name,all_subs)

           se='-FN-'
           
           all_data.append(('[COLOR lightgreen][FN] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q,name,pre))
    
    for saved_name,links,names,quality in link_cin:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-CIN-'
           all_data.append(('[CIN] '+saved_name+" - "+names.replace("Watch",""), links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in link_upto:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-UPT-'
           all_data.append(('[COLOR crimson][UPT] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in link_direct:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-DIR-'
           all_data.append(('[COLOR tan][DIR] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in links_we:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-WE-'
           all_data.append(('[COLOR blue][WE] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in links_dwatch:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-DW-'
           all_data.append(('[COLOR indianred][DW] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in links_cmovies:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-CM-'
           all_data.append(('[COLOR slategray][CM] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))

    for saved_name,links,names,quality in links_flix:
           fixed_q=fix_q(quality)

   
           pre=check_pre(saved_name,all_subs)

           
           se='-Flix-'
           all_data.append(('[COLOR slateblue][FLIX] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in links_put:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)
            
           se='-PUT-'
           all_data.append(('[COLOR darkcyan][PUT] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in links_seil:
           fixed_q=fix_q(quality)
           #pre=check_pre(saved_name,all_subs)
           pre=101
           se='-SERIL-'
           all_data.append(('[COLOR powderblue][SERIL] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in links_sc:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-SC-'
           all_data.append(('[COLOR lime][SC] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in links_1movie:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-1Movie-'
           all_data.append(('[COLOR grey][1M] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
   
    for saved_name,links,names,quality in link_goo:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-GOSTREAM-'
           all_data.append(('[COLOR yellow][GOS] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
           
    for saved_name,links,names,quality in link_tmp:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)

           se='-tmp-'
           all_data.append(('[COLOR green][tmp] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
           
    for saved_name,links,names,quality in link_ava:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)
        
           se='-ava-'
           all_data.append(('[COLOR pink][ava] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
           
    for saved_name,links,names,quality in cooltvzion:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)
 
           se='TVZION'
           all_data.append(('[COLOR steelblue][TVZ] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
           
    for saved_name,links,names,quality in link_dl20:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)
 
           se='DL20'
           all_data.append(('[COLOR skyblue][DL] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
           
    for saved_name,links,names,quality in link_hdonline:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)
           if '-VIP-' in names:
             se='-VIP-'
           else:
             se='HDONLINE'
           all_data.append(('[COLOR coral][HO] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,se,fixed_q,saved_name,pre))
           
    for saved_name,links,names,quality in link_showbox:
           fixed_q=fix_q(quality)
           pre=check_pre(saved_name,all_subs)
           all_data.append(('[COLOR lightgreen][SB] '+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,'SHOWBOX',fixed_q,saved_name,pre))
           
    if Addon.getSetting("daily")=='true' and url2!=None:
      for links,names,server,quality in link_daily:
           fixed_q=fix_q(quality)
           pre=check_pre(names,all_subs)
           all_data.append(('[COLOR khaki]'+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,'DailyMotion',fixed_q,names.replace("Watch",""),pre))
   
    for saved_name,links,names,quality in link_source1:
           fixed_q=fix_q(quality)
           #pre=check_pre(saved_name,all_subs)
           pre=101
           all_data.append(('[COLOR bisque][SP]'+ 'תרגום מובנה '.decode('utf8')+saved_name+" - "+names.replace("Watch","")+'[/COLOR]', links,icon,image,plot,year,quality,'SP Source',fixed_q,saved_name,pre))
    match_a=[]
    for link,name2,server,quality in match_a:
      
          if 'div class="tagged"' in quality:

            regex_q='<div class="tagged">(.+?)<'
            match_q=re.compile(regex_q).findall(quality)
            q=match_q[0]
          else:
            q=' '

          original_f= re.sub("[^a-zA-Z]+", "", original_title).lower()
          name_f=re.sub("[^a-zA-Z]+", "",  name2).lower()
          precent=similar(list(original_f),list(name_f))
          
   
          if precent>50 or eng_name.replace("%20"," ").lower() in name2.lower() or original_title.replace("%20"," ").lower() in name2.lower():
            fixed_q=fix_q(q)

            all_data.append((str(precent)+'-'+ name2.replace("Watch",""), domain_s+'pron.tv'+link,icon,image,plot,year,q,'-ALLUC-'+server,fixed_q))
    if Addon.getSetting("order")=='0':
      all_data=sorted(all_data, key=lambda x: x[8], reverse=False)
    elif Addon.getSetting("order")=='1':
       all_data=sorted(all_data, key=lambda x: x[10], reverse=True)
    else:
      all_1080=[]
      all_720=[]
      all_480=[]
      all_else=[]
      all_rd=[]
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_data:
        if '[RD-TVR]' in name or '[2Dl]' in name:
          all_rd.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
        if q=='1080':
         all_1080.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
        elif q=='720':
         all_720.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
        elif q=='480':
         all_480.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
        else :
         all_else.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
      all_rd=sorted(all_rd, key=lambda x: x[10], reverse=True)
      all_1080=sorted(all_1080, key=lambda x: x[10], reverse=True)
      all_720=sorted(all_720, key=lambda x: x[10], reverse=True)
      all_480=sorted(all_480, key=lambda x: x[10], reverse=True)
      all_else=sorted(all_else, key=lambda x: x[10], reverse=True)
      all_data=[]
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_rd:
         all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_1080:
         all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_720:
         all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_480:
         all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
      for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_else:
         all_data.append((name,link,icon,image,plot,year,q,server,f_q,saved_name,pre))
    if get_local==True:

     return all_data
    
    all_in=[]
    if imdb_global==None:
      imdb_global=' '
    if all_subs==None:
      all_subs=[]
      
    if isr==0 and Addon.getSetting("magnet")=='true':
      all_in.append(( '[COLOR aqua][I]קישורי מגנט -(%s)[/I][/COLOR]'%len(all_magnet), json.dumps(all_magnet),21,icon,image,plot,year,json.dumps(all_subs),season,episode,imdb_global))

    if isr==0 and Addon.getSetting("magnet")=='true':
      if  Addon.getSetting("all_t")=='false':
       addDir3( '[COLOR aqua][I]קישורי מגנט -(%s)[/I][/COLOR]'%len(all_magnet), json.dumps(all_magnet),21,icon,image,plot,data=year,original_title=json.dumps(all_subs),season=season,episode=episode,id=imdb_global)
      else:
       
        play_by_subs('[COLOR aqua][I]קישורי מגנט -(%s)[/I][/COLOR]'%len(all_magnet),json.dumps(all_magnet),icon,fanart,plot,year,json.dumps(all_subs),season,episode,imdb_global,'','',one_list=True)
    playingUrlsList = []
    t=0
    for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_data:
      t=t+1
      if plot==None:
         plot=' '

      
      playingUrlsList.append(link+'$$$$$$$'+server+'$$$$$$$'+q+'$$$$$$$'+saved_name+'$$$$$$$'+'[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot)
      

    addLink( '[COLOR aqua][I]ניגון אוטומטי[/I][/COLOR]', json.dumps(playingUrlsList),6,False,icon,image,plot,data=year,original_title=original_title.replace("%20"," "),season=season,episode=episode,id=id,saved_name=original_title,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year)
    if Addon.getSetting("fast_play2")=='true':
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
    once=0
    for name,link,icon,image,plot,year,q,server,f_q,saved_name,pre in all_data:
      
      if server==None:
        server=' '
      if q==None:
        q=' '
      if plot==None:
        plot=' '
      name=name.replace("|"," ").replace("  "," ").replace("\n","").replace("\r","").replace("\t","").strip()
      if Addon.getSetting("fast_play2")=='true':
          listItem=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=image)
          listItem.setInfo('video', {'Title': name, 'Genre': 'Kids'})
          link2=('%s?name=%s&mode=5&url=%s&data=%s&season=%s&episode=%s&original_title=%s&saved_name=%s&heb_name=%s&show_original_year=%s&eng_name=%s&isr=%s&id=%s&description=%s'%(sys.argv[0],name,urllib.quote_plus(link),show_original_year,season,episode,original_title,name,heb_name,show_original_year,eng_name,isr,id,urllib.quote_plus(('[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot).encode('utf8'))))
          playlist.add(url=link2, listitem=listItem)
       
      
           
           
          
           
      
      if isr==0:
        addLink('[COLOR gold][I]'+str(pre)+'%[/I][/COLOR]-'+ name, link,5,False,icon,image,'[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot,data=o_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year)
      else:
         addLink( name, link,5,False,icon,image,'[COLOR gold]'+q+'[/COLOR]\n[COLOR lightblue]'+server+'[/COLOR]\n'+plot,data=o_year,original_title=original_title,season=season,episode=episode,id=id,saved_name=saved_name,prev_name=o_name,eng_name=eng_name,heb_name=heb_name,show_original_year=show_original_year)
    search_done=1
    if Addon.getSetting("trailer_wait")=='true' and Addon.getSetting("trailer_dp")=='true' :
       while xbmc.Player().isPlaying():
         xbmc.sleep(100)

    if Addon.getSetting("fast_play2")=='true':
       
           xbmc.Player().stop()

           xbmc.Player().play(playlist,windowed=False)
    if len (next_p_all)>0:
      addDir3('[COLOR aqua][I]'+'עוד תוצאות'.decode('utf8')+'[/I][/COLOR]',domain_s+'www.alluc.ee'+match[0],4,icon,image,plot.decode('utf8'),data=year,original_title=original_title,season=season,episode=episode,id=id)
            
def auto_play(name,urls,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id):
   
    year=show_original_year
    image=fanart
    plot=description
    icon=iconimage
    all_data=[]
    '''
    if Addon.getSetting("dp")=='true' and silent_mode==False:
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','מנגן', '','')
        dp.update(0, 'אנא המתן','מנגן', '' )
    '''
    z=0

    
    all_links=json.loads(urls)

    for link in all_links:#for name2,link,icon,image,plot,year,q,server,f_q in all_data:
      
       server=link.split("$$$$$$$")[1]
       q=link.split("$$$$$$$")[2]
       name=link.split("$$$$$$$")[3]
       plot=urllib.unquote_plus(link.split("$$$$$$$")[4].decode('utf8'))
       link=link.split("$$$$$$$")[0]
       
       
       try:
        if '-Sdarot' not in plot:
         r=play(name,link,iconimage,fanart,plot,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,auto_play=True)
        
         if r=='ok':
            
            while not xbmc.Player().isPlaying():
                xbmc.sleep(100) #wait until video is being played
            time.sleep(5)
            if xbmc.Player().isPlaying():
             
             mode=1999
             
             xbmc.executebuiltin('Dialog.Close(okdialog, true)')
             
             break
                
       except Exception as e:
         logging.warning(e)
         if Addon.getSetting("dp")=='true' and silent_mode==False:
           dp.update(int(z/(len(all_links)*100.0)),str(server)+"-"+q,str(z)+'/'+str(len(all_links)),str(e))
       z=z+1
    
def resolve_thevideo(url):
    url=url.replace('thevideo.me','thevideo.website')
    headers = {
    'Host': 'thevideo.cc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    }
    
    x,cook=cloudflare.request(url)
    

    regex='sources.+?"file":"(.+?)"'
    match=re.compile(regex).findall(x)
    video_url=match[0]
    
    
    regex="var thief='(.+?)'"
    match=re.compile(regex).findall(x)
    
    
    url_new=domain_s+'thevideo.cc/vsign/player/'+match[0]
   
    y,cook=cloudflare.request(url_new)

    regex_new='jwConfig\|(.+?)\|return'
    key=re.compile(regex_new).findall(y)[0]
    
    url_final=video_url+"?direct=false&va=1&vt="+key

    return url_final
def check_link(x,full_data=False):
    if full_data==False:
      html=x.content
    else:
      html=x
    if len(html)<20:
      return False
    if "The video has been blocked at the copyright owner".lower() in html.lower() or "his stream doesn't exist !".lower() in html.lower() or 'Invalid Download Link'.lower() in html.lower() or 'page not found' in html.lower() or 'this file has been removed ' in html.lower() or 'removed due a copyright violation' in html.lower() or 'no longer available' in html.lower() or 'file has been deleted' in html.lower() or 'Page Not Found' in html.lower() or 'got removed by the owner.' in html.lower() or 'it maybe got deleted' in html.lower() or 'file not found' in html.lower() or 'file was deleted' in html.lower() or '<title>Error 404</title>' in html or '<H2>Error 404</H2>' in html or '<h1>Not Found</h1>' in html or '<b>File Not Found</b>' in html:
      return False
    else:
      return True
class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"
def get_redirect(url):
 try:
     if KODI_VERSION>=17:
         request = HeadRequest(url)
         response = urllib2.urlopen(request)
         
         new_url=response.geturl() 
         return new_url
     else:
       return url
 except:
   return url
def chek_play_l(url):
 request = HeadRequest(url)
 response = urllib2.urlopen(request)
 response_headers = response.info()

 return response_headers
def resolve_uptobox(url):
    import requests
    if 'uptostream' not in url:
        x=requests.get(url).content
        regex='<a href="https://uptostream.com/(.+?)"'
        match=re.compile(regex).findall(x)

      
        url=domain_s+'uptostream.com/'+match[0]
    
    

    cookies = {
        #'__cfduid': 'd0dfe3eedd616e0f275edcea08cdb6e521520582950',
        'video': '55srlypu0c08',
    }

    headers = {
        'Host': 'uptostream.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = requests.get(url, headers=headers, cookies=cookies).content
    regex='var sources = (.+?);'
    match=re.compile(regex).findall(response)
    links=json.loads(match[0])
    quality=[]
    links2=[]
    for data in links:
      quality.append(data['label'])
      links2.append(data['src'])
    
    ret = xbmcgui.Dialog().select("בחר איכות", quality)
    if ret!=-1:
        f_link=links2[ret]
    else:
      sys.exit()
    return f_link
   

    '''
    import requests

    

    headers = {
        'Host': 'uptobox.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    x=requests.get(url, headers=headers).content

    regex="'waitingToken' value='(.+?)'"
    match=re.compile(regex).findall(x)

    if len (match)>0:
        token=match[0]
        
        data = [
          ('waitingToken', token),
        ]

        response = requests.post(url, headers=headers, cookies=cookies, data=data).content
        regex="td class='cell countdown-.+?<a href=\"(.+?)\""
        match=re.compile(regex,re.DOTALL).findall(response)
    else:
        regex="td class='cell countdown-.+?<a href=\"(.+?)\""
        match=re.compile(regex,re.DOTALL).findall(x)
    return match[0]
    '''
def decrypt(url):
    from base64 import b64decode
    ''' decrypt the given encrypted code '''
    html=requests.get(url).content
    

    regex="var ysmm = '(.+?)'"
    match=re.compile(regex).findall(html)
    if len(match)>0:
        
        ysmm = match[0]
      
        #ysmm='Y=jMkDyNM3GUUD1MYwzIJWiNYx2UZmmNOkTVcDyMMi2Rh20Yd6HIAT6MLiyN9G0Nd33McTuZdymMljkYZvWU9G3bZpWZV1kLLzmV'
        code=(ysmm.decode('utf-8'))

        zeros, ones = '', ''

        for num, letter in enumerate(code):
            if num % 2 == 0: zeros += code[num]
            else: ones = code[num] + ones

        key = zeros + ones
 
        u=list((key))
 
        m=0
        while m <(len(u)-1):
          if u[m].isnumeric():
              R=m+1
              while R< (len(u)-1): 
                if u[R].isnumeric():
                     
                  S =(int(u[m]) ^ int(u[R]))


                  if ((S) < 10):

                    u[m] = unicode(S)
                  m = R
                  R = len(u)
                R=R+1
          m=m+1
        t3="".join(u)

        key = (t3).decode('base64')

        key=key[(len(t3)-(len(t3)-16)):]
 
        key=key[:((len(key)-16))]
    else:
      from unshort import unshorten
 
     
      unshortened_uri, status = unshorten(url,type='shst')

      if unshortened_uri==url:
        unshortened_uri, status = unshorten(url,type='shst')
      key=unshortened_uri
     
   
    return key
def resolve_rd(url):
    host = url.split('//')[1].replace('www.','')
    
    debrid = host.split('/')[0].lower()
    
    debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()]
    all_resolve=[]
    for key in debrid_resolvers:
      all_resolve.append(key.name)
    
    if 'Real-Debrid' not in all_resolve and 'MegaDebrid' not in all_resolve:
       
       xbmc.executebuiltin("RunPlugin(plugin://script.module.resolveurl/?mode=auth_rd)")
   
    if len(debrid_resolvers) == 0:

        debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True,include_universal=False) if 'rapidgator.net' in resolver.domains]

    debrid_resolver = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()][0]
 
    debrid_resolver.login()
    _host, _media_id = debrid_resolver.get_host_and_id(url)

    stream_url = debrid_resolver.get_media_url(_host, _media_id)

    return stream_url
def decode(encoded, code):
        #from https://github.com/jsergio123/script.module.urlresolver
        _0x59b81a = ""
        k = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        k = k[::-1]

        count = 0

        for index in range(0, len(encoded) - 1):
            while count <= len(encoded) - 1:
                _0x4a2f3a = k.index(encoded[count])
                count += 1
                _0x29d5bf = k.index(encoded[count])
                count += 1
                _0x3b6833 = k.index(encoded[count])
                count += 1
                _0x426d70 = k.index(encoded[count])
                count += 1

                _0x2e4782 = ((_0x4a2f3a << 2) | (_0x29d5bf >> 4))
                _0x2c0540 = (((_0x29d5bf & 15) << 4) | (_0x3b6833 >> 2))
                _0x5a46ef = ((_0x3b6833 & 3) << 6) | _0x426d70
                _0x2e4782 = _0x2e4782 ^ code

                _0x59b81a = str(_0x59b81a) + chr(_0x2e4782)

                if _0x3b6833 != 64:
                    _0x59b81a = str(_0x59b81a) + chr(_0x2c0540)
                if _0x3b6833 != 64:
                    _0x59b81a = str(_0x59b81a) + chr(_0x5a46ef)

        return _0x59b81a
def resolve_streamango(url):
        sHtmlContent = requests.get(url).content

        r1 = re.search("srces\.push\({type:\"video/mp4\",src:\w+\('([^']+)',(\d+)", sHtmlContent)
        if (r1):
            api_call = decode(r1.group(1), int(r1.group(2)))
            api_call = 'http:' + api_call
            
            return api_call
def resolve_req(url):
    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    }
    x=requests.get(url,headers=headers).content
    regex='POST".+?"_csrfToken" value="(.+?)".+?"alias" value="(.+?)".+?"ci" value="(.+?)".+?"cui" value="(.+?)".+?"cii" value="(.+?)".+?"ref" value="(.+?)".+?"country" value="(.+?)".+?"_Token\[fields\]" value="(.+?)".+?"_Token\[unlocked\]" value="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(x)
    csrtoken,alias,ci,cui,cii,ref,country,Token_fields,Token_unlocked=match[0]
    cookies = {
        #'AdLinkFly': 'eb8eac21c0dd7b9ba8ca2df6cc07c54e',
        'csrfToken': csrtoken,
        #'visitor': 'Q2FrZQ%3D%3D.NTg5YjdiNWYxODVlYTIzNDdiZDY3ZDU2MDE3Y2M1YzI5N2UzZWJjMjNhYzc0MzgzNTliNzA4MmVkMTA2YmUwNVVrvUk76HJ0rSgx5Wt%2BYIxoqr9bRVvztgxaiI3Kyw3iOCMBcbBtHDyrkkJboTMHcbqkOV775%2FEH1t5BCf6L3XTOAoDNGdbCPOMnP%2FBmf6A9',
        #'ab': '2',
    }

    headers = {
        'Pragma': 'no-cache',
        'Origin': 'http://reqlinks.net',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': url,
    }

    data = [
      ('_method', 'POST'),
      ('_csrfToken', csrtoken),
      ('alias', alias),
      ('ci', ci),
      ('cui', cui),
      ('cii', cii),
      ('ref', ''),
      ('country', country),
      ('_Token[fields]', Token_fields),
      ('_Token[unlocked]', Token_unlocked),
    ]
   
    response = requests.post('http://reqlinks.net/links/go', headers=headers, cookies=cookies, data=data).json()
    return (response['url'])
def play(name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id,auto_play=False):
     global silent_mode
     tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
     silent_mode=True
     import requests
     year=data
     if len (saved_name)<3:
       saved_name=name

     #url=os.path.join(user_dataDir ,'new.m3u8')
     #xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'Resolving')).encode('utf-8'))
     #url=domain_s+'openload.co/embed/h_ViopSrup0/'
     error_link=0

     if season!=None and season!="%20":
       url2='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(id,tmdbKey)
     else:
     
       url2='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=he&append_to_response=external_ids'%(id,tmdbKey)
     try:
        imdb_id=requests.get(url2).json()['external_ids']['imdb_id']
     except:
        imdb_id=" "

     if '-REQ-' in description:
       url=resolve_req(url)
     if '-Sdarot' in description:
       url_data=json.loads(url)
       
       url, cookie=get_final_video_and_cookie(url_data[0], url_data[1], url_data[2], False, False)
     if '-SN-' in description or '-Sno-' in description:
        url=decrypt(url)
     if 'streamango' in url:
        url=resolve_streamango(url)
        
     if 'vidup' in url:
        url=getMediaLinkForGuest_vidup(url)[1]
     if 'vidlox' in url:
       url=getMediaLinkForGuest_vidlox(url)[1]
     if 'movix' in url:
        url=resolve_movix(url)
     if '://vidtod' in url and rd_sources=='false':
       
       url=VidToDoResolver(url)[1]

     if 'thevideo' in url and rd_sources=='false':
        url=getMediaLinkForGuest_thevid(url)[1]

     if 'vshare' in url and rd_sources=='false':
   
        url=getMediaLinkForGuest_vshare(url)[1]
        
       

     if  rd_sources=='true':
       import resolveurl
     elif 'uptobox' not in url and 'vidtod' not in url and 'thevideo' not in url and 'vshare' not in url and 'vidlox' not in url and 'vidup' not in url and '-Sdarot' not in description:
       import resolveurl
     url3=url
     if 'pron.tv' in url:
      
        url3=get_allu_links(url)

     if url3!=None:
           url=url3
     
     if  rd_sources=='true' and '-Sdarot' not in description:
        try:
          
          url=resolve_rd(url)
        except Exception as e:
          logging.warning(e)
          pass
        #resolvable=resolveurl.HostedMediaFile(url, include_disabled=True,include_universal=True).valid_url()
        resolvable=False
     elif 'streamango' not in url and 'uptobox' not in url and 'vidtod' not in url and 'thevideo' not in url  and 'vshare' not in url and 'vidlox' not in url and 'vidup' not in url and '-Sdarot' not in description:
       resolvable=resolveurl.HostedMediaFile(url).valid_url()
       
       
     else:
       resolvable=False
     if 'googleusercontent' in url:
       resolvable=False
     
     if  rd_sources=='true':
        universal=True
     else:
        universal=False

     if 1:#try:
         
         

     

         video_data={}
         regex_name='] (.+?) -'
         match_name=re.compile(regex_name).findall(saved_name)
         if len(match_name)>0:
           fixed_name=match_name[0]
         else:
           fixed_name=saved_name
         if season!=None and season!="%20":
           video_data['TVshowtitle']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'")
           video_data['mediatype']='tvshow'
         else:
           video_data['mediatype']='movies'
         video_data['OriginalTitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'")
         video_data['title']=fixed_name
         video_data['poster']=fanart
         video_data['plot']=description
         video_data['icon']=iconimage
         video_data['year']=data
         video_data['season']=season
         video_data['episode']=episode
         video_data['imdb']=imdb_id
         video_data['code']=imdb_id
         if '-TVL-' in description or '-Sno-' in description or 'SP Source' in description or '-SC-' in description or '-SERIL-' in description or '-MX-' in description or '-FN-' in description or '-SN-' in description or '-Sdarot' in description :
             video_data[u'mpaa']=unicode('heb')

         video_data['imdbnumber']=imdb_id
         pass_openload='ok'
 
         if  resolvable:
           regex='//(.+?)/'
           match=re.compile(regex).findall(url)
           if len (match)>0:
             src=match[0]
           else:
             src=url
           src=src.lower().replace("openload","vumoo").replace("thevideo","vumoo.li").replace("Openload","vumoo")
           
           xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'Source Resolving:'+src)).encode('utf-8'))
           Domain=Addon.getSetting("server")
           En_Domain=Addon.getSetting("serveroption")
           
           x=requests.get(url,timeout=20)
               
           if x.status_code!=200:
            
               error_link=x.status_code
           else:
             yz=check_link(x)
             if yz==False:
               error_link='File Not Found'
           if error_link!=0:
             xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'Fault:'+str(error_link))).encode('utf-8'))
       
           if ('openload' in url or 'oload.stream' in url) and error_link==0 and rd_sources=='false':
             
               xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'Vummo Source')).encode('utf-8'))
      
               streamurl=getMediaLinkForGuest(url)
               pass_openload='ok'
               error_link=0
               link=streamurl
               xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', '[COLOR lighgreen]Vummo OK[/COLOR]')).encode('utf-8'))
               '''
               if 'openload' in url and  len(Domain)>0 and En_Domain=='true' and error_link==0:
               
                   import requests
                   if 'http' not in Domain:
                          Domain='http://'+Domain
                   new_serv=Domain+":8080/GetVideoUrl?url="+(url)
                   new_serv=new_serv.replace("openload.co",'oload.stream').replace("embed",'f')
           
                   try:
                     
                       x=requests.get(new_serv, timeout=70).content
                       regex='>(.+?)<'
                       link=re.compile(regex).findall(x)[0]
                       
                 
                               
                   except:
                     pass_openload='fail'
                     pass
                   
               '''
           
       
           else:
             pass_openload='ok'
             
             try:
               
               x=requests.get(url,timeout=20)
               yz=True
               if x.status_code!=200 :
                 
                   error_link=x.status_code
               else:
                 yz=check_link(x)
          
               if yz==False:
                   error_link='File Not Found'
  
               if  rd_sources=='true':
                 
                 hmf = resolveurl.HostedMediaFile(url=url, include_disabled=True, include_universal=False)
                 link = hmf.resolve()
               else:
               
                 link =resolveurl.resolve(url)
         
             except Exception as e:
               logging.warning(e)
               link=url
               pass
           if pass_openload=='fail':
             
             try:
              
               x=requests.get(url,timeout=20)
               
               if x.status_code!=200:
                
                   error_link=x.status_code
               else:
                 yz=check_link(x)
                 if yz==False:
                   error_link='File Not Found'
               link =resolveurl.resolve(url)
               
             except:
               link=url
               pass
             
         else:
           xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'Source Resolving:Direct')).encode('utf-8'))
           link=url
         
        
         if 1:#try:
           if '-Sdarot' not in description and 'ftp://' not in link and '-MK-' not in description:
             link=link.replace(" ","").replace("\n","").replace("\r","").replace("\t","")
           elif 'ftp://' in link:
             
             link=urllib.unquote(link)
             #link=urllib.unquote(link)
   
         
         #except:
         #  link=url
         
         if '-4K' in description:
              xx=requests.get(url).content
              regex='iframe .+? src="(.+?)"'
              match2=re.compile(regex).findall(xx)
              link_f=match2[0]
            
              link =resolveurl.resolve(link_f)
      
         if '-Sdarot' in description:
      
           error_link=0
         if 'uptobox' in url and rd_sources=='false':
           link=resolve_uptobox(url)
           error_link=0
         if 'thevideo' in url:
           error_link=0
         if 'upfile' in link or 'www.upf.co.il' in url:
            name2,link=get_upfile_det(url)
            error_link=0
        
         if error_link==0:
         
             
             listItem = xbmcgui.ListItem(video_data['title'], path=link) 
             listItem.setInfo(type='Video', infoLabels=video_data)


             listItem.setProperty('IsPlayable', 'true')
     
             if auto_play==True:
               ok=xbmc.Player().play(link,listitem=listItem)
               ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
             else:
             
               ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
             
             try:
              
              if season!=None and season!="%20":
                match_a= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,str(int(episode)+1),id,eng_name,show_original_year,heb_name,isr, table='pages')
                #xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'פרק הבא מוכן'.decode('utf8'))).encode('utf-8'))
                '''
                match_a= cache.get(c_get_sources, time_to_save, original_title,year,original_title,season,str(int(episode)+1),id,eng_name,show_original_year,heb_name,isr, table='pages')
                xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'פרק הבא מוכן'.decode('utf8'))).encode('utf-8'))
                url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s/episode/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'%(id,season,str(int(episode)+1))
                html=requests.get(url).json()
                
                while xbmc.Player().isPlaying():
                  xbmc.sleep(1000)
                if 'overview' in html:
                    next_link="plugin://plugin.video.allmoviesin/?mode=4&title=%s&season=%s&episode=%s&data=%s&eng_name=%s&heb_name=%s&name=%s&original_title=%s&show_original_year=%s&id=%s&url=http://api.themoviedb.org/3/movie/popular?api_key=34142515d9d23817496eeb4ff1d223d0&language=he&page=1"%(original_title,season,episode,year,eng_name,heb_name,original_title,original_title,show_original_year,id)
                    
                    match_final=[html['overview']]
                    image=domain_s+'image.tmdb.org/t/p/original/'+html['still_path']
                    window = POPUPTEXT('פרק הבא',match_final,image=image,next_link=next_link)
                    window.doModal()
                    del window
                '''
             except Exception as e:
               logging.warning('ERRORRRRRRRRRRRRRRR: '+str(e))
               pass
             return 'ok'
         else:
           return error_link
     #except Exception as e:
     # if auto_play==True:
     #  return e
     # else:
     #  xbmcgui.Dialog().ok('Error occurred',str(e))

def get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr):
   payload= {
                    "apikey": "0629B785CE550C8D",
                    "userkey": "",
                    "username": ""
   }

   #headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Accept-Language': 'he'}
   #r = requests.post(domain_s+'api.thetvdb.com/login', json=payload, headers=headers)
   #r_json = r.json()

   url=domain_s+'api.themoviedb.org/3/tv/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he,en&append_to_response=external_ids'%id
   
   html=requests.get(url).json()
   show_original_year=html['first_air_date'].split("-")[0]

   #tmdb data
   #headers['Authorization'] = "Bearer %s" %  str(r_json.get('token'))
   tmdbid=html['external_ids']['tvdb_id']
   if tmdbid==None:
     response2 = requests.get(domain_s+'www.thetvdb.com/?string=%s&searchseriesid=&tab=listseries&function=Search'%name).content

     SearchSeriesRegexPattern = 'a href=".+?tab=series.+?id=(.+?)mp'
     match=re.compile(SearchSeriesRegexPattern).findall(response2)
   
     for tmnum in match:
       tmnum=tmnum.replace("&a","")
       if len(tmnum)>0:
         tmdbid=tmnum

   response = requests.get('http://thetvdb.com/api/0629B785CE550C8D/series/%s/all/he.xml'%html['external_ids']['tvdb_id']).content
   attr=['Combined_season','FirstAired']
   regex='<Episode>.+?<EpisodeName>(.+?)</EpisodeName>.+?<EpisodeNumber>(.+?)</EpisodeNumber>.+?<FirstAired>(.+?)</FirstAired>.+?<SeasonNumber>(.+?)</SeasonNumber>'
   match=re.compile(regex,re.DOTALL).findall(response)
   #seasons_tvdb=parseDOM(response,'Episode', attr)
   all_season=[]
   all_season_tvdb_data=[]

   for ep_name,ep_num,aired,s_number in match:
     if s_number not in all_season:

       all_season.append(str(s_number))
       all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"season_number":s_number,"poster_path":iconimage})

   all_season_tmdb=[]
   for data in html['seasons']:
      all_season_tmdb.append(str(data['season_number']))
   for items_a in all_season:
     if items_a not in all_season_tmdb:
       html['seasons'].append(all_season_tvdb_data[all_season.index(items_a)])
   plot=html['overview']
   original_name=html['original_name']
   for data in html['seasons']:
   
     new_name=' עונה '.decode('utf8')+str(data['season_number'])
     if data['air_date']!=None:
         year=str(data['air_date'].split("-")[0])
     else:
       year=0
     season=str(data['season_number'])
     if data['poster_path']==None:
      icon=iconimage
     else:
       icon=data['poster_path']
     if 'backdrop_path' in data:
         if data['backdrop_path']==None:
          fan=fanart
         else:
          fan=data['backdrop_path']
     else:
        fan=html['backdrop_path']
     if plot==None:
       plot=' '
     if fan==None:
       fan=fanart
     if 'http' not in fan:
       fan=domain_s+'image.tmdb.org/t/p/original/'+fan
     if 'http' not in icon:
       icon=domain_s+'image.tmdb.org/t/p/original/'+icon
     addDir3(new_name,url,8,icon,fan,plot,data=year,original_title=original_name,id=id,season=season,tmdbid=tmdbid,show_original_year=show_original_year,heb_name=heb_name,isr=isr)
def get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr):
   import _strptime
   url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'%(id,season)

   html=requests.get(url).json()
   #tmdb data
   if html['episodes'][0]['name']=='':
     url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=eng'%(id,season)
     html=requests.get(url).json()
   response = requests.get('http://thetvdb.com/api/0629B785CE550C8D/series/%s/all/he.xml'%tmdbid).content
   
   attr=['Combined_season','FirstAired']
   regex='<Episode>.+?<EpisodeName>(.+?)</EpisodeName>.+?<EpisodeNumber>(.+?)</EpisodeNumber>.+?<FirstAired>(.+?)</FirstAired>.+?<Overview>(.+?)</Overview>.+?<SeasonNumber>(.+?)</SeasonNumber>'
   match=re.compile(regex,re.DOTALL).findall(response)
   regex_eng='<slug>(.+?)</slug>'
   match_eng=re.compile(regex_eng).findall(response)
   
   eng_name=name
   if len (match_eng)>0:
     eng_name=match_eng[0]

   #seasons_tvdb=parseDOM(response,'Episode', attr)

   all_episodes=[]
   all_season_tvdb_data=[]
   image2=' '
   for ep_name,ep_num,aired,overview,s_number in match:
     
     image2=fanart
     if s_number==season:
         if ep_num not in all_episodes:
           
           all_episodes.append(str(ep_num))
           all_season_tvdb_data.append({"name":ep_name,"episode_number":ep_num,"air_date":aired,"overview":overview,"season_number":s_number,"still_path":iconimage,"poster_path":image2})

   all_episodes_tmdb=[]

   if 'episodes' not in html:
     html['episodes']=[]
     html['poster_path']=fanart
   for data in html['episodes']:
      all_episodes_tmdb.append(str(data['episode_number']))
   for items_a in all_episodes:
     if items_a not in all_episodes_tmdb:
       html['episodes'].append(all_season_tvdb_data[all_episodes.index(items_a)])

   original_name=original_title
   if Addon.getSetting("dp")=='true' and (Addon.getSetting("disapear")=='true' or Addon.getSetting("check_subs")=='true'):
            dp = xbmcgui.DialogProgress()
            dp.create("טוען סרטים", "אנא המתן", '')
            dp.update(0)
   xxx=0
   start_time = time.time()
   from datetime import datetime
   for data in html['episodes']:
     plot=data['overview']
     new_name=str(data['episode_number'])+" . "+data['name']
     air_date=''
     if 'air_date' in data:
       if data['air_date']!=None:
         
         year=str(data['air_date'].split("-")[0])
       else:
         year=0
     else:
       year=0
     
     if data['still_path']!=None:
       if 'https' not in data['still_path']:
         image=domain_s+'image.tmdb.org/t/p/original/'+data['still_path']
       else:
         image=data['still_path']
       
     elif html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       image=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
         image=html['poster_path']
     else:
       image=fanart
     if html['poster_path']!=None:
      if 'https' not in html['poster_path']:
       icon=domain_s+'image.tmdb.org/t/p/original/'+html['poster_path']
      else:
        icon=html['poster_path']
     else:
       icon=iconimage
     #if image2==fanart:
     #  icon=iconimage
      
     #  image=fanart
     color2='white'
     if 'air_date' in data:
       try:
           datea='[COLOR aqua]'+str(time.strptime(data['air_date'], '%Y-%m-%d'))+'[/COLOR]\n'
           
           a=(time.strptime(data['air_date'], '%Y-%m-%d'))
           b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
           
       
           if a>b:
             color2='red'
           else:
             
             color2='white'
       except:
             
             datea=''
             color2='red'
     f_subs=[]
     datea='[COLOR aqua]'+' שודר בתאריך '+time.strftime( "%d-%m-%Y",a) + '[/COLOR]\n'
     
     if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
         f_subs=cache.get(get_subs,9999,'tv',original_name,season,str(data['episode_number']),id,year,True, table='pages')
         #f_subs=get_subs('tv',original_name,season,str(data['episode_number']),id,year,check_one=True)
     
     

     if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
          if len(f_subs)>0:
            color='white'
          else:
            color='red'
            
     else:
         color=color2
     if season!=None and season!="%20":
        tv_movie='tv'
     else:
       tv_movie='movie'
     dbcur.execute("SELECT * FROM AllData WHERE original_title = '%s' AND type='%s' AND season='%s' AND episode = '%s'"%(original_title,tv_movie,season,data['episode_number']))
     
     match = dbcur.fetchone()

     if match!=None:
       color='magenta'
     elapsed_time = time.time() - start_time
     if (Addon.getSetting("check_subs")=='true'  or Addon.getSetting("disapear")=='true') and Addon.getSetting("dp")=='true':
        dp.update(int(((xxx* 100.0)/(len(html['episodes']))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
     xxx=xxx+1
     if  Addon.getSetting("disapear")=='true' and color=='red':
        a=1
     else:
       
       addDir3( '[COLOR %s]'%color+new_name+'[/COLOR]', url,4, icon,image,datea+plot,data=year,original_title=original_name,id=id,season=season,episode=data['episode_number'],eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr)
              
     xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
def resolve_wait_upto(url,id,match):
    import requests

    

    headers = {
        'Host': 'uptobox.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    cookies = {
        #'__cfduid': 'd0dfe3eedd616e0f275edcea08cdb6e521520582950',
        'video': id,
    }
    if len (match)>0:
        token=match[0]
       
        data = [
          ('waitingToken', token),
        ]

        response = requests.post(url, headers=headers, cookies=cookies, data=data).content

        regex="td class='cell countdown-.+?<a href=\"(.+?)\""
        match=re.compile(regex,re.DOTALL).findall(response)
    else:
        regex="td class='cell countdown-.+?<a href=\"(.+?)\""
        match=re.compile(regex,re.DOTALL).findall(x)
    return match[0]
def get_more_upt(dp):
  import requests
  x=requests.get('http://uptoboxsearch.com/').content
  regex="var cx = '(.+?)'"
  match=re.compile(regex).findall(x)
  cx=match[0]
  all_links=[]
  x=requests.get(domain_s+'cse.google.com/cse.js?cx='+cx).content
  regex='"cse_token": "(.+?)"'
  match=re.compile(regex).findall(x)
  cse=match[0]
  z=0
  q='2160p mkv'
  headers = {
        'Host': 'www.googleapis.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://uptoboxsearch.com/',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
  }
  all_urls=[]
  count=0
  start_time = time.time()
  for yy in range(0,10):
      params = (
            ('key', 'AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY'),
            ('rsz', 'filtered_cse'),
            ('num', '15'),
            ('hl', 'en'),
            ('prettyPrint', 'false'),
            ('source', 'gcsc'),
            ('gss', '.com'),
            ('start',str(yy)),
            ('cx', cx),
            ('q', q),
            ('cse_tok', cse),
            ('sort', ''),
            ('googlehost', 'www.google.com'),
            ('oq', q),
           
            ('callback', 'google.search.Search.apiary11806'),
      )

      html = requests.get(domain_s+'www.googleapis.com/customsearch/v1element', headers=headers, params=params).content
      
        #NB. Original query string below. It seems impossible to parse and
        #reproduce query strings 100% accurately so the one below is given
        #in case the reproduced version is not "correct".
        # response = requests.get(domain_s+'www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=45e50696e04f15ce6310843f10a3a8fb&cx=004238030042834740991:-46442tgrgu&q=justice%20league%202017&cse_tok=AOdTmaC-ij38dzKkMq3QK2HyVv31W5gTHw:1520722941794&sort=&googlehost=www.google.com&oq=justice%20league%202017&gs_l=partner-generic.12...0.0.3.1622277.0.0.0.0.0.0.0.0..0.0.gsnos%2Cn%3D13...0.0jj1..1ac..25.partner-generic..36.5.239.zlYYXWhpZYw&callback=google.search.Search.apiary11806', headers=headers)

     
      regex='\((.+?)\);'
      match=re.compile(regex).findall(html)

      all_results=json.loads(match[0])
     
      for data in all_results['results']:
       elapsed_time = time.time() - start_time
       z=z+1
       if 'upto' in data['url']:

        title=data['titleNoFormatting']
     
        info=(PTN.parse(title.replace('..','.')))

        if 'resolution' in info:
          res=info['resolution']
        else:
          res=' '
        if 'http' not in data['url']:
          link_f='http://'+data['url']
        else:
          link_f=data['url']
        x=requests.get(link_f).content
        regex='<a href="https://uptostream.com/(.+?)"'
        match=re.compile(regex).findall(x)
        
        if len (match)>0:
            url=domain_s+'uptostream.com/'+match[0]
            
 
            if url not in all_urls:
              dp.update(int(((z* 100.0)/(len(all_results['results'])*10)) ), ' אוסף מקורות נוספים '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),data['titleNoFormatting'], 'OK')
              count=count+1
              all_urls.append(url)
              all_links.append((title.replace("%20"," "),link_f,' '))
              link_upto=all_links
        else:
            dp.update(int(((z* 100.0)/(len(all_results['results'])*10)) ), ' אוסף מקורות נוספים '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),data['titleNoFormatting'], 'Preimium')
        '''
        else:
             regex="'waitingToken' value='(.+?)'"
             match=re.compile(regex).findall(x)
 
             regex="referer=(.+?)'"
             id=re.compile(regex).findall(x)[0]
             if len (match)>0:
       
               link_f2=resolve_wait_upto(link_f,id,match)
 
               all_links.append((title.replace("%20"," "),link_f2,' '))
               link_upto=all_links
               
        '''
 
  return all_links

def get_qu(url):
    tmdbKey = '653bb8af90162bd98fc7ee32bcbbfb3d'
    
    html=requests.get(url).content
    regx='<div class="metadata">.+?<span>(.+?)<.+?"texto">(.+?)<.+?<img src="(.+?)".+?<a href="(.+?)".+?<a href=".+?>(.+?)<'
    match=re.compile(regx,re.DOTALL).findall(html)
    if Addon.getSetting("dp")=='true':
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','מחפש מקורות', '','')
        dp.update(0, 'אנא המתן','מחפש מקורות', '' )
    z=0
    start_time = time.time()
    for year,plot_o,image,link,name_o in match:
      if Addon.getSetting("dp")=='true':
          if dp.iscanceled(): 
                dp.close()
                break
      name_o=name_o.replace('4K','').replace('4k','').replace('2160p','').replace('2160P','').replace('&#8217;',"'")
      tmdb_data="http://api.tmdb.org/3/search/movie?api_key=%s&query=%s&year=%s&language=he&append_to_response=external_ids"%(tmdbKey,urllib.quote_plus(name_o),year)
      all_data=requests.get(tmdb_data).json()
     
      if len(all_data['results'])>0:
            if (all_data['results'][0]['id'])!=None:
                url='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=he&append_to_response=external_ids'%(all_data['results'][0]['id'],tmdbKey)
                try:
                    imdb_id=requests.get(url).json()['external_ids']['imdb_id']
                except:
                    imdb_id=" "
              
            try:
                    name=all_data['results'][0]['title']
                    try:
                      icon=domain_s+'image.tmdb.org/t/p/original/'+all_data['results'][0]['poster_path']
                      fanart=domain_s+'image.tmdb.org/t/p/original/'+all_data['results'][0]['backdrop_path']
                    except:
                     pass
                    plot=all_data['results'][0]['overview']
            except:
                    name=info['title']
                    fanart=' '
                    icon=' '
                    plot=' '
      else:
           name=name_o
           fanart=image
           icon=image
           plot=plot_o
      elapsed_time = time.time() - start_time
      if Addon.getSetting("dp")=='true':
        dp.update(int(((z* 100.0)/(len(match))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),name, name_o)
      z=z+1
      addLink( name, link,5,False,icon,fanart,'[COLOR gold]'+'4K'+'[/COLOR]\n[COLOR lightblue]'+'-4K-'+'[/COLOR]\n'+plot,data=year,original_title=name_o,id=imdb_id)
    regex='rel="next" href="(.+?)"'
    match=re.compile(regex).findall(html)
    if len (match)>0:
      addDir3('[COLOR gold]עמוד הבא[/COLOR]'.decode('utf8'),match[0],10,' ',' ','סרטי 4K'.decode('utf8'))
    if Addon.getSetting("dp")=='true':
     dp.close()

    #new 4k:
    if Addon.getSetting("dp")=='true':
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','מחפש מקורות', '','')
        dp.update(0, 'אנא המתן','מחפש מקורות', '' )
    z=0
    start_time = time.time()
    x=requests.get('http://mavericktv.net/data/movies/uhd.xml').content
    regex='<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>'
    match=re.compile(regex,re.DOTALL).findall(x)
    count=0
    
  
   
      
    
    for name_o,link,image in match:
      name_o=name_o.replace('(','.').replace('7.1CH','').replace('4K','').replace('DD','').replace('5.1','').replace('4k','').replace('lime','').replace(')','.').replace(' ','.').replace('[','').replace(']','').replace('COLOR','').replace('blue','').replace('red','').replace('/','').replace('...','.').replace('..','.')
      info=(PTN.parse(name_o))
      
      count=count+1
      imdb_id=' '
      year_n='0'
      if 1:
         if 'title' in info:
          a=info['title']
         else:
           info['title']=name_o.replace('.',' ')
         
         if len(info['title'])>0:
          a=a
         else:
           info['title']=name_o.replace('.',' ')
         if 1:
          if 'year' in info:
            tmdb_data="http://api.tmdb.org/3/search/movie?api_key=%s&query=%s&year=%s&language=he&append_to_response=external_ids"%(tmdbKey,urllib.quote_plus(info['title']),info['year'])
            year_n=info['year']
          else:
            tmdb_data="http://api.tmdb.org/3/search/movie?api_key=%s&query=%s&language=he&append_to_response=external_ids"%(tmdbKey,urllib.quote_plus(info['title']))
  
          all_data=requests.get(tmdb_data).json()
          
          if len(all_data['results'])>0:
                if (all_data['results'][0]['id'])!=None:
                    url='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=he&append_to_response=external_ids'%(all_data['results'][0]['id'],tmdbKey)
                    try:
                        imdb_id=requests.get(url).json()['external_ids']['imdb_id']
                    except:
                        imdb_id=" "
                  
                try:
                        name=all_data['results'][0]['title']
                        rating=all_data['results'][0]['vote_average']
                        try:
                          icon=domain_s+'image.tmdb.org/t/p/original/'+all_data['results'][0]['poster_path']
                          fanart=domain_s+'image.tmdb.org/t/p/original/'+all_data['results'][0]['backdrop_path']
                        except:
                         pass
                        plot=all_data['results'][0]['overview']
                except:
                        name=info['title']
                        fanart=' '
                        icon=' '
                        plot=' '
          else:
               name=name_o
               fanart=image
               icon=image
               plot=' '
         else:
               name=name_o
               fanart=image
               icon=image
               plot=' '
      else:
               name=name_o
               fanart=image
               icon=image
               plot=' '
      elapsed_time = time.time() - start_time
      if Addon.getSetting("dp")=='true':
            dp.update(int(((z* 100.0)/(len(match))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),name, name_o)
      z=z+1
      addLink( name, link,5,False,icon,fanart,'[COLOR gold]'+'4K'+'[/COLOR]\n[COLOR lightblue]'+'-NEW K-'+'[/COLOR]\n'+plot,data=year_n,original_title=info['title'],id=imdb_id,rating=rating)
      xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
      xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

      xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
def get_image(name,year,pre_image):
          fanart=pre_image
          url2=domain_s+'api.themoviedb.org/3/search/movie?api_key=34142515d9d23817496eeb4ff1d223d0&language=en-US&query=%s&page=1&include_adult=false&year=%s'%(name,year)
          x=requests.get(url2).json()
          for data in x['results']:
            if 'backdrop_path' in data:
             if data['backdrop_path']==None:
              fanart=pre_image
             else:
              fanart=domain_s+'image.tmdb.org/t/p/original/'+data['backdrop_path']
            else:
              fanart=pre_image
          return fanart
def get_dub(page):
        import requests
        if page=="search":
            search_entered =''
            keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
            keyboard.doModal()
            if keyboard.isConfirmed():
                   search_entered = keyboard.getText()
                   
            else:
              sys.exit()

       

            headers = {
                'Host': 'moridim.tv',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': domain_s+'moridim.tv/',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
            }

            data = [
              ('table', 'movies'),
              ('q', search_entered),
              ('index', '0'),
              ('limit', '30'),
              ('type', '4'),
            ]

            response = requests.post(domain_s+'moridim.tv/ajax/indexFetch.php', headers=headers, data=data).content
            
            regex_pre='<div class="download">(.+?)תאריך העלאה'
            match_pre=re.compile(regex_pre,re.DOTALL).findall(response)
            for items in match_pre:
           
              regex='title="(.+?)"><img src="(.+?)".+?<div class="clear">.+?<p>(.+?)</p.+?שנת יציאה: <b>(.+?)</b>'
              match=re.compile(regex,re.DOTALL).findall(items)
              for name,image,plot,year in match:
                iconimage=domain_s+'moridim.tv/'+image
                fanart=domain_s+'moridim.tv/'+image
                heb_name=name.split('/')[0]
                eng_name=name.split('/')[1]
                addDir3(heb_name,'www',12,iconimage,fanart,plot,data=year,original_title=name,eng_name=eng_name,show_original_year=str(year),rating=0,heb_name=heb_name)
            page="0"
  
        

        else:
            headers = {
                'Host': 'moridim.tv',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': domain_s+'moridim.tv/%D7%A1%D7%A8%D7%98%D7%99%D7%9D.html',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'keep-alive',
            }

            data = [
              ('type', 'movies'),
              ('index', page),
              ('types[]', '4'),
              ('order', 'lastupdate'),
              ('sort', 'DESC'),
              ('limit', '30'),
            ]

            response = requests.post(domain_s+'moridim.tv/ajax/fetch.php', headers=headers, data=data).json()
            for data_in in response:
              fanart=cache.get(get_image,999,data_in['engName'],data_in['year'],domain_s+'moridim.tv/'+data_in['image'], table='posters')
              #fanart=get_image(data_in['engName'],data_in['year'],domain_s+'moridim.tv/'+data_in['image'])
            
              name=data_in['hebName']
              heb_name=data_in['hebName']
              iconimage=domain_s+'moridim.tv/'+data_in['image']
              
              description=data_in['plot']
              original_title=data_in['engName']
              eng_name=data_in['engName']
              data=data_in['year']
              rating=data_in['imdbRate']
              addDir3(name,'www',12,iconimage,fanart,description,data=data,original_title=original_title,eng_name=eng_name,show_original_year=str(data_in['year']),rating=rating,heb_name=heb_name)
            addDir3('[COLOR blue][I]עמוד הבא[/I][/COLOR]',str(int(url)+30),11,' ',' ','[COLOR blue][I]עמוד הבא[/I][/COLOR]')
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

            xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
def resolve_movix(link):
         from base64 import b64decode
         retUrl=' '
         try:
           decoded_uri=link.split('link=')[1].decode('base64')
           x,cook=cloudflare.request(decoded_uri)

           regex='<IFRAME SRC="(.+?)"'
           match=re.compile(regex).findall(x)[0]
           
           return match
         except:
           pass
         
         html,cook = cloudflare.request(link)
       
         ysmm = re.findall(r"var ysmm =.*\;?", html)
         if len(ysmm)<3:
           decoded_uri=link.split('link=')[1].decode('base64')
    
        
         if len(ysmm) > 0:
            ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])

            left = ''
            right = ''

            for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
                left += c[0]
                right = c[1] + right
            
            # Additional digit arithmetic 
            encoded_uri = list(left + right)
            numbers = ((i, n) for i, n in enumerate(encoded_uri) if str.isdigit(n))
            for first, second in zip(numbers, numbers):
                xor = int(first[1]) ^ int(second[1])
                if xor < 10:
                    encoded_uri[first[0]] = str(xor)

            decoded_uri = b64decode("".join(encoded_uri).encode())[16:-16].decode()

            if re.search(r'go\.php\?u\=', decoded_uri):
                decoded_uri = b64decode(re.sub(r'(.*?)u=', '', decoded_uri)).decode()
         
         x,cook=cloudflare.request(decoded_uri)

         regex='<IFRAME SRC="(.+?)"'
         match=re.compile(regex).findall(x)[0]

         return match
def get_movix(original_title,name,show_original_year,dub='yes'):
        global links_mx,stop_all
        #movix
        all_links=[]
        name=name.replace('[COLOR magenta]','').replace('[/COLOR]','')
        
        url=domain_s+'www.movix.me/search_movies?q=%s&sb=&year=%s'%(urllib.quote_plus(name),show_original_year)
      
        html,cook=cloudflare.request(url)
  

        regex='<h3><a href="(.+?)">(.+?)<'
       
        match=re.compile(regex).findall(html)
        
        for link,name in match:
          if stop_all==1:
            break
          if dub=='yes':
            if 'מדובב' in name:
              cn=True
            else:
              cn=False
          else:
             cn=True
          if cn:
     
            x,cook=cloudflare.request(domain_s+'www.movix.me'+link)

            regex='<div id="wrapserv"><a href="(.+?)".+?/img/servers/(.+?)png".+?<b>(.+?)</b>'
            match=re.compile(regex,re.DOTALL).findall(x)
            
            for link,server,quality in match:
              '''
              logging.warning(link)
              link2=resolve_movix(link)
              logging.warning(link2)
              name1,match_s,res,check=server_data(link2,original_title)
              if check :
              '''
              all_links.append((name,link,server,quality))
              links_mx=all_links
        return all_links
def get_serno(original_title,name,show_original_year,dub='yes'):
    global links_sno
   
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'seretnow.me',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }

    all_links=[]
    url='http://seretnow.me/?s='+urllib.quote_plus(name)

    x=requests.get(url,headers=headers).content
    regex='<a href="(.+?)" rel="bookmark" title="(.+?)">'
    match=re.compile(regex).findall(x)

    for link,name_in in match:
      if dub=='yes':
        if 'מדובב' in name_in:
          cn=True
        else:
          cn=False
      else:
         cn=True
      name_fix='$$$'+name_in.split('/')[0].strip()

      if '$$$'+name+' לצפייה ' in name_fix and cn==True:
      
        y=requests.get(link).content
        regex2='<a href="(.+?)" target="_blank" rel=".+?">(.+?)<'
        match2=re.compile(regex2).findall(y)
        if len(match2)==0:
           regex2='a href="(.+?)" target="_blank">(.+?)<'
           match2=re.compile(regex2).findall(y)

        

        for links,server in match2:

             
            quality=' '
            all_links.append((name_in,links,server,quality))
            
            links_sno=all_links
    return all_links
def get_funlopy(original_title,name,show_original_year,dub='yes'):
    global links_fun,stop_all
    import resolveurl
    all_links=[]
    url='http://funloty.com/search/'+urllib.quote_plus(name)
    x=requests.get(url).content
    regex='<meta itemprop="name" content="(.+?)".+?<meta itemprop="url" content="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(x)
    
    for name_in,link in match:
      if stop_all==1:
        break
      if dub=='yes':
        if 'מדובב' in name_in:
          cn=True
        else:
          cn=False
      else:
         cn=True
      
   
      if name in name_in and cn==True:
        y=requests.get(link).content
        regex2='<a href="/awa.+?to=(.+?)"'
        match2=re.compile(regex2).findall(y)
        
        for links in match2:
         if stop_all==1:
             break
         if '.jpg' not in links:
          match_in=urllib.unquote_plus(links)
    
          resolvable=resolveurl.HostedMediaFile(match_in).valid_url()
          if 'upf.co.il' in match_in:
            resolvable=True
            if "adblockLandingPage.php?url=" in match_in:
              match_in=match_in.replace("adblockLandingPage.php?url=",'file/')+'.html'
    
          name1,match_s,res,check=server_data(match_in,original_title)
          if check and resolvable:
            all_links.append((name1,match_in,match_s,res))
            links_fun=all_links
    return all_links
def search_lists(original_title,name_o,show_original_year,id=None):
    global links_list,stop_all
    all_links=[]
    imdb=None
    if id!=None:
            imdbid_data=domain_s+'api.themoviedb.org/3/movie/%s?api_key=34142515d9d23817496eeb4ff1d223d0'%id
            x=requests.get(imdbid_data).json()
            imdb=x['imdb_id']
    lists=[domain_s+'raw.githubusercontent.com/shimonar/sh/master/%D7%94%D7%A0%D7%95%D7%A7%D7%9D%20%D7%94%D7%A8%D7%90%D7%A9%D7%95%D7%9F%20.txt']
    for item in lists:
      if stop_all==1:
        break
      if ("_encoded") in item:
        item=u_list(item.split('_encoded')[0])
      if len (item)>0:
       if 'http' not in item:
         item=domain_s+'pastebin.com/raw/'+item

       paste_list=requests.get(item).content
      

       
      
       regex='<it.+?>(.+?)</it'
       match_in_up=re.compile(regex).findall(paste_list)
          
       all_links_o=[]
       for all_data in match_in_up:
            if stop_all==1:
                  break
            regex_in='(.+?)="(.+?)"'
            #match_in=re.compile(regex_in).findall(all_data)
            match_in=all_data.split('=')
            
            regex_data='data=@@(.+?)}@@'
            match_data=re.compile(regex_data).findall(all_data)
 
            name='ללא שם - '
            link=' '
            icon=' '
            image=' '
            plot=' '
            data=' '

            try:
                name=match_in[1].replace('"',"").split("&")[0]
                link=match_in[2].replace('"',"").split("&")[0]
                icon=match_in[3].replace('"',"").split("&")[0]
                image=match_in[4].replace('"',"").split("&")[0]
                plot=match_in[5].replace('"',"").split("&")[0]
                if (match_in[0][0])=='name':
                  name=match_in[0][1]
                if (match_in[1][0])=='&link':
                  link=match_in[1][1]
                if (match_in[2][0])=='&icon':
                  icon=match_in[2][1]
                if (match_in[3][0])=='&fanart':
                  image=match_in[3][1]
                if (match_in[4][0])=='&plot':
                  plot=match_in[4][1]
                if len(match_data)>0:
                  data=match_data[0]+'}'
            except:
              pass
            if imdb!=None:
               if imdb in data:
                temp_link=link
                regex='//(.+?)/'
                match=re.compile(regex).findall(link)
                if len(match)>0:
                  server=match[0]
                else:
                   server=link
                if link not in all_links_o:
                  all_links_o.append(link)
                  all_links.append((name,link,server,' '))
                  links_list=all_links
            else:
             if (name_o in name ):
                temp_link=link
                regex='//(.+?)/'
                match=re.compile(regex).findall(link)
                if len(match)>0:
                  server=match[0]
                else:
                   server=link
                if link not in all_links_o:
                  all_links_o.append(link)
                  all_links.append((name,link,server,' '))
                  links_list=all_links
               
                
    return links_list
def search_lists2(original_title,name_o,show_original_year):
    global links_list2,stop_all
    all_links=[]
    lists=[domain_s+'goo.gl/vCA3Mq']
    for item in lists:
      if stop_all==1:
        break
      if ("_encoded") in item:
        item=u_list(item.split('_encoded')[0])
      if len (item)>0:
       if 'http' not in item:
         item=domain_s+'pastebin.com/raw/'+item

       paste_list=requests.get(item).content
      

       
      
       regex='<it.+?>(.+?)</it'
       match_in_up=re.compile(regex).findall(paste_list)
          
    
       for all_data in match_in_up:
            if stop_all==1:
                 break
            regex_in='(.+?)="(.+?)"'
            #match_in=re.compile(regex_in).findall(all_data)
            match_in=all_data.split('=')
            
            regex_data='data=@@(.+?)}@@'
            match_data=re.compile(regex_data).findall(all_data)
 
            name='ללא שם - '
            link=' '
            icon=' '
            image=' '
            plot=' '
            data=' '

            try:
                name=match_in[1].replace('"',"").split("&")[0]
                link=match_in[2].replace('"',"").split("&")[0]
                icon=match_in[3].replace('"',"").split("&")[0]
                image=match_in[4].replace('"',"").split("&")[0]
                plot=match_in[5].replace('"',"").split("&")[0]
                if (match_in[0][0])=='name':
                  name=match_in[0][1]
                if (match_in[1][0])=='&link':
                  link=match_in[1][1]
                if (match_in[2][0])=='&icon':
                  icon=match_in[2][1]
                if (match_in[3][0])=='&fanart':
                  image=match_in[3][1]
                if (match_in[4][0])=='&plot':
                  plot=match_in[4][1]
                if len(match_data)>0:
                  data=match_data[0]+'}'
            except:
              pass
          
            if name_o in name or name_o in data:
                temp_link=link
                regex='//(.+?)/'
                match=re.compile(regex).findall(link)
                if len(match)>0:
                  server=match[0]
                else:
                   server=link
                all_links.append((name,link,server,' '))
                links_list2=all_links
                
    return links_list2
def get_jksp(original_title,heb_name,show_original_year):
    global links_jksp
    all_links=[]
    url=domain_s+'raw.githubusercontent.com/Jksp/jksp.repo/master/db/HebDub.json'
    html=requests.get(url).json()
    
    for item in html['movies']:
        
         if urllib.unquote_plus(heb_name) in item :
         
           name1=item
           link="https://www.rapidvideo.com/v/%s" % html['movies'][item]['video_id']
           
           all_links.append((name1,link,'rapidvideo','HD'))
           links_jksp=all_links
    return all_links
    
def search_dub(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name):
    global links_mx
    thread=[]
    all_data=[]
    original_title=original_title.replace('%3a','')
    if Addon.getSetting("movix")=='true':
       thread.append(Thread(get_movix,original_title,name,show_original_year))
    if Addon.getSetting("fun")=='true':
       thread.append(Thread(get_funlopy,original_title,name,show_original_year))
    if Addon.getSetting("snow")=='true':
       thread.append(Thread(get_serno,original_title,name,show_original_year))
    if Addon.getSetting("list")=='true':
       thread.append(Thread(search_lists,original_title,name,show_original_year))
       thread.append(Thread(search_lists2,original_title,name,show_original_year))
       
    if Addon.getSetting("lk")=='true':
       thread.append(Thread(get_linkia,'movie',original_title,heb_name,'','',season,episode,show_original_year,'yes'))
    if Addon.getSetting("jksp")=='true':
       thread.append(Thread(get_jksp,original_title,heb_name,show_original_year))
       
       
    title_size=0
    start_time = time.time()
    stop_all=0
    for td in thread:
      td.start()
      #td.join()
    max_time=int(Addon.getSetting("time_s"))
    if Addon.getSetting("dp")=='true':
        dp = xbmcgui . DialogProgress ( )
        dp.create('אנא המתן','מחפש מקורות', '','')
        dp.update(0, 'אנא המתן','מחפש מקורות', '' )
    num_live=0
    tt={}
    for i in range (0,30): 
      tt[i]=0
    while 1:
      num_live=0
     
      
     

      for threads in thread:
          num_live=0
          string_dp=''
          string_dp2=''
          still_alive=0
          for yy in range(0,len(thread)):
            if not thread[yy].is_alive():
              num_live=num_live+1
              tt[yy]="lightgreen"
            else:
              still_alive=1
              tt[yy]="red"
          elapsed_time = time.time() - start_time
             
          if Addon.getSetting("dp")=='true':
             zz=0
             if Addon.getSetting("movix")=='true':
                 string_dp=string_dp+('MX:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_mx)))
                 zz=zz+1
             if Addon.getSetting("fun")=='true':
                 string_dp=string_dp+('FN:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_fun)))
                 zz=zz+1
             if Addon.getSetting("snow")=='true':
                 string_dp=string_dp+('SN:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_sno)))
                 zz=zz+1
             if Addon.getSetting("list")=='true':
                 string_dp=string_dp+('FA:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_list)))
                 zz=zz+1
                 string_dp=string_dp+('OR:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_list2)))
                 zz=zz+1
             if Addon.getSetting("lk")=='true':
                 string_dp=string_dp+('LK:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_linkia)))
                 zz=zz+1
             if Addon.getSetting("jksp")=='true':
                 string_dp=string_dp+('JK:[COLOR %s]%s[/COLOR]'%(tt[zz],len(links_jksp)))
                 zz=zz+1
      if still_alive==0:
        break
      if Addon.getSetting("dp")=='true':
        if dp.iscanceled():
          dp_c=True
        else:
          dp_c=False
      else:
       dp_c=False
      if dp_c or elapsed_time>max_time: 
       for threads in thread:
         if threads.is_alive():
             stop_all=1
             threads._Thread__stop()
      xbmc.sleep(1000)
      if Addon.getSetting("dp")=='true':
          dp.update(int(((num_live* 100.0)/(len(thread))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),string_dp, string_dp2)
    if Addon.getSetting("dp")=='true':
      dp.close()
    for name,link,server,quality in links_jksp:
           fixed_q=fix_q(quality)

           se='-JK-'
           all_data.append(('[COLOR purple][JK] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q))
    for name,link,server,quality in links_linkia:
           fixed_q=fix_q(quality)

           se='-LK-'
           all_data.append(('[COLOR dodgerblue][LK] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q))
    for name,link,server,quality in links_mx:
           fixed_q=fix_q(quality)

           se='-MX-'
           all_data.append(('[COLOR crimson][MX] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q))
    for name,link,server,quality in links_fun:
           fixed_q=fix_q(quality)

           se='-FN-'
           all_data.append(('[COLOR lightgreen][FN] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q))
    
    for name,link,server,quality in links_sno:
           fixed_q=fix_q(quality)

           se='-SN-'
           all_data.append(('[COLOR lime][SN] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q))
    for name,link,server,quality in links_list:
           fixed_q=fix_q(quality)

           se='-FA-'
           all_data.append(('[COLOR khaki][FA] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q))
    
    for name,link,server,quality in links_list2:
           fixed_q=fix_q(quality)

           se='-OR-'
           all_data.append(('[COLOR orange][OR] '+name+" - "+server+'[/COLOR]', link,iconimage,fanart,description,show_original_year,quality,se,fixed_q))
    
    all_data=sorted(all_data, key=lambda x: x[8], reverse=False)
    playingUrlsList = []
    t=0
    for name,link,icon,image,plot,year,q,server,f_q in all_data:
      t=t+1
      if description==None:
         description=' '

      
      playingUrlsList.append(link+'$$$$$$$'+server+'$$$$$$$'+q+'$$$$$$$'+name+'$$$$$$$'+'[COLOR gold]'+q.decode('utf8')+'[/COLOR]\n[COLOR lightblue]'+server.decode('utf8')+'[/COLOR]\n'+plot)
      

    addLink( '[COLOR aqua][I]ניגון אוטומטי[/I][/COLOR]', json.dumps(playingUrlsList),6,False,iconimage,fanart,description,data=show_original_year,original_title=original_title.replace("%20"," "))
    for name,link,icon,image,plot,year,q,server,f_q in all_data:
      
      if server==None:
        server=' '
      if q==None:
        q=' '
      if plot==None:
        plot=' '
      name=name.replace("|"," ")
      addLink( name.decode('utf8'), link,5,False,icon,image,'[COLOR gold]'+q.decode('utf8')+'[/COLOR]\n[COLOR lightblue]'+server.decode('utf8')+'[/COLOR]\n'+plot.decode('utf8'),data=year,original_title=original_title.decode('utf8'),season=season,episode=episode,id=id)

def open_fav(url):
    save_file=os.path.join(user_dataDir,"fav.txt")
    if url=='movies':
      type='movies'
    elif url=='tv':
      type='tv'
    else:
      type='all'
    url=None
    name=None
    mode=None
    iconimage=None
    fanart=None
    description=None
    original_title=None
    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
    num=0
    for items in file_data:
       if len(items)>1:
            list1=items.split("$$")
            full_str=''
            for item_as in list1:
              full_str=full_str+chr(int(item_as))
            
            params=get_custom_params(full_str)
           
            url=None
            name=None
            mode=None
            iconimage=None
            fanart=None
            description=None
            original_title=None
            data=0
            id=' '
            season=0
            episode=0
            show_original_year=0
            heb_name=' '
            tmdbid=' '
            eng_name=' '
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
                    original_title=(params["original_title"])
            except:
                    pass
            try:        
                    id=(params["id"])
            except:
                    pass
            try:        
                    season=(params["season"])
            except:
                    pass
            try:        
                    episode=(params["episode"])
            except:
                    pass
            try:        
                    tmdbid=(params["tmdbid"])
            except:
                    pass
            try:        
                    eng_name=(params["eng_name"])
            except:
                    pass
            try:        
                    show_original_year=(params["show_original_year"])
            except:
                    pass
            try:        
                    heb_name=(params["heb_name"])
            except:
                    pass
            
            te1=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
            
            te2="&name="+(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&heb_name="+urllib.quote_plus(heb_name)
    
            te3="&data="+str(data)+"&original_title="+urllib.quote_plus(original_title)+"&id="+(id)+"&season="+str(season)
            te4="&episode="+str(episode)+"&tmdbid="+str(tmdbid)+"&eng_name="+(eng_name)+"&show_original_year="+(show_original_year)
     
           
            
            
            u=te1 + te2 + te3 + te4.decode('utf8')
            link="ActivateWindow(10025,%s,return)" % (u)
            if (type=='movies' and mode==4) or type=='all' or (type=='tv' and mode==7):
             addLink( name, link,99,True, iconimage,fanart,description,data=data,original_title=original_title,id=id,season=season,episode=episode,num_in_list=num)
       num=num+1

def remove_to_fav(plot):
    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
    
    if plot+'\n' in file_data:
      file_data.pop(file_data.index(plot+'\n'))
      change=1
    if change>0:
       
          file = open(save_file, 'w')
          file.write('\n'.join(file_data))
          file.close()
          xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'נמחק')).encode('utf-8'))
def remove_fav_num(plot):
    file_data=[]
    change=0

    if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()

    if len(file_data)>=int(plot):
      file_data.pop(int(plot))
      change=1
    if change>0:
       
          file = open(save_file, 'w')
          file.write('\n'.join(file_data))
          file.close()
          xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'נמחק')).encode('utf-8'))
          xbmc.executebuiltin('Container.Refresh')
def play_by_subs(name,urls,iconimage,fanart,description_o,data,original_title,season,episode,id,eng_name,saved_name,one_list=False):
   all_magents=json.loads(urls)
   
   all_subs_in=json.loads(urllib.unquote_plus(original_title))
   all_data=[]
   for mag in all_magents:
     
     title=mag['name']
     pre=check_pre(title,all_subs_in)
     description='PE:'+str(mag['peers'])+'/Se:'+str(mag['seeds'])+'\n'+'Size:'+mag['size']+'\n'+description_o
     if 1:#try:
          info=(PTN.parse(title))
          
          if 'resolution' in info:
             res=info['resolution']
          else:
             if "HD" in title:
              res="HD"
             elif "720" in title:
              res="720"
             elif "1080" in title:
               res="1080"
             else:
               res=' '
     #except:
     #   res=' '
     #   pass
     fixed_q=fix_q(res)
     all_data.append((str(pre)+'% '+ title,mag['uri'],urllib.quote_plus(str(mag)),pre,res,fixed_q,description))
   if Addon.getSetting("order")=='0':
      all_data=sorted(all_data, key=lambda x: x[5], reverse=False)
   else:
       all_data=sorted(all_data, key=lambda x: x[3], reverse=True)
   for name,link,origi,pre,res,fixed_q,description in all_data:
     if one_list==True:
      name='[I]'+name+'[/I]'
     addLink(name, link,22,False, iconimage,fanart,'[COLOR aqua]'+res+'[/COLOR]\n'+description,original_title=origi,id=id,data=data)
def activate_torrent(sub,urls,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,saved_name):

    from play import play
    items=eval(urllib.unquote_plus(original_title))

    title=sub.split("% ")[1]
    try:
      s=int (season)
      tv_mode='tv'
    except:
      tv_mode='movie'
      pass
    if tv_mode=='movie':
      payload = '?search=movie&imdb_id=%s&title=%s&year=%s' % (id, title, data)
      play(urls, payload, items)
def server_test():
    addLink('סריקת שרתים ישירים', 'www',33,False, ' ',' ',' ')
    for name in all_servers:
      addLink(name, name,23,False, ' ',' ',' ')
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass


def run_test(name_o):
    global stop_all

    original_title='The%20Matrix'
    show_original_year="1999"
    year='1999'
    year_w=year
    name=original_title
    sources=[]
    error=''
    id='603'
    #tv
    result=''
    thread=[]
    original_title_tv='The%20Flash'
    show_original_year_tv="2014"
    season_n='04'
    episode_n='05'
    season='4'
    episode='5'
    name_tv=original_title_tv
    id_tv='60735'
    if name_o=='Dlt' or name_o=='Afdah'  or name_o=='Dwatch' or name_o=='Seil' or name_o=='List' or name_o=='List2' or name_o=='fun':
       option=['Movie']
    elif  name_o=='moviesak' or name_o=='Cin' or name_o=='We' or name_o=='Showbox' or name_o=='Cooltvzion' or name_o=='Ct' or name_o=='Sdarot' or name_o=='tvl':
       option=['Tv']
    else:
      option=['Tv','Movie']
    activated_arr=[]
    ret=xbmcgui.Dialog().select("בחר סוג", option)
    if ret==-1:
        sys.exit()
    if name_o=='Dlt' or name_o=='Afdah'  or name_o=='Dwatch' or name_o=='Seil' or name_o=='List' or name_o=='List2' or name_o=='fun':
      ret=1
      

    if name_o=='Dlt' or name_o=='Check All':
       
        if ret==1:
          activated_arr.append('dlt')
          thread.append(Thread(get_dlt,'movie',original_title,name,'','','','',show_original_year))

    if name_o=='M4u'or name_o=='Check All':
         activated_arr.append('m4u')

         if ret==1:
          thread.append(Thread(get_m4u,'movie',original_title,name,season_n,episode_n,season,episode,show_original_year))

         if ret==0:
          thread.append(Thread(get_m4u,'tv',original_title_tv,name_tv,season_n,episode_n,season,episode,show_original_year_tv))
          for name,lk,sr,res in sources:
            
            result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'


    if name_o=='Magnet' or name_o=='Check All':
         activated_arr.append('magnet')
         result=result+'\n[COLOR aqua]Magnet- Movies[/COLOR]\n'
        
         if ret==1:
          thread.append(Thread(get_magnet,'movie',original_title.replace("%20"," "),'','',id,show_original_year))

         if ret==0:
          thread.append(Thread(get_magnet,'tv',original_title_tv.replace("%20"," "),season,episode,id_tv,show_original_year_tv))

            
         
        
          
          
          
    if name_o=='Rd_tvr' or name_o=='Check All':
         activated_arr.append('rd_tvr')

         if ret==1:
          tv_movie='movie'
   
          thread.append(Thread(get_rd_tvr,tv_movie,original_title,name,'','','','',show_original_year))

         if ret==0:
          tv_movie='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_rd_tvr,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))

          
    if name_o=='Pf' or name_o=='Check All':
         activated_arr.append('pf')
    
         if ret==1:
          tv_movie='movie'
   
          thread.append(Thread(get_pf,tv_movie,original_title,name,'','','','',show_original_year))
          

         if ret==0:
          tv_movie='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_pf,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
         
          
    if name_o=='Afdah' or name_o=='Check All':
       
         if ret==1:
          activated_arr.append('afdah')
          tv_movie='movie'
   
          thread.append(Thread(get_afdah,tv_movie,original_title,name,'','','','',show_original_year))
          
            
  

    if name_o=='Seehd' or name_o=='Check All':
        
         activated_arr.append('seehd')

         if ret==1:
          
          tv_movie='movie'
          original_title='The%20Maze%20Runner'
          show_original_year="2014"
   
          thread.append(Thread(get_seehd,tv_movie,original_title,name,'','','','',show_original_year))

         if ret==0:
          tv_movie='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_seehd,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))

          
    if name_o=='Cin' or name_o=='Check All':

         if ret==0:
          activated_arr.append('cin')
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_cin,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))

    if name_o=='Upto' or name_o=='Check All':
        
         activated_arr.append('upto')

         if ret==1:
          
          tv_movie='movie'
   
   
          thread.append(Thread(get_upto,tv_movie,original_title,name,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_upto,tv_movie,original_title,name,season_n,episode_n,season,episode,year))
          
    if name_o=='Direct' or name_o=='Check All':
        
         if ret==0:
          activated_arr.append('direct')
          tv_mode='tv'
          original_title=original_title_tv
          year_w=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_direct_links,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))

         if ret==1:
         
          activated_arr.append('direct')
          tv_mode='movie'
   
          original_title='the maze runner'
          year='2014'
          thread.append(Thread(get_direct_links,tv_mode,original_title,name,season_n,episode_n,season,episode,year))
    if name_o=='We' or name_o=='Check All':
        
         

       
         if ret==0:
          activated_arr.append('we')
          tv_mode='tv'
          original_title=original_title_tv
          year_w=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_we,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))
        

    if name_o=='Dwatch' or name_o=='Check All':
        
         

         if ret==1:
         
          activated_arr.append('dwatch')
          tv_mode='movie'
   

          thread.append(Thread(get_dwatch,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))
    if name_o=='Cmovies' or name_o=='Check All':
        
         activated_arr.append('cmovies')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_cmovies,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_cmovies,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))
#jump here
    if name_o=='Flix' or name_o=='Check All':
        
         activated_arr.append('flix')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_flix,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          
          id=id_tv
          thread.append(Thread(get_flix,tv_mode,original_title,name,season_n,episode_n,season,episode,year_w))

    if name_o=='Showbox' or name_o=='Check All':
        
         

         if ret==0:
          activated_arr.append('showbox')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_showbox,tv_movie,original_title,season_n,episode_n,season,episode,year))
    if name_o=='Put' or name_o=='Check All':
        
         activated_arr.append('put')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_put,tv_movie,original_title,name,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_put,tv_movie,original_title,name,season_n,episode_n,season,episode,year))
          
    if name_o=='Seil' or name_o=='Check All':
        
         activated_arr.append('sil')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
          name=('הנסיכה והצפרדע')
          thread.append(Thread(get_seretil,tv_movie,original_title,name,season_n,episode_n,season,episode,year))
    if name_o=='Sc' or name_o=='Check All':
        
         activated_arr.append('sc')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_sc,tv_movie,original_title,name,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_sc,tv_movie,original_title,name,season_n,episode_n,season,episode,year))
    
    if name_o=='Goo' or name_o=='Check All':
        
         activated_arr.append('gos')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_goo,tv_movie,original_title,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_goo,tv_movie,original_title,season_n,episode_n,season,episode,year))
          
          
    if name_o=='Tmp' or name_o=='Check All':
        
         activated_arr.append('tmp')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_tmp,tv_movie,original_title,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_tmp,tv_movie,original_title,season_n,episode_n,season,episode,year))
          
          
    if name_o=='Ava' or name_o=='Check All':
        
         activated_arr.append('ava')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
          original_title='Maze Runner The Death Cure'
          year="2018"
          thread.append(Thread(get_ava,tv_movie,original_title,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_ava,tv_movie,original_title,season_n,episode_n,season,episode,year))
          
          
    if name_o=='Cooltvzion' or name_o=='Check All':
        
         

        
         if ret==0:
          activated_arr.append('cooltvzion')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_cooltvzion,tv_movie,original_title,season_n,episode_n,season,episode,year))
    if name_o=='Dl20' or name_o=='Check All':
        
         activated_arr.append('dl20')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_dl20,tv_movie,original_title,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_dl20,tv_movie,original_title,season_n,episode_n,season,episode,year))
          
    if name_o=='Hdonline' or name_o=='Check All':
        
         activated_arr.append('hdonline')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
   
          thread.append(Thread(get_hdonline,tv_movie,original_title,season_n,episode_n,season,episode,year))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_hdonline,tv_movie,original_title,season_n,episode_n,season,episode,year))
          
    if name_o=='Sp' or name_o=='Check All':
        
         activated_arr.append('sp')

         if ret==1:
          
          tv_movie='movie'
          tv_mode='movie'
          title='Rogue One'
          name='רוג אחת: מלחמת הכוכבים' 
          thread.append(Thread(get_sp,title,name,'%20','%20'))

         if ret==0:
          tv_movie='tv'
          tv_mode='tv'
          title=original_title_tv
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          name='הפלאש'
          thread.append(Thread(get_sp,title,name,season,episode))
          
    if name_o=='List' or name_o=='Check All':
        
         

         if ret==1:
          activated_arr.append('list')
          tv_movie='movie'
          tv_mode='movie'
          
          original_title='son of batman' 
          name='בנו של באטמן'
          thread.append(Thread(search_lists,original_title,name,show_original_year))

    if name_o=='List2' or name_o=='Check All':
        
         

         if ret==1:
          activated_arr.append('list2')
          tv_movie='movie'
          tv_mode='movie'
          
          original_title='lost and found' 
          name='אבידות ומציאות'
          thread.append(Thread(search_lists2,original_title,name,show_original_year))
         

    if name_o=='Sno' or name_o=='Check All':
  
         

         if ret==1:
          activated_arr.append('sno')
          tv_movie='movie'
          tv_mode='movie'
          
          original_title='black panther' 
          name='הפנתר השחור'
          thread.append(Thread(get_serno,original_title,name,show_original_year,'No'))
         
    if name_o=='fun' or name_o=='Check All':
        
         

         if ret==1:
          activated_arr.append('fun')
          tv_movie='movie'
          tv_mode='movie'
          
          original_title='shrek 2' 
          name='שרק 2'
          thread.append(Thread(get_funlopy,original_title,name,show_original_year,'no'))
    if name_o=='mx' or name_o=='Check All':
        
         

         if ret==1:
          activated_arr.append('mx')
          tv_movie='movie'
          tv_mode='movie'
          
          original_title='shrek 2' 
          name='שרק 2'
          thread.append(Thread(get_movix,original_title,name,show_original_year,'no'))

    if name_o=='daily' or name_o=='Check All':
        
         if ret==0:
          activated_arr.append('daily')
          url2=domain_s+'api.dailymotion.com//videos?fields=available_formats,description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search=%s&sort=relevance&limit=100&family_filter=1'%((original_title.replace(" ","%20"))+"%20S"+season_n+'E'+episode_n)
          thread.append(Thread(get_daily,url2,original_title_tv,season_n,episode_n,season,episode))

         if ret==1:
          activated_arr.append('daily')
          tv_movie='movie'
          tv_mode='movie'
          
          original_title='shrek 2' 
          name='שרק 2'
          year="2004"
          url2=domain_s+'api.dailymotion.com//videos?fields=available_formats,description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&search=%s&sort=relevance&limit=100&family_filter=1'%(original_title.replace(" ","%20")+"%20"+year)
          thread.append(Thread(get_daily,url2,original_title,'%20','%20','%20','%20'))

    if name_o=='Ct' or name_o=='Check All':
        
         

         if ret==0:
          activated_arr.append('ct')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_ct,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
          
    if name_o=='Sdarot' or name_o=='Check All':
        
        

         if ret==0:
          activated_arr.append('sd')
          tv_movie='tv'
          tv_mode='tv'
          name='פאודה'
          season='2'
          episode='1'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_sdarot,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
          
    if name_o=='Linkia' or name_o=='Check All':
        
         

         if ret==1:
          activated_arr.append('linkia')
          tv_movie='movie'
          tv_mode='movie'
          name=urllib.quote_plus('אחותי כלה')

          show_original_year='2017'
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_linkia,tv_movie,original_title,name,'','','','',show_original_year))
         if ret==0:
          activated_arr.append('linkia')
          tv_movie='tv'
          tv_mode='tv'
          name=urllib.quote_plus('פאודה')
          season='2'
          episode='1'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_linkia,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year))
    if name_o=='Uni' or name_o=='Check All':
        
         

         if ret==1:
          activated_arr.append('Uni')
          tv_movie='movie'
          tv_mode='movie'
          


          year_w=show_original_year
          year=show_original_year
        
          thread.append(Thread(get_uni,tv_movie,original_title,name,'','','','',show_original_year,id))
         if ret==0:
          activated_arr.append('Uni')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          season='2'
          episode='1'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_uni,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if name_o=='2ddl' or name_o=='Check All':
        
         

         if ret==1:
          activated_arr.append('2ddl')
          tv_movie='movie'
          tv_mode='movie'
          
          original_title='Maze Runner The Death Cure'
          show_original_year="2018"

          
          
        
          thread.append(Thread(get_2ddl,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('2ddl')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          season='4'
          episode='17'
          season_n='04'
          episode_n='17'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_2ddl,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
          
          
    if name_o=='filep' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('filep')
              tv_movie='movie'
              tv_mode='movie'

              thread.append(Thread(get_filepursuit,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('filep')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
         
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_filepursuit,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if name_o=='Onitube' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('onitube')
              tv_movie='movie'
              tv_mode='movie'

              thread.append(Thread(get_onitube,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('onitube')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
         
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_onitube,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if name_o=='tvl' or name_o=='Check All':
   
         if ret==0:
          activated_arr.append('tvl')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
         
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_tvl,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
          
    if name_o=='ftp' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('ftp')
              tv_movie='movie'
              tv_mode='movie'

              thread.append(Thread(get_ftp,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('ftp')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
         
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_ftp,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if name_o=='reqzone' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('reqzone')
              tv_movie='movie'
              tv_mode='movie'
              original_title='the maze runner'
              year='2014'
              thread.append(Thread(get_raqlink,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('reqzone')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
         
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_raqlink,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if name_o=='moviesak' or name_o=='Check All':
         
       
         if ret==0:
          activated_arr.append('moviesak')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
         
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          #season='2'
          #episode='2'
          #season_n='02'
          #episode_n='02'
          id=id_tv
          thread.append(Thread(get_links_moviesak,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if name_o=='getgona' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('getgona')
              tv_movie='movie'
              tv_mode='movie'
         
              thread.append(Thread(get_gonaw,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('getgona')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          episode='6'
          episode_n='06'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_gonaw,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
          
    if name_o=='shuid' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('shuid')
              tv_movie='movie'
              tv_mode='movie'
              original_title='the maze runner'
              year='2014'
              thread.append(Thread(get_shuid,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('shuid')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          episode='6'
          episode_n='06'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_shuid,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))

    if name_o=='kizi' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('kizi')
              tv_movie='movie'
              tv_mode='movie'
         
              thread.append(Thread(get_kizi,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('kizi')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          episode='6'
          episode_n='06'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_kizi,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
    if name_o=='bmovie' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('bmovie')
              tv_movie='movie'
              tv_mode='movie'
         
              thread.append(Thread(get_bmovie,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('bmovie')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          episode='5'
          episode_n='01'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_bmovie,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
          
    if name_o=='1movie' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('1movie')
              tv_movie='movie'
              tv_mode='movie'
         
              thread.append(Thread(get_1movie,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('1movie')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          episode='5'
          episode_n='01'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_1movie,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
          
    if name_o=='scn' or name_o=='Check All':
         
         if ret==1:
              activated_arr.append('scn')
              tv_movie='movie'
              tv_mode='movie'
         
              thread.append(Thread(get_scnsrc,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
         if ret==0:
          activated_arr.append('scn')
          tv_movie='tv'
          tv_mode='tv'
          original_title=original_title_tv
          episode='5'
          episode_n='05'
          show_original_year=show_original_year_tv
          year_w=show_original_year_tv
          year=show_original_year_tv
          id=id_tv
          thread.append(Thread(get_scnsrc,tv_movie,original_title,name,season_n,episode_n,season,episode,show_original_year,id))
          
    title_size=0
    start_time = time.time()
    stop_all=0
    for td in thread:
      td.start()
    num_live=0
    tt={}
    for i in range (0,30): 
      tt[i]=0
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel('Results')
            win.getControl(5).setText(text)
            return
        except:
            pass
      
    close_all=0

    while 1:
         num_live=0
         zz=0
         for threads in thread:
              num_live=0
              string_dp=''
              string_dp2=''
              still_alive=0
              for yy in range(0,len(thread)):
                if not thread[yy].is_alive():
                  num_live=num_live+1
                  tt[yy]="lightgreen"
                else:
                  still_alive=1
                  tt[yy]="red"
              elapsed_time = time.time() - start_time
              
              
              if "scn" in activated_arr:
                 result=''
                 
                 for name,lk,sr,res in links_scn:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('1M:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_scn),result))
                 zz=zz+1
              if "1movie" in activated_arr:
                 result=''
                 
                 for name,lk,sr,res in links_1movie:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('1M:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_1movie),result))
                 zz=zz+1
              if "bmovie" in activated_arr:
                 result=''
                 
                 for name,lk,sr,res in links_bmovie:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('BV:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_bmovie),result))
                 zz=zz+1
              if "kizi" in activated_arr:
                 result=''
                 
                 for name,lk,sr,res in links_kizi:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('KZ:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_kizi),result))
                 zz=zz+1
              if "shuid" in activated_arr:
                 result=''
                 for name,lk,sr,res in links_shu:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('SU:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_shu),result))
                 zz=zz+1
              if "getgona" in activated_arr:
                 result=''
                 for name,lk,sr,res in links_gona:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('GET:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_gona),result))
                 zz=zz+1
              if "moviesak" in activated_arr:
                 result=''
                 for name,lk,sr,res in links_moviesak:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('REQ:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_moviesak),result))
                 zz=zz+1
              if "reqzone" in activated_arr:
                 result=''
                 for name,lk,sr,res in links_reqzone:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('REQ:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_reqzone),result))
                 zz=zz+1
              if "ftp" in activated_arr:
                 result=''
                 for name,lk,sr,res in links_ftp:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('FTP:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_ftp),result))
                 zz=zz+1
              if "tvl" in activated_arr:
                 result=''
                 for name,lk,sr,res in links_tvl:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('Tvl:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_tvl),result))
                 zz=zz+1
              if "onitube" in activated_arr:
                 result=''
                 for name,lk,sr,res in link_onitube:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('Onitube:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_onitube),result))
                 zz=zz+1
              if "filep" in activated_arr:
                 result=''
                 for name,lk,sr,res in link_filepursuit:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('Filep:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_filepursuit),result))
                 zz=zz+1
              if "2ddl" in activated_arr:
                 result=''
                 for name,lk,sr,res in link_2ddl:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('2DDL:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_2ddl),result))
                 zz=zz+1
              if "magnet" in activated_arr:
                 result=''
                 for mag in (all_magnet):
            
                     result=result+'[COLOR lightblue]'+mag['name']+'[/COLOR]'+' - '+mag['size']+'\n'
                 if name_o=='Check All':
                  result=''
                 string_dp=string_dp+('Magnet:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( all_magnet),result))
                 zz=zz+1
              if "afdah" in activated_arr:
          
                 result=''
                 for name,lk,sr,res in link_afdah:
            
                     result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('Afa:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_afdah),result))
                 zz=zz+1
              
         
              if ("seehd") in activated_arr:
                 result=''
                 for name,lk,sr,res in link_seehd:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('SHD:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_seehd),result))
                 zz=zz+1
              if ("upto") in activated_arr:
                 result=''
                 for name,lk,sr,res in link_upto:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('UPT:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_upto),result))
                 zz=zz+1
              if ("direct") in activated_arr:
                 result=''
                 for name,lk,sr,res in link_direct:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('DIR:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_direct),result))
                 zz=zz+1
              
              
              if ("we") in activated_arr:
                 result=''
                 for name,lk,sr,res in links_we:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('WE:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_we),result))
                 zz=zz+1
              
              
              if ("dwatch") in activated_arr:
                 result=''
                 for name,lk,sr,res in links_dwatch:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('DW:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_dwatch),result))
                 zz=zz+1
              
              
              if ("cmovies") in activated_arr:
                 result=''
                 for name,lk,sr,res in links_cmovies:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('CM:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_cmovies),result))
                 zz=zz+1
              if ("flix") in activated_arr:
                 result=''
                 for name,lk,sr,res in links_flix:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('FLIX:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_flix),result))
                 zz=zz+1
              if ("put") in activated_arr:
                 result=''
                 for name,lk,sr,res in links_put:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('PUT:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_put),result))
                 zz=zz+1
              if ("sil") in activated_arr:
                 result=''
                 for name,lk,sr,res in links_seil:
                    
                    result=result+'[COLOR lightblue]'+name.decode('utf8')+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('SIL:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_seil),result))
                 zz=zz+1
                 
              if ("sc") in activated_arr:
                 result=''
                 for name,lk,sr,res in links_sc:
                    
                    result=result+'[COLOR lightblue]'+name.decode('utf8')+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('SC:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_sc),result))
                 zz=zz+1
              if ("tmp") in activated_arr:
                 result=''
                 for name,lk,sr,res in link_tmp:
                    
                    result=result+'[COLOR lightblue]'+name.decode('utf8')+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('Tmp:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_tmp),result))
                 zz=zz+1
              if ("cooltvzion") in activated_arr:
                result=''
                for name,lk,sr,res in cooltvzion:
                    
                    result=result+'[COLOR lightblue]'+name.decode('utf8')+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                if name_o=='Check All':
                    result=''
                string_dp=string_dp+('TVZ:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( cooltvzion),result))
                zz=zz+1
              if ("ava") in activated_arr:
                result=''
                for name,lk,sr,res in link_ava:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                if name_o=='Check All':
                    result=''
                string_dp=string_dp+('AV:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_ava),result))
                zz=zz+1
              if ("dl20") in activated_arr:
                result=''
                for name,lk,sr,res in link_dl20:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                if name_o=='Check All':
                    result=''
                string_dp=string_dp+('DL:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_dl20),result))
                zz=zz+1
              if ("hdonline") in activated_arr:
                result=''
                for name,lk,sr,res in link_hdonline:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                if name_o=='Check All':
                    result=''
                string_dp=string_dp+('HO:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_hdonline),result))
                zz=zz+1
              if ("showbox") in activated_arr:
                 result=''
                 for name,lk,sr,res in link_showbox:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('SB:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_showbox),result))
                 zz=zz+1
   
              if ("sp") in activated_arr:
                result=''
                for name,lk,sr,res in link_source1:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                if name_o=='Check All':
                    result=''
                string_dp=string_dp+('SP:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_source1),result))
                zz=zz+1
              if ("gos") in activated_arr:
              
                result=''
                for name,lk,sr,res in link_goo:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                if name_o=='Check All':
                    result=''
                string_dp=string_dp+('GO:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_goo),result))
                zz=zz+1
              if ("cin") in activated_arr:
                 result=''
                 for name,lk,sr,res in link_cin:
                    
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
                 if name_o=='Check All':
                    result=''
                 string_dp=string_dp+('CIN:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_cin),result))
                 zz=zz+1
               
              if ("pf") in activated_arr:
               result=''
               for name,lk,sr,res in links_pf:
            
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('PF:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_pf),result))
               zz=zz+1
              
              if ("dlt") in activated_arr:
               result=''
               for name,lk,sr,res in link_dlt:
            
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('DLT:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_dlt),result))
               zz=zz+1
               
              
              if ("rd_tvr") in activated_arr:
               result=''
               for name,lk,sr,res in rd_tvr:
            
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('RD:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( rd_tvr),result))
               zz=zz+1
              
              if ("list") in activated_arr:
               result=''
               for name,lk,sr,res in links_list:
            
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('List:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_list),result))
               zz=zz+1
               
              if ("list2") in activated_arr:
               result=''
               for name,lk,sr,res in links_list2:
            
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('List2:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_list2),result))
               zz=zz+1
               
              if "m4u" in activated_arr:
               result=''
               for name,lk,sr,res in links_m4u:
            
                 result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('M4u:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_m4u),result))
               zz=zz+1
               
              if ("sno") in activated_arr:
               result=''
               for name,lk,sr,res in links_sno:
            
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('Sno:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_sno),result))
               zz=zz+1
               
              if ("fun") in activated_arr:
               result=''
               for name,lk,sr,res in links_fun:
            
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('Fun:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_fun),result))
               zz=zz+1
               
              if ("mx") in activated_arr:
               result=''
               for name,lk,sr,res in links_mx:
            
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('Mx:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_mx),result))
               zz=zz+1
              
              if ("daily") in activated_arr:
               result=''
               for name,lk,sr,res in link_daily:
          
                  result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('daily:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_daily),result))
               zz=zz+1
               
              if ("ct") in activated_arr:
               result=''
               for name,lk,sr,res in link_ct:
            
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('Ct:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( link_ct),result))
               zz=zz+1

              if ("sd") in activated_arr:
               result=''
               for name,lk,sr,res in links_sdarot:
            
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('Sd:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_sdarot),result))
               zz=zz+1
               
              if ("linkia") in activated_arr:
               result=''
               for name,lk,sr,res in links_linkia:
            
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('Link:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_linkia),result))
               zz=zz+1

              if ("Uni") in activated_arr:
               result=''
               for name,lk,sr,res in links_uni:
            
                    result=result+'[COLOR lightblue]'+name+'[/COLOR]'+' - '+lk+' - '+sr+' - '+res+'\n'
               if name_o=='Check All':
                result=''
               string_dp=string_dp+('Link:[COLOR %s]%s[/COLOR] - %s'%(tt[zz],len( links_uni),result))
               zz=zz+1
              string_dp=string_dp.replace("	"," ").replace("  "," ").strip()
              win.getControl(5).setText(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+'\n'+string_dp)
              
              #dp.update(int(((num_live* 100.0)/(len(thread))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),string_dp, string_dp2)
              xbmc.sleep(100)
              if xbmc.getCondVisibility( "Window.IsActive(10147)")==0:
              #  dp.close()
              
                for threads in thread:
                     if threads.is_alive():
                         stop_all=1
                         threads._Thread__stop()
                logging.warning("Stop_All")
                sys.exit()
                break
                
              xbmc.sleep(1000)
    xbmc.executebuiltin('Dialog.Close(okdialog, true)')
    sys.exit()
def open_settings():
    __settings__.openSettings()
def play_trailer_f(id,tv_movie):
    import random
    global search_done
    if tv_movie=='movie':
      url_t='http://api.themoviedb.org/3/movie/%s/videos?api_key=34142515d9d23817496eeb4ff1d223d0'%id
    else:
      url_t='http://api.themoviedb.org/3/tv/%s/videos?api_key=34142515d9d23817496eeb4ff1d223d0'%id
    html_t=requests.get(url_t).json()

    if len(html_t['results'])>0:
        vid_num=random.randint(0,len(html_t['results'])-1)
    else:
      return 0
    video_id=(html_t['results'][vid_num]['key'])
    from pytube import YouTube
    playback_url = YouTube(domain_s+'www.youtube.com/watch?v='+video_id).streams.first().download()

    if search_done==0:
      xbmc.Player().play(playback_url)
def play_trailer(id):
    url_t='http://api.themoviedb.org/3/movie/%s/videos?api_key=34142515d9d23817496eeb4ff1d223d0'%id
    html_t=requests.get(url_t).json()
    video_id=(html_t['results'][0]['key'])
    from pytube import YouTube
    playback_url = YouTube(domain_s+'www.youtube.com/watch?v='+video_id).streams.first().download()
     
   
    
    #playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
    item = xbmcgui.ListItem(path=playback_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
def movie_recomended():
   from random import randint
   save_file=os.path.join(user_dataDir,"fav_movie.txt")
   file_data=[]
   change=0
   
   
   if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
   else:
     xbmcgui.Dialog().ok('שגיאה', ':-) לא קיימת היסטוריית צפייה , תתחיל לראות משהו למי אתה מחכה??')
     sys.exit()
   count=0
   x=0
   url_array=[]
   new_name_array=[]
   while count<5:
    id=file_data[randint(0, len(file_data)-1)]
    x=x+1
    if x==len(file_data):
      break
    
    if len(id)>1 and '%' not in id:
     url=domain_s+'api.themoviedb.org/3/movie/%s/recommendations?api_key=34142515d9d23817496eeb4ff1d223d0&language=heb&page=1'%id.replace('\n','')
     count=count+1
     
     if url not in url_array:
       url_array.append(url)
  
       new_name_array=get_movies(url,0,reco=1,new_name_array=new_name_array)
def tv_recomended():
   from random import randint
   save_file=os.path.join(user_dataDir,"fav_tv.txt")
   file_data=[]
   change=0
   
   
   if os.path.exists(save_file):
        f = open(save_file, 'r')
        file_data = f.readlines()
        f.close()
   else:
     xbmcgui.Dialog().ok('שגיאה', ':-) לא קיימת היסטוריית צפייה , תתחיל לראות משהו למי אתה מחכה??')
     sys.exit()
   count=0
   x=0
   url_array=[]
   while count<4:
    id=file_data[randint(0, len(file_data)-1)]
    x=x+1
    if x==len(file_data):
      break
    
    if len(id)>1 and '%' not in id:
          
     url=domain_s+'api.themoviedb.org/3/tv/%s/recommendations?api_key=34142515d9d23817496eeb4ff1d223d0&language=heb&page=1'%id.replace('\n','')
     
     count=count+1
     if url not in url_array:
       url_array.append(url)
       get_movies(url,0,reco=1)
 
 
def latest_dvd(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.dvdsreleasedates.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    url_g=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
    html_g=requests.get(url_g).json()
    
    html_o=requests.get(url,headers=headers).content
    regex="'fieldtable-inner'.+?<a id='.+?'></a>(.+?)<(.+?)</table></td></tr>"
    match=re.compile(regex,re.DOTALL).findall(html_o)
    name_array=[]
    for dat,rest in match:
      addNolink('[COLOR aqua][I]'+dat+'[/I][/COLOR]','www',199,False,iconimage=domain_s+'pbs.twimg.com/profile_images/421736697647218688/epigBm2J.jpeg',fanart='http://www.dream-wallpaper.com/free-wallpaper/cartoon-wallpaper/spawn-wallpaper/1280x1024/free-wallpaper-24.jpg')
      regex="'http://www.imdb.com/title/(.+?)/'"
      match_in=re.compile(regex,re.DOTALL).findall(rest)
     

      for imdb in match_in:
        if imdb not in name_array:
            name_array.append(imdb)
            url=domain_s+'api.themoviedb.org/3/find/%s?api_key=34142515d9d23817496eeb4ff1d223d0&external_source=imdb_id&language=heb'%imdb
            html=requests.get(url).json()
            for data in html['movie_results']:
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               year=str(data['first_air_date'].split("-")[0])
             else:
                year=str(data['release_date'].split("-")[0])
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             if 'original_title' in data:
               original_name=data['original_title']
               mode=4
               
               id=str(data['id'])
              
             else:
               original_name=data['original_name']
               id=str(data['id'])
               mode=7
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x] for x in data['genre_ids']])
             except:genere=''

             trailer = "plugin://plugin.video.allmoviesin?mode=25&url=www&id=%s" % id

             addDir3(new_name,url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer)
    if "a class='monthlink' href='" in html_o:
     regex="<a class='monthlink' href='(.+?)' >(.+?)<"
     match=re.compile(regex).findall(html_o)
     for link,name in match:
       addDir3('[COLOR aqua][I]'+name+'[/I][/COLOR]'.decode('utf8'),domain_s+'www.dvdsreleasedates.com'+link,28,' ',' ','תוצאות ישנות יותר'.decode('utf8'))
       break
SETTING_TRAKT_EXPIRES_AT = "trakt_expires_at"
SETTING_TRAKT_ACCESS_TOKEN = "trakt_access_token"
SETTING_TRAKT_REFRESH_TOKEN = "trakt_refresh_token"
CLIENT_ID = "8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6"
CLIENT_SECRET = "1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426"
def trakt_get_device_code():
    data = { 'client_id': CLIENT_ID }
    return call_trakt("oauth/device/code", data=data, with_auth=False)
def trakt_authenticate():
    code = trakt_get_device_code()
    token = trakt_get_device_token(code)
    if token:
        expires_at = time.time() + 60*60*24*30#*3
        Addon.setSetting(SETTING_TRAKT_EXPIRES_AT, str(expires_at))
        Addon.setSetting(SETTING_TRAKT_ACCESS_TOKEN, token["access_token"])
        Addon.setSetting(SETTING_TRAKT_REFRESH_TOKEN, token["refresh_token"])
        return True
    return False
def trakt_refresh_token():
    data = {        
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token",
        "refresh_token": unicode(Addon.getSetting(SETTING_TRAKT_REFRESH_TOKEN))
    }
    response = call_trakt("oauth/token", data=data, with_auth=False)
    if response:
        Addon.setSetting(SETTING_TRAKT_ACCESS_TOKEN, response["access_token"])
        Addon.setSetting(SETTING_TRAKT_REFRESH_TOKEN, response["refresh_token"])
def trakt_get_device_token(device_codes):
    data = {
        "code": device_codes["device_code"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    start = time.time()
    expires_in = device_codes["expires_in"]
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(("Authenticate Trakt"), ("Please go to https://trakt.tv/activate and enter the code"),str(device_codes["user_code"])    )
    try:
        time_passed = 0
        while not xbmc.abortRequested and not progress_dialog.iscanceled() and time_passed < expires_in:            
            try:
                response = call_trakt("oauth/device/token", data=data, with_auth=False)
            except requests.HTTPError, e:
                if e.response.status_code != 400:
                    raise e
                progress = int(100 * time_passed / expires_in)
                progress_dialog.update(progress)
                xbmc.sleep(max(device_codes["interval"], 1)*1000)
            else:
                return response
            time_passed = time.time() - start
    finally:
        progress_dialog.close()
        del progress_dialog
    return None
def call_trakt(path, params={}, data=None, is_delete=False, with_auth=True, pagination = False, page = 1):
    params = dict([(k, (v).encode('utf8')) for k, v in params.items() if v])
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': CLIENT_ID
    }


    API_ENDPOINT = "https://api-v2launch.trakt.tv"
    def send_query():
        if with_auth:
            try:
                expires_at = int(Addon.getSetting(SETTING_TRAKT_EXPIRES_AT))
                if time.time() > expires_at:
                    trakt_refresh_token()
            except:
                pass
            token =unicode( Addon.getSetting(SETTING_TRAKT_ACCESS_TOKEN))
            if token:
                headers['Authorization'] = 'Bearer ' + token
        if data is not None:
            assert not params
            return requests.post("{0}/{1}".format(API_ENDPOINT, path), json=data, headers=headers)
        elif is_delete:
            return requests.delete("{0}/{1}".format(API_ENDPOINT, path), headers=headers)
        else:
            return requests.get("{0}/{1}".format(API_ENDPOINT, path), params, headers=headers)

    def paginated_query(page):
        lists = []
        params['page'] = page
        results = send_query()
        if with_auth and results.status_code == 401 and xbmcgui.Dialog().yesno(("Authenticate Trakt"), ("You must authenticate with Trakt. Do you want to authenticate now?")) and trakt_authenticate():
            response = paginated_query(1)
            return response
        results.raise_for_status()
        results.encoding = 'utf-8'
        lists.extend(results.json())
        return lists, results.headers["X-Pagination-Page-Count"]

    if pagination == False:
        response = send_query()
        if with_auth and response.status_code == 401 and xbmcgui.Dialog().yesno(("Authenticate Trakt"),("You must authenticate with Trakt. Do you want to authenticate now?")) and trakt_authenticate():
            response = send_query()
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.json()
    else:
        (response, numpages) = paginated_query(page)
        return response, numpages
def get_movie_data(url):
    html=requests.get(url).json()
    return html
def get_trakt():
    trakt_lists=call_trakt("users/me/lists")
    
    my_lists = []
    
    for list in trakt_lists:
        my_lists.append({
            'name': list["name"],
            'user': list["user"]["username"],
            'slug': list["ids"]["slug"]
        })
    
    for item in my_lists:
        user = item['user']
        slug = item['slug']
        url=user+'$$$$$$$$$$$'+slug
        addDir3(item['name'],url,31,' ',' ',item['name'])
def get_trk_data(url):
        time_to_save=int(Addon.getSetting("save_time"))
        xxx=0
        data_in=url.split('$$$$$$$$$$$')
        user = data_in[0]
        slug = data_in[1]
        selected={'slug':data_in[1],'user':data_in[0]}
      
        src="tmdb"
        start_time = time.time()

        if selected['slug']=='movies':
              url_g=domain_s+'api.themoviedb.org/3/genre/movie/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
                 
        else:
             url_g=domain_s+'api.themoviedb.org/3/genre/tv/list?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'
        html_g=requests.get(url_g).json()
        if Addon.getSetting("dp")=='true':
                dp = xbmcgui.DialogProgress()
                dp.create("טוען סרטים", "אנא המתן", '')
                dp.update(0)
        responce=call_trakt("/users/{0}/lists/{1}/items".format(user, slug))
        
        new_name_array=[]

        for items in responce:
          if slug=='movies':
            url='http://api.themoviedb.org/3/movie/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['movie']['ids']['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          else:
            url='http://api.themoviedb.org/3/tv/%s?api_key=%s&language=he&append_to_response=external_ids'%(items['show']['ids']['tmdb'],'653bb8af90162bd98fc7ee32bcbbfb3d')
          
          html=cache.get(get_movie_data,time_to_save,url, table='pages')
          if 'The resource you requested could not be found' not in str(html):
             data=html
             
             if 'vote_average' in data:
               rating=data['vote_average']
             else:
              rating=0
             if 'first_air_date' in data:
               year=str(data['first_air_date'].split("-")[0])
             else:
 
                  year=str(data['release_date'].split("-")[0])
        
             if data['overview']==None:
               plot=' '
             else:
               plot=data['overview']
             if 'title' not in data:
               new_name=data['name']
             else:
               new_name=data['title']
             f_subs=[]
             if slug=='movies':
               original_name=data['original_title']
               mode=4
               
               id=str(data['id'])
               if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                 f_subs=cache.get(get_subs,9999,'movie',original_name,'0','0',id,year,True, table='pages')
               
               
             else:
               original_name=data['original_name']
               id=str(data['id'])
               mode=7
             if data['poster_path']==None:
              icon=' '
             else:
               icon=data['poster_path']
             if 'backdrop_path' in data:
                 if data['backdrop_path']==None:
                  fan=' '
                 else:
                  fan=data['backdrop_path']
             else:
                fan=html['backdrop_path']
             if plot==None:
               plot=' '
             if 'http' not in fan:
               fan=domain_s+'image.tmdb.org/t/p/original/'+fan
             if 'http' not in icon:
               icon=domain_s+'image.tmdb.org/t/p/original/'+icon
             genres_list= dict([(i['id'], i['name']) for i in html_g['genres'] \
                    if i['name'] is not None])
             try:genere = u' / '.join([genres_list[x['id']] for x in data['genres']])
             except:genere=''

   
            
             trailer = "plugin://plugin.video.allmoviesin?mode=25&url=www&id=%s" % id
             if new_name not in new_name_array:
              new_name_array.append(new_name)
              if Addon.getSetting("check_subs")=='true' or Addon.getSetting("disapear")=='true':
                  if len(f_subs)>0:
                    color='white'
                  else:
                    color='red'
                    
              else:
                 color='white'
              elapsed_time = time.time() - start_time
              if Addon.getSetting("dp")=='true':
                dp.update(int(((xxx* 100.0)/(len(html))) ), ' אנא המתן '+ time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),'[COLOR'+color+']'+new_name+'[/COLOR]')
              xxx=xxx+1

              addDir3('[COLOR '+color+']'+new_name+'[/COLOR]',url,mode,icon,fan,plot,data=year,original_title=original_name,id=id,rating=rating,heb_name=new_name,show_original_year=year,isr=isr,generes=genere,trailer=trailer)
          else:
            responce=call_trakt("movies/{0}".format(items['movie']['ids']['trakt']), params={'extended': 'full'})
           
            addNolink('[COLOR red][I]'+ responce['title']+'[/I][/COLOR]', 'www',999,False)
            
        if Addon.getSetting("dp")=='true':
          dp.close()
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
def reset_trakt():
    ret =xbmcgui.Dialog().yesno(("Authenticate Trakt"), ("אתה בטוח שאתה רוצה לאפס את אישור Trakt?"))
    if ret:
      Addon.setSetting(SETTING_TRAKT_ACCESS_TOKEN, '')
      xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'אישור Trakt אופס'.decode('utf8'))).encode('utf-8'))
def last_viewed(url_o):
    color='white'
    
    if url_o=='tv':
        dbcur.execute("SELECT  * FROM Lastepisode WHERE  type='tv' ")
    else:
       dbcur.execute("SELECT * FROM AllData WHERE  type='movie'")
    match = dbcur.fetchall()
    for item in match:
      name,url,icon,image,plot,year,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,tv_movie=item
      dates=' '
      
      if url_o=='tv':
          url=domain_s+'api.themoviedb.org/3/tv/%s/season/%s?api_key=34142515d9d23817496eeb4ff1d223d0&language=he'%(id,season)
         
          html=requests.get(url).json()
          ep=0
          f_episode=0
          catch=0
          counter=0
          for items in html['episodes']:
            if 'air_date' in items:
               #try:
                   datea=items['air_date']+'\n'
                   
                   a=(time.strptime(items['air_date'], '%Y-%m-%d'))
                   b=time.strptime(str(time.strftime('%Y-%m-%d')), '%Y-%m-%d')
                  
               
                   if a>b:
                     if catch==0:
                       f_episode=counter
                       
                       catch=1
                   counter=counter+1
                   
               #except:
               #      ep=0
          episode_fixed=int(episode)-1
          plot=html['episodes'][int(episode_fixed)]['overview']
          ep=len(html['episodes'])
          if (html['episodes'][int(episode_fixed)]['still_path'])==None:
            fanart=image
          else:
            fanart=domain_s+'image.tmdb.org/t/p/original/'+html['episodes'][int(episode_fixed)]['still_path']
          if f_episode==0:
            f_episode=ep
          data_ep='[COLOR aqua]'+'עונה '+season+'-פרק '+episode+ '[/COLOR]\n[COLOR yellow] מתוך ' +str(f_episode)  +' פרקים לעונה זו [/COLOR]\n' 
          if int(episode)>1:
            
            prev_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)-1]['air_date'], '%Y-%m-%d'))) 
          else:
            prev_ep=0

      

                  
          if int(episode)<ep:

            if (int(episode)+1)>=f_episode:
              color_ep='magenta'
              next_ep='[COLOR %s]'%color_ep+time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) +'[/COLOR]'
            else:
              
              next_ep=time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)+1]['air_date'], '%Y-%m-%d'))) 
          else:
            next_ep=0
          dates=((prev_ep,time.strftime( "%d-%m-%Y",(time.strptime(html['episodes'][int(episode_fixed)]['air_date'], '%Y-%m-%d'))) ,next_ep))
          if int(episode)<int(f_episode):
           color='yellow'
          else:
           color='white'
           xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_EPISODE)
      else:
       data_ep=''
       dates=' '
       fanart=image
      
      try:
        f_name=urllib.unquote_plus(heb_name.encode('utf8'))
 
      except:
        f_name=name
      if (heb_name)=='':
        f_name=name
      addDir3('[COLOR %s]'%color+ f_name+'[/COLOR]', url,4, icon,fanart,data_ep+plot,data=year,original_title=original_title,id=id,season=season,episode=episode,eng_name=eng_name,show_original_year=show_original_year,heb_name=heb_name,isr=isr,dates=json.dumps(dates))
def scan_direct_links(next):
    from timeit import default_timer as timer
    dp = xbmcgui.DialogProgress()
    dp.create("סורק שרתים", "אנא המתן", '','')
    dp.update(0)
    dbconserver = database.connect(servers_db)
    dbcurserver = dbconserver.cursor()


    dbcurserver.execute("CREATE TABLE IF NOT EXISTS %s ( ""name TEXT, ""speed TEXT);" % 'servers')
    dbcurserver.execute("VACUUM 'AllData';")
    dbcurserver.execute("PRAGMA auto_vacuum;")
    dbcurserver.execute("PRAGMA JOURNAL_MODE=MEMORY ;")
    dbcurserver.execute("PRAGMA temp_store=MEMORY ;")
    dbconserver.commit()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'filepursuit.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}
    if next=='www':
     html=requests.get(domain_s+'filepursuit.com/discover.php',headers=headers).content
    else:
      html=requests.get(domain_s+'filepursuit.com/discover.php?startrow='+next,headers=headers).content

    
    regex="discover.php\?link=(.+?)'>(.+?)<"
    match_all=re.compile(regex).findall(html)
    f_time_avg=0
    xxx=0
    for links,name in match_all:
      f_time_avg=0
      for i in range(0,5):
          try:
            start = timer()
            html2=requests.get(links,headers=headers2,timeout=1).content
            if  'provider nor the domain owner maintain any relationship with the advertisers.' in html2 or 'tehmovies.org has expired' in html2 or domain_s+'www.google.com/recaptcha/api/fallback?k=' in html2 or 'Access Denied' in html2 or 'not found' in html2.lower() or 'Unauthorized' in html2 or 'Forbidden' in html2 or 'Service Unavailable' in html2:
              f_time='TIMEOUT'
              f_time_avg='TIMEOUT'
            else:
                end = timer()
                f_time=float(end-start)
                f_time_avg=f_time_avg+f_time
          except Exception as e:
            logging.warning(e)
            f_time='TIMEOUT'
            f_time_avg='TIMEOUT'
            break
      if dp.iscanceled():
          dp.close()
          sys.exit()
          break
      if f_time_avg!='TIMEOUT':
        final_time=str(f_time_avg/6)
      else:
        final_time='TIMEOUT'
      if next=='www':
        next=0
      dp.update(int(((xxx* 100.0)/(len(match_all))) ), name,final_time,'Page '+str(int(next)/50))
      xxx=xxx+1
      dbcurserver.execute("SELECT * FROM servers WHERE name = '%s'"%(name))

      match = dbcur.fetchone()
      if match==None:
          dbcurserver.execute("INSERT INTO servers Values ('%s', '%s');" %  (name.replace("'"," "),final_time))
          dbconserver.commit()
      else:
          
          dbcurserver.execute("UPDATE servers SET speed='%s' WHERE name = '%s'"%(final_time,name.replace("'"," ")))
          dbconserver.commit()
    dp.close()
    regex='"discover.php\?startrow=(.+?)">Next</'
    match_next=re.compile(regex).findall(html)
    if len(match_next)>0:
      scan_direct_links(match_next[0])
def remove_from_trace(name,original_title,id,season,episode):

    if id=='0':
      ok=xbmcgui.Dialog().yesno(("הסרה ממעקב סדרות"),(' ממעקב סדרות?'+name+"אתה בטוח שאתה רוצה להסיר את "))
    else:
      ok=xbmcgui.Dialog().yesno(("הסרת סימון נצפה"),(' ממצב נצפה?'+name+"אתה בטוח שאתה רוצה להסיר את "))
    if ok:
      if id=='0':
        dbcur.execute("DELETE  FROM Lastepisode WHERE original_title = '%s'"%(original_title))
      
        dbcon.commit()
      else:
      
        if len(episode)==0:
          episode='%20'
        if len(season)==0:
          season='%20'
        episode=episode.replace(" ","%20")
        season=season.replace(" ","%20")
        dbcur.execute("DELETE  FROM  AllData WHERE original_title = '%s'  AND season='%s' AND episode = '%s'"%(original_title,season.replace(" ","%20"),episode.replace(" ","%20")))
       
        
        dbcon.commit()
       
      xbmc.executebuiltin('Container.Refresh')
def play_level_movies(url):
    from pytube import YouTube
    playback_url = YouTube(url).streams.first().download()
     
   
    
    
    item = xbmcgui.ListItem(path=playback_url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
def my_resolver(url):
     url=url.strip()
     if '$$$' in url:
       url=url.split('$$$')[0]
     if 'upfile' in url or 'www.upf.co.il' in url:
        name2,url=get_upfile_det(url)
     if 'sratim-il.com' in url:
            regex_t='/(.+?).mp4'
            match_t=re.compile(regex_t).findall(url)
            headers={'Accept':'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                    'Accept-Language':'en-US,en;q=0.5',
                    'Cache-Control':'no-cache',
                    'Connection':'keep-alive',
                    'Host':'server2.sratim-il.com',
                    'Pragma':'no-cache',

                    'Referer':'http://www.sratim-il.cf/newsite/%s/'%match_t[0],
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/59.0'}
            head=urllib.urlencode(headers)

            url=url+"|"+head
     if 'streamango' in url:
        url=resolve_streamango(url)
        
     if 'vidup' in url:
        url=getMediaLinkForGuest_vidup(url)[1]
     if 'vidlox' in url:
       url=getMediaLinkForGuest_vidlox(url)[1]
    
     if '://vidtod' in url and rd_sources=='false':
       
       url=VidToDoResolver(url)[1]

     if 'thevideo' in url and rd_sources=='false':
        url=getMediaLinkForGuest_thevid(url)[1]

     if 'vshare' in url and rd_sources=='false':
   
        url=getMediaLinkForGuest_vshare(url)[1]
        
       

     if  rd_sources=='true':
       import resolveurl
     elif 'uptobox' not in url and 'vidtod' not in url and 'thevideo' not in url and 'vshare' not in url and 'vidlox' not in url and 'vidup' not in url:
       import resolveurl
     
     if  rd_sources=='true' :
        try:
          url=resolve_rd(url)
        except Exception as e:
          logging.warning(e)
          pass
        #resolvable=resolveurl.HostedMediaFile(url, include_disabled=True,include_universal=True).valid_url()
        resolvable=False
     elif 'streamango' not in url and 'uptobox' not in url and 'vidtod' not in url and 'thevideo' not in url  and 'vshare' not in url and 'vidlox' not in url and 'vidup' not in url and '-Sdarot' not in description:
       resolvable=resolveurl.HostedMediaFile(url).valid_url()
       
       
     else:
       resolvable=False
     if 'googleusercontent' in url:
       resolvable=False
     if ('openload' in url or 'oload.stream' in url)  and rd_sources=='false':
             
        url=getMediaLinkForGuest(url)
        resolvable=False
     if resolvable:
         hmf = resolveurl.HostedMediaFile(url=url, include_disabled=True, include_universal=False)
         link = hmf.resolve()
         return link
     else:
       return url
def tv_mode_avg(url):


    import random



    
  
    html=requests.get(url).content
    regex='name="(.+?)"&link="(.+?)"'
    match=re.compile(regex).findall(html)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    video_data={}
    
    video_data[u'mpaa']=unicode('heb')
    all_name_links=[]
    all_lins_in=[]
    for name,link in match:
     if link not in all_lins_in:
      all_lins_in.append(link)
      all_name_links.append((name,link))
    random.shuffle(all_name_links)
    once=0

    xbmc.executebuiltin((u'Notification(%s,%s)' % ('EverySource', 'בונה רשימת צפייה מ '.decode('utf8')+str(len(all_lins_in))+' סרטים')).encode('utf-8'))
    for name,link in all_name_links:
     try:
      link2=my_resolver(link)

      video_data['title']=name
             
      listItem=xbmcgui.ListItem(name)
      listItem.setInfo('video', video_data)
      if once==1 and not xbmc.Player().isPlaying():
        break
      playlist.add(url=link2, listitem=listItem)
      if once==0:
        once=1
        ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
 
        xbmc.sleep(10000)
     except Exception as e:
       logging.warning(e)
       pass
def tv_mode_oni():
    import random
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    for c in range (0,3):
        page=random.randint(1,400)
        url=domain_s+'www.onitube.com/videos?o=mv&page='+str(page)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.onitube.com',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
        }
        html=requests.get(url,headers=headers).content
        regex='<a href="https://www.onitube.com/video/(.+?)/.+?title="(.+?)".+?"hd-text-icon">(.+?)<'
        match=re.compile(regex,re.DOTALL).findall(html)
        once=0
        for link,name,quality in match:
           info=(PTN.parse(name.replace(" ",".")))
          
           ok=1
           if ok==1:
           
                if "1080" in quality:
                  res="1080"
                elif "720" in quality:
                  res="720"
                elif "480" in quality:
                  res="480"
                elif "hd" in quality.lower():
                  res="HD"
                else:
                 res=' '
                 
                
                match_s='Direct'
                name1=clean_name(original_title,1)
                
                f_link=domain_s+'ont-assets-1.finalservers.net/mp4sd.php?id='+link
      
                if 'season' in info:
                  
                  season=info['season']
                else:
                  season='0'
                if 'episode' in info:
                  episode=info['episode']
                else:
                  episode='0'
                if 'year' in info:
                  year=info['year']
                
                  url2='http://www.omdbapi.com/?apikey=8e4dcdac&t=%s&year=%s'%(original_title,year)
                else:
                  year=''
                  url2='http://www.omdbapi.com/?apikey=8e4dcdac&t=%s'%(original_title)
                imdb_id="0"
                try:
                   imdb_id=requests.get(url2).json()['imdbID']
                except:
                  pass
                if once==1 and not xbmc.Player().isPlaying():
                    break
                video_data={}
           
                fixed_name=info['title']
              
                video_data['mediatype']='movies'
                video_data['OriginalTitle']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'")
                video_data['title']=fixed_name
 
     
         
                video_data['year']=data
                video_data['season']=season
                video_data['episode']=episode
                video_data['imdb']=imdb_id
                video_data['code']=imdb_id
              

                video_data['imdbnumber']=imdb_id
             
                listItem=xbmcgui.ListItem(name)
                listItem.setInfo('video', infoLabels=video_data)
                playlist.add(url=f_link, listitem=listItem)
                if once==0:
                    once=1
                    ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
             
                    xbmc.sleep(10000)
    playlist.shuffle()
def get_1m_link(original_title,link):

            all_links=[]
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': '1movies.biz',
                'Pragma': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            }

            x=requests.get(link,headers=headers).content
           
            regex='load_player\((.+?)\);'
            id=re.compile(regex).findall(x)[0]
            headers1 = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.5',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': '1movies.biz',
                'Pragma': 'no-cache',
                'Referer': link,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'X-Requested-With': 'XMLHttpRequest',
            }
            url='http://1movies.biz/ajax/movie/load_player_v3?id='+id
            x=requests.get(url,headers=headers1).json()
            headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'play.1movies.biz',
            'Origin': 'http://1movies.biz',
            'Pragma': 'no-cache',
            'Referer': link,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            }
            
            y=requests.get('http:'+x['value'],headers=headers).json()

            if 'playlist' not in y:
                url='http://1movies.biz/ajax/movie/load_player_v3?retry=2&id='+id

                x=requests.get(url,headers=headers1).json()
        
                y=requests.get('http:'+x['value'],headers=headers).json() 
            url=y['playlist'][0]['file']
            name1=original_title
            res=' '
            
            if 'tracks' in y:
               if len(y['tracks'])>0:
                 if 'file' in y['tracks'][0]:
                  names=y['tracks'][0]['file'].split('/')
                  name1=names[len(names)-1].replace('.vtt','')
                  if '1080' in name1:
                      res='1080'
                  elif '720' in name1:
                      res='720'
                  elif '480' in name1:
                      res='480'
                  elif '360' in name1:
                      res='360'
                  else:
                      res='HD'
                      

            new_file=url
            if '.m3u8' in url:
              responce,cook=cloudflare.request(url)
  
              subfixs=url.rsplit('/', 1)[1]
             
              subflix=url.replace(subfixs,'')
            
              regex='URI="(.+?)"'
              match=re.compile(regex).findall(responce)
              responce,cook=cloudflare.request(match[0])
              f_data=responce.replace("BYTERANGE",'TARGETDURATION')
              f_data=f_data.replace("seg-",subflix+'seg-')
              new_file=os.path.join(user_dataDir ,'new.m3u8')
              try:
                xbmcvfs.delete(new_file)
              except:
               pass
              with open(new_file, "w") as text_file:
                    text_file.write(f_data)
            all_links.append((name1,new_file))
            return all_links
def m1_channel():
    import random
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': '1movies.biz',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    url='http://1movies.biz/movies/mostviewed/?page='+str(random.randint(1,10))
    html=requests.get(url,headers=headers).content
    regex='<a class="thumb" href="(.+?)" title="(.+?)"'
    match=re.compile(regex).findall(html)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    once=0
    for link,title in match:
      try:
         info=(PTN.parse(title.replace(" ",".").replace("(",".").replace(")",".").replace("_",".")))
         video_data={}
         fixed_name=info['title']
         original_title=info['title']
         if season!=None and season!="%20":
           video_data['TVshowtitle']=fixed_name.replace('%20',' ').replace('%3a',':').replace('%27',"'")
           video_data['mediatype']='tvshow'
           if 'season' in info:
             video_data['season']=info['season']
           if 'episode' in info:
             video_data['episode']=info['episode']
         else:
           video_data['mediatype']='movies'
         video_data['OriginalTitle']=original_title.replace('%20',' ').replace('%3a',':').replace('%27',"'")
         video_data['title']=fixed_name
         
         if 'year' in info:
           video_data['year']=info['year']
        
   
         new_url=get_1m_link(title,link)

         listItem=xbmcgui.ListItem(new_url[0][0])
         listItem.setInfo('video', video_data)
          
         playlist.add(url=new_url[0][1], listitem=listItem)
         if once==1 and not xbmc.Player().isPlaying():
            break

         if once==0:
            once=1
            ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
     
            xbmc.sleep(10000)
      except:
       pass
params=get_params()
for items in params:
   params[items]=params[items].replace(" ","%20")
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
original_title=' '
data=0
id=' '
saved_name=' '
prev_name=' '
isr=0
season="%20"
episode="%20"
show_original_year=0
heb_name=' '
tmdbid=' '
eng_name=' '
dates=' '
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
        original_title=(params["original_title"])
except:
        pass
try:        
        id=(params["id"])
except:
        pass
try:        
        season=(params["season"])
except:
        pass
try:        
        episode=(params["episode"])
except:
        pass
try:        
        tmdbid=(params["tmdbid"])
except:
        pass
try:        
        eng_name=(params["eng_name"])
except:
        pass
try:        
        show_original_year=(params["show_original_year"])
except:
        pass
try:        
        heb_name=(params["heb_name"])
except:
        pass
try:        
        isr=int(params["isr"])
except:
        pass
try:        
        saved_name=int(params["saved_name"])
except:
        pass
try:        
        prev_name=(params["prev_name"])
except:
        pass
try:        
        dates=(params["dates"])
except:
        pass

episode=str(episode).replace('+','%20')
season=str(season).replace('+','%20')
original_title=original_title.replace('+','%20').replace('%3A','%3a')
all_data=((name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr))

#ClearCache()
if mode==None or url==None or len(url)<1:
        main_menu()
elif mode==2:
        get_genere(url)
elif mode==3:
       get_movies(url,isr)
elif mode==4:
      get_sources(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name,isr,dates=dates)
elif mode==5:
     play(name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id)
elif mode==6:
     auto_play(name,url,iconimage,fanart,description,data,season,episode,original_title,saved_name,heb_name,show_original_year,eng_name,isr,prev_name,id)
elif mode==7:
      get_seasons(name,url,iconimage,fanart,description,data,original_title,id,heb_name,isr)
elif mode==8:
      get_episode(name,url,iconimage,fanart,description,data,original_title,id,season,tmdbid,show_original_year,heb_name,isr)
elif mode==10:
      get_qu(url)
elif mode==11:
      get_dub(url)
elif mode==12:
      search_dub(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,show_original_year,heb_name)
elif mode==13:
      movies_menu()
elif mode==14:
     tv_menu()
elif mode==15:
      search_menu()
elif mode==16:
      ClearCache()
elif mode==17:
      save_to_fav(description)
elif mode==18:
      open_fav(url)
elif mode==19:
      remove_to_fav(description)
elif mode==20:
      remove_fav_num(description)
elif mode==21:
      play_by_subs(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,saved_name)
elif mode==22:
      activate_torrent(name,url,iconimage,fanart,description,data,original_title,season,episode,id,eng_name,saved_name)
elif mode==23:
      run_test(name)
elif mode==24:
      open_settings()
elif mode==25:
      play_trailer(id)
elif mode==26:
      movie_recomended()
elif mode==27:
      tv_recomended()
elif mode==28:
      latest_dvd(url)
elif mode==29:
      get_trakt()
elif mode==30:
      reset_trakt()
elif mode==31:
     get_trk_data(url)
elif mode==32:
     last_viewed(url)
elif mode==33:
     scan_direct_links(url)
elif mode==34:
     remove_from_trace(name,original_title,id,season,episode)
elif mode==35:
     play_level_movies(url)
elif mode==36:
     tv_mode_avg(url)
elif mode==37:
     tv_mode_oni()
elif mode==38:
     movies_channel()
elif mode==39:
     m1_channel()
     
     
elif mode==98:
      server_test()
elif mode==99:

    xbmc.executebuiltin(url)
if mode==4 or mode==21:
  xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
else:
  xbmcplugin.setContent(int(sys.argv[1]), 'movies')


xbmcplugin.endOfDirectory(int(sys.argv[1]))

