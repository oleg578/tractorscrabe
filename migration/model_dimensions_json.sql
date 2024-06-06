DROP TABLE IF EXISTS `model_dimensions_json`;
CREATE TABLE `model_dimensions_json` (
    `ModelID` INT UNSIGNED NOT NULL,
    `DimensionsJSON` JSON,
    PRIMARY KEY (`ModelID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
