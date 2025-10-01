from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `permission` (
    `permission_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `role` (
    `role_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '角色ID',
    `name` VARCHAR(255) NOT NULL COMMENT '角色名称',
    `description` VARCHAR(255) NOT NULL COMMENT '角色描述',
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `rolepermission` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `permission_id_id` INT NOT NULL,
    `role_id_id` INT NOT NULL,
    CONSTRAINT `fk_roleperm_permissi_e53c25b0` FOREIGN KEY (`permission_id_id`) REFERENCES `permission` (`permission_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_roleperm_role_82cfb324` FOREIGN KEY (`role_id_id`) REFERENCES `role` (`role_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `uid` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(255) NOT NULL COMMENT '用户名',
    `nickname` VARCHAR(255) NOT NULL COMMENT '昵称',
    `email` VARCHAR(255) NOT NULL COMMENT '邮箱',
    `password` VARCHAR(255) NOT NULL COMMENT '密码',
    `created_at` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL COMMENT '更新时间' DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `is_first_login` BOOL NOT NULL COMMENT '是否首次登录' DEFAULT 1
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `userrole` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户角色ID',
    `role_id_id` INT NOT NULL COMMENT '角色ID',
    `user_id_id` BIGINT NOT NULL COMMENT '用户ID',
    CONSTRAINT `fk_userrole_role_371ea05b` FOREIGN KEY (`role_id_id`) REFERENCES `role` (`role_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_userrole_user_2634076a` FOREIGN KEY (`user_id_id`) REFERENCES `user` (`uid`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
