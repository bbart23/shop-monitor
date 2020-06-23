import requests
from bs4 import BeautifulSoup

URL = 'https://www.supremenewyork.com/shop/all/jackets'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='container')

print(results.prettify())