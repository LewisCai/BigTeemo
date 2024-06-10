from random import choice, randint
import os
from dotenv import load_dotenv
import requests

class ResponseManager:
        
    def __init__(self, user_input: str):
        load_dotenv()
        self.KEY: str = os.getenv('RIOT_API_KEY')
        self.user_input = user_input
        self.puuid = self.get_puuid(self.user_input)
        self.summoner_id = ""
        self.account_id = ""
        self.profile_icon_id = ""
        self.summoner_level = ""
        self.tier = ""
        self.rank = ""
        self.lp = "" #league points
        self.wins = ""
        self.losses = ""
        self.win_rate = ""
        self.get_response_summoner()


    def get_puuid(self, user_input: str) -> str:
        gameName = user_input.split("#")[0]
        tagLine = user_input.split("#")[1]

        #API URL
        api_url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" +gameName+ "/" +tagLine+ "?api_key=" + self.KEY

        #call API
        response = requests.get(api_url)
        data = response.json()

        #extract data
        puuid = data['puuid']
        return puuid

    def get_response_mastery(self) -> list[str]:
        puuid = self.puuid

        #API URL
        api_url = "https://oc1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/" + puuid + "/top?count=5&api_key=" + self.KEY

        #call API
        response = requests.get(api_url)
        data = response.json()

        output_list = []
        for i in range(len(data)):
            champion_id = data[i]['championId']
            champion_name = self.get_response_champion(champion_id)
            champion_level = data[i]['championLevel']
            champion_points = data[i]['championPoints']
            
            output_list.append((champion_name, champion_level, champion_points))

        return output_list



    def get_response_champion(self, champion_id: str) -> str:
        #API URL
        api_url = "http://ddragon.leagueoflegends.com/cdn/11.20.1/data/en_US/champion.json"

        #call API
        response = requests.get(api_url)
        data = response.json()

        # Find the champion name by matching the key
        for champion_data in data['data'].values():
            if int(champion_data['key']) == champion_id:
                return champion_data['name']
        return "Unknown Champion"
    
    def get_response_summoner(self) -> None:
        #https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/eLUepsw-GPkwrAjHKonm_3srlxG3NO8p66150ZgOQR-MT8QJkCePKbe3iOLVMtvOSCCRiB--pJ0aZg?api_key=RGAPI-65d95742-26d6-4830-9e9c-08d793068818
        puuid = self.puuid

        #API URL
        api_url = "https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/" + puuid + "?api_key=" + self.KEY


        #call API
        response = requests.get(api_url)
        data = response.json()

        self.summoner_id = data['id']
        self.account_id = data['accountId']
        self.profile_icon_id = data['profileIconId']
        self.summoner_level = data['summonerLevel']

        #https://oc1.api.riotgames.com/lol/league/v4/entries/by-summoner/H3EMMQQmQ85Yvu5ZkvPl8NWB2zxpACdk0lFZK_8627Zjltc?api_key=RGAPI-65d95742-26d6-4830-9e9c-08d793068818
        summoner_id = self.summoner_id

        #API URL
        api_url = "https://oc1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + summoner_id + "?api_key=" + self.KEY

        #call API
        response = requests.get(api_url)
        data = response.json()[2]

        self.tier = data['tier']
        self.rank = data['rank']
        self.lp = data['leaguePoints']
        self.wins = data['wins']
        self.losses = data['losses']
        self.win_rate = str(round((int(self.wins)/(int(self.wins)+int(self.losses)))*100, 2)) + "%"

        return 

    def get_response_icon(self) -> str:
        return f"https://ddragon.leagueoflegends.com/cdn/11.20.1/img/profileicon/{self.profile_icon_id}.png"

    def get_response_level(self) -> str:
        return str(self.summoner_level)
    
    def get_response_tier(self) -> str:
        return self.tier
    
    def get_response_rank(self) -> str:
        return self.rank
    
    def get_response_lp(self) -> str:
        return str(self.lp)
    
    def get_response_wins(self) -> str:
        return str(self.wins)

    def get_response_losses(self) -> str:
        return str(self.losses)
    
    def get_response_win_rate(self) -> str:
        return self.win_rate