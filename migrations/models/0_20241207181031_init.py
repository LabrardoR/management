from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` CHAR(36) NOT NULL  PRIMARY KEY,
    `account` VARCHAR(100) NOT NULL  COMMENT '账户' DEFAULT '',
    `username` VARCHAR(100) NOT NULL  COMMENT '名称' DEFAULT '',
    `password` VARCHAR(100) NOT NULL  COMMENT '密码' DEFAULT '',
    `phone` VARCHAR(100) NOT NULL  COMMENT '电话号' DEFAULT '',
    `points` INT NOT NULL  COMMENT '积分' DEFAULT 0,
    `email` VARCHAR(100) NOT NULL  DEFAULT '',
    `gender` SMALLINT NOT NULL  COMMENT '0 为男，1 为女' DEFAULT 0,
    `role` SMALLINT NOT NULL  COMMENT '0 为普通用户，1 为 VIP 用户，9 为管理员' DEFAULT 0,
    `create_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `video` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` BIGINT NOT NULL,
    `file_name` VARCHAR(255) NOT NULL,
    `file_path` VARCHAR(255) NOT NULL  COMMENT '文件路径',
    `duration` DOUBLE NOT NULL  COMMENT '视频时长（秒）',
    `upload_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    KEY `idx_video_user_id_242052` (`user_id`),
    KEY `idx_video_file_na_e5649b` (`file_name`),
    KEY `idx_video_file_pa_dea5fe` (`file_path`)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userform` (
    `id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` BIGINT NOT NULL,
    `phone` VARCHAR(20)   COMMENT '电话号/账号',
    `email` VARCHAR(30) NOT NULL,
    `message` LONGTEXT NOT NULL,
    `create_time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
