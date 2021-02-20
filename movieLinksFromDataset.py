import csv
from furl import furl
BASE_URL = 'https://imdb.com/title'

def getMovieLinkMap(linkFilename, movieFilename):
    movieLinkMap = {}
    with open(linkFilename) as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            imdbId = row['imdbId']
            f = furl(BASE_URL)
            f.path.segments.append('tt{0}'.format(str(imdbId)))
            f.path.segments.append('reviews')
            f.path.normalize()
            movieLinkMap[row['movieId']] = f.url
    movieNameLinkMap = {}
    with open(movieFilename) as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            if row['movieId'] in movieLinkMap:
                movieNameLinkMap[row['title']] = movieLinkMap[row['movieId']]
    return movieNameLinkMap

def fillMovieLinks(inputFilename, outputFilename, movieLinkMap):
    fieldNames = ['movieId','title','genre','reviewLink']
    unknownMovies = 0
    inputFile = open(inputFilename, 'r')
    with open(outputFilename, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames= fieldNames)
        writer.writeheader()
        for movie in inputFile.readlines():
            movieId,title,genre = movie.split('::')
            link = '-'
            if title in movieLinkMap:
                link = movieLinkMap[title]
            else:
                unknownMovies += 1
                print('not found for {0}'.format(title))
            writer.writerow({
                'movieId': movieId,
                'title': title,
                'genre': genre,
                'reviewLink': link
            })
    print('{0} unknown movies'.format(unknownMovies))

if __name__ == '__main__':
    movieLinkMap = getMovieLinkMap('./movielens/ml-25m/links.csv','./movielens/ml-25m/movies.csv')
    fillMovieLinks('./movielens/ml-1m/movies-copy.dat', './dataset/movies.csv', movieLinkMap)

            
    
