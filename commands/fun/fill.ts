import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { DiscordOption } from '../../utils/discordoptions';
import { getEmote } from '../../utils/emotes';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'fill',
    description: 'Fill the message with something.',
    category: 'Fun',
    cooldown: '30s',

    testOnly: true,

    slash: true,
    minArgs: 1,
    expectedArgs: '<string>',
    options: [
        {
            name: 'string',
            description: 'The string to fill the message with.',
            type: DiscordOption('STRING'),
            required: true,
        },
    ],

    callback: ({ interaction }) => {
        let string = interaction.options.getString('string');

        if (!string) {
            return errorEmbed('string argument empty.');
        }

        while (string.length < 500) {
            string += ` ${string}`;
        }

        const embed = doobEmbed(string);

        return embed;
    },
} as ICommand;
