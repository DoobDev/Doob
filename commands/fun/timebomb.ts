import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { DiscordOption } from '../../utils/discordoptions';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'timebomb',
    description: 'a message that automatically deletes after a certain time.',
    usage: 'timebomb <message: str> <time: num>',
    category: 'fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    options: [
        {
            name: 'msg',
            description: 'message to send',
            required: true,
            type: DiscordOption('STRING'),
        },
        {
            name: 'time',
            description: 'the time until the message gets deleted.',
            required: true,
            type: DiscordOption('INTEGER'),
        },
    ],

    callback: async ({ interaction, args }) => {
        const msg = args[0];
        let time = parseInt(args[1]);

        if (time < 1) {
            time = 1;
        } else if (time > 1001) {
            time = 1000;
        }

        const embed = new MessageEmbed()
            .setDescription(`**${interaction.user.username} said:**\n${getEmote('transparent>')} "${msg}"`)
            .setThumbnail(`${interaction.user.avatarURL()}`)
            .setFooter(`this message lasts ${time}s`)
            .setColor(getDoobColor.DOOB);

        await interaction.reply({ embeds: [embed] });

        await new Promise((resolve) => setTimeout(resolve, time * 1000));

        await interaction.deleteReply();
    },
} as ICommand;
