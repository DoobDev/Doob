export function getDoobColor(color: string) {
    const colorName = color;

    let colorOptions = [
        { color: 'SUCCESS', hex: 0x5ef059 },
        { color: 'DANGER', hex: 0xf05959 },
        { color: 'WARNING', hex: 0xf09d59 },
        { color: 'DOOB', hex: 0xff99fa },
    ];

    return colorOptions.find((e) => e.color === colorName)?.hex || '';
}
