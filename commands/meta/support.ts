import { ICommand } from 'wokcommands';
import { getEmote } from '../../utils/emotes';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    name: 'support',
    description: 'get support for the bot in our official support server!',
    usage: 'support',
    category: 'meta',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({}) => {
        const embed = doobEmbed(
            `${getEmote('pinkStar')} get help at our support server\n${getEmote('transparent>')} https://doob.link/supportserver`
        );

        return embed;
    },
} as ICommand;
