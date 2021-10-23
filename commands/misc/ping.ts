import { ICommand } from 'wokcommands';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    name: 'ping',
    description: 'ping the bot',
    usage: 'ping',
    category: 'misc',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({}) => {
        return doobEmbed(`🏓 pong!`);
    },
} as ICommand;
