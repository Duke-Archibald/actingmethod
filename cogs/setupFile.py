import random
import sqlite3

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
class setupfile(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.conn = sqlite3.connect(r".\resources\acting_method.db")

    guildID = 1005560781603090504
    @nextcord.slash_command(name="setup", guild_ids=[guildID], description="create channels")
    @commands.has_any_role(*["Admin"])
    async def setup(self, interaction: Interaction):
        await setupfile.setup_bot_role(self, interaction)
        await setupfile.channel_setup(self,interaction)
        await setupfile.createRoles(self,interaction)
    async def setup_bot_role(self,interaction):
        Rname = "selfBot"

        if Rname in [role.name for role in interaction.guild.roles]:
            pass
        else:
            await interaction.guild.create_role(name=Rname)
        role = nextcord.utils.get(interaction.guild.roles, name=Rname)
        member = interaction.guild.get_member(1005525121496268830)
        if Rname in [role.name for role in member.roles]:
            pass
        else:
            await member.add_roles(role)
    async def createRoles(self,interaction):
        x = 0

        await interaction.response.defer()

        sequencesCursor = self.conn.execute("SELECT sequences_name, sequences_color,sequences_num from sequences")
        pathway = "none"
        for seq in sequencesCursor:
            roles = [role for role in interaction.guild.roles]
            if seq[2] == 0:
                pathway = seq[0]
            if seq[0] in [role.name for role in roles]:
                x += 1
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
    async def channel_setup(self,interaction):
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
            self.conn.execute("INSERT INTO channels(channels_id,channels_name,channels_channel_id,channels_guild_id,channels_category_id) VALUES();")
        else:
            category = interaction.guild.get_channel(guildChannelDict[categoryName])
            self.conn.execute("INSERT INTO channels(channels_id,channels_name,channels_channel_id,channels_guild_id,channels_category_id) VALUES();")
        for channelname in toAddChannelList:
            if channelname not in guildChannelList:
                await interaction.guild.create_text_channel(name=channelname, category=category)
    #todo add a way to store channel info in the database
def setup(client):
    client.add_cog(setupfile(client))
    print("setup loaded")


