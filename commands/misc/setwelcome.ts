import { ICommand } from 'wokcommands';
import welcomeSchema from '../../models/welcome-schema';
import { DiscordOption } from '../../utils/discordoptions';

export default {
    name: 'setwelcome',
    description: 'Set a welcome channel + message for your server',
    category: 'Misc',

    permissions: ['ADMINISTRATOR'],

    minArgs: 2,
    expectedArgs: '<channel> <text>',

    slash: true,
    testOnly: true,
    guildOnly: true,

    options: [
        {
            name: 'channel',
            description: 'The channel you want your new members to be welcomed in.',
            type: DiscordOption('CHANNEL'),
            required: true,
        },
        {
            name: 'text',
            description: 'The message to welcome your members. Use the `<user>` variable to mention the user joining.',
            type: DiscordOption('STRING'),
            required: true,
        },
    ],

    callback: async ({ guild, interaction }) => {
        const target = interaction.options.getChannel('channel');

        if (!guild) {
            return 'Error: Running a guild only command in a Direct Message';
        }

        if (!target || target.type !== 'GUILD_TEXT') {
            return 'Error: Incorrect channel type.';
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
                upset: true,
            }
        );

        return 'Welcome channel has been set.';
    },
} as ICommand;
