declare interface ReportData {
  actual_run_count: string
  case_id: string | number
  duration: string | number
  in_out: InOut
  log: string
  message: string
  name: string
  run_count: number
  run_err_count: number
  run_fail_count: number
  run_skip_count: number
  run_success_count: number
  start_time: number
  step_results: Array<StepResult>
  start_time_iso_format: string
  success: boolean
}

declare interface InOut {
  config_vars: object
  export_vars: object
}


declare interface StepResult {
  name: string
  case_id: string | number
  duration: number
  case_variables: object
  export_vars: object
  message: string
  parent_step_id: string
  post_hook_data: Array<StepResult>
  pre_hook_data: Array<StepResult>
  setup_hook_results: Array<StepResult>
  teardown_hook_results: Array<StepResult>
  session_data: SessionData
  start_time: number
  status: string
  step_result: Array<StepResult>
  step_id: string
  step_tag: string
  step_type: string
  success: boolean
  variables: object
  env_variables: object
  log:string
}


declare interface SessionData {
  address: Address
  req_resp: ReqResps
  stat: statData
  success: boolean
  validators: ValidateExtractor
  start_time: number
  status: string
  step_data: string
  step_id: string
  step_tag: string
  step_type: string
  variables: object

}

declare interface ReqResp {
  request: RequestData,
  response: ResponseData
}


declare interface Address {
  client_ip: number | string
  client_port: number | string
  server_ip: number | string
  server_port: number | string
}


declare interface RequestData {
  body: object
  cookies: object
  headers: object
  method: string
  url: string
}

declare interface ResponseData {
  body: object
  cookies: object
  headers: object
  content_type: string
  encoding: string
  status_code: number
}

declare interface ValidateExtractor {
  validate_extractor: Array<ValidateExtractorData>
}

declare interface ValidateExtractorData {
  check: string
  expect_value: string
  check_value: string
  check_result: string
}

declare interface statData {
  content_size: number
  elapsed_ms: number
  response_time_ms: number
}
