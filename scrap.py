#!/usr/bin/env python
# coding: utf-8

import sys
import httplib2
from functools import partial
from BeautifulSoup import BeautifulSoup
from urllib2 import urlparse

class HTTPFetchError(Exception):
    pass



def obtener_pagina(http, url):
    headers, content = http.request(url)
    status = int(headers.status)
    if 200 <= status < 300:
        return content
    raise HTTPFetchError("Error: %d\n%s" % (status, content))

def buscar_links(content):
    links = []
    html = BeautifulSoup(content)
    for params in html.findAll('param'):
        value = params.get('value', None)
        if not value or not value.startswith('mp3'):
            continue
        value = value[4:] # Sacar el mp3=
        mp3_list = value.split('&')[0]
        mp3_list =  mp3_list.split('|')
        links.extend(mp3_list)
        #print mp3_list
        #import ipdb; ipdb.set_trace()
    try:
        next_link = html.find('a', title="Siguiente").get('href', None)
    except:
        next_link = None
    return next_link, links

def main(argv = sys.argv):
    ''' Punto de entrada al programa '''
    url = ("http://www.vientonomade.com.ar/index.php?option=com_content&view=category&"
                "layout=blog&id=8&Itemid=10")
    fetcher = httplib2.Http()
    get = partial(obtener_pagina, fetcher)

    while url:
        html = get(url)
        uri, links = buscar_links(html)
        for link in links:
            try:
                print urlparse.urljoin(url, link)
            except UnicodeEncodeError:
                pass
        url = uri and urlparse.urljoin(url, uri) or None
        
        
    


if __name__ == "__main__":
    sys.exit(main())