export function getDoobColor(color: string) {
    let colorName = color.toUpperCase();
    let colorOptions: any = {
        SUCCESS: 0x5ef059,
        DANGER: 0xf05959,
        WARNING: 0xf09d59,
        DOOB: 0xff99fa,
    };

    return colorOptions[colorName] || 0xff99fa;
}
