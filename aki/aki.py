"""
MIT License

Copyright (c) 2020-2021 phenom4n4n

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging

import akinator
import discord
from akinator.async_aki import Akinator
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

from .menus import channel_is_nsfw, get_menu

log = logging.getLogger("red.phenom4n4n.aki")


class Aki(commands.Cog):
    """
    Joue a Akinator sur Discord !
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=8237578807127857,
            force_registration=True,
        )

    __version__ = "1.1.0"

    def format_help_for_context(self, ctx):
        pre_processed = super().format_help_for_context(ctx)
        n = "\n" if "\n\n" not in pre_processed else ""
        return f"{pre_processed}{n}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(self, *, requester: str, user_id: int) -> None:
        return

    @commands.max_concurrency(1, commands.BucketType.channel)
    @commands.bot_has_permissions(embed_links=True, add_reactions=True)
    @commands.command(aliases=["akinator"])
    async def aki(
        self, ctx: commands.Context, language: str.lower = "fr", use_buttons: bool = True
    ):
        """
        Demarre une partie d'Akinator!

        Controls:
        > ✅ : oui
        > ❎ : non
        > ❔ : je ne sais pas
        > 📉 : probablement
        > 📈 : probablement pas
        > 🔙 : retour
        > 🏆 : gagné !
        > 🗑️ : stopper
        """
        await ctx.trigger_typing()
        aki = Akinator()
        child_mode = not channel_is_nsfw(ctx.channel)
        try:
            await aki.start_game(language=language.replace(" ", "_"), child_mode=child_mode)
        except akinator.InvalidLanguageError:
            await ctx.send(
                "Langue invalide .\n<https://github.com/NinjaSnail1080/akinator.py#functions>"
            )
        except Exception:
            await ctx.send("Erreur de connection avec les serveurs Akinator.")
        else:
            aki_color = discord.Color(0xE8BC90)
            menu = get_menu(buttons=use_buttons)
            await menu(aki, aki_color).start(ctx)
