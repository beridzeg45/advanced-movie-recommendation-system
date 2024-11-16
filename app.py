#imports
import pandas as pd
import numpy as np
import os
import pickle

import streamlit as st

#path=r"C:\Users\berid\python\yts mx project"
path=''




#load movies df
df=pd.read_csv(os.path.join('scraped_data','merged_df.csv'))
df['TITLE_YEAR']=df['TITLE']+' ('+df['YEAR'].astype(str)+')'




#load similarity matrix
loaded_parts = []

for file in os.listdir(os.path.join('scraped_data','similarities_matrix')):
    if file.endswith('.pkl'):
        file_path=os.path.join('scraped_data','similarities_matrix',file)
        part_of_matrix=pickle.load(open(file_path,'rb'))
        loaded_parts.append(part_of_matrix)

similarity_matrix = np.concatenate(loaded_parts)




#return recommended movies df
def return_recommendations(movie_title):

    try:
        movie_index=df[df['TITLE_YEAR']==movie_title].index[0]
    except:
        st.warning("No movies found matching the input title.")
        return [], [], []
    
    sim_scores=list(enumerate(similarity_matrix[movie_index]))
    sim_scores=sorted(sim_scores,key=lambda items:items[1],reverse=True)
    top_sim_scores=sim_scores[1:101]
    top_movie_indexes=[i[0] for i in top_sim_scores]
    top_recommended_movies=df.loc[top_movie_indexes]

    
    #similar_genres_count_list=[]
    #for genres in top_recommended_movies['GENRES']:
    #    similar_genres_count=0
    #    for genre in df[df['TITLE_YEAR']==movie_title]['GENRES'].iloc[0].split('|'):
    #        if genre in genres:
    #            similar_genres_count+=1
    #    similar_genres_count_list.append(similar_genres_count)
    #top_recommended_movies['SIMILAR_GENRES_COUNT']=similar_genres_count_list
    #top_recommended_movies=top_recommended_movies.sort_values(['SIMILAR_GENRES_COUNT','IMDB_RATING_COUNT'],ascending=False)[:10]
    
    top_recommended_movies=top_recommended_movies.head(10)

    similar_movies_titles = top_recommended_movies['TITLE_YEAR'].tolist()
    similar_movies_posters = top_recommended_movies['POSTER'].tolist()
    similar_movies_urls = top_recommended_movies['IMDB_LINK'].tolist()
    


    similar_tags=[]
    top_recommended_movies['ALL_TAGS'].apply(lambda x:similar_tags.extend(list(set(x.split('|')))))
    similar_tags=[tag for tag in pd.Series(similar_tags).value_counts().sort_values(ascending=False).head(16).index.tolist() if tag!='']

    return similar_movies_titles, similar_movies_posters, similar_movies_urls, similar_tags



#streamlit
list_of_movies = df['TITLE_YEAR'].unique().tolist()

st.set_page_config(layout="wide")

st.header('Movie Recommendation System 🍿🎥🎞️📽️🎬🎦 - By Giorgi Beridze')
input_value = st.selectbox('Select a movie title', [''] + list_of_movies, help='Type movie title to get recommendations')

if input_value:
    titles, posters, urls, similar_tags = return_recommendations(input_value)

    input_poster = df[df['TITLE_YEAR'] == input_value]['POSTER'].values[0]
    
    st.image(input_poster, caption=f"Similar movies like {input_value}", width=200)  # Adjust the width as needed

    cols = st.columns(len(titles))
    for i, (title, poster, url) in enumerate(zip(titles, posters, urls)):
        with cols[i]:
            st.markdown(f"<span style='font-size: 14px;'><a href='{url}'>{title}</a></span>", unsafe_allow_html=True)
            st.image(poster)

    st.markdown(f"**Similar Tags:**<br>{'<br>'.join(similar_tags)}", unsafe_allow_html=True)




# Add intro text to upper left corner of sidebar
st.sidebar.markdown("# About Me:")

intro_text = """
Hi! 👋 I'm Giorgi Beridze, a passionate movie and Python enthusiast. 

This is my latest movie recommendation project.

Previously, I created a movie recommendation system that recommended movies solely based on the director. 

This time, the system is more advanced—it recommends movies based on **Genres**, **Director**, **Movie Plot**, and **Tags**. 

To make the recommendations even more accurate, I’ve assigned different weights to each feature.

The movie information was collected using Python's **Selenium**, **Requests**, and **BeautifulSoup** web-scraping libraries from two different movie websites, to gather as many tags as possible for better recommendations.

If you're curious about the code and want to explore it, feel free to visit my Github account! [GitHub](https://github.com/beridzeg45)\n
You will be able to check the scraped dataset on my Kaggle page: [Kaggle](https://www.kaggle.com/datasets/beridzeg45/all-movies-on-imdb)\n
"""
st.sidebar.markdown(intro_text)






