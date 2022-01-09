import { ICommand } from 'wokcommands';
import { doobEmbed } from '../../utils/generic_embeds';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'invite',
    description: 'invite the bot to your server.',
    category: 'meta',

    slash: true,
    testOnly: true,

    callback: ({}) => {
        return doobEmbed(`invite doob to your server ${getEmote('pinkLink')} https://doob.link/invite`);
    },
} as ICommand;
