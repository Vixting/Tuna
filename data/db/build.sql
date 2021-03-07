
CREATE TABLE IF NOT EXISTS exp (
  UserID integer PRIMARY KEY,
  XP integer DEFAULT 0,
  evel integer DEFAULT 0,
  XPLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS guilds(
  GuildID integer PRIMARY KEY,
  Prefix text DEFAULT "!"
);

CREATE TABLE IF NOT EXISTS users(
  UserID VARCHAR(32),
  SteamID VARCHAR(32),
  Join_Date varchar(255),
  Leave_Date varchar(255)
);

CREATE TABLE IF NOT EXISTS mutes (
  UserID integer PRIMARY KEY,
  RoleIDS int,
  SanctionedBy text,
  reason text,
  duration int,
  EndTime text

);

CREATE TABLE IF NOT EXISTS schedules(
  Title text,
  Description text,
  Day text,
  Hour text,
  Minute text,
  Author text DEFAULT "Scheduled announcment"
);
