CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "doob/",
    LogChannel text,
    MutedRole text,
    StarBoardChannel text,
    LevelMessages text DEFAULT "yes"
);

CREATE TABLE IF NOT EXISTS exp (
    UserID integer PRIMARY KEY,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mutes(
    UserID integer PRIMARY KEY,
    RoleIDs text,
	GuildID integer
);