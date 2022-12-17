// 获取请求方式tag颜色
import {useIdCenterApi} from "/@/api/useSystemApi/idCenter";

export function getMethodColor(method: string) {
  let color = ""
  if (method == "GET") {
    color = "#61affe"
  } else if (method == "POST") {
    color = "#49cc90"
  } else if (method == "DELETE") {
    color = "#f93e3d"
  } else if (method == "PUT") {
    color = "#fca130"
  }
  return color
}

// 获取步骤颜色
/*获取步骤数据，颜色，背景颜色，icon*/
export function getStepTypeInfo(stepType: string, type: string) {
  let obj: any = {
    script: {color: "#7B4D12FF", background: "#F1EEE9FF", icon: 'iconfont icon-code'},
    wait: {color: "#67C23AFF", background: "#F2F9EEFF", icon: 'iconfont icon-time'},
    case: {color: "#61649f", background: "#f5f5fa", icon: 'iconfont icon-case-o'},
    loop: {color: "#02A7F0FF", background: "#F4F4F5FF", icon: 'iconfont icon-loop'},
    extract: {color: "#015478FF", background: "#E6EEF2FF", icon: ''},
    sql: {color: "#783887FF", background: "#F2ECF3FF", icon: ''},
    if: {color: "#E6A23C", background: "#FCF6EE", icon: 'iconfont icon-fenzhi'},
  }
  return obj[stepType][type]
}

/*步骤类型*/
export const stepTypes = {
  extract: "参数提取",
  script: "自定义脚本",
  condition: "条件控制器",
  loop: "循环控制器",
  sql: "SQL控制器",
  wait: "等待控制器",
  scene: "场景断言",
  case: "用例引用",
}

/* 根据使用类型获取对应展示的菜单 */
export function getStepTypesByUse(use_type: String) {
  let stepTypes: any
  switch (use_type) {
    case "pre":
      stepTypes = {
        script: "前置脚本",
        sql: "前置SQL",
        wait: "等待控制器",
        // case: "引用用例",
      }
      break
    case "post":
      stepTypes = {
        script: "后置脚本",
        sql: "后置SQL",
        wait: "等待控制器",
        // extract: "提取参数",
      }
      break
    case "suite":
      stepTypes = {
        script: "自定义脚本",
        if: "条件控制器",
        loop: "循环控制器",
        // sql: "SQL控制器",
        wait: "等待控制器",
        // scene: "场景断言",
        case: "引用用例",
      }
      break
  }
  return stepTypes
}


export const getId = async () => {
  let res = await useIdCenterApi().getId()
  return res.data
}


export function getStatusTag(status:string) {
  switch (status) {
    case "FAILURE":
      return "warning"
    case "SUCCESS":
      return "success"
    case "ERROR":
      return "danger"
    case "SKIP":
      return "info"
  }
}
