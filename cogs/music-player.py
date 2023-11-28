import discord
import wavelink
from discord import app_commands
from discord.ext import commands


class Music_list(discord.ui.View):
  def __init__(self, tracks):
    self.track_id = 0
    super().__init__(timeout=None)
    self.tracks = tracks
    self.init_buttons()
  
  def init_buttons(self):
    for i in range(len(self.tracks)):
      if i == 5:
        break
      button = discord.ui.Button(label=str(i + 1), style=discord.ButtonStyle.blurple, custom_id=str(i))
      async def callback_function(interaction, i):
        self.track_id = i
        self.stop()
      
      button.callback = lambda interaction, i=i: callback_function(interaction, i)
      self.add_item(button)


class Music_player(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @app_commands.command(name="play", description="Play music")
  @app_commands.guild_only()
  @app_commands.describe(search="Search or link")
  async def play(self, interaction: discord.Integration, search: str):
    if not interaction.user.voice:
      return await interaction.response.send_message(embed=discord.Embed(description="You are not in a voice channel"))
    if not interaction.guild.voice_client:
      vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    else:
      vc: wavelink.Player = interaction.guild.voice_client
    
    tracks = await wavelink.Playable.search(search)

    view = Music_list(tracks)

    def format_length(milliseconds):
      seconds = milliseconds // 1000
      minutes = seconds // 60
      hours = minutes // 60

      seconds %= 60
      minutes %= 60

      if hours == 0:
          return "{:02d}:{:02d}".format(minutes, seconds)
      if minutes == 0:
          return "{:02d}".format(seconds)
      
      return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    
    if tracks:
      description = f"Showing results for `{search}`. Select one of result below\n"
      for i in range(len(tracks)):
        if i == 5:
          break
        description += f'{i + 1}. {tracks[i]} ({format_length(tracks[i].length)}) - {tracks[i].source.capitalize()}\n'
      embed = discord.Embed(
        description=description,
        color=0xad1457
      )
    else:
      embed = discord.Embed(
        description="nothing was found",
        color=0xad1457
      )
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    await view.wait()

    if not vc.playing:
      await vc.play(tracks[view.track_id])
    embed = discord.Embed(
      description=f"**{tracks[view.track_id].title}** has been added to the queue.",
      color=0xad1457
    )
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
    await interaction.channel.send(embed=embed)

  @app_commands.command(name="leave", description="Leave voice channel")
  @app_commands.guild_only()
  async def leave(self, interaction: discord.Integration):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.disconnect()
    await interaction.response.send_message(embed=discord.Embed(description="Disconnected from voice channel", color=0xad1457))
  
  @app_commands.command(name="pause", description="Pause Music")
  async def pause(self, interaction: discord.Integration):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.pause(not vc.paused)
    await interaction.response.send_message(embed=discord.Embed(description=f"The pleyer is now {vc.paused}", color=0xad1457))
  
  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    vc = member.guild.voice_client

    if not vc:
      return
    
    if len(vc.channel.members) == 1:
      await vc.stop()
      await vc.disconnect()


async def setup(bot: commands.Bot):
  await bot.add_cog(Music_player(bot))
