import discord
import random
import string
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='/', intents = intents)

@client.event
async def on_ready():
    print('Bot is ready.')

# @client.event
# async def on_member_join(member):
#     print(f"{member} has joined the server.")

# @client.event
# async def on_member_remove(member):
#     print(f"{member} has left the server.")

# @client.command()
# async def mine(ctx, *, miningtime):
#     lower_upper_alphabet = string.ascii_letters
#     url = 'https://discord.gg/'
#     i = 0
#     while i < int(miningtime):
#         n = random.randint(8, 10)
#         for z in range(n):
#             random_choice = random.randint(1, 5)
#             if random_choice != 1:
#                 random_letter = random.choice(lower_upper_alphabet)
#                 url1 = url + random_letter
#                 url = url1
#             else:
#                 random_number = random.randint(1, 9)
#                 url2 = url + str(random_number)
#                 url = url2
#         await ctx.send(url)
#         url = 'https://discord.gg/'
#         i += 1


# @client.command()
# async def ping(ctx):
#     await ctx.send(f'Ping! {round(client.latency * 1000)}ms')

# @client.command(aliases=['8ball', 'test'])
# async def _8ball(ctx, *, question):
#     responses = ['It is certain.',
#                  'It is decidedly so.',
#                  'Without a doubt.',
#                  'Yes - definitely.',
#                  'You may rely on it',
#                  'As I see it, yes',
#                  'Most likely',
#                  'Outlook good',
#                  'Yes',
#                  'Signs point to yes.',
#                  'Reply hazy, try again.',
#                  'Ask again later.',
#                  'Better not tell you now.',
#                  'Cannot predict now.',
#                  'Concentrate and ask again.',
#                  'Don\'t count on it.',
#                  'My reply is no.',
#                  'My sources say no.',
#                  'Outlook not so good.',
#                  'Very doubtful.']
#     await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# @client.command()
# async def clear(ctx):
#     await ctx.channel.purge()

# @client.command()
# async def kick(ctx, member : discord.Member, *, reason=None):
#     await member.kick(reason = reason)

# @client.command()
# async def ban(ctx, member : discord.Member, *, reason=None):
#     await member.ban(reason = reason)
#     await ctx.send(f'Banned {member.mention}')

# @client.command()
# async def unban(ctx, *, member):
#     banned_users = await ctx.guild.bans()
#     member_name, member_discriminator = member.split('#')
#     for ban_entry in banned_users:
#         user = ban_entry.user
#         if(user.name, user.discriminator) == (member_name, member_discriminator):
#             await ctx.guild.unban(user)
#             await ctx.send(f'Unbanned {member_name}#{member_discriminator}')
#             return


client.run('ODUwNzA5ODU5NTk0MTQxNzI2.YLtrSw._jNKpYk8ntPA7unzfOc6mbJuf8g')