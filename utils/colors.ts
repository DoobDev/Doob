export function getDoobColor(color: string) {
    let colorName = color.toUpperCase();
    let colorOptions: any = {
        SUCCESS: 0x8fff94,
        DANGER: 0xff8f8f,
        WARNING: 0xf09d59,
        DOOB: 0xff99fa,
    };

    return colorOptions[colorName] || 0xff99fa;
}
