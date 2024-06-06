DROP TABLE IF EXISTS `model`;
CREATE TABLE `model` (
    `ID` int(10) unsigned NOT NULL,
    `Category` varchar(10) NOT NULL,
    `Manufacturer` varchar(128) NOT NULL,
    `Model` varchar(255) NOT NULL,
    `Link` varchar(500) DEFAULT '',
    PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
