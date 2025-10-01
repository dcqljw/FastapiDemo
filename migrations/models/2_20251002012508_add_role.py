from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `permission` RENAME COLUMN `name` TO `resource`;
        ALTER TABLE `permission` ADD `permission_key` VARCHAR(255) NOT NULL;
        ALTER TABLE `permission` ADD `action` VARCHAR(255) NOT NULL;
        ALTER TABLE `permission` DROP COLUMN `created_at`;
        ALTER TABLE `permission` DROP COLUMN `updated_at`;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `permission` ADD `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `permission` RENAME COLUMN `resource` TO `name`;
        ALTER TABLE `permission` ADD `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `permission` DROP COLUMN `permission_key`;
        ALTER TABLE `permission` DROP COLUMN `action`;"""
