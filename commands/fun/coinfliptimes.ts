import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { DiscordOption } from '../../utils/discordoptions';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'coinfliptimes',
    description: 'Flip a coin x amount of times.',
    usage: 'coinfliptimes <amount: int>',
    category: 'Fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    options: [
        {
            name: 'amount',
            description: 'The amount of times to flip the coin.',
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
        let embed = new MessageEmbed()
            .setDescription(`${getEmote('transparent>')} ${heads} heads and ${tails} tails.`)
            .setColor(getDoobColor('DOOB'));

        return embed;
    },
} as ICommand;
