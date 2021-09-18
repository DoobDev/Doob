import axios from 'axios';
import { MessageEmbed } from 'discord.js';
import { ICommand } from 'wokcommands';
import { getDoobColor } from '../../utils/colors';
import { getEmote } from '../../utils/emotes';

export default {
    name: 'dog',
    description: 'Sends a random dog image',
    usage: 'dog',
    category: 'Fun',

    slash: true,
    testOnly: true,
    guildOnly: true,

    callback: async ({}) => {
        try {
            let resp = await axios.get('https://dog.ceo/api/breeds/image/random');
            const embed = new MessageEmbed().setImage(resp.data.message).setColor(getDoobColor('DOOB'));
            return embed;
        } catch (error) {
            const embed = new MessageEmbed()
                .setDescription(
                    `${getEmote('red!')} An error occured while trying to get a dog image.\n${getEmote('transparentSpace')}${getEmote(
                        'transparent>'
                    )} ${error}`
                )
                .setColor(getDoobColor('DANGER'));
            return embed;
        }
    },
} as ICommand;
