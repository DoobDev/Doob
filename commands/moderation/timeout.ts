import { GuildMember } from 'discord.js';
import { ICommand } from 'wokcommands';
import { DiscordOption } from '../../utils/discordoptions';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'timeout',
    description: 'timeout a user',
    usage: 'timeout <user> <length> <reason>',
    category: 'moderation',

    permissions: ['KICK_MEMBERS'],

    minArgs: 2,
    expectedArgs: '<user> <length> <reason>',
    options: [
        {
            name: 'user',
            description: 'the user you would like to timeout',
            type: DiscordOption('USER'),
            required: true,
        },
        {
            name: 'length',
            description: 'the length you would like to timeout the user (in seconds)',
            type: DiscordOption('NUMBER'),
            required: true,
        },
        {
            name: 'reason',
            description: 'the reason you would like to timeout the user',
            type: DiscordOption('STRING'),
            required: false,
        },
    ],

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({ interaction }) => {
        const user = interaction.options.getMember('user') as GuildMember;
        const length = interaction.options.getNumber('length');
        let reason = interaction.options.getString('reason');

        if (!user) {
            return errorEmbed('invalid user provided');
        } else if (!length) {
            return errorEmbed('invalid length provided');
        } else if (length < 1) {
            return errorEmbed('invalid length provided');
        } else if (!reason) {
            reason = 'no reason provided';
        }

        user.timeout(length * 1000, reason).then((user) => {
            user.send(`⚠️ you have been timed out in ${user.guild.name} for ${length} seconds for \`${reason}\``);
        });
        return doobEmbed(`${user.nickname || user.user.username} has been timed out for ${length} seconds`);
    },
} as ICommand;
