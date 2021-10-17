import { ICommand } from 'wokcommands';

export default {
    category: 'Misc',
    description: 'Sim join',

    slash: false,
    testOnly: true,

    callback: ({ member, client }) => {
        client.emit('guildMemberAdd', member);
        return 'Emited guildMemberAdd';
    },
} as ICommand;
