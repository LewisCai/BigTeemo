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
            champ_mastery = response_manager.get_response_mastery()
            icon_url = response_manager.get_response_icon()
            level = response_manager.get_response_level()

            bio = "Level: " + level + "\n" + "Best "+champ_mastery[0][0]+ " player"
            
            #create embed, which is a fancy message
            final_response = Embed(title=user_message[1:], description= bio, type="rich")
            final_response.set_thumbnail(url=icon_url)

            for i in range(len(champ_mastery)):
                final_response.add_field(name=champ_mastery[i][0], value="Level: " + str(champ_mastery[i][1]) + "\n" + "Points: " + str(champ_mastery[i][2]), inline=False)


        elif type == "game":
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


#main entry point
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()