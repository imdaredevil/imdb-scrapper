from bs4 import BeautifulSoup
import requests
import sys
from furl import furl
URL = 'https://www.google.com/search'


def getSoup(movie):
    response = requests.get(URL, params={ 'q': '{0} movie imdb'.format(movie) })
    html = response.content
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getMovieLink(movie):
    movieLink = ''
    soup = getSoup(movie)
    searchResults = soup.findAll('div', attrs = { 'class' : 'kCrYT' })
    for searchResult in searchResults:
        link = searchResult.find('a')
        if link:
            link = link.get('href')
            result = furl(link)
            link = result.args['q']
            linkObj = furl(link)
            if linkObj.host == 'www.imdb.com':
                linkObj.path.segments.append('reviews')
                linkObj.path.normalize()
                movieLink = linkObj.url
                break
    return movieLink

if __name__ == '__main__':
    if len(sys.argv) == 2:
        movie = sys.argv[-1]
        print(getMovieLink(movie))
    else:
        print('The format is python <filename> <movie>')