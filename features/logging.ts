import { Client, TextChannel } from 'discord.js';
import loggingSchema from '../models/logging-schema';
import { getDoobColor } from '../utils/colors';
import { getEmote, tab } from '../utils/emotes';
import { doobEmbed } from '../utils/generic_embeds';

const loggingData = {} as {
    // Guild ID
    [key: string]: [TextChannel];
};

export default (client: Client) => {
    client.on('guildMemberAdd', async (member) => {
        const { guild } = member;

        let data = loggingData[guild.id];

        if (!data) {
            const results = await loggingSchema.findById(guild.id);

            if (!results) {
                return;
            }

            const { channelId } = results;
            const channel = guild.channels.cache.get(channelId) as TextChannel;
            data = loggingData[guild.id] = [channel];
        }

        data[0].send({
            embeds: [
                doobEmbed(
                    `${getEmote('greenUser')} **${member?.nickname || member.user.username} has joined the server.**`,
                    getDoobColor.SUCCESS,
                    member.user?.avatarURL()
                ),
            ],
        });
    });

    client.on('guildMemberRemove', async (member) => {
        const { guild } = member;

        let data = loggingData[guild.id];

        if (!data) {
            const results = await loggingSchema.findById(guild.id);

            if (!results) {
                return;
            }

            const { channelId } = results;
            const channel = guild.channels.cache.get(channelId) as TextChannel;
            data = loggingData[guild.id] = [channel];
        }

        data[0].send({
            embeds: [
                doobEmbed(
                    `${getEmote('redUser')} **${member?.nickname || member.user?.username} has left the server.**`,
                    getDoobColor.DANGER,
                    member.user?.avatarURL()
                ),
            ],
        });
    });

    client.on('messageUpdate', async (oldMessage, newMessage) => {
        const { guild, member } = newMessage;

        if (!guild) {
            return;
        }

        let data = loggingData[guild.id];

        if (!data) {
            const results = await loggingSchema.findById(guild.id);

            if (!results) {
                return;
            }

            const { channelId } = results;
            const channel = guild.channels.cache.get(channelId) as TextChannel;
            data = loggingData[guild.id] = [channel];
        }

        if (oldMessage.content === newMessage.content) {
            return;
        } else if (oldMessage.content === null || oldMessage.content === null) {
            return;
        } else if (oldMessage.content === '' || newMessage.content === '') {
            return;
        } else {
            data[0].send({
                embeds: [
                    doobEmbed(
                        `${getEmote('pinkMsg')} **${member?.nickname || member?.user.username} edited their message.**\n` +
                            `${tab} Old Message: \`${oldMessage.content}\`\n` +
                            `${tab} New Message: \`${newMessage.content}\``
                    ),
                ],
            });
        }
    });

    client.on('messageDelete', async (message) => {
        const { guild, member } = message;

        if (!guild) {
            return;
        }

        let data = loggingData[guild.id];

        if (!data) {
            const results = await loggingSchema.findById(guild.id);

            if (!results) {
                return;
            }

            const { channelId } = results;
            const channel = guild.channels.cache.get(channelId) as TextChannel;
            data = loggingData[guild.id] = [channel];
        }

        if (!message) {
            return;
        } else if (message.content === '@everyone' || '@here') {
            data[0].send({
                embeds: [
                    doobEmbed(
                        `${getEmote('redTrash')} **${member?.nickname || member?.user.username} deleted their ghost ping.**\n` +
                            `${tab} \`${message.content}\``
                    ),
                ],
            });
        }
    });
};

export const config = {
    displayName: 'logging actions',
    dbName: 'LOGGING', // Database Name, DO NOT CHANGE.
};
