import { ICommand } from 'wokcommands';

export default {
    name: 'ping',
    description: 'Ping the bot',
    usage: 'ping',
    category: 'Misc',

    slash: true,
    testOnly: true,

    callback: ({}) => {
        return `🏓 Pong!`;
    },
} as ICommand;
