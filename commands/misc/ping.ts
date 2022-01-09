import { ICommand } from 'wokcommands';
import { getEmote } from '../../utils/emotes';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    name: 'ping',
    description: 'ping the bot',
    usage: 'ping',
    category: 'misc',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: ({ interaction, client }) => {
        return doobEmbed(
            `🏓 pong!` +
                `\n${getEmote('transparentSpace')}${getEmote('transparent>')}message latency: ${Date.now() - interaction.createdTimestamp}ms.` +
                `\n${getEmote('transparentSpace')}${getEmote('transparent>')}api latency: ${Math.round(client.ws.ping)}ms`
        );
    },
} as ICommand;
