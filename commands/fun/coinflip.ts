import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'coinflip',
    description: 'Flip a coin!',
    usage: 'coinflip',
    category: 'Fun',

    slash: true,
    testOnly: true,

    callback: ({}) => {
        const coin = Math.floor(Math.random() * 2) === 0 ? 'Heads' : 'Tails'; // I'm not even going to lie, GitHub Copilot just did this for me lol

        let embed = new MessageEmbed().setDescription(`${getEmote('transparent>')} ${coin}!`).setColor(getDoobColor('DOOB'));
        return embed;
    },
} as ICommand;
