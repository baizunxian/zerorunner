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
  }else if (method == "N/A") {
    color = "#f56c6c"
  }
  return color
}

// 获取步骤颜色
/*获取步骤数据，颜色，背景颜色，icon*/
export function getStepTypeInfo(stepType: string, type: string) {
  let obj: any = {
    script: {color: "#7B4D12FF", background: "#F1EEE9FF", icon: 'iconfont icon-code'},
    wait: {color: "#67C23AFF", background: "#F2F9EEFF", icon: 'iconfont icon-time'},
    api: {color: "#61649f", background: "#f5f5fa", icon: 'iconfont icon-apiInfo-o'},
    case: {color: "#61649f", background: "#f5f5fa", icon: 'iconfont icon-apiInfo-o'},
    loop: {color: "#02A7F0FF", background: "#F4F4F5FF", icon: 'iconfont icon-loop'},
    extract: {color: "#015478FF", background: "#E6EEF2FF", icon: ''},
    sql: {color: "#783887FF", background: "#F2ECF3FF", icon: ''},
    if: {color: "#E6A23C", background: "#FCF6EE", icon: 'iconfont icon-fenzhi'},
  }
  return obj[stepType][type]
}

/*步骤类型*/
export const stepTypes: object = {
  extract: "参数提取",
  script: "自定义脚本",
  if: "条件控制器",
  loop: "循环控制器",
  sql: "SQL控制器",
  wait: "等待控制器",
  scene: "场景断言",
  api: "引用接口",
  case: "引用用例",
}

/*字典过滤*/
export function objectFilter(obj: object, field: Array<string>) {
  let res = Object.entries(obj).filter(([key, val]) => field.includes(key))
  return Object.fromEntries(res)
}

/* 根据使用类型获取对应展示的菜单 */
export function getStepTypesByUse(use_type: String) {
  let stepTypeMapping: object
  let stepContain: Array<string>
  switch (use_type) {
    case "pre":
      stepContain = ["script", "sql", "wait"]
      stepTypeMapping = objectFilter(stepTypes, stepContain)
      break
    case "post":
      stepContain = ["script", "sql", "wait"]
      stepTypeMapping = objectFilter(stepTypes, stepContain)
      break
    case "suite":
      stepContain = ["script", "if", "loop", "wait", "api"]
      stepTypeMapping = objectFilter(stepTypes, stepContain)
      break
    default:
      stepTypeMapping = {}
  }
  return stepTypeMapping
}


export const getId = async () => {
  let res = await useIdCenterApi().getId()
  return res.data
}


export function getStatusTag(status: string) {
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


export function formatSizeUnits(bytes: number) {
  let BodySizeStr
  if (bytes >= 1073741824) {
    BodySizeStr = (bytes / 1073741824).toFixed(2) + " GB";
  } else if (bytes >= 1048576) {
    BodySizeStr = (bytes / 1048576).toFixed(2) + " MB";
  } else if (bytes >= 1024) {
    BodySizeStr = (bytes / 1024).toFixed(2) + " KB";
  } else if (bytes > 1) {
    BodySizeStr = bytes + " B";
  } else if (bytes == 1) {
    BodySizeStr = bytes + " B";
  } else {
    BodySizeStr = "0 B";
  }

  return BodySizeStr;

}