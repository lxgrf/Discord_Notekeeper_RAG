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
The bot relies on a Notion integration to retrieve data. Configure the `NOTION_API_KEY` and `DISCORD_NOTEKEEPER_KEY` environment variables to enable data access.

### Ollama LLM
Ollama is required to host the local LLM. Ensure Ollama is installed and configured locally. No additional configuration within this project should be necessary for Ollama beyond installation.

### Embeddings
The `embeddings.py` module handles text embeddings to support improved query handling. Fine-tuning embeddings may be necessary for specialized use cases or large databases.

## Usage
After setting up and running the bot:
- **Add Bot to Discord Server**: Invite your bot to your Discord server using the OAuth2 URL generated in the Discord Developer Portal.
- **Ask Questions in Discord**: Users can interact with the bot by mentioning it or using a command prefix. Example:
  ```
  @BotName Can you summarize the latest data on <topic>?
  ```

The bot will respond by querying the Notion database and processing the response with the locally hosted LLM to generate a natural language answer.

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Ensure that your code adheres to the project’s code style and that you’ve tested your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
