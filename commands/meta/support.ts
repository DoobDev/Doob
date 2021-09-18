import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'support',
    description: 'Get support for the bot in our official support server!',
    usage: 'support',
    category: 'Meta',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({}) => {
        let embed = new MessageEmbed()
            .setDescription(
                `${getEmote('pinkStar')} Get help at our Support Server\n${getEmote('transparent>')} https://discord.gg/hgQTTU7 [${getEmote(
                    'pinkLink'
                )}](https://discord.gg/hgQTTU7)`
            )
            .setColor(getDoobColor('DOOB'));

        return embed;
    },
} as ICommand;
