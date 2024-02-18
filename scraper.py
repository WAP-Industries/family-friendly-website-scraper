import requests
from bs4 import BeautifulSoup
from random import choice
import os

class Scraper:
    Home = "https://static.doujins.com"
    SaveFile = f"{os.path.dirname(os.path.abspath(__file__))}/config.txt"
    Config = {
        "Tags": [],
        "Exclude": []
    }
    
    @staticmethod
    def Error(message: str, code: str="") -> str:
        return f"Error{code:>{len(code)+bool(code)}}: {message}"

    @staticmethod
    def Scrape(tags: list, exclude: list, page: int, batch_size: int, random: bool, save: bool) -> str:
        try:
            response = requests.get(f"{Scraper.Home}/searches?words={'+'.join([*tags, *map(lambda x:f'-{x}', exclude)])}&page={page}")

            if response.status_code==200:
                doujins = [
                    f'{i.find("div", class_="title").find("div", class_="text").get_text()}\n{Scraper.Home}{i["href"]}'
                    for i in BeautifulSoup(response.text, "html.parser").find_all('a', href=True, class_="gallery-visited-from-favorites")     
                ][:batch_size]

                if save:
                    Scraper.Config["Tags"], Scraper.Config["Exclude"] = tags, exclude
                    Scraper.SaveConfig()
                
                return (choice(doujins or [None]) if random else "\n\n".join(doujins)) or "No doujins found"
            else:
                return Scraper.Error(response.reason, str(response.status_code))
        
        except Exception as e:
            return Scraper.Error(e)
        
    @staticmethod
    def SaveConfig() -> None:
        with open(Scraper.SaveFile, "w") as f:
            f.write("\n\n".join(["[{}]\n{}".format(i, "\n".join(Scraper.Config[i])) for i in Scraper.Config]))

    @staticmethod
    def LoadConfig() -> tuple:
        if not os.path.exists(Scraper.SaveFile):
            return (False, "save file does not exist")

        with open(Scraper.SaveFile, "r") as f:
            contents = [i for i in f.read().split("\n") if i.strip()]

        try:
            ind = contents.index("[Exclude]")
            Scraper.Config["Tags"], Scraper.Config["Exclude"] = contents[contents.index("[Tags]")+1:ind], contents[ind+1:] 
            return (True, "")
        except:
            return (False, "save file format is invalid")
