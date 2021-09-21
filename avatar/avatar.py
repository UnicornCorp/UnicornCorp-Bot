# Simple avatar URL fetch by Yukirin#0048

# Discord
import discord

# Red
from redbot.core import commands

# Libs


BaseCog = getattr(commands, "Cog", object)


class Avatar(BaseCog):
    """Récupère l'URL d'une PP."""

    @commands.command()
    async def pp(self, ctx, *, user: discord.Member=None):
        """Affiche la PP.
        """
        author = ctx.author

        if not user:
            user = author

        if user.is_avatar_animated():
            url = user.avatar_url_as(format="gif")
        if not user.is_avatar_animated():
            url = user.avatar_url_as(static_format="png")

        await ctx.send("Profil de {} : {}".format(user.name, url))
