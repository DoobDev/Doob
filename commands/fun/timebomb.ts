import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { DiscordOption } from '../../utils/discordoptions';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'timebomb',
    description: 'Timebomb',
    usage: 'timebomb <message: str> <time: num>',
    category: 'Fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    options: [
        {
            name: 'msg',
            description: 'Message to send',
            required: true,
            type: DiscordOption('STRING'),
        },
        {
            name: 'time',
            description: 'The time until the message gets deleted.',
            required: true,
            type: DiscordOption('INTEGER'),
        },
    ],

    callback: async ({ interaction, args }) => {
        const [msg, time] = args;

        const embed = new MessageEmbed()
            .setDescription(`**${interaction.user.username} said:**\n${getEmote('transparent>')} "${msg}"`)
            .setThumbnail(`${interaction.user.avatarURL()}`)
            .setFooter(`This message lasts ${time}s`)
            .setColor(getDoobColor('DOOB'));

        await interaction.reply({ embeds: [embed] });

        await new Promise((resolve) => setTimeout(resolve, parseInt(time) * 1000));

        await interaction.deleteReply();
    },
} as ICommand;
