DROP TABLE IF EXISTS `model_attachments_json`;
CREATE TABLE `model_attachments_json` (
    `ModelID` INT UNSIGNED NOT NULL,
    `AttachmentsJSON` JSON,
    PRIMARY KEY (`ModelID`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci
