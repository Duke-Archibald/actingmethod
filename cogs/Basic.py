import sqlite3
import aiosqlite
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from nextcord.abc import GuildChannel
import nextcord
from nextcord.types.channel import TextChannel

import colorsFunc
import loaders2
import Loaders
from testing import sqlittest


class ButtonsView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None


class DropDown(nextcord.ui.Select):
    def __init__(self):
        self.pathways = Loaders.load_Pathway()
        print(self.pathways)
        selectoption = []
        for pathway in self.pathways:
            selectoption.append(nextcord.SelectOption(label=pathway))
        super().__init__(placeholder="choose one pathway", options=selectoption)

    async def callback(self, interaction: Interaction):
        role = nextcord.utils.get(interaction.guild.roles, name=f"{self.values[0]}")

        # userroles = interaction.user.roles
        # for userrole in userroles:
        #     if userrole in pathways:
        #         await interaction.user.remove_roles(userrole)
        await interaction.user.add_roles(role)
        await interaction.user.send(f"you chose the {self.values[0]} pathway")
        await interaction.response.defer()


class DropDownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropDown())


class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pathways = Loaders.load_Pathway()
        self.colors = Loaders.load_Color()

    guildID = 1005560781603090504

    @nextcord.slash_command(name="basic-command",
                            description="this is just a command template it does nothing",
                            guild_ids=[guildID])
    async def basic_command(self, interaction: Interaction):
        await interaction.response.send_message(f'nothing')

    async def createRoles(self, interaction: Interaction):
        x = 0
        # color = colorsFunc.linear_gradient(self.colors[x],"#5B626B")

        await interaction.response.defer()
        # await sqlittest.createRoles()
        conn = sqlite3.connect('./acting_method.db')
        print(conn)
        print("Opened database successfully")

        cursor = conn.execute("SELECT sequences_name, sequences_color,sequences_num from sequences")
        pathway = "none"
        for seq in cursor:
            roles = [role for role in interaction.guild.roles]
            print("roles", roles)
            if seq[2] == 0:
                pathway = seq[0]
            if x >= 10:
                continue
            if seq[0] in [role.name for role in roles]:
                x += 1
                print("already there", x)
            else:
                x += 1
                await interaction.followup.send(f"creating {seq[0]}")
                if seq[2] == 0:
                    await interaction.guild.create_role(name=f"pathway:{seq[0]}",
                                                        colour=nextcord.Colour(int(seq[1], 16)), hoist=True)
                    await interaction.guild.create_role(name=f"{seq[0]}", colour=nextcord.Colour(int(seq[1], 16)))
                elif seq[2] == 5:
                    if f"{pathway} pathway mid sequence" in [role.name for role in roles]:
                        pass
                    else:
                        await interaction.guild.create_role(name=f"{pathway} pathway mid sequence",
                                                        colour=nextcord.Colour(int(seq[1], 16)))
                elif seq[2] == 6:
                    continue
                elif seq[2] == 7:
                    continue
                elif seq[2] == 8:
                    if f"{pathway} pathway low sequence" in [role.name for role in roles]:
                        pass
                    else:
                        await interaction.guild.create_role(name=f"{pathway} pathway low sequence",
                                                        colour=nextcord.Colour(int(seq[1], 16)))
                elif seq[2] == 9:
                    continue
                else:
                    await interaction.guild.create_role(name=f"{seq[0]}", colour=nextcord.Colour(int(seq[1], 16)))

        await interaction.followup.send("done")
        # await interaction.response.send_message("done")

    @nextcord.slash_command(name="deltest", guild_ids=[guildID], description="create channels")
    async def deltest(self, interaction: Interaction):
        roles = [role for role in interaction.guild.roles]
        for role1 in roles:
            if role1.name == "@everyone":
                print("not", role1)
                continue
            print(role1)

            await role1.delete()

    @nextcord.slash_command(name="setup", guild_ids=[guildID], description="create channels")
    @commands.has_any_role(*["Admin"])
    async def setup(self, interaction: Interaction):
        categoryName = "Acting Method"
        toAddChannelList = ["pathways-menu", "digestion-update", "trash-bot"]
        guildChannels = interaction.guild.channels
        guildChannelList = []
        guildChannelDict = {}

        for channel in guildChannels:
            guildChannelList.append(channel.name)
            guildChannelDict[channel.name] = channel.id
        if categoryName not in guildChannelList:
            category = await interaction.guild.create_category(name=categoryName)
        else:
            category = self.client.get_channel(guildChannelDict[categoryName])
        print(guildChannelList)
        for channelname in toAddChannelList:
            print(channelname)
            print(channelname not in guildChannelList)
            if channelname not in guildChannelList:
                channel = await interaction.guild.create_text_channel(name=channelname, category=category)
                print(channel)
        await self.createRoles(interaction=interaction)

    @nextcord.slash_command(name="drop",
                            guild_ids=[guildID],
                            description="dropdown test")
    @commands.has_any_role(*["Admin"])
    async def drop(self, interaction: Interaction):
        try:
            with open("test.txt", "r") as f:
                view = DropDownView()

                ids = f.readlines()
                message_id = int(ids[0])
                channel = self.client.get_channel(int(ids[1]))
                msg = await channel.fetch_message(message_id)
                await msg.edit(content=" choose your pathway", view=view)
                await interaction.response.send_message("pathways reloaded")
        except IOError:
            view = DropDownView()
            channel = nextcord.utils.get(interaction.guild.channels, name="pathways-menu")
            message = await channel.send("choose your pathway", view=view)
            with open("test.txt", "w", encoding="utf8") as f:
                f.write(str(message.id))
                f.write("\n")

                f.write(str(message.channel.id))
            print(message.id)
            print(message.channel.id)
    @nextcord.slash_command(name="botaction",
                            guild_ids=[guildID],
                            description="dropdown test")
    @commands.has_any_role(*["Admin"])
    async def actionOnBot(self, interaction: Interaction):
        await interaction.guild.create_role(name=f"selfbot")
        role = nextcord.utils.get(interaction.guild.roles, name=f"selfbot")
        await self.client.user.add_roles(role)

def setup(client):
    client.add_cog(Basic(client))
    print("basic loaded")
# f"create or choose a channel for the digestion update ('lom potion', 'lom ritual', and digestion update)\n"
# f"create or choose a channel for the pathways menu (choosing of one's pathways)\n"
# f"create or choose a channel for the bot trash (all system messages from the bot (update notification and admin command output)\n"
# f"\n"
# f"use the command\n"
# f"lom Setup channels (lom s c)[ID of Pathways Menu] [ID of Digestion Update] [ID of bot trash] "
# f"(order is important) ---to assign the channel for the bot messages\n"
# f"lom Setup roles (lom s ro) ---to create all the roles\n"
# f"lom Setup emote (lom s e) ---to create all the emoji\n"
# f"lom Setup menu (lom s m) ---to create the reaction menu\n"
# f"all command are not case sensitive\n"
