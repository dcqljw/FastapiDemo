from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP FOREIGN KEY `fk_user_role_e3f2eb49`;
        ALTER TABLE `role` ADD `users_id` INT;
        ALTER TABLE `user` DROP COLUMN `roles_id`;
        ALTER TABLE `role` ADD CONSTRAINT `fk_role_user_3e8cb9e2` FOREIGN KEY (`users_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `role` DROP FOREIGN KEY `fk_role_user_3e8cb9e2`;
        ALTER TABLE `role` DROP COLUMN `users_id`;
        ALTER TABLE `user` ADD `roles_id` INT UNIQUE;
        ALTER TABLE `user` ADD CONSTRAINT `fk_user_role_e3f2eb49` FOREIGN KEY (`roles_id`) REFERENCES `role` (`id`) ON DELETE CASCADE;"""
