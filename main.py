from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import nextcord
import os
from dotenv import load_dotenv

from cogs.Basic import DropDownView

# load_dotenv()
TOKEN = os.getenv("TOKEN")
TOKEN2 = os.getenv("TOKEN2")
client = commands.Bot()
guildID = 1005560781603090504
cogs_list = ["all"]
test="test"
cogs_dict = {}


@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")
    try:
        with open("test.txt", "r") as f:
            view = DropDownView()

            ids = f.readlines()
            message_id = int(ids[0])
            channel = client.get_channel(int(ids[1]))
            msg = await channel.fetch_message(message_id)
            await msg.edit(content=" choose your pathway", view=view)
    except IOError:
        pass

@client.slash_command(description="cogs", guild_ids=[guildID])
async def cogs(interaction: Interaction,
               action: int = SlashOption(
                   name="action",
                   choices={"reload": 3,"load": 1, "unload": 2}),
               cog: str = SlashOption(
                   name="cog",
                   choices=cogs_list)):
    if cog == "all":
        cogs_list.pop(0)
        for cogsingle in cogs_list:
            if action == 1:
                client.load_extension(f"cogs.{cogsingle}")
            elif action == 2:
                client.unload_extension(f"cogs.{cogsingle}")
            elif action == 3:
                client.reload_extension(f"cogs.{cogsingle}")
        await interaction.response.send_message(f"all cogs where updated.")
        cogs_list.insert(0,"all")
    else:
        if action == 1:
            client.load_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"Loaded {cog}.")
        elif action == 2:
            client.unload_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"Unloaded {cog}.")
        elif action == 3:
            client.reload_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"Reloaded {cog}.")


for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        cogs_list.append(f"{fn[:-3]}")
        client.load_extension(f"cogs.{fn[:-3]}")

client.run(TOKEN2)
