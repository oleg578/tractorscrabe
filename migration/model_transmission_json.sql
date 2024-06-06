DROP TABLE IF EXISTS `model_transmission_json`;
CREATE TABLE `model_transmission_json` (
    `ModelID` INT UNSIGNED NOT NULL,
    `TransmissionJSON` JSON,
    PRIMARY KEY (`ModelID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
