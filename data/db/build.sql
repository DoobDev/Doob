/* Builds the database using the following tables */

CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "d!",
    LogChannel text,
    MutedRole text,
    StarBoardChannel text,
    LevelMessages text DEFAULT "no",
    YesNoReaction text DEFAULT "no"
);

CREATE TABLE IF NOT EXISTS users(
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP,
    OverwatchUsername text,
    OverwatchPlatform text,
    OverwatchRegion text,
    LastfmUsername text,
    osuUsername text,
    ShortLinkAmount integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS "mutes" (
	UserID integer,
	GuildID integer,
	RoleIDs	text,
	PRIMARY KEY("UserID","GuildID")
);

CREATE TABLE IF NOT EXISTS votes(
	UserID integer PRIMARY KEY,
	HAVEVOTED text DEFAULT "no",
	VoteLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS guildexp(
    GuildID integer,
    UserID integer,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("GuildID", "UserID")
);

CREATE TABLE IF NOT EXISTS luckydogs(
    UserID integer,
    LuckyDogs integer DEFAULT 0,
    LastUpdated text DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("UserID")
);

CREATE TABLE IF NOT EXISTS starboard(
    MessageID integer,
    StarMessageID integer,
    Stars integer DEFAULT 1,
    GuildID integer,
    PRIMARY KEY("MessageID", "GuildID")
);

CREATE TABLE IF NOT EXISTS warns(
    UserID integer,
    Warns integer DEFAULT 0,
    GuildID integer,
    PRIMARY KEY("UserID", "GuildID")   
);

CREATE TABLE IF NOT EXISTS globalwarns(
    UserID integer,
    Warns integer DEFAULT 0,
    PRIMARY KEY("UserID")
);

CREATE TABLE IF NOT EXISTS blacklist(
    UserID integer,
    Reason text DEFAULT "Unknown",
    PRIMARY KEY("UserID")
)