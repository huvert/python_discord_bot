import os
import discord
import requests
import youtube_dl
from discord.ext import commands

TOKEN = "NzQxMzg5MDc1NzM0NTkzNTQ0.Xy22YQ.UUvYxRbMfzSMa3BU8D6FnOhJq6o"
PREFIX = '_'

# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


bot = commands.Bot(PREFIX, description='Yet another music bot.')


for filename in os.listdir('./cogs'):   # ./ --> Current folder
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


# ------------------------------------
# ----------    Commands    ----------
@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))


@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')


@bot.command()
async def clear(ctx, amount=1):
    """Clear 'x' number of messages. ex: _clear 3"""
    await ctx.channel.purge(limit=(amount+1))


@bot.command()
async def insult(ctx):
    """Random insult"""
    res = requests.get('https://evilinsult.com/generate_insult.php?lang=en')
    await ctx.send(res.text)


@bot.command()
async def nobody(ctx):
    """Returns AI-generated image of a person"""
    res = requests.get('https://thispersondoesnotexist.com/image')
    if res.status_code == 200:
        with open('nobody.png', 'wb') as f:
            f.write(res.content)
        with open('nobody.png', 'rb') as f:
            await ctx.send("Here is an AI generated picture of no one in particular\n", file=discord.File(f))
    else:
        await ctx.send("Something went wrong =(")


@bot.command()
async def pwbreach(ctx, myPasswordSHA1):
    """Checks for pw-breaches. Input: Your pw in SHA-1 format"""
    res = requests.get(f"https://api.pwnedpasswords.com/range/{myPasswordSHA1[:5]}")
    myPW = myPasswordSHA1[5:]
    mes = "No breaches found! :D"
    if res.status_code == 200:
        content = res.text.split("\r\n")
        for cnt in content:
            if myPW == cnt[:35]:
                print("[bot] Password has been breached!")
                x = cnt.split(":")
                mes = f"Your password has been found in breached files {x[1]} times!"
    else:
        mes = "Something went wrong! :("
    await ctx.send(mes)


@bot.command()
async def HELPpwbreach(ctx):
    """Shows more info about function 'pwbreach'"""
    await ctx.send("""***DO NOT TYPE YOUR OWN UNENCRYPTED PASSWORD ON DISCORD!***\n
    function should be used as follows:
    \t \t_pwbreach 'Passowrd in format SHA-1'
    ex:\t_pwbreach FFC0F2952FD99C4B9147D6A101D031DABB9\n
    visit https://passwordsgenerator.net/sha1-hash-generator/ for SHA-1 convertion""")


bot.run(TOKEN)
