import requests
from bs4 import BeautifulSoup as bs

# Start the session
session = requests.Session()

# Create the payload
payload = {'username':'userjzfw5pml', 
          'password':'oliver0424'
         }

# Post the payload to the site to log in
s = session.post("https://coderbyte.com/sl", data=payload)

# Navigate to the next page and scrape the data
s = session.get('https://coderbyte.com/developers')

soup = bs(s.text, 'html.parser')

print(soup)
