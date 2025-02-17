# Release History

## 1.1.1 (2022-04-26)

**Added**

**Changed**

- httprunner升级 3.1.6 -> 3.1.11
- 支持项目，模块，用例的配置参数

## 1.2.0 (2022-04-28)

**Added**

**Changed**

- 增加无yaml文件运行用例方式（对于测试套件，大量测试用例运行时，节省系统的IO操作优化执速度）
- 修复用例并行运行时，可能导致函数信息覆盖的问题

## 1.2.1 (2022-05-04)

**Added**

**Changed**

- 定时任务功能完善
- 数据字典开发使用
- 部分界面优化

## 1.2.2 (2022-05-18)

**Added**

**Changed**

- 首页统计接口完善
- 兼容V2报告模板


## 1.2.3 (2022-05-24)

**Added**

**Changed**

- 支持原生参数请求
- 页面优化,执行选择原生数据参数


## 1.3.0 (2022-06-02)

**Added**
- 新增postman文件转用例(现在支持,form-data,raw-json,raw-text)

**Changed**
- 用例解析优化
- 前端body页面优化

## 2.0.0 (2023-04-26)

**Added**
- 从后端项目从flask切换到fastApi
- 使用自定义执行引擎，支持多种类型步骤
- 添加celery对async异步函数的支持


## 2.0.0 (2023-04-28)

**Changed**
- 用例页面优化，卡顿问题修复
- 前端body页面优化增加 none 模式请求


## 2.0.1 (2023-05-11)

**Added**
- 增加docker部署配置文件，能实现一键部署 （需要修改对应的配置文件）
- api用例支持前后置code 实现对请求变量等数据的修改

**Changed**
- 其他页面优化

## 2.1.0 (2023-06-27)

**Added**
- 增加ui用例
- 增加ui调试
- 增加ui用例报告
- 增加异步任务执行记录
- 其他页面优化

**Changed**
- **其他页面优化**


## 2.1.2 (2023-10-11)

**Added**
- 增加Api血缘关系 (目前只支持用例关联api的关系，后续会加上 定时任务，用例血缘等)
- 增加接口x-www-form-urlencoded的支持
- 增加json解析工具

**Changed**
- **其他页面优化**

## 2.1.3 (2023-10-19)

**Added**
- 接口环境配置只初始化一次

**Changed**
- **其他页面优化**
- **数据库变更 ddl**
```sql
ALTER TABLE `zerorunner`.`api_test_report` 
ADD COLUMN `error_msg` text NULL AFTER `exec_user_name`;
```

## 2.1.4 (2023-10-21)

**Added**
- 用例结构优化，方便扩展

**Changed**
- **其他页面优化**
- **数据库变更 ddl**
```sql
ALTER TABLE `zerorunner`.`api_test_report_detail_0` 
ADD COLUMN `source_id` bigint NULL AFTER `exec_user_name`;
```

## 2.1.5 (2023-11-01)

**Added**
- 血缘关系完善

**Changed**
- **bugfix**

