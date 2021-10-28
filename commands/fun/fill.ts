import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { DiscordOption } from '../../utils/discordoptions';
import { getEmote } from '../../utils/emotes';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'fill',
    description: 'fill the message with something.',
    category: 'fun',
    cooldown: '30s',

    testOnly: true,

    slash: true,
    minArgs: 1,
    expectedArgs: '<string>',
    options: [
        {
            name: 'string',
            description: 'the string to fill the message with.',
            type: DiscordOption('STRING'),
            required: true,
        },
    ],

    callback: ({ interaction }) => {
        let string = interaction.options.getString('string');

        if (!string) {
            return errorEmbed('string argument empty.');
        }
        // TODO: make this      v  guild configurable
        // maybe with addition of automod/max msg length?
        while (string.length < 500) {
            string += ` ${string}`;
        }

        const embed = doobEmbed(string);

        return embed;
    },
} as ICommand;
