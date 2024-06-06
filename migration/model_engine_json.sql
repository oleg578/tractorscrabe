DROP TABLE IF EXISTS `model_engine_json`;
CREATE TABLE `model_engine_json` (
    `ModelID` INT UNSIGNED NOT NULL,
    `EngineJSON` JSON,
    PRIMARY KEY (`ModelID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
