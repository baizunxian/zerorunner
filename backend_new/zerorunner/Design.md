# Design

## 0.0.1 (2022-07-28)

**一，引擎执行顺序**

1. Init Env Variables              (初始化环境变量)
2. Init TestCase Public Variables  (初始化用例公共变量)
3. Check If Skip <TestCase>        (校验是否跳过用例)
4. TestCase SetUp Hook             (测试用例执行前钩子函数)
5. Check If Skip <Step>            (校验是否跳过步骤)
6. Parse API Request               (解析请求参数)
7. TestStep Init Variables         (测试步骤执初始化变量)
8. TestStep SetUp Hook             (测试步骤执行前钩子函数)
9. TestStep SetUp Script           (测试步骤执行前执行脚本)
10. Check SSL                      (SSL校验)
11. Send Request                   (发送请求)
12. Request Extract                (提取参数)
13. TestStep TearDown Script       (测试步骤执行后执行脚本)
14. TestStep TearDown Hook         (测试步骤执行后执行脚本)
15. Validate                       (校验)
16. Extract                        (退出)

**二，用例结构设计**

```json 
{
    "base_url": '',
    "variables": {},
    "env_variables": {},
    "skip":false,
    "setp": [
        {
            "skip":false,
            "ssl": false,
            "request":{
                "type":"json",
                "json":{
                    "key":"value"
                    ...
                },
                "url":"wwwww",
                "method":"POST",
                "headers":{
                    "Content-Type":"application/json"
                    ...
                }
            },
            "setup_hooks":[
                {
                    "type":"script",
                    "content":"",
                }
            ],
            "teardown_hooks":[
                {
                    "type":"script",
                    "content":"",
                }
            ],
            "validate":[
                {
                    "check":"body.code",
                    "comparator":"equals",
                    "type":"int",
                    "expected":0
                }
            ],
            "extract":[
                {
                    "test":"body.test",
                    "remarks_":"111111"
                }
            ],
            "variables":[
                {
                    "test":"test1",
                    "remarks_":"111111"
                }
            ],
            "parameters":[
                {
                    "remarks_":"test",
                    "a":[
                        1
                    ]
                }
            ]
        }
    ]
}


```


