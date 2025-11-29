import os
import asyncio
import discord
from discord.ext import commands

TOKEN = MTQ0MjI1MDY0OTg4NTczNjk2MQ.GpLreG.oN3WJ0myq6LWUJ9DJ-aMvJ655OyewdP4AoRxPI

# 🔐 Sécurité : seulement TOI + seulement TON serveur de test
ALLOWED_USER = 1316068882154393693
ALLOWED_GUILD = 1333038486332248135

# 🚫 Limites pour éviter les bans
MAX_CHANNELS = 100
SPAM_MESSAGES = 100

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


def allowed(ctx):
    return (
        ctx.author.id == ALLOWED_USER and
        ctx.guild and ctx.guild.id == ALLOWED_GUILD
    )


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")


@bot.command()
async def nuke(ctx, amount: int = 5):
    if not allowed(ctx):
        return await ctx.send("❌ Tu n'as pas le droit d'utiliser cette commande.")

    amount = max(1, min(amount, MAX_CHANNELS))
    guild = ctx.guild

    await ctx.send("⚠️ **Préparation du NUKE...**")

    # 🔥 0️⃣ Changer le nom du serveur
    try:
        await guild.edit(name="💥 SERVEUR DÉTRUIT 💥")
    except:
        pass

    # 2️⃣ Créer des salons "nuke"
    new_channels = []
    for i in range(amount):
        try:
            c = await guild.create_text_channel(f"nuked-{i+1}")
            new_channels.append(c)
            await asyncio.sleep(0.1)
        except:
            pass

    # 3️⃣ Spam dans les nouveaux salons
    for c in new_channels:
        for i in range(SPAM_MESSAGES):
            try:
                await c.send("💥 Serveur NUKED💥")
                await asyncio.sleep(0.03)
            except:
                pass

    # 4️⃣ Message d'annonce final
    try:
        await new_channels[0].send("@everyone🚨 **LE SERVEUR A ÉTÉ DÉTRUIT** 🚨")
    except:
        pass

    await ctx.send("🔥 **NUKE TERMINÉ !**")