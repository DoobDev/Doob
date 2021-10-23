import axios from 'axios';
import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';
import { errorEmbed } from '../../utils/generic_embeds';

export default {
    name: 'dog',
    description: 'sends a random dog image',
    usage: 'dog',
    category: 'fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: async ({}) => {
        try {
            let resp = await axios.get('https://dog.ceo/api/breeds/image/random');
            const embed = new MessageEmbed().setImage(resp.data['message']).setColor(getDoobColor('DOOB'));
            return embed;
        } catch (error) {
            const embed = errorEmbed(
                `an error occured while trying to get a dog image.\n${getEmote('transparentSpace')}${getEmote('transparent>')} ${error}`
            );
            return embed;
        }
    },
} as ICommand;
