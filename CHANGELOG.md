## v2.1.1
* Added `doob/osu`
    - See your osu! profile!
* Added `doob/setosu`
    - Set your osu! profile for `doob/osu`!

## v2.1.0
* Per-Server XP Leaderboards (`doob/serverleaderboard`)
* Removed `doob/slap`
    - There has been an exploit discovered to ping everyone, decided to go ahead and remove the command, wasn't used at all.
* New `doob/timebomb` command
    - Lets you have a message with a time limit!
* Doob Logging now sends in regular messages instead of embeds.
    - I saw [stageosu/Kaguya](https://github.com/stageosu/kaguya) do this recently, and I love the look of it, go check out Stage's bot, its great :D
* Added `doob/streamlookup` command!
    - Lookup your favorite streamers, see if they are online or not, and if they are online, see information like what game they are playing!
* Added `doob/owstats` command!
    - Check your (or your friends) Overwatch stats in Discord!
* Added `doob/setowusername` command!
    - Add your platform, username, and region to be able to look up your stats on Doob!
        - Only acceptable platforms are `pc` `xbl` and `psn`
        - Only acceptable regions are `us` `eu` or `asia`
        - For battletags, make sure you do `{username}-{numbers}` NOT `{username}#{numbers}`
* Changed around some of the fields on `doob/streamlookup`
* Added `doob/bio` command!
    - Lookup your/your friend's Discord.bio profile in Discord!
* Added `doob/lastfm` command!
    - Lookup your/your friend's Last.fm profiles directly in Discord!
* Added `doob/setlastfm` command!
    - Set your default last.fm username, so you don't have to type your username every time you want to use a Last.fm command.
* Added some Doob emojis to `doob/info`
* `doob/lastfm` only does your profile now.
    - To do other people's do `doob/lastfm search {username}`
* Added `doob/lastfm recent`!
    - See the last 5 songs you or someone else has listened to!
* Added `doob/lastfm top albums`!
    - Get your top 10 most listened to albums on Last.fm
* Added `doob/lastfm artist charts`!
    - See the top 10 artists on Last.fm!
* Added `doob/lastfm top tracks`!
    - See the top 10 tracks you have played on last.fm!
* Added `doob/lastfm top artists`!
    - See the top 10 artists you have played on last.fm!

## v2.0.9
#### The muting update!
* Finally! Doob has muting!
* New `doob/mute` command!
    - Mutes a member from your server!
        - Example: `doob/mute @X Daniel lol`
            - Make sure to set your "Muted Role" by doing `doob/setmutedrole`
* New `doob/unmute` command!
    - Unmutes a member from your server!
        - Example: `doob/unmute @X Daniel`
* Per-Server XP is now avaliable!
* Updated `doob/level` to include Server XP
* Updated `doob/profile` to say "Doob Global XP/Level/Rank".
* Made unmute/mute commands have embeds.
* Fixed Level Messages not working
* Fixed `doob/slc` and `doob/slm` so it no longer shows "None"
* Instead of help messages and such saying `@Doob ` for the prefix, it now says your server's prefix.
* Removed the description for the Among Us Commands.
    * You can still find them in `doob/help {cmd}`
* Added a new Patreon only command! `doob/luckydog`
    * Gives you instant access to all the lucky dog's avaliable.
* Lucky Dog Nitro Giveaways are BACK!
    - Every month, whoever gets the most Lucky Dogs, gets 1 month of Nitro Classic!
* New `doob/luckydogs` command!
    - Check how many lucky dogs you have "caught" over the month.
* Updated `doob/userinfo` "Bot or not" field.
    - "Bot or not." ==> "Bot"
* New `doob/unban` command!
* Starboards!
    - New `doob/setstarboardchannel` command!
* Updated starboard embed to have a "Jump to link"
    - Lets you jump to the message that was starred.
* Really bad `doob/jumpscare` command lol.
* Removed jumpscare
* Lucky Dogs now occur 1/500
* Updated `doob/info` to have system stats.

## v2.0.8
* Updated description (on the help command) for
    - `doob/Leaderboard`
* New `doob/patreon` command!
* Added some debugging for doob/dog
    - It gives me the roll numbers for P_AD and L_DOG if I need to check if it is working or not.
* Default Level Messages are off.
    - This feature is on the live bot now.
* Default error message gives support server.
* `doob/setlevelmessages` now:
    - Tells you if you have level messages on or off if you just type `doob/setlevelmessages`
    - Only sets your level message setting if you type
        - `yes`
        - `Yes`
        - `no`
        - `No`
* `doob/slap` should no longer gives you a Bad Argument error.
    - Instead, it defaults to slapping yourself, silly you!
        - If you try to pass a reason in when doing `doob/slap` with no member found, it says that you accidently slapped yourself instead of the person you meant to slap.
            - This also means it removes the default reason.
                - For instance, instead of it saying "for no reason!" it will just say "Reason - None!"
* `doob/serverinfo` no longer requires server permissions!
    - The reason it needed server permissions last time is because of the "Banned Members" field, if Doob has Administrator permissions in a server, it will still show the "Banned Members" field.
* `doob/prefix` and `doob/setlevelmessages` can no longer be abused to do @everyone pings.
* `doob/setmutedrole` and `doob/setlogchannel` no longer have to be IDs anymore.
    - I believe they now **are required** to be pings.
        - Example: `doob/setmutedrole @Muted` and `doob/setlogchannel #logs`
            - Instead of from 2.0.7 (this is outdated, don't do this anymore.) `doob/setmutedrole {role id}` and `doob/setlogchannel {channel id}`
* Logs have been removed from `doob/kick` and `doob/ban`.
    - This will most likely be changed next patch, but for now they have been removed.
        - Why?: If you didn't have a log channel set, it would error out, but still kick / ban the person.
* `doob/ai` and `doob/nai` doesn't ping everyone anymore
* `doob/dog` now has a lower chance of getting a Lucky Dog
    - Instead of 1/100 it is now 1/1000
    - The reason I did this is because people were getting them too often, and for the nitro giveaway in the support server, at least like 2/3 people a day got a lucky dog every single day since the bot hit about 70+ servers, so I knew it would be unfair to keep it 1/100 so I changed it, if this change has any problem, we might bump it back up to 1/500. Hopefully you understand the change.
* `doob/kick` and `doob/ban` now check for role hierarchys
    - For example, a Helper can't kick a Moderator.
* No more random "This Command didn't work" error.
* Changed the message for the "Forbidden" error.
* Removed the "HTTPException" error handling, for now.
* `doob/slap` no longer sends 2 messages.
* `doob/prefix` is now in an embed
* Added [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob for a Lucky Dog!
* Made the cooldown for `doob/dog` longer.
    - Someone suggested in the [Doob Support Discord](https://discord.gg/hgQTTU7) to make a cooldown on the command, little did they know, it had a command, appearently it wasn't long enough so I have increased it.
        - You can only use it 2 times every 5 seconds.
* Added owner only `doob/nitrogiveaway` command to tell users on how Doob's Nitro Classic giveaways work.
* New dog API!
    - Now there are so many more regular dogs!
* Statcord integration!
* Added polls (hi mr. jones)
* Added actual command descriptions for when you do `doob/help {cmd}`
    - Example: `doob/help ban` shows a description + the usage.
* Decreased the command cooldown for `doob/help`
* Made it so it only clears reactions on the `doob/help` timeout, and not delete the message.
* Made a new owner only `doob/update` command for giving brief updates about the bot.
* Updated some help commands so that the permissions that are required are on a new line, instead of the same line, makes it look nicer imo.

## v2.0.7
* Added doob/support - Gives link to the Doob support server.
* Added doob/invite - Gives link to invite Doob to another server.
* 1 in 50 chance of a Lucky Dog for [Patrons](https://patreon.com/doobdev) instead of 1 in 100
    - With this change, I added an ad on the top of the embed that only appear sometiems.
* Added a [Patreon](https://patreon.com/doobdev) field to doob/info
    - If you are a patron it thanks you! :)
* Echo is now a [Patreon](https://patreon.com/doobdev) only command!
    - "BUT WHY, BUT WHY" 
        1. Moderation
        2. I don't want random people to say random garbage on my bot
        3. Rack in those patrons EZ
* Patron status is now displayed in doob/profile

## v2.0.6
* New Lucky Dog! (Kevin from [@Weesterner](https://twitter.com/weesterner)!)
* Changed Description on the Lucky Dog embeds.
    - Added Twitter links to the description.
* Decreased the odds so they are actually 1 in 100
    - With me adding more Lucky Dogs, it has actually increased the chance for you to get one, so now it is actually a 1 in 100 chance to get a lucky dog!
* Removed message deletes for errors.
* Moved old v1 folder to a [new repository](https://github.com/doobdev/old-doob).
* Added some fun Among Us commands!
    - doob/notanimposter {user} -  gives an ascii of an among us crewmate floating through space with text saying "{user} was not an imposter"
    - doob/animposter {user} - gives the same ascii except it says "{user} was an imposter"
* XP Leaderboard is BACK! (fixed by [@X Daniel](https://github.com/x-daniel-17))

## v2.0.5
* Added doob/levelmessages.
    - Made a way to disable level messages in your server, Do `doob/levelmessages no` if you want to disable them, `doob/levelmessages yes` to re-enable them.

## v2.0.4
* Deleted Message logs have been added.
* Made log embeds look nicer.
* Updated some of the lingo used on the Lucky Dogs descriptions.
* Changelog link on doob/info now automatically updates with the latest GitHub changelog "jump to" link.
* Added channels to message update / message delete logs
* Updated the doob/level message to say that you are ranked based on the amount of users globally.
* doob/profile now shows XP and Rank
* Disabled on_user_update logging events for now, as I don't know how to grab a guild id

## v2.0.3
* os.sep in `__init__.py` for cogs
* adds server to DB when bot is added to said server.
* multiple bug fixes

## v2.0.2
* Added another lucky dog! (mmatt's GAMING server icon!)

## v2.0.1:
* Added a Lucky dog! (Koda from [@Mendo](https://twitter.com/mendo)!)


------------------------------


## Old Doob V1 changelog below.
## v1.0.1:
* Patreon added
    - You can now purchase a subscription to help support Doob! Head on over to [patreon.com/doobdev](https://patreon.com/doobdev) and get your subscription!
        - Tier 1 gives you:
            1. Patron-only posts and messages
            2. Priority Support
            3. General Support
            4. Exclusive Doob commands to use!
        - Tier 2 gives you:
            1. Everything from Tier 1
            2. Hosting the Among Us Bot in your server!
        - Tier 3 gives you:
            1. Everything from Tiers 1/2
            2. Doob Beta Bot in your server!
