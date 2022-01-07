import { GuildMember } from 'discord.js';
import { ICommand } from 'wokcommands';
import { DiscordOption } from '../../utils/discordoptions';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'untimeout',
    description: 'remove a timeout a user',
    usage: 'untimeout <user>',
    category: 'moderation',

    permissions: ['KICK_MEMBERS'],

    minArgs: 1,
    expectedArgs: '<user>',
    options: [
        {
            name: 'user',
            description: 'the user you would like to timeout',
            type: DiscordOption('USER'),
            required: true,
        },
    ],

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({ interaction }) => {
        const user = interaction.options.getMember('user') as GuildMember;

        if (!user) {
            return errorEmbed('invalid user provided');
        }

        user.timeout(null).then((user) => {
            user.send(`⚠️ you have been untimed out in ${user.guild.name}`);
        });
        return doobEmbed(`${user.nickname || user.user.username} has been untimed out`);
    },
} as ICommand;
