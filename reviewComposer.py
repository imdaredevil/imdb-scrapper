import csv
import movieReviewFetcher
import traceback 

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

def writeFile(filename, reviews):
    fieldNames = ['movieId','userId','userName','review','shortReview','rating']
    with open(filename, 'a') as csvf:
        writer = csv.DictWriter(csvf, fieldNames)
        for review in reviews:
            writer.writerow(review)


def main(st, en):
    movies = readFile('./dataset/movies2.csv')
    for i,movie in enumerate(movies[st:en]):
        if i%50 == 49:
            print('{0} movies out of {1} done'.format(i+1, en - st))        
        try:
            reviews = movieReviewFetcher.getMovieReviews(movie)
            reviewRows = [{
                'movieId': movie['movieId'],
                'userId': review['userId'],
                'userName': review['userName'],
                'review': review['review'],
                'shortReview': review['shortReview'],
                'rating': review['score']
                } for review in reviews]
            writeFile('./dataset/reviews.csv',reviewRows)
        except Exception as e:
            print('some error with the movie - {0}'.format(movie['title']))
            traceback.print_exc()
            movieReviewFetcher.writeLog(movie,'./dataset/toBeRepeated.csv', str(e))
    
if __name__ == '__main__':
    main(50,200)