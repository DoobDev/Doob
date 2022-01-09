import { Webhook } from '@top-gg/sdk';
import DiscordJS, { Intents } from 'discord.js';
import express from 'express';
import path from 'path';
import { AutoPoster } from 'topgg-autoposter';
import WOKCommands from 'wokcommands';
import config from './config';
import { getDoobColor } from './utils/colors';

const WEBHOOK_PORT = config.webhookPort || 80;

const webhook_server = express();

export const version = '3.0.0 [BETA]'; // The version the bot is running on, edit this on every release.

const client = new DiscordJS.Client({
    intents: [Intents.FLAGS.GUILDS, Intents.FLAGS.GUILD_MESSAGES, Intents.FLAGS.GUILD_MESSAGE_REACTIONS],
    // Enables intents for `Guilds`, `Guild Messages` and `Reactions from Guild Message`
});

let typeScript_bool: boolean | undefined = undefined;

if (!config.devMode) {
    // Top.gg Auto post stats
    const topgg_ap = AutoPoster(config.topggKey, client);

    topgg_ap.on('posted', () => {
        console.log('stats have been posted to top.gg');
    });

    typeScript_bool = false;
} else {
    typeScript_bool = true;
}

client.on('ready', () => {
    new WOKCommands(client, {
        commandsDir: path.join(__dirname, 'commands'), // Directory where commands are stored
        featuresDir: path.join(__dirname, 'features'), // Directory where features (event listeners pretty much) are stored
        typeScript: typeScript_bool, // This is disabled when running for prod, otherwise while testing it is enabled.
        testServers: ['702352937980133386', '815021537303986176'], // The two Doob test servers  (70... is the Doob Dev server, 815... is a private test server)
        mongoUri: config.mongoUri, // MongoDB connection string (Stored as MONGO_URI in .env)
        disabledDefaultCommands: ['language'], // Disabled the language command in WOKCommands, I don't plan to support different languages until later.
        defaultLanguage: 'english', // Default language for Doob is English.
        ignoreBots: true, // WOKCommands ignores other Discord Bots, for no echoing of commands and such.
        delErrMsgCooldown: 5, // After 5 seconds, the default WOKCommands error messages delete.
        dbOptions: { keepAlive: true },
        botOwners: ['308000668181069824'], // For owner only commands (3080... is mmatt)
    })
        .setDefaultPrefix('d!') // Default prefix for legacy commands (which most are not used for the public) is d!
        // @ts-ignore
        .setColor(getDoobColor.DOOB) // Default color for embeds like d!help
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
            {
                name: 'moderation',
                emoji: '🔨',
            },
        ])
        .setDisplayName('Doob');

    console.log(`Doob ${version} is ready!`);
    client.user?.setPresence({
        status: 'online',
        activities: [
            {
                name: `doob ${version} || server count: ${client.guilds.cache.size}`,
            },
        ],
    });
});

if (!config.devMode) {
    // Top.gg Webhook integration
    const webhook = new Webhook(config.webhookAuth);
    webhook_server.post(
        '/dblwebhook',
        webhook.listener((vote: { user: any }) => {
            console.log(vote.user);
        })
    );

    webhook_server.get('/', (req, res) => {
        res.sendStatus(200);
    });

    webhook_server.listen(WEBHOOK_PORT);
    console.log(`Webhook server listening on port ${WEBHOOK_PORT}`);
}

client.login(config.discordToken);
