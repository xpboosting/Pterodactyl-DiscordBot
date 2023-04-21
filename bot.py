import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def register(ctx):
    # Create the initial embed and send it to the user
    embed = discord.Embed(title="User Registration", color=discord.Color.green())
    embed.add_field(name="Step 1", value="Please enter your username:")
    message = await ctx.send(embed=embed)

    # Wait for the username to be entered
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    username = await bot.wait_for('message', check=check)

    # Update the embed with the new information
    embed.set_field_at(0, name="Step 1", value=username.content)
    embed.add_field(name="Step 2", value="Please enter your password:")
    await message.edit(embed=embed)

    # Wait for the password to be entered
    password = await bot.wait_for('message', check=check)

    # Update the embed with the new information
    embed.set_field_at(1, name="Step 2", value="**********")
    embed.add_field(name="Step 3", value="Please enter your email:")
    await message.edit(embed=embed)

    # Wait for the email to be entered
    email = await bot.wait_for('message', check=check)

    # Call the API to register the user
    API_URL = "url"
    API_KEY = "key"

    data = {
        "email": email.content,
        "username": username.content,
        "password": password.content,
        "first_name": "First",
        "last_name": "Last",
        "language": "en",
        "root_admin": False,
        "2fa": False
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, headers=headers, json=data)

    # Update the embed with the registration status
    if response.status_code == 201:
        embed.set_field_at(2, name="Step 3", value=email.content)
        embed.add_field(name="Registration Status", value="User created successfully!", inline=False)
        embed.color = discord.Color.green()
    else:
        embed.add_field(name="Registration Status", value="User could not be created.", inline=False)
        embed.color = discord.Color.red()

    await message.edit(embed=embed)


bot.run('token')
