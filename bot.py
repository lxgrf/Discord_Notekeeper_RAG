from dotenv import load_dotenv
import os
import discord
from discord import app_commands

class GuildCheckFailure(app_commands.errors.CheckFailure):
    pass

class RoleCheckFailure(app_commands.errors.CheckFailure):
    pass

# Load secrets
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# List of approved guild IDs
APPROVED_GUILDS = [1114617197931790376]

def guild_check():
    @app_commands.check
    def is_approved_guild(interaction: discord.Interaction) -> bool:
        if interaction.guild_id not in APPROVED_GUILDS:
            raise GuildCheckFailure()
        return True
    return is_approved_guild

def authority_check():
    @app_commands.check
    def has_required_role(interaction: discord.Interaction) -> bool:
        member_roles = [role.name.lower() for role in interaction.user.roles]
        if not any(role in member_roles for role in ['admin', 'lorekeeper']):
            raise RoleCheckFailure()
        return True
    return has_required_role


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        await tree.sync()
        print("Synced command tree")
    except Exception as e:
        print(e)

@tree.command(name="hello", description="Get a friendlty greeting from the bot! (And prove that it's responsive)")
@guild_check
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.use.name}!")

@tree.command(name="ask", description = "Ask the bot a question")
@guild_check
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)

    #TODO Carry out local LLM query

    await interaction.followup.send("This function has not yet been implemented.")

@tree.command(name="update",description="Update the database. This may take a few minutes.")
@guild_check
@authority_check
async def update(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    #TODO Update Notion elements, create embeds, store

    await interaction.followup.send("This function has not yet been implemented.")

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    error_messages = {
        GuildCheckFailure: "Sorry, this bot is not authorized to respond in this server.",
        RoleCheckFailure: "You don't have permission to use this command. Required role: Admin or Lorekeeper",
    }
    
    # Get the appropriate error message or default to generic error
    message = error_messages.get(type(error), "An error occurred while processing the command.")
    await interaction.response.send_message(message, ephemeral=True)
    

# Run the bot
if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_NOTEKEEPER_KEY'))