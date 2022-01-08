import { Octokit } from '@octokit/rest';
import { ICommand } from 'wokcommands';
import config from '../../../config';
import { getEmote } from '../../../utils/emotes';
import { doobEmbed, errorEmbed } from '../../../utils/generic_embeds';

const octokit = new Octokit({ auth: config.githubPat }); // github personal access token, stored as `GITHUB_PAC` in .env

export default {
    category: 'api',
    name: 'issues',
    description: "get all the issues from doob's issue list on github",

    testOnly: true,
    slash: true,

    callback: async ({ interaction }) => {
        interaction.deferReply();
        let embed = '';
        await octokit.rest.issues.listForRepo({ owner: 'doobdev', repo: 'doob' }).then(({ data }) => {
            let issues: string[] = [];

            data.forEach((issue) => {
                issues.push(`[#${issue.number} - ${issue.title}](${issue.html_url})`);
            });

            const tab = `${getEmote('transparentSpace')}${getEmote('transparent>')}`;

            let issue_list: string[] = [];

            issues.forEach((issue) => {
                issue_list.push(`${tab} ${issue}`);
            });

            embed = `**issue list: doobdev/doob**\n` + `${issue_list.join('\n')}`;
        });

        if (!embed) {
            return errorEmbed('could not find any issues.');
        }

        interaction.editReply({ embeds: [doobEmbed(embed)] });
    },
} as ICommand;
