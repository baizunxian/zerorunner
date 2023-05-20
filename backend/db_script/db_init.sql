/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80021
 Source Host           : localhost:3306
 Source Schema         : localhost

 Target Server Type    : MySQL
 Target Server Version : 80021
 File Encoding         : 65001

 Date: 11/05/2023 14:33:19
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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_case
-- ----------------------------

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `enabled_flag_index`(`enabled_flag`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of api_info
-- ----------------------------

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
  `exec_user_id` int DEFAULT NULL,
  `exec_user_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of celery_periodic_task_changed
-- ----------------------------

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of lookup
-- ----------------------------
INSERT INTO `lookup` VALUES (3, 'api_report_run_type', '测试报告执行类型', '2022-05-04 12:48:38', '2022-05-04 12:48:37', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (4, 'api_report_run_mode', '测试报告运行模式', '2022-05-04 14:29:45', '2022-05-04 14:29:44', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (5, 'api_timed_task_status', '定时任务运行状态', '2022-05-04 16:36:13', '2022-09-15 16:44:26', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (7, 'api_step_type', '用例类型', '2022-12-16 15:55:42', '2022-12-16 15:55:42', 1, 7, 7, NULL);
INSERT INTO `lookup` VALUES (9, 'test', 'test', '2023-02-01 14:40:57', '2023-02-01 14:40:57', 1, 7, 7, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of lookup_value
-- ----------------------------
INSERT INTO `lookup_value` VALUES (6, 3, 'case', '用例', '', 1, 1, '7', '2022-05-04 12:48:53', '7', '2022-05-04 12:48:52', NULL);
INSERT INTO `lookup_value` VALUES (7, 3, 'suite', '套件', '', 2, 1, '7', '2022-05-04 12:49:12', '7', '2022-05-04 12:49:11', NULL);
INSERT INTO `lookup_value` VALUES (8, 4, '1', '同步', '', 1, 1, '7', '2022-05-04 14:39:14', '7', '2022-05-04 14:39:14', NULL);
INSERT INTO `lookup_value` VALUES (9, 4, '2', '异步', '', 2, 1, '7', '2022-05-04 14:39:26', '7', '2022-05-04 14:39:25', NULL);
INSERT INTO `lookup_value` VALUES (10, 4, '3', '定时任务', '', 3, 1, '7', '2022-05-04 14:39:26', '7', '2022-05-04 14:39:26', NULL);
INSERT INTO `lookup_value` VALUES (11, 3, 'module', '模块', '', 3, 1, '7', '2022-05-04 15:32:17', '7', '2022-05-04 15:32:17', NULL);
INSERT INTO `lookup_value` VALUES (12, 5, '1', '运行中', '', 2, 1, '7', '2022-05-04 16:36:34', '7', '2022-05-04 16:36:33', NULL);
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
) ENGINE = InnoDB AUTO_INCREMENT = 63 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of menu
-- ----------------------------
INSERT INTO `menu` VALUES (1, 0, '/home', 'home', 'home/index', '首页', 0, 0, 'ele-HomeFilled', 1, 1, 0, 'admin', 1, NULL, 10, NULL, NULL, '2023-02-01 14:41:05', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (28, 0, '/system', 'system', 'layout/routerView/parent', '系统设置', 0, 0, 'ele-Tools', NULL, 0, 0, NULL, 3, NULL, 10, '/system/menu', NULL, '2022-03-17 22:08:13', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (29, 28, '/system/menu', 'systemMenu', 'system/menu/index', '菜单管理', 0, 0, 'ele-Menu', 1, 0, 0, NULL, 1, NULL, 10, NULL, NULL, '2022-03-14 10:23:12', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (30, 28, '/system/user', 'systemUser', 'system/user/index', '用户管理', 0, 0, 'ele-User', 1, 0, 0, NULL, 2, NULL, 10, NULL, NULL, '2022-03-10 20:48:01', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (31, 28, '/system/role', 'systemRole', 'system/role/index', '角色管理', 0, 0, 'ele-UserFilled', 1, 0, 0, '', 1, NULL, 10, '', '2022-03-11 16:43:26', '2022-03-11 16:43:26', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (32, 0, '/api', 'api', 'layout/routerView/parent', 'API测试', 0, 0, 'ele-Apple', 1, 0, 0, '', 2, NULL, 10, '/api/project', '2022-03-14 17:02:22', '2022-03-14 17:02:22', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (33, 63, '/api/project', 'apiProject', 'api/project/index.vue', '项目列表', 0, 0, 'ele-Files', 1, 0, 0, '', 1, NULL, 10, '', '2022-03-14 17:16:38', '2023-02-23 11:08:26', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (34, 63, '/api/module', 'apiModule', 'api/module/index.vue', '模块列表', 0, 0, 'ele-FolderRemove', 1, 0, 0, '', 2, NULL, 10, '', '2022-03-19 18:36:51', '2023-02-23 11:08:31', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (35, 32, '/api/env', 'ApiEnv', 'api/environment/index.vue', '环境管理', 0, 0, 'ele-Monitor', 1, 0, 0, '', 8, NULL, 10, '', '2022-03-19 22:13:59', '2022-03-19 22:13:59', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (36, 32, '/api/timedTask', 'apiTimedTask', 'api/timedTask/index.vue', '定时任务', 0, 0, 'ele-Clock', 1, 0, 0, '', 7, NULL, 10, '', '2022-03-20 13:58:39', '2022-03-20 13:58:39', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (37, 32, '/api/apiInfo', 'apiInfo', 'api/apiInfo/index.vue', '接口管理', 0, 0, 'ele-DocumentRemove', 1, 0, 0, '', 3, NULL, 10, '', '2022-03-30 14:23:46', '2022-03-30 14:23:46', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (38, 37, '/api/apiInfo/edit', 'EditApiInfo', 'api/apiInfo/components/EditApi', '接口编辑', 0, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-03-30 15:53:20', '2022-03-30 15:53:20', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (40, 32, '/api/functions', 'ApiFunctions', '/api/functions/index.vue', '自定义函数', 0, 0, 'ele-MagicStick', 1, 0, 0, '', 6, NULL, 10, '', '2022-04-02 17:09:56', '2022-04-02 17:09:56', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (41, 40, '/api/functions/edit', 'EditFunc', '/api/functions/EditFunc', '编辑自定义函数', 0, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-04-02 17:27:20', '2022-04-02 17:27:20', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (42, 47, '/api/testcase/testReport', 'report', 'api/Report/components/report.vue', '报告详情', 0, 1, '', 0, 0, 0, '', 0, NULL, 10, '', '2022-04-07 17:20:19', '2022-04-07 17:20:19', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (47, 32, '/api/testcase/reportList', 'apiReport', 'api/Report/index.vue', '测试报告', 0, 0, 'ele-Document', 1, 0, 0, '', 5, NULL, 10, '', '2022-04-09 21:49:17', '2022-04-09 21:49:17', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (48, 32, '/api/config', 'config', 'api/configure/index.vue', '配置管理', 0, 1, 'ele-SetUp', 1, 0, 0, '', 4, NULL, 10, '', '2022-04-10 18:25:10', '2023-03-02 16:38:59', 1, 0, 7, 7, NULL, '18c372786f3d48b7966d888517098635');
INSERT INTO `menu` VALUES (49, 32, '/api/apiCase', 'apiCase', 'api/apiCase/index.vue', '测试用例', 0, 0, 'ele-Fold', 1, 0, 0, '', 4, NULL, 10, '', '2022-04-12 10:50:09', '2022-04-12 10:50:09', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (50, 49, '/api/apiCase/edit', 'EditApiCase', 'api/apiCase/EditApiCase', '编辑用例', 0, 1, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-04-12 11:42:09', '2022-04-12 11:42:09', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (51, 28, '/system/lookup', 'systemLookup', 'system/lookup/index.vue', '数据字典', 0, 0, 'ele-Management', 1, 0, 0, '', 3, NULL, 10, '', '2022-05-03 17:11:59', '2022-05-03 17:11:59', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (53, 0, '/tools', 'tools', 'layout/routerView/parent', '工具', 0, 0, '', 1, 0, 0, '', 5, NULL, 10, '', '2022-06-14 21:08:01', '2022-06-14 21:08:00', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (54, 53, '/tools/query_db', 'query_db', 'tools/queryDB/index.vue', '数据查询', 0, 0, '', 1, 0, 0, '', 0, NULL, 10, '', '2022-06-14 21:09:29', '2022-06-14 21:09:28', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (57, 0, 'kjhgf', 'jh', 'uu', 'UI自动化', 1, 1, 'ele-Pear', 1, 0, 0, 'admin', 111, NULL, 10, '', '2022-08-23 11:05:09', '2022-08-23 11:05:08', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (58, 32, '/api/dataSource', 'ApiDataSource', 'api/dataSource/index.vue', '数据源管理', 0, 0, 'ele-Tickets', 1, 0, 0, '', 9, NULL, 10, '', '2022-09-13 14:34:44', '2022-09-13 14:34:43', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (59, 53, '/tools/testcase', 'apiTest', 'api/apiTest/index.vue', '接口测试', 0, 0, '', 0, 0, 0, '', 0, NULL, 10, '', '2022-09-13 16:00:00', '2022-09-13 15:59:59', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (61, 28, '/system/personal', 'personal', 'system/personal/index', '个人中心', 0, 0, 'ele-User', 1, 0, 0, '', 0, NULL, 10, '', '2023-01-16 16:37:40', '2023-01-31 14:42:58', 1, 3, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (62, 53, '/websocket', '连接1', 'tools/websocket/index.vue', '连接1', 0, 0, '', 1, 0, 0, '0', 0, NULL, 10, '', '2023-02-09 12:27:42', '2023-02-09 12:29:52', 1, 0, 7, 7, NULL, NULL);
INSERT INTO `menu` VALUES (63, 0, '/projectOrModule', '/projectOrModule', 'layout/routerView/parent', '项目/模块', 0, 0, 'ele-Files', 1, 0, 1, '0', 2, NULL, 10, '', '2023-02-23 11:07:56', '2023-02-23 15:02:37', 1, 0, NULL, NULL, NULL, NULL);

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
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of roles
-- ----------------------------
INSERT INTO `roles` VALUES (1, '管理员', '管理员', 10, '1,29,30,31,51,61,33,34,35,36,38,41,42,48,50,58,54,59,62', '2021-04-12 16:56:20', '2023-02-23 11:08:43', 1, 7, 7, 10, NULL);
INSERT INTO `roles` VALUES (3, '测试工程师', '测试工程师', 10, '1,57,33,34,38,48,50,42,41,36,35,29,31,30,51,58,54', '2021-05-21 17:24:53', '2022-01-21 10:57:59', 1, 7, 7, 10, NULL);

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
  `exec_user_id` int DEFAULT NULL,
  `exec_user_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE,
  INDEX `name_index`(`name`) USING BTREE,
  INDEX `creation_date_index`(`creation_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
  `avatar` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '头像数据',
  `tags` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `trace_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'trace_id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_user_email`(`email`) USING BTREE,
  INDEX `ix_user_password`(`password`) USING BTREE,
  INDEX `ix_user_username`(`username`) USING BTREE,
  INDEX `id_index`(`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (NULL, NULL, 1, 0, '系统', '', NULL, '1', '系统', 1, NULL, NULL, 10, NULL, NULL, NULL, NULL);
INSERT INTO `user` VALUES ('2022-03-09 16:03:43', '2023-02-23 14:36:44', 1, 7, 'admin', 'o1qooQ2aDAxzq2r7YAxbk7mNHvyDQ0iyFngiSpp6rkBUwzpCqYwyd4hpXKk8x4ZUKKEKUbCIZSS+1lEnHhOH67COnHszbOq/vWdVGHZOXehYv02yj3jO/q7/Moh9KoLWHSpBJN8MfqdxvdmvowfWzeQz2DbD81BlyKXTSwyYeek=', '12546@qq.com', '1', 'admin', 1, 7, 7, 10, '富在术数，不在劳身；利在势居，不在力耕。', 'data:image/jpeg;base64,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', '测试,1111', NULL);

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
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_login_record
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
