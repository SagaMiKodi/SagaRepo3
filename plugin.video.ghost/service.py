# -*- coding: utf-8 -*-
import xbmc,time,requests,logging,xbmcaddon,os,xbmcgui

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')
logging.warning(addonID)
__settings__ = xbmcaddon.Addon(id=addonID)
user_dataDir = xbmc.translatePath(__settings__.getAddonInfo("profile")).decode("utf-8")
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)
     
last_run=time.time()
update_time=1
logging.warning("My EPG Service Started")
while not xbmc.abortRequested:
    if(time.time() > last_run + update_time):
                  
                      update_time=36000
                      now = time.time()
                      last_run = now - (now % update_time)
                      try:
                          response = requests.get('http://super-iptv.tv/files/israel.xml', stream=True)
                          #xbmcgui.Dialog().notification('Tv Guide', "מעדכן תוכניות", xbmcgui.NOTIFICATION_INFO,1000 )
                          # Throw an error for bad status codes
                          response.raise_for_status()

                          with open(user_dataDir+'/guide.xml', 'wb') as handle:
                                for block in response.iter_content(1024):
                                    handle.write(block)
                      except:
                         pass
                      #xbmcgui.Dialog().notification('Tv Guide', "תוכניות עודכנו", xbmcgui.NOTIFICATION_INFO,1000 )

    xbmc.sleep(1000)