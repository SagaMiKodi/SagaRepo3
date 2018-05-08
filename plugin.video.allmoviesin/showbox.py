"""
    Exodus Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urlparse, urllib, json, base64, xbmc,requests,logging


import pyaes

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movietimeapp.com']
        self.base_link = 'http://sbfunapi.cc'
        self.server = 'http://%s/video/%s/manifest_mp4.json?sign=%s&expires_at=%s'
        self.key = b'\x38\x36\x63\x66\x37\x66\x66\x63\x62\x33\x34\x64\x37\x64\x33\x30\x64\x33\x62\x63\x31\x35\x61\x38\x35\x31\x36\x33\x34\x33\x32\x38'
        self.show_search = '/api/serials/tv_list/?query=%s'
        self.movie_search = '/api/serials/movies_list/?query=%s'
        self.episode_details = '/api/serials/episode_details/?h=%s&u=%s&y=%s'
        self.movie_details = '/api/serials/movie_details/?id=%s'
        self.fetcher = '/api/serials/mw_sign/?token=%s'
        self.headers = {
            'User-Agent': 'Show Box'
        }

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year, 'imdb': imdb}
            return urllib.urlencode(url)

        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            data = {'tvshowtitle': tvshowtitle, 'year': year, 'imdb': imdb}
            return urllib.urlencode(data)

        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            data.update({'season': season, 'episode': episode, 'title': title, 'premiered': premiered})

            return urllib.urlencode(data)

        except Exception:
            return

    def sources(self, url):
        try:
            sources = []

            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)

            if 'tvshowtitle' in data:
                url = self.__get_episode_url(data)
            else:
                url = self.__get_movie_url(data)
         
            token = urlparse.parse_qs(urlparse.urlparse(url).query)['token'][0]

            response = requests.get(url, headers=self.headers).content
            manifest_info_encrpyted = json.loads(response)['hash']

            manifest_info = self.__decrypt(manifest_info_encrpyted)
            manifest_info = manifest_info.split(':')

            url = self.server % (manifest_info[0], token, manifest_info[2], manifest_info[1])

            response = requests.get(url, headers=self.headers).content
            manifest = json.loads(response)

            for k, v in manifest.iteritems():
                try:
                    sources.append({
                        'source': 'CDN',
                        'quality': k + 'p',
                        'language': 'en',
                        'url': v,
                        'direct': True,
                        'debridonly': False
                    })

                except Exception:
                    pass

            return sources

        except Exception:
            return

    def resolve(self, url):
        try:
            return url

        except Exception:
            return

    def __get_episode_url(self, data):
        #try:
            query = data['tvshowtitle'].lower().replace(' ', '+')
            path = self.show_search % query
            url = urlparse.urljoin(self.base_link, path)

            response = requests.get(url, headers=self.headers).content

            show_id = json.loads(response)[0]['id']

            path = self.episode_details % (show_id, data['season'], data['episode'])
            url = urlparse.urljoin(self.base_link, path)

            response = requests.get(url, headers=self.headers).content
            token_encrypted = json.loads(response)[0]['sources'][0]['hash']


            token = self.__decrypt(token_encrypted)

            path = self.fetcher % token
            url = urlparse.urljoin(self.base_link, path)

            return url

        #except Exception:
        #    return

    def __get_movie_url(self, data):
        #try:
            query = data['title'].lower().replace(' ', '+')
            path = self.movie_search % query
            logging.warning(path)
            url = urlparse.urljoin(self.base_link, path)
            logging.warning(url)
            response = requests.get(url, headers=self.headers).content

            movie_id = json.loads(response)[0]['id']

            path = self.movie_details % movie_id
            url = urlparse.urljoin(self.base_link, path)

            response = requests.get(url, headers=self.headers).content
            token_encrypted = json.loads(response)['langs'][0]['sources'][0]['hash']

            token = self.__decrypt(token_encrypted)

            path = self.fetcher % token
            url = urlparse.urljoin(self.base_link, path)

            return url

        #except Exception:
        #    return

    def __decrypt(self, ciphertext):
        try:
            ciphertext = base64.b64decode(ciphertext)

            decrypter = pyaes.Decrypter(pyaes.AESModeOfOperationECB(self.key))
            plaintext = decrypter.feed(ciphertext)
            plaintext += decrypter.feed()

            return plaintext

        except Exception:
            return
