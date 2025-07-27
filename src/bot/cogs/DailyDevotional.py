import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime
import logging


class DailyDevotional(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.devotional_data = []
        self.channel_id = os.getenv("Devotion_Channel")
        self.load_devotional_data()

    def load_devotional_data(self):
        """Load devotional prompts from JSON file"""
        try:
            # Get the path to the resources directory
            resources_path = os.path.join(os.path.dirname(__file__), "..", "resource", "devotional_prompts.json")

            with open(resources_path, "r", encoding="utf-8") as file:
                self.devotional_data = json.load(file)

            logging.info(f"Loaded {len(self.devotional_data)} devotional prompts")

        except FileNotFoundError:
            logging.error("devotional_prompts.json not found in resources directory")
            self.devotional_data = []
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing devotional_prompts.json: {e}")
            self.devotional_data = []
        except Exception as e:
            logging.error(f"Unexpected error loading devotional data: {e}")
            self.devotional_data = []

    def get_todays_devotional(self):
        """Get the devotional for the current day of the year"""
        current_day = datetime.now().timetuple().tm_yday  # Day of year (1-366)

        # Find the devotional for today
        for devotional in self.devotional_data:
            if devotional.get("day") == current_day:
                return devotional

        # If no exact match found, return None
        return None

    def get_random_devotional(self):
        """Get a random devotional from the available data"""
        if not self.devotional_data:
            return None

        return random.choice(self.devotional_data)

    def create_devotional_embed(self, devotional):
        """Create a Discord embed for the devotional"""
        embed = discord.Embed(
            title=f"Daily Devotional - Day {devotional['day']}",
            color=0x7289DA,  # Discord blurple
            timestamp=datetime.now(),
        )

        # Add season and theme
        if devotional.get("season"):
            embed.add_field(name="Season", value=devotional["season"], inline=True)

        if devotional.get("theme"):
            embed.add_field(name="Theme", value=devotional["theme"], inline=True)

        # Add a spacer field for better formatting
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        # Add scripture
        if devotional.get("scripture"):
            embed.add_field(name="📖 Scripture", value=devotional["scripture"], inline=False)

        # Add quote
        if devotional.get("quote"):
            embed.add_field(name="✒️ Brother Lawrence", value=f'*"{devotional["quote"]}"*', inline=False)

        # Add reflection
        if devotional.get("reflection"):
            embed.add_field(name="💡 Reflection", value=devotional["reflection"], inline=False)

        return embed

    @tasks.loop(hours=24)
    async def daily_devotional_task(self):
        """Task that runs once per day to post the devotional"""
        if not self.channel_id:
            logging.warning("Channel ID not set for daily devotional")
            return

        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            logging.error(f"Could not find channel with ID {self.channel_id}")
            return

        devotional = self.get_todays_devotional()
        if not devotional:
            logging.warning(f"No devotional found for day {datetime.now().timetuple().tm_yday}")
            return

        try:
            embed = self.create_devotional_embed(devotional)
            await channel.send(embed=embed)
            logging.info(f"Posted daily devotional for day {devotional['day']}")

        except discord.Forbidden:
            logging.error("Bot doesn't have permission to send messages in the channel")
        except discord.HTTPException as e:
            logging.error(f"Failed to send devotional message: {e}")
        except Exception as e:
            logging.error(f"Unexpected error posting devotional: {e}")

    @daily_devotional_task.before_loop
    async def before_daily_devotional(self):
        """Wait until the bot is ready before starting the task"""
        await self.bot.wait_until_ready()

        # Calculate time until next 9 AM (or your preferred time)
        now = datetime.now()
        next_run = now.replace(hour=9, minute=0, second=0, microsecond=0)

        # If it's already past 9 AM today, schedule for tomorrow
        if now.hour >= 9:
            next_run = next_run.replace(day=next_run.day + 1)

        # Wait until the scheduled time
        wait_seconds = (next_run - now).total_seconds()
        if wait_seconds > 0:
            logging.info(f"Daily devotional will start in {wait_seconds / 3600:.1f} hours")
            await discord.utils.sleep_until(next_run)

    @commands.command(name="devotional")
    async def manual_devotional(self, ctx):
        """Manually post today's devotional"""
        devotional = self.get_todays_devotional()
        if not devotional:
            await ctx.send(f"No devotional found for day {datetime.now().timetuple().tm_yday}")
            return

        embed = self.create_devotional_embed(devotional)
        await ctx.send(embed=embed)

    @commands.command(name="randomdevotional", aliases=["random_devotional", "rd"])
    async def random_devotional(self, ctx):
        """Get a random devotional from the collection"""
        if not self.devotional_data:
            await ctx.send("❌ No devotional data available. Please check if the devotional file is loaded properly.")
            return

        devotional = self.get_random_devotional()
        if not devotional:
            await ctx.send("❌ Unable to retrieve a random devotional.")
            return

        embed = self.create_devotional_embed(devotional)
        await ctx.send(embed=embed)

    def cog_unload(self):
        """Clean up when the cog is unloaded"""
        self.daily_devotional_task.cancel()


async def setup(bot):
    await bot.add_cog(DailyDevotional(bot))
