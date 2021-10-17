import DiscordJS, { Intents } from 'discord.js';
import WOKCommands from 'wokcommands';
import path from 'path';
import dotenv from 'dotenv';
import { getDoobColor } from './utils/colors';
import Statcord from 'statcord.js';
dotenv.config();

const version = '3.0.0 [BETA]';

const client = new DiscordJS.Client({
    intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS],
});
const statcord = new Statcord.Client({
    key: `${process.env.STATCORD_KEY}`,
    client,
    postCpuStatistics: true,
    postMemStatistics: true,
    postNetworkStatistics: true,
});

client.on('ready', () => {
    new WOKCommands(client, {
        commandsDir: path.join(__dirname, 'commands'),
        featuresDir: path.join(__dirname, 'features'),
        typeScript: true,
        testServers: ['702352937980133386', '815021537303986176'],
        mongoUri: process.env.MONGO_URI,
        disabledDefaultCommands: ['language'],
        defaultLanguage: 'english',
        ignoreBots: true,
        delErrMsgCooldown: 5,
        dbOptions: { keepAlive: true },
        botOwners: ['308000668181069824'],
    })
        .setDefaultPrefix('d!')
        // @ts-ignore
        .setColor(getDoobColor('DOOB'))
        .setCategorySettings([
            {
                name: 'API',
                emoji: '🔗',
            },
            {
                name: 'Fun',
                emoji: '🎲',
            },
            {
                name: 'Info',
                emoji: 'ℹ️',
            },
            {
                name: 'Logging',
                emoji: '📋',
            },
            {
                name: 'Meta',
                emoji: '💫',
            },
            {
                name: 'Misc',
                emoji: '💠',
            },
        ])
        .setDisplayName('Doob');

    console.log(`Doob ${version} is ready!`);
    client.user?.setPresence({
        status: 'online',
        activities: [
            {
                name: `Doob ${version}`,
            },
        ],
    });
    statcord.autopost();
});

statcord.on('autopost-start', () => {
    // Emitted when statcord autopost starts
    console.log('Started Statcord autopost');
});

client.login(process.env.TOKEN);
