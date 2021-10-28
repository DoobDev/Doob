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
            // posts to the `rebrandly` api to shorten the given url
            resp = (await axios.post(
                'https://api.rebrandly.com/v1/links',
                {
                    destination: link,
                    domain: { fullName: 'doob.link' }, // domain linked to rebrandly
                    slashtag: vanity,
                },
                {
                    headers: {
                        'Content-Type': 'application/json',
                        apikey: `${process.env.REBRANDLY_API_KEY}`, // api key in your rebrandly account settings
                        workspace: `${process.env.REBRANDLY_WORKSPACE}`, // get this by going to `workspaces` -> click on your workspace -> id is in the url
                    },
                }
            )) as any;
        } catch (err) {
            return errorEmbed(`short link api returned an error\n${getEmote('transparentSpace')}${getEmote('transparent>')} ${err}`);
        }

        // doob.link logging
        // sends a message everytime someone shortens a link, just to moderate for abuse
        if (resp.data.shortUrl) {
            const logging_guild = client.guilds.cache.get('702352937980133386'); // TODO: make this a config value or an environment variable
            const logging_channel = logging_guild?.channels.cache.get('843657332083654726') as TextChannel; // TODO: same as above

            logging_channel?.send({
                content: `<@308000668181069824>`, // TODO: grab owner IDs from WOKCommands
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
