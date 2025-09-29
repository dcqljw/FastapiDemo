from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `UserRole`;
        ALTER TABLE `user` ADD `roles_id` INT UNIQUE;
        ALTER TABLE `user` ADD CONSTRAINT `fk_user_role_e3f2eb49` FOREIGN KEY (`roles_id`) REFERENCES `role` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP FOREIGN KEY `fk_user_role_e3f2eb49`;
        ALTER TABLE `user` DROP COLUMN `roles_id`;
        CREATE TABLE `UserRole` (
    `role_id` INT NOT NULL REFERENCES `role` (`id`) ON DELETE CASCADE,
    `user_id` INT NOT NULL REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""
