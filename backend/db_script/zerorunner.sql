/*
 Navicat Premium Data Transfer

 Source Server         : zerorunner
 Source Server Type    : MySQL
 Source Server Version : 50743
 Source Host           : zerorunner:3306
 Source Schema         : zerorunner

 Target Server Type    : MySQL
 Target Server Version : xiaobai
 File Encoding         : 65001

 Date: 12/10/2023 20:48:50
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
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_case
-- ----------------------------

-- ----------------------------
-- Table structure for api_case_step
-- ----------------------------
DROP TABLE IF EXISTS `api_case_step`;
CREATE TABLE `api_case_step`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `step_id` bigint(20) NULL DEFAULT NULL,
  `parent_id` bigint(20) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `step_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `case_id` int(11) NULL DEFAULT NULL,
  `step_data` json NULL,
  `enable` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `index` int(11) NULL DEFAULT NULL,
  `api_id` bigint(20) NULL DEFAULT NULL,
  `node_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `version` int(11) NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

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
  `sql_request` json NULL,
  `if_data` json NULL,
  `wait_data` json NULL,
  `loop_data` json NULL,
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
) ENGINE = InnoDB AUTO_INCREMENT = 1711681836897411062 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_test_report_detail_0
-- ----------------------------

-- ----------------------------
-- Table structure for case_info
-- ----------------------------
DROP TABLE IF EXISTS `case_info`;
CREATE TABLE `case_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_type` int(11) NULL DEFAULT 1 COMMENT 'test/config,测试类型, 1 case  2 config',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用例/配置名称',
  `project_id` int(11) NULL DEFAULT NULL COMMENT '所属项目',
  `module_id` int(11) NULL DEFAULT NULL COMMENT '所属模块',
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `include` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '前置config/test',
  `testcase` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `service_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '所属服务名称',
  `run_type` int(11) NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `case_status` int(11) NULL DEFAULT 10 COMMENT '用例状态 10, 生效 ， 20 失效',
  `priority` int(11) NULL DEFAULT NULL COMMENT '优先级',
  `config_id` int(11) NULL DEFAULT NULL COMMENT '用例配置id',
  `code_id` int(11) NULL DEFAULT NULL COMMENT '关联接口id',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '接口code',
  `case_tab` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用例标签',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of case_info
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
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_interval_schedule
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_periodic_task
-- ----------------------------
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
INSERT INTO `celery_periodic_task_changed` VALUES (1, '2023-10-11 16:44:40', NULL, NULL, '2023-10-11 14:28:22', NULL, NULL, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_task_record
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env_data_source
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env_func
-- ----------------------------

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
INSERT INTO `functions` VALUES (3, NULL, 'import random\r\nimport string\r\n\r\ndef random_phone(prefix=\"139\"):\r\n    \"\"\"\r\n    :desc 生成随机手机号码\r\n    :name 手机号码\r\n    :param prefix: 号码前缀\r\n    :return phone<string>: 手机号码\r\n    \"\"\"\r\n    print(prefix)\r\n    random_len=11\r\n    phone_list=[]\r\n    if prefix:\r\n        phone_list.append(prefix)\r\n        random_len = random_len-len(prefix)\r\n    random_list=random.choices(string.digits, k=random_len)\r\n    phone_list.extend(random_list)\r\n    phone=\'\'.join(phone_list)\r\n    return phone\r\n\r\n\r\ndef dictionary_value(val, key):\r\n    \"\"\"\r\n    字典取值\r\n    \"\"\"\r\n    return val[key]\r\n', '2022-12-28 10:57:31', 7, '2023-10-11 13:54:40', 7, 1, '测试打的', '阿萨德', 'dae14e3bda8b48c78cb141699dce07bd', NULL, NULL);
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
INSERT INTO `lookup` VALUES (3, 'api_report_run_type', '测试报告执行类型', '2022-05-04 12:48:38', '2023-10-10 17:08:40', 1, 7, 7, '96d421c1bce14772b9128a3ea340ec94');
INSERT INTO `lookup` VALUES (4, 'api_report_run_mode', '测试报告运行模式', '2022-05-04 14:29:45', '2022-05-04 14:29:44', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (5, 'api_timed_task_status', '定时任务运行状态', '2022-05-04 16:36:13', '2022-09-15 16:44:26', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (6, 'test', 'test', '2022-09-15 16:44:37', '2022-09-15 17:03:08', 0, 7, 7, NULL);
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
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of lookup_value
-- ----------------------------
INSERT INTO `lookup_value` VALUES (6, 3, '10', '同步', '', 1, 1, '7', '2022-05-04 12:48:53', '7', '2023-07-06 10:54:26', 'd3d2611f5e384b97b6904595caeff75c');
INSERT INTO `lookup_value` VALUES (7, 3, 'suite', '套件', '', 2, 0, '7', '2022-05-04 12:49:12', '7', '2023-05-19 16:31:37', NULL);
INSERT INTO `lookup_value` VALUES (8, 4, '1', '同步', '', 1, 1, '7', '2022-05-04 14:39:14', '7', '2022-05-04 14:39:14', NULL);
INSERT INTO `lookup_value` VALUES (9, 4, '2', '异步', '', 2, 1, '7', '2022-05-04 14:39:26', '7', '2022-05-04 14:39:25', NULL);
INSERT INTO `lookup_value` VALUES (10, 4, '3', '定时任务', '', 3, 1, '7', '2022-05-04 14:39:26', '7', '2022-05-04 14:39:26', NULL);
INSERT INTO `lookup_value` VALUES (11, 3, '20', '异步', '', 3, 1, '7', '2022-05-04 15:32:17', '7', '2023-05-19 16:36:44', '97ad0c098dce4a8ba6a6bc0c445ab05e');
INSERT INTO `lookup_value` VALUES (12, 5, '1', '运行中', '', 2, 1, '7', '2022-05-04 16:36:34', '7', '2022-05-04 16:36:33', NULL);
INSERT INTO `lookup_value` VALUES (13, 5, '0', '停止', '', 1, 0, '7', '2022-05-04 16:36:34', '7', '2023-03-08 15:14:02', NULL);
INSERT INTO `lookup_value` VALUES (14, 7, 'case', '普通步骤', '', 12, 1, '7', '2022-12-16 15:56:00', '7', '2023-02-01 14:40:48', NULL);
INSERT INTO `lookup_value` VALUES (15, 7, 'if', 'IF', '', 2, 1, '7', '2022-12-16 15:56:12', '7', '2022-12-16 15:56:12', NULL);
INSERT INTO `lookup_value` VALUES (16, 7, 'loop', 'loop', '', 3, 1, '7', '2022-12-16 15:56:27', '7', '2022-12-16 15:56:26', NULL);
INSERT INTO `lookup_value` VALUES (17, 5, '0', '停止', '', 1, 1, '7', '2023-02-01 10:59:29', '7', '2023-02-01 10:59:29', NULL);


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
) ENGINE = InnoDB AUTO_INCREMENT = 79 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `menu` VALUES (54, 53, '/tools/query_db', 'query_db', 'tools/queryDB/index.vue', '数据查询', 0, NULL, 0, 'ele-MagicStick', 1, 0, 0, '', 0, NULL, 10, '', '2022-06-14 21:09:29', '2023-05-17 16:55:10', 1, 0, 7, 7, NULL, 'ca8c2ca5bffe43c0929d6819ac4cb16e');
INSERT INTO `menu` VALUES (57, 0, '/ui', 'ui', 'layout/routerView/parent', 'UI测试', 0, NULL, 0, 'ele-Cherry', 1, 0, 0, 'admin', 3, NULL, 10, '', '2022-08-23 11:05:09', '2023-10-12 19:44:23', 1, 0, 7, 7, NULL, '6b3d418ffeb040478f9be028cdcc3ee5');
INSERT INTO `menu` VALUES (58, 32, '/api/dataSource', 'ApiDataSource', 'api/dataSource/index.vue', '数据源管理', 0, NULL, 0, 'ele-Tickets', 1, 0, 0, '', 9, NULL, 10, '', '2022-09-13 14:34:44', '2022-09-13 14:34:43', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (59, 53, '/tools/testcase', 'apiTest', 'api/apiTest/index.vue', '接口测试', 0, NULL, 1, '', 0, 0, 0, '', 0, NULL, 10, '', '2022-09-13 16:00:00', '2023-07-31 10:31:56', 1, 0, 7, 7, NULL, '730571c1b89d46d492c1f07b83a0b726');
INSERT INTO `menu` VALUES (60, 49, '/api/ApiCase/edit', 'EditApiCase', 'api/apiCase/EditApiCase', '编辑套件新', 0, NULL, 1, 'ele-Apple', 1, 0, 0, '', 0, NULL, 10, '', '2022-09-27 16:12:03', '2022-09-27 16:12:02', 0, 0, 7, 7, NULL, NULL);
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
INSERT INTO `menu` VALUES (72, 35, '/ss', 'ss', '', 'ss', 0, NULL, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-08-09 20:28:15', '2023-08-18 12:54:34', 1, 0, 7, 7, NULL, '63646cdf20764ba3a25d14b9d820f64c');
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
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of module_info
-- ----------------------------

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of project_info
-- ----------------------------

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
-- Table structure for test_reports
-- ----------------------------
DROP TABLE IF EXISTS `test_reports`;
CREATE TABLE `test_reports`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_at` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `scene_num` int(11) NULL DEFAULT NULL COMMENT '场景数',
  `duration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '执行用时 秒',
  `run_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '运行类型，同步，异步',
  `task_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '任务类型, test,module,project',
  `run_mode` int(11) NULL DEFAULT NULL,
  `project_id` int(11) NULL DEFAULT NULL,
  `module_id` int(11) NULL DEFAULT NULL,
  `report_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `run_case_priority` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `execute_user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `execute_source` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `execute_service` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `successful_use_case` int(11) NULL DEFAULT NULL COMMENT '成功用例数',
  `report_body` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '报告详情',
  `run_test_count` int(11) NULL DEFAULT NULL COMMENT '运行用例数',
  `success` int(11) NULL DEFAULT NULL,
  `enabled_flag` int(11) NULL DEFAULT 1,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `created_by` int(11) NULL DEFAULT NULL,
  `updated_by` int(11) NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `creation_date_index`(`creation_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of test_reports
-- ----------------------------

-- ----------------------------
-- Table structure for test_suite
-- ----------------------------
DROP TABLE IF EXISTS `test_suite`;
CREATE TABLE `test_suite`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `project_id` int(11) NULL DEFAULT NULL,
  `include` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `config_id` int(11) NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int(11) NOT NULL COMMENT '更新人',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int(11) NULL DEFAULT NULL COMMENT '创建人',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of test_suite
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ui_case
-- ----------------------------

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
  `run_type` int(11) NULL DEFAULT NULL,
  `run_count` int(11) NULL DEFAULT NULL,
  `run_success_count` int(11) NULL DEFAULT NULL,
  `run_fail_count` int(11) NULL DEFAULT NULL,
  `run_skip_count` int(11) NULL DEFAULT NULL,
  `run_err_count` int(11) NULL DEFAULT NULL,
  `run_log` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `env_id` int(11) NULL DEFAULT NULL,
  `exec_user_id` int(11) NULL DEFAULT NULL,
  `exec_user_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
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
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('2022-03-09 16:03:43', '2023-10-11 14:47:23', 1, 7, 'admin', '123456', NULL, '[9, 3, 1]', 'admin', 1, 7, 7, NULL, '111', '', '[\"3231321\", \"3213\", \"萨达阿伟\"]', 'a79903f7516c4ceeb9c88221ee6ce206');
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
) ENGINE = InnoDB AUTO_INCREMENT = 13127913 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_login_record
-- ----------------------------
SET FOREIGN_KEY_CHECKS = 1;
