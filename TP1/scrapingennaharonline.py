import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

articles = []

for i in range(1, 1000):  
    url = f"https://www.ennaharonline.com/algeria/page/{i}/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page {i}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')
    
    for article in soup.find_all('article'):
        title_tag = article.find('a', class_='bunh')
        date_tag = article.find('time')  
        
        if title_tag and date_tag:
            title = title_tag.text.strip()
            date = date_tag.text.strip()
            articles.append([title, date])

if articles:
    df = pd.DataFrame(articles, columns=['Title', 'Date'])
    save_path = os.path.join(os.getcwd(), 'ennahar_articles.csv')  
    df.to_csv(save_path, index=False, encoding='utf-8-sig')
    
    print(f"Data saved successfully at: {save_path}")
    
    os.system(f"code {save_path}")
else:
    print("No articles found!")
