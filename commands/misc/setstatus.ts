import { ICommand } from 'wokcommands';

export default {
    category: 'Misc',
    name: 'setstatus',
    description: 'Set the bots status [OWNER ONLY]',

    minArgs: 1,
    expectedArgs: '<status>',

    slash: false,
    testOnly: true,

    ownerOnly: true,

    callback: ({ client, text }) => {
        client.user?.setPresence({
            status: 'online',
            activities: [
                {
                    name: text,
                },
            ],
        });

        return `Changed status to \`${text}\`.`;
    },
} as ICommand;
