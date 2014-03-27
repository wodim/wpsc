from bs4 import BeautifulSoup
import requests

url = 'http://marketplaceedgeservice.windowsphone.com/v8/catalog/apps/6e5405fa-e5cc-4a6c-8e54-3932ab7075c3?os=8.0.10521.0&cc=VE&lang=es-ve&moId='
contenido = requests.get(url).text.encode('utf-8')
soup = BeautifulSoup(contenido, 'xml')
print soup