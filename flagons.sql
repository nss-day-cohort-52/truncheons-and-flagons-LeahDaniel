-- DELETE FROM Teams;
-- DELETE FROM Players;
-- DELETE FROM TeamScore;

DROP TABLE IF EXISTS TeamScore;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Team;

CREATE TABLE `Teams` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL
);

CREATE TABLE `Players` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `first_name`    TEXT NOT NULL,
    `last_name`    TEXT NOT NULL,
    `team_id` INTEGER NOT NULL,
    FOREIGN KEY(`team_id`) REFERENCES `Team`(`id`)
);


CREATE TABLE `TeamScores` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `team_id` INTEGER NOT NULL,
	`score`  TEXT NOT NULL,
	`time_stamp` TEXT NOT NULL,
    FOREIGN KEY(`team_id`) REFERENCES `Team`(`id`)
);


INSERT INTO `Teams` VALUES (null, 'Golden Gryphons');
INSERT INTO `Teams` VALUES (null, 'Shrill Harpies');
INSERT INTO `Teams` VALUES (null, 'Green Wyverns');


INSERT INTO `Players` VALUES (null, "Madi", "Peper", 1);
INSERT INTO `Players` VALUES (null, "Leah", "Gwin", 1);
INSERT INTO `Players` VALUES (null, "Kimmy", "Bird", 1);
INSERT INTO `Players` VALUES (null, "Meg", "Ducharme", 2);
INSERT INTO `Players` VALUES (null, "Emily", "Lemmon", 2);
INSERT INTO `Players` VALUES (null, "Mo", "Silvera", 2);
INSERT INTO `Players` VALUES (null, "Bryan", "Nilsen", 3);
INSERT INTO `Players` VALUES (null, "Jenna", "Solis", 3);
INSERT INTO `Players` VALUES (null, "Ryan", "Tanay", 3);

INSERT INTO `TeamScores` VALUES (null, 1, 3, 1583873462376);
INSERT INTO `TeamScores` VALUES (null, 1, 2, 1583873462376);
INSERT INTO `TeamScores` VALUES (null, 1, 4, 1583873462376);
INSERT INTO `TeamScores` VALUES (null, 2, 1, 1583873462376);
INSERT INTO `TeamScores` VALUES (null, 2, 6, 1583873462376);
INSERT INTO `TeamScores` VALUES (null, 2, 3, 1583873462376);

