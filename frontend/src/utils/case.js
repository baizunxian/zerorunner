// 获取请求方式tag颜色
import {useIdCenterApi} from "/@/api/useSystemApi/idCenter";

export function getMethodColor(method) {
	let color = ""
	if (method === "GET") {
		color = "#61affe"
	} else if (method === "POST") {
		color = "#49cc90"
	} else if (method === "DELETE") {
		color = "#f93e3d"
	} else if (method === "PUT") {
		color = "#fca130"
	} else if (method === "N/A") {
		color = "#f56c6c"
	}
	return color
}

// 获取步骤颜色
/*获取步骤数据，颜色，背景颜色，icon*/
export function getStepTypeInfo(stepType, type) {
	let obj = {
		script: {color: "#7B4D12FF", background: "#F1EEE9FF", icon: 'iconfont icon-code'},
		wait: {color: "#67C23AFF", background: "#F2F9EEFF", icon: 'iconfont icon-time'},
		api: {color: "#61649f", background: "#f5f5fa", icon: 'iconfont icon-c158API'},
		case: {color: "#f4664a", background: "#f5f5faFF", icon: 'iconfont icon-a-case-o1'},
		loop: {color: "#02A7F0FF", background: "#F4F4F5FF", icon: 'iconfont icon-loop'},
		extract: {color: "#015478FF", background: "#E6EEF2FF", icon: ''},
		sql: {color: "#783887FF", background: "#F2ECF3FF", icon: 'iconfont icon-suffix-sql'},
		if: {color: "#E6A23C", background: "#FCF6EE", icon: 'iconfont icon-fenzhijiedian'},
		timed_task: {color: "#AE445A", background: "#AE445A", icon: 'iconfont icon-time'},
	}
	return obj[stepType][type]
}

export const baseModeType = [
	{key: "jmespath", value: "jmespath"},
	{key: "JsonPath", value: "JsonPath"},
	{key: "变量&函数", value: "variable_or_func"},
]

export function getModeTypeObj(modeType) {
	return baseModeType
	// if (modeType === 'extract') {
	// 	//  提取的
	// 	return baseModeType
	// }
	// if (modeType === 'validator') {
	// 	//  断言
	// 	let validModeTypes = [
	// 		{key: "变量&函数", value: "variable_or_func"},
	// 	]
	// 	return [...baseModeType, ...validModeTypes]
	// }
	// return []
}

export function getComparators(useType) {
	return {
		equals: "等于",
		not_equal: "不等",
		length_equals: "长度等于",
		contains: "包含",
		startswith: "以...开始",
		endswith: "以...结束",
		// regex_match: "正则",
		// type_match: "类型等于",
		less_than: "小于",
		less_than_or_equals: "小于或者等于",
		greater_than: "大于或等于",
		greater_than_or_equals: "大于或等于",
	}
}


export const getPlaceholder = (modeType) => {
	if (modeType === 'jmespath') {
		return "jmespath表达式 例如：body.code"
	}
	if (modeType === 'JsonPath') {
		return "JsonPath表达式  列如：$.data.rows[0].id"
	}
	if (modeType === 'variable_or_func') {
		return "变量或者函数 例如${test} ${函数名()}"
	}
	return ""
}

/*步骤类型*/
export const stepTypes = {
	api: "引用接口",
	if: "条件控制器",
	loop: "循环控制器",
	extract: "参数提取",
	script: "自定义脚本",
	sql: "SQL控制器",
	wait: "等待控制器",
	scene: "场景断言",
	case: "引用用例",
}

/*字典过滤*/
export function objectFilter(obj, field) {
	let res = Object.entries(obj).filter(([key, val]) => field.includes(key))
	return Object.fromEntries(res)
}

/* 根据使用类型获取对应展示的菜单 */
export function getStepTypesByUse(use_type) {
	let stepTypeMapping
	let stepContain
	switch (use_type) {
		case "hook":
			stepContain = ["sql", "wait"]
			stepTypeMapping = objectFilter(stepTypes, stepContain)
			break
		case "case":
			stepContain = ["api", "if", "loop", "wait", "script", "sql"]
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


export function getStatusTag(status) {
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


export function formatSizeUnits(bytes) {
	let BodySizeStr
	if (bytes >= 1073741824) {
		BodySizeStr = (bytes / 1073741824).toFixed(2) + " GB";
	} else if (bytes >= 1048576) {
		BodySizeStr = (bytes / 1048576).toFixed(2) + " MB";
	} else if (bytes >= 1024) {
		BodySizeStr = (bytes / 1024).toFixed(2) + " KB";
	} else if (bytes > 1) {
		BodySizeStr = bytes + " B";
	} else if (bytes === 1) {
		BodySizeStr = bytes + " B";
	} else {
		BodySizeStr = "0 B";
	}

	return BodySizeStr;

}