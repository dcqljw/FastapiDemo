from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `userrole` DROP FOREIGN KEY `fk_userrole_role_371ea05b`;
        ALTER TABLE `userrole` DROP FOREIGN KEY `fk_userrole_user_2634076a`;
        ALTER TABLE `rolepermission` DROP FOREIGN KEY `fk_roleperm_role_82cfb324`;
        ALTER TABLE `rolepermission` DROP FOREIGN KEY `fk_roleperm_permissi_e53c25b0`;
        ALTER TABLE `rolepermission` RENAME COLUMN `permission_id_id` TO `permission_id`;
        ALTER TABLE `rolepermission` RENAME COLUMN `role_id_id` TO `role_id`;
        ALTER TABLE `userrole` RENAME COLUMN `user_id_id` TO `user_id`;
        ALTER TABLE `userrole` RENAME COLUMN `role_id_id` TO `role_id`;
        ALTER TABLE `rolepermission` ADD CONSTRAINT `fk_roleperm_role_5e79ed3f` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE CASCADE;
        ALTER TABLE `rolepermission` ADD CONSTRAINT `fk_roleperm_permissi_0435b7e4` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`permission_id`) ON DELETE CASCADE;
        ALTER TABLE `userrole` ADD CONSTRAINT `fk_userrole_role_5ea23e2c` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`) ON DELETE CASCADE;
        ALTER TABLE `userrole` ADD CONSTRAINT `fk_userrole_user_7369096d` FOREIGN KEY (`user_id`) REFERENCES `user` (`uid`) ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `rolepermission` DROP FOREIGN KEY `fk_roleperm_permissi_0435b7e4`;
        ALTER TABLE `rolepermission` DROP FOREIGN KEY `fk_roleperm_role_5e79ed3f`;
        ALTER TABLE `userrole` DROP FOREIGN KEY `fk_userrole_user_7369096d`;
        ALTER TABLE `userrole` DROP FOREIGN KEY `fk_userrole_role_5ea23e2c`;
        ALTER TABLE `userrole` RENAME COLUMN `user_id` TO `user_id_id`;
        ALTER TABLE `userrole` RENAME COLUMN `role_id` TO `role_id_id`;
        ALTER TABLE `rolepermission` RENAME COLUMN `permission_id` TO `permission_id_id`;
        ALTER TABLE `rolepermission` RENAME COLUMN `role_id` TO `role_id_id`;
        ALTER TABLE `userrole` ADD CONSTRAINT `fk_userrole_user_2634076a` FOREIGN KEY (`user_id_id`) REFERENCES `user` (`uid`) ON DELETE CASCADE;
        ALTER TABLE `userrole` ADD CONSTRAINT `fk_userrole_role_371ea05b` FOREIGN KEY (`role_id_id`) REFERENCES `role` (`role_id`) ON DELETE CASCADE;
        ALTER TABLE `rolepermission` ADD CONSTRAINT `fk_roleperm_permissi_e53c25b0` FOREIGN KEY (`permission_id_id`) REFERENCES `permission` (`permission_id`) ON DELETE CASCADE;
        ALTER TABLE `rolepermission` ADD CONSTRAINT `fk_roleperm_role_82cfb324` FOREIGN KEY (`role_id_id`) REFERENCES `role` (`role_id`) ON DELETE CASCADE;"""
