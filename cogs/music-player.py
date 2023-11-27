from typing import Optional
import discord
import wavelink
from discord import app_commands
from discord.ext import commands
import pprint


class Music_list(discord.ui.View):
  def __init__(self):
    self.track_id = 0
    super().__init__(timeout=300)
  
  @discord.ui.button(label="1", style=discord.ButtonStyle.blurple)
  async def play_1(self, button, interaction):
    self.track_id = 0
    self.stop()

  @discord.ui.button(label="2", style=discord.ButtonStyle.blurple)
  async def play_2(self, button, interaction):
    self.track_id = 1
    self.stop()

  @discord.ui.button(label="3", style=discord.ButtonStyle.blurple)
  async def play_3(self, button, interaction):
    self.track_id = 2
    self.stop()
  
  @discord.ui.button(label="4", style=discord.ButtonStyle.blurple)
  async def play_4(self, button, interaction):
    self.track_id = 3
    self.stop()
  
  @discord.ui.button(label="5", style=discord.ButtonStyle.blurple)
  async def play_5(self, button, interaction):
    self.track_id = 4
    self.stop()
  
  @discord.ui.button(label="", style=discord.ButtonStyle.red, emoji='<:yt:1178649329678954496>')
  async def youtube(self, button, interaction):
    pass


class Music_player(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
  
  @app_commands.command(name="play", description="Play music")
  @app_commands.guild_only()
  @app_commands.describe(search="Search request")
  async def play(self, interaction: discord.Integration, search: str):
    if not interaction.guild.voice_client:
      vc: wavelink.Player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
    else:
      vc: wavelink.Player = interaction.guild.voice_client

    tracks = await wavelink.YouTubeTrack.search(search)

    view = Music_list()

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
    
    embed = discord.Embed(
      description=f"Showing results for `{search}`. Select one of result below\n" + '\n'.join([f'{i + 1}. {tracks[i]} ({format_length(tracks[i].length)})' for i in range(5)]),
      color=0xad1457
    )
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    await view.wait()
    if view.track_id:
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
    await interaction.response.send_message(embed=discord.Embed(description="Disconnected channel", color=0xad1457))
  
  @app_commands.command(name="pause", description="Pause Music")
  async def pause(self, interaction: discord.Integration):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.pause()
    await interaction.response.send_message(embed=discord.Embed(description="The pleyer is now paused", color=0xad1457))
  
  @app_commands.command(name="resume", description="Resume Music")
  async def resume(self, interaction: discord.Integration):
    vc: wavelink.Player = interaction.guild.voice_client
    await vc.resume()
    await interaction.response.send_message(embed=discord.Embed(description="The pleyer is now resumed", color=0xad1457))
  
  @commands.Cog.listener()
  async def on_voice_state_update(self, member, before, after):
    vc = member.guild.voice_client

    if not vc:
      return
    
    if len(vc.channel.members) == 1:
      await vc.disconnect()


async def setup(bot: commands.Bot):
  await bot.add_cog(Music_player(bot))
