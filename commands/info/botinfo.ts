import { version } from 'discord.js';
import { ICommand } from 'wokcommands';
import { version as doobversion } from '../..';
import { getEmote } from '../../utils/emotes';
import { doobEmbed } from '../../utils/generic_embeds';

export default {
    category: 'info',
    name: 'botinfo',
    description: 'get info about the bot, and the infrestructure running it',

    testOnly: true,
    slash: true,

    callback: ({ client, instance }) => {
        const bot_owners = instance.botOwner.map((owner: any) => {
            return `<@${owner}>`;
        });
        const tab = `${getEmote('transparentSpace')}${getEmote('transparent>')}`;

        const description =
            `**doob info!**` +
            `\n-------------------------------------------\n` +
            `**${getEmote('greyMisc')} description:**\n` +
            `${tab} a bot with moderation, logging, fun commands, and integrations with your favorite services!\n` +
            `**${getEmote('pinkPerson')} developers:**\n` +
            `${tab} ${bot_owners.join(', ')}\n` +
            `**${getEmote('pinkBot')} server count:**\n` +
            `${tab} ${client.guilds.cache.size}\n` +
            `**🏓 api latency:**\n` +
            `${tab} ${Math.round(client.ws.ping)}ms\n` +
            `**📚 library:**\n` +
            `${tab} discord.js ${version}\n` +
            `**${getEmote('pink!')} bot version:**\n` +
            `${tab} ${doobversion}\n` +
            `**${getEmote('pinkLink')} top.gg link**\n` +
            `${tab} https://top.gg/bot/680606346952966177\n` +
            `**🧑‍💻 github repo:**\n` +
            `${tab} https://github.com/doobdev/doob\n` +
            `**${getEmote('green+')} patreon/ko-fi**\n` +
            `${tab} https://ko-fi.com/mmatt || https://patreon.com/doobdev`;
        return doobEmbed(description, null, client.user?.avatarURL());
    },
} as ICommand;
