// 通用函数
import useClipboard from 'vue-clipboard3';
import {ElMessage} from 'element-plus';
import {formatDate} from '/@/utils/formatTime';

export default function () {
  const {toClipboard} = useClipboard();
  //百分比格式化
  const percentFormat = (row: any, column: number, cellValue: any) => {
    return cellValue ? `${cellValue}%` : '-';
  };
  //列表日期时间格式化
  const dateFormatYMD = (row: any, column: number, cellValue: any) => {
    if (!cellValue) return '-';
    return formatDate(new Date(cellValue), 'YYYY-mm-dd');
  };
  //列表日期时间格式化
  const dateFormatYMDHMS = (row: any, column: number, cellValue: any) => {
    if (!cellValue) return '-';
    return formatDate(new Date(cellValue), 'YYYY-mm-dd HH:MM:SS');
  };
  //列表日期时间格式化
  const dateFormatHMS = (row: any, column: number, cellValue: any) => {
    if (!cellValue) return '-';
    let time = 0;
    if (typeof row === 'number') time = row;
    if (typeof cellValue === 'number') time = cellValue;
    return formatDate(new Date(time * 1000), 'HH:MM:SS');
  };
  // 小数格式化
  const scaleFormat = (value: any = 0, scale: number = 4) => {
    return Number.parseFloat(value).toFixed(scale);
  };
  // 小数格式化
  const scale2Format = (value: any = 0) => {
    return Number.parseFloat(value).toFixed(2);
  };
  // 点击复制文本
  const copyText = (text: string) => {
    return new Promise((resolve, reject) => {
      try {
        //复制
        toClipboard(text);
        //下面可以设置复制成功的提示框等操作
        ElMessage.success('复制成功 😃');
        resolve(text);
      } catch (e) {
        //复制失败
        ElMessage.error('复制失败 😅');
        reject(e);
      }
    });
  };
  return {
    percentFormat,
    dateFormatYMD,
    dateFormatYMDHMS,
    dateFormatHMS,
    scaleFormat,
    scale2Format,
    copyText,
  };
}
