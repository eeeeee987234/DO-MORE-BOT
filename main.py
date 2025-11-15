import os
import discord
from discord import app_commands
from discord.ui import Select, View

# Get token - try different environment variable names
token = os.getenv('DISCORD_TOKEN') or os.getenv('TOKEN')

if not token:
    print("ERROR: No token found!")
    print("Please set DISCORD_TOKEN environment variable in Koyeb")
    exit(1)

print(f"Token found, starting bot...")

class UpdateBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Commands synced!")

bot = UpdateBot()

status_choices = [
    app_commands.Choice(name="Friendly", value="Friendly"),
    app_commands.Choice(name="Neutral", value="Neutral"),
    app_commands.Choice(name="Hostile", value="Hostile"),
    app_commands.Choice(name="Unknown", value="Unknown"),
    app_commands.Choice(name="N/A", value="N/A"),
]

class FactionSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Global Occult Coalition (GOC)", value="Global Occult Coalition (GOC)"),
            discord.SelectOption(label="Foundation", value="Foundation"),
            discord.SelectOption(label="Chaos Insurgency", value="Chaos Insurgency"),
            discord.SelectOption(label="Serpent's Hand", value="Serpent's Hand"),
            discord.SelectOption(label="UIU", value="UIU"),
            discord.SelectOption(label="Marshall, Carter & Dark", value="Marshall, Carter & Dark"),
            discord.SelectOption(label="Horizon Initiative", value="Horizon Initiative"),
            discord.SelectOption(label="Other", value="Other"),
        ]
        super().__init__(placeholder="Select faction...", max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        faction = self.values[0]
        view = StatusSelectView(faction)
        embed = discord.Embed(
            title="📊 Status Selection",
            description=f"Faction: **{faction}**\n\nNow select the status change:",
            color=0x5865F2)
        await interaction.response.edit_message(embed=embed, view=view)

class StatusSelectView(View):
    def __init__(self, faction):
        super().__init__()
        self.faction = faction
        self.add_item(OldStatusSelect())
        self.add_item(NewStatusSelect())

class OldStatusSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Friendly", value="Friendly", emoji="🟢"),
            discord.SelectOption(label="Neutral", value="Neutral", emoji="🟡"),
            discord.SelectOption(label="Hostile", value="Hostile", emoji="🔴"),
            discord.SelectOption(label="Unknown", value="Unknown", emoji="⚫"),
            discord.SelectOption(label="N/A", value="N/A", emoji="❔"),
        ]
        super().__init__(placeholder="Old Status...", max_values=1, options=options, row=0)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class NewStatusSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Friendly", value="Friendly", emoji="🟢"),
            discord.SelectOption(label="Neutral", value="Neutral", emoji="🟡"),
            discord.SelectOption(label="Hostile", value="Hostile", emoji="🔴"),
        ]
        super().__init__(placeholder="New Status...", max_values=1, options=options, row=1)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        old_status_select = view.children[0]
        new_status_select = view.children[1]

        if not hasattr(old_status_select, 'values') or not old_status_select.values:
            await interaction.response.send_message("Please select the OLD status first!", ephemeral=True)
            return

        old_status = old_status_select.values[0]
        new_status = new_status_select.values[0]
        faction = view.faction

        message_content = f"<@&1438590573178257530>"
        embed = discord.Embed(title="📊 Status Change", color=0x00ff00)
        embed.add_field(
            name=f"**{faction} :-**",
            value=f"INRP Status: **{old_status} --> {new_status}**\n\n**GoI File:** will be made within 24h.",
            inline=False)
        embed.set_footer(text="DoEA Console")
        await interaction.response.send_message(content=message_content, embed=embed)

@bot.tree.command(name="update", description="Update faction status (quick command)")
@app_commands.choices(previous_status=status_choices, new_status=status_choices)
async def update(interaction: discord.Interaction,
                 faction_name: str,
                 previous_status: app_commands.Choice[str],
                 new_status: app_commands.Choice[str],
                 file: str = "will be made within 24h"):
    message_content = f"<@&1438590573178257530>"
    embed = discord.Embed(title="📊 Status Change", color=0x00ff00)
    embed.add_field(
        name=f"**{faction_name} :-**",
        value=f"INRP Status: **{previous_status.value} --> {new_status.value}**\n\n**GoI File:** {file}",
        inline=False)
    embed.set_footer(text="DoEA Console")
    await interaction.response.send_message(content=message_content, embed=embed)

@bot.tree.command(name="status", description="Update faction status with menus")
async def status(interaction: discord.Interaction):
    view = View()
    view.add_item(FactionSelect())
    embed = discord.Embed(title="🏛️ DoEA Status Console",
                          description="Select the faction to update:",
                          color=0x5865F2)
    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    print(f'✅ DoEA Console is online as {bot.user}!')

bot.run(token)
