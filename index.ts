import DiscordJS, { Intents } from 'discord.js';
import WOKCommands from 'wokcommands';
import path from 'path';
import dotenv from 'dotenv';
import { getDoobColor } from './utils/colors';
import Statcord from 'statcord.js';
dotenv.config();

const version = '3.0.0 [BETA]'; // The version the bot is running on, edit this on every release.

const client = new DiscordJS.Client({
    intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS],
    // Enables intents for `Guilds`, `Guild Messages` and `Reactions from Guild Message`
});
const statcord = new Statcord.Client({
    // Statistics client for statcord.com
    key: `${process.env.STATCORD_KEY}`,
    client,
    postCpuStatistics: true,
    postMemStatistics: true,
    postNetworkStatistics: true,
});

client.on('ready', () => {
    new WOKCommands(client, {
        commandsDir: path.join(__dirname, 'commands'), // Directory where commands are stored
        featuresDir: path.join(__dirname, 'features'), // Directory where features (event listeners pretty much) are stored
        typeScript: true, // Enabled because Doob v3 uses Typescript
        testServers: ['702352937980133386', '815021537303986176'], // The two Doob test servers  (70... is the Doob Dev server, 815... is a private test server)
        mongoUri: process.env.MONGO_URI, // MongoDB connection string (Stored as MONGO_URI in .env)
        disabledDefaultCommands: ['language'], // Disabled the language command in WOKCommands, I don't plan to support different languages until later.
        defaultLanguage: 'english', // Default language for Doob is English.
        ignoreBots: true, // WOKCommands ignores other Discord Bots, for no echoing of commands and such.
        delErrMsgCooldown: 5, // After 5 seconds, the default WOKCommands error messages delete.
        dbOptions: { keepAlive: true },
        botOwners: ['308000668181069824'], // For owner only commands (3080... is mmatt)
    })
        .setDefaultPrefix('d!') // Default prefix for legacy commands (which most are not used for the public) is d!
        // @ts-ignore
        .setColor(getDoobColor('DOOB')) // Default color for embeds like d!help
        .setCategorySettings([
            {
                name: 'api',
                emoji: '🔗',
            },
            {
                name: 'fun',
                emoji: '🎲',
            },
            {
                name: 'info',
                emoji: 'ℹ️',
            },
            {
                name: 'meta',
                emoji: '💫',
            },
            {
                name: 'misc',
                emoji: '💠',
            },
            {
                name: 'config',
                emoji: '🔧',
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
