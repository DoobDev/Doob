import { ICommand } from 'wokcommands';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    category: 'misc',
    name: 'simremove',
    description: 'simulate a user removal',

    ownerOnly: true,
    slash: false,

    callback: ({ client, member }) => {
        client.emit('guildMemberRemove', member);
        return doobEmbed('simulated a guild member remove event');
    },
} as ICommand;
