import { ICommand } from 'wokcommands';
import welcomeSchema from '../../models/welcome-schema';
import { DiscordOption } from '../../utils/discordoptions';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'setwelcome',
    description: 'set a welcome channel + message for your server',
    category: 'config',

    permissions: ['ADMINISTRATOR'],

    minArgs: 2,
    expectedArgs: '<channel> <text>',

    slash: true,
    testOnly: true,
    guildOnly: true,

    options: [
        {
            name: 'channel',
            description: 'the channel you want your new members to be welcomed in.',
            type: DiscordOption('CHANNEL'),
            required: true,
        },
        {
            name: 'text',
            description: 'the message to welcome your members. use the `<user>` variable to mention the user joining.',
            type: DiscordOption('STRING'),
            required: true,
        },
    ],

    callback: async ({ guild, interaction }) => {
        const target = interaction.options.getChannel('channel');

        if (!guild) {
            return errorEmbed('this command can only be ran in servers');
        }

        // error handling just in case a user tries to make a welcome channel a `voice/anything that isn't text` channel.
        if (!target || target.type !== 'GUILD_TEXT') {
            return errorEmbed('incorrect channel type.');
        }

        let text = interaction?.options.getString('text');

        await welcomeSchema.findOneAndUpdate(
            {
                _id: guild.id,
            },
            {
                _id: guild.id,
                text,
                channelId: target.id,
            },
            {
                upsert: true,
            }
        );

        return doobEmbed('welcome channel has been set.');
    },
} as ICommand;
