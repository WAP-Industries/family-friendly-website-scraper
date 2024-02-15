import requests
from bs4 import BeautifulSoup
from random import choice

class Scraper:
    Home = "https://static.doujins.com"

    @staticmethod
    def FormQuery(t, e, p):
        return f"{Scraper.Home}/searches?words={'+'.join([*t, *map(lambda x:f'-{x}', e)])}&page={p}"

    @staticmethod
    def Scrape(tags, exclude, page=1, batch_size=None, random=False):
        try:
            response = requests.get(Scraper.FormQuery(tags, exclude, page))

            if response.status_code==200:
                contents = BeautifulSoup(response.text, "html.parser")
                doujins = [
                    f'{i.find("div", class_="title").find("div", class_="text").get_text()}\n{Scraper.Home}/{i["href"]}'
                    for i in contents.find_all('a', href=True, class_="gallery-visited-from-favorites")     
                ][:batch_size]
                
                return (choice(doujins) if random else "\n\n".join(doujins)) or "No doujin found"
            else:
                return f"{response.status_code}: {response.reason}" 
        
        except Exception as e:
            return f"Error: {e}"