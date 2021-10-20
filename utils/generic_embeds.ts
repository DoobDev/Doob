import { MessageEmbed } from 'discord.js';
import { getDoobColor } from './colors';
import { getEmote } from './emotes';

export function errorEmbed(text: string) {
    const embed = new MessageEmbed()
        .setDescription(`${getEmote('red!')} ERR: ${text}`)
        .setColor(getDoobColor('DANGER'))
        .setFooter(`🛑 Make sure to join the support server to report this error.`);
    return embed as MessageEmbed;
}

export function doobEmbed(text: string) {
    const embed = new MessageEmbed().setDescription(text).setColor(getDoobColor('DOOB'));
    return embed as MessageEmbed;
}
