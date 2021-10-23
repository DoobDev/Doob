import { ICommand } from 'wokcommands';
import { getEmote } from '../../utils/emotes';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    name: 'patreon',
    description: 'get the link to the patreon page',
    usage: 'patreon',
    category: 'meta',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({}) => {
        const embed = doobEmbed(`${getEmote('pinkStar')} donate to Doob and get perks! https://patreon.com/doobdev/ ${getEmote('pinkStar')}`);

        return embed;
    },
} as ICommand;
