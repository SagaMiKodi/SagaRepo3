# -*- coding: utf-8 -*-
###### Source collector #####
import xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging,json
import js2py
from Cookie import SimpleCookie
Domain='www.sparo.xyz'
global link_source1

def get_c(url):
        
        regex=",S='(.+?)'"
        match=re.compile(regex,re.DOTALL).findall(url)
        
        jscode=\
        '''
        var s={},u,c,U,r,i,l=0,a,e=eval,w=String.fromCharCode,sucuri_cloudproxy_js='',
        S='$$$$$$';L=S.length;U=0;r='';var A='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
        for(u=0;u<64;u++)
        {
            s[A.charAt(u)]=u;
            }
        for(i=0;i<L;i++)
        {
        c=s[S.charAt(i)];
        U=(U<<6)+c;
        l+=6;
        while(l>=8)
        {
        ((a=(U>>>(l-=8))&0xff)||(i<(L-2)))&&(r+=w(a));
        }}; r;
        '''
        jscode=jscode.replace('$$$$$$',match[0])
        jcode2=\
        '''
        var j,document
        j="4" + 'UxF9'.substr(3, 1) +String.fromCharCode(49) + '>a'.slice(1,2)+'51'.slice(1,2)+"3" + String.fromCharCode(56) + "fsu".slice(0,1) + "5" + "9" + '46'.slice(1,2)+"4sucur".charAt(0)+"5su".slice(0,1) +  '' +String.fromCharCode(48) + 'e' +  "" +"d".slice(0,1) +  '' +"dsucur".charAt(0)+"1" + "f" + 'RyKb'.substr(3, 1) + '' +"d" + "3" + "6su".slice(0,1) + String.fromCharCode(53) + '>tHc'.substr(3, 1) + '' +'6rL5'.substr(3, 1) +'d' +  "bsucur".charAt(0)+ '' +''+"f" +  '' +''+'pT4'.charAt(2)+ '' +''+String.fromCharCode(49) +  '' +''+"0sucur".charAt(0)+ '' +'';
        document='s'+'u'+'c'+'u'+'rsuc'.charAt(0)+ 'i'+'_'+'c'+'l'+'osuc'.charAt(0)+ 'sucuriu'.charAt(6)+'sucurd'.charAt(5) + 'p'+'r'+'sucuo'.charAt(4)+ 'x'+'ysucu'.charAt(0)  +'_'+'sucuu'.charAt(4)+ 'u'+''+'i'.charAt(0)+'dsucu'.charAt(0)  +'sucur_'.charAt(5) + '9'+'3'+'8'.charAt(0)+'su2'.charAt(2)+'asuc'.charAt(0)+'7'+'asuc'.charAt(0)+ '8'+'8'+''+"=" + j + ';path=/;max-age=86400'; 
        '''

        result=js2py.eval_js(jscode)

        result2=js2py.eval_js(result.replace('location.reload();','').replace('document.cookie','document'))

        return result2,match[0]
def read_sparo_html(url):
    import requests
    
    coockie={}
    
    cookies = {
   
    'sucuri_cloudproxy_uuid_53a9650e8': '6c3d2f947083eaa2a62370d6c90b4495',
    'laravel_session': 'xC5WAE2yuuU0L8k8pCYUQZGh6YMbsv0vjYNvhGBN',
    'XSRF-TOKEN': 'eyJpdiI6IjB3OHhLaUNzTEpSXC83ZUtZYnBQVUtnPT0iLCJ2YWx1ZSI6ImtNQWM4b2ZLSE4yN3l0VHFCNEIyMVNmQ2s5THdNdW8zS21tQmluVFVZNDFSNlpZM3UwRkptd1wvMWxnMHBVT09PM3BlMTU1TVVRdm02S3pCUXZlVjU4Zz09IiwibWFjIjoiYzcxZTM4MDU4ZmMxMGE5NjljMTdiMzBjZDI0ODcyOTEzNDc1NDBjNmU5MGQwN2JiZTZiMmNjNjZkOGUwMjhlMSJ9',
    }


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

      
      #cookies['X-CSRF-TOKEN'] = "wYZBYILaf7Dbw0TZDKjJ3udNO8aPUa7Bns3EQcUe"
      #cookies['XSRF-TOKEN'] = "eyJpdiI6IkVZSmViYXpCdWZwMThjSmJ6dVwvRUhRPT0iLCJ2YWx1ZSI6IkpPQkE5QW83QWc1NzMxY2VwbGR1NkM3RlRDOTJ3dGpXaFF6Q29GWENlY0NOQ3NzSTBTK2ZRN2xPeDJ6dnh5TVlnNEQwbGgweHkwXC85djllSkZ0WTVOQT09IiwibWFjIjoiNTg5Y2U1OTIzY2E0YTM5ZTYxMTY2NjBhOTI4NjhjN2MyMGU1ZDJmM2U0MmEzNDBkYThmNDQ4YzU1M2NkODY5ZCJ9"
      #cookies['laravel_session'] = "xC5WAE2yuuU0L8k8pCYUQZGh6YMbsv0vjYNvhGBN"




      x=requests.get(url, headers=headers, cookies=cookies)
      
      x.encoding = 'utf-8'
      x=x.content
   
    return x

def get_sources_source1(title,season,episode):
          global link_source1
          link_source1=[]
          html=read_sparo_html('http://%s/searchlike?search='%Domain+title)
          
          all_links=[]
          all_links_only=[]
          results_json=json.loads(html)
          saved_name=' '
          for record in results_json:
            saved_name=record['title']
            o_link='http://%s/'%Domain+record['categoria_name'].replace(' ','%20').encode('utf-8')+'/'+str(record['id'])+'/'+record['title'].replace(' ','%20').encode('utf-8')
            
            if (('series' in o_link) or ('סדרות' in o_link)) :
                new_mode=6

            else:
                new_mode=3
   
            season_title='עונה-%s'%season
            episode_title='פרק-%s'%episode
            if season!=None and season!='%20':
               html=read_sparo_html(o_link)
               logging.warning(o_link)
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
               logging.warning(saved_link)
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
            
            logging.warning(saved_link)
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
                        
                        if 'sparo' in links_dip:
         
                          html_source_dip=read_sparo_html(links_dip)
                         
                          
                          regex_source_dip='<iframe src="(.+?)"'
                          match_s_dip=re.compile(regex_source_dip).findall(html_source_dip)
                          regex_more='<source src="(.+?)" type="video/mp4">'
                          match_more=re.compile(regex_more,re.DOTALL).findall(html_source_dip)
             
                        else:
                          
                            regex_source_dip='class="btn btn-success" href="(.+?)"'
                            match_s_dip=re.compile(regex_source_dip).findall(html_source)
                        for in_link in match_s_dip:
                          if 'http' in in_link:
                              
                              names=re.compile('//(.+?)/',re.DOTALL).findall(in_link)[0]
                              if in_link not in all_links_only:
                                all_links_only.append(in_link)
                                all_links.append((saved_name,in_link,names,quality))
                        
                        for links2 in match_more:
                           
                           if 'http' in links2:
                            if 'http' in links2:
                              if 'href' in links2:
                                regex_l2='href=&quot;(.+?)&quot'
                                match_le=re.compile(regex_l2).findall(links2)
                                links2=match_le[0]
                              logging.warning(links2)
                              try:
                                names=re.compile('//(.+?)/',re.DOTALL).findall(links2)[0]
                              except:
                                names='Direct'
                        
                              if links2 not in all_links_only:
                                all_links_only.append(links2)
                                all_links.append((saved_name,links2,names,quality))
          link_source1=all_links
          logging.warning('link_source1 SP')
          logging.warning(link_source1)
          return (all_links)