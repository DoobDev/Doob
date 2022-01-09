import { ICommand } from 'wokcommands';

export default {
    category: 'misc',
    description: 'simulate a join',

    slash: false,
    ownerOnly: true,

    callback: ({ member, client }) => {
        client.emit('guildMemberAdd', member);
        return 'Emited guildMemberAdd';
    },
} as ICommand;
