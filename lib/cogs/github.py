from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import Cog, group

import json

from typing import Optional

with open("config.json") as config_file:
    config = json.load(config_file)

from github import Github

import os
from dotenv import load_dotenv

load_dotenv()

owner_id = config["owner_ids"][0]

token = os.environ.get("github")


class GitHub(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_github_issues(self, ctx):
        ghclient = Github(token)
        repo = ghclient.get_repo("DoobDev/Doob")

        open_issues = repo.get_issues(state="open")

        llist = [f"[‣ #{i.number} - {i.title}]({i.html_url})" for i in open_issues]

        if llist:
            embed = Embed(
                title="Open Issues in `DoobDev/Doob`",
                description="\n".join(llist),
                colour=ctx.author.colour,
            )
            await ctx.reply(embed=embed)

        else:
            await ctx.reply("⚠ No Opened Issues found in `DoobDev/Doob`")

    @group(name="issue", aliases=["issues"])
    async def issue(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.show_github_issues(ctx)

    @issue.command(name="-create", aliases=["-c"])
    @commands.is_owner()
    async def create_github_issue(
        self, ctx, label: str, priority_label: str, *, title: str
    ):
        ghclient = Github(token)
        repo = ghclient.get_repo("DoobDev/Doob")

        if priority_label == "high":
            gh_priority_label = "High Priority"

        elif priority_label == "medium":
            gh_priority_label = "Medium Priority"

        elif priority_label == "low":
            gh_priority_label = "Low Priority"

        issue = repo.create_issue(
            title=title, body="`Issue Created via Doob for Discord`", labels=[label]
        )

        issue.add_to_labels(gh_priority_label)

        await ctx.reply(f"Issue Created. {issue.html_url}")

    @issue.command(name="-close", aliases=["-d", "-cl"])
    @commands.is_owner()
    async def close_github_issue(
        self, ctx, issue_number: int, *, reason: Optional[str]
    ):
        if reason is None:
            reason = ""

        ghclient = Github(token)
        repo = ghclient.get_repo("DoobDev/Doob")

        issue = repo.get_issue(issue_number)

        issue.edit(state="closed")
        issue.create_comment(f"{reason}\n\n`Issue Closed via Doob for Discord`")

        await ctx.reply(f"Issue closed. {issue.html_url}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("github")


def setup(bot):
    bot.add_cog(GitHub(bot))
