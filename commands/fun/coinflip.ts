import { ICommand } from 'wokcommands';
import { getEmote } from '../../utils/emotes';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    name: 'coinflip',
    description: 'flip a coin!',
    usage: 'coinflip',
    category: 'fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({}) => {
        const coin = Math.floor(Math.random() * 2) === 0 ? 'heads' : 'tails'; // i'm not even going to lie, GitHub Copilot just did this for me lol

        let embed = doobEmbed(`${getEmote('transparent>')} ${coin}!`);
        return embed;
    },
} as ICommand;
