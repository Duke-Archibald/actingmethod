import random
import sqlite3

from resources import setupFile
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from resources.dropview import DropDownView


class ButtonsView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None


class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client

    guildID = 1005560781603090504

    @nextcord.slash_command(name="basic-command",
                            description="this is just a command template it does nothing",
                            guild_ids=[guildID])
    async def basic_command(self, interaction: Interaction):
        await interaction.response.send_message(f'nothing')

        # await interaction.response.send_message("done")

    @nextcord.slash_command(name="deltest", guild_ids=[guildID],
                            description="delete ALL roles, use carefully, will be removed after testing")
    async def deltest(self, interaction: Interaction):
        for role1 in [role for role in interaction.guild.roles]:
            if role1.name == "@everyone":
                print("not", role1)
                continue
            print(role1)

            await role1.delete()

    @nextcord.slash_command(name="setup", guild_ids=[guildID], description="create channels")
    @commands.has_any_role(*["Admin"])
    async def setup(self, interaction: Interaction):
        await setupFile.setup_bot_role(interaction)
        await setupFile.channel_setup(interaction)
        await setupFile.createRoles(interaction)

    @nextcord.slash_command(name="drop",
                            guild_ids=[guildID],
                            description="dropdown test")
    @commands.has_any_role(*["Admin"])
    async def drop(self, interaction: Interaction):
        print("drop")
        view = DropDownView()
        channel = nextcord.utils.get(interaction.guild.channels, name="pathways-menu")
        message = await channel.send("choose your pathway", view=view)
        self.conn
        # with open("test.txt", "w", encoding="utf8") as f:
        #     f.write(str(message.id))
        #     f.write("\n")
        #     f.write(str(message.channel.id))

    @nextcord.slash_command(name="botcolor",
                            guild_ids=[guildID],
                            description="dropdown test")
    @commands.has_any_role(*["Admin"])
    async def botcolor(self, interaction: Interaction, hexinput=SlashOption(required=False)):
        Rname = "selfBot"

        role = nextcord.utils.get(interaction.guild.roles, name=Rname)
        if hexinput:
            color = hexinput
        else:
            color = "%06x" % random.randint(0, 0xFFFFFF)
        await role.edit(colour=nextcord.Colour(int(color, 16)))
        await interaction.response.send_message(f"bot color changed to {color}")


def setup(client):
    client.add_cog(Basic(client))
    print("basic loaded")
