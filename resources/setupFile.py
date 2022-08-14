import random
import sqlite3

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

async def setup_bot_role(interaction):
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
async def createRoles(interaction):
    x = 0

    await interaction.response.defer()
    conn = sqlite3.connect(r"..\resources\acting_method.db")
    print(conn)
    print("Opened database successfully")

    sequencesCursor = conn.execute("SELECT sequences_name, sequences_color,sequences_num from sequences")
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
async def channel_setup(interaction):
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
        category = interaction.get_channel(guildChannelDict[categoryName])
    for channelname in toAddChannelList:
        if channelname not in guildChannelList:
            await interaction.guild.create_text_channel(name=channelname, category=category)
    #todo add a way to store channel info in the database