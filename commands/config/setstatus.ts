import { ICommand } from 'wokcommands';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    category: 'config',
    name: 'setstatus',
    description: 'set the bots status [OWNER ONLY]',

    minArgs: 1,
    expectedArgs: '<status>',

    slash: false,
    testOnly: true,

    ownerOnly: true, // owner only command (keep)

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
