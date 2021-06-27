## v2.8.10
* Added new logtypes [(#242)](https://github.com/DoobDev/issues/242)

## v2.8.9
* Added /dog [(#248)](https://github.com/DoobDev/Doob/issues/248)

## v2.8.8
* Added member join logs.
* Added member leave (remove) logs.

## v2.8.7
* Added d!fortniteskin [(#231)](https://github.com/DoobDev/Doob/issues/231)

## v2.8.6
* Added /poll [(#213)](https://github.com/DoobDev/Doob/issues/213)
* Added /endpoll [(#213)](https://github.com/DoobDev/Doob/issues/213)
* Reverted the November 2020 Log Changes (from v2.1.0) [(#211)](https://github.com/DoobDev/Doob/issues/211)
* Shows Server XP Rank on on `d!level` [(#244)](https://github.com/DoobDev/Doob/issues/244)

## v2.8.5
* Added "xp to next level" to `d!level` [(#221)](https://github.com/DoobDev/Doob/issues/221)

## v2.8.4
* Added who made the link to short link logs ([#209](https://github.com/doobdev/Doob/issues/209))
* Added end poll command (d!endpoll) ([#212](https://github.com/doobdev/Doob/issues/212))

## v2.8.3
* Added unlimited short links for owners ([#207](https://github.com/doobdev/Doob/issues/207))
* Made a better description for d!link

## v2.8.2
* Added short link logs ([#206](https://github.com/doobdev/Doob/issues/206))

## v2.8.1
* Changed invite link.

## v2.8.0
* Added `d!coinfliptimes`
    - Flips a coin the amount of times you want, and shows you the outcome.
* Added `d!link`
    - Shorten a link with doob.link!
        - 6 links for regular people
        - 12 links for [Patrons](https://patreon.com/doobdev/)
* Added /link

## v2.7.2
* Added /support
* Added /invite

## v2.7.1
* Added Error handling for EmojiNotFound

## v2.7.0
Too many changes, forgot to docuement, sorry.
- https://github.com/DoobDev/Doob/milestone/1?closed=1

## v2.6.8
* Added `d!dogehouse`

## v2.6.7
* Fixed `d!bio` command description. ([#160](https://github.com/doobdev/Doob/issues/160))
* Added `d!owroll` ([#163](https://github.com/doobdev/Doob/issues/163))
* Added `d!valroll` subcommands. ([#164](https://github.com/doobdev/Doob/issues/164))
    - Documented at: https://docs.doobbot.com/#d-valroll-subcommands
* Added priority labels to `d!issue -c`

## v2.6.6
* Added `d!issue`
* Added `d!issue` subcommands.
    - Documented at: https://docs.doobbot.com/#d-issue-subcommands
    - Owner Only

## v2.6.5
* Added `d!owoify`

## v2.6.4
* Added `d!role`
* Added `d!role` subcommands.
    - Documented at: https://docs.doobbot.com/#d-role-subcommands

## v2.6.3
* Added `d!warn`
* Added `d!warnings`

## v2.6.2
* Added `d!twitch` subcommands.
    - Documented at: https://docs.doobbot.com/#d-twitch-subcommands

## v2.6.1
* Added a description for `d!fight` command.
* Added `d!overlay`
    - From: https://github.com/DoobDev/Krinio/blob/master/lib/cogs/overlay.py

## v2.6.0
* Added `d!battle` ([#132](https://github.com/doobdev/Doob/pull/132))
    - Battle a friend or foe!

## v2.5.1
* Added `d!valroll`
    - Rolls a random VALORANT character for you to play.

## v2.5.0
* Changed Doob's default prefix to `d!`.
    - The only reason it was `doob/` to begin with was because Top.gg muted Doob for having too much of a unique prefix "back then". Now, Top.gg removed all bots from their server, so there is no reason to have a 5 character prefix.
#### Note: Only servers that are new to Doob will be affected, old servers will keep their `doob/` prefix unless they change it themselves. (Custom prefixes have not been touched with this update.)

## v2.4.5
* Added `d!ownerprefix`

## v2.4.4
* Added basic error handling for not having permissions for a command.
* Removed the error handling from Ban/Kick/Mute commands, because of the change above.

## v2.4.3
* Added `d!createtextchannel`
* Added `d!createvoicechannel`

## v2.4.2
* Now running on Discord.py 1.6.0
* Instead of the commands just sending, it replies to you.

## v2.4.1
* Added command descriptions for music commands.

## v2.4.0
### Added music support to Doob!
* Added `d!connect`
    - Connects to a Voice Channel
* Added `d!disconnect`
    - Disconnects from a Voice Channel
* Added `d!play`
    - Plays a song either linked from YouTube, or searched.
* Added `d!pause`
    - Pauses the current song.
* Added `d!resume`
    - Resumes the current song.
        - (Using `d!play` with nothing after it does the same thing.)
* Added `d!stop`
    - Stops the music, and clears the queue.
* Added `d!next`
    - Skips the current track.
* Added `d!previous`
    - Goes to the previous track in the queue and plays it.
* Added `d!shuffle`
    - Shuffles the queue.
* Added `d!repeat`
    - Allows you to repeat using `none`, `1`, or `all`.
        - `none` = Stops repeating
        - `1` = 1 track repeating
        - `all` = Queue repeating.
* Added `d!queue`
    - Lets you see the queue for that server.

## I worked super hard for this to come out, however I must provide a disclaimer that at this time (1/4/2021) this is in **OPEN BETA**, ~~meaning this *might* be on the public bot (meaning by the time this changelog is out, I might not have figured out how to install lavalink [the "music"/"voice" ""server""] on my VPS.)~~, but it still might be buggy and stuff like command descriptions aren't finished yet.
(Music is available on the public bot.)

## v2.3.4
* Added `Patreon Only` command `d!phone`.

## v2.3.3
* Added some DM commands
    - DM the bot, "donate" and it gives you a donation link.
    - DM the bot, "help" and it gives you instructions on how to get help.
    - DM the bot anything else, and it tells you that most commands can't be DMd

## v2.3.2
* Fixed `d!timebomb`'s lower time error.

## v2.3.1
* Forgot to move to `users` table instead of `exp` table on 2 lines.
    - This fixes `d!fm --np`

## v2.2.1
### This should technically be v2.3.0, but I'm dumb lol
### (bigger update then usual, because the main bot was offline while I was working on this stuff, so I just wanted it to be 1 update instead of speread across a bunch of different updates)
* Added rounding to:
    - osu! commands
* Made `d!setosu` show your profile picture from osu! instead of from Discord.
* (if all went well) Added `d!remind`
    - Lets you set a reminder!

## v2.2.0
* `d!timebomb` now has a timelimit of 1000 seconds.

## v2.1.6
* Added a **HUGE** cooldown to `d!russianroulette`
    - 1 command per 30 seconds in a guild.

## v2.1.5
* Added `d!fm --np`
* Added `d!russianroulette`
    - Put people in a russian roulette to be banned.

## v2.1.4
* Added `d!startgiveaway`
    - Starts a giveaway!
* Added `d!stopgiveaway`
    - Stops a giveaway!
* Removed cooldown on `d!echo`
* Made the message delete itself on `d!echo`
    - Ex: `d!echo Hello` <== That message would be deleted.

## v2.1.3
* Made `d!fm artist search` only when the response status is 200
* Added `d!vote`

## v2.1.2
* `d!osu` checks if you have no username saved
    - If you don't, it tells you how to add your username.
* `d!osuset` is now an alias for `d!setosu`
* Added `d!fm artist search`!
    - Search for artists and get their 
        1. Listeners
        2. Play Count
        3. Wiki Link
        4. Similar Artists
        5. Top Tracks
        6. Top Albums

## v2.1.1
* Added `d!osu`
    - See your osu! profile!
* Added `d!setosu`
    - Set your osu! profile for `d!osu`!

## v2.1.0
* Per-Server XP Leaderboards (`d!serverleaderboard`)
* Removed `d!slap`
    - There has been an exploit discovered to ping everyone, decided to go ahead and remove the command, wasn't used at all.
* New `d!timebomb` command
    - Lets you have a message with a time limit!
* Doob Logging now sends in regular messages instead of embeds.
    - I saw [stageosu/Kaguya](https://github.com/stageosu/kaguya) do this recently, and I love the look of it, go check out Stage's bot, its great :D
* Added `d!streamlookup` command!
    - Lookup your favorite streamers, see if they are online or not, and if they are online, see information like what game they are playing!
* Added `d!owstats` command!
    - Check your (or your friends) Overwatch stats in Discord!
* Added `d!setowusername` command!
    - Add your platform, username, and region to be able to look up your stats on Doob!
        - Only acceptable platforms are `pc` `xbl` and `psn`
        - Only acceptable regions are `us` `eu` or `asia`
        - For battletags, make sure you do `{username}-{numbers}` NOT `{username}#{numbers}`
* Changed around some of the fields on `d!streamlookup`
* Added `d!bio` command!
    - Lookup your/your friend's Discord.bio profile in Discord!
* Added `d!lastfm` command!
    - Lookup your/your friend's Last.fm profiles directly in Discord!
* Added `d!setlastfm` command!
    - Set your default last.fm username, so you don't have to type your username every time you want to use a Last.fm command.
* Added some Doob emojis to `d!info`
* `d!lastfm` only does your profile now.
    - To do other people's do `d!lastfm search {username}`
* Added `d!lastfm recent`!
    - See the last 5 songs you or someone else has listened to!
* Added `d!lastfm top albums`!
    - Get your top 10 most listened to albums on Last.fm
* Added `d!lastfm artist charts`!
    - See the top 10 artists on Last.fm!
* Added `d!lastfm top tracks`!
    - See the top 10 tracks you have played on last.fm!
* Added `d!lastfm top artists`!
    - See the top 10 artists you have played on last.fm!

## v2.0.9
#### The muting update!
* Finally! Doob has muting!
* New `d!mute` command!
    - Mutes a member from your server!
        - Example: `d!mute @X Daniel lol`
            - Make sure to set your "Muted Role" by doing `d!setmutedrole`
* New `d!unmute` command!
    - Unmutes a member from your server!
        - Example: `d!unmute @X Daniel`
* Per-Server XP is now avaliable!
* Updated `d!level` to include Server XP
* Updated `d!profile` to say "Doob Global XP/Level/Rank".
* Made unmute/mute commands have embeds.
* Fixed Level Messages not working
* Fixed `d!slc` and `d!slm` so it no longer shows "None"
* Instead of help messages and such saying `@Doob ` for the prefix, it now says your server's prefix.
* Removed the description for the Among Us Commands.
    * You can still find them in `d!help {cmd}`
* Added a new Patreon only command! `d!luckydog`
    * Gives you instant access to all the lucky dog's avaliable.
* Lucky Dog Nitro Giveaways are BACK!
    - Every month, whoever gets the most Lucky Dogs, gets 1 month of Nitro Classic!
* New `d!luckydogs` command!
    - Check how many lucky dogs you have "caught" over the month.
* Updated `d!userinfo` "Bot or not" field.
    - "Bot or not." ==> "Bot"
* New `d!unban` command!
* Starboards!
    - New `d!setstarboardchannel` command!
* Updated starboard embed to have a "Jump to link"
    - Lets you jump to the message that was starred.
* Really bad `d!jumpscare` command lol.
* Removed jumpscare
* Lucky Dogs now occur 1/500
* Updated `d!info` to have system stats.

## v2.0.8
* Updated description (on the help command) for
    - `d!Leaderboard`
* New `d!patreon` command!
* Added some debugging for d!dog
    - It gives me the roll numbers for P_AD and L_DOG if I need to check if it is working or not.
* Default Level Messages are off.
    - This feature is on the live bot now.
* Default error message gives support server.
* `d!setlevelmessages` now:
    - Tells you if you have level messages on or off if you just type `d!setlevelmessages`
    - Only sets your level message setting if you type
        - `yes`
        - `Yes`
        - `no`
        - `No`
* `d!slap` should no longer gives you a Bad Argument error.
    - Instead, it defaults to slapping yourself, silly you!
        - If you try to pass a reason in when doing `d!slap` with no member found, it says that you accidently slapped yourself instead of the person you meant to slap.
            - This also means it removes the default reason.
                - For instance, instead of it saying "for no reason!" it will just say "Reason - None!"
* `d!serverinfo` no longer requires server permissions!
    - The reason it needed server permissions last time is because of the "Banned Members" field, if Doob has Administrator permissions in a server, it will still show the "Banned Members" field.
* `d!prefix` and `d!setlevelmessages` can no longer be abused to do @everyone pings.
* `d!setmutedrole` and `d!setlogchannel` no longer have to be IDs anymore.
    - I believe they now **are required** to be pings.
        - Example: `d!setmutedrole @Muted` and `d!setlogchannel #logs`
            - Instead of from 2.0.7 (this is outdated, don't do this anymore.) `d!setmutedrole {role id}` and `d!setlogchannel {channel id}`
* Logs have been removed from `d!kick` and `d!ban`.
    - This will most likely be changed next patch, but for now they have been removed.
        - Why?: If you didn't have a log channel set, it would error out, but still kick / ban the person.
* `d!ai` and `d!nai` doesn't ping everyone anymore
* `d!dog` now has a lower chance of getting a Lucky Dog
    - Instead of 1/100 it is now 1/1000
    - The reason I did this is because people were getting them too often, and for the nitro giveaway in the support server, at least like 2/3 people a day got a lucky dog every single day since the bot hit about 70+ servers, so I knew it would be unfair to keep it 1/100 so I changed it, if this change has any problem, we might bump it back up to 1/500. Hopefully you understand the change.
* `d!kick` and `d!ban` now check for role hierarchys
    - For example, a Helper can't kick a Moderator.
* No more random "This Command didn't work" error.
* Changed the message for the "Forbidden" error.
* Removed the "HTTPException" error handling, for now.
* `d!slap` no longer sends 2 messages.
* `d!prefix` is now in an embed
* Added [@KittyKay000](https://twitter.com/kittykay000)'s concept drawing of Doob for a Lucky Dog!
* Made the cooldown for `d!dog` longer.
    - Someone suggested in the [Doob Support Discord](https://discord.gg/hgQTTU7) to make a cooldown on the command, little did they know, it had a command, appearently it wasn't long enough so I have increased it.
        - You can only use it 2 times every 5 seconds.
* Added owner only `d!nitrogiveaway` command to tell users on how Doob's Nitro Classic giveaways work.
* New dog API!
    - Now there are so many more regular dogs!
* Statcord integration!
* Added polls (hi mr. jones)
* Added actual command descriptions for when you do `d!help {cmd}`
    - Example: `d!help ban` shows a description + the usage.
* Decreased the command cooldown for `d!help`
* Made it so it only clears reactions on the `d!help` timeout, and not delete the message.
* Made a new owner only `d!update` command for giving brief updates about the bot.
* Updated some help commands so that the permissions that are required are on a new line, instead of the same line, makes it look nicer imo.

## v2.0.7
* Added d!support - Gives link to the Doob support server.
* Added d!invite - Gives link to invite Doob to another server.
* 1 in 50 chance of a Lucky Dog for [Patrons](https://patreon.com/doobdev) instead of 1 in 100
    - With this change, I added an ad on the top of the embed that only appear sometiems.
* Added a [Patreon](https://patreon.com/doobdev) field to d!info
    - If you are a patron it thanks you! :)
* Echo is now a [Patreon](https://patreon.com/doobdev) only command!
    - "BUT WHY, BUT WHY" 
        1. Moderation
        2. I don't want random people to say random garbage on my bot
        3. Rack in those patrons EZ
* Patron status is now displayed in d!profile

## v2.0.6
* New Lucky Dog! (Kevin from [@Weesterner](https://twitter.com/weesterner)!)
* Changed Description on the Lucky Dog embeds.
    - Added Twitter links to the description.
* Decreased the odds so they are actually 1 in 100
    - With me adding more Lucky Dogs, it has actually increased the chance for you to get one, so now it is actually a 1 in 100 chance to get a lucky dog!
* Removed message deletes for errors.
* Moved old v1 folder to a [new repository](https://github.com/doobdev/old-doob).
* Added some fun Among Us commands!
    - d!notanimposter {user} -  gives an ascii of an among us crewmate floating through space with text saying "{user} was not an imposter"
    - d!animposter {user} - gives the same ascii except it says "{user} was an imposter"
* XP Leaderboard is BACK! (fixed by [@X Daniel](https://github.com/x-daniel-17))

## v2.0.5
* Added d!levelmessages.
    - Made a way to disable level messages in your server, Do `d!levelmessages no` if you want to disable them, `d!levelmessages yes` to re-enable them.

## v2.0.4
* Deleted Message logs have been added.
* Made log embeds look nicer.
* Updated some of the lingo used on the Lucky Dogs descriptions.
* Changelog link on d!info now automatically updates with the latest GitHub changelog "jump to" link.
* Added channels to message update / message delete logs
* Updated the d!level message to say that you are ranked based on the amount of users globally.
* d!profile now shows XP and Rank
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
