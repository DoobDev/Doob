import axios from 'axios';
import { ICommand } from 'wokcommands';
import { getEmote } from '../../utils/emotes';
import { doobEmbed, errorEmbed } from '../../utils/generic_embeds';

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
            let resp = (await axios.get('https://dog.ceo/api/breeds/image/random')) as any;
            const text = '';
            const embed = doobEmbed(text, null, resp.data.message);
            return embed;
        } catch (error) {
            const embed = errorEmbed(
                `an error occured while trying to get a dog image.\n${getEmote('transparentSpace')}${getEmote('transparent>')} ${error}`
            );
            return embed;
        }
    },
} as ICommand;
