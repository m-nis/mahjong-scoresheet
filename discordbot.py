import discord
import os
import traceback
from discord.ext import commands

# TODO get players from discord channel joiners
# def command add_player?
players = {0: 'nishiya', 1: 'hattori', 2: 'sugai aka kasu', 3: 'ofuji',
           4: 'nakamura', 5: 'yamada', 6: 'takeda', 7: 'komoto', 8: 'arisawa', 9: 'kogai'}

cur_players = []

scores_db = []
scores_sum = [0, 0, 0, 0]

description = '''bot to store/calc mahjong scores'''

token = os.environ['MAHJONG_BOT_TOKEN']
print(token)
bot = commands.Bot(command_prefix='/', description=description)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def choose(ctx, p1: int, p2: int, p3: int, p4: int) -> list:
    """choose 4 players from dictionary: players"""
    # TODO check if there are no
    # initialization
    global scores_db
    global scores_sum
    scores_db = []
    scores_sum = [0, 0, 0, 0]
    global cur_players
    cur_players = [players[p1], players[p2], players[p3], players[p4]]

    await ctx.send('you chose: {0}'.format(cur_players))
    await ctx.send('''add scores using `/add` command
eg) `/add 45.1 4.9 -20.0 -30.0`
*tobashitara +10, tobasaretara -10 shiteoite''')


@bot.command()
async def add(ctx, s1: float, s2: float, s3: float, s4: float):
    """convert game score to final score"""
    scores = [s1, s2, s3, s4]
    if sum(scores) != 0.0:
        await ctx.send('sum of scores should be 0; type again')
        return
    scores.sort()
    scores[0] -= 10
    scores[1] -= 10
    scores[3] += 20
    await ctx.send(scores)
    global scores_db
    global scores_sum
    global cur_players
    scores_db.append(scores)
    displayed_player_name = cur_players[:]

    for i in range(4):
        scores_sum[i] += scores[i]
        displayed_player_name[i] = displayed_player_name[i][:5]
    displayed_scores_db = ''
    for i in scores_db:
        displayed_scores_db += str(i) + '\n'

    await ctx.send('''```
{0}
{1}

total
{2}```'''.format(displayed_player_name, displayed_scores_db, scores_sum))

# TODO def command `del` to delete 1 previous score
# @bot.command()
# async def del(ctx):

# TODO def command `help` to inform about bot usage


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(
        traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


bot.run(token)
