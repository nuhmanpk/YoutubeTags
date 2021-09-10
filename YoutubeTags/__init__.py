from bs4 import BeautifulSoup
import html5lib
import requests 

def videotags(url):
      
         try:
              request = requests.get(url)
              soup = BeautifulSoup(request.content, 'html5lib') 
              tags = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta",{"property": "og:video:tag"}) ])
              return tags
      	
         except:
              return None
