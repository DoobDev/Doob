import { Client } from 'discord.js';
import afkSchema from '../models/afk-schema';

export default (client: Client) => {
    client.on('messageCreate', async (message) => {
        const { channel, author } = message;
        const results = await afkSchema.findById(author.id);

        if (!results) {
            return;
        } else {
            console.log(results);
            channel.send({
                content: 'fdm',
            });
        }
    });
};

export const config = {
    displayName: 'welcome members',
    dbName: 'WELCOME_MEMBER', // Database Name, DO NOT CHANGE.
};
