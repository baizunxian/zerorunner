<template>
  <div ref="terminalRef"></div>
</template>

<script setup name="webSsh">
import {nextTick, onDeactivated, onMounted, reactive, ref} from "vue"
import {Terminal} from "xterm"
import {FitAddon} from 'xterm-addon-fit'
import 'xterm/css/xterm.css'

const terminalRef = ref()

const props = defineProps({});

const stata = reactive<TerminalState>({
  term: null,
  wsTime: null,
  ws: null,
  command: "",
})

onMounted(() => {
  initTerminal()
  websocket()
})

const initTerminal = () => {
  nextTick(() => {

  })
  stata.term = new Terminal({
    rows: 40, //行数，影响最小高度
    cols: 100, // 列数，影响最小宽度
    convertEol: true, //启用时，光标将设置为下一行的开头
    // scrollback: 50, //终端中的滚动条回滚量
    disableStdin: false, //是否应禁用输入。
    cursorStyle: "underline", //光标样式
    cursorBlink: true, //光标闪烁
    fontWeight: "bold",
    theme: {
      foreground: '#F8F8F8',
      background: '#2D2E2C',
      cursor: "help", //设置光标
    },
    fontFamily: '"PingFang SC, HarmonyOS_Medium, Helvetica Neue, Microsoft YaHei, sans-serif", Menlo, monospace'
  });
}


const writeDefaultInfo = () => {
  let defaultInfo = [
    '┌\x1b[1m zerorunner \x1b[0m─────────────────────────────────────────────────────────────────┐ ',
    '│                                                                             │ ',
    '│  \x1b[1;34m  ✨  欢迎使用 ✨ \x1b[0m                                                           │ ',
    '│                                                                             │ ',
    '└─────────────────────────────────────────────────────────────────────────────┘ ',]
  // 测试颜色区间
  // let arr = Array.from({length:100},(v,i)=>v = i)
  // console.log(arr)
  // arr.map((item,i) => {
  //     defaultInfo.push(`Hello from \x1B[1;3;${i}m ${i} \x1B[0m  \u2764\ufe0f   ${i}`)
  // })
  stata.term.write(defaultInfo.join('\n\r'))
  // stata.term.write('\r\n > ')
}

const websocket = () => {
  if ('WebSocket' in window) {
    let url = `ws://127.0.0.1:8101/api/ws/user1`
    let ws = new WebSocket(url)
    stata.ws = ws
    nextTick(() => {
      userWrite()
    })
    ws.onopen = (event) => {
      console.log('已建立连接stata.term：', stata.term)
      // 输入换行符可让终端显示当前用户的工作路径
      // ws.send('get test')
      // 窗口自适应插件
      let fitAddon = new FitAddon();
      // 窗口尺寸变化时，终端尺寸自适应
      window.onresize = () => {
        fitAddon.fit()
      }
      stata.term.loadAddon(fitAddon)
      stata.term.open(terminalRef.value);
      stata.term.focus()
      // 自定义终端默认展示内容
      writeDefaultInfo()
      writeOfColor(`\n连接成功！`, '0;', '37m')

      // writeOfColor("\r\n > ")
      stata.term.write("\r\n > ")
    };
    ws.onmessage = (event) => {
      console.log('接收信息：', event)
      //将字符串转换成 Blob对象
      const blob = new Blob([event.data], {
        type: 'text/plain'
      });
      //将Blob 对象转换成字符串
      const reader = new FileReader();
      reader.readAsText(blob, 'utf-8');
      reader.onload = (e) => {
        // 可以根据返回值判断使用何种颜色或者字体，不过返回值自带了一些字体颜色
        writeOfColor(`${reader.result}`, '0;', '37m')
        stata.term.write("\r\n > ")
      }

    };
    ws.onerror = (event) => {
      console.log('错误信息：', event)
      reconnect()
    };
    ws.onclose = (event) => {
      writeOfColor(`\r\n连接已断开 ❗`, '0;', '37m')
      reconnect()

    };
  } else {
    console.log('浏览器不支持 WebSocket..')
  }


  const reconnect = () => {
    console.info('尝试重连...')
    stata.term.write("\r\n尝试重连...")
    if (stata.wsTime) {
      window.clearTimeout(stata.wsTime)
      stata.wsTime = null
    }
    stata.wsTime = window.setTimeout(() => {
      initTerminal()
      websocket()
    }, 5000)

  }
}

const userWrite = () => {
  stata.term.onData((e) => {
    console.log("e", JSON.stringify(e))
    switch (e) {
      case '\u0003': // Ctrl+C
        stata.term.write('^C ');
        stata.term.write('\r\n > ')
          console.log(stata.term.getSelection(), "getSelection")
        break;
      case '\r': // Enter
        stata.ws.send(stata.command)
        // stata.ws.send('\n')
        stata.command = ''
        stata.term.write('\r\n')
        break;
      case '\u007F': // Backspace (DEL)
        // Do not delete the prompt
        if (stata.term._core.buffer.x > 2) {
          stata.term.write('\b \b');
          if (stata.command.length > 0) {
            stata.command = stata.command.substr(0, stata.command.length - 1);
          }
        }
        break;
      default: // Print all other characters for demo
        if (e >= String.fromCharCode(0x20) && e <= String.fromCharCode(0x7E) || e >= '\u00a0') {
          stata.command += e;
          writeOfColor(e, '0', '33m')
          console.log('用户输入command', stata.command)
        }
    }
  });
}

const writeOfColor = (txt, fontCss = "", bgColor = "") => {
  // 在Linux脚本中以 \x1B[ 开始，中间前部分是样式+内容，以 \x1B[0m 结尾
  // 示例 \x1B[1;3;31m 内容 \x1B[0m
  // fontCss
  // 0;-4;字体样式（0;正常 1;加粗 2;变细 3;斜体 4;下划线）
  // bgColor
  // 30m-37m字体颜色（30m:黑色 31m:红色 32m:绿色 33m:棕色字 34m:蓝色 35m:洋红色/紫色 36m:蓝绿色/浅蓝色 37m:白色）
  // 40m-47m背景颜色（40m:黑色 41m:红色 42m:绿色 43m:棕色字 44m:蓝色 45m:洋红色/紫色 46m:蓝绿色/浅蓝色 47m:白色）
  stata.term.write(`\x1B[${fontCss}${bgColor}${txt}\x1B[0m`)
}

onDeactivated(() => {
  // toRaw(stata.term)?.dispose()
  stata.ws?.close()
  stata.ws = null
  console.log("退出页面!")
})

</script>
