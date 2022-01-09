import { Octokit } from '@octokit/rest';
import { ICommand } from 'wokcommands';
import config from '../../../config';
import { getEmote } from '../../../utils/emotes';
import { doobEmbed, errorEmbed } from '../../../utils/generic_embeds';

const octokit = new Octokit({ auth: config.githubPat }); // github personal access token, stored as `GITHUB_PAC` in .env

export default {
    category: 'api',
    name: 'createissue',
    description: 'create an issue on doobdev/doob.',

    testOnly: true,
    ownerOnly: true, // don't remove
    slash: false,

    minArgs: 1,
    expectedArgs: '<label> <title>',

    callback: async ({ message }) => {
        const args = message.content.split(' || ');
        const label = args[0].replace('d!createissue', '');
        let embed_title = '';
        const tab = `${getEmote('transparentSpace')}${getEmote('transparent>')}`;

        if (!args[0]) {
            return errorEmbed('label missing');
        } else if (!args[1]) {
            return errorEmbed('title missing');
        }

        await octokit.rest.issues
            .create({
                owner: 'doobdev',
                repo: 'doob',
                title: args[1],
                labels: [label],
            })
            .then(({ data }) => {
                embed_title = `**issue #${data.number} created**\n${tab} ${data.html_url}`;
            });

        return doobEmbed(embed_title);
    },
} as ICommand;
