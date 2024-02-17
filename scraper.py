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
        return f"Error{code}: {message}"

    @staticmethod
    def FormQuery(t: list, e: list, p: int) -> str:
        return f"{Scraper.Home}/searches?words={'+'.join([*t, *map(lambda x:f'-{x}', e)])}&page={p}"

    @staticmethod
    def Scrape(tags: list, exclude: list, page: int, batch_size: int, random: bool, save: bool) -> str:
        try:
            response = requests.get(Scraper.FormQuery(tags, exclude, page))

            if response.status_code==200:
                contents = BeautifulSoup(response.text, "html.parser")
                doujins = [
                    f'{i.find("div", class_="title").find("div", class_="text").get_text()}\n{Scraper.Home}{i["href"]}'
                    for i in contents.find_all('a', href=True, class_="gallery-visited-from-favorites")     
                ][:batch_size]

                if save:
                    Scraper.Config["Tags"], Scraper.Config["Exclude"] = tags, exclude
                    Scraper.SaveConfig()
                
                return (choice(doujins or [None]) if random else "\n\n".join(doujins)) or "No doujins found"
            else:
                return Scraper.Error(response.reason, f" {response.status_code}")
        
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
            Scraper.Config["Tags"] = contents[contents.index("[Tags]")+1:ind]
            Scraper.Config["Exclude"] = contents[ind+1:]
            return (True, "")
        except:
            return (False, "save file format is invalid")