
import json
import requests
from urlparse import urlparse, urljoin

def dictprettystr(d, sep=', '):
    return sep.join(['%s: %s' % (k, v) for k, v in d.iteritems()])

def printstreaminfo(stream):
    print('%d : %s' % (stream['id'], stream['name']))
    for i, uri in enumerate(stream['streams']):
        print('\t#%d %s' % (i + 1, uri))

class RadioClientError(Exception):
    def __init__(self, *args, **kwargs):
        super(RadioClientError, self, args, kwargs)

class RadioClient(object):

    def __init__(self, host, port=5000):

        self.host = host
        self.port = port
        self.uri = urlparse('{}:{}'.format(host, port))


    def makeurl(self, endpoint):
        return urljoin(self.uri.geturl(), endpoint)


    def list(self):
        
        searchurl = self.makeurl('search')

        r = requests.post(searchurl)

        if r.status_code != 200:
            print('will fail with status {}'.format(r.status_code))
            raise RadioClientError('Request Failed') 
        
        return json.loads(r.text)


    def search(self, query):
        if not isinstance(query, str):
            raise ValueError('search query must be string')
        
        searchurl = self.makeurl('search')

        r = requests.post(searchurl, data={'term': query})

        if r.status_code != 200:
            raise RadioClientError('Request Failed') 
        
        return json.loads(r.text)
     

    def query(self):

        queryurl = self.makeurl('player')

        r = requests.get(queryurl)
        return json.loads(r.text)


    def volume(self, level):
        volurl = self.makeurl('player/volume', )

        r = requests.post(volurl, data={'level': float(level)})
        return json.loads(r.text)


    def play(self, url=None):

        if not url:
            playurl = self.makeurl('player')
            r = requests.post(playurl, data={'state': 'play'})

            if r.status_code != 200:
                raise RadioClientError('Request Failed')
        else:
            if not any(url.startswith(proto) for proto in ('http')):
                raise ValueError('Request Failed')

            playurl = self.makeurl('player/uri')
            r = requests.put(playurl, data={'stream': url})

            if r.status_code != 201:
                raise RadioClientError('Request Failed') 

    def stop(self):
        stopurl = self.makeurl('player')
        r = requests.post(stopurl, data={'state': 'stop'})
        
        if r.status_code != 200:
            raise RadioClientError('Request Failed')

    
if __name__ == '__main__':

    import sys
    from time import sleep

    host = 'localhost' if len(sys.argv) < 2 else sys.argv[1]

    rc = RadioClient('http://%s' % host)

    print(dictprettystr(rc.query()))

    for d in rc.list():
        print("station::")
        print(printstreaminfo(d))

    

    for d in rc.search('seymour'):
        print("station::")
        print(printstreaminfo(d))

    sys.exit()

    pdata = rc.play('http://live-radio01.mediahubaustralia.com/2TJW/mp3/')


    for i in reversed(xrange(0, 10, 2)):
        vold = rc.volume(i)
        print('%d - %r' % (i, vold))
        sleep(1)


    sleep(1)
    rc.stop()
    sleep(1)
    rc.play()
    sleep(10)
    rc.stop()

    