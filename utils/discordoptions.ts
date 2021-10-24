export function DiscordOption(
    options: 'SUB_COMMAND' | 'SUB_COMMAND_GROUP' | 'STRING' | 'INTEGER' | 'BOOLEAN' | 'USER' | 'CHANNEL' | 'ROLE' | 'MENTIONABLE' | 'NUMBER'
) {
    const optionsName = options;

    let discOptions = [
        { type: 'SUB_COMMAND', num: 1 },
        { type: 'SUB_COMMAND_GROUP', num: 2 },
        { type: 'STRING', num: 3 },
        { type: 'INTEGER', num: 4 },
        { type: 'BOOLEAN', num: 5 },
        { type: 'USER', num: 6 },
        { type: 'CHANNEL', num: 7 },
        { type: 'ROLE', num: 8 },
        { type: 'MENTIONABLE', num: 9 },
        { type: 'NUMBER', num: 10 },
    ];

    return discOptions.find((e) => e.type === optionsName)?.num || '';
}
