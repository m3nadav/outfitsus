CREATE TABLE IF NOT EXISTS `classes` (
  `class_fid` varchar(100) NOT NULL,
  `name` text NOT NULL,
  `school_fid` varchar(100) NOT NULL,
  PRIMARY KEY (`class_fid`),
  KEY `school_fid` (`school_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `classes_from_users` (
  `ufid` varchar(100) NOT NULL,
  `from_ufid` varchar(100) NOT NULL,
  `class_fid` varchar(100) NOT NULL,
  PRIMARY KEY (`ufid`,`from_ufid`,`class_fid`),
  KEY `class_fid` (`class_fid`),
  KEY `from_ufid` (`from_ufid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `classes_with_users` (
  `ufid` varchar(100) NOT NULL,
  `with_ufid` varchar(100) NOT NULL,
  `class_fid` varchar(100) NOT NULL,
  PRIMARY KEY (`ufid`,`with_ufid`,`class_fid`),
  KEY `with_ufid` (`with_ufid`),
  KEY `class_fid` (`class_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `fav_teams` (
  `team_fid` varchar(100) NOT NULL,
  `name` text NOT NULL,
  PRIMARY KEY (`team_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `fb_logged_users` (
  `ufid` varchar(100) NOT NULL,
  `name` text NOT NULL,
  `birthday` date DEFAULT NULL,
  `email` text NOT NULL,
  `locale` text,
  `gender` text,
  `updated_time` datetime DEFAULT NULL,
  `link` text NOT NULL,
  `relationship_status` varchar(100) DEFAULT NULL,
  `oauth_token` text NOT NULL,
  PRIMARY KEY (`ufid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `schools` (
  `school_fid` varchar(100) NOT NULL,
  `name` text NOT NULL,
  `type` text NOT NULL,
  PRIMARY KEY (`school_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `sports` (
  `sport_fid` varchar(100) NOT NULL,
  `name` text NOT NULL,
  PRIMARY KEY (`sport_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `sports_from_users` (
  `ufid` varchar(100) NOT NULL,
  `from_ufid` varchar(100) NOT NULL,
  `sport_fid` varchar(100) NOT NULL,
  PRIMARY KEY (`ufid`,`from_ufid`,`sport_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `sports_with_users` (
  `ufid` varchar(100) NOT NULL,
  `with_ufid` varchar(100) NOT NULL,
  `sport_fid` varchar(100) NOT NULL,
  PRIMARY KEY (`ufid`,`with_ufid`,`sport_fid`),
  KEY `sport_fid` (`sport_fid`),
  KEY `with_ufid` (`with_ufid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `users_fav_team` (
  `ufid` varchar(100) NOT NULL,
  `team_fid` varchar(100) NOT NULL,
  PRIMARY KEY (`ufid`,`team_fid`),
  KEY `team_fid` (`team_fid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE `classes`
  ADD CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`school_fid`) REFERENCES `schools` (`school_fid`) ON DELETE CASCADE;
ALTER TABLE `classes_from_users`
  ADD CONSTRAINT `classes_from_users_ibfk_4` FOREIGN KEY (`from_ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE,
  ADD CONSTRAINT `classes_from_users_ibfk_1` FOREIGN KEY (`ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE,
  ADD CONSTRAINT `classes_from_users_ibfk_2` FOREIGN KEY (`class_fid`) REFERENCES `classes` (`class_fid`) ON DELETE CASCADE,
  ADD CONSTRAINT `classes_from_users_ibfk_3` FOREIGN KEY (`ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE;
ALTER TABLE `classes_with_users`
  ADD CONSTRAINT `classes_with_users_ibfk_3` FOREIGN KEY (`class_fid`) REFERENCES `classes` (`class_fid`) ON DELETE CASCADE,
  ADD CONSTRAINT `classes_with_users_ibfk_1` FOREIGN KEY (`ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE,
  ADD CONSTRAINT `classes_with_users_ibfk_2` FOREIGN KEY (`with_ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE;
ALTER TABLE `sports_with_users`
  ADD CONSTRAINT `sports_with_users_ibfk_3` FOREIGN KEY (`with_ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE,
  ADD CONSTRAINT `sports_with_users_ibfk_1` FOREIGN KEY (`sport_fid`) REFERENCES `sports` (`sport_fid`) ON DELETE CASCADE,
  ADD CONSTRAINT `sports_with_users_ibfk_2` FOREIGN KEY (`ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE;
ALTER TABLE `users_fav_team`
  ADD CONSTRAINT `users_fav_team_ibfk_2` FOREIGN KEY (`team_fid`) REFERENCES `fav_teams` (`team_fid`) ON DELETE CASCADE,
  ADD CONSTRAINT `users_fav_team_ibfk_1` FOREIGN KEY (`ufid`) REFERENCES `fb_logged_users` (`ufid`) ON DELETE CASCADE;

