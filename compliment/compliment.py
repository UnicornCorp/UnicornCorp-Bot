from random import choice
from typing import List

import discord
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Compliment", __file__)

compliments: List[str] = [
    _("Ton sourire est magnifique."),
    _("Tu es génial(e) !"),
    _("Tu es comme un cookie."),
    _("J'aime ton style."),
    _("Tu as le meilleur rire."),
    _("Je t'aime bien."),
    _("Tu es parfait(e)."),
    _("Tu es adorable."),
    _("Tu es fort(e) !"),
    _("Te voir fait du bien."),
    _("Tu es un(e) superbe ami(e)."),
    _("Tu remplis de lumière nos esprits."),
    _("Tu mérites des calins."),
    _("Sois fier(e) de toi."),
    _("Tu es plus important que tu ne le pense."),
    _("Tu as un superbe sens de l'humour."),
    _("Tu fais toujours les bon choix"),
    _("Ta photo est à coté de 'sublime' dans le dictionnaire?"),
    _("Tu es la plus belle rencontre que l'on puisse faire."),
    _("Tu es comme un gros paquet de chips."),
    _("Si on te note entre 1 et 10, tu as 20."),
    _("Tu es brave."),
    _("Tu brilles plus que Beyonce dans un océan de paillettes."),
    _("J'aime toutes tes blagues, surtout celles en carton."),
    _("Tu es plus cool qu'un chaton déguisé en licorne."),
    _("Ta gentillesse me réconforte."),
    _("Plus je te connais, plus je t’apprécie."),
    _("Tu es aussi beau (belle) à l’intérieur qu’à l’extérieur."),
    _("Merci d’être toi !"),
    _("Avec toi, on ne s’ennuie jamais."),
    _("J’aime tellement ton humour."),
    _("Je t’admire pour ton intelligence, ton courage, ta générosité, ton honnêteté, ta force de caractère, ta patience, ton talent…"),
    _("Merci d’exister."),
    _("Tu fais voir le monde comme personne ne l’a jamais fait voir."),
    _("Ton énergie est communicative."),
    _("Il y a de la douceur dans tes yeux."),
    _("Ton rire est mon bruit préféré."),
    _("Le monde serait tellement ennuyeux sans toi."),

    _("Est-ce que tu es réel ?"),
    _("Tu rends importantes les petites choses."),
    _("Tu m’impressionnes chaque jour."),
    _("Ta gentillesse n’a pas de limite."),
    _("J’aimerais être au moins la moitié de l’être humain que tu es. (Oui je suis un bot je sais)"),
    _(
        "Il n’y a personne comme toi."
    ),
    _("Ton âme est magnifique."),
    _("You're wonderful."),
    _(
        "Tu es plus un superhéros que n’importe quel personnage de Marvel."
    ),
    _("Tu m’inspires."),
    _("Tu as si bon coeur."),
    _("Tu es vraiment inoubliable."),
    _("N’arrête jamais d’être toi, s’il te plaît."),
    _("J’ai foi en la bonté, grâce à toi."),
    _(
        "Tu as un esprit tellement généreux."
    ),
    _("Ton coeur doit faire dix fois la taille normale."),
    _("Comment as-tu appris à être si bon ?"),
]


@cog_i18n(_)
class Compliment(commands.Cog):
    """Fais un compliment parce que les insultes c'est trop facile"""

    __author__ = ["Airen", "JennJenn", "TrustyJAID", "Francais par UnicornCorp"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        Thanks Sinbad!
        """
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Rien à delete
        """
        return

    @commands.command()
    async def compliment(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """
        Complimente un utilisateur

        `user` l'utilisateur a qui tu veux faire un compliment
        """
        msg = " "
        if user:
            if user.id == self.bot.user.id:
                user = ctx.message.author
                bot_msg: List[str] = [
                    _("Hey, j'aime le compliment ! :smile:"),
                    _("Non ***TU ES*** génial ! :smile:"),
                ]
                await ctx.send(f"{ctx.author.mention} {choice(bot_msg)}")

            else:
                await ctx.send(user.mention + msg + choice(compliments))
        else:
            await ctx.send(ctx.message.author.mention + msg + choice(compliments))
