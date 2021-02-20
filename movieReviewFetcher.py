from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from furl import furl
import csv

driver = webdriver.Chrome('./chromedriver')
LIMIT = 20

def writeLog(movie, filename, error):
    fieldNames = ['movieId', 'title', 'error']
    with open(filename, 'a') as csvf:
        writer = csv.DictWriter(csvf, fieldNames)
        writer.writerow({
            'movieId': movie['movieId'],
            'title': movie['title'],
            'error': error
        })

def printMovieReview(review):
    for key in review.keys():
        print('---------------------------------------------')
        print(key,end=' : ')
        print(review[key])
    print('---------------------------------------------')


def getMovieReviews(movie):
    f = furl(movie['reviewLink'])
    f.args['sort'] = 'reviewVolume'
    f.args['dir'] = 'desc'
    driver.get(f.url)
    reviewDicts = []
    alreadyHappened = False
    for i in range(50):
        try:
            nextB = driver.find_element_by_class_name('ipl-load-more__button')
            nextB.click()
            sleep(3)
            alreadyHappened = False
        except Exception as e:
            if alreadyHappened:
                break
            alreadyHappened = True
    html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html5lib')
    headDiv = soup.find('div', attrs = { 'class': 'lister'})
    headDiv = headDiv.find('div', attrs = { 'class' : 'header'})
    headSpan = headDiv.find('span')
    totalReviews = int(headSpan.text.split()[0].replace(',',''))
    reviews = soup.findAll('div',attrs = { 'class' : 'lister-item-content' })
    improperCount = 0
    for review in reviews:
        reviewShort = review.find('a', attrs = { 'class': 'title'})
        reviewTextDiv = review.find('div', attrs = { 'class' : 'content'})
        reviewText = reviewTextDiv.find('div')
        reviewerNameSpan = review.find('span', attrs = { 'class' : 'display-name-link'})
        reviewerName = reviewerNameSpan.find('a')
        reviewScoreDiv = review.find('div', attrs = { 'class' : 'ipl-ratings-bar'})
        reviewDict = {}
        if reviewText and reviewerName and reviewScoreDiv and reviewShort:
            reviewDict['review'] = reviewText.text.replace('\n','').replace('  ','')
            reviewDict['userId'] = furl(reviewerName['href']).path.segments[1]
            reviewDict['userName'] = reviewerName.text
            reviewScoreSpan = reviewScoreDiv.find('span')
            reviewScore = reviewScoreSpan.find('span')
            reviewDict['shortReview'] = reviewShort.text
            reviewDict['score'] = 0.5*int(reviewScore.text.replace(',',''))
            reviewDicts.append(reviewDict)
        else:
            improperCount += 1
    if improperCount>250 or (totalReviews - len(reviewDicts) - improperCount > 100 and totalReviews < 1250):
        print(totalReviews)
        print(improperCount)
        print(len(reviewDicts))
        print('some problem with the movie - {0} {1}'.format(movie['movieId'],movie['title']))
        error = 'movie count mismatch\ntotalReviews: {0}, noRatingCount: {1}, fetchedCount: {2}'.format(totalReviews, improperCount, len(reviewDicts))
        writeLog(movie,'./dataset/toBeRepeated.csv', error)
    # driver.close()
    return reviewDicts

if __name__ == '__main__':
    if len(sys.argv) == 2:
        movie = { 
            'reviewLink': sys.argv[-1]
        }
        count = 0
        for review in getMovieReviews(movie):
            print('*********************************************')
            print("Movie Review - {0}".format(count))
            printMovieReview(review)
            count += 1
    else:
        print('The format is python <filename> <movie name>')