from discord.ext import commands
from HeartSanctifier import HeartSanctifier


class DistractionCog(commands.Cog, name="Distractions"):
    def __init__(self, bot):
        self.bot = bot

    def get_user_heart(self, user_id: int) -> HeartSanctifier:
        """Get or create a HeartSanctifier instance for a user"""
        if user_id not in self.bot.user_hearts:
            self.bot.user_hearts[user_id] = HeartSanctifier()
        return self.bot.user_hearts[user_id]

    @commands.group(
        name="distraction", aliases=["d"], description="Manage your distraction log", invoke_without_command=True
    )
    async def distraction_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Use `!d help` to see available distraction commands.")

    @distraction_group.command(name="add", aliases=["log"], description="Add a distraction to your log")
    async def add_distraction(self, ctx, *, distraction: str):
        """Add a distraction to the user's log"""
        if not distraction.strip():
            await ctx.send("❌ Please provide a distraction to log.")
            return

        heart = self.get_user_heart(ctx.author.id)
        heart.heart.insert(0, distraction.strip())
        await ctx.send(f"📝 Logging distraction: '{distraction.strip()}'")

    @distraction_group.command(name="clear", aliases=["release"], description="Release all distractions")
    async def clear_all_distractions(self, ctx):
        """Clear all distractions for the user"""
        heart = self.get_user_heart(ctx.author.id)
        heart.heart = []
        await ctx.send("💨 Releasing distractions...")

    @distraction_group.command(name="help", description="Learn about distraction commands")
    async def help_distractions(self, ctx):
        """Show help for distraction commands"""
        message = """**📝 Distraction Management Guide**
Track the things that distract you from spiritual focus:

📝 `!distraction add <text>` - Log a new distraction (aliases: `!d add`, `!d log`)

💨 `!distraction clear` - Release all distractions (aliases: `!d clear`, `!d release`)

💡 **Examples:**
`!d add worried about work meeting`
`!d add phone notifications`
`!d clear`

*Track distractions to become more aware of what pulls you away from peace 🕊️*"""
        await ctx.send(message)


async def setup(bot) -> None:
    await bot.add_cog(DistractionCog(bot))
