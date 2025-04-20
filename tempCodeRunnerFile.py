import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

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

# Take input from the user (in your website, this would come from a form submission)
user_input = "X Fires Its Election Team Before a Huge Election Year"

# Preprocess the user input
user_input_processed = preprocess_input(user_input)

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
