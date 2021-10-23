import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { DiscordOption } from '../../utils/discordoptions';
import { getEmote } from '../../utils/emotes';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    name: 'coinfliptimes',
    description: 'flip a coin x amount of times.',
    usage: 'coinfliptimes <amount: int>',
    category: 'fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    options: [
        {
            name: 'amount',
            description: 'the amount of times to flip the coin.',
            required: true,
            type: DiscordOption('INTEGER'),
        },
    ],

    callback: ({ text }) => {
        let amount = parseInt(text);

        let heads = 0;
        let tails = 0;

        if (amount > 1000) {
            amount = 1000;
        } else {
            amount = amount;
        }

        for (let i = 0; i < amount; i++) {
            const flip = Math.random() >= 0.5 ? 'heads' : 'tails';

            if (flip === 'heads') {
                heads++;
            } else {
                tails++;
            }
        }
        // GitHub Copilot took it to ten
        let embed = doobEmbed(`${getEmote('transparent>')} ${heads} heads and ${tails} tails.`);

        return embed;
    },
} as ICommand;
