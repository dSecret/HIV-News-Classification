import string
import collections
import json
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
 
                            # Tokenize text and stem words removing punctuation

def process_text(text, stem=True):

    #remove punctuation
    trans = str.maketrans('','',("“”’").join(string.punctuation))
    text = text.translate(trans)

    #tokenize 
    tokens = word_tokenize(text)
    newtokens =[]

    #remove stopwords
    for i in tokens:
    	if i in stopwords.words('english'):
    		tokens.remove(i)
    
    #stem tokens 
    if stem:
    	stemmer = SnowballStemmer('english',ignore_stopwords=True)
    	tokens = [stemmer.stem(t) for t in tokens]
    
    return tokens

                            #Transform texts to Tf-Idf coordinates and cluster texts using K-Means 
 
def cluster_texts(texts, clusters=3):
    vectorizer = TfidfVectorizer(tokenizer=process_text,
                                 max_df=0.5,
                                 min_df=0.1,
                                 lowercase=True)
 
    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)
 
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)

    order_centroids=km_model.cluster_centers_.argsort()[:,::-1]
    terms = vectorizer.get_feature_names()

    print('top 10 terms per cluster:')

    for i in range(clusters):
    	print("\n Cluster",i,'\n')
    	for ind in order_centroids[i, :10]:	
    		print(terms[ind],)

    return clustering
 
articles = []

                            # retrive all articles
with open('toi_news_pages.json','r') as news:

	for i in json.load(news):
		articles.append(i['body']+" "+i['title']) 

                            #  3 clusters
cluster_texts(articles, 5)
