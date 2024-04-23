from flask import Flask, request, jsonify
import urllib.request
from bs4 import BeautifulSoup
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Function to fetch text data from a given URL
def fetch_text_from_url(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    text_data = []
    for paragraph in soup.find_all('p'):
        text_data.append(paragraph.get_text())
    full_text = '\n'.join(text_data)
    cleaned_text = re.sub(r'\[[0-9]*\]', ' ', full_text)  # Remove citation numbers
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with a single space
    sentences = re.split(r'\.|\?|\!', cleaned_text)
    return sentences

# Initialize TF-IDF Vectorizer and transform sentences into TF-IDF matrix
url = 'https://en.wikipedia.org/wiki/Chatbot'
sentences = fetch_text_from_url(url)
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

# Function to find the most matching response to a user query
def find_matching_response(user_query, sentences, tfidf_vectorizer, tfidf_matrix):
    query_vector = tfidf_vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    most_similar_index = similarities.argmax()
    return sentences[most_similar_index]

# Define Flask API endpoint
@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_query = data['query']
    matching_response = find_matching_response(user_query, sentences, tfidf_vectorizer, tfidf_matrix)
    return jsonify({'response': matching_response})

if __name__ == '__main__':
    app.run(debug=True)
