import movieLinksFetcher
import csv

def readFile(filename):
    movies = []
    with open(filename) as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            movie = {}
            for key in reader.fieldnames:
                movie[key] = row[key]
            movies.append(movie)
    return movies

def writeFile(filename, movies):
    fieldNames = ['movieId','title','genre','reviewLink']
    with open(filename, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldNames)
        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)

def fillMissingLinks(movies):
    for movie in movies:
        if movie['reviewLink'] == '-':
            print('{0} - movie name'.format(movie['title']))
            movie['reviewLink'] = movieLinksFetcher.getMovieLink(movie['title'])
            print('{0} - movie link'.format(movie['reviewLink']))
    return movies

if __name__ == '__main__':
    movies = readFile('./dataset/movies.csv')
    movies = fillMissingLinks(movies)
    writeFile('./dataset/movies2.csv', movies)

