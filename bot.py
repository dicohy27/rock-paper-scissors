import discord
from discord.ext import commands
from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class RSP(Enum):
    ROCK = 1
    SCISSORS = 2
    PAPER = 3

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def hello(message):
    await message.send('Hi!')

def get_winner(user1, user2):
    rsp1 = user1[1]
    rsp2 = user2[1]
    name1 = user1[0]
    name2 = user2[0]

    ret = ''
    ret += f'{name1}님은 {rsp1}를 냈고, {name2}님은 {rsp2}를 냈습니다.\n'
    if rsp1 == rsp2:
        ret += '무승부 입니다!'
    elif (rsp1 == '바위' and rsp2 == '가위') or (rsp1 == '가위' and rsp2 == '보') or (rsp1 == '보' and rsp2 == '바위'):
        ret += f'{name1}님이 이겼습니다!'
    else:
        ret +=  f'{name2}님이 이겼습니다!'
    return ret
    
@bot.command()
async def play(ctx):
    dropdown = discord.ui.Select(
        placeholder="Select an option",
        options=[
            discord.SelectOption(label="가위", value=RSP.SCISSORS.value),
            discord.SelectOption(label="바위", value=RSP.ROCK.value),
            discord.SelectOption(label="보", value=RSP.PAPER.value),
        ],
    )

    selections = []
    async def my_callback(interaction):
        rsp = ""
        if(int(interaction.data['values'][0])==RSP.ROCK.value): rsp = "바위"
        elif(int(interaction.data['values'][0])==RSP.SCISSORS.value): rsp = "가위"
        elif(int(interaction.data['values'][0])==RSP.PAPER.value): rsp = "보"
        selections.append([interaction.user.display_name, rsp])
        
        await interaction.response.send_message(f"{interaction.user.display_name}님이 {rsp}를 선택하셨습니다.", ephemeral=True)
        if len(selections)==2:
            channel = interaction.channel
            await channel.send(f"{selections[0][0]} vs {selections[1][0]}")
            str = get_winner(selections[0], selections[1])
            await channel.send(str)
            selections.clear()
            #disable dropdown
            dropdown.disabled = True
            await message.edit(view=view)

    dropdown.callback = my_callback
    view = discord.ui.View()
    view.add_item(dropdown)
    message = await ctx.send("선택하세요:", view=view)

bot.run(DISCORD_TOKEN)
