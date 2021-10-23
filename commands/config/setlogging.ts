import { ICommand } from 'wokcommands';
import loggingSchema from '../../models/logging-schema';
import { DiscordOption } from '../../utils/discordoptions';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'setlogging2',
    description: 'set the logging channel for your server',
    category: 'config',

    minArgs: 1,
    expectedArgs: '<channel>',

    slash: true,
    testOnly: true,
    guildOnly: true,

    options: [
        {
            name: 'channel',
            description: 'the channel to set as the logging channel',
            type: DiscordOption('CHANNEL'),
            required: true,
        },
    ],

    callback: async ({ interaction, guild }) => {
        const channel = interaction.options.getChannel('channel');

        if (!guild) {
            return errorEmbed('this command can only be ran in servers');
        }

        if (!channel || channel.type !== 'GUILD_TEXT') {
            return errorEmbed('invalid channel provided');
        }

        await loggingSchema.findOneAndUpdate(
            {
                _id: guild.id,
            },
            {
                _id: guild.id,
                channelId: channel.id,
            },
            {
                upsert: true,
            }
        );

        return doobEmbed('logging channel has been set.');
    },
} as ICommand;
