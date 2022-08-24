CREATE TABLE ProductData.`celery_log`(
    `retry` VARCHAR(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `status` INT(11) NOT NULL,
    `worker` VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `ctime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `task_id` VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `msg` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `info` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `args` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `kwargs` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `id` BIGINT(20) NOT NULL
);
--
-- 資料表索引 `celery_log`
--
ALTER TABLE ProductData.`celery_log`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `celery_log`
--
ALTER TABLE ProductData.`celery_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- 資料表 `schedule_task`
--
CREATE TABLE `ProductData`.`schedule_task` (
  `id` INT NOT NULL,
  `platform` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  `name` VARCHAR(255) NULL,
  `url` TEXT NULL,
  `start_page` INT NULL,
  `end_page` INT NULL,
  `updated_at` DATETIME NULL,
  `in_queue` INT NOT NULL,
  PRIMARY KEY (`id`)
);

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `schedule_task`
--
ALTER TABLE `ProductData`.`schedule_task` 
CHANGE COLUMN `id` `id` INT NOT NULL AUTO_INCREMENT ,
CHANGE COLUMN `platform` `platform` VARCHAR(45) NOT NULL ,
CHANGE COLUMN `type` `type` VARCHAR(45) NOT NULL ,
CHANGE COLUMN `name` `name` VARCHAR(255) NOT NULL ,
CHANGE COLUMN `url` `url` TEXT NOT NULL ,
CHANGE COLUMN `updated_at` `updated_at` DATETIME NOT NULL ;

--
-- 資料表 `product`
--
CREATE TABLE `ProductData`.`products` (
  `id` INT NOT NULL,
  `code` VARCHAR(100) NOT NULL,
  `platform` VARCHAR(45) NOT NULL,
  `product_code` VARCHAR(45) NOT NULL,
  `category_code` VARCHAR(45) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL,
  `category` VARCHAR(255) NULL,
  `brand` VARCHAR(45) NULL,
  `currency` VARCHAR(45) NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `promotion_tag` VARCHAR(255) NULL,
  `review_avg_rating` DECIMAL(4,2) NULL,
  `url` TEXT NOT NULL,
  `image` TEXT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`));

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `products`
--
ALTER TABLE `ProductData`.`products` 
CHANGE COLUMN `id` `id` INT NOT NULL AUTO_INCREMENT