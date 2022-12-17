export declare interface ReportData {
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
  step_datas: Array<StepData>
  start_time_iso_format: string
  success: boolean
}

export declare interface InOut {
  config_vars: object
  export_vars: object
}


export declare interface StepData {
  name: string
  case_id: string | number
  duration: string | number
  env_variables: object
  export_vars: object
  message: string
  parent_step_id: string
  post_hook_data: Array<StepData>
  pre_hook_data: Array<StepData>
  session_data: SessionData
  start_time: number
  status: string
  step_data: string
  step_id: string
  step_tag: string
  step_type: string
  success: boolean
  variables: object
}


export declare interface SessionData {
  address: Address
  req_resps: Array<RequestData, ResponseData>
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


export declare interface Address {
  client_ip: number | string
  client_port: number | string
  server_ip: number | string
  server_port: number | string
}


export declare interface RequestData {
  body: object
  cookies: object
  headers: object
  method: string
  url: string
}

export declare interface ResponseData {
  body: object
  cookies: object
  headers: object
  content_type: string
  encoding: string
  status_code: number
}

export declare interface ValidateExtractor {
  validate_extractor: Array<object>
}

export declare interface statData {
  content_size: number
  elapsed_ms: number
  response_time_ms: number
}





