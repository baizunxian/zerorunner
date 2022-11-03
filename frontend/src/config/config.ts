//自动化平台后端域名

let url = null
let webSocketUri = null

export const getEnv = () => {
  if (window.location.href.includes('xiaobaicodes.com') || window.location.href.includes('42.192.38.108')) return 'prd'     //prd
  return 'dev'                                                 //本地环境
}

const env = getEnv()

export const initConfig = () => {
  if (env === 'prd') {
    url = 'https://xiaobaicodes.com:8888'
  } else {
    url = 'http://127.0.0.1:8012'
  }
}

initConfig()

//自动化平台后端接口
export const BaseUrl = url + '/api'
const WebSocketUrl = ((window.location.protocol === 'https:') ? 'wss' : 'wss') + '://' + webSocketUri + '/ws/message'
export default {
  BaseUrl,
  env,
  WebSocketUrl,
}