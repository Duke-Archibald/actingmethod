import random
import sqlite3

from resources import setupFile
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class DropDown(nextcord.ui.Select):
    def __init__(self):
        self.pathways = []
        self.conn = sqlite3.connect('./resources/acting_method.db')
        pathwaysCursor = self.conn.execute(f"SELECT pathways_name"
                                           f" FROM pathways")
        for path in pathwaysCursor:
            self.pathways.append(path[0])
        print(self.pathways)
        selectoption = []
        for pathway in self.pathways:
            # print(pathway)
            # print(type(pathway))
            selectoption.append(nextcord.SelectOption(label=pathway))
        super().__init__(placeholder="choose one pathway", options=selectoption,)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()

        role = nextcord.utils.get(interaction.guild.roles, name=f"pathway:{self.values[0]}")

        userroles = interaction.user.roles
        for userrole in userroles:
            if userrole.name.replace("pathway:", "") in self.pathways:
                await interaction.user.remove_roles(userrole)
                seqQuery = f"SELECT sequences_name,sequences_num FROM sequences where sequences_pathway = '{userrole.name.replace('pathway:', '')}'"
                sequencesCursor = self.conn.execute(seqQuery)
                for seq, num in sequencesCursor:
                    if num in [0, 1, 2, 3, 4]:
                        print(seq, num)
                        Rrole = nextcord.utils.get(interaction.guild.roles, name=f"{seq}")
                        if Rrole in userroles:
                            await interaction.user.remove_roles(Rrole)
                    elif num in [5, 6, 7]:
                        print("mid", num)
                        Rrole = nextcord.utils.get(interaction.guild.roles,
                                                   name=f"{userrole.name.replace('pathway:', '')} pathway mid sequence")
                        if Rrole in userroles:
                            await interaction.user.remove_roles(Rrole)
                    elif num in [8, 9]:
                        print("low", num)
                        Rrole = nextcord.utils.get(interaction.guild.roles,
                                                   name=f"{userrole.name.replace('pathway:', '')} pathway low sequence")
                        if Rrole in userroles:
                            await interaction.user.remove_roles(Rrole)
        await interaction.user.add_roles(role)
        await interaction.user.send(f"you chose the {self.values[0]} pathway")


class DropDownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DropDown())
