import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('always')
import warnings
warnings.filterwarnings('ignore')
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import flask
from flask import Flask, render_template, request

app= Flask(__name__)
zomato_df=pd.read_csv("zomato.csv")


@app.route('/')# route to display the home page

def home():

    return render_template('index.html') #rendering the home page

@app.route('/extractor')
def extractor():

    return render_template('extractor.html')


@app.route('/keywords', methods=['POST'])
def keywords():
    output=request.form['output']
    print(output)
    print(type(output))
    df_percent=zomato_df.sample(frac=0.5) 
    print("23")
    df_percent.set_index('name', inplace=True) 
    print("12")
    indices = pd.Series(df_percent.index)
    print("34")
    tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0.1, stop_words='english')
    print("45")
    tfidf_matrix = tfidf.fit_transform(df_percent['reviews_list'].fillna(''))
    print("56")
    cosine_similarities=linear_kernel(tfidf_matrix,tfidf_matrix)
    print("67")
    
    def recommend(name, cosine_similarities = cosine_similarities):
        print(1)
        
        recommend_restaurant = []
        
        idx=indices.index[0]
        
        score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
        
        top30_indexes = list(score_series.iloc[0:31].index)
        
        for each in top30_indexes:
            print(2)
            recommend_restaurant.append(list(df_percent.index)[each])
            
        # df_new=pd.DataFrame(columns=['cuisines', 'Mean Rating', 'cost'])
        
        # for each in recommend_restaurant:
        #     print(3)
        #     df_new=df_new._append(pd.DataFrame(df_percent[['cuisines', 'Mean Rating', 'cost']][df_percent.index == each].sample()))
            
        # df_new=df_new.drop_duplicates(subset=['cuisines', 'Mean Rating', 'cost'], keep=False)
        # pd.set_option('display.max_columns',None)
        
        # df_new = df_new.sort_values(by='Mean Rating', ascending=False).head(10) 
        # print('TOP %s RESTAURANTS LIKE %s WITH SIMILAR REVIEWS: ' % (str(len(df_new)), name))
        
        return recommend_restaurant

    result=recommend(output)
    print(result)
    print(type(result))

    return render_template('keywords.html', keyword=result)

if __name__ == '__main__':
    app.run(debug=True)
