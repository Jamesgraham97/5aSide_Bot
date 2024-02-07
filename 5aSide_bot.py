import discord
import random
import schedule
import time

intents = discord.Intents.default()  # Create Intents object with default intents
client = discord.Client(intents=intents)  # Pass Intents object when creating Client instance
all_players = {}  # Dictionary to store player data with MMR for all players
game_pool = []    # List to store players available for the upcoming game
team1 = []        # List to store players in Team 1
team2 = []        # List to store players in Team 2

# Handle all messages
@client.event
async def on_message(message):
    global team1, team2  # Declare team1 and team2 as global

    if message.content.startswith('!join'):
        player_name = message.content.split(' ')[1]  # Extract player name from message
        if player_name not in all_players:
            all_players[player_name] = 1000  # Assign base MMR if the player is new
            await message.channel.send(f'{player_name} joined the players pool.')
        else:
            await message.channel.send(f'{player_name} is already in the players pool.')

    elif message.content.startswith('!addmatch'):
        player_name = message.content.split(' ')[1]  # Extract player name from message
        if player_name in all_players:  # Check if the player exists
            game_pool.append(player_name)
            await message.channel.send(f'{player_name} added to the match pool for this week.')
        else:
            await message.channel.send(f'{player_name}, you need to join the players pool first using !join.')

    elif message.content.startswith('!clearmatch'):
        game_pool.clear()
        team1.clear()  # Clear Team 1
        team2.clear()  # Clear Team 2
        await message.channel.send('Match pool cleared for the next week.')

    elif message.content.startswith('!generateteams'):
        if len(game_pool) < 2:
            await message.channel.send('Not enough players in the match pool.')
        else:
            team1, team2 = generate_teams()  # Assign the generated teams directly
            await message.channel.send(f'Team 1: {", ".join(team1)}\nTeam 2: {", ".join(team2)}')

    elif message.content.startswith('!win'):
        winning_team = message.content.split(' ')[1]  # Extract the winning team from the message

        if winning_team == '1':
            # Increase MMR of players in Team 1 and decrease MMR of players in Team 2
            for player in team1:
                all_players[player] += 50  # You can adjust the MMR increment as needed
            for player in team2:
                all_players[player] -= 50  # You can adjust the MMR decrement as needed
            await message.channel.send('Team 1 wins! MMR updated for both teams.')
        elif winning_team == '2':
            # Increase MMR of players in Team 2 and decrease MMR of players in Team 1
            for player in team2:
                all_players[player] += 50  # You can adjust the MMR increment as needed
            for player in team1:
                all_players[player] -= 50  # You can adjust the MMR decrement as needed
            await message.channel.send('Team 2 wins! MMR updated for both teams.')
        else:
            await message.channel.send('Invalid team number.')

# Function to generate balanced teams based on overall MMR and equal team size
def generate_teams():
    global game_pool  # Use the global game_pool

    random.shuffle(game_pool)  # Randomize the order of players

    # Determine the team size
    team_size = len(game_pool) // 2

    # Divide the players into two teams
    team1 = game_pool[:team_size]
    team2 = game_pool[team_size:]

    # Calculate overall MMR for each team
    team1_mmr = sum(all_players[player] for player in team1)
    team2_mmr = sum(all_players[player] for player in team2)

    # Adjust teams to balance overall MMR
    while abs(team1_mmr - team2_mmr) > 100:  # Adjust threshold as needed
        # If the difference in overall MMR is too large, swap a player between the teams
        if team1_mmr > team2_mmr:
            random_player = random.choice(team1)
            team1.remove(random_player)
            team2.append(random_player)
        else:
            random_player = random.choice(team2)
            team2.remove(random_player)
            team1.append(random_player)

        # Update overall MMR for each team
        team1_mmr = sum(all_players[player] for player in team1)
        team2_mmr = sum(all_players[player] for player in team2)

    return team1, team2

client.run('MTIwNDc1ODI0NDg3OTI0NTM0Mg.GtuCJM.GEdSngnRjvBhrMaIreUA3jACFNfdmmYaqvrJwk')
