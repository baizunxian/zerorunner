/*
 Navicat Premium Data Transfer

 Source Server         : 42.192.38.108-tx
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : 42.192.38.108:3306
 Source Schema         : zero_autotest

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 11/05/2022 10:36:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for case_info
-- ----------------------------
DROP TABLE IF EXISTS `case_info`;
CREATE TABLE `case_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `case_type` int NOT NULL DEFAULT 1 COMMENT 'test/config,测试类型, 1 case  2 config',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用例/配置名称',
  `project_id` int NULL DEFAULT NULL COMMENT '所属项目',
  `module_id` int NULL DEFAULT NULL COMMENT '所属模块',
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `include` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '前置config/test',
  `testcase` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `service_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '所属服务名称',
  `run_type` int NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `case_status` int NULL DEFAULT 10 COMMENT '用例状态 10, 生效 ， 20 失效',
  `priority` int NULL DEFAULT NULL COMMENT '优先级',
  `config_id` int NULL DEFAULT NULL COMMENT '用例配置id',
  `code_id` int NULL DEFAULT NULL COMMENT '关联接口id',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '接口code',
  `case_tab` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用例标签',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for celery_crontab_schedule
-- ----------------------------
DROP TABLE IF EXISTS `celery_crontab_schedule`;
CREATE TABLE `celery_crontab_schedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `hour` varchar(96) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `day_of_week` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `day_of_month` varchar(124) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `month_of_year` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `timezone` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for celery_interval_schedule
-- ----------------------------
DROP TABLE IF EXISTS `celery_interval_schedule`;
CREATE TABLE `celery_interval_schedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `every` int NOT NULL,
  `period` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for celery_periodic_task
-- ----------------------------
DROP TABLE IF EXISTS `celery_periodic_task`;
CREATE TABLE `celery_periodic_task`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `task` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `interval_id` int NULL DEFAULT NULL,
  `crontab_id` int NULL DEFAULT NULL,
  `solar_id` int NULL DEFAULT NULL,
  `args` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `kwargs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `queue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `exchange` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `routing_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `priority` int NULL DEFAULT NULL,
  `expires` datetime NULL DEFAULT NULL,
  `one_off` tinyint(1) NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `enabled` tinyint(1) NULL DEFAULT NULL,
  `last_run_at` datetime NULL DEFAULT NULL,
  `total_run_count` int NOT NULL,
  `date_changed` datetime NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `run_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `project_id` int NULL DEFAULT NULL,
  `module_id` int NULL DEFAULT NULL,
  `suite_id` int NULL DEFAULT NULL,
  `case_ids` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for celery_periodic_task_changed
-- ----------------------------
DROP TABLE IF EXISTS `celery_periodic_task_changed`;
CREATE TABLE `celery_periodic_task_changed`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for celery_solar_schedule
-- ----------------------------
DROP TABLE IF EXISTS `celery_solar_schedule`;
CREATE TABLE `celery_solar_schedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `latitude` float NULL DEFAULT NULL,
  `longitude` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for debug_talk
-- ----------------------------
DROP TABLE IF EXISTS `debug_talk`;
CREATE TABLE `debug_talk`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `debug_talk` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for env
-- ----------------------------
DROP TABLE IF EXISTS `env`;
CREATE TABLE `env`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NOT NULL DEFAULT 1,
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for lookup
-- ----------------------------
DROP TABLE IF EXISTS `lookup`;
CREATE TABLE `lookup`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '数据字典编码',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '描述',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NOT NULL DEFAULT 1,
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for lookup_value
-- ----------------------------
DROP TABLE IF EXISTS `lookup_value`;
CREATE TABLE `lookup_value`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `lookup_id` bigint NOT NULL COMMENT '所属类型',
  `lookup_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '编码',
  `lookup_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '值',
  `ext` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '拓展1',
  `display_sequence` int NULL DEFAULT NULL COMMENT '显示顺序',
  `enabled_flag` int NOT NULL DEFAULT 1 COMMENT '是否有效',
  `created_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '创建人',
  `creation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '最后更新人',
  `updation_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_lookup_code`(`lookup_code`) USING BTREE,
  INDEX `idx_lookup_enable`(`enabled_flag`) USING BTREE,
  INDEX `idx_lookup_id`(`lookup_id`, `enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_id` int NULL DEFAULT NULL COMMENT '父级id',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '菜单路径',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单名称',
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '组件路径',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'title',
  `isLink` int NULL DEFAULT 0 COMMENT '开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`',
  `isHide` int NULL DEFAULT 0 COMMENT '菜单是否隐藏（菜单不显示在界面，但可以进行跳转）',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '图标',
  `isKeepAlive` int NULL DEFAULT NULL COMMENT '菜单是否缓存',
  `isAffix` int NULL DEFAULT NULL COMMENT '固定标签',
  `isIframe` int NULL DEFAULT NULL COMMENT '是否内嵌',
  `roles` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限',
  `sort` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `active_menu` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '显示页签',
  `menu_type` int NULL DEFAULT 10 COMMENT '菜单类型',
  `redirect` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '重定向',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `views` int NULL DEFAULT 0 COMMENT '访问数',
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `lookup_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`, `path`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for module_info
-- ----------------------------
DROP TABLE IF EXISTS `module_info`;
CREATE TABLE `module_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模块名称',
  `project_id` int NULL DEFAULT NULL COMMENT '归属项目id',
  `config_id` int NULL DEFAULT NULL COMMENT '关联配置id',
  `test_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '测试负责人id',
  `simple_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '简要描述',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '其他信息',
  `leader_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '负责人',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人',
  `updated_by` int NULL DEFAULT NULL,
  `module_packages` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `priority` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_module_info_module_name`(`name`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for project_info
-- ----------------------------
DROP TABLE IF EXISTS `project_info`;
CREATE TABLE `project_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '项目名称',
  `responsible_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '负责人',
  `test_user` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '测试人员',
  `dev_user` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '开发人员',
  `publish_app` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '发布应用',
  `simple_desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '简要描述',
  `remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '其他信息',
  `config_id` int NULL DEFAULT NULL COMMENT '关联配置id',
  `product_id` int NULL DEFAULT NULL COMMENT '产品线',
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int NOT NULL COMMENT '更新人',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_project_info_name`(`name`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 582 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '名称',
  `role_type` int NULL DEFAULT 10 COMMENT '权限类型',
  `menus` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单ids',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `updated_by` int NOT NULL COMMENT '更新人',
  `created_by` int NOT NULL COMMENT '创建人',
  `status` int NULL DEFAULT 10 COMMENT '角色状态 10 启用，20 禁用',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for test_reports
-- ----------------------------
DROP TABLE IF EXISTS `test_reports`;
CREATE TABLE `test_reports`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_at` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `scene_num` int NULL DEFAULT NULL COMMENT '场景数',
  `duration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '执行用时 秒',
  `run_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运行类型，同步，异步',
  `task_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '任务类型, test,module,project',
  `run_mode` int NULL DEFAULT NULL,
  `project_id` int NULL DEFAULT NULL,
  `module_id` int NULL DEFAULT NULL,
  `report_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `run_case_priority` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `execute_user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `execute_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `execute_service` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `successful_use_case` int NULL DEFAULT NULL COMMENT '成功用例数',
  `report_body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '报告详情',
  `run_test_count` int NULL DEFAULT NULL COMMENT '运行用例数',
  `success` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 62 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for test_suite
-- ----------------------------
DROP TABLE IF EXISTS `test_suite`;
CREATE TABLE `test_suite`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `project_id` int NULL DEFAULT NULL,
  `include` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `config_id` int NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int NOT NULL COMMENT '更新人',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `enabled_flag` tinyint(1) NULL DEFAULT 1 COMMENT '是否删除',
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `roles` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '1' COMMENT '用户角色',
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户昵称',
  `status` int NULL DEFAULT 1 COMMENT '用户状态 0 正常 1锁定',
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `user_type` int NULL DEFAULT 10 COMMENT '用户类型， 10 管理人员, 20 测试人员',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户描述',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_user_email`(`email`) USING BTREE,
  INDEX `ix_user_password`(`password`) USING BTREE,
  INDEX `ix_user_username`(`username`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
