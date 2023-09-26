declare interface TStepDataStat {
	id: string | number | null
	name: string
	case_id: string | number | null
	enable: boolean
	index: number
	step_type: string
	variables: Array<T>
	setup_hooks: Array<TStepDataStat>
	teardown_hooks: Array<TStepDataStat>
	extracts: Array<ExtractData>
	export: Array<T>
	validators: Array<ValidatorData>
	request: TRequestData | TApiData | null
	sql_request: TSqlRequest | null
	loop_request: TStepLoopData | null
	if_request: TStepIFData | null
	wait_request: TStepWaitData | null
	script_request: TStepScriptData | null
	ui_request: TUiRequestData | null
	// 其他字段
	showDetail: boolean | null
}

declare interface ExtractData {
	name: string
	path: string
	continue_extract: boolean
	continue_index: number
	extract_type: string
}


declare interface ValidatorData {
	mode: string
	check: string
	comparator: string
	expect: string
	continue_extract: boolean
	continue_index: number | any
}

declare interface ApiBodyFileDataSchema {
	key: string
	value: string | ApiBodyFileValueSchema
	type: string
}

declare interface ApiBodyFileValueSchema {
	id: string
	name: string
}


declare interface TRequestData {
	method: string
	url: string
	params: object
	headers: object
	json: string
	cookies: object
	timeout: number
	allow_redirects: boolean
	verify: boolean
	upload: object
	mode: string
	data: string | Array<ApiBodyFileDataSchema>
	language: string
}

declare interface TApiData {
	name: string
	api_id: string | number
}

declare interface TSqlRequest {
	env_id: number | null
	source_id: string | number | null
	sql: string
	timeout: number
	variable_name: string
}

declare interface TStepLoopData {
	// loop_type = count
	loop_type: string
	count_number: number
	count_sleep_time: number

	// loop_type == "for"
	for_variable_name: string
	for_variable: string
	for_sleep_time: number

	// loop_type == "while"
	while_comparator: string
	while_variable: string
	while_value: string
	while_sleep_time: number
	while_timeout: number
}

declare interface TStepIFData {
	check: string
	comparator: string
	expect: string
	remarks: string
}

declare interface TStepWaitData {
	wait_time: number
}

declare interface TStepScriptData {
	script_content: string
}

declare interface TUiRequestData {
	action: string
	data: string
	location_method: string
	location_value: string
	cookie: string
	output: string
	enable: boolean
	breakpoint: boolean
}


