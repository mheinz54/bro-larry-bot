# bro-larry

A Discord bot that shares daily devotionals inspired by Brother Lawrence's "The Practice of the Presence of God". The bot automatically posts devotionals and provides commands for users to access devotional content, practice mindfulness, and manage distractions.

## Features

- **Daily Devotionals**: Automatically posts a devotional each day at 9 AM
- **Manual Devotional**: Get today's devotional on demand
- **Random Devotional**: Access any devotional from the collection randomly
- **Heart Practice**: Mindfulness and presence exercises
- **Distraction Management**: Tools to help refocus on spiritual practice
- **Rich Embeds**: Beautiful Discord embeds with scripture, quotes, and reflections
- **Seasonal Themes**: Devotionals organized by liturgical seasons and spiritual themes

## Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `!devotional` | - | Get today's devotional |
| `!randomdevotional` | `!random_devotional`, `!rd` | Get a random devotional from the collection |
| `!heart` | - | Practice presence and mindfulness exercises |
| `!distraction` | - | Get help managing distractions and refocusing |

## Getting Started

### Prerequisites

- Python 3.8 or higher (for local installation)
- Docker and Docker Compose (for containerized deployment)
- Discord Bot Token
- A Discord server where you have permission to add bots

### Installation Options

Choose one of the following installation methods:

#### Option 1: Local Python Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bro-larry.git
   cd bro-larry
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env-dist .env
   ```
   
   Then edit `.env` and replace the values with your actual configuration:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   Devotion_Channel=your_channel_id_here
   ```

4. **Prepare devotional data**
   - Ensure `resource/devotional_prompts.json` contains your devotional content

5. **Run the bot**
   ```bash
   python bot.py
   ```

#### Option 2: Docker Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bro-larry.git
   cd bro-larry
   ```

2. **Set up environment variables**
   ```bash
   cp .env-dist .env
   ```
   
   Then edit `.env` with your configuration:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   Devotion_Channel=your_channel_id_here
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

   Or build and run manually:
   ```bash
   # Build the image
   docker build -t bro-larry .
   
   # Run the container
   docker run -d --name bro-larry --env-file .env bro-larry
   ```

4. **View logs**
   ```bash
   # With docker-compose
   docker-compose logs -f
   
   # With docker run
   docker logs -f bro-larry
   ```

5. **Stop the bot**
   ```bash
   # With docker-compose
   docker-compose down
   
   # With docker run
   docker stop bro-larry
   docker rm bro-larry
   ```

### Discord Bot Setup

1. **Create a Discord Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" section and click "Add Bot"
   - Copy the bot token for your `.env` file

2. **Set Bot Permissions**
   - In the "Bot" section, enable the following permissions:
     - Send Messages
     - Use Slash Commands
     - Embed Links
     - Read Message History

3. **Invite Bot to Server**
   - Go to the "OAuth2" > "URL Generator" section
   - Select "bot" scope
   - Select the permissions mentioned above
   - Use the generated URL to invite the bot to your server

4. **Get Channel ID**
   - Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
   - Right-click on the channel where you want devotionals posted
   - Click "Copy ID" and use this in your `.env` file

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_TOKEN` | Your Discord bot token | Yes |
| `Devotion_Channel` | Channel ID where daily devotionals will be posted | Yes |

### Devotional Data Format

The bot expects devotional data in `resource/devotional_prompts.json` with the following structure:

```json
{
  "day": 1,
  "season": "Advent",
  "theme": "Waiting in Hope",
  "scripture": "Isaiah 40:31 - 'But those who hope in the Lord will renew their strength...'",
  "quote": "We must not be surprised at our faults; we must only be sorry for them.",
  "reflection": "Today, let us practice being present with God in all our activities..."
}
```

## Project Structure

```
bro-larry/
├── cogs/
│   ├── daily_devotional.py    # Main devotional functionality
│   ├── heart.py               # Heart practice and mindfulness commands
│   └── distraction.py         # Distraction management commands
├── resource/
│   └── devotional_prompts.json # Devotional content data
├── bot.py                      # Bot entry point
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose configuration
├── .env-dist                   # Environment template
├── .env                        # Your environment variables (not in git)
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── LICENSE                     # License file
└── README.md                   # This file
```

## Docker Configuration

### Dockerfile

The included `Dockerfile` creates a lightweight container based on Python Alpine:

```dockerfile
FROM python:3.9-slim

ARG VERSION
ENV VERSION=$VERSION

WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt

COPY ./src/bot .

CMD ["python", "bot.py"]

LABEL \
        org.opencontainers.image.title="bro-larry-bot"
```

### Docker Compose

The `docker-compose.yml` file provides an easy way to manage the bot:

```yaml
version: '3.8'

services:
  bot:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        VERSION: 1.0.0
    container_name: brolarry
    env_file:
      - .env

networks:
  default:
    driver: bridge
```

### Docker Management Commands

```bash
# Start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Restart the bot
docker-compose restart

# Stop the bot
docker-compose down

# Rebuild and restart (after code changes)
docker-compose up -d --build

# View container status
docker-compose ps
```

## Usage Examples

### Daily Automatic Posting
The bot will automatically post the devotional for the current day at 9 AM in the configured channel.

### Manual Commands

**Devotional Commands:**
```
!devotional
```
Posts today's devotional immediately.

```
!randomdevotional
```
or
```
!rd
```
Posts a random devotional from the collection.

**Spiritual Practice Commands:**
```
!heart
```
Provides mindfulness and presence exercises inspired by Brother Lawrence's teachings.

```
!distraction
```
Offers guidance and techniques for managing distractions and returning focus to spiritual practice.

## Deployment

### Production Deployment with Docker

For production deployment, consider these additional steps:

1. **Use Docker secrets or external secret management**
   ```bash
   # Example with Docker secrets
   echo "your_discord_token" | docker secret create discord_token -
   ```

2. **Set up proper logging**
   ```yaml
   # In docker-compose.yml
   services:
     bro-larry:
       logging:
         driver: "json-file"
         options:
           max-size: "10m"
           max-file: "3"
   ```

3. **Configure health checks**
   ```dockerfile
   # Add to Dockerfile
   HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
     CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1
   ```

4. **Use a reverse proxy** (if exposing web endpoints)
   ```yaml
   # Example with nginx
   services:
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
   ```

## Customization

### Changing Post Time
Edit the `before_daily_devotional` method in `cogs/daily_devotional.py` to change the posting time:

```python
next_run = now.replace(hour=9, minute=0, second=0, microsecond=0)  # Change hour here
```

### Adding More Commands
Create new command methods in the respective cog classes using the `@commands.command()` decorator.

### Customizing Embeds
Modify the embed creation methods in each cog to change the appearance of the bot's responses.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Brother Lawrence's "The Practice of the Presence of God"
- Built with [discord.py](https://discordpy.readthedocs.io/)
- Thanks to the Discord.py community for excellent documentation and support

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/bro-larry/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your setup and the error you're experiencing

## Troubleshooting

### Common Issues

**Bot doesn't respond to commands**
- Ensure the bot has "Send Messages" permission in the channel
- Check that your command prefix is correct (default is `!`)
- Verify the bot is online and connected

**Daily devotional not posting**
- Check that `Devotion_Channel` ID is correct
- Ensure the bot has permissions in that channel
- Verify the devotional data file is properly formatted

**"No devotional found" error**
- Check that `devotional_prompts.json` exists in the `resource/` directory
- Verify the JSON format matches the expected structure
- Ensure there's a devotional entry for the current day of year

**Commands not working**
- Verify all cog files are present in the `cogs/` directory
- Check that the main bot file is loading all cogs properly
- Ensure there are no syntax errors in the cog files

### Docker-Specific Issues

**Container won't start**
- Check Docker logs: `docker-compose logs`
- Verify `.env` file exists and has correct values
- Ensure Docker has permission to read the project directory

**Bot can't read devotional file**
- Verify the `resource/` directory is properly mounted
- Check file permissions on the host system
- Ensure the JSON file is valid

**Container keeps restarting**
- Check for Python errors in logs
- Verify all required environment variables are set
- Ensure the Discord token is valid and has proper permissions

**Time zone issues**
- Set the `TZ` environment variable in docker-compose.yml
- Example: `TZ=America/New_York` or `TZ=UTC`