import { ICommand } from 'wokcommands';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    category: 'misc',
    name: 'setstatus',
    description: 'set the bots status [OWNER ONLY]',

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

        return doobEmbed(`changed status to \`${text}\`.`);
    },
} as ICommand;
