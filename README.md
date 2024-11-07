# Discord Bot with Notion Database and Local Language Model Integration

This project is a Discord bot designed to pull data from a Notion database and respond to user queries through a locally hosted Large Language Model (LLM) using [Ollama](https://ollama.com/). Users can ask questions in natural language, and the bot retrieves relevant data from the Notion database, processes it through an LLM, and provides answers directly within Discord.

_NOTE - This bot was written to pull information from a [specific Notion template](https://www.notion.so/marketplace/templates/rpg-campaign-notekeeper), and may require alteration to meet your requirements. 

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Notion Integration**: Seamlessly fetch data from a specified Notion database.
- **Natural Language Processing**: Use a locally hosted LLM via Ollama to interpret and answer user questions.
- **Discord Integration**: Communicate with users through Discord, making data retrieval and querying accessible.
- **Embeddings**: Enhanced query relevance with custom embeddings, supporting better response accuracy.

## Requirements
- **Python 3.8+**
- **Ollama**: Locally hosted LLM framework ([Ollama installation guide](https://ollama.com/docs/getting-started))
- **Discord Bot Token**: [Setup a bot on Discord Developer Portal](https://discord.com/developers/applications)
- **Notion API Key**: [Create an integration in Notion](https://www.notion.so/my-integrations)
- **Python Dependencies**: Listed in `pyproject.toml`

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   Use the package manager of your choice or follow these examples with `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Set up necessary environment variables in a `.env` file in the root of your project:

   ```
   DISCORD_NOTEKEEPER_KEY=<Your Discord Bot Token>
   NOTION_API_KEY=<Your Notion API Key>
   ```

4. **Update your Discord server ID and your Notion Database IDs**
    This information is kept in the `GUILD_DATABASES` dictionary in `data_fetch/llm_utils.py`. Note that this can support multiple servers and databases.

    ### Finding Your Notion Database ID
    To get your Notion database ID:
    1. Open your Notion database in a web browser
    2. Click "Share" in the top right corner
    3. Copy the share link
    4. The database ID is the string of characters between the last `/` and `?` in the URL
    
    Example URL:
    ```
    https://www.notion.so/workspace/8a111111bbbb2222cccc3333dddd4444?v=...
                                    └─────────── Database ID ────-──┘
    ```

    ### Finding Your Discord Server ID
    To get your Discord server (Guild) ID:
    1. Open Discord Settings → App Settings → Advanced
    2. Enable "Developer Mode"
    3. Right-click on your server name
    4. Click "Copy Server ID"

5. **Run the Bot**
   ```bash
   python main.py
   ```

## Configuration

### Notion Integration
The bot relies on a Notion integration to retrieve data. Follow these steps to set up your integration:

1. Go to [Notion Integrations Page](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Name your integration (e.g., "Discord Bot")
4. Select the workspace where your database is located
5. Configure the capabilities (required permissions):
   - Read content
   - Read user information
   - Read comments
6. Click "Submit" to create the integration
7. Copy the "Internal Integration Token" - this will be your `NOTION_API_KEY`
8. Go to your Notion database page
9. Click the "..." menu in the top right
10. Select "Add connections" and choose your new integration

After setup, configure the `NOTION_API_KEY` environment variable with your integration token.

> ⚠️ **Important**: Keep your Notion token secret! Never share it or commit it to version control.

### Discord Bot Setup
To create and configure your Discord bot:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Add Bot"
5. Under the bot's username, click "Reset Token" and copy the new token - this will be your `DISCORD_NOTEKEEPER_KEY`
6. Enable these options under "Privileged Gateway Intents":
   - Message Content Intent
   - Server Members Intent
   - Presence Intent
7. Go to "OAuth2" → "URL Generator" in the left sidebar
8. Select these scopes:
   - `bot`
   - `applications.commands`
9. Select these bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Use Slash Commands
10. Copy the generated URL at the bottom and use it to invite the bot to your server

After setup, configure the `DISCORD_NOTEKEEPER_KEY` environment variable with your bot token.

> ⚠️ **Important**: Keep your bot token secret! Never share it or commit it to version control.


### Ollama LLM
Ollama is required to host the local LLM. Follow these steps to set up:

1. Install Ollama for your platform from [ollama.ai](https://ollama.ai)

2. Download the required models by running these commands in your terminal:
```bash
ollama pull llama3.1
ollama pull all-minilm:l6-v2
```
`all-minilm:l6-v2` is used as part of the RAG pipeline, creating data embeddings and retrieving data from the embedding cache. This model is extremely small and should run on almost any hardware. 
`llama3.1` is used to process the retrieved data and generate an answer. This model is a little larger - if you run into issues running it, feel free to substitute for a smaller model (or a larger one, if you have the compute resources). Simply update the value of `answer_model` in `llm_utils/embeddings.py`


### Embeddings
The `embeddings.py` module handles text embeddings to support improved query handling. Fine-tuning embeddings may be necessary for specialized use cases or large databases.

## Usage
After setting up and running the bot:
- **Add Bot to Discord Server**: Invite your bot to your Discord server using the OAuth2 URL generated in the Discord Developer Portal.
- **Ask Questions in Discord**: Users can interact with the bot using Discord Slash commands. For example:
  ```
  /ask Can you summarize the latest data on <topic>?
  ```

The first time a question is asked it may take slightly longer as the bot fetches the data, creates embeddings, and caches them locally. If there is new data and you wish to update this cache:
```
/update
```
will force an update. Note that you need to have either the Admin or Lorekeeper Discord rules to use this command.

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Ensure that your code adheres to the project’s code style and that you’ve tested your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
