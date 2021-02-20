import csv
import movieReviewFetcher
import traceback 
import sys

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
        if i%10 == 9:
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
    if len(sys.argv) == 3:
        st = int(sys.argv[-2])
        en = int(sys.argv[-1])
        main(st,en)
    else:
        print('The format is python <filename> <start> <end>')