import requests
import re
import string
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup





# Make a request to the website
r = requests.get('http://www.xophura.net/')

# Create an object to parse the HTML format
soup = BeautifulSoup(r.content, 'html.parser')
documents = soup.get_text()

# # Retrieve all popular news links (Fig. 1)
# link = []
# for i in soup.find('div', {'class':'most__wrap'}).find_all('a'):
#     i['href'] = i['href'] + '?page=all'
#     link.append(i['href'])
# # For each link, we retrieve paragraphs from it, combine each paragraph as one string, and save it to documents (Fig. 2)
# documents = []
# for i in link:
#     # Make a request to the link
#     r = requests.get(i)
  
#     # Initialize BeautifulSoup object to parse the content 
#     soup = BeautifulSoup(r.content, 'html.parser')
  
#     # Retrieve all paragraphs and combine it as one
#     sen = []
#     for i in soup.find('div', {'class':'read__content'}).find_all('p'):
#         sen.append(i.text)
  
#     # Add the combined paragraphs to documents
#     documents.append(' '.join(sen))


documents_clean = []
for d in documents:
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
    # Remove Mentions
    document_test = re.sub(r'@\w+', '', document_test)
    # Lowercase the document
    document_test = document_test.lower()
    # Remove punctuations
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    # Lowercase the numbers
    document_test = re.sub(r'[0-9]', '', document_test)
    # Remove the doubled space
    document_test = re.sub(r'\s{2,}', ' ', document_test)
    documents_clean.append(str(document_test, encoding='utf-8'))


# Instantiate a TfidfVectorizer object
vectorizer = TfidfVectorizer()
# It fits the data and transform it as a vector
X = vectorizer.fit_transform(documents_clean)
# Convert the X as transposed matrix
X = X.T.toarray()
# Create a DataFrame and set the vocabulary as the index
df = pd.DataFrame(X, index=vectorizer.get_feature_names())

def get_similar_articles(q, df):
    print("query:", q)
    print("Berikut artikel dengan nilai cosine similarity tertinggi: ")
    # Convert the query become a vector
    q = [q]
    q_vec = vectorizer.transform(q).toarray().reshape(df.shape[0],)
    sim = {}
    # Calculate the similarity
    for i in range(10):
        sim[i] = np.dot(df.loc[:, i].values, q_vec) / np.linalg.norm(df.loc[:, i]) * np.linalg.norm(q_vec)

    # Sort the values 
    sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
    # Print the articles and their similarity values
    for k, v in sim_sorted:
        if v != 0.0:
            print("Nilai Similaritas:", v)
            print(documents_clean[k])
            print()
# Add The Query
q1 = 'barcelona'
# Call the function
get_similar_articles(q1, df)