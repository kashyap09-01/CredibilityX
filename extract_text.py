from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pickle

class extractText :
    def __init__(self,url):
        self.url = url
        self.file = open('Downloads/vectorizer.pkl','rb')
        self.vectorizer = pickle.load(open('Downloads/vectorizer.pkl','rb'))
    def getText(self):
        html = urlopen(self.url).read()
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
        # print(text)
        # print(text,type(text))
        port_stem = PorterStemmer()
        def stemming(content):
            stemmed_content = re.sub('[^a-zA-Z]',' ',content)
            stemmed_content = stemmed_content.lower()
            stemmed_content = stemmed_content.split()
            stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
            stemmed_content = ' '.join(stemmed_content)
            return stemmed_content
        X = stemming(text)
        X = self.vectorizer.transform([X])   
        # print(X)
        return text

if __name__=="__name__":
    pass