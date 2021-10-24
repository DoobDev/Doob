import axios from 'axios';
import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'dogfact',
    description: 'get a random dog fact',
    usage: 'dogfact',
    category: 'fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: async ({}) => {
        try {
            let data = (await axios.get('https://some-random-api.ml/facts/dog')) as any;
            const embed = doobEmbed(`${getEmote('transparent>')} ${data.data.fact}`);
            return embed;
        } catch (error) {
            const embed = errorEmbed(
                `an error occured while trying to get a dog image.\n${getEmote('transparentSpace')}${getEmote('transparent>')} ${error}`
            );

            return embed;
        }
    },
} as ICommand;
