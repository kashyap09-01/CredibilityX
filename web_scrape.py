from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request
import time

# Function to scrape website
def scrape_website(page_number):
    page_num = str(page_number)
    URL = 'https://www.politifact.com/factchecks/list/?page='+page_num
    webpage = requests.get(URL)
    soup = BeautifulSoup(webpage.text,'html.parser')
    statement_footer = soup.find_all('footer', attrs={'class':'m-statement__footer'})
    statement_quote = soup.find_all('div', attrs={'class': 'm-statement__quote'})
    statement_meta = soup.find_all('div', attrs={'class':'m-statement__meta'})
    target = soup.find_all('div', attrs={'class':'m-statement__meter'})

    for i in statement_footer:
        link1 = i.text.strip()
        name_and_date = link1.split()
        first_name = name_and_date[1]
        last_name = name_and_date[2]
        full_name = first_name + ' ' + last_name
        month = name_and_date[4]
        day = name_and_date[5]
        year = name_and_date[6]
        date = month + ' ' + day + ' ' + year
        dates.append(date)
        authors.append(full_name)

    for i in statement_quote:
        link2 = i.find_all('a')
        statement_text = link2[0].text.strip()
        statements.append(statement_text)

    for i in statement_meta:
        link3 = i.find_all('a')
        source_text = link3[0].text.strip()
        sources.append(source_text)

    for i in target:
        link4 = i.find('div', attrs={'class':'c-image'}).find('img').get('alt')
        targets.append(link4)

# Load existing data from CSV
try:
    existing_data = pd.read_csv('file.csv')
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=['author', 'statement', 'source', 'date', 'target'])

# Lists to store scraped data
authors = []
dates = []
statements = []
sources = []
targets = []

n = 2
for i in range(1, n):
    scrape_website(i)

# Combine new data with existing data
new_data = pd.DataFrame({
    'author': authors,
    'statement': statements,
    'source': sources,
    'date': dates,
    'target': targets
})

# Check if entries already exist in the database based on author and statement
new_data = new_data[~new_data[['author', 'statement']].apply(tuple, axis=1).isin(existing_data[['author', 'statement']].apply(tuple, axis=1))]

# Append new entries to existing data
updated_data = pd.concat([existing_data, new_data], ignore_index=True)

# Save updated data back to CSV
updated_data.to_csv('file.csv', index=False)

print(new_data)