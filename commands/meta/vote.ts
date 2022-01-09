import { ICommand } from 'wokcommands';
import { getEmote } from '../../utils/emotes';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    name: 'vote',
    description: 'Vote for the bot on Top.gg',
    usage: 'vote',
    category: 'meta',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({}) => {
        const embed = doobEmbed(`${getEmote('^')} vote for Doob on Top.gg https://doob.link/votedoob ${getEmote('pinkStar')}`);

        return embed;
    },
} as ICommand;
