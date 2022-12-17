import Driver from "driver.js"
import "driver.js/dist/driver.min.css";


const showDriver = () => {
  // 页面提示引导
  let el = document.querySelector("#header-run-env")
  if (el) {
    const steps: Driver.Step[] = [
      {
        element: el, //获取元素节点
        popover: {
          title: "环境",
          description: "请选择运行环境",
          position: "bottom-center", //提示框的位置
        },
      }
    ];
    const driver = new Driver({ //初始化引导页
      doneBtnText: "知道了", // 结束按钮的文字
      allowClose: false, // 是否可以通过点击遮罩层关闭指引
      stageBackground: "#fff", // 突出显示元素的背景颜色
      nextBtnText: "下一步", // 下一步按钮的文字
      prevBtnText: "上一步", // 上一步按钮的文字
      closeBtnText: "关闭", // 关闭按钮的文字
      keyboardControl: true, // 是否允许键盘操控
      showButtons: true, // 是否允许键盘操控
      // xCloseButton: true, // 将关闭按钮作为X放在弹出
    });
    driver.defineSteps(steps);
    driver.start();

  }


}


export default showDriver