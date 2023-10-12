<template>
  <el-dialog
      title="调试"
      v-model="state.showDebugPage"
      width="80%"
      destroy-on-close
      @close="closeDebugPage"
      :close-on-click-modal="false"
  >
    <div>
      <el-form inline size="default" v-model="state.debugForm">
        <el-form-item label="执行机">
          <el-select v-model="state.debugForm.executeNode">
            <el-option label="服务器" value="1"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="浏览器">
          <el-select v-model="state.debugForm.browser">
            <el-option label="Chrome" value="Chrome"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="">
          <el-button type="primary" @click="start">开始</el-button>
          <el-button type="primary">执行到下个断点</el-button>
          <el-button type="primary" @click="clearLog">清除日志</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-row>
      <el-col :span="14">
        <UiStepInfo :step-data-list="stepDataList" useType="debug"></UiStepInfo>
      </el-col>
      <el-col :span="10">
        <z-monaco-editor
            style="height: 400px"
            ref="monacoEditRef"
            :options="{readOnly: true}"
            v-model:value="state.log"
            lang="text"
        ></z-monaco-editor>
      </el-col>
    </el-row>

  </el-dialog>
</template>

<script setup name="EditPage">
import {onDeactivated, reactive} from "vue";
import {ElMessage} from 'element-plus';
import UiStepInfo from "/@/views/ui/uiCase/uiStepInfo.vue";
import {getWebSocketUrl} from "/@/utils/config";

const props = defineProps({
  stepDataList: {
    type: Array,
  }
})


const state = reactive({
  uid: null,
  ws: null,
  wsTime: null,
  showDebugPage: false,
  log: "",
  debugForm: {
    browser: "Chrome",
    executeNode: "1",
  }
});

const onOpenDebugPage = () => {
  state.uid = guid()
  websocket()
  state.showDebugPage = !state.showDebugPage
}
const guid = () => {
  function S4() {
    return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1)
  }

  return (S4() + S4() + S4() + S4() + S4() + S4() + S4() + S4())
}

const websocket = () => {
  if ('WebSocket' in window) {
    let url = `${getWebSocketUrl()}/api/ws/uiCase/debug/${state.uid}`
    let ws = new WebSocket(url)
    state.ws = ws
    ws.onopen = (event) => {
      console.log('已建立连接....')
    };
    ws.onmessage = (event) => {
      console.log('接收信息：', event)
      //将字符串转换成 Blob对象
      let message = JSON.parse(event.data)
      if (message.message_type === "log") {
        state.log += message.data + "\n"
      }
      if (message.message_type === "step_result") {
        state.log += message.step_result.log + "\n"
      }
      if (message.message_type === "err") {
        ElMessage.error(message.data || "调试失败！")
      }

    };
    ws.onerror = (event) => {
      console.log('错误信息：', event)
      reconnect()
    };
    ws.onclose = (event) => {
      console.log('关闭信息：', event)
      reconnect()
    };
  } else {
    console.log('浏览器不支持 WebSocket..')
  }


  const reconnect = () => {
    console.info('尝试重连...')
    if (state.wsTime) {
      window.clearTimeout(state.wsTime)
      state.wsTime = null
    }
    state.wsTime = window.setTimeout(() => {
      websocket()
    }, 5000)

  }
}


const start = () => {
  let data = {
    operation_type: "start",
    data: {
      name: "debug",
      browser: state.debugForm.browser,
      executeNode: state.debugForm.executeNode,
      steps: props.stepDataList
    }
  }
  state.ws?.send(JSON.stringify(data))
}

// 清除日志
const clearLog = () => {
  state.log = ""
}

const onDebug = () => {
  console.log("onDebug")
}

const closeDebugPage = () => {
  state.showDebugPage = false
  state.ws?.close()
  state.ws = null
  state.uid = null
}

defineExpose({
  onOpenDebugPage,
})

onDeactivated(() => {
  state.showDebugPage = false
  state.ws?.close()
  state.ws = null
  state.uid = null
  console.log("退出页面!")
})

</script>

<style scoped lang="scss">
:deep(.el-table .el-table__cell) {
  padding: 8px 0;

}

</style>