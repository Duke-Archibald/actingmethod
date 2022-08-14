import random
import sqlite3

from resources import setupFile
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands


class DropDown(nextcord.ui.Select):
    def __init__(self):
        self.pathways = []
        conn = sqlite3.connect('../resources/acting_method.db')
        pathwaysCursor = conn.execute(f"SELECT pathways_name"
                                      f" FROM pathways")
        for path in pathwaysCursor:
            self.pathways.append(path)
        print(self.pathways)
        selectoption = []
        for pathway in self.pathways:
            selectoption.append(nextcord.SelectOption(label=pathway))
        super().__init__(placeholder="choose one pathway", options=selectoption)

    async def callback(self, interaction: Interaction):
        role = nextcord.utils.get(interaction.guild.roles, name=f"{self.values[0]}")

        userroles = interaction.user.roles
        for userrole in userroles:
            if userrole in self.pathways:
                await interaction.user.remove_roles(userrole)
        await interaction.user.add_roles(role)
        await interaction.user.send(f"you chose the {self.values[0]} pathway")
        await interaction.response.defer()


class DropDownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropDown())