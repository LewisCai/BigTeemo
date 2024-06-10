import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Embed
from responses import *

#Load token
load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')

#Setup bot 
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


#Message handling 
async def send_message(message: Message, user_message: str, type:str) -> None:
    message_content = user_message[1:]
    response_manager = ResponseManager(message_content)
    try:
        if type == "mastery":
            #attributes
            champ_mastery = response_manager.get_response_mastery()
            icon_url = response_manager.get_response_icon()
            level = response_manager.get_response_level()

            bio = "Level: " + level + "\n" + "Best "+champ_mastery[0][0]+ " player"
            
            #create embed, which is a fancy message
            final_response = Embed(title=user_message[1:], description= bio, type="rich", color=0x00ff00)
            final_response.set_thumbnail(url=icon_url)

            for i in range(len(champ_mastery)):
                final_response.add_field(name=champ_mastery[i][0], value="Level: " + str(champ_mastery[i][1]) + "\n" + "Points: " + str(champ_mastery[i][2]), inline=False)

        elif type == "rank":
            #attributes
            rank = response_manager.get_response_rank()
            tier = response_manager.get_response_tier()
            icon_url = response_manager.get_response_icon()
            lp = response_manager.get_response_lp()
            wins = response_manager.get_response_wins()
            losses = response_manager.get_response_losses()
            win_rate = response_manager.get_response_win_rate()

            #get specific rank icon
            if tier == "UNRANKED":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/1/1c/Season_2013_-_Unranked.png/revision/latest?cb=20181116163918"
            elif tier == "IRON":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/f/fe/Season_2022_-_Iron.png/revision/latest/scale-to-width-down/250?cb=20220105213520"
            elif tier == "BRONZE":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/e/e9/Season_2022_-_Bronze.png/revision/latest/scale-to-width-down/250?cb=20220105214224"
            elif tier == "SILVER":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/4/44/Season_2022_-_Silver.png/revision/latest/scale-to-width-down/250?cb=20220105214225"
            elif tier == "GOLD":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/8/8d/Season_2022_-_Gold.png/revision/latest/scale-to-width-down/250?cb=20220105214225"
            elif tier == "PLATINUM":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/3/3b/Season_2022_-_Platinum.png/revision/latest/scale-to-width-down/250?cb=20220105214225"
            elif tier == "DIAMOND":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/3/37/Season_2023_-_Diamond.png/revision/latest/scale-to-width-down/250?cb=20231007195826"
            elif tier == "MASTER":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/e/eb/Season_2022_-_Master.png/revision/latest/scale-to-width-down/250?cb=20220105214311"
            elif tier == "GRANDMASTER":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/f/fc/Season_2022_-_Grandmaster.png/revision/latest/scale-to-width-down/250?cb=20220105214312"
            elif tier == "CHALLENGER":
                rank_icon_url = "https://static.wikia.nocookie.net/leagueoflegends/images/0/02/Season_2022_-_Challenger.png/revision/latest/scale-to-width-down/250?cb=20220105214312"

            #create embed, which is a fancy message
            if float(win_rate[:-2]) < 50:
                bio = "Win Rate: " + win_rate + "%\n" + "You're a noob"
            else:
                bio = "Win Rate: " + win_rate + "%\n" + "You're a pro"

            final_response = Embed(title=user_message[1:], description= bio, type="rich", color=0x00ff00)
            final_response.set_thumbnail(url=icon_url)
            final_response.set_image(url=rank_icon_url)

            final_response.add_field(name="Rank", value= tier + " " + rank + "\n", inline=True)
            final_response.add_field(name="LP", value=lp, inline=True)
            final_response.add_field(name="Wins", value=wins, inline=True)
            final_response.add_field(name="Losses", value=losses, inline=True)

            pass
        await message.reply(embed=final_response, mention_author=True, delete_after=100) #delete after 100 seconds
    except Exception as e:
        print(e)
        await message.reply("Sorry, I'm not sure how to respond to that", delete_after=10)

@client.event
async def on_ready() -> None:
    print(f'{client.user} has connected to Discord!')


#handle incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    if message.content.startswith('!'):
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'{username} in {channel} sent: {user_message}')
        await send_message(message, user_message, type="mastery")
    elif message.content.startswith('?'):
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'{username} in {channel} sent: {user_message}')
        await send_message(message, user_message, type="rank")
    elif message.content.startswith('$'):
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'{username} in {channel} sent: {user_message}')
        await send_message(message, user_message, type="all")


#main entry point
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()