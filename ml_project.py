# -*- coding: utf-8 -*-
"""ML_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1T8Z8GkeWgAy5mMrNoLIsDmbzGykZBZf_
"""

import pandas as pd
import numpy as np

movies = pd.read_csv('/content/tmdb_5000_movies.csv.zip')

credits = pd.read_csv('/content/tmdb_5000_credits.csv.zip')

credits.head()

movies.head()

movies.info()

credits.head()

movies.shape

credits.shape

movies.shape

movies = movies.merge(credits,on='title')

movies.shape

movies.info()

#now we are removing extra colums from movies dataset
#budget is not useful column, genres is useful (drama, horror), homepage not useful, id is ueful-- poster ko fetch krne k liye
#keywords - useful (ind of tags)
#title
#overview
#cast (we recommend movies on the basis of actors)
#crew (director)

movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.isnull().sum()

movies.dropna(inplace=True)

movies.isnull().sum()

movies.duplicated().sum()

movies.iloc[0].genres

#{'Action','Adventure','FFantasy','SciFi'} i want to write in this format
#so we create a function called create

# def  convert(obj):
#   L = []
#   for i in obj:
#     L.append(i['name'])
#   return L

#convert([{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}])
#we have to convert this string of lists in list
#we have a module in python ast.literal_eval()

import ast
# ast.literal_eval([{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}])

def  convert(obj):
  L = []
  for i in ast.literal_eval(obj):
    L.append(i['name'])
  return L

movies['genres']=movies['genres'].apply(convert)

movies.head()

movies['keywords'] = movies['keywords'].apply(convert)

movies.head()

#from cast we need top 3 actors

movies['cast'][0]

#means from above we need 3 dictionaries, we need actual name

def  convert3(obj):
  L = []
  counter = 0
  for i in ast.literal_eval(obj):
    if counter != 3:
        L.append(i['name'])
        counter+=1
    else:
      break
  return L

movies['cast'] = movies['cast'].apply(convert3)

#so we get top 3 actors name

movies.head()

#now we will work on crew
movies['crew'][0]

#we need only those dictionaries whose job is director and name of only those dictonaries

def fetch_director(obj):
  L=[]
  for i in ast.literal_eval(obj):
    if i['job'] == 'Director':
      L.append(i['name'])
      break
    return L

movies['crew']=movies['crew'].apply(fetch_director)

movies.head()

movies['overview'][0]

#now we convert this also in list so that we can concatenate this with another lists

movies['overview'] = movies['overview'].apply(lambda x:x.split())

#we have to apply transformation on these columns
#transformation means remove space b/w words
#like Sam Worthington in SamWorthington ,because we have same name with different surname
#Sam and Worthington k alg alg tags bn jayenge

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])

movies['crew'] = movies['crew'].apply(
    lambda x: [i.replace(" ", "") for i in x] if x else []
)

#now we will create a new column named tags and then we will concatenate all columns

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

movies.head()

#now we will delete all other duplicate column

new_df = movies[['movie_id','title','tags']]

new_df

#now convert list into string (tags wali)

new_df['tags'] = new_df['tags'].apply(lambda x:" ".join(x))

new_df.head()

new_df['tags'][0]

#now convert in lowercase

new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

new_df.head()

#now use vectorization
#we have to calculate similarity score
#we will convert all texts of tags in vector called text vectors and this techniques is called "bag of words"
#in bag of words we concatenate all tags and then we need 5000 most common words
#we calculate frequency of all words
#now we will see how many times these words come in movie1, similarly for m2, m3
#example:
#         w1           w2          w3 ....             w5000
# m1      5            3            0                   1
# m2      2            0            1                   3
# m3      1            1            1                   1
# .
#m5000    5            2            5                   5

#this single row is actually a vector, means this movie converted into vector
#then we will fetch 5 closest 5 vectors (movies)

#stopwords - are, and, the, a, is ,to ... we will remove all these words then perform vectorization

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

cv.fit_transform(new_df['tags']).toarray().shape

vectors

vectors[0]

cv.get_feature_names_out()

#all words are arranged in alphabetically
#issue in code 2 words - activity, activities; action, actions
#so we use stemming
#to use stemming we need library nltk

!pip install nltk

import nltk

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

new_df['tags'][0]

new_df['tags'][1300]

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

#now we have to calculate distance b/w all movies
#less distance = more similarity
#now we will calculate cosine similarity (angle)

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

similarity

similarity.shape

similarity[1]

new_df[new_df['title']=='Batman Begins'].index[0]

#after sorting indices will loose, so will use enumerate fn so that it does not get loose

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

def recommend(movie):
  movie_index = new_df[new_df['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  for i in movies_list:
    print(i[0])

new_df

recommend('Avatar')

new_df.iloc[1214]

new_df.iloc[1214].title

def recommend(movie):
  movie_index = new_df[new_df['title'] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  for i in movies_list:
    print(new_df.iloc[i[0]].title)

recommend('Batman Begins')

#now convert it into a websites

import pickle

pickle.dump(new_df,open('movies.pkl','wb'))        # opening this file in write binary mode

new_df['title'].values

pickle.dump(new_df.to_dict(),open('movie_dict.pkl','wb'))

pickle.dump(similarity,open('similarity.pkl','wb'))

