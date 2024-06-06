DROP TABLE IF EXISTS `model_json`;
CREATE TABLE `model_json` (
    `ModelID` INT UNSIGNED NOT NULL,
    `ModelJSON` JSON,
    PRIMARY KEY (`ModelID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
