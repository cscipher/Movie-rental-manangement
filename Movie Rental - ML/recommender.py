import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity    
from sklearn.feature_extraction.text import CountVectorizer

def recommend(movie_chosen, movieid):

    def title_from_index(index):
        return fdf[fdf.index == index]['Movie title'].values[0]

        
    df = pd.read_csv('movie_metadata.csv')

    fdf = df.query("title_year > 2015")
    fdf = fdf.reset_index(drop=True)         
    fdf = fdf.drop(['imdb_score','title_year'], axis=1)
    fdf['genres'] = fdf.genres.str.split('|')

    def combined_features(row):
        return row['director_name']+''+str(row['genres'])+''+row['Actor name']+''+row['Movie title']

    fdf['Combined features'] = fdf.apply(combined_features,axis=1)

    countv = CountVectorizer()
    count_matrix = countv.fit_transform(fdf['Combined features'])

    cosine_sim = cosine_similarity(count_matrix)

    get_index = movieid
    similar_movies = list(enumerate(cosine_sim[get_index]))
    
    sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1],reverse=True)
    
    check=0
    for movie in sorted_similar_movies:
        print(title_from_index(movie[0]))
        check+=1
        if check > 5 : break


