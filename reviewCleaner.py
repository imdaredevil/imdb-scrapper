import csv
import pandas as pd 

def dataframeMaker(filename):
    result = []
    with open(filename,'r') as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            result.append({
                "userId": row['userId'],
                "movieId": row['movieId'],
                "shortReview": row['shortReview'],
                "review": row['review'],
                "rating": row['rating']
            })
    df = pd.DataFrame.from_dict(result)
    return df

def getEligibleUsers(df):
    userGroup = df.groupby('userId').count()
    userGroup = userGroup[userGroup['movieId'] >= 10]
    print('Number of valid users: {0}'.format(len(userGroup)))
    userIds = userGroup.index.values.tolist()
    eligibleUserSeries = pd.Series(userIds)
    return eligibleUserSeries

def getCleanMovies(movieFileName, cleanDf):
    movieIdsList = cleanDf['movieId'].unique().tolist()
    print('Number of Valid movies: {0}'.format(len(movieIdsList)))
    movieIds = pd.Series(movieIdsList).astype(int)
    moviesDf = pd.read_csv(movieFileName)
    cleanMovies = moviesDf[moviesDf['movieId'].isin(movieIds)]
    return cleanMovies

if __name__ == '__main__':
    df = dataframeMaker('./dataset/reviews3.csv')
    eligibleUsers = getEligibleUsers(df)
    cleanDf = df[df['userId'].isin(eligibleUsers)]
    cleanDf.to_csv('./dataset/reviews-mini.csv', index=False)
    eligibleMovies = getCleanMovies('./dataset/movies2.csv', cleanDf)
    eligibleMovies.to_csv('./dataset/movies-mini.csv', index=False)