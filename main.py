from dotenv import load_dotenv
import os
import discord
from discord import app_commands
from llm_utils import get_answer, get_embeddings

class GuildCheckFailure(app_commands.errors.CheckFailure):
    """Custom exception raised when a command is used in an unauthorized guild.
    
    This exception inherits from discord.py's CheckFailure and is used to handle
    guild-specific authorization failures.
    """
    pass

class RoleCheckFailure(app_commands.errors.CheckFailure):
    """Custom exception raised when a user lacks the required role for a command.
    
    This exception inherits from discord.py's CheckFailure and is used to handle
    role-based authorization failures.
    """
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
    """Decorator factory that creates a check for approved guild IDs.
    
    Returns:
        app_commands.check: A decorator that validates if the command is being used
            in an approved guild.
    
    Raises:
        GuildCheckFailure: If the command is used in an unauthorized guild.
    """
    @app_commands.check
    def is_approved_guild(interaction: discord.Interaction) -> bool:
        if interaction.guild_id not in APPROVED_GUILDS:
            raise GuildCheckFailure()
        return True
    return is_approved_guild

def authority_check():
    """Decorator factory that creates a check for required user roles.
    
    Returns:
        app_commands.check: A decorator that validates if the user has the required role
            ('admin' or 'lorekeeper').
    
    Raises:
        RoleCheckFailure: If the user lacks the required roles.
    """
    @app_commands.check
    def has_required_role(interaction: discord.Interaction) -> bool:
        member_roles = [role.name.lower() for role in interaction.user.roles]
        if not any(role in member_roles for role in ['admin', 'lorekeeper']):
            raise RoleCheckFailure()
        return True
    return has_required_role


@bot.event
async def on_ready():
    """Event handler that executes when the bot successfully connects to Discord.
    
    Attempts to sync the command tree and prints connection status messages.
    """
    print(f'{bot.user} has connected to Discord!')
    try:
        await tree.sync()
        print("Synced command tree")
    except Exception as e:
        print(e)

# @tree.command(name="hello", description="Get a friendly greeting from the bot! (And prove that it's responsive)")
# @guild_check()
# async def hello(interaction: discord.Interaction):
#     """Responds with a friendly greeting to the user.
    
#     Args:
#         interaction (discord.Interaction): The interaction object containing
#             information about the command invocation.
#     """
#     await interaction.response.send_message(f"Hello, {interaction.user.name}!")

@tree.command(name="ask", description = "Ask the bot a question")
@guild_check()
async def ask(interaction: discord.Interaction, question: str):
    """Processes a user's question and provides an AI-generated answer.
    
    Args:
        interaction (discord.Interaction): The interaction object containing
            information about the command invocation.
        question (str): The question asked by the user.
    """
    await interaction.response.defer(thinking=True)
    response = f"**Question**: {question}\n\n"
    answer = get_answer(guild=interaction.guild_id,question=question)
    response += f"**Answer**: {answer}"
    await interaction.followup.send(response)

@tree.command(name="update",description="Update the database. This may take a few minutes.")
@guild_check()
@authority_check()
async def update(interaction: discord.Interaction):
    """Updates the knowledge database with fresh embeddings.
    
    This command requires admin or lorekeeper privileges to execute.
    
    Args:
        interaction (discord.Interaction): The interaction object containing
            information about the command invocation.
    """
    await interaction.response.defer(thinking=True)
    get_embeddings(guild=interaction.guild_id,force_refresh=True)
    await interaction.followup.send("The knowledge database has been updated.")

@tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Global error handler for application commands.
    
    Args:
        interaction (discord.Interaction): The interaction object containing
            information about the command invocation.
        error (app_commands.AppCommandError): The error that was raised during
            command execution.
    """
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