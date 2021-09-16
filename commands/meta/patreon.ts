import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'patreon',
    description: 'Get the link to the patreon page',
    usage: 'patreon',
    category: 'Meta',

    slash: true,
    testOnly: true,

    callback: ({}) => {
        const embed = new MessageEmbed()
            .setDescription(`${getEmote('pinkStar')} Donate to Doob and get perks! https://patreon.com/doobdev/ ${getEmote('pinkStar')}`)
            // @ts-ignore
            .setColor(getDoobColor('DOOB'));

        return embed;
    },
} as ICommand;
