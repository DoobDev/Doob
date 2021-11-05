/**
 * get emotes that doob uses in discord embeds
 * @param emote the emote you want to get
 * @returns the emote code for discord.
 */
export function getEmote(emote: string): string {
    const emoteName = emote;

    let emotes = [
        { name: 'transparentSpace', emote: '<:Dspace:869830848743092247>' },
        {
            name: 'redAccessDenied',
            emote: '<:DAccessDenied:869815358758985779>',
        },
        {
            name: 'greyBot',
            emote: '<:Dbot:869815359652397076>',
        },
        {
            name: 'greyMap',
            emote: '<:Dmap:869815361594343454>',
        },
        {
            name: 'greyClock',
            emote: '<:Dclock:869815363003613234>',
        },
        {
            name: 'grey!',
            emote: '<:Dexclaim:869815363238498344>',
        },
        {
            name: 'greyMisc',
            emote: '<:Dmisc:869815363276243006>',
        },
        {
            name: 'greyLink',
            emote: '<:Dlinkgrey:869815363381125180>',
        },
        {
            name: 'grey?',
            emote: '<:Dquestion:869815363779579924>',
        },
        {
            name: 'greyCog',
            emote: '<:Dsettings:869815363838304316>',
        },
        {
            name: 'redCheck',
            emote: '<:Dcheckneg:869815364110913566>',
        },
        {
            name: 'greyStar',
            emote: '<:Dstar:869815364148666368>',
        },
        {
            name: 'greenCheck',
            emote: '<:Dcheckpos:869815364278702080>',
        },
        {
            name: 'redCross',
            emote: '<:Dcrossneg:869815364383572059>',
        },
        {
            name: 'greyWrench',
            emote: '<:Dwrench:869815364576481330>',
        },
        {
            name: 'pinkMap',
            emote: '<:Dmappink:869815364731678762>',
        },
        {
            name: 'red!',
            emote: '<:Dexclaimneg:869815364828160070>',
        },
        {
            name: 'greenPlay',
            emote: '<:Dplaypos:869815364828160074>',
        },
        {
            name: 'redMod',
            emote: '<:Dmodneg:869815364933013516>',
        },
        {
            name: 'green+',
            emote: '<:Dplus:869815365025271829>',
        },
        {
            name: 'pinkBot',
            emote: '<:Dbotpink:869815365071413258>',
        },
        {
            name: 'pinkShare',
            emote: '<:Dshare:869815365142740994>',
        },
        {
            name: 'redPlay',
            emote: '<:Dplayneg:869815365155319870>',
        },
        {
            name: 'redStar',
            emote: '<:Dstarneg:869815365285326873>',
        },
        {
            name: 'redTrash',
            emote: '<:Dtrashcan:869815365323079733>',
        },
        {
            name: 'pinkMsg',
            emote: '<:Ddmsgpink:869815365616664579>',
        },
        {
            name: 'green!',
            emote: '<:Dexclaimpos:869815365708955770>',
        },
        {
            name: 'greenCross',
            emote: '<:Dcrosspos:869815366002556928>',
        },
        {
            name: 'pinkHeart',
            emote: '<:Dheart:869815366132576286>',
        },
        {
            name: 'pinkPlay',
            emote: '<:Dplaypink:869815366233251861>',
        },
        {
            name: 'greenMod',
            emote: '<:Dmodpos:869815366300344340>',
        },
        {
            name: 'pinkStar',
            emote: '<:Dstarpink:869815366539419648>',
        },
        {
            name: 'greenStar',
            emote: '<:Dstarpos:869815366577176586>',
        },
        {
            name: 'toggleOff',
            emote: '<:Dtoggleoff:869815366593945640>',
        },
        {
            name: 'greenTicket',
            emote: '<:Dticketpos:869815366631710751>',
        },
        {
            name: 'redUser',
            emote: '<:Duserneg:869815366715580466>',
        },
        {
            name: 'greenWarning',
            emote: '<:Dwarningpos:869815366715584513>',
        },
        {
            name: 'redWarning',
            emote: '<:Dwarningneg:869815366803668992>',
        },
        {
            name: 'greenUser',
            emote: '<:Duserpos:869815366816239626>',
        },
        {
            name: 'pinkClock',
            emote: '<:Dclockpink:869815366816239666>',
        },
        {
            name: 'pink!',
            emote: '<:Dexclaimpink:869815366816260167>',
        },
        {
            name: 'toggleOn',
            emote: '<:Dtoggleon:869815366837223495>',
        },
        {
            name: 'full>',
            emote: '<:Drightfull:869815366841409598>',
        },
        {
            name: '>',
            emote: '<:Dright:869815366874959963>',
        },
        {
            name: 'v',
            emote: '<:Ddown:869815366975623178>',
        },
        {
            name: 'full<',
            emote: '<:Dleftfull:869815366975623179>',
        },
        {
            name: 'pinkLink',
            emote: '<:Dlinkpink:869815367004995604>',
        },
        {
            name: 'pinkMusic',
            emote: '<:Dmusic:869815367030165515>',
        },
        {
            name: '<',
            emote: '<:Dleft:869815367046926376>',
        },
        {
            name: 'Previous',
            emote: '<:Dprevious:869815367051141200>',
        },
        {
            name: 'orangeWarning',
            emote: '<:Dwarning:899150530553724978>',
        },
        {
            name: 'Skip',
            emote: '<:Dskip:899150477411885086>',
        },
        {
            name: '^',
            emote: '<:Dup:899150414363103262>',
        },
        {
            name: 'pinkPerson',
            emote: '<:Dusernuetral:899150442410434571>',
        },
        {
            name: 'pinkWrench',
            emote: '<:Dwrenchpink:899150363633000498>',
        },
        {
            name: 'transparent<',
            emote: '<:DLeftTrans:899150323673870367>',
        },
        {
            name: 'transparent>',
            emote: '<:DRightTrans:899150324034584636>',
        },
        {
            name: 'transparentChar',
            emote: ' ',
        },
    ];

    return emotes.find((e) => e.name === emoteName)?.emote || '';
}
