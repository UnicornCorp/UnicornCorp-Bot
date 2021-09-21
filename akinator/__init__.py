from .akinatorcog import AkinatorCog


def setup(bot):
    cog = AkinatorCog(bot)
    bot.add_cog(cog)
