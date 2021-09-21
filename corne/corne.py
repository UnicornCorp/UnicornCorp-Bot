import discord
import random
from redbot.core import commands
from redbot.core.utils.chat_formatting import pagify


class corne(commands.Cog):
    """Commande corne."""

    @commands.command()
    async def corne(self, ctx, *users: discord.Member):
        """Toi aussi vois la taille de ta corne !
        Compare ta belle corne avec les autres.
        Qui aura la plus longue ?"""
        if not users:
            await ctx.send_help()
            return

        dongs = {}
        msg = ""
        state = random.getstate()

        for user in users:
            random.seed(str(user.id))

            if ctx.bot.user.id == user.id:
                length = 50

            elif 220506606218117122 == user.id:
                length = 1900

            elif 277811453010903060 == user.id:
                length = 90

            else:
                length = random.randint(0, 45)

            dongs[user] = "///{}=--".format("=" * length)

        random.setstate(state)
        dongs = sorted(dongs.items(), key=lambda x: x[1])

        for user, dong in dongs:
            msg += "**Regardez la belle corne de {}:**\n{}\n".format(user.display_name, dong)

        for page in pagify(msg):
            await ctx.send(page)