import { ICommand } from 'wokcommands';
import { DiscordOption } from '../../utils/discordoptions';
import welcomeSchema from '../../models/welcome-schema';

export default {
    name: 'setwelcome',
    description: 'Set the welcome message for the server',
    category: 'config',

    permissions: ['ADMINISTRATOR'],

    minArgs: 2,
    expectedArgs: '<channel> <text>',

    testOnly: true,
    slash: true,

    options: [
        {
            name: 'channel',
            description: 'The channel to set the welcome message in',
            required: true,
            type: DiscordOption('CHANNEL'),
        },
        {
            name: 'text',
            description: 'The text to set the welcome message to',
            required: true,
            type: DiscordOption('STRING'),
        },
    ],

    callback: async ({ guild, interaction }) => {
        if (!guild) {
            return 'This command only works in a server.';
        }

        const target = interaction.options.getChannel('channel');

        if (!target || target.type !== 'GUILD_TEXT') {
            return 'Please use a Text Channel.';
        }

        let text = interaction.options.getString('text');

        await welcomeSchema.findOneAndUpdate(
            {
                _id: guild.id,
            },
            {
                _id: guild.id,
                channelId: target.id,
                text: text,
            },
            {
                upsert: true,
            }
        );

        return 'Welcome Message has been set!';
    },
} as ICommand;
