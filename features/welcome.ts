import { Client, TextChannel } from 'discord.js';
import welcomeSchema from '../models/welcome-schema';

const welcomeData = {} as {
    // Guild ID  : [channel    , message]
    [key: string]: [TextChannel, string];
};

export default (client: Client) => {
    client.on('guildMemberAdd', async (member) => {
        const { guild, id } = member;

        let data = welcomeData[guild.id];

        if (!data) {
            const results = await welcomeSchema.findById(guild.id);

            if (!results) {
                return; // If no welcome message/channel set, return.
            }

            const { channelId, text } = results;
            const channel = guild.channels.cache.get(channelId) as TextChannel;
            data = welcomeData[guild.id] = [channel, text];
        }

        data[0].send({
            content: data[1].replace(/<user>/g, `<@${id}>`),
        });
    });
};

export const config = {
    displayName: 'welcome members',
    dbName: 'WELCOME_MEMBER', // Database Name, DO NOT CHANGE.
};
