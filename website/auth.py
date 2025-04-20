from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import warnings
from urllib.request import urlopen
from bs4 import BeautifulSoup


# Ignore all warnings (not recommended for production code)
warnings.filterwarnings("ignore")

# Or, ignore specific types of warnings (recommended)
warnings.filterwarnings("ignore", category=UserWarning)

# Load the model and vectorizer
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Function to preprocess user input
def preprocess_input(user_input):
    port_stem = PorterStemmer()
    stemmed_content = re.sub('[^a-zA-Z]',' ',user_input)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content


auth = Blueprint('auth', __name__)

@auth.route('/text-check', methods=['GET', 'POST'])
def text_check():
    if request.method == 'POST':
        text = request.form.get('text')
        user_input_processed = preprocess_input(text)

        # Convert to numerical data
        user_input_vectorized = vectorizer.transform([user_input_processed])

        # Predict using the pre-trained model
        user_prediction = model.predict(user_input_vectorized)

        # Calculate confidence percentage
        confidence_percentage = model.predict_proba(user_input_vectorized)[0][1] * 100

        # Determine the result and confidence to display on your website
        if user_prediction[0] == 1:
            result = "REAL"
        else:
            result = "FAKE"
        
        output = {
                "result": result,
                "confidence_percentage": confidence_percentage
        }

        return render_template('index.html', output = output)
    else:
        return render_template('index.html')

from pypdf import PdfReader

@auth.route('/file-check', methods=['GET', 'POST'])
def file_check():
    if request.method == 'POST':
        file_name = request.form.get('myfile')
        reader = PdfReader(file_name)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            page_text=page_text.replace(' ','')
            text+=page_text.replace('\n',' ')+ " "

        user_input_processed = preprocess_input(text)

        # Convert to numerical data
        user_input_vectorized = vectorizer.transform([user_input_processed])

        # Predict using the pre-trained model
        user_prediction = model.predict(user_input_vectorized)

        # Calculate confidence percentage
        confidence_percentage = model.predict_proba(user_input_vectorized)[0][1] * 100

        # Determine the result and confidence to display on your website
        if user_prediction[0] == 1:
            result = "REAL"
        else:
            result = "FAKE"
        
        pdf_output = {
                "result": result,
                "confidence_percentage": confidence_percentage
        }

        return render_template('index.html', pdf_output = pdf_output)
    else:
        return render_template('index.html')

@auth.route('/link-check', methods=['GET', 'POST'])
def link_check():
    if request.method == 'POST':
        url = request.form.get('url')
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ' '.join(chunk for chunk in chunks if chunk)

        user_input_processed = preprocess_input(text)

        # Convert to numerical data
        user_input_vectorized = vectorizer.transform([user_input_processed])

        # Predict using the pre-trained model
        user_prediction = model.predict(user_input_vectorized)

        # Calculate confidence percentage
        confidence_percentage = model.predict_proba(user_input_vectorized)[0][1] * 100

        # Determine the result and confidence to display on your website
        if user_prediction[0] == 1:
            result = "REAL"
        else:
            result = "FAKE"
        
        url_output = {
                "result": result,
                "confidence_percentage": confidence_percentage
        }

        return render_template('index.html', url_output = url_output)
    else:
        return render_template('index.html')