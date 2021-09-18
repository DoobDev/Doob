import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'vote',
    description: 'Vote for the bot on Top.gg',
    usage: 'vote',
    category: 'Meta',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({}) => {
        const embed = new MessageEmbed()
            .setDescription(`${getEmote('^')} Vote for Doob on Top.gg https://top.gg/bot/680606346952966177/vote ${getEmote('pinkStar')}`)
            .setColor(getDoobColor('DOOB'));

        return embed;
    },
} as ICommand;
