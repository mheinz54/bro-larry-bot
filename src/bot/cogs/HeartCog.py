import discord
from discord.ext import commands, tasks
from datetime import datetime, time
from HeartSanctifier import HeartSanctifier


class HeartSanctifierCog(commands.Cog, name="Heart"):
    def __init__(self, bot):
        self.bot = bot

        # Define reset times (6 AM, 12 PM, 6 PM)
        self.reset_times = [time(6, 0), time(12, 0), time(18, 0)]

        # Start the reset task
        self.heart_reset_task.start()

    def get_user_heart(self, user_id: int) -> HeartSanctifier:
        """Get or create a HeartSanctifier instance for a user"""
        if user_id not in self.bot.user_hearts:
            self.bot.user_hearts[user_id] = HeartSanctifier()
        return self.bot.user_hearts[user_id]

    def should_reset_heart(self, heart: HeartSanctifier) -> bool:
        """Check if a heart should be reset based on the current time"""
        now = datetime.now()
        current_time = now.time()

        if heart.last_reset is None:
            return True

        last_reset_date = heart.last_reset.date()
        today = now.date()

        if today > last_reset_date:
            return True

        last_reset_time = heart.last_reset.time()

        for reset_time in self.reset_times:
            if current_time >= reset_time and last_reset_time < reset_time:
                return True

        return False

    @tasks.loop(minutes=30)
    async def heart_reset_task(self):
        """Reset hearts at designated times"""
        for user_id, heart in self.bot.user_hearts.items():
            if self.should_reset_heart(heart):
                heart.reset_heart()

    @heart_reset_task.before_loop
    async def before_heart_reset_task(self):
        await self.bot.wait_until_ready()

    @commands.group(name="heart", description="Spiritual heart sanctification commands", invoke_without_command=True)
    async def heart_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Use `!heart help` to see available heart commands.")

    @heart_group.command(name="empty", description="Empty your heart of distractions")
    async def empty_heart(self, ctx):
        heart = self.get_user_heart(ctx.author.id)
        message = f"**Empty Heart**\n{heart.empty_heart()}"
        await ctx.send(message)

    @heart_group.command(name="invite", description="Invite God into your heart")
    async def invite_god(self, ctx):
        heart = self.get_user_heart(ctx.author.id)
        message = f"**Invite God**\n{heart.invite_god()}"
        await ctx.send(message)

    @heart_group.command(name="allow", description="Allow God to move freely in your soul")
    async def allow_god_to_act(self, ctx):
        heart = self.get_user_heart(ctx.author.id)
        message = f"**Allow God To Act**\n{heart.allow_god_to_act()}"
        await ctx.send(message)

    @heart_group.command(
        name="surrender", description="Complete surrender - empty heart, invite God, and allow divine action"
    )
    async def surrender(self, ctx):
        heart = self.get_user_heart(ctx.author.id)
        message = f"**Surrender**\n{heart.surrender()}"
        await ctx.send(message)

    @heart_group.command(name="status", description="Check the current state of your heart")
    async def heart_status(self, ctx):
        heart = self.get_user_heart(ctx.author.id)

        # Determine heart state
        if heart.presence_of_god and not heart.heart:
            status = "🕊️ **Sanctified** - God dwells within"
            description = "Your heart is pure and filled with divine presence."
        elif not heart.heart and not heart.presence_of_god:
            status = "🧹 **Empty but Waiting** - Ready for invitation"
            description = "Your heart is empty and ready to invite God."
        elif heart.heart and not heart.presence_of_god:
            status = "⚠️ **Distracted** - Needs cleansing"
            description = "Your heart contains distractions that need to be cleared."
        else:
            status = "🔄 **In Transition**"
            description = "Your heart is in a state of spiritual transition."

        heart_empty = "✅" if not heart.heart else "❌"
        gods_presence = "✅" if heart.presence_of_god else "❌"

        message = f"**💖 Heart Status**\n{status}\n\n{description}\n\n**Current State:**\nHeart Empty: {heart_empty}\nGod's Presence: {gods_presence}"

        await ctx.send(message)

    @heart_group.command(name="help", description="Learn about the spiritual heart commands")
    async def help_heart(self, ctx):
        embed = discord.Embed(
            title="💖 Heart Sanctification Guide",
            description="Welcome to your spiritual heart journey. Here are the available heart commands:",
            color=0xFFD700,
        )

        embed.add_field(
            name="🧹 `!heart empty`", value="Clear your heart of all distractions and worldly concerns.", inline=False
        )

        embed.add_field(
            name="🕊️ `!heart invite`", value="Invite God into your prepared heart (requires empty heart).", inline=False
        )

        embed.add_field(
            name="✨ `!heart allow`",
            value="Allow God to move freely within your soul (requires God's presence).",
            inline=False,
        )

        embed.add_field(
            name="🙏 `!heart surrender`", value="Complete surrender - performs all steps in sequence.", inline=False
        )

        embed.add_field(
            name="💖 `!heart status`", value="Check the current spiritual state of your heart.", inline=False
        )

        embed.set_footer(text="Each user has their own spiritual journey • May you find peace 🕊️")

        await ctx.send(embed=embed)

    async def cog_unload(self):
        """Clean up when the cog is unloaded"""
        self.heart_reset_task.cancel()


async def setup(bot) -> None:
    await bot.add_cog(HeartSanctifierCog(bot))
