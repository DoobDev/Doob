import { MessageEmbed } from 'discord.js';
import { getDoobColor } from './colors';
import { getEmote } from './emotes';

export function errorEmbed(text: string) {
    const embed = new MessageEmbed()
        .setDescription(`${getEmote('red!')} ERR: ${text}`)
        .setColor(getDoobColor.DANGER)
        .setFooter(`🛑 make sure to join the support server to report this error.`);
    return embed as MessageEmbed;
}

export function doobEmbed(text: string, color?: number | null, image?: string | null) {
    const embed = new MessageEmbed().setDescription(text).setColor(color || getDoobColor.DOOB);

    if (image) {
        embed.setThumbnail(image);
    }

    return embed as MessageEmbed;
}
