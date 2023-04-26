/*
 Navicat Premium Data Transfer

 Source Server         : 42.192.38.108-tx
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : 42.192.38.108:3306
 Source Schema         : zerorunner

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 26/04/2023 14:30:34
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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 190 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
-- Table structure for celery_solar_schedule
-- ----------------------------
DROP TABLE IF EXISTS `celery_solar_schedule`;
CREATE TABLE `celery_solar_schedule`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `event` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `latitude` float NULL DEFAULT NULL,
  `longitude` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 43 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 64 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

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
) ENGINE = InnoDB AUTO_INCREMENT = 596 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 13126515 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
