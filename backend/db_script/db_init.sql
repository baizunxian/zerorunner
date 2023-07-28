/*
 Navicat Premium Data Transfer

 Source Server         : 0.0.0.0-tx
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : 0.0.0.0:3306
 Source Schema         : zerorunner

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 28/07/2023 14:12:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for api_case
-- ----------------------------
DROP TABLE IF EXISTS `api_case`;
CREATE TABLE `api_case`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `project_id` int NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int NOT NULL COMMENT '更新人',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人',
  `headers` json NULL COMMENT '请求头',
  `variables` json NULL COMMENT '变量',
  `step_data` json NULL COMMENT '步骤',
  `step_rely` int NULL DEFAULT 1 COMMENT '步骤依赖  1依赖， 0 不依赖',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for api_case_step
-- ----------------------------
DROP TABLE IF EXISTS `api_case_step`;
CREATE TABLE `api_case_step`  (
  `id` bigint NOT NULL,
  `parent_id` bigint NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `step_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `case_id` int NULL DEFAULT NULL,
  `value` json NULL,
  `enable` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `index` int NULL DEFAULT NULL,
  `suite_id` int NULL DEFAULT NULL,
  `node_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_case_step
-- ----------------------------

-- ----------------------------
-- Table structure for api_info
-- ----------------------------
DROP TABLE IF EXISTS `api_info`;
CREATE TABLE `api_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用例/配置名称',
  `project_id` int NULL DEFAULT NULL COMMENT '所属项目',
  `module_id` int NULL DEFAULT NULL COMMENT '所属模块',
  `status` int NULL DEFAULT 10 COMMENT '用例状态 10, 生效 ， 20 失效',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '接口code',
  `code_id` int NULL DEFAULT NULL COMMENT '关联接口id',
  `priority` int NULL DEFAULT NULL COMMENT '优先级',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '请求地址',
  `method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '请求方法',
  `tags` json NULL COMMENT '用例标签',
  `enable` int NULL DEFAULT NULL,
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
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
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
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;


-- ----------------------------
-- Table structure for api_test_report
-- ----------------------------
DROP TABLE IF EXISTS `api_test_report`;
CREATE TABLE `api_test_report`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '报告名称',
  `start_time` datetime NULL DEFAULT NULL COMMENT '执行时间',
  `duration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运行耗时',
  `case_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '执行用例id',
  `run_mode` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '运行模式， case 用例， suites 套件',
  `run_type` int NULL DEFAULT NULL COMMENT '运行类型， 10 同步， 20 异步，30 定时任务',
  `success` int NULL DEFAULT NULL COMMENT '是否成功， True, False',
  `run_count` int NULL DEFAULT NULL COMMENT '运行步骤数',
  `actual_run_count` int NULL DEFAULT NULL COMMENT '实际步骤数',
  `run_success_count` int NULL DEFAULT NULL COMMENT '运行成功数',
  `run_fail_count` int NULL DEFAULT NULL,
  `run_err_count` int NULL DEFAULT NULL,
  `run_skip_count` int NULL DEFAULT NULL COMMENT '跳过',
  `run_log` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '运行日志',
  `project_id` int NULL DEFAULT NULL COMMENT '项目id',
  `module_id` int NULL DEFAULT NULL COMMENT '模块id',
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1 COMMENT '是否删除, 0 删除 1 非删除',
  `env_id` int NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `exec_user_id` int NULL DEFAULT NULL,
  `exec_user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 380 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_test_report
-- ----------------------------

-- ----------------------------
-- Table structure for api_test_report_detail_0
-- ----------------------------
DROP TABLE IF EXISTS `api_test_report_detail_0`;
CREATE TABLE `api_test_report_detail_0`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `case_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `success` int NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `step_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `parent_step_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `step_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `env_variables` json NULL,
  `variables` json NULL,
  `case_variables` json NULL,
  `session_data` json NULL,
  `export_vars` json NULL,
  `report_id` int NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1 COMMENT '是否删除, 0 删除 1 非删除',
  `duration` decimal(10, 3) NULL DEFAULT NULL COMMENT '运行耗时',
  `step_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'pre 前置，post 后置，controller 控制器',
  `pre_hook_data` json NULL,
  `post_hook_data` json NULL,
  `setup_hook_results` json NULL COMMENT '前置hook结果',
  `teardown_hook_results` json NULL COMMENT '后置hook结果',
  `index` int NULL DEFAULT NULL,
  `status_code` int NULL DEFAULT NULL,
  `response_time_ms` decimal(10, 2) NULL DEFAULT NULL,
  `elapsed_ms` decimal(10, 2) NULL DEFAULT NULL,
  `log` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `exec_user_id` int NULL DEFAULT NULL,
  `exec_user_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3018 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_test_report_detail_0
-- ----------------------------

-- ----------------------------
-- Table structure for case_info
-- ----------------------------
DROP TABLE IF EXISTS `case_info`;
CREATE TABLE `case_info`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `case_type` int NULL DEFAULT 1 COMMENT 'test/config,测试类型, 1 case  2 config',
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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of case_info
-- ----------------------------

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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
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
  `id` int NOT NULL AUTO_INCREMENT,
  `every` int NOT NULL,
  `period` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_interval_schedule
-- ----------------------------

-- ----------------------------
-- Table structure for celery_periodic_task
-- ----------------------------
DROP TABLE IF EXISTS `celery_periodic_task`;
CREATE TABLE `celery_periodic_task`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `task` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `interval_id` int NULL DEFAULT NULL,
  `crontab` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
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
  `total_run_count` int NULL DEFAULT NULL,
  `date_changed` datetime NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `run_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `project_id` int NULL DEFAULT NULL,
  `module_id` int NULL DEFAULT NULL,
  `suite_id` int NULL DEFAULT NULL,
  `case_ids` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `ui_env_id` int NULL DEFAULT NULL,
  `ui_ids` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `script_ids` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT NULL,
  `run_mode` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `task_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'crontab interval',
  `case_env_id` int NULL DEFAULT NULL,
  `interval_every` int NULL DEFAULT NULL,
  `interval_period` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `task_tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_periodic_task
-- ----------------------------

-- ----------------------------
-- Table structure for celery_periodic_task_changed
-- ----------------------------
DROP TABLE IF EXISTS `celery_periodic_task_changed`;
CREATE TABLE `celery_periodic_task_changed`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `last_update` datetime NOT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_periodic_task_changed
-- ----------------------------
INSERT INTO `celery_periodic_task_changed` VALUES (1, '2023-07-25 10:58:43', NULL, NULL, '2023-07-25 10:58:42', NULL, NULL, NULL);

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_solar_schedule
-- ----------------------------

-- ----------------------------
-- Table structure for celery_task_record
-- ----------------------------
DROP TABLE IF EXISTS `celery_task_record`;
CREATE TABLE `celery_task_record`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `task_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `task_type` int NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `end_time` datetime NULL DEFAULT NULL,
  `duration` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `traceback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `business_id` int NULL DEFAULT NULL,
  `kwargs` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `args` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of celery_task_record
-- ----------------------------

-- ----------------------------
-- Table structure for data_source
-- ----------------------------
DROP TABLE IF EXISTS `data_source`;
CREATE TABLE `data_source`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源类型',
  `host` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '主机名',
  `port` int NULL DEFAULT NULL COMMENT '端口',
  `user` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '数据源名称',
  `env_id` int NULL DEFAULT NULL COMMENT '所属环境id',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `enabled_flag` tinyint(1) NULL DEFAULT 1 COMMENT '是否删除',
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
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
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `domain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '环境域名',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NOT NULL DEFAULT 1,
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `variables` json NULL COMMENT '环境变量',
  `headers` json NULL COMMENT '环境请求头',
  `data_sources` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env
-- ----------------------------

-- ----------------------------
-- Table structure for env_config
-- ----------------------------
DROP TABLE IF EXISTS `env_config`;
CREATE TABLE `env_config`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '环境名称',
  `domain_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '环境域名',
  `variables` json NULL COMMENT '环境变量',
  `headers` json NULL COMMENT '环境请求头',
  `creation_date` datetime NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `enabled_flag` int NOT NULL DEFAULT 1,
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of env_config
-- ----------------------------

-- ----------------------------
-- Table structure for env_data_source
-- ----------------------------
DROP TABLE IF EXISTS `env_data_source`;
CREATE TABLE `env_data_source`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `env_id` int NULL DEFAULT NULL,
  `data_source_id` int NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `creation_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_id`(`id`) USING BTREE,
  INDEX `index_env_id`(`env_id`) USING BTREE,
  INDEX `index_data_source_id`(`data_source_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 51 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of env_data_source
-- ----------------------------

-- ----------------------------
-- Table structure for env_func
-- ----------------------------
DROP TABLE IF EXISTS `env_func`;
CREATE TABLE `env_func`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `env_id` int NULL DEFAULT NULL,
  `func_id` int NULL DEFAULT NULL,
  `enabled_flag` tinyint(1) NULL DEFAULT NULL COMMENT '是否删除',
  `creation_date` timestamp NULL DEFAULT NULL COMMENT '创建时间',
  `updation_date` timestamp NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created_by` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_id`(`id`) USING BTREE,
  INDEX `index_env_id`(`env_id`) USING BTREE,
  INDEX `index_data_source_id`(`func_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_file_info_extend_name`(`extend_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of file_info
-- ----------------------------

-- ----------------------------
-- Table structure for functions
-- ----------------------------
DROP TABLE IF EXISTS `functions`;
CREATE TABLE `functions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `func_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `func_tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of functions
-- ----------------------------

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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of lookup
-- ----------------------------
INSERT INTO `lookup` VALUES (3, 'api_report_run_type', '测试报告执行类型', '2022-05-04 12:48:38', '2022-05-04 12:48:37', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (4, 'api_report_run_mode', '测试报告运行模式', '2022-05-04 14:29:45', '2022-05-04 14:29:44', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (5, 'api_timed_task_status', '定时任务运行状态', '2022-05-04 16:36:13', '2022-09-15 16:44:26', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (7, 'api_step_type', '用例类型', '2022-12-16 15:55:42', '2022-12-16 15:55:42', 1, 7, 7, NULL);

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
  `creation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '最后更新人',
  `updation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后更新时间',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_lookup_code`(`lookup_code`) USING BTREE,
  INDEX `idx_lookup_enable`(`enabled_flag`) USING BTREE,
  INDEX `idx_lookup_id`(`lookup_id`, `enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
INSERT INTO `lookup_value` VALUES (18, 9, '1', '2', '', 3, 1, '7', '2023-02-03 14:39:19', '7', '2023-02-03 14:39:19', NULL);
INSERT INTO `lookup_value` VALUES (19, 9, '2', '2', '', 2, 1, '7', '2023-02-03 14:58:39', '7', '2023-02-03 14:58:39', NULL);
INSERT INTO `lookup_value` VALUES (20, 9, '3', '3', '', 3, 1, '7', '2023-02-03 15:08:21', '7', '2023-02-03 15:08:21', NULL);
INSERT INTO `lookup_value` VALUES (21, 9, '4', '4', '', 4, 1, '7', '2023-02-03 15:12:30', '7', '2023-02-03 15:12:30', NULL);
INSERT INTO `lookup_value` VALUES (22, 9, '5', '5', '', 5, 1, '7', '2023-02-03 15:14:58', '7', '2023-02-03 15:19:51', NULL);
INSERT INTO `lookup_value` VALUES (23, 9, '6', '6', '', 6, 1, '7', '2023-02-03 15:30:51', '7', '2023-02-03 15:30:51', NULL);
INSERT INTO `lookup_value` VALUES (24, 9, '7', '7', '', 7, 1, '7', '2023-02-03 15:31:48', '7', '2023-02-03 15:31:48', NULL);
INSERT INTO `lookup_value` VALUES (25, 9, '8', '8', '', 8, 1, '7', '2023-02-03 15:33:40', '7', '2023-02-03 15:33:40', NULL);
INSERT INTO `lookup_value` VALUES (26, 9, '9', '9', '', 9, 1, '7', '2023-02-03 15:35:47', '7', '2023-02-03 15:35:47', NULL);
INSERT INTO `lookup_value` VALUES (27, 9, '10', '10', '', 10, 1, '7', '2023-02-03 15:36:22', '7', '2023-02-03 15:36:22', NULL);
INSERT INTO `lookup_value` VALUES (28, 9, '11', '11', '', 11, 1, '7', '2023-02-03 15:37:26', '7', '2023-02-03 15:37:26', NULL);
INSERT INTO `lookup_value` VALUES (29, 9, '12', '12', '', 12, 1, '7', '2023-02-03 15:46:26', '7', '2023-02-03 15:46:26', NULL);
INSERT INTO `lookup_value` VALUES (30, 9, '121', '12', '', 12, 1, '7', '2023-02-03 15:46:30', '7', '2023-02-03 15:46:30', NULL);
INSERT INTO `lookup_value` VALUES (31, 9, '13', '13', '', 13, 1, '7', '2023-02-03 15:52:31', '7', '2023-02-03 15:56:00', NULL);
INSERT INTO `lookup_value` VALUES (32, 9, '14', '14', '', 1, 1, '7', '2023-02-03 15:56:11', '7', '2023-02-03 15:56:11', NULL);

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
  `sort` int NULL DEFAULT NULL,
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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`, `path`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 72 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, 0, '/home', 'home', 'home/index.vue', '首页', 0, 0, 'ele-HomeFilled', 1, 1, 0, 'admin', 1, NULL, 10, NULL, NULL, '2023-07-25 10:57:18', 1, 0, 7, 7, NULL, 'eeacdb728f1a435aa4943565a25a9aa6');
INSERT INTO `menu` VALUES (28, 0, '/system', 'system', 'layout/routerView/parent', '系统设置', 0, 0, 'ele-Tools', 0, 0, 0, NULL, 10, NULL, 10, '/system/menu', NULL, '2023-05-26 14:46:00', 1, 0, 7, 7, NULL, 'b4803273f622479bbcd8b34a432554fc');
INSERT INTO `menu` VALUES (29, 28, '/system/menu', 'systemMenu', 'system/menu/index', '菜单管理', 0, 0, 'ele-Menu', 1, 0, 0, NULL, 1, NULL, 10, NULL, NULL, '2022-03-14 10:23:12', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (30, 28, '/system/user', 'systemUser', 'system/user/index', '用户管理', 0, 0, 'ele-User', 1, 0, 0, NULL, 2, NULL, 10, NULL, NULL, '2022-03-10 20:48:01', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (31, 28, '/system/role', 'systemRole', 'system/role/index', '角色管理', 0, 0, 'ele-UserFilled', 1, 0, 0, '', 1, NULL, 10, '', '2022-03-11 16:43:26', '2022-03-11 16:43:26', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (32, 0, '/api', 'api', 'layout/routerView/parent', 'API测试', 0, 0, 'ele-Apple', 1, 0, 0, '', 2, NULL, 10, '/api/project', '2022-03-14 17:02:22', '2022-03-14 17:02:22', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (33, 63, '/api/project', 'apiProject', 'api/project/index.vue', '项目列表', 0, 0, 'ele-Files', 1, 0, 0, '', 1, NULL, 10, '', '2022-03-14 17:16:38', '2023-02-23 11:08:26', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (34, 63, '/api/module', 'apiModule', 'api/module/index.vue', '模块列表', 0, 0, 'ele-FolderRemove', 1, 0, 0, '', 2, NULL, 10, '', '2022-03-19 18:36:51', '2023-02-23 11:08:31', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (35, 32, '/api/env', 'ApiEnv', 'api/environment/index.vue', '环境管理', 0, 0, 'ele-Monitor', 1, 0, 0, '', 8, NULL, 10, '', '2022-03-19 22:13:59', '2022-03-19 22:13:59', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (36, 69, '/api/timedTask', 'apiTimedTask', 'api/timedTask/index.vue', '定时任务', 0, 0, 'ele-Clock', 1, 0, 0, '', 7, NULL, 10, '', '2022-03-20 13:58:39', '2023-06-15 20:18:09', 1, 0, 7, 7, NULL, 'ea54da9ab01b4366a4a3290b77933600');
INSERT INTO `menu` VALUES (37, 32, '/api/apiInfo', 'apiInfo', 'api/apiInfo/index.vue', '接口管理', 0, 0, 'ele-DocumentRemove', 1, 0, 0, '', 3, NULL, 10, '', '2022-03-30 14:23:46', '2022-03-30 14:23:46', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (38, 37, '/api/apiInfo/edit', 'EditApiInfo', 'api/apiInfo/components/EditApi', '接口编辑', 0, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-03-30 15:53:20', '2023-07-28 12:25:49', 1, 0, 7, 7, NULL, '67f3ad18951e4ef19e2352dbd9c75a66');
INSERT INTO `menu` VALUES (40, 32, '/api/functions', 'ApiFunctions', '/api/functions/index.vue', '自定义函数', 0, 0, 'ele-MagicStick', 1, 0, 0, '', 6, NULL, 10, '', '2022-04-02 17:09:56', '2022-04-02 17:09:56', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (41, 40, '/api/functions/edit', 'EditFunc', '/api/functions/EditFunc', '编辑自定义函数', 0, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-04-02 17:27:20', '2022-04-02 17:27:20', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (42, 47, '/api/testcase/testReport', 'report', 'api/Report/components/report.vue', '报告详情', 0, 1, '', 0, 0, 0, '', 0, NULL, 10, '', '2022-04-07 17:20:19', '2022-04-07 17:20:19', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (47, 32, '/api/testcase/reportList', 'apiReport', 'api/Report/index.vue', '测试报告', 0, 0, 'ele-Document', 1, 0, 0, '', 5, NULL, 10, '', '2022-04-09 21:49:17', '2022-04-09 21:49:17', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (48, 32, '/api/config', 'config', 'api/configure/index.vue', '配置管理', 0, 1, 'ele-SetUp', 1, 0, 0, '', 4, NULL, 10, '', '2022-04-10 18:25:10', '2023-03-02 16:38:59', 1, 0, 7, 7, NULL, '18c372786f3d48b7966d888517098635');
INSERT INTO `menu` VALUES (49, 32, '/api/apiCase', 'apiCase', 'api/apiCase/index.vue', '测试用例', 0, 0, 'ele-Fold', 1, 0, 0, '', 4, NULL, 10, '', '2022-04-12 10:50:09', '2022-04-12 10:50:09', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (50, 49, '/api/apiCase/edit', 'EditApiCase', 'api/apiCase/EditApiCase', '编辑用例', 0, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-04-12 11:42:09', '2022-04-12 11:42:09', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (51, 28, '/system/lookup', 'systemLookup', 'system/lookup/index.vue', '数据字典', 0, 0, 'ele-Management', 1, 0, 0, '', 3, NULL, 10, '', '2022-05-03 17:11:59', '2022-05-03 17:11:59', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (53, 0, '/tools', 'tools', 'layout/routerView/parent', '便捷工具', 0, 0, 'ele-ForkSpoon', 1, 0, 0, '', 5, NULL, 10, '', '2022-06-14 21:08:01', '2023-05-17 16:55:23', 1, 0, 7, 7, NULL, 'b2160537cf404a4c8158c760a9782183');
INSERT INTO `menu` VALUES (54, 53, '/tools/query_db', 'query_db', 'tools/queryDB/index.vue', '数据查询', 0, 0, 'ele-MagicStick', 1, 0, 0, '', 0, NULL, 10, '', '2022-06-14 21:09:29', '2023-05-17 16:55:10', 1, 0, 7, 7, NULL, 'ca8c2ca5bffe43c0929d6819ac4cb16e');
INSERT INTO `menu` VALUES (57, 0, '/ui', 'ui', 'layout/routerView/parent', 'UI测试', 1, 0, 'ele-Cherry', 1, 0, 0, 'admin', 3, NULL, 10, '', '2022-08-23 11:05:09', '2023-07-25 10:58:21', 1, 0, 7, 7, NULL, 'c409bf80a3224713b5edb5a842cc6aa8');
INSERT INTO `menu` VALUES (58, 32, '/api/dataSource', 'ApiDataSource', 'api/dataSource/index.vue', '数据源管理', 0, 0, 'ele-Tickets', 1, 0, 0, '', 9, NULL, 10, '', '2022-09-13 14:34:44', '2022-09-13 14:34:43', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (59, 53, '/tools/testcase', 'apiTest', 'api/apiTest/index.vue', '接口测试', 0, 1, '', 0, 0, 0, '', 0, NULL, 10, '', '2022-09-13 16:00:00', '2023-05-17 16:55:33', 1, 0, 7, 7, NULL, 'f125ed0be43d4fff99d121a21aef54a5');
INSERT INTO `menu` VALUES (60, 49, '/api/ApiCase/edit', 'EditApiCase', 'api/apiCase/EditApiCase', '编辑套件新', 0, 1, 'ele-Apple', 1, 0, 0, '', 0, NULL, 10, '', '2022-09-27 16:12:03', '2022-09-27 16:12:02', 0, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (61, 28, '/system/personal', 'personal', 'system/personal/index', '个人中心', 0, 0, 'ele-User', 1, 0, 0, '', 0, NULL, 10, '', '2023-01-16 16:37:40', '2023-01-31 14:42:58', 1, 3, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (62, 53, '/websocket', '连接1', 'tools/websocket/index.vue', '连接1', 0, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-02-09 12:27:42', '2023-05-17 16:55:29', 1, 0, 7, 7, NULL, 'a8c4c5077f514f55b97dca9c981d413b');
INSERT INTO `menu` VALUES (63, 0, '/projectOrModule', '/projectOrModule', 'layout/routerView/parent', '项目/模块', 0, 0, 'ele-Files', 1, 0, 1, '0', 1, NULL, 10, '', '2023-02-23 11:07:56', '2023-07-07 15:49:06', 1, 0, NULL, 7, NULL, '702b232958d84ce59b5dced44a4836ff');
INSERT INTO `menu` VALUES (64, 57, '/ui/page', 'uiPage', 'ui/page/index.vue', '页面管理', 0, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-05-26 11:12:13', '2023-05-26 11:12:57', 1, 0, 7, 7, NULL, 'ae8cbb970fe94b57a74243e5a2448b5b');
INSERT INTO `menu` VALUES (65, 64, '/ui/page/edite', 'EditPage', 'ui/page/EditPage.vue', '页面编辑', 0, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-05-26 14:47:33', '2023-05-26 15:21:36', 1, 0, 7, 7, NULL, 'dcbd130fd512496ba3b95292bfaf370c');
INSERT INTO `menu` VALUES (66, 57, '/ui/uiCase', 'uiCase', 'ui/uiCase/index.vue', '测试用例', 0, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-05-27 23:29:46', '2023-06-14 16:18:50', 1, 0, 7, 7, NULL, '0041e560003f4337b5d9326a499e0447');
INSERT INTO `menu` VALUES (67, 66, '/ui/uiCase/edit', 'editUiCase', 'ui/uiCase/editUiCase.vue', '用例编辑', 0, 1, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-06-02 10:02:18', '2023-06-14 16:18:57', 1, 0, 7, 7, NULL, 'a745d4ae3e7940ddbb8515ea06a26fb5');
INSERT INTO `menu` VALUES (68, 57, '/ui/uiReport', 'uiReport', 'ui/uiReport/index.vue', '测试报告', 0, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-06-13 16:48:52', '2023-06-14 16:19:01', 1, 0, 7, 7, NULL, '325eeece337b450c8e04bc83d0a802d3');
INSERT INTO `menu` VALUES (69, 0, '/job', 'job', 'layout/routerView/parent', '定时任务', 0, 0, 'ele-AlarmClock', 1, 0, 0, '0', 4, NULL, 10, '', '2023-06-15 19:53:23', '2023-06-15 20:36:07', 1, 0, 7, 7, NULL, '0fe72ee35bdc41ca9adc60e01576383f');
INSERT INTO `menu` VALUES (70, 69, '/job/taskRecord', 'taskRecord', 'job/taskRecord/index.vue', '执行记录', 0, 0, 'ele-Document', 1, 0, 0, '0', 2, NULL, 10, '', '2023-06-15 19:54:28', '2023-06-15 20:19:14', 1, 0, 7, 7, NULL, '9f7d85770e004da6a97d4e0ec29a21c3');

-- ----------------------------
-- Table structure for menu_view_history
-- ----------------------------
DROP TABLE IF EXISTS `menu_view_history`;
CREATE TABLE `menu_view_history`  (
  `menu_id` int NULL DEFAULT NULL COMMENT '菜单id',
  `remote_addr` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '访问ip',
  `user_id` int NULL DEFAULT NULL COMMENT '访问人',
  `id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_menu_view_history_remote_addr`(`remote_addr`) USING BTREE,
  INDEX `ix_menu_view_history_user_id`(`user_id`) USING BTREE,
  INDEX `ix_menu_view_history_menu_id`(`menu_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of menu_view_history
-- ----------------------------

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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_module_info_module_name`(`name`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of module_info
-- ----------------------------

-- ----------------------------
-- Table structure for notify
-- ----------------------------
DROP TABLE IF EXISTS `notify`;
CREATE TABLE `notify`  (
  `user_id` int NULL DEFAULT NULL COMMENT '用户id',
  `group` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '组',
  `message` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '消息',
  `send_status` int NULL DEFAULT NULL COMMENT '发送状态，10成功 20 失败',
  `read_status` int NULL DEFAULT NULL COMMENT '消息状态，10未读 20 已读',
  `id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_notify_user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of notify
-- ----------------------------

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
  `enabled_flag` int NULL DEFAULT NULL COMMENT '是否删除',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int NOT NULL COMMENT '更新人',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_project_info_name`(`name`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 601 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of project_info
-- ----------------------------

-- ----------------------------
-- Table structure for request_history
-- ----------------------------
DROP TABLE IF EXISTS `request_history`;
CREATE TABLE `request_history`  (
  `id` int NOT NULL AUTO_INCREMENT,
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
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of request_history
-- ----------------------------

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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES (1, '管理员', '管理员', 10, '1,38,50,48,42,41,36,35,58,33,34,65,67,68,70,62,59,54,61,31,29,30,51', '2021-04-12 16:56:20', '2023-06-15 19:55:00', 1, 7, 7, 10, 'ceee14e4b6784b1bb38d63b91afde1e3');
INSERT INTO `roles` VALUES (3, '测试工程师', '测试工程师', 10, '1,33,34,38,50,48,42,41,35,58,65,67,68,36,59,54,31,29,30,51', '2021-05-21 17:24:53', '2023-07-22 16:22:43', 1, 7, 7, 10, '7ff342ceb2ea4eedba0f70929b8d7c57');
INSERT INTO `roles` VALUES (6, '', '报表查看', 10, '60,34,51,62', '2021-11-29 19:49:40', '2022-05-06 21:45:44', 0, 15, 15, 10, NULL);
INSERT INTO `roles` VALUES (7, '', 'ui自动化', 10, '67,13,14,16,15', '2022-02-09 17:57:12', '2022-05-06 21:45:40', 0, 7, 15, 10, NULL);
INSERT INTO `roles` VALUES (8, '测试角色', '测试角色', 10, '1,28,29,31,30', '2022-03-14 16:32:17', '2022-03-14 16:58:27', 0, 7, 7, 10, NULL);
INSERT INTO `roles` VALUES (9, '1', 'test', 10, '1,33,34,38,48,50,42,41,36,35', '2022-05-12 10:30:05', '2023-02-03 15:57:14', 1, 7, 7, 10, NULL);
INSERT INTO `roles` VALUES (10, '', ',', 10, '33,34,38,48,50,42,41,36,35', '2022-06-24 10:13:52', '2022-10-09 20:50:30', 0, 7, 7, 10, NULL);
INSERT INTO `roles` VALUES (11, '测试', '测试角色', 10, '1,2,3', '2023-01-31 15:36:59', '2023-01-31 15:39:11', 0, 10, 10, 10, NULL);

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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `creation_date_index`(`creation_date`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 55 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of test_reports
-- ----------------------------

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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
  `id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `project_id` int NULL DEFAULT NULL,
  `module_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_case_name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
  `page_id` int NOT NULL COMMENT '关联页面',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_element_name`(`name`) USING BTREE,
  INDEX `ix_ui_element_page_id`(`page_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
  `project_id` int NULL DEFAULT NULL COMMENT '项目id',
  `module_id` int NULL DEFAULT NULL COMMENT '模块id',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `id` int NOT NULL AUTO_INCREMENT,
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `tags` json NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_page_project_id`(`project_id`) USING BTREE,
  INDEX `ix_ui_page_name`(`name`) USING BTREE,
  INDEX `ix_ui_page_module_id`(`module_id`) USING BTREE,
  INDEX `ix_ui_page_url`(`url`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ui_page
-- ----------------------------

-- ----------------------------
-- Table structure for ui_report_detail_0
-- ----------------------------
DROP TABLE IF EXISTS `ui_report_detail_0`;
CREATE TABLE `ui_report_detail_0`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `index` int NULL DEFAULT NULL,
  `variables` json NULL,
  `data` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `action` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `location_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `location_value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `report_id` int NULL DEFAULT NULL,
  `success` int NULL DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `case_id` int NULL DEFAULT NULL,
  `step_id` int NULL DEFAULT NULL,
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `start_time` datetime NULL DEFAULT NULL,
  `duration` decimal(10, 3) NULL DEFAULT NULL,
  `setup_hook_results` json NULL,
  `teardown_hook_results` json NULL,
  `validator_results` json NULL,
  `screenshot_file_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `log` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `creation_date` datetime NULL DEFAULT NULL,
  `created_by` int NULL DEFAULT NULL,
  `updation_date` datetime NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `enabled_flag` int NULL DEFAULT 1,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ui_report_detail_0
-- ----------------------------

-- ----------------------------
-- Table structure for ui_reports
-- ----------------------------
DROP TABLE IF EXISTS `ui_reports`;
CREATE TABLE `ui_reports`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '报告名',
  `project_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '项目id',
  `module_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '模块id',
  `success` int NULL DEFAULT NULL COMMENT '是否成功',
  `status` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '状态',
  `duration` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '执行耗时',
  `case_id` int NULL DEFAULT NULL COMMENT '用例id',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'trace_id',
  `start_time` datetime NULL DEFAULT NULL,
  `run_type` int NULL DEFAULT NULL,
  `run_count` int NULL DEFAULT NULL,
  `run_success_count` int NULL DEFAULT NULL,
  `run_fail_count` int NULL DEFAULT NULL,
  `run_skip_count` int NULL DEFAULT NULL,
  `run_err_count` int NULL DEFAULT NULL,
  `run_log` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `env_id` int NULL DEFAULT NULL,
  `exec_user_id` int NULL DEFAULT NULL,
  `exec_user_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_reports_project_id`(`project_id`) USING BTREE,
  INDEX `ix_ui_reports_module_id`(`module_id`) USING BTREE,
  INDEX `ix_ui_reports_case_id`(`case_id`) USING BTREE,
  INDEX `ix_ui_reports_success`(`success`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of ui_reports
-- ----------------------------

-- ----------------------------
-- Table structure for ui_steps
-- ----------------------------
DROP TABLE IF EXISTS `ui_steps`;
CREATE TABLE `ui_steps`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `index` int NOT NULL COMMENT '步骤排序',
  `operation` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '操作',
  `input_data` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '输入数据',
  `location_method` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '定位元素方式',
  `location_value` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '定位元素值',
  `output` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '输出',
  `remarks` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '备注',
  `case_id` int NULL DEFAULT NULL COMMENT '关联ui测试用例',
  `creation_date` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `created_by` int NULL DEFAULT NULL COMMENT '创建人ID',
  `updation_date` datetime NOT NULL COMMENT '更新时间',
  `updated_by` int NULL DEFAULT NULL COMMENT '更新人ID',
  `enabled_flag` tinyint(1) NOT NULL COMMENT '是否删除, 0 删除 1 非删除',
  `trace_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'trace_id',
  `version` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_ui_steps_index`(`index`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '密码',
  `roles` json NULL COMMENT '用户角色',
  `nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户昵称',
  `status` int NULL DEFAULT 1 COMMENT '用户状态 0 正常 1锁定',
  `created_by` int NULL DEFAULT NULL,
  `updated_by` int NULL DEFAULT NULL,
  `user_type` int NULL DEFAULT 10 COMMENT '用户类型， 10 管理人员, 20 测试人员',
  `remarks` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户描述',
  `avatar` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '头像数据',
  `tags` json NULL COMMENT '用户标签',
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_user_email`(`email`) USING BTREE,
  INDEX `ix_user_password`(`password`) USING BTREE,
  INDEX `ix_user_username`(`username`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (NULL, NULL, 1, 0, '系统', '', NULL, '[1]', '系统', 1, NULL, NULL, 10, NULL, NULL, NULL, NULL);
INSERT INTO `user` VALUES ('2020-11-20 10:04:08', '2023-05-20 22:08:26', 1, 1, 'xiaobai', 'o1qooQ2aDAxzq2r7YAxbk7mNHvyDQ0iyFngiSpp6rkBUwzpCqYwyd4hpXKk8x4ZUKKEKUbCIZSS+1lEnHhOH67COnHszbOq/vWdVGHZOXehYv02yj3jO/q7/Moh9KoLWHSpBJN8MfqdxvdmvowfWzeQz2DbD81BlyKXTSwyYeek=', '546142369@qq.com', '[1]', '小白', 1, 7, 1, 10, 'xiaobai', 'data:image/jpeg;base64,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', '[\"xiaobai\"]', '6b8991eb68314e54ad5c175fa301e790');
INSERT INTO `user` VALUES ('2021-04-12 15:35:51', '2022-03-11 16:27:57', 1, 3, 'dabai', 'o1qooQ2aDAxzq2r7YAxbk7mNHvyDQ0iyFngiSpp6rkBUwzpCqYwyd4hpXKk8x4ZUKKEKUbCIZSS+1lEnHhOH67COnHszbOq/vWdVGHZOXehYv02yj3jO/q7/Moh9KoLWHSpBJN8MfqdxvdmvowfWzeQz2DbD81BlyKXTSwyYeek=', NULL, '[3]', '大白', 1, 7, 7, 20, NULL, NULL, NULL, NULL);
INSERT INTO `user` VALUES ('2022-03-09 15:23:11', '2022-03-09 15:23:11', 1, 6, '小白01', 'j9rAQQneij3uCnynqVM4ymCR809ZHI/iLzheP7I/0f/u7vGTaBi+S6XW0jliJdjFnYTxRL8o3v6rZwjazO0TmaEHmY5/isF7UPPyDPDm43l2DoiY9CRz4vpuIr/EGHXkhq45q/Wv2XFDPWW0irxRGH6bLmxEBb0HlP8VYV1Vszs=', NULL, NULL, NULL, 0, 7, 7, 20, NULL, NULL, NULL, NULL);
INSERT INTO `user` VALUES ('2022-05-11 09:46:50', '2022-05-11 09:46:49', 1, 8, 'tangsong', 'BRjQu2+2PGD+xqgNQgsr96izijhsWDFMwRK5jRk7bDYDthGEdt0tmlx1BLHbBPsaSiG9U5MQWSD//Jt3k26uDG0HgOm3J0OnpugdD+S28w9O0lv5O7//Op0rcyHPThuWYZFKfJXyljuZnq1FZiijwqHLXuFIWvfVvOiMDTGitGQ=', '', '[3]', 'tangsong', 1, 7, 7, 20, '', NULL, NULL, NULL);
INSERT INTO `user` VALUES (NULL, '2023-05-20 22:02:05', 1, 9, 'xiaobai01', '123456', NULL, '[9, 1]', 'xiaobai01', 0, NULL, 7, 20, NULL, NULL, '[9]', '26b706149c6141479a3f9972aa1f839c');
INSERT INTO `user` VALUES ('2023-01-30 21:00:32', '2023-01-31 10:31:56', 0, 10, 'xiaobai02', 'STLoIYvZxlbKe4nQODu1zm16d5YDpdG2Z+lrg0RKGj4KRUI48qdY6w/82C4sKatiJ98H83xHxIsI5BKzlnZYs2hGUNCGIE85FkBc5YuD7EDF+6u3BVaMa+whcxjKFVVOd5Y/XzaIQ6FIyNRe/MHotYicgQ1d/dZUULanu9dns1k=', NULL, NULL, 'xiaobai021', 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for user_login_record
-- ----------------------------
DROP TABLE IF EXISTS `user_login_record`;
CREATE TABLE `user_login_record`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '登陆token',
  `code` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '账号',
  `user_id` int NULL DEFAULT NULL,
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
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_login_record_code`(`code`) USING BTREE,
  INDEX `idx_login_record_login_time`(`login_time`) USING BTREE,
  INDEX `idx_login_record_login_type`(`login_type`) USING BTREE,
  INDEX `idx_login_record_login_ip`(`login_ip`) USING BTREE,
  INDEX `idx_login_record_ret_code`(`ret_code`) USING BTREE,
  INDEX `idx_login_record_token`(`token`) USING BTREE,
  INDEX `idx_login_record_code_logintime`(`code`, `login_time`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13127234 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_login_record
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
