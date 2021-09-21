import asyncio
from json import JSONDecodeError

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.predicates import MessagePredicate
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.embed import randomize_colour

from akinator.async_aki import Akinator
from akinator import CantGoBackAnyFurther, InvalidLanguageError, AkiNoQuestions

import discord

__author__ = ["Predeactor , trad francaise par UnicornCorp"]
__version__ = "Beta v0.6.3 -- FR v0.1"


class AkinatorCog(commands.Cog, name="Akinator"):
    """
    Tu veux défier Akinator ? Vraiment ?!
    """

    def __init__(self, bot: Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.ongoing_games = {}

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """
        ([p]help Akinator)
        """
        pre_processed = super().format_help_for_context(ctx)
        return "{pre_processed}\n\nAuthor: {authors}\nVersion: {version}".format(
            pre_processed=pre_processed,
            authors=humanize_list(__author__),
            version=__version__,
        )

    @commands.group(aliases=["aki"])
    async def akinator(self, ctx: commands.GuildContext):
        """
        Repond a mes question !
        """

    @akinator.command()
    async def start(self, ctx: commands.Context):
        """
        C'est partie avec Akanator.

        Pour répondre tape :
        - "yes" ou "y" pour "OUI".
        - "no" ou "n" pour "NON".
        - "i" ou "idk" pour "je ne sais pas".
        - "p" pour "Peut-etre".
        - "pn" pour "Probablement non".

        Tu peux aussi faire "b" pour revenir en arriere.
        """

        await ctx.send_help()
        await ctx.send("Tu es pret a repondre ? (y/n)")
        check = MessagePredicate.yes_or_no(ctx=ctx)
        await self.bot.wait_for("message", timeout=60, check=check)
        if not check.result:
            await ctx.send("A bientot ! \N{WAVING HAND SIGN}")
            return
        await ctx.send("Let's go!")
        game_class = UserGame(ctx.author, ctx.channel, self.bot)
        self.ongoing_games[ctx.author.id] = game_class
        await ctx.send(
            "Tu peux changer le theme en tapant maintenant : "
            "fr_animals ou fr_object "
            "sinon dis no"
        )
        try:
            res = await self.bot.wait_for(
                "message", timeout=60, check=MessagePredicate.same_context(ctx=ctx)
            )
        except asyncio.TimeoutError:
            await ctx.send("Tu as disparu... \N{PENSIVE FACE}")
            return
        res = res.content.lower()
        lang = res if res not in ("no", "n") else "fr"
        await game_class.start_akinator_game(language=lang)
        try:
            del self.ongoing_games[ctx.author.id]
        except KeyError:
            pass

    @akinator.command()
    async def cancel(self, ctx: commands.Context):
        """Cancel your game with Akinator."""
        if ctx.author.id not in self.ongoing_games:
            await ctx.send("Tu n'es pas en game!")
            return
        game_class: UserGame = self.ongoing_games[ctx.author.id]
        game_class.task.cancel()
        self.ongoing_games.pop(ctx.author.id)
        await ctx.tick()


class UserGame:
    def __init__(self, user: discord.User, channel: discord.TextChannel, bot: Red):
        self.user = user
        self.channel = channel
        self.bot = bot
        self.akinator = Akinator()
        self.task = None
        self.question = None
        self.prog = 80
        self.count = 1

    async def ask_question(self):
        await self.channel.send("Question #{num}: ".format(num=self.count) + str(self.question))
        received = await self.wait_for_input()
        return received

    async def wait_for_input(self):
        valid_answer = False
        done = None  # Linters are lovely
        answer = [
            "yes",
            "y",
            "no",
            "n",
            "i",
            "idk",
            "i don't know",
            "i dont know",
            "probably",
            "p",
            "probably not",
            "pn",
            "0",
            "1",
            "2",
            "3",
            "4",
            "b",
        ]
        while valid_answer is not True:
            self.task = asyncio.create_task(
                self.bot.wait_for(
                    "message",
                    check=MessagePredicate.lower_contained_in(
                        collection=answer, user=self.user, channel=self.channel
                    ),
                    timeout=60,
                )
            )
            try:
                done = await self.task
            except (asyncio.TimeoutError, asyncio.CancelledError):
                return None
            valid_answer = True
        return done.content

    async def start_akinator_game(self, language: str):
        if not self.question:
            try:
                self.question = await self.akinator.start_game(
                    language=language, child_mode=True if self.channel.nsfw else False
                )
            except InvalidLanguageError:
                await self.channel.send("Réponse invalide.")
                return None

        answer = await self.answer_questions()

        if answer:
            await self.determine_win()

    async def answer_questions(self):
        """A while loop."""
        user_prompt = None
        while self.akinator.progression <= self.prog:
            user_prompt = await self.ask_question()
            if not user_prompt:
                await self.channel.send("Fin de la partie.")
                return False

            if user_prompt in ("b", "back"):
                await self.go_back()
                continue

            try:
                self.question = await self.akinator.answer(user_prompt)
                self.count += 1
            except JSONDecodeError:
                await self.channel.send("C'est cassé, appel Yohann.")
            except AkiNoQuestions:
                return True
        return True

    async def go_back(self) -> str:
        """Go back to the latest question."""
        try:
            self.question = await self.akinator.back()
            self.count -= 1
        except CantGoBackAnyFurther:
            await self.channel.send(
                "Il faut deja repondre a une question."
            )
        return self.question

    async def determine_win(self):
        await self.akinator.win()
        await self.channel.send(embed=await self.make_guess_embed())
        check = MessagePredicate.yes_or_no(channel=self.channel, user=self.user)
        self.task = asyncio.create_task(self.bot.wait_for("message", check=check, timeout=60))
        try:
            await self.task
        except (asyncio.TimeoutError, asyncio.CancelledError):
            await self.channel.send("J'espere avoir juste. \N{WEARY FACE}")
            return
        if check.result:
            await self.channel.send("Je lis dans ta tete !")
            return True
        await self.channel.send(
            "Arf je suis triste de n'avoir pas trouvé."
        )
        return False

    async def make_guess_embed(self):
        embed = discord.Embed(
            title="Je crois que j'ai trouvé...",
            description="C'est {name}? Voila la description : {desc}.".format(
                name=self.akinator.first_guess["name"],
                desc=self.akinator.first_guess["description"],
            ),
        )
        embed = randomize_colour(embed)
        embed.set_image(url=self.akinator.first_guess["absolute_picture_path"])
        embed.set_footer(
            icon_url=self.user.avatar_url,
            text=(
                "Partie de {name}. En {num} questions! UnicornCorp"
            ).format(name=self.user.name, num=self.count, ver=__version__),
        )
        return embed
