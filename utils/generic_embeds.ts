import { MessageEmbed } from 'discord.js';
import { getDoobColor } from './colors';
import { getEmote } from './emotes';

/**
 * get the generic error embed
 * @param text the error message to be displayed to the user (required)
 * @returns a message embed with the error message
 */
export function errorEmbed(text: string) {
    const embed = new MessageEmbed()
        .setDescription(`${getEmote('red!')} ERR: ${text}`)
        .setColor(getDoobColor.DANGER)
        .setFooter(`🛑 make sure to join the support server to report this error.`);
    return embed as MessageEmbed;
}

/**
 * get the generic doob embed
 * @param text the text to be displayed to the user in the embed. (required)
 * @param color the color shown to the left side of the embed (optional: defaults to `getDoobColor.DOOB`)
 * @param image the image shown to the right side of the embed (optional: no default) (`setThumbnail` in discord.js)
 * @returns a message embed with the text and optional arguments
 */

export function doobEmbed(text: string, color?: number | null, image?: string | null) {
    const embed = new MessageEmbed().setDescription(text).setColor(color || getDoobColor.DOOB);

    if (image) {
        embed.setThumbnail(image);
    }

    return embed as MessageEmbed;
}
