from bs4 import BeautifulSoup
import html5lib
import requests 

class Tags:
      
      def __init__(url:str):
      
         try:
              request = requests.get(url)
              soup = BeautifulSoup(request.content, 'html5lib') 
              tags = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta",{"property": "og:video:tag"}) ])
              return tags
      	
         except:
              print(error)    
                
