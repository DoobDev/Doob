import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { DiscordOption } from '../../utils/discordoptions';
import { errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'userinfo',
    description: 'get information about a user',
    category: 'info',

    options: [
        {
            name: 'user',
            description: 'user to get info about',
            required: false,
            type: DiscordOption('USER'),
        },
    ],
    minArgs: 0,

    expectedArgs: '<user>',

    slash: true,
    testOnly: true,

    callback: ({ interaction, user }) => {
        let userToGet;
        if (!interaction.options.getUser('user')) {
            userToGet = user;
        } else if (interaction.options.getUser('user')) {
            userToGet = interaction.options.getUser('user');
        } else {
            return errorEmbed('user not found');
        }

        if (!userToGet) {
            return errorEmbed('user not found');
        }

        return new MessageEmbed()
            .setThumbnail(`${userToGet.avatarURL()}`)
            .setTitle(`${userToGet.username}'s information.`)
            .setDescription(`${userToGet.id}`)
            .setColor(userToGet.accentColor ?? getDoobColor.DOOB);
    },
} as ICommand;
