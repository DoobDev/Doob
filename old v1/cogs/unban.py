import discord
from discord.ext import commands
doob_logo = "https://cdn.discordapp.com/avatars/680606346952966177/ada47c5940b5cf8f7e12f61eefecc610.webp?size=1024"

class unban(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    # Unbans a user that the user has specified.
    @commands.command()
    # Checks to see if user has the Ban Members permission.
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title="User Unbanned", description=f"{user.name} has been unbanned from the server.", colour=discord.Color.blue())

                embed.add_field(name="User", value=f"@{user.name}#{user.discriminator}")
                embed.set_thumbnail(url="https://www.flaticon.com/svg/static/icons/svg/1250/1250740.svg")
                await ctx.send(embed=embed)


                return

def setup(client):
    client.add_cog(unban(client))