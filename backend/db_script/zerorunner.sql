/*
 Navicat Premium Data Transfer

 Source Server         : xiaobaicodes
 Source Server Type    : MySQL
 Source Server Version : 50743
 Source Host           : xiaobaicodes
 Source Schema         : zerorunner

 Target Server Type    : MySQL
 Target Server Version : 50743
 File Encoding         : 65001

 Date: 24/10/2023 12:01:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for api_case
-- ----------------------------
DROP TABLE IF EXISTS `api_case`;
CREATE TABLE `api_case`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `project_id` bigint(22) NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人',
  `headers` json NULL COMMENT '请求头',
  `variables` json NULL COMMENT '变量',
  `step_data` json NULL COMMENT '步骤',
  `step_rely` int(11) NULL DEFAULT 1 COMMENT '步骤依赖  1依赖， 0 不依赖',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `version` int(11) NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_case
-- ----------------------------

-- ----------------------------
-- Table structure for api_case_step
-- ----------------------------
DROP TABLE IF EXISTS `api_case_step`;
CREATE TABLE `api_case_step`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `case_id` bigint(20) NULL DEFAULT NULL,
  `source_id` bigint(20) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用例/配置名称',
  `project_id` bigint(20) NULL DEFAULT NULL COMMENT '所属项目',
  `module_id` bigint(20) NULL DEFAULT NULL COMMENT '所属模块',
  `status` int(11) NULL DEFAULT 10 COMMENT '用例状态 10, 生效 ， 20 失效',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '接口code',
  `code_id` bigint(20) NULL DEFAULT NULL COMMENT '关联接口id',
  `priority` int(11) NULL DEFAULT NULL COMMENT '优先级',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '请求地址',
  `method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '请求方法',
  `tags` json NULL COMMENT '用例标签',
  `enable` int(11) NULL DEFAULT 1,
  `teardown_hooks` json NULL COMMENT '后置操作',
  `setup_hooks` json NULL COMMENT '前置操作',
  `variables` json NULL COMMENT '变量',
  `request` json NULL COMMENT '请求参数',
  `validators` json NULL COMMENT '断言规则',
  `extracts` json NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `pre_steps` json NULL,
  `post_steps` json NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `step_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `export` json NULL,
  `headers` json NULL,
  `setup_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `teardown_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `step_id` bigint(20) NULL DEFAULT NULL,
  `parent_step_id` bigint(20) NULL DEFAULT NULL,
  `index` int(11) NULL DEFAULT NULL,
  `node_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `version` int(11) NULL DEFAULT 0,
  `is_quotation` int(2) NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_case_step
-- ----------------------------

-- ----------------------------
-- Table structure for api_info
-- ----------------------------
DROP TABLE IF EXISTS `api_info`;
CREATE TABLE `api_info`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用例/配置名称',
  `project_id` bigint(20) NULL DEFAULT NULL COMMENT '所属项目',
  `module_id` bigint(20) NULL DEFAULT NULL COMMENT '所属模块',
  `status` int(11) NULL DEFAULT 10 COMMENT '用例状态 10, 生效 ， 20 失效',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '接口code',
  `code_id` bigint(20) NULL DEFAULT NULL COMMENT '关联接口id',
  `priority` int(11) NULL DEFAULT NULL COMMENT '优先级',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '请求地址',
  `method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '请求方法',
  `tags` json NULL COMMENT '用例标签',
  `enable` int(11) NULL DEFAULT NULL,
  `teardown_hooks` json NULL COMMENT '后置操作',
  `setup_hooks` json NULL COMMENT '前置操作',
  `variables` json NULL COMMENT '变量',
  `request` json NULL COMMENT '请求参数',
  `validators` json NULL COMMENT '断言规则',
  `extracts` json NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `pre_steps` json NULL,
  `post_steps` json NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `step_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `export` json NULL,
  `headers` json NULL,
  `setup_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `teardown_code` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_info
-- ----------------------------

-- ----------------------------
-- Table structure for api_test_report
-- ----------------------------
DROP TABLE IF EXISTS `api_test_report`;
CREATE TABLE `api_test_report`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '报告名称',
  `start_time` datetime NULL DEFAULT NULL COMMENT '执行时间',
  `duration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '运行耗时',
  `case_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '执行用例id',
  `run_mode` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '运行模式， case 用例， suites 套件',
  `run_type` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '运行类型， 10 同步， 20 异步，30 定时任务',
  `success` int(11) NULL DEFAULT NULL COMMENT '是否成功， True, False',
  `run_count` int(11) NULL DEFAULT NULL COMMENT '运行步骤数',
  `actual_run_count` int(11) NULL DEFAULT NULL COMMENT '实际步骤数',
  `run_success_count` int(11) NULL DEFAULT NULL COMMENT '运行成功数',
  `run_fail_count` int(11) NULL DEFAULT NULL,
  `run_err_count` int(11) NULL DEFAULT NULL,
  `run_skip_count` int(11) NULL DEFAULT NULL COMMENT '跳过',
  `run_log` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '运行日志',
  `project_id` bigint(20) NULL DEFAULT NULL COMMENT '项目id',
  `module_id` bigint(20) NULL DEFAULT NULL COMMENT '模块id',
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1 COMMENT '是否删除, 0 删除 1 非删除',
  `env_id` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `exec_user_id` int(11) NULL DEFAULT NULL,
  `exec_user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `error_msg` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_test_report
-- ----------------------------

-- ----------------------------
-- Table structure for api_test_report_detail_0
-- ----------------------------
DROP TABLE IF EXISTS `api_test_report_detail_0`;
CREATE TABLE `api_test_report_detail_0`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `case_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `success` int(11) NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `step_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `parent_step_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `step_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `env_variables` json NULL,
  `variables` json NULL,
  `case_variables` json NULL,
  `session_data` json NULL,
  `export_vars` json NULL,
  `report_id` int(11) NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1 COMMENT '是否删除, 0 删除 1 非删除',
  `duration` decimal(10, 3) NULL DEFAULT NULL COMMENT '运行耗时',
  `step_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'pre 前置，post 后置，controller 控制器',
  `pre_hook_data` json NULL,
  `post_hook_data` json NULL,
  `setup_hook_results` json NULL COMMENT '前置hook结果',
  `teardown_hook_results` json NULL COMMENT '后置hook结果',
  `index` int(11) NULL DEFAULT NULL,
  `status_code` int(11) NULL DEFAULT NULL,
  `response_time_ms` decimal(10, 2) NULL DEFAULT NULL,
  `elapsed_ms` decimal(10, 2) NULL DEFAULT NULL,
  `log` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `exec_user_id` int(11) NULL DEFAULT NULL,
  `exec_user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `source_id` bigint(20) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_test_report_detail_0
-- ----------------------------

-- ----------------------------
-- Table structure for celery_crontab_schedule
-- ----------------------------
DROP TABLE IF EXISTS `celery_crontab_schedule`;
CREATE TABLE `celery_crontab_schedule`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(240) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `hour` varchar(96) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `day_of_week` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `day_of_month` varchar(124) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `month_of_year` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `timezone` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_crontab_schedule
-- ----------------------------
INSERT INTO `celery_crontab_schedule` VALUES (8, '0', '4', '*', '*', '*', 'Asia/Shanghai', NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `celery_crontab_schedule` VALUES (9, '*', '*', '*', '*', '*', 'Asia/Shanghai', '2023-03-03 14:12:26', '2023-03-03 14:12:26', NULL, NULL, 1, '36c09171a1c54d629beee0e67c53c6d7');
INSERT INTO `celery_crontab_schedule` VALUES (10, '09', '09', '*', '*', '*', 'Asia/Shanghai', '2023-07-17 09:45:17', '2023-07-17 09:45:17', 7, 7, 1, '7a4ceec4cd3b41b4b03971b1300b7cb9');
INSERT INTO `celery_crontab_schedule` VALUES (11, '10', '10', '*', '*', '*', 'Asia/Shanghai', '2023-07-17 09:55:11', '2023-07-17 09:55:11', 7, 7, 1, 'e564a059261540039ca8dfee9a262611');

-- ----------------------------
-- Table structure for celery_interval_schedule
-- ----------------------------
DROP TABLE IF EXISTS `celery_interval_schedule`;
CREATE TABLE `celery_interval_schedule`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_interval_schedule
-- ----------------------------
INSERT INTO `celery_interval_schedule` VALUES (1, 30, 'seconds', '2023-03-06 16:27:29', '2023-03-06 16:27:29', NULL, NULL, 1, '0b1885c0e3214929bd4155c71c1718fd');
INSERT INTO `celery_interval_schedule` VALUES (2, 1, 'minutes', '2023-03-06 16:55:33', '2023-03-06 16:55:33', NULL, NULL, 1, '6b3f067202c14bcc877e02a865214f4d');
INSERT INTO `celery_interval_schedule` VALUES (3, 3, 'minutes', '2023-03-06 17:07:36', '2023-03-06 17:07:36', NULL, NULL, 1, 'cad3a8da8037417faef7a26cd217d25f');
INSERT INTO `celery_interval_schedule` VALUES (4, 40, 'seconds', '2023-04-25 18:52:06', '2023-04-25 18:52:06', 7, 7, 1, '657f88ae298045b9b590131d9ffa5fea');
INSERT INTO `celery_interval_schedule` VALUES (5, 30, 'minutes', '2023-06-22 17:03:36', '2023-06-22 17:03:36', 7, 7, 1, '60f45fd294dc4700ae40264487e7ea05');
INSERT INTO `celery_interval_schedule` VALUES (6, 1, 'hours', '2023-07-05 15:27:39', '2023-07-05 15:27:39', 7, 7, 1, '94c76ab1530745308980ed8c4e39e2a2');
INSERT INTO `celery_interval_schedule` VALUES (7, 29, 'seconds', '2023-07-17 12:02:20', '2023-07-17 12:02:20', 7, 7, 1, '26d3f7ac1b3c493583ed234ad31100bd');
INSERT INTO `celery_interval_schedule` VALUES (8, 3, 'days', '2023-09-18 23:34:24', '2023-09-18 23:34:24', 7, 7, 1, '741516e888224bed94fb604bfcf108ea');
INSERT INTO `celery_interval_schedule` VALUES (9, 1, 'seconds', '2023-10-23 16:57:24', '2023-10-23 16:57:24', 7, 7, 1, 'c5f86daf0291470faab14ec8ba4f1bc6');

-- ----------------------------
-- Table structure for celery_periodic_task
-- ----------------------------
DROP TABLE IF EXISTS `celery_periodic_task`;
CREATE TABLE `celery_periodic_task`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `task` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `interval_id` int(11) NULL DEFAULT NULL,
  `crontab` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `crontab_id` int(11) NULL DEFAULT NULL,
  `solar_id` int(11) NULL DEFAULT NULL,
  `args` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `kwargs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `queue` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `exchange` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `routing_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `priority` int(11) NULL DEFAULT NULL,
  `expires` datetime NULL DEFAULT NULL,
  `one_off` tinyint(1) NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `enabled` tinyint(1) NULL DEFAULT NULL,
  `last_run_at` datetime NULL DEFAULT NULL,
  `total_run_count` int(11) NULL DEFAULT NULL,
  `date_changed` datetime NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `run_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `project_id` bigint(20) NULL DEFAULT NULL,
  `module_id` bigint(20) NULL DEFAULT NULL,
  `suite_id` int(11) NULL DEFAULT NULL,
  `case_ids` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `ui_env_id` bigint(20) NULL DEFAULT NULL,
  `ui_ids` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `script_ids` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT NULL,
  `run_mode` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `task_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'crontab interval',
  `case_env_id` bigint(20) NULL DEFAULT NULL,
  `interval_every` int(11) NULL DEFAULT NULL,
  `interval_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `task_tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_periodic_task
-- ----------------------------
INSERT INTO `celery_periodic_task` VALUES (13, 'bzx_test001', 'zerorunner.batch_async_run_testcase', NULL, NULL, NULL, NULL, NULL, '{\"case_ids\": [\"29\"], \"case_env_id\": 24, \"ui_ids\": null, \"ui_env_id\": null, \"name\": \"bzx_test001\", \"project_id\": 588, \"run_type\": \"timed_task\", \"run_mode\": 30, \"env_id\": null, \"exec_user_id\": 1, \"exec_user_name\": \"\\u5c0f\\u767d\"}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, 0, NULL, NULL, NULL, 588, NULL, NULL, '29', NULL, NULL, NULL, '2023-10-23 12:09:55', '2023-10-23 12:42:21', 1, 1, 1, NULL, '9955ba80ac1f48119b5096178fd75809', 'interval', 24, 1, 'minutes', '测试任务bzx_', NULL);
INSERT INTO `celery_periodic_task` VALUES (16, '323', 'zerorunner.batch_async_run_testcase', 9, '1-2 * * * * ? ', NULL, NULL, NULL, '{\"case_ids\": [\"29\", \"30\"], \"case_env_id\": 25, \"ui_ids\": null, \"ui_env_id\": null, \"name\": \"323\", \"project_id\": 581, \"run_type\": 30, \"run_mode\": null, \"env_id\": null, \"exec_user_id\": 7, \"exec_user_name\": \"admin\"}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, 0, NULL, NULL, NULL, 581, NULL, NULL, '29,30', NULL, NULL, NULL, '2023-10-23 16:57:24', '2023-10-23 16:57:24', 7, 7, 1, NULL, 'c5f86daf0291470faab14ec8ba4f1bc6', 'interval', 25, 1, 'seconds', '', NULL);

-- ----------------------------
-- Table structure for celery_periodic_task_changed
-- ----------------------------
DROP TABLE IF EXISTS `celery_periodic_task_changed`;
CREATE TABLE `celery_periodic_task_changed`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_update` datetime NOT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_periodic_task_changed
-- ----------------------------
INSERT INTO `celery_periodic_task_changed` VALUES (1, '2023-10-23 16:57:24', NULL, NULL, '2023-10-23 16:57:24', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for celery_solar_schedule
-- ----------------------------
DROP TABLE IF EXISTS `celery_solar_schedule`;
CREATE TABLE `celery_solar_schedule`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `latitude` float NULL DEFAULT NULL,
  `longitude` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_solar_schedule
-- ----------------------------

-- ----------------------------
-- Table structure for celery_task_record
-- ----------------------------
DROP TABLE IF EXISTS `celery_task_record`;
CREATE TABLE `celery_task_record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `task_type` int(11) NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `end_time` datetime NULL DEFAULT NULL,
  `duration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `traceback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `business_id` bigint(20) NULL DEFAULT NULL,
  `kwargs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `args` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_task_record
-- ----------------------------
INSERT INTO `celery_task_record` VALUES (1, 'e6b3c0d4-5c98-422e-a01e-14bd10b8ac18', 'zerorunner.batch_async_run_testcase', 20, 'SUCCESS', 'None', '2023-10-23 16:57:35', '2023-10-23 16:57:35', NULL, NULL, '2023-10-23 16:57:35', 0, '2023-10-23 16:57:35', 0, 1, '7ba6eb5fe9ea45f3b1a2903de464d4e6', 16, '{\"case_ids\": [\"29\", \"30\"], \"case_env_id\": 25, \"ui_ids\": null, \"ui_env_id\": null, \"name\": \"323\", \"project_id\": 581, \"run_type\": 30, \"run_mode\": null, \"env_id\": null, \"exec_user_id\": 7, \"exec_user_name\": \"admin\"}', '[]');
INSERT INTO `celery_task_record` VALUES (2, 'b8745fef-8664-407d-af9b-b63a2652f714', 'celery_worker.tasks.test_case.async_run_testcase', 10, 'SUCCESS', 'None', '2023-10-23 16:57:35', '2023-10-23 16:57:36', NULL, NULL, '2023-10-23 16:57:35', 0, '2023-10-23 16:57:35', 0, 1, '7ba6eb5fe9ea45f3b1a2903de464d4e6', 30, '{\"case_ids\": [\"29\", \"30\"], \"case_env_id\": 25, \"ui_ids\": null, \"ui_env_id\": null, \"name\": \"323\", \"project_id\": 581, \"run_type\": 30, \"run_mode\": null, \"env_id\": null, \"exec_user_id\": 7, \"exec_user_name\": \"admin\"}', '[\"30\"]');
INSERT INTO `celery_task_record` VALUES (3, '3869911b-6f15-4a09-9c25-b93887511baf', 'celery_worker.tasks.test_case.async_run_testcase', 10, 'SUCCESS', 'None', '2023-10-23 16:57:35', '2023-10-23 16:57:36', NULL, NULL, '2023-10-23 16:57:35', 0, '2023-10-23 16:57:35', 0, 1, '7ba6eb5fe9ea45f3b1a2903de464d4e6', 29, '{\"case_ids\": [\"29\", \"30\"], \"case_env_id\": 25, \"ui_ids\": null, \"ui_env_id\": null, \"name\": \"323\", \"project_id\": 581, \"run_type\": 30, \"run_mode\": null, \"env_id\": null, \"exec_user_id\": 7, \"exec_user_name\": \"admin\"}', '[\"29\"]');
INSERT INTO `celery_task_record` VALUES (4, '2b35ba01-4c10-46d7-b182-7f0fd8c5adec', 'celery_worker.tasks.test_case.async_run_testcase', 10, 'FAILURE', 'parse_obj() got an unexpected keyword argument \'env_id\'', '2023-10-24 09:55:18', '2023-10-24 09:55:27', NULL, 'Traceback (most recent call last):\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\venv\\lib\\site-packages\\celery\\app\\trace.py\", line 477, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\celery_worker\\worker.py\", line 186, in __call__\n    return WorkerPool.run(self.run(*args, **kwargs))\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\autotest\\utils\\async_converter.py\", line 181, in run\n    raise error\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\celery_worker\\tasks\\test_case.py\", line 67, in async_run_testcase\n    run_params = TestCaseRun.parse_obj(case_info, env_id=kwargs.get(\'case_env_id\', None))\n  File \"pydantic\\main.py\", line 519, in pydantic.main.BaseModel.parse_obj\nTypeError: parse_obj() got an unexpected keyword argument \'env_id\'\n', '2023-10-24 09:55:17', 0, '2023-10-24 09:55:17', 0, 1, '61664e0683f2449fb08fd8b653f974ed', NULL, '{\"case_id\": 29, \"case_env_id\": null, \"exec_user_id\": 1, \"exec_user_name\": \"\\u5c0f\\u767d\", \"__business_id\": 29, \"callback\": \"<function ApiCaseService.run_callback at 0x000001F031F07670>\"}', '[]');
INSERT INTO `celery_task_record` VALUES (5, 'c3bcd6db-c102-4aeb-ae75-b575e251e7ab', 'celery_worker.tasks.test_case.async_run_testcase', 10, 'FAILURE', 'parse_obj() got an unexpected keyword argument \'env_id\'', '2023-10-24 09:55:28', '2023-10-24 09:55:31', NULL, 'Traceback (most recent call last):\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\venv\\lib\\site-packages\\celery\\app\\trace.py\", line 477, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\celery_worker\\worker.py\", line 186, in __call__\n    return WorkerPool.run(self.run(*args, **kwargs))\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\autotest\\utils\\async_converter.py\", line 181, in run\n    raise error\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\celery_worker\\tasks\\test_case.py\", line 67, in async_run_testcase\n    run_params = TestCaseRun.parse_obj(case_info, env_id=kwargs.get(\'case_env_id\', None))\n  File \"pydantic\\main.py\", line 519, in pydantic.main.BaseModel.parse_obj\nTypeError: parse_obj() got an unexpected keyword argument \'env_id\'\n', '2023-10-24 09:55:27', 0, '2023-10-24 09:55:27', 0, 1, 'ec16eac20e1444ad87d06907b79a9a47', NULL, '{\"case_id\": 29, \"case_env_id\": null, \"exec_user_id\": 1, \"exec_user_name\": \"\\u5c0f\\u767d\", \"__business_id\": 29, \"callback\": \"<function ApiCaseService.run_callback at 0x000001F031F07670>\"}', '[]');
INSERT INTO `celery_task_record` VALUES (6, '1d054b22-0152-465a-8976-71d1adc52ebf', 'celery_worker.tasks.test_case.async_run_api', 10, 'SUCCESS', 'None', '2023-10-24 09:55:38', '2023-10-24 09:55:42', NULL, NULL, '2023-10-24 09:55:38', 0, '2023-10-24 09:55:38', 0, 1, 'ac22956b99c146a6b5db97f00d134070', 1711681836897411071, '{\"id\": 1711681836897411071, \"ids\": [], \"env_id\": null, \"name\": null, \"run_type\": \"api\", \"run_mode\": 20, \"number_of_run\": null, \"exec_user_id\": 1, \"exec_user_name\": \"\\u5c0f\\u767d\", \"api_run_mode\": \"one\"}', '[]');
INSERT INTO `celery_task_record` VALUES (7, '66af1f8c-69f3-4e45-b9c0-fff031cb2e59', 'celery_worker.tasks.test_case.async_run_testcase', 10, 'FAILURE', 'parse_obj() got an unexpected keyword argument \'env_id\'', '2023-10-24 09:56:19', '2023-10-24 09:56:20', NULL, 'Traceback (most recent call last):\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\venv\\lib\\site-packages\\celery\\app\\trace.py\", line 477, in trace_task\n    R = retval = fun(*args, **kwargs)\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\celery_worker\\worker.py\", line 186, in __call__\n    return WorkerPool.run(self.run(*args, **kwargs))\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\autotest\\utils\\async_converter.py\", line 181, in run\n    raise error\n  File \"D:\\codes\\pythonProject\\zerorunner\\backend\\celery_worker\\tasks\\test_case.py\", line 67, in async_run_testcase\n    run_params = TestCaseRun.parse_obj(case_info, env_id=kwargs.get(\'case_env_id\', None))\n  File \"pydantic\\main.py\", line 519, in pydantic.main.BaseModel.parse_obj\nTypeError: parse_obj() got an unexpected keyword argument \'env_id\'\n', '2023-10-24 09:56:18', 0, '2023-10-24 09:56:18', 0, 1, 'a8275996a4fc4126b9e440a1a8533ea8', NULL, '{\"case_id\": 31, \"case_env_id\": null, \"exec_user_id\": 1, \"exec_user_name\": \"\\u5c0f\\u767d\", \"__business_id\": 31, \"callback\": \"<function ApiCaseService.run_callback at 0x000001F031F07670>\"}', '[]');
INSERT INTO `celery_task_record` VALUES (8, 'd28f262a-4901-41fb-a0b7-efa44aaab0fc', 'celery_worker.tasks.test_case.async_run_testcase', 10, 'SUCCESS', 'None', '2023-10-24 09:59:21', '2023-10-24 09:59:26', NULL, NULL, '2023-10-24 09:59:21', 0, '2023-10-24 09:59:21', 0, 1, '28674e45d31a4c2b88fdeaa97f4c5d06', NULL, '{\"case_id\": 31, \"case_env_id\": null, \"exec_user_id\": 1, \"exec_user_name\": \"\\u5c0f\\u767d\", \"__business_id\": 31, \"callback\": \"<function ApiCaseService.run_callback at 0x000002A3C7B05F70>\"}', '[]');
INSERT INTO `celery_task_record` VALUES (9, 'dcf521f9-4fc8-48da-8c1c-45f33c6aa532', 'celery_worker.tasks.test_case.async_run_testcase', 10, 'SUCCESS', 'None', '2023-10-24 10:08:26', '2023-10-24 10:08:26', NULL, NULL, '2023-10-24 10:08:25', 0, '2023-10-24 10:08:25', 0, 1, '84f622f831894506a320539fcd8a22be', NULL, '{\"case_id\": 31, \"case_env_id\": 25, \"exec_user_id\": 7, \"exec_user_name\": \"admin\", \"__business_id\": 31, \"callback\": \"<function ApiCaseService.run_callback at 0x7ff448b42e50>\"}', '[]');
INSERT INTO `celery_task_record` VALUES (10, '5536c2fa-a6ff-4641-a5d1-0b85a34bf354', 'celery_worker.tasks.ui_case.async_run_ui', 10, 'RUNNING', NULL, '2023-10-24 10:08:51', NULL, NULL, NULL, '2023-10-24 10:08:50', 0, '2023-10-24 10:08:50', 0, 1, NULL, 11, '{\"ui_id\": 11, \"env_id\": null, \"exec_user_id\": 7, \"exec_user_name\": \"admin\"}', '[]');

-- ----------------------------
-- Table structure for coverage_backend_report
-- ----------------------------
DROP TABLE IF EXISTS `coverage_backend_report`;
CREATE TABLE `coverage_backend_report`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `report_type` int(11) NULL DEFAULT NULL,
  `new_branches` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `new_last_commit_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `old_branches` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `old_last_commit_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `package_count` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class_count` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `method_count` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `coverage_rate` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of coverage_backend_report
-- ----------------------------
INSERT INTO `coverage_backend_report` VALUES (1, 'zero_java', 20, 'master', NULL, 'test', NULL, NULL, NULL, NULL, NULL, '2023-09-05 17:08:30', 7, '2023-09-05 17:08:30', 7, 1, '743393a0b19d42dbb0754589b3398ce5');
INSERT INTO `coverage_backend_report` VALUES (2, 'zero_java', 20, 'master', NULL, 'test', NULL, NULL, NULL, NULL, NULL, '2023-09-05 17:08:53', 7, '2023-09-05 17:08:53', 7, 1, '839e9bab54ce44afb5435aeb3a2ee91e');
INSERT INTO `coverage_backend_report` VALUES (3, 'zero_java', 20, 'master', NULL, 'test', NULL, NULL, NULL, NULL, NULL, '2023-09-05 17:09:59', 7, '2023-09-05 17:09:59', 7, 1, '8d4914eca7d841e396282ee9a6784405');
INSERT INTO `coverage_backend_report` VALUES (4, 'zero_java', 20, 'master', NULL, 'test', NULL, NULL, NULL, NULL, NULL, '2023-09-05 17:12:02', 7, '2023-09-05 17:12:02', 7, 1, '8411ff66812b4a04a2ae7331485e9017');
INSERT INTO `coverage_backend_report` VALUES (5, 'zero_java', 20, 'master', NULL, 'test', NULL, NULL, NULL, NULL, NULL, '2023-09-05 17:15:25', 7, '2023-09-05 17:15:25', 7, 1, 'ef8c33b4bf2e43058e775aacc1f801fe');
INSERT INTO `coverage_backend_report` VALUES (6, 'zero_java', 20, 'master', NULL, 'test', NULL, NULL, NULL, NULL, NULL, '2023-09-05 17:16:12', 7, '2023-09-05 17:16:12', 7, 1, 'a8389db555a84993b6dfde3b2a02504a');
INSERT INTO `coverage_backend_report` VALUES (7, 'zero_java', 20, 'test', NULL, 'master', NULL, NULL, NULL, NULL, NULL, '2023-09-05 17:18:55', 7, '2023-09-05 17:18:55', 7, 1, '333fb13d16b04b4ba889a865a2469d8e');
INSERT INTO `coverage_backend_report` VALUES (8, 'zero_java', 20, 'master', '', 'master', '', NULL, NULL, NULL, NULL, '2023-09-05 17:33:30', 7, '2023-09-05 17:33:30', 7, 1, 'f877942745f74f639b7b934143c121c8');
INSERT INTO `coverage_backend_report` VALUES (9, 'zero_java', 20, 'test', '', 'master', '', NULL, NULL, NULL, NULL, '2023-09-05 17:33:38', 7, '2023-09-05 17:33:38', 7, 1, '5f195d15742146f8a186f7534a375878');
INSERT INTO `coverage_backend_report` VALUES (10, 'zero_java', 20, 'test', '', 'master', '', NULL, NULL, NULL, NULL, '2023-09-05 17:36:23', 7, '2023-09-05 17:36:23', 7, 1, '47abac21ab8d4d3c90921930228fcaca');
INSERT INTO `coverage_backend_report` VALUES (11, 'zero_java', 20, 'test', 'bdb350cf3fb337d123bab2497f1281fd85826382', 'master', '4c5ef292fe85b5ad47101d2f5f7a629d7fd040d5', NULL, NULL, NULL, NULL, '2023-09-05 17:38:05', 7, '2023-09-05 17:38:05', 7, 1, '61647ab25d704d8b85120b4b416f2070');

-- ----------------------------
-- Table structure for coverage_class_detail
-- ----------------------------
DROP TABLE IF EXISTS `coverage_class_detail`;
CREATE TABLE `coverage_class_detail`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `report_id` bigint(20) NULL DEFAULT NULL,
  `package_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class_file_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `class_source_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class_md5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `branch_missed` int(11) NULL DEFAULT 0,
  `branch_covered` int(11) NULL DEFAULT 0,
  `instruction_missed` int(11) NULL DEFAULT 0,
  `instruction_covered` int(11) NULL DEFAULT 0,
  `line_missed` int(11) NULL DEFAULT 0,
  `line_covered` int(11) NULL DEFAULT 0,
  `complexity_missed` int(11) NULL DEFAULT 0,
  `complexity_covered` int(11) NULL DEFAULT 0,
  `method_missed` int(11) NULL DEFAULT 0,
  `method_covered` int(11) NULL DEFAULT 0,
  `class_missed` int(11) NULL DEFAULT 0,
  `class_covered` int(11) NULL DEFAULT 0,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of coverage_class_detail
-- ----------------------------
INSERT INTO `coverage_class_detail` VALUES (1, 3, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\"add-line \" id=\"L3\" title=\"\">import com.github.pagehelper.PageInfo;</span>\n<span class=\"add-line \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.common.ResponseDataPage;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L6\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import com.zero.zeroAdmin.model.User;</span>\n<span class=\" \" id=\"L8\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L9\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.*;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\" \" id=\"L45\" title=\"\">}</span>\n', NULL, 'nN3T2MSndCMkEGQDr1F7tg==', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, '2023-09-05 09:10:10', NULL, '2023-09-05 09:10:10', NULL, 1, NULL);
INSERT INTO `coverage_class_detail` VALUES (2, 4, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\"add-line \" id=\"L3\" title=\"\">import com.github.pagehelper.PageInfo;</span>\n<span class=\"add-line \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.common.ResponseDataPage;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L6\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import com.zero.zeroAdmin.model.User;</span>\n<span class=\" \" id=\"L8\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L9\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.*;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\" \" id=\"L45\" title=\"\">}</span>\n', NULL, 'nN3T2MSndCMkEGQDr1F7tg==', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, '2023-09-05 09:15:15', NULL, '2023-09-05 09:15:15', NULL, 1, NULL);
INSERT INTO `coverage_class_detail` VALUES (3, 5, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\"add-line \" id=\"L3\" title=\"\">import com.github.pagehelper.PageInfo;</span>\n<span class=\"add-line \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.common.ResponseDataPage;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L6\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import com.zero.zeroAdmin.model.User;</span>\n<span class=\" \" id=\"L8\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L9\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.*;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\" \" id=\"L45\" title=\"\">}</span>\n', NULL, 'nN3T2MSndCMkEGQDr1F7tg==', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, '2023-09-05 09:16:01', NULL, '2023-09-05 09:16:01', NULL, 1, NULL);
INSERT INTO `coverage_class_detail` VALUES (4, 6, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\"add-line \" id=\"L3\" title=\"\">import com.github.pagehelper.PageInfo;</span>\n<span class=\"add-line \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.common.ResponseDataPage;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L6\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import com.zero.zeroAdmin.model.User;</span>\n<span class=\" \" id=\"L8\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L9\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.*;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\" \" id=\"L45\" title=\"\">}</span>\n', NULL, 'nN3T2MSndCMkEGQDr1F7tg==', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, '2023-09-05 09:18:48', NULL, '2023-09-05 09:18:48', NULL, 1, NULL);
INSERT INTO `coverage_class_detail` VALUES (5, 7, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\" \" id=\"L3\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L6\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import org.springframework.web.bind.annotation.RequestBody;</span>\n<span class=\"add-line \" id=\"L8\" title=\"\">import org.springframework.web.bind.annotation.RequestMapping;</span>\n<span class=\"add-line \" id=\"L9\" title=\"\">import org.springframework.web.bind.annotation.RequestMethod;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.RestController;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\"add-line \" id=\"L45\" title=\"\"></span>\n<span class=\"add-line \" id=\"L46\" title=\"\">    @RequestMapping(value = \"/getTest3\", method = RequestMethod.POST)</span>\n<span class=\"add-line \" id=\"L47\" title=\"\">    public ResponseData<String> getTest3() {</span>\n<span class=\"nc add-line \" id=\"L48\" title=\"\">        String test2 = \"getTest3\";</span>\n<span class=\"nc add-line \" id=\"L49\" title=\"\">        userService.getTest();</span>\n<span class=\"nc add-line \" id=\"L50\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\"add-line \" id=\"L51\" title=\"\">    }</span>\n<span class=\" \" id=\"L52\" title=\"\">}</span>\n', NULL, 'Qg8mCLak6vyhs3Vg3fFmIw==', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, '2023-09-05 09:19:07', NULL, '2023-09-05 09:19:07', NULL, 1, NULL);
INSERT INTO `coverage_class_detail` VALUES (6, 9, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\" \" id=\"L3\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L6\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import org.springframework.web.bind.annotation.RequestBody;</span>\n<span class=\"add-line \" id=\"L8\" title=\"\">import org.springframework.web.bind.annotation.RequestMapping;</span>\n<span class=\"add-line \" id=\"L9\" title=\"\">import org.springframework.web.bind.annotation.RequestMethod;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.RestController;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\"add-line \" id=\"L45\" title=\"\"></span>\n<span class=\"add-line \" id=\"L46\" title=\"\">    @RequestMapping(value = \"/getTest3\", method = RequestMethod.POST)</span>\n<span class=\"add-line \" id=\"L47\" title=\"\">    public ResponseData<String> getTest3() {</span>\n<span class=\"nc add-line \" id=\"L48\" title=\"\">        String test2 = \"getTest3\";</span>\n<span class=\"nc add-line \" id=\"L49\" title=\"\">        userService.getTest();</span>\n<span class=\"nc add-line \" id=\"L50\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\"add-line \" id=\"L51\" title=\"\">    }</span>\n<span class=\" \" id=\"L52\" title=\"\">}</span>\n', NULL, 'Qg8mCLak6vyhs3Vg3fFmIw==', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, '2023-09-05 09:33:49', NULL, '2023-09-05 09:33:49', NULL, 1, NULL);
INSERT INTO `coverage_class_detail` VALUES (7, 10, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\" \" id=\"L3\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L6\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import org.springframework.web.bind.annotation.RequestBody;</span>\n<span class=\"add-line \" id=\"L8\" title=\"\">import org.springframework.web.bind.annotation.RequestMapping;</span>\n<span class=\"add-line \" id=\"L9\" title=\"\">import org.springframework.web.bind.annotation.RequestMethod;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.RestController;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\"add-line \" id=\"L45\" title=\"\"></span>\n<span class=\"add-line \" id=\"L46\" title=\"\">    @RequestMapping(value = \"/getTest3\", method = RequestMethod.POST)</span>\n<span class=\"add-line \" id=\"L47\" title=\"\">    public ResponseData<String> getTest3() {</span>\n<span class=\"nc add-line \" id=\"L48\" title=\"\">        String test2 = \"getTest3\";</span>\n<span class=\"nc add-line \" id=\"L49\" title=\"\">        userService.getTest();</span>\n<span class=\"nc add-line \" id=\"L50\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\"add-line \" id=\"L51\" title=\"\">    }</span>\n<span class=\" \" id=\"L52\" title=\"\">}</span>\n', NULL, 'Qg8mCLak6vyhs3Vg3fFmIw==', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, '2023-09-05 09:36:36', NULL, '2023-09-05 09:36:36', NULL, 1, NULL);
INSERT INTO `coverage_class_detail` VALUES (8, 11, 'com/zero/zeroAdmin/controller', 'com/zero/zeroAdmin/controller/UserController', '<span class=\" \" id=\"L1\" title=\"\">package com.zero.zeroAdmin.controller;</span>\n<span class=\" \" id=\"L2\" title=\"\"></span>\n<span class=\" \" id=\"L3\" title=\"\">import com.zero.zeroAdmin.common.ResponseData;</span>\n<span class=\" \" id=\"L4\" title=\"\">import com.zero.zeroAdmin.dto.UserParams;</span>\n<span class=\" \" id=\"L5\" title=\"\">import com.zero.zeroAdmin.service.UserService;</span>\n<span class=\" \" id=\"L6\" title=\"\">import org.springframework.beans.factory.annotation.Autowired;</span>\n<span class=\"add-line \" id=\"L7\" title=\"\">import org.springframework.web.bind.annotation.RequestBody;</span>\n<span class=\"add-line \" id=\"L8\" title=\"\">import org.springframework.web.bind.annotation.RequestMapping;</span>\n<span class=\"add-line \" id=\"L9\" title=\"\">import org.springframework.web.bind.annotation.RequestMethod;</span>\n<span class=\"add-line \" id=\"L10\" title=\"\">import org.springframework.web.bind.annotation.RestController;</span>\n<span class=\" \" id=\"L11\" title=\"\"></span>\n<span class=\" \" id=\"L12\" title=\"\">import java.util.List;</span>\n<span class=\" \" id=\"L13\" title=\"\"></span>\n<span class=\" \" id=\"L14\" title=\"\">@RestController</span>\n<span class=\" \" id=\"L15\" title=\"\">@RequestMapping(\"/user\")</span>\n<span class=\" \" id=\"L16\" title=\"\">public class UserController {</span>\n<span class=\" \" id=\"L17\" title=\"\">    @Autowired</span>\n<span class=\" \" id=\"L18\" title=\"\">    UserService userService;</span>\n<span class=\" \" id=\"L19\" title=\"\"></span>\n<span class=\" \" id=\"L20\" title=\"\">    @RequestMapping(value = \"/getUserListNew\", method = RequestMethod.GET)</span>\n<span class=\" \" id=\"L21\" title=\"\">    public ResponseData<String> getUserListNew(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L22\" title=\"\">        String test = \"test\";</span>\n<span class=\" \" id=\"L23\" title=\"\">        return ResponseData.success(test);</span>\n<span class=\" \" id=\"L24\" title=\"\">    }</span>\n<span class=\" \" id=\"L25\" title=\"\"></span>\n<span class=\" \" id=\"L26\" title=\"\">    @RequestMapping(value = \"/getUserList\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L27\" title=\"\">    public ResponseData<String> getUserList(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L28\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L29\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L30\" title=\"\">    }</span>\n<span class=\" \" id=\"L31\" title=\"\"></span>\n<span class=\" \" id=\"L32\" title=\"\">    @RequestMapping(value = \"/getUserListAll\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L33\" title=\"\">    public ResponseData<List<String>> getUserListAll(@RequestBody UserParams userParams) {</span>\n<span class=\" \" id=\"L34\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L35\" title=\"\">        List<String> data = userService.listAll(userParams.getId());</span>\n<span class=\" \" id=\"L36\" title=\"\">        return ResponseData.success(data);</span>\n<span class=\" \" id=\"L37\" title=\"\">    }</span>\n<span class=\" \" id=\"L38\" title=\"\"></span>\n<span class=\" \" id=\"L39\" title=\"\">    @RequestMapping(value = \"/getTest\", method = RequestMethod.POST)</span>\n<span class=\" \" id=\"L40\" title=\"\">    public ResponseData<String> getTest() {</span>\n<span class=\" \" id=\"L41\" title=\"\">        String test2 = \"test2\";</span>\n<span class=\" \" id=\"L42\" title=\"\">        userService.getTest();</span>\n<span class=\" \" id=\"L43\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\" \" id=\"L44\" title=\"\">    }</span>\n<span class=\"add-line \" id=\"L45\" title=\"\"></span>\n<span class=\"add-line \" id=\"L46\" title=\"\">    @RequestMapping(value = \"/getTest3\", method = RequestMethod.POST)</span>\n<span class=\"add-line \" id=\"L47\" title=\"\">    public ResponseData<String> getTest3() {</span>\n<span class=\"nc add-line \" id=\"L48\" title=\"\">        String test2 = \"getTest3\";</span>\n<span class=\"nc add-line \" id=\"L49\" title=\"\">        userService.getTest();</span>\n<span class=\"nc add-line \" id=\"L50\" title=\"\">        return ResponseData.success(test2);</span>\n<span class=\"add-line \" id=\"L51\" title=\"\">    }</span>\n<span class=\" \" id=\"L52\" title=\"\">}</span>\n', NULL, 'Qg8mCLak6vyhs3Vg3fFmIw==', 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, '2023-09-05 09:38:17', NULL, '2023-09-05 09:38:17', NULL, 1, NULL);

-- ----------------------------
-- Table structure for coverage_method_detail
-- ----------------------------
DROP TABLE IF EXISTS `coverage_method_detail`;
CREATE TABLE `coverage_method_detail`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `report_id` bigint(20) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `method_md5` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class_id` int(11) NULL DEFAULT NULL,
  `params_string` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `offset` int(11) NULL DEFAULT NULL,
  `branch_missed` int(11) NULL DEFAULT 0,
  `branch_covered` int(11) NULL DEFAULT 0,
  `instruction_missed` int(11) NULL DEFAULT 0,
  `instruction_covered` int(11) NULL DEFAULT 0,
  `line_missed` int(11) NULL DEFAULT 0,
  `line_covered` int(11) NULL DEFAULT 0,
  `complexity_missed` int(11) NULL DEFAULT 0,
  `complexity_covered` int(11) NULL DEFAULT 0,
  `method_missed` int(11) NULL DEFAULT 0,
  `method_covered` int(11) NULL DEFAULT 0,
  `lines_covered_status` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of coverage_method_detail
-- ----------------------------
INSERT INTO `coverage_method_detail` VALUES (1, 7, 'getTest3', '/+LqNsdHT/30lzOD2Vurhw==', 5, '()', 48, 0, 0, 8, 0, 3, 0, 1, 0, 1, 0, '1,1,1', '2023-09-05 09:19:07', NULL, '2023-09-05 09:19:07', NULL, 1, NULL);
INSERT INTO `coverage_method_detail` VALUES (2, 9, 'getTest3', '/+LqNsdHT/30lzOD2Vurhw==', 6, '()', 48, 0, 0, 8, 0, 3, 0, 1, 0, 1, 0, '1,1,1', '2023-09-05 09:33:49', NULL, '2023-09-05 09:33:49', NULL, 1, NULL);
INSERT INTO `coverage_method_detail` VALUES (3, 10, 'getTest3', '/+LqNsdHT/30lzOD2Vurhw==', 7, '()', 48, 0, 0, 8, 0, 3, 0, 1, 0, 1, 0, '1,1,1', '2023-09-05 09:36:36', NULL, '2023-09-05 09:36:36', NULL, 1, NULL);
INSERT INTO `coverage_method_detail` VALUES (4, 11, 'getTest3', '/+LqNsdHT/30lzOD2Vurhw==', 8, '()', 48, 0, 0, 8, 0, 3, 0, 1, 0, 1, 0, '1,1,1', '2023-09-05 09:38:17', NULL, '2023-09-05 09:38:17', NULL, 1, NULL);

-- ----------------------------
-- Table structure for data_source
-- ----------------------------
DROP TABLE IF EXISTS `data_source`;
CREATE TABLE `data_source`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源类型',
  `host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '主机名',
  `port` int(11) NULL DEFAULT NULL COMMENT '端口',
  `user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源名称',
  `env_id` int(11) NULL DEFAULT NULL COMMENT '所属环境id',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `enabled_flag` tinyint(1) NULL DEFAULT 1 COMMENT '是否删除',
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of data_source
-- ----------------------------
INSERT INTO `data_source` VALUES (1, 'mysql', 'xiaobaicodes.com', 3306, 'zero_autotest', 'Bai.123456', 'zero_autotest', 8, NULL, '2023-05-17 19:15:00', 0, 7, 7, NULL);
INSERT INTO `data_source` VALUES (2, 'mysql', '127.0.0.1', 8888, 'xioabai', 'passwowrd', 'test', NULL, '2022-09-21 14:19:30', '2023-05-17 19:15:02', 0, 7, 7, NULL);
INSERT INTO `data_source` VALUES (3, 'mysql', '127.0.0.1', 8888, 'xiaobao', 'xiaobai', 'test12', NULL, '2022-09-21 14:32:58', '2023-05-17 19:15:02', 0, 7, 7, NULL);
INSERT INTO `data_source` VALUES (4, 'mysql', 'test', 3006, '', '', 'test', 7, '2022-10-10 17:19:09', '2023-05-17 19:15:03', 0, 7, 7, NULL);
INSERT INTO `data_source` VALUES (5, 'mysql', 'xiaobaicodes.com', 13306, 'zero_test_user', 'eJFYXP37KuEAMityTmfpPBTSgLGTHRLfhpPWRhlatEW0JToXixMaLcdMld6gGn2Lmz7ArYG90IMbyhs+to6lxPi7o/8tzdKYuobVBAyaXm7Zu7wkM2eWGqFXKRxs75Y77AgGyJ3ODx+ho1eiqQ/yp9OH6V4dw/fmftl5RkDlhrk=', 'zero_测试数据库', NULL, '2023-02-06 14:49:17', '2023-05-17 17:03:39', 1, 7, 7, 'db0ad77b991444caa1c86be7a4ab1949');
INSERT INTO `data_source` VALUES (6, 'mysql', 'xiaobaicodes.com', 3306, 'zero_autotest', 'Bai.123456', 'zero_autotest', NULL, '2023-05-15 09:25:36', '2023-05-17 19:15:04', 0, 7, 7, '26d311a7ea154a38a3c9b41559fffd22');

-- ----------------------------
-- Table structure for env
-- ----------------------------
DROP TABLE IF EXISTS `env`;
CREATE TABLE `env`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `domain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '环境域名',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int(11) NOT NULL DEFAULT 1,
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `variables` json NULL COMMENT '环境变量',
  `headers` json NULL COMMENT '环境请求头',
  `data_sources` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env
-- ----------------------------
INSERT INTO `env` VALUES (24, '自营', 'http://t.weather.sojson.com', '', '2023-10-11 14:28:02', '2023-10-13 15:15:18', 1, 7, 7, '[]', '[]', 'null', 'f74ea7c96f4f4b76b43280e642028d9a');
INSERT INTO `env` VALUES (25, '百度测试', 'www.baidu.com', '', '2023-10-13 18:03:06', '2023-10-18 17:14:39', 1, 7, 1, '[{\"key\": \"req\", \"value\": \"${get_rand(size=5)}\", \"remarks\": \"\"}, {\"key\": \"b\", \"value\": \"$a\", \"remarks\": \"\"}, {\"key\": \"a\", \"value\": \"1\", \"remarks\": \"\"}]', '[]', 'null', '860c96bbc52e4923951ca24b2df9f1eb');

-- ----------------------------
-- Table structure for env_config
-- ----------------------------
DROP TABLE IF EXISTS `env_config`;
CREATE TABLE `env_config`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '环境名称',
  `domain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '环境域名',
  `variables` json NULL COMMENT '环境变量',
  `headers` json NULL COMMENT '环境请求头',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int(11) NOT NULL DEFAULT 1,
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env_config
-- ----------------------------

-- ----------------------------
-- Table structure for env_data_source
-- ----------------------------
DROP TABLE IF EXISTS `env_data_source`;
CREATE TABLE `env_data_source`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `env_id` int(11) NULL DEFAULT NULL,
  `data_source_id` int(11) NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `creation_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_id`(`id`) USING BTREE,
  INDEX `index_env_id`(`env_id`) USING BTREE,
  INDEX `index_data_source_id`(`data_source_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 54 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env_data_source
-- ----------------------------
INSERT INTO `env_data_source` VALUES (17, 1, 1, 1, '2023-03-10 16:46:28', '2023-03-10 16:46:28', '7', '7', NULL);
INSERT INTO `env_data_source` VALUES (18, 1, 2, 1, '2023-03-10 16:46:28', '2023-03-10 16:46:28', '7', '7', NULL);
INSERT INTO `env_data_source` VALUES (37, 8, 5, 1, '2023-04-21 16:03:04', '2023-04-21 16:03:04', '7', '7', NULL);
INSERT INTO `env_data_source` VALUES (38, NULL, NULL, 1, '2023-04-21 16:07:36', '2023-04-21 16:07:36', NULL, NULL, NULL);
INSERT INTO `env_data_source` VALUES (39, NULL, NULL, 1, '2023-04-21 16:07:48', '2023-04-21 16:07:48', NULL, NULL, NULL);
INSERT INTO `env_data_source` VALUES (41, NULL, NULL, 1, '2023-04-21 16:22:54', '2023-04-21 16:22:54', NULL, NULL, NULL);
INSERT INTO `env_data_source` VALUES (43, NULL, NULL, 1, '2023-04-28 14:14:15', '2023-04-28 14:14:15', NULL, NULL, NULL);
INSERT INTO `env_data_source` VALUES (46, 15, 5, 1, '2023-05-03 20:51:31', '2023-05-03 20:51:31', '7', '7', NULL);
INSERT INTO `env_data_source` VALUES (47, NULL, NULL, 1, '2023-05-20 09:25:06', '2023-05-20 09:25:06', NULL, NULL, NULL);
INSERT INTO `env_data_source` VALUES (48, NULL, NULL, 1, '2023-06-15 22:09:57', '2023-06-15 22:09:57', NULL, NULL, NULL);
INSERT INTO `env_data_source` VALUES (49, 14, 5, 1, '2023-06-15 22:10:29', '2023-06-15 22:10:29', '7', '7', '7177e7f6645046cf8fd40c2d388c8d72');
INSERT INTO `env_data_source` VALUES (50, 20, 5, 1, '2023-07-05 15:31:04', '2023-07-05 15:31:04', '7', '7', 'f128bd51b11644efa13c996da199beb4');
INSERT INTO `env_data_source` VALUES (51, 7, 5, 1, '2023-08-22 14:42:25', '2023-08-22 14:42:25', '7', '7', 'a29b2fe6cd2544559914e09c0583f927');
INSERT INTO `env_data_source` VALUES (52, 23, 5, 1, '2023-09-08 16:09:29', '2023-09-08 16:09:29', '7', '7', '1813351b1d0f4bd4893dd07ee541dcbb');
INSERT INTO `env_data_source` VALUES (53, 24, 5, 1, '2023-10-13 15:15:07', '2023-10-13 15:15:07', '7', '7', '931c8a1b06244362911cbbc957458cd3');

-- ----------------------------
-- Table structure for env_func
-- ----------------------------
DROP TABLE IF EXISTS `env_func`;
CREATE TABLE `env_func`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `env_id` int(11) NULL DEFAULT NULL,
  `func_id` int(11) NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `creation_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_id`(`id`) USING BTREE,
  INDEX `index_env_id`(`env_id`) USING BTREE,
  INDEX `index_data_source_id`(`func_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env_func
-- ----------------------------
INSERT INTO `env_func` VALUES (2, NULL, NULL, 1, '2023-04-24 11:19:25', '2023-04-24 11:19:25', NULL, NULL, NULL);
INSERT INTO `env_func` VALUES (4, NULL, NULL, 1, '2023-04-28 14:22:41', '2023-04-28 14:22:41', NULL, NULL, NULL);
INSERT INTO `env_func` VALUES (5, NULL, NULL, 1, '2023-05-20 09:25:12', '2023-05-20 09:25:12', NULL, NULL, NULL);
INSERT INTO `env_func` VALUES (6, 15, 4, 1, '2023-05-31 14:04:23', '2023-05-31 14:04:23', '7', '7', '0ac63d50e6744d9781c98bd3b0ccbe42');
INSERT INTO `env_func` VALUES (7, 15, 3, 1, '2023-05-31 14:04:23', '2023-05-31 14:04:23', '7', '7', '0ac63d50e6744d9781c98bd3b0ccbe42');
INSERT INTO `env_func` VALUES (9, 20, 3, 1, '2023-08-07 14:39:59', '2023-08-07 14:39:59', '7', '7', 'f64f28eb814e412abc6c3f4e64bd6ed9');
INSERT INTO `env_func` VALUES (11, 23, 3, 1, '2023-09-08 16:09:18', '2023-09-08 16:09:18', '7', '7', 'b11e7ec40ddb4e6b8f3789dd763f6f23');
INSERT INTO `env_func` VALUES (12, 23, 4, 1, '2023-09-19 11:22:15', '2023-09-19 11:22:15', '7', '7', '66236dfcfce5485dbf09919cee0c4853');
INSERT INTO `env_func` VALUES (13, 24, 3, 1, '2023-10-13 15:15:12', '2023-10-13 15:15:12', '7', '7', '19c51e4214194b9888a90b544b212ca8');
INSERT INTO `env_func` VALUES (14, 24, 4, 1, '2023-10-13 15:15:12', '2023-10-13 15:15:12', '7', '7', '19c51e4214194b9888a90b544b212ca8');
INSERT INTO `env_func` VALUES (16, 8, 3, 1, '2023-10-19 12:04:15', '2023-10-19 12:04:15', '1', '1', '2d2861a41a1a4f59afc76ff7f455f766');
INSERT INTO `env_func` VALUES (17, 25, 4, 1, '2023-10-19 15:38:20', '2023-10-19 15:38:20', '1', '1', '0135d142e7ef43debda7e128ab42a920');
INSERT INTO `env_func` VALUES (18, 25, 3, 1, '2023-10-19 15:38:20', '2023-10-19 15:38:20', '1', '1', '0135d142e7ef43debda7e128ab42a920');

-- ----------------------------
-- Table structure for file_info
-- ----------------------------
DROP TABLE IF EXISTS `file_info`;
CREATE TABLE `file_info`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '存储的文件名',
  `file_path` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '文件路径',
  `extend_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '扩展名称',
  `original_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '原名称',
  `content_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '文件类型',
  `file_size` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '文件大小',
  `id` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_file_info_extend_name`(`extend_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of file_info
-- ----------------------------

-- ----------------------------
-- Table structure for functions
-- ----------------------------
DROP TABLE IF EXISTS `functions`;
CREATE TABLE `functions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `func_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `func_tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of functions
-- ----------------------------
INSERT INTO `functions` VALUES (1, NULL, '\"\"\"\n基本函数实现\n提供使用中使用的获取随机数，时间等基本方法\n\"\"\"\nimport os\nimport random\nimport traceback\nimport shutil\nimport time\nimport datetime\nimport arrow as arrow\nimport math\nimport uuid\n\n\n\n# -----------------------------------  随机  ----------------------------------------------\n\ndef get_randint(min_num=0, max_num=100):\n    \"\"\"\n    生成指定范围随机整数\n    :param min_num: 最小数\n    :param max_num: 最大数\n    :return: number\n    \"\"\"\n    return random.randint(min_num, max_num)\n\n\ndef get_rand(size=5):\n    \"\"\"\n    生成指定位数随机数\n    :param size:\n    :return:\n    \"\"\"\n    value = int(random.random() * math.pow(10, size))\n    if len(str(value)) < size:\n        value = value * math.pow(10, size - len(str(value)))\n    return int(value)\n\n\ndef get_rand_chinese(size=1):\n    \"\"\"\n    生成指定位数随机中文\n    :param size:\n    :return:\n    \"\"\"\n    rand_str = \'\'\n    for i in range(size):\n        head = random.randint(0xb0, 0xf7)\n        body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围\n        val = f\'{head:x}{body:x}\'\n        rand_str = rand_str + bytes.fromhex(val).decode(\'gb2312\')\n    return rand_str\n\n\ndef get_uuid(size=32):\n    \"\"\"\n    生成随机字符,默认32位\n    :param size:\n    :return:\n    \"\"\"\n    return str(uuid.uuid1()).replace(\'-\', \'\')[0:size]\n\n\ndef int_to_str(str):\n    \"\"\"\n    数字转字段串，JS超过15位后，精度会丢失，\n    :param str:\n    :return:\n    \"\"\"\n    try:\n        return int(str)\n    except:\n        return str\n\n\ndef sum_number(num1=0, num2=0):\n    \"\"\"\n    返回两个数字相加\n    :param num1:\n    :param num2:\n    :return:\n    \"\"\"\n    try:\n        sum = num1 + num2\n    except:\n        sum = \"参数错误，请检查\"\n    return sum\n\n\n# -----------------------------------  时间 ----------------------------------------------\ndef get_timestamp():\n    \"\"\"\n    成当前时间戳\n    :return: timestamp\n    \"\"\"\n    return int(round(time.time() * 1000))\n\n\ndef time_sleep(seconds=0):\n    \"\"\"\n    线程睡眠，对进程挂起,seconds:秒数\n    :param seconds:\n    :return:\n    \"\"\"\n    time.sleep(seconds)\n\n\ndef get_time(time_type=1, day=0, add_time_unit=\"days\"):\n    \"\"\"\n    生成当前时间字符\n    :param time_type: 时间格式类型 day 增加天数 add_time_unit 增加时间单位\n    :param day:\n    :param add_time_unit:\n    :return:\n    \"\"\"\n    format_json = {\n        1: \'%Y-%m-%d %H:%M:%S\',\n        2: \'%Y-%m-%d %H:%M\',\n        3: \'%Y-%m-%d %H\',\n        4: \'%Y-%m-%d\',\n        5: \'%Y-%m\',\n        6: \'%Y\',\n        7: \'%Y%m%d%H%M%S\',\n        8: \'%Y%m%d%H%M\',\n        9: \'%Y%m%d%H\',\n        10: \'%Y%m%d\',\n        11: \'%Y%m\',\n        12: \'%M\',\n        13: \'%d\',\n        14: \'%H\',\n        15: \'%M\',\n        16: \'%S\',\n        17: \'%Y-%m-%dT%H:%M:%S\'\n    }\n\n    data_format = format_json.get(time_type)\n    if add_time_unit == \'hours\':\n        return (datetime.datetime.now() + datetime.timedelta(hours=day)).strftime(data_format)\n    if add_time_unit == \'minutes\':\n        return (datetime.datetime.now() + datetime.timedelta(minutes=day)).strftime(data_format)\n    if add_time_unit == \'seconds\':\n        return (datetime.datetime.now() + datetime.timedelta(seconds=day)).strftime(data_format)\n    if add_time_unit == \'weeks\':\n        return (datetime.datetime.now() + datetime.timedelta(weeks=day)).strftime(data_format)\n\n    return (datetime.datetime.now() + datetime.timedelta(days=day)).strftime(data_format)\n\n\ndef get_today_start():\n    \"\"\"获取今天开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"day\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_today_start_timestamp():\n    \"\"\"获取今天开始时间搓\"\"\"\n    return int(time.mktime(time.strptime(str(get_today_start()), \'%Y-%m-%d %H:%M:%S\')) * 1000)\n\n\ndef get_today_end():\n    \"\"\"获取今天结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"day\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_today_end_timestamp():\n    \"\"\"获取今天开始时间搓\"\"\"\n    return int(time.mktime(time.strptime(str(get_today_end()), \'%Y-%m-%d %H:%M:%S\')) * 1000)\n\n\ndef get_week_start():\n    \"\"\"获取当前周开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"week\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_week_end():\n    \"\"\"获取当前周结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"week\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_month_start():\n    \"\"\"获取当前月开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"month\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_month_end():\n    \"\"\"获取当前月结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"month\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_quarter_start():\n    \"\"\"获取当前季度开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"quarter\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_quarter_end():\n    \"\"\"获取当前季度结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"quarter\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_year_start():\n    \"\"\"获取当前年开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"year\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_year_end():\n    \"\"\"获取当前年开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"year\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\n# -----------------------------------  redis操作  ----------------------------------------------\n\ndef redis_get(key):\n    \"\"\"\n    获取key值\n    :param key: key\n    :return:\n    \"\"\"\n    return br.get(key)\n\n\ndef redis_set(key, value, expire=0):\n    \"\"\"\n    插入redis值\n    :param key: key\n    :param value: value\n    :param expire: 时效\n    :return:\n    \"\"\"\n    return br.set(key, value, expire)\n\n\ndef redis_delete(*keys):\n    \"\"\"\n    删除key\n    :param keys: key 列表\n    :return:\n    \"\"\"\n    return br.delete(*keys)\n\n\n# -----------------------------------  db操作  ----------------------------------------------\n\ndef db_execute(host, port, user, password, database, sql):\n    \"\"\"\n    执行sql语句\n    :param host: 数据库地址\n    :param port: 端口号\n    :param user: 用户名\n    :param password: 密码\n    :param database: 数据库\n    :param sql: sql语句\n    :param decrypt: 密码是否加密\n    :return:\n    \"\"\"\n    db = DB(host, port, user, password, database)\n    return db.execute(sql)\n', '2022-12-28 10:56:44', 7, '2023-03-02 16:35:17', 7, 0, '测试函数', NULL, 'eed44d1d097b48e4aeb66f3933e260d9', NULL, NULL);
INSERT INTO `functions` VALUES (2, NULL, '\"\"\"\n基本函数实现\n提供使用中使用的获取随机数，时间等基本方法\n\"\"\"\nimport os\nimport random\nimport traceback\nimport shutil\nimport time\nimport datetime\n\n\n\n# -----------------------------------  随机  ----------------------------------------------\n\ndef get_randint(min_num=0, max_num=100):\n    \"\"\"\n    生成指定范围随机整数\n    :param min_num: 最小数\n    :param max_num: 最大数\n    :return: number\n    \"\"\"\n    return random.randint(min_num, max_num)\n\n\ndef get_rand(size=5):\n    \"\"\"\n    生成指定位数随机数\n    :param size:\n    :return:\n    \"\"\"\n    value = int(random.random() * math.pow(10, size))\n    if len(str(value)) < size:\n        value = value * math.pow(10, size - len(str(value)))\n    return int(value)\n\n\ndef get_rand_chinese(size=1):\n    \"\"\"\n    生成指定位数随机中文\n    :param size:\n    :return:\n    \"\"\"\n    rand_str = \'\'\n    for i in range(size):\n        head = random.randint(0xb0, 0xf7)\n        body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围\n        val = f\'{head:x}{body:x}\'\n        rand_str = rand_str + bytes.fromhex(val).decode(\'gb2312\')\n    return rand_str\n\n\ndef get_uuid(size=32):\n    \"\"\"\n    生成随机字符,默认32位\n    :param size:\n    :return:\n    \"\"\"\n    return str(uuid.uuid4()).replace(\'-\', \'\')[0:size]\n\n\ndef int_to_str(str):\n    \"\"\"\n    数字转字段串，JS超过15位后，精度会丢失，\n    :param str:\n    :return:\n    \"\"\"\n    try:\n        return int(str)\n    except:\n        return str\n\n\ndef sum_number(num1=0, num2=0):\n    \"\"\"\n    返回两个数字相加\n    :param num1:\n    :param num2:\n    :return:\n    \"\"\"\n    try:\n        sum = num1 + num2\n    except:\n        sum = \"参数错误，请检查\"\n    return sum\n\n\n# -----------------------------------  时间 ----------------------------------------------\ndef get_timestamp():\n    \"\"\"\n    成当前时间戳\n    :return: timestamp\n    \"\"\"\n    return int(round(time.time() * 1000))\n\n\ndef time_sleep(seconds=0):\n    \"\"\"\n    线程睡眠，对进程挂起,seconds:秒数\n    :param seconds:\n    :return:\n    \"\"\"\n    time.sleep(seconds)\n\n\ndef get_time(time_type=1, day=0, add_time_unit=\"days\"):\n    \"\"\"\n    生成当前时间字符\n    :param time_type: 时间格式类型 day 增加天数 add_time_unit 增加时间单位\n    :param day:\n    :param add_time_unit:\n    :return:\n    \"\"\"\n    format_json = {\n        1: \'%Y-%m-%d %H:%M:%S\',\n        2: \'%Y-%m-%d %H:%M\',\n        3: \'%Y-%m-%d %H\',\n        4: \'%Y-%m-%d\',\n        5: \'%Y-%m\',\n        6: \'%Y\',\n        7: \'%Y%m%d%H%M%S\',\n        8: \'%Y%m%d%H%M\',\n        9: \'%Y%m%d%H\',\n        10: \'%Y%m%d\',\n        11: \'%Y%m\',\n        12: \'%M\',\n        13: \'%d\',\n        14: \'%H\',\n        15: \'%M\',\n        16: \'%S\',\n        17: \'%Y-%m-%dT%H:%M:%S\'\n    }\n\n    data_format = format_json.get(time_type)\n    if add_time_unit == \'hours\':\n        return (datetime.datetime.now() + datetime.timedelta(hours=day)).strftime(data_format)\n    if add_time_unit == \'minutes\':\n        return (datetime.datetime.now() + datetime.timedelta(minutes=day)).strftime(data_format)\n    if add_time_unit == \'seconds\':\n        return (datetime.datetime.now() + datetime.timedelta(seconds=day)).strftime(data_format)\n    if add_time_unit == \'weeks\':\n        return (datetime.datetime.now() + datetime.timedelta(weeks=day)).strftime(data_format)\n\n    return (datetime.datetime.now() + datetime.timedelta(days=day)).strftime(data_format)\n\n\ndef get_today_start():\n    \"\"\"获取今天开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"day\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_today_start_timestamp():\n    \"\"\"获取今天开始时间搓\"\"\"\n    return int(time.mktime(time.strptime(str(get_today_start()), \'%Y-%m-%d %H:%M:%S\')) * 1000)\n\n\ndef get_today_end():\n    \"\"\"获取今天结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"day\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_today_end_timestamp():\n    \"\"\"获取今天开始时间搓\"\"\"\n    return int(time.mktime(time.strptime(str(get_today_end()), \'%Y-%m-%d %H:%M:%S\')) * 1000)\n\n\ndef get_week_start():\n    \"\"\"获取当前周开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"week\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_week_end():\n    \"\"\"获取当前周结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"week\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_month_start():\n    \"\"\"获取当前月开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"month\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_month_end():\n    \"\"\"获取当前月结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"month\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_quarter_start():\n    \"\"\"获取当前季度开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"quarter\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_quarter_end():\n    \"\"\"获取当前季度结束时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"quarter\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_year_start():\n    \"\"\"获取当前年开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.floor(\"year\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\ndef get_year_end():\n    \"\"\"获取当前年开始时间\"\"\"\n    now = arrow.utcnow().to(\"local\")\n    return now.ceil(\"year\").format(\'YYYY-MM-DD HH:mm:ss\')\n\n\n# -----------------------------------  redis操作  ----------------------------------------------\n\ndef redis_get(key):\n    \"\"\"\n    获取key值\n    :param key: key\n    :return:\n    \"\"\"\n    return br.get(key)\n\n\ndef redis_set(key, value, expire=0):\n    \"\"\"\n    插入redis值\n    :param key: key\n    :param value: value\n    :param expire: 时效\n    :return:\n    \"\"\"\n    return br.set(key, value, expire)\n\n\ndef redis_delete(*keys):\n    \"\"\"\n    删除key\n    :param keys: key 列表\n    :return:\n    \"\"\"\n    return br.delete(*keys)\n\n\n# -----------------------------------  db操作  ----------------------------------------------\n\ndef db_execute(host, port, user, password, database, sql):\n    \"\"\"\n    执行sql语句\n    :param host: 数据库地址\n    :param port: 端口号\n    :param user: 用户名\n    :param password: 密码\n    :param database: 数据库\n    :param sql: sql语句\n    :param decrypt: 密码是否加密\n    :return:\n    \"\"\"\n    db = DB(host, port, user, password, database)\n    return db.execute(sql)\n', '2022-12-28 10:56:55', 7, '2023-05-26 14:16:53', 7, 0, '公共函数', '', '8564a02884804af083a38070b2844514', NULL, NULL);
INSERT INTO `functions` VALUES (3, NULL, 'import random\r\nimport string\r\n\r\ndef random_phone(prefix=\"139\"):\r\n    \"\"\"\r\n    :desc 生成随机手机号码\r\n    :name 手机号码\r\n    :param prefix: 号码前缀\r\n    :return phone<string>: 手机号码\r\n    \"\"\"\r\n    print(prefix)\r\n    random_len=11\r\n    phone_list=[]\r\n    if prefix:\r\n        phone_list.append(prefix)\r\n        random_len = random_len-len(prefix)\r\n    random_list=random.choices(string.digits, k=random_len)\r\n    phone_list.extend(random_list)\r\n    phone=\'\'.join(phone_list)\r\n    return phone\r\n\r\n\r\ndef dictionary_value(val, key):\r\n    \"\"\"\r\n    字典取值\r\n    \"\"\"\r\n    return val[key]\r\n\r\n\r\n\r\ndef get_list_data():\r\n    return [1, 2, 3]', '2022-12-28 10:57:31', 7, '2023-10-19 12:05:25', 1, 1, '测试打的', '', '5556597d2c7a473aa3edbf54c7cf4360', NULL, NULL);
INSERT INTO `functions` VALUES (4, NULL, '\"\"\"\r\n基本函数实现\r\n提供使用中使用的获取随机数，时间等基本方法\r\n\"\"\"\r\nimport os\r\nimport random\r\nimport traceback\r\nimport shutil\r\nimport time\r\nimport datetime\r\nimport arrow\r\nimport math\r\nimport uuid\r\n\r\n\r\n# -----------------------------------  随机  ----------------------------------------------\r\n\r\ndef get_randint(min_num=0, max_num=100):\r\n    \"\"\"\r\n    生成指定范围随机整数\r\n    :param min_num: 最小数\r\n    :param max_num: 最大数\r\n    :return: number\r\n    \"\"\"\r\n    return random.randint(min_num, max_num)\r\n\r\n\r\ndef get_rand(size=5):\r\n    \"\"\"\r\n    生成指定位数随机数\r\n    :param size:\r\n    :return:\r\n    \"\"\"\r\n    value = int(random.random() * math.pow(10, size))\r\n    if len(str(value)) < size:\r\n        value = value * math.pow(10, size - len(str(value)))\r\n    return int(value)\r\n\r\n\r\ndef get_rand_chinese(size=1):\r\n    \"\"\"\r\n    生成指定位数随机中文\r\n    :param size:\r\n    :return:\r\n    \"\"\"\r\n    rand_str = \'\'\r\n    for i in range(size):\r\n        head = random.randint(0xb0, 0xf7)\r\n        body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围\r\n        val = f\'{head:x}{body:x}\'\r\n        rand_str = rand_str + bytes.fromhex(val).decode(\'gb2312\')\r\n    return rand_str\r\n\r\n\r\ndef get_uuid(size=32):\r\n    \"\"\"\r\n    生成随机字符,默认32位\r\n    :param size:\r\n    :return:\r\n    \"\"\"\r\n    return str(uuid.uuid1()).replace(\'-\', \'\')[0:size]\r\n\r\n\r\ndef int_to_str(str):\r\n    \"\"\"\r\n    数字转字段串，JS超过15位后，精度会丢失，\r\n    :param str:\r\n    :return:\r\n    \"\"\"\r\n    try:\r\n        return int(str)\r\n    except:\r\n        return str\r\n\r\n\r\ndef sum_number(num1=0, num2=0):\r\n    \"\"\"\r\n    返回两个数字相加\r\n    :param num1:\r\n    :param num2:\r\n    :return:\r\n    \"\"\"\r\n    try:\r\n        sum = num1 + num2\r\n    except:\r\n        sum = \"参数错误，请检查\"\r\n    return sum\r\n\r\n\r\n# -----------------------------------  时间 ----------------------------------------------\r\ndef get_timestamp():\r\n    \"\"\"\r\n    成当前时间戳\r\n    :return: timestamp\r\n    \"\"\"\r\n    # a = sonsf(1)\r\n    return int(round(time.time() * 1000))\r\n\r\n\r\ndef time_sleep(seconds=0):\r\n    \"\"\"\r\n    线程睡眠，对进程挂起,seconds:秒数\r\n    :param seconds:\r\n    :return:\r\n    \"\"\"\r\n    time.sleep(seconds)\r\n\r\n\r\ndef get_time(time_type=1, day=0, add_time_unit=\"days\"):\r\n    \"\"\"\r\n    生成当前时间字符\r\n    :param time_type: 时间格式类型 day 增加天数 add_time_unit 增加时间单位\r\n    :param day:\r\n    :param add_time_unit:\r\n    :return:\r\n    \"\"\"\r\n    format_json = {\r\n        1: \'%Y-%m-%d %H:%M:%S\',\r\n        2: \'%Y-%m-%d %H:%M\',\r\n        3: \'%Y-%m-%d %H\',\r\n        4: \'%Y-%m-%d\',\r\n        5: \'%Y-%m\',\r\n        6: \'%Y\',\r\n        7: \'%Y%m%d%H%M%S\',\r\n        8: \'%Y%m%d%H%M\',\r\n        9: \'%Y%m%d%H\',\r\n        10: \'%Y%m%d\',\r\n        11: \'%Y%m\',\r\n        12: \'%M\',\r\n        13: \'%d\',\r\n        14: \'%H\',\r\n        15: \'%M\',\r\n        16: \'%S\',\r\n        17: \'%Y-%m-%dT%H:%M:%S\'\r\n    }\r\n\r\n    data_format = format_json.get(time_type)\r\n    if add_time_unit == \'hours\':\r\n        return (datetime.datetime.now() + datetime.timedelta(hours=day)).strftime(data_format)\r\n    if add_time_unit == \'minutes\':\r\n        return (datetime.datetime.now() + datetime.timedelta(minutes=day)).strftime(data_format)\r\n    if add_time_unit == \'seconds\':\r\n        return (datetime.datetime.now() + datetime.timedelta(seconds=day)).strftime(data_format)\r\n    if add_time_unit == \'weeks\':\r\n        return (datetime.datetime.now() + datetime.timedelta(weeks=day)).strftime(data_format)\r\n\r\n    return (datetime.datetime.now() + datetime.timedelta(days=day)).strftime(data_format)\r\n\r\n\r\ndef get_today_start():\r\n    \"\"\"获取今天开始时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.floor(\"day\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_today_start_timestamp():\r\n    \"\"\"获取今天开始时间搓\"\"\"\r\n    return int(time.mktime(time.strptime(str(get_today_start()), \'%Y-%m-%d %H:%M:%S\')) * 1000)\r\n\r\n\r\ndef get_today_end():\r\n    \"\"\"获取今天结束时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.ceil(\"day\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_today_end_timestamp():\r\n    \"\"\"获取今天开始时间搓\"\"\"\r\n    return int(time.mktime(time.strptime(str(get_today_end()), \'%Y-%m-%d %H:%M:%S\')) * 1000)\r\n\r\n\r\ndef get_week_start():\r\n    \"\"\"获取当前周开始时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.floor(\"week\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_week_end():\r\n    \"\"\"获取当前周结束时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.ceil(\"week\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_month_start():\r\n    \"\"\"获取当前月开始时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.floor(\"month\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_month_end():\r\n    \"\"\"获取当前月结束时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.ceil(\"month\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_quarter_start():\r\n    \"\"\"获取当前季度开始时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.floor(\"quarter\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_quarter_end():\r\n    \"\"\"获取当前季度结束时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.ceil(\"quarter\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_year_start():\r\n    \"\"\"获取当前年开始时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.floor(\"year\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\ndef get_year_end():\r\n    \"\"\"获取当前年开始时间\"\"\"\r\n    now = arrow.utcnow().to(\"local\")\r\n    return now.ceil(\"year\").format(\'YYYY-MM-DD HH:mm:ss\')\r\n\r\n\r\n# -----------------------------------  redis操作  ----------------------------------------------\r\n\r\ndef redis_get(key):\r\n    \"\"\"\r\n    获取key值\r\n    :param key: key\r\n    :return:\r\n    \"\"\"\r\n    return br.get(key)\r\n\r\n\r\ndef redis_set(key, value, expire=0):\r\n    \"\"\"\r\n    插入redis值\r\n    :param key: key\r\n    :param value: value\r\n    :param expire: 时效\r\n    :return:\r\n    \"\"\"\r\n    return br.set(key, value, expire)\r\n\r\n\r\ndef redis_delete(*keys):\r\n    \"\"\"\r\n    删除key\r\n    :param keys: key 列表\r\n    :return:\r\n    \"\"\"\r\n    return br.delete(*keys)\r\n\r\n    \r\n\r\n\r\n# -----------------------------------  db操作  ----------------------------------------------\r\n\r\ndef db_execute(host, port, user, password, database, sql):\r\n    \"\"\"\r\n    执行sql语句\r\n    :param host: 数据库地址\r\n    :param port: 端口号\r\n    :param user: 用户名\r\n    :param password: 密码\r\n    :param database: 数据库\r\n    :param sql: sql语句\r\n    :param decrypt: 密码是否加密\r\n    :return:\r\n    \"\"\"\r\n    db = DB(host, port, user, password, database)\r\n    return db.execute(sql)\r\n', '2022-12-29 19:28:09', 7, '2023-10-11 13:53:52', 7, 1, '公共函数', '', '412d63658a634f449896d0b6d9832c5e', NULL, NULL);

-- ----------------------------
-- Table structure for lookup
-- ----------------------------
DROP TABLE IF EXISTS `lookup`;
CREATE TABLE `lookup`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '数据字典编码',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '描述',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int(11) NOT NULL DEFAULT 1,
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of lookup
-- ----------------------------
INSERT INTO `lookup` VALUES (3, 'api_report_run_type', '测试报告执行类型', '2022-05-04 12:48:38', '2023-10-23 14:08:26', 1, 7, 1, '02fea3346229426086d427ac3173a853');
INSERT INTO `lookup` VALUES (4, 'api_report_run_mode', '测试报告运行模式', '2022-05-04 14:29:45', '2022-05-04 14:29:44', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (5, 'api_timed_task_status', '定时任务运行状态', '2022-05-04 16:36:13', '2022-09-15 16:44:26', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (7, 'api_step_type', '用例类型', '2022-12-16 15:55:42', '2022-12-16 15:55:42', 1, 7, 7, NULL);

-- ----------------------------
-- Table structure for lookup_value
-- ----------------------------
DROP TABLE IF EXISTS `lookup_value`;
CREATE TABLE `lookup_value`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `lookup_id` bigint(20) NOT NULL COMMENT '所属类型',
  `lookup_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '编码',
  `lookup_value` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '值',
  `ext` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '拓展1',
  `display_sequence` int(11) NULL DEFAULT NULL COMMENT '显示顺序',
  `enabled_flag` int(11) NOT NULL DEFAULT 1 COMMENT '是否有效',
  `created_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '创建人',
  `creation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '最后更新人',
  `updation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_lookup_code`(`lookup_code`) USING BTREE,
  INDEX `idx_lookup_enable`(`enabled_flag`) USING BTREE,
  INDEX `idx_lookup_id`(`lookup_id`, `enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of lookup_value
-- ----------------------------
INSERT INTO `lookup_value` VALUES (6, 3, '10', '同步', '', 1, 1, '7', '2022-05-04 12:48:53', '7', '2023-07-06 10:54:26', 'd3d2611f5e384b97b6904595caeff75c');
INSERT INTO `lookup_value` VALUES (8, 4, '1', '同步', '', 1, 1, '7', '2022-05-04 14:39:14', '7', '2022-05-04 14:39:14', NULL);
INSERT INTO `lookup_value` VALUES (9, 4, '2', '异步', '', 2, 1, '7', '2022-05-04 14:39:26', '7', '2022-05-04 14:39:25', NULL);
INSERT INTO `lookup_value` VALUES (10, 4, '3', '定时任务', '', 3, 1, '7', '2022-05-04 14:39:26', '7', '2022-05-04 14:39:26', NULL);
INSERT INTO `lookup_value` VALUES (11, 3, '20', '异步', '', 3, 1, '7', '2022-05-04 15:32:17', '7', '2023-05-19 16:36:44', '97ad0c098dce4a8ba6a6bc0c445ab05e');
INSERT INTO `lookup_value` VALUES (12, 5, '1', '运行中', '', 2, 1, '7', '2022-05-04 16:36:34', '7', '2022-05-04 16:36:33', NULL);
INSERT INTO `lookup_value` VALUES (14, 7, 'case', '普通步骤', '', 12, 1, '7', '2022-12-16 15:56:00', '7', '2023-02-01 14:40:48', NULL);
INSERT INTO `lookup_value` VALUES (15, 7, 'if', 'IF', '', 2, 1, '7', '2022-12-16 15:56:12', '7', '2022-12-16 15:56:12', NULL);
INSERT INTO `lookup_value` VALUES (16, 7, 'loop', 'loop', '', 3, 1, '7', '2022-12-16 15:56:27', '7', '2022-12-16 15:56:26', NULL);
INSERT INTO `lookup_value` VALUES (17, 5, '0', '停止', '', 1, 1, '7', '2023-02-01 10:59:29', '7', '2023-02-01 10:59:29', NULL);
INSERT INTO `lookup_value` VALUES (34, 3, '30', '定时任务', '', 4, 1, '1', '2023-10-23 12:43:49', '1', '2023-10-23 12:43:49', '5cfc1fcea66b4aa799265f2eb6c3c00c');

-- ----------------------------
-- Table structure for menu
-- ----------------------------
DROP TABLE IF EXISTS `menu`;
CREATE TABLE `menu`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NULL DEFAULT NULL COMMENT '父级id',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单路径',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单名称',
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '组件路径',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'title',
  `isLink` tinyint(4) NULL DEFAULT 0 COMMENT '开启外链条件，`1、isLink: true 2、链接地址不为空（meta.isLink） 3、isIframe: false`',
  `linkUrl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `isHide` tinyint(4) NULL DEFAULT NULL COMMENT '菜单是否隐藏（菜单不显示在界面，但可以进行跳转）',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '图标',
  `isKeepAlive` tinyint(4) NULL DEFAULT NULL COMMENT '菜单是否缓存',
  `isAffix` tinyint(4) NULL DEFAULT NULL COMMENT '固定标签',
  `isIframe` tinyint(4) NULL DEFAULT NULL COMMENT '是否内嵌',
  `roles` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '权限',
  `sort` int(11) NULL DEFAULT NULL,
  `active_menu` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '显示页签',
  `menu_type` int(11) NULL DEFAULT 10 COMMENT '菜单类型',
  `redirect` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '重定向',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `views` int(11) NULL DEFAULT 0 COMMENT '访问数',
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `lookup_id` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`, `path`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 78 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, 0, '/home', 'home', 'home/index.vue', '首页', 0, NULL, 0, 'ele-HomeFilled', 1, 1, 0, 'admin', 0, NULL, 10, NULL, NULL, '2023-10-12 20:08:26', 1, 0, 7, 7, NULL, '2680357518b54db485ef12c6731ec788');
INSERT INTO `menu` VALUES (28, 0, '/system', 'system', 'layout/routerView/parent', '系统设置', 0, NULL, 0, 'ele-Tools', 0, 0, 0, NULL, 10, NULL, 10, '/system/menu', NULL, '2023-05-26 14:46:00', 1, 0, 7, 7, NULL, 'b4803273f622479bbcd8b34a432554fc');
INSERT INTO `menu` VALUES (29, 28, '/system/menu', 'systemMenu', 'system/menu/index', '菜单管理', 0, NULL, 0, 'ele-Menu', 1, 0, 0, NULL, 1, NULL, 10, NULL, NULL, '2022-03-14 10:23:12', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (30, 28, '/system/user', 'systemUser', 'system/user/index', '用户管理', 0, NULL, 0, 'ele-User', 1, 0, 0, NULL, 2, NULL, 10, NULL, NULL, '2022-03-10 20:48:01', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (31, 28, '/system/role', 'systemRole', 'system/role/index', '角色管理', 0, NULL, 0, 'ele-UserFilled', 1, 0, 0, '', 1, NULL, 10, '', '2022-03-11 16:43:26', '2022-03-11 16:43:26', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (32, 0, '/api', 'api', 'layout/routerView/parent', 'API测试', 0, NULL, 0, 'ele-Apple', 1, 0, 0, '', 2, NULL, 10, '/api/apiInfo', '2022-03-14 17:02:22', '2023-10-12 20:45:58', 1, 0, 7, 1, NULL, '46d23d11aa834610a6a816fb65170389');
INSERT INTO `menu` VALUES (33, 63, '/projectOrModule/project', 'apiProject', 'api/project/index.vue', '项目列表', 0, NULL, 0, 'ele-Files', 1, 0, 0, '', 1, NULL, 10, '', '2022-03-14 17:16:38', '2023-10-12 20:45:10', 1, 0, 7, 1, NULL, '3bc0f62b090048d48c0606ea158a0f2c');
INSERT INTO `menu` VALUES (34, 63, '/projectOrModule/module', 'apiModule', 'api/module/index.vue', '模块列表', 0, NULL, 0, 'ele-FolderRemove', 1, 0, 0, '', 2, NULL, 10, '', '2022-03-19 18:36:51', '2023-10-12 20:45:13', 1, 0, 7, 1, NULL, '9fe7e632840149318abe10e90ec8283f');
INSERT INTO `menu` VALUES (35, 32, '/api/env', 'ApiEnv', 'api/environment/index.vue', '环境管理', 0, NULL, 0, 'ele-Monitor', 1, 0, 0, '', 8, NULL, 10, '', '2022-03-19 22:13:59', '2022-03-19 22:13:59', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (36, 69, '/job/timedTask', 'apiTimedTask', 'api/timedTask/index.vue', '定时任务', 0, NULL, 0, 'ele-Clock', 1, 0, 0, '', 7, NULL, 10, '', '2022-03-20 13:58:39', '2023-10-12 20:20:07', 1, 0, 7, 1, NULL, '6e28bbb30849486c8807fd564f98f1f0');
INSERT INTO `menu` VALUES (37, 32, '/api/apiInfo', 'apiInfo', 'api/apiInfo/index.vue', '接口管理', 0, NULL, 0, 'ele-DocumentRemove', 1, 0, 0, '', 3, NULL, 10, '', '2022-03-30 14:23:46', '2022-03-30 14:23:46', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (38, 37, '/api/apiInfo/edit', 'EditApiInfo', 'api/apiInfo/components/EditApi', '接口编辑', 0, NULL, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-03-30 15:53:20', '2023-10-09 17:57:10', 1, 0, 7, 7, NULL, '8e96b50b2f0c461cb4c7602d94fd6b78');
INSERT INTO `menu` VALUES (40, 32, '/api/functions', 'ApiFunctions', '/api/functions/index.vue', '自定义函数', 0, NULL, 0, 'ele-MagicStick', 1, 0, 0, '', 6, NULL, 10, '', '2022-04-02 17:09:56', '2022-04-02 17:09:56', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (41, 40, '/api/functions/edit', 'EditFunc', '/api/functions/EditFunc', '编辑自定义函数', 0, NULL, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-04-02 17:27:20', '2022-04-02 17:27:20', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (42, 47, '/api/ApiReport/ApiReportDetail', 'ApiReportDetail', 'api/Report/ApiReportDetail.vue', '报告详情', 0, NULL, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-04-07 17:20:19', '2023-10-08 14:17:29', 1, 0, 7, 7, NULL, '5f7659989f2645949badd41a7329b157');
INSERT INTO `menu` VALUES (47, 32, '/api/ApiReport', 'apiReport', 'api/Report/index.vue', '测试报告', 0, NULL, 0, 'ele-Document', 1, 0, 0, '', 5, NULL, 10, '', '2022-04-09 21:49:17', '2023-10-08 12:00:20', 1, 0, 7, 1, NULL, '9450764c5cf540f9ad9e35b4d47cdb1d');
INSERT INTO `menu` VALUES (48, 32, '/api/config', 'config', 'api/configure/index.vue', '配置管理', 0, NULL, 1, 'ele-SetUp', 1, 0, 0, '', 4, NULL, 10, '', '2022-04-10 18:25:10', '2023-03-02 16:38:59', 1, 0, 7, 7, NULL, '18c372786f3d48b7966d888517098635');
INSERT INTO `menu` VALUES (49, 32, '/api/apiCase', 'apiCase', 'api/apiCase/index.vue', '测试用例', 0, NULL, 0, 'ele-Fold', 1, 0, 0, '', 4, NULL, 10, '', '2022-04-12 10:50:09', '2022-04-12 10:50:09', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (50, 49, '/api/apiCase/edit', 'EditApiCase', 'api/apiCase/EditApiCase', '编辑用例', 0, NULL, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-04-12 11:42:09', '2023-07-28 17:54:09', 1, 0, 7, 7, NULL, '271ab5852e804b7b8e80e2e6d4295edf');
INSERT INTO `menu` VALUES (51, 28, '/system/lookup', 'systemLookup', 'system/lookup/index.vue', '数据字典', 0, NULL, 0, 'ele-Management', 1, 0, 0, '', 3, NULL, 10, '', '2022-05-03 17:11:59', '2022-05-03 17:11:59', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (53, 0, '/tools', 'tools', 'layout/routerView/parent', '便捷工具', 0, NULL, 0, 'ele-ForkSpoon', 1, 0, 0, '', 5, NULL, 10, '', '2022-06-14 21:08:01', '2023-05-17 16:55:23', 1, 0, 7, 7, NULL, 'b2160537cf404a4c8158c760a9782183');
INSERT INTO `menu` VALUES (54, 53, '/tools/QueryDB', 'QueryDB', 'tools/queryDB/index.vue', '数据查询', 0, NULL, 0, 'ele-MagicStick', 1, 0, 0, '', 0, NULL, 10, '', '2022-06-14 21:09:29', '2023-10-13 15:09:28', 1, 0, 7, 7, NULL, '9516ca9f7bc4483481f839771c3892e0');
INSERT INTO `menu` VALUES (57, 0, '/ui', 'ui', 'layout/routerView/parent', 'UI测试', 0, NULL, 0, 'ele-Cherry', 1, 0, 0, 'admin', 3, NULL, 10, '', '2022-08-23 11:05:09', '2023-10-12 19:44:23', 1, 0, 7, 7, NULL, '6b3d418ffeb040478f9be028cdcc3ee5');
INSERT INTO `menu` VALUES (58, 32, '/api/dataSource', 'ApiDataSource', 'api/dataSource/index.vue', '数据源管理', 0, NULL, 0, 'ele-Tickets', 1, 0, 0, '', 9, NULL, 10, '', '2022-09-13 14:34:44', '2022-09-13 14:34:43', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (59, 53, '/tools/testcase', 'apiTest', 'api/apiTest/index.vue', '接口测试', 0, NULL, 1, '', 0, 0, 0, '', 0, NULL, 10, '', '2022-09-13 16:00:00', '2023-07-31 10:31:56', 1, 0, 7, 7, NULL, '730571c1b89d46d492c1f07b83a0b726');
INSERT INTO `menu` VALUES (61, 28, '/system/personal', 'personal', 'system/personal/index', '个人中心', 0, NULL, 0, 'ele-User', 1, 0, 0, '', 1, NULL, 10, '', '2023-01-16 16:37:40', '2023-10-08 14:30:39', 1, 3, 7, 7, NULL, 'fab84ae3470d41a884c68b509a633d72');
INSERT INTO `menu` VALUES (62, 53, '/websocket', '连接1', 'tools/websocket/index.vue', '连接1', 0, NULL, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-02-09 12:27:42', '2023-07-31 10:31:39', 1, 0, 7, 7, NULL, 'e514be038d7c4f779854292fc9a4bc31');
INSERT INTO `menu` VALUES (63, 0, '/projectOrModule', '/projectOrModule', 'layout/routerView/parent', '项目/模块', 0, '', 0, 'ele-Files', 1, 0, 0, '0', 1, NULL, 10, '', '2023-02-23 11:07:56', '2023-10-12 20:08:33', 1, 0, NULL, 7, NULL, 'd08da515ca754613a1ef591310dd3be3');
INSERT INTO `menu` VALUES (64, 57, '/ui/page', 'uiPage', 'ui/page/index.vue', '页面管理', 0, NULL, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-05-26 11:12:13', '2023-05-26 11:12:57', 1, 0, 7, 7, NULL, 'ae8cbb970fe94b57a74243e5a2448b5b');
INSERT INTO `menu` VALUES (65, 64, '/ui/page/edite', 'EditPage', 'ui/page/EditPage.vue', '页面编辑', 0, NULL, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-05-26 14:47:33', '2023-05-26 15:21:36', 1, 0, 7, 7, NULL, 'dcbd130fd512496ba3b95292bfaf370c');
INSERT INTO `menu` VALUES (66, 57, '/ui/uiCase', 'uiCase', 'ui/uiCase/index.vue', '测试用例', 0, NULL, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-05-27 23:29:46', '2023-06-14 16:18:50', 1, 0, 7, 7, NULL, '0041e560003f4337b5d9326a499e0447');
INSERT INTO `menu` VALUES (67, 66, '/ui/uiCase/edit', 'editUiCase', 'ui/uiCase/editUiCase.vue', '用例编辑', 0, NULL, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-06-02 10:02:18', '2023-06-14 16:18:57', 1, 0, 7, 7, NULL, 'a745d4ae3e7940ddbb8515ea06a26fb5');
INSERT INTO `menu` VALUES (68, 57, '/ui/uiReport', 'uiReport', 'ui/uiReport/index.vue', '测试报告', 0, NULL, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-06-13 16:48:52', '2023-06-14 16:19:01', 1, 0, 7, 7, NULL, '325eeece337b450c8e04bc83d0a802d3');
INSERT INTO `menu` VALUES (69, 0, '/job', 'job', 'layout/routerView/parent', '定时任务', 0, NULL, 0, 'ele-AlarmClock', 1, 0, 0, '0', 4, NULL, 10, '', '2023-06-15 19:53:23', '2023-06-15 20:36:07', 1, 0, 7, 7, NULL, '0fe72ee35bdc41ca9adc60e01576383f');
INSERT INTO `menu` VALUES (70, 69, '/job/taskRecord', 'taskRecord', 'job/taskRecord/index.vue', '执行记录', 0, NULL, 0, 'ele-Document', 1, 0, 0, '0', 2, NULL, 10, '', '2023-06-15 19:54:28', '2023-06-15 20:19:14', 1, 0, 7, 7, NULL, '9f7d85770e004da6a97d4e0ec29a21c3');
INSERT INTO `menu` VALUES (73, 0, '/precisionTest', 'precisionTest', 'layout/routerView/parent', '精准测试', 0, NULL, 0, 'ele-Grape', 1, 0, 0, '0', 6, NULL, 10, '', '2023-08-17 20:17:19', '2023-09-07 15:38:45', 1, 0, 7, 7, NULL, 'd7a0498eb7f24f09a7997342085bd58b');
INSERT INTO `menu` VALUES (74, 75, '/precisionTest/CoverageDetail', 'CoverageDetail', 'precisionTest/CoverageDetail/index.vue', '覆盖率详情', 0, NULL, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-08-17 20:19:57', '2023-09-13 17:36:14', 1, 0, 7, 1, NULL, 'a009e130592f4a92b419bb49e3004bc2');
INSERT INTO `menu` VALUES (75, 73, '/precisionTest/CoverageList', 'CoverageList', 'precisionTest/CoverageList/index.vue', '覆盖率报告', 0, NULL, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-08-31 11:12:08', '2023-09-13 17:35:48', 1, 0, 7, 1, NULL, 'fb4f611267b045a09c3081f76cffd6c6');
INSERT INTO `menu` VALUES (76, 73, '/precisionTest/RepositoryManager', 'RepositoryManager', 'precisionTest/RepositoryManager/index.vue', '仓库管理', 0, NULL, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-09-04 11:24:55', '2023-09-04 11:25:26', 1, 0, 7, 7, NULL, 'dc4a6250d18647fe8ebf503ec79678a4');
INSERT INTO `menu` VALUES (77, 53, '/tools/JsonParse', 'JsonParse', 'tools/JsonParse/index.vue', 'Json解析', 0, NULL, 0, 'ele-ColdDrink', 1, 0, 0, '0', 0, NULL, 10, '', '2023-09-23 09:48:10', '2023-09-25 17:31:17', 1, 0, 1, 7, NULL, 'a7a991b583274a09aaa7ce03b5b2235b');

-- ----------------------------
-- Table structure for menu_view_history
-- ----------------------------
DROP TABLE IF EXISTS `menu_view_history`;
CREATE TABLE `menu_view_history`  (
  `menu_id` int(11) NULL DEFAULT NULL COMMENT '菜单id',
  `remote_addr` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '访问ip',
  `user_id` int(11) NULL DEFAULT NULL COMMENT '访问人',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_menu_view_history_remote_addr`(`remote_addr`) USING BTREE,
  INDEX `ix_menu_view_history_user_id`(`user_id`) USING BTREE,
  INDEX `ix_menu_view_history_menu_id`(`menu_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu_view_history
-- ----------------------------

-- ----------------------------
-- Table structure for module_info
-- ----------------------------
DROP TABLE IF EXISTS `module_info`;
CREATE TABLE `module_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '模块名称',
  `project_id` int(11) NULL DEFAULT NULL COMMENT '归属项目id',
  `config_id` int(11) NULL DEFAULT NULL COMMENT '关联配置id',
  `test_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '测试负责人id',
  `simple_desc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '简要描述',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '其他信息',
  `leader_user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '负责人',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人',
  `updated_by` int(11) NULL DEFAULT NULL,
  `module_packages` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `priority` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_module_info_module_name`(`name`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of module_info
-- ----------------------------
INSERT INTO `module_info` VALUES (7, '2022-03-19 22:25:49', '2022-07-14 09:31:47', 0, '博客内容', 577, NULL, '小白', NULL, NULL, '小白', 7, 7, NULL, '4', NULL);
INSERT INTO `module_info` VALUES (34, '2023-10-23 16:59:36', '2023-10-24 10:07:33', 1, '测试模块', 581, NULL, '', '', NULL, NULL, 1, 7, NULL, NULL, 'cb137ddcbf9d4b04b4995bce5a1f3e8d');

-- ----------------------------
-- Table structure for notify
-- ----------------------------
DROP TABLE IF EXISTS `notify`;
CREATE TABLE `notify`  (
  `user_id` int(11) NULL DEFAULT NULL COMMENT '用户id',
  `group` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '组',
  `message` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '消息',
  `send_status` int(11) NULL DEFAULT NULL COMMENT '发送状态，10成功 20 失败',
  `read_status` int(11) NULL DEFAULT NULL COMMENT '消息状态，10未读 20 已读',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_notify_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of notify
-- ----------------------------

-- ----------------------------
-- Table structure for project_info
-- ----------------------------
DROP TABLE IF EXISTS `project_info`;
CREATE TABLE `project_info`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '项目名称',
  `responsible_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '负责人',
  `test_user` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '测试人员',
  `dev_user` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '开发人员',
  `publish_app` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '发布应用',
  `simple_desc` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '简要描述',
  `remarks` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '其他信息',
  `config_id` int(11) NULL DEFAULT NULL COMMENT '关联配置id',
  `product_id` int(11) NULL DEFAULT NULL COMMENT '产品线',
  `enabled_flag` int(11) NULL DEFAULT NULL COMMENT '是否删除',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_project_info_name`(`name`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1699677678757617616 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of project_info
-- ----------------------------
INSERT INTO `project_info` VALUES (577, '个人博客', '小白', '小白', '小白', '', '', NULL, NULL, NULL, 1, '2022-03-19 17:48:12', 7, '2022-03-19 17:48:12', 7, NULL);
INSERT INTO `project_info` VALUES (581, '跨境好运', '段小段', '段小段', '段小段', '', '', '', NULL, NULL, 1, '2023-10-24 10:07:25', 7, '2022-04-29 09:45:19', 7, '09e529e385154429874aea0c88f70bbb');

-- ----------------------------
-- Table structure for repository_manager
-- ----------------------------
DROP TABLE IF EXISTS `repository_manager`;
CREATE TABLE `repository_manager`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '组件',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '仓库名称',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '仓库地址',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '账户',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` bigint(20) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` bigint(20) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of repository_manager
-- ----------------------------
INSERT INTO `repository_manager` VALUES (1, 'gitee', 'gitee.com', NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL);

-- ----------------------------
-- Table structure for request_history
-- ----------------------------
DROP TABLE IF EXISTS `request_history`;
CREATE TABLE `request_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `remote_addr` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名称',
  `real_ip` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名称',
  `request` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户名称',
  `method` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `args` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `form` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `json` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '操作',
  `response` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '操作',
  `endpoint` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '操作',
  `elapsed` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '操作',
  `request_time` datetime NULL DEFAULT NULL COMMENT '操作',
  `env` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `employee_code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `toekn` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of request_history
-- ----------------------------

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '名称',
  `role_type` int(11) NULL DEFAULT 10 COMMENT '权限类型',
  `menus` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '菜单ids',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `updated_by` int(11) NOT NULL COMMENT '更新人',
  `created_by` int(11) NOT NULL COMMENT '创建人',
  `status` int(11) NULL DEFAULT 10 COMMENT '角色状态 10 启用，20 禁用',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES (1, '管理员', '管理员', 10, '1,33,34,38,48,50,42,41,72,58,65,67,68,70,36,54,59,62,77,74,76,61,29,31,30,51', '2021-04-12 16:56:20', '2023-09-23 09:49:17', 1, 1, 7, 10, '51e01f09d66743efa9f9cf1ab546d7dc');
INSERT INTO `roles` VALUES (3, '测试工程师', '测试工程师', 10, '1,78,33,34,38,48,50,42,41,72,58,65,67,68,70,36,54,59,62', '2021-05-21 17:24:53', '2023-09-27 17:46:14', 1, 16, 7, 10, 'a431078051684e74bc1440044a13a07c');

-- ----------------------------
-- Table structure for ui_case
-- ----------------------------
DROP TABLE IF EXISTS `ui_case`;
CREATE TABLE `ui_case`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用例名',
  `tags` json NULL COMMENT '自动化标记',
  `steps` json NULL COMMENT '运行步骤',
  `setup_hooks` json NULL COMMENT '前置操作',
  `teardown_hooks` json NULL COMMENT '后置操作',
  `variables` json NULL COMMENT '变量',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `project_id` int(11) NULL DEFAULT NULL,
  `module_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_case_name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ui_case
-- ----------------------------
INSERT INTO `ui_case` VALUES ('百度搜索', 'null', '[{\"id\": null, \"data\": \"http://baidu.com\", \"name\": \"测试11111\", \"index\": 1, \"action\": \"open\", \"cookie\": null, \"enable\": true, \"output\": null, \"script\": \"测试111111\", \"page_id\": \"\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"su\", \"location_method\": \"name\", \"page_element_id\": null}, {\"id\": null, \"data\": \"哇哈哈\", \"name\": \"测试步骤\", \"index\": 2, \"action\": \"input\", \"cookie\": null, \"enable\": true, \"output\": null, \"script\": \"print(\\\"test1111111111111\\\")\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"8\", \"action_value\": [\"常规操作\", \"input\"], \"location_value\": \"kw\", \"location_method\": \"id\", \"page_element_id\": [1, 8]}]', 'null', 'null', 'null', '测试百度', 1, '2023-05-27 23:23:51', 7, '2023-07-24 19:14:42', 7, 0, 'a8286c3fd17e44f9a9332fd9158b24ae', '1.0.0', 577, 17);
INSERT INTO `ui_case` VALUES ('baidu1', '[\"测试\"]', '[{\"id\": null, \"data\": \"http://baidu.com\", \"name\": \"ces 1\", \"index\": 1, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"su\", \"location_method\": \"name\", \"page_element_id\": null}]', 'null', 'null', 'null', '111', 2, '2023-06-15 14:37:01', 7, '2023-07-24 19:14:44', 7, 0, '610463528b1d410791240929c06734d5', NULL, 577, 17);
INSERT INTO `ui_case` VALUES ('login', '[]', '[{\"id\": null, \"data\": \"\", \"name\": \"打开浏览器\", \"index\": 1, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"123\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"3\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"su\", \"location_method\": \"name\", \"page_element_id\": [1, 3]}]', 'null', 'null', 'null', '', 3, '2023-07-04 16:36:25', 7, '2023-07-24 19:14:45', 7, 0, '708c3f755c5e4999a68d1063858abc2c', NULL, 577, 17);
INSERT INTO `ui_case` VALUES ('ces', '[]', '[{\"id\": null, \"data\": \"\", \"name\": \"\", \"index\": 1, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"3\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"su\", \"location_method\": \"name\", \"page_element_id\": [1, 3]}]', 'null', 'null', 'null', '', 4, '2023-07-06 14:19:40', 7, '2023-07-24 19:14:40', 7, 0, '531c9c24e21440ae890aac232bd18021', NULL, 577, 17);
INSERT INTO `ui_case` VALUES ('1', '[]', '[{\"id\": null, \"data\": \"123\", \"name\": \"222222222222\", \"index\": 1, \"action\": \"input\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"1\", \"action_value\": [\"常规操作\", \"input\"], \"location_value\": \"username2\", \"location_method\": \"name\", \"page_element_id\": [1, 1]}, {\"id\": null, \"data\": \"11\", \"name\": \"1222222222\", \"index\": 2, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"dddddddddddd\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"3\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"su\", \"location_method\": \"name\", \"page_element_id\": [1, 3]}]', 'null', 'null', 'null', '1', 5, '2023-07-07 19:49:46', 7, '2023-08-23 10:02:07', 7, 1, '44fd2981a61f461f96ccf05a1748bf56', NULL, 577, 17);
INSERT INTO `ui_case` VALUES ('发送文字消息给小佘', '[]', '[{\"id\": null, \"data\": \"\", \"name\": \"安达市多\", \"index\": 1, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"18\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"15\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"asdasd\", \"location_method\": \"id\", \"page_element_id\": [18, 15]}, {\"id\": null, \"data\": \"\", \"name\": \"打开微信\", \"index\": 2, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"17\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"14\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"22\", \"location_method\": \"xpath\", \"page_element_id\": [17, 14]}]', 'null', 'null', 'null', '', 6, '2023-08-15 18:03:02', 7, '2023-10-08 09:17:19', 1, 1, 'f86384edc92c4007b129c046c8e9e8e7', NULL, 582, 18);
INSERT INTO `ui_case` VALUES ('12333', '[]', '[{\"id\": null, \"data\": \"python\", \"name\": \"\", \"index\": 1, \"action\": \"input\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"19\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"18\", \"action_value\": [\"常规操作\", \"input\"], \"location_value\": \"kw\", \"location_method\": \"id\", \"page_element_id\": [19, 18]}, {\"id\": null, \"data\": \"\", \"name\": \"\", \"index\": 2, \"action\": \"click\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"19\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"19\", \"action_value\": [\"常规操作\", \"click\"], \"location_value\": \"su\", \"location_method\": \"id\", \"page_element_id\": [19, 19]}]', 'null', 'null', 'null', '', 7, '2023-08-17 14:30:39', 7, '2023-08-17 14:30:39', 7, 1, 'd60e858250a4466a96b372385cfa7e77', NULL, 582, 18);
INSERT INTO `ui_case` VALUES ('12333fff', '[]', '[{\"id\": null, \"data\": \"python\", \"name\": \"\", \"index\": 1, \"action\": \"input\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"19\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"18\", \"action_value\": [\"常规操作\", \"input\"], \"location_value\": \"kw\", \"location_method\": \"id\", \"page_element_id\": [19, 18]}, {\"id\": null, \"data\": \"\", \"name\": \"\", \"index\": 2, \"action\": \"click\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"19\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"19\", \"action_value\": [\"常规操作\", \"click\"], \"location_value\": \"su\", \"location_method\": \"id\", \"page_element_id\": [19, 19]}]', 'null', 'null', 'null', '', 8, '2023-08-17 14:30:46', 7, '2023-08-17 14:30:46', 7, 1, '44ff128cc1b14a22a1c700538e7ab96d', NULL, 582, 18);
INSERT INTO `ui_case` VALUES ('12333fff', '[]', '[{\"id\": null, \"data\": \"python\", \"name\": \"\", \"index\": 1, \"action\": \"input\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"19\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"18\", \"action_value\": [\"常规操作\", \"input\"], \"location_value\": \"kw\", \"location_method\": \"id\", \"page_element_id\": [19, 18]}, {\"id\": null, \"data\": \"\", \"name\": \"\", \"index\": 2, \"action\": \"click\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"19\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"19\", \"action_value\": [\"常规操作\", \"click\"], \"location_value\": \"su\", \"location_method\": \"id\", \"page_element_id\": [19, 19]}]', 'null', 'null', 'null', '', 9, '2023-08-17 14:30:48', 7, '2023-08-22 14:32:07', 7, 0, '9e9e102da77847d7a8c7df8afedea797', NULL, 582, 18);
INSERT INTO `ui_case` VALUES ('啥事', '[]', '[{\"id\": null, \"data\": \"哈哈哈\", \"name\": \"asgasgaags\", \"index\": 1, \"action\": \"input\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"dddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddd\\r\\n\\r\\n\\r\\n\\r\\nddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddd\\r\\nddddddddddddddddddddddddddddddddddddd\\r\\nddddddddddddddddddddddddd\\r\\nddddddddddddddddddddddddddddddddd\\r\\n\", \"page_id\": \"20\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"21\", \"action_value\": [\"常规操作\", \"input\"], \"location_value\": \"kw\", \"location_method\": \"id\", \"page_element_id\": [20, 21]}, {\"id\": null, \"data\": \"\", \"name\": \"dddddddddddddddddddddd\", \"index\": 2, \"action\": \"click\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"dddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd\\r\\ndddddddddddddddddddddd\", \"page_id\": \"20\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"22\", \"action_value\": [\"常规操作\", \"click\"], \"location_value\": \"su\", \"location_method\": \"id\", \"page_element_id\": [20, 22]}]', 'null', 'null', 'null', '', 10, '2023-08-23 10:00:27', 7, '2023-09-01 15:52:42', 7, 1, '830f9b17e3bf476f8bc3567190cd4c85', NULL, 577, 17);
INSERT INTO `ui_case` VALUES ('百度', '[]', '[{\"id\": null, \"data\": \"https://www.baidu.com/\", \"name\": \"\", \"index\": 1, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"4\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"测试\", \"location_method\": \"tag_name\", \"page_element_id\": [1, 4]}, {\"id\": null, \"data\": \"\", \"name\": \"2\", \"index\": 2, \"action\": \"click\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"3\", \"action_value\": [\"常规操作\", \"click\"], \"location_value\": \"su\", \"location_method\": \"name\", \"page_element_id\": [1, 3]}, {\"id\": null, \"data\": \"23231233\", \"name\": \"1\", \"index\": 3, \"action\": \"input\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"8\", \"action_value\": [\"常规操作\", \"input\"], \"location_value\": \"kw\", \"location_method\": \"id\", \"page_element_id\": [1, 8]}]', 'null', 'null', 'null', '', 11, '2023-09-05 17:55:42', 7, '2023-10-17 23:45:17', 7, 1, 'cdbb7712b9d84a4bb2fd48a2c4a1b521', NULL, 582, 18);
INSERT INTO `ui_case` VALUES ('ces', '[]', '[{\"id\": null, \"data\": \"123\", \"name\": \"12\", \"index\": true, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"3\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"su\", \"location_method\": \"name\", \"page_element_id\": [1, 3]}]', 'null', 'null', 'null', '', 12, '2023-10-13 14:16:13', 7, '2023-10-13 14:16:13', 7, 1, 'dda3d676199a422d8e08724695f1553b', NULL, 577, 17);
INSERT INTO `ui_case` VALUES ('132', '[]', '[{\"id\": null, \"data\": \"123\", \"name\": \"b步骤1\", \"index\": 1, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"import flask\\r\\nfor i in range(5):\\r\\n    print(i)\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n    \", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"1\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"username2\", \"location_method\": \"name\", \"page_element_id\": [1, 1]}, {\"id\": null, \"data\": \"123213\", \"name\": \"步骤2\", \"index\": true, \"action\": \"open\", \"cookie\": \"\", \"enable\": true, \"output\": \"\", \"script\": \"import a\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\\r\\n\", \"page_id\": \"1\", \"remarks\": null, \"variables\": [], \"breakpoint\": false, \"element_id\": \"1\", \"action_value\": [\"常规操作\", \"open\"], \"location_value\": \"username2\", \"location_method\": \"name\", \"page_element_id\": [1, 1]}]', 'null', 'null', 'null', '', 13, '2023-10-24 09:29:38', 7, '2023-10-24 09:30:56', 7, 1, '816bf0457d734b79a6945465f2d34307', NULL, 581, 34);

-- ----------------------------
-- Table structure for ui_element
-- ----------------------------
DROP TABLE IF EXISTS `ui_element`;
CREATE TABLE `ui_element`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '元素名称',
  `location_method` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '定位类型',
  `location_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '定位元素值',
  `page_id` int(11) NOT NULL COMMENT '关联页面',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_element_name`(`name`) USING BTREE,
  INDEX `ix_ui_element_page_id`(`page_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ui_element
-- ----------------------------
INSERT INTO `ui_element` VALUES ('休息休息', 'id', 'asdasd', 18, '', 15, '2023-08-17 09:07:52', 7, '2023-08-17 09:07:52', 7, 1, '3f1ef54e4b4d4ad4852996a1123adb15');
INSERT INTO `ui_element` VALUES ('搜索输入框', 'id', 'kw', 0, '', 16, '2023-08-17 14:27:46', 7, '2023-08-17 14:27:46', 7, 1, '0020e2783b624a81b8df7be7630b0020');
INSERT INTO `ui_element` VALUES ('搜索按钮', 'id', 'su', 0, '', 17, '2023-08-17 14:28:06', 7, '2023-08-17 14:28:06', 7, 1, '3996ddc77f61437a8bbf01ec5b8451c4');
INSERT INTO `ui_element` VALUES ('输入框', 'id', 'kw', 19, '', 18, '2023-08-17 14:28:44', 7, '2023-09-05 17:44:00', 7, 1, '6dfb487315194f8caa6fd86c0179608d');
INSERT INTO `ui_element` VALUES ('按钮', 'id', 'su', 19, '', 19, '2023-08-17 14:28:53', 7, '2023-09-26 09:05:15', 7, 1, '010abce6b966472c993ca5edaeb94158');
INSERT INTO `ui_element` VALUES ('ss', 'id', 'kw', 0, '', 20, '2023-08-23 09:55:45', 7, '2023-08-23 09:55:45', 7, 1, '09361747ebba4adab3c502b6c6ec04df');
INSERT INTO `ui_element` VALUES ('输入框', 'id', 'kw', 20, '', 21, '2023-08-23 09:58:16', 7, '2023-09-07 17:39:16', 7, 0, '9f698a28373a428897be8be76421914e');
INSERT INTO `ui_element` VALUES ('点击', 'id', 'su', 20, '', 22, '2023-08-23 09:59:24', 7, '2023-09-15 23:48:12', 7, 1, '4940d00654c44002be7a2e93f829871e');
INSERT INTO `ui_element` VALUES ('输入框', 'id', 'kw', 21, '', 23, '2023-09-27 20:06:25', 7, '2023-10-17 23:43:50', 7, 1, 'f871e87f96fa4a9ea02f0e07c6c5e70e');

-- ----------------------------
-- Table structure for ui_page
-- ----------------------------
DROP TABLE IF EXISTS `ui_page`;
CREATE TABLE `ui_page`  (
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '页面名称',
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'url',
  `project_id` int(11) NULL DEFAULT NULL COMMENT '项目id',
  `module_id` int(11) NULL DEFAULT NULL COMMENT '模块id',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `tags` json NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_page_project_id`(`project_id`) USING BTREE,
  INDEX `ix_ui_page_name`(`name`) USING BTREE,
  INDEX `ix_ui_page_module_id`(`module_id`) USING BTREE,
  INDEX `ix_ui_page_url`(`url`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ui_page
-- ----------------------------
INSERT INTO `ui_page` VALUES ('百度页面', 'https://www.baidu.com', 577, 17, '百度', 1, '2023-05-26 14:35:41', 7, '2023-08-16 11:50:47', 7, 1, '37059d5b5e2f4d4db1bb9864c5ddc8d2', '[\"tags\", \"ces \"]');
INSERT INTO `ui_page` VALUES ('百度页面测试', 'https://www.baidu.com/', 591, 21, 'test', 17, '2023-07-12 17:26:32', 7, '2023-08-02 18:15:39', 7, 1, '0bbccf58291d44e6b3ad289c9e83f13e', 'null');
INSERT INTO `ui_page` VALUES ('4434', '4434', 582, 18, NULL, 18, '2023-08-02 17:54:25', 7, '2023-08-17 09:07:58', 7, 1, 'dcd95b7d6794477c82eee51e304944df', 'null');
INSERT INTO `ui_page` VALUES ('百度搜索', 'https://www.baidu.com', 582, 18, NULL, 19, '2023-08-17 14:28:24', 7, '2023-08-17 14:28:57', 7, 1, '0dadab479f1441db90db66754c51df01', 'null');
INSERT INTO `ui_page` VALUES ('baidu', 'www.baidu.com', 577, 17, NULL, 20, '2023-08-23 09:55:49', 7, '2023-08-23 09:59:30', 7, 1, '7b0d73f7d4914c19afe9907181fee9cb', 'null');
INSERT INTO `ui_page` VALUES ('测试百度', 'https://www.baidu.com/', 577, 17, '123', 21, '2023-09-16 00:00:34', 7, '2023-10-23 18:59:52', 7, 1, 'c4624961e93a4a77bd9fb354394f015f', '[\"a\"]');

-- ----------------------------
-- Table structure for ui_report_detail_0
-- ----------------------------
DROP TABLE IF EXISTS `ui_report_detail_0`;
CREATE TABLE `ui_report_detail_0`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `index` int(11) NULL DEFAULT NULL,
  `variables` json NULL,
  `data` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `action` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `location_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `location_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `report_id` int(11) NULL DEFAULT NULL,
  `success` int(11) NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `case_id` int(11) NULL DEFAULT NULL,
  `step_id` int(11) NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `duration` decimal(10, 3) NULL DEFAULT NULL,
  `setup_hook_results` json NULL,
  `teardown_hook_results` json NULL,
  `validator_results` json NULL,
  `screenshot_file_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `log` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ui_report_detail_0
-- ----------------------------

-- ----------------------------
-- Table structure for ui_reports
-- ----------------------------
DROP TABLE IF EXISTS `ui_reports`;
CREATE TABLE `ui_reports`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '报告名',
  `project_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '项目id',
  `module_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '模块id',
  `success` int(11) NULL DEFAULT NULL COMMENT '是否成功',
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '状态',
  `duration` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '执行耗时',
  `case_id` int(11) NULL DEFAULT NULL COMMENT '用例id',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `start_time` datetime NULL DEFAULT NULL,
  `run_count` int(11) NULL DEFAULT NULL,
  `run_success_count` int(11) NULL DEFAULT NULL,
  `run_fail_count` int(11) NULL DEFAULT NULL,
  `run_skip_count` int(11) NULL DEFAULT NULL,
  `run_err_count` int(11) NULL DEFAULT NULL,
  `run_log` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `env_id` int(11) NULL DEFAULT NULL,
  `exec_user_id` int(11) NULL DEFAULT NULL,
  `exec_user_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `run_mode` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_reports_project_id`(`project_id`) USING BTREE,
  INDEX `ix_ui_reports_module_id`(`module_id`) USING BTREE,
  INDEX `ix_ui_reports_case_id`(`case_id`) USING BTREE,
  INDEX `ix_ui_reports_success`(`success`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ui_reports
-- ----------------------------

-- ----------------------------
-- Table structure for ui_steps
-- ----------------------------
DROP TABLE IF EXISTS `ui_steps`;
CREATE TABLE `ui_steps`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `index` int(11) NOT NULL COMMENT '步骤排序',
  `operation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `input_data` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '输入数据',
  `location_method` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '定位元素方式',
  `location_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '定位元素值',
  `output` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '输出',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `case_id` int(11) NULL DEFAULT NULL COMMENT '关联ui测试用例',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int(11) NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_steps_index`(`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ui_steps
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `enabled_flag` tinyint(1) NULL DEFAULT 1 COMMENT '是否删除',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `roles` json NULL COMMENT '用户角色',
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户昵称',
  `status` int(11) NULL DEFAULT 1 COMMENT '用户状态 0 正常 1锁定',
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `user_type` int(11) NULL DEFAULT 10 COMMENT '用户类型， 10 管理人员, 20 测试人员',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户描述',
  `avatar` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '头像数据',
  `tags` json NULL COMMENT '用户标签',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_user_email`(`email`) USING BTREE,
  INDEX `ix_user_password`(`password`) USING BTREE,
  INDEX `ix_user_username`(`username`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('2020-11-20 10:04:08', '2023-10-19 21:36:57', 1, 1, 'xiaobai', '123456', NULL, '[1]', '小白', 1, 7, 1, NULL, '测试111111111111111111111111111111111测测试', 'data:image/jpeg;base64,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', '[\"xiaobai\"]', '5536c745867c459f81eb62c3e95ab1b4');
INSERT INTO `user` VALUES ('2022-03-09 16:03:43', '2023-10-24 09:43:39', 1, 7, 'admin', '123456', NULL, '[9, 3, 1]', 'admin', 1, 7, 7, NULL, '21332132131241242143414324341', 'data:image/jpeg;base64,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', '[\"3231321\", \"3213\", \"萨达阿伟\"]', '940cfe4316cc4c1785edc0545ccd2564');
INSERT INTO `user` VALUES (NULL, NULL, 1, 12, '系统', '', NULL, '[1]', '系统', 1, NULL, NULL, 10, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for user_login_record
-- ----------------------------
DROP TABLE IF EXISTS `user_login_record`;
CREATE TABLE `user_login_record`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `token` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '登陆token',
  `code` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '账号',
  `user_id` int(11) NULL DEFAULT NULL,
  `user_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '用户名称',
  `logout_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '退出类型',
  `login_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '登陆方式   扫码  账号密码等',
  `login_time` datetime NULL DEFAULT NULL COMMENT '登陆时间',
  `logout_time` datetime NULL DEFAULT NULL COMMENT '退出时间',
  `login_ip` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '登录IP',
  `ret_msg` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '返回信息',
  `ret_code` varchar(9) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '是否登陆成功  返回状态码  0成功',
  `address` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '地址',
  `source_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '来源',
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `creation_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_login_record_code`(`code`) USING BTREE,
  INDEX `idx_login_record_login_time`(`login_time`) USING BTREE,
  INDEX `idx_login_record_login_type`(`login_type`) USING BTREE,
  INDEX `idx_login_record_login_ip`(`login_ip`) USING BTREE,
  INDEX `idx_login_record_ret_code`(`ret_code`) USING BTREE,
  INDEX `idx_login_record_token`(`token`) USING BTREE,
  INDEX `idx_login_record_code_logintime`(`code`, `login_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_login_record
-- ----------------------------

-- ----------------------------
-- Table structure for timed_task_case
-- ----------------------------
DROP TABLE IF EXISTS `timed_task_case`;
CREATE TABLE `timed_task_case`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` bigint(20) NULL DEFAULT NULL,
  `case_id` bigint(20) NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '类型, case, ui, script, api',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `enabled_flag` tinyint(1) NULL DEFAULT 1 COMMENT '是否删除',
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of timed_task_case
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
