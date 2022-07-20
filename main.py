from multiprocessing import connection
from pickle import NONE
import sqlite3
import discord
from discord.ext import commands
import asyncio
import datetime
from datetime import date
import os

bot = commands.Bot(command_prefix='+', intents=discord.Intents.all())

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Готов')
    await bot.change_presence(activity=discord.Game(name="Слежку"))

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    extension = extension.lower()
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} загружен')
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    extension = extension.lower()
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} разгружен')
    await ctx.message.delete()

@bot.command(name="secretrole")
async def role(ctx):
    role = discord.utils.get(ctx.author.guild.roles, id=997379312628023306)
    author = ctx.message.author.id
    await ctx.author.add_roles(role)
    await ctx.author.send(f'<@{author}> пс парень, ты кажется отгадал секретную роль.')
    await ctx.message.delete()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
@commands.has_permissions(administrator=True)
async def sendembed(ctx):
  embed = discord.Embed(title="Стой:bangbang:", description="Напиши наше секретное слово[+open]")
  msg = await ctx.channel.send(embed=embed)
  await ctx.message.delete()

@bot.command(name="open")
async def role(ctx):
    role = discord.utils.get(ctx.author.guild.roles, id=996701807629848606)
    await ctx.author.add_roles(role)
    await ctx.author.send(f'{ctx.author.display_name} вы успешно прошли на наш сервер, удачи вам (соблюдайте правила)', delete_after = 120)
    await ctx.message.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None, time = None, *, reasone = None):
    muted_role = discord.utils.get(ctx.guild.roles, name = 'Muted')
    author = ctx.message.author.id
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    if member == None:
        await ctx.send(f'<@{author}> Вы забыли указать пользователя.')
    elif time == None:
        await ctx.send(f'<@{author}> Вы забыли указать время.')
    elif reasone == None:
        reasone = "не указана"
    tempmute = int(time[:-1]) * time_convert[time[-1]]
    embed = discord.Embed(title = '**Выдал пользователю мут**', description = f'Пользователь {member.mention} получил мут от модера <@{author}>.', color=0xff0000)

    await member.send(embed = embed)
    await ctx.message.delete()
    await member.add_roles(muted_role)
    await asyncio.sleep(tempmute)
    await member.remove_roles(muted_role)


bot.run('TOKEN')
