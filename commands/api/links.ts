import { ICommand } from 'wokcommands';
import { DiscordOption } from '../../utils/discordoptions';
import axios from 'axios';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';
import { getEmote } from '../../utils/emotes';
import { TextChannel } from 'discord.js';

export default {
    name: 'shortenlink',
    description: 'shorten a link using doob.link',
    category: 'api',

    options: [
        {
            name: 'link',
            description: 'link to shorten',
            required: true,
            type: DiscordOption('STRING'),
        },
        {
            name: 'vanity',
            description: 'custom url ending',
            required: false,
            type: DiscordOption('STRING'),
        },
    ],

    slash: true,
    testOnly: true,
    minArgs: 1,
    expectedArgs: '<link> <vanity>',

    callback: async ({ client, interaction }) => {
        const link = interaction.options.getString('link');
        const vanity = interaction.options.getString('vanity');
        let resp;
        try {
            resp = (await axios.post(
                'https://api.rebrandly.com/v1/links',
                {
                    destination: link,
                    domain: { fullName: 'doob.link' },
                    slashtag: vanity,
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        apikey: `${process.env.REBRANDLY_API_KEY}`,
                        workspace: `${process.env.REBRANDLY_WORKSPACE}`,
                    },
                }
            )) as any;
        } catch (err) {
            return errorEmbed(`short link api returned an error\n${getEmote('transparentSpace')}${getEmote('transparent>')} ${err}`);
        }

        if (resp.data.shortUrl) {
            const logging_guild = client.guilds.cache.get('702352937980133386');
            const logging_channel = logging_guild?.channels.cache.get('843657332083654726') as TextChannel;

            logging_channel?.send({
                content: `<@308000668181069824>`,
                embeds: [
                    doobEmbed(
                        `new short link!\nfrom <@${interaction.member?.user.id}> (username: ${interaction.member?.user.username}#${interaction.member?.user.discriminator} // id: \`${interaction.member?.user.id}\`)\nshort link: https://${resp.data.shortUrl}\nlong link: ${link}`
                    ),
                ],
            });
            return doobEmbed(`boom! link shortened: [${getEmote('pinkLink')}](https://${resp.data.shortUrl}) https://${resp.data.shortUrl}`);
        }
    },
} as ICommand;
