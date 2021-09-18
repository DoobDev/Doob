import axios from 'axios';
import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'dogfact',
    description: 'Get a random dog fact',
    usage: 'dogfact',
    category: 'Fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: async ({}) => {
        try {
            let data = await axios.get('https://some-random-api.ml/facts/dog');
            const embed = new MessageEmbed().setDescription(`${getEmote('transparent>')} ${data.data.fact}`).setColor(getDoobColor('DOOB'));
            return embed;
        } catch (error) {
            return `An error occurred: ${error}`;
        }
    },
} as ICommand;
