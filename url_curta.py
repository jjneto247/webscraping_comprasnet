#Importing the required libraries
from __future__ import with_statement
import contextlib
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
import sys
from socket import error as SocketError
import errno
from http.client import HTTPConnection
from urllib.parse import urlparse



#Defining the function to shorten a URL
def make_shorten(url):
    request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        try:
            resp = response.read().decode('utf-8')
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise  # Not error we are looking for
            pass  # Handle error here.
    return resp



def unshorten_url(url):
    parsed = urlparse(url)
    h = HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status//100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url
#The main function to receive user inputs
def main():
    for shortyurl in map(make_shorten, sys.argv[1:]):
        print(shortyurl)

if __name__ == '__main__':
    url_ex = 'http://comprasnet.gov.br/livre/pregao/termohom.asp?prgcod=817208&co_no_uasg=120625&numprp=00063/2019&f_lstSrp=&f_Uf=&f_numPrp=00063/2019&f_coduasg=120625&f_tpPregao=E&f_lstICMS=&f_dtAberturaIni=&f_dtAberturaFim='
    url_short = make_shorten(url_ex)
    print(url_short)