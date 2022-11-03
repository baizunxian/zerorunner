import {store} from "/@/store";

/**
 * 返回数据字典
 * @param code 数据字典编码
 * @param lookup_code 数据字典值编码
 * @returns return 对应的字符串，否则返回原值
 */
export function formatLookup(code: string, lookup_code: string): string {
  let lookup: any = store.state.lookup.lookup[code]
  if (!lookup) return lookup_code;
  if (lookup[lookup_code]) return lookup[lookup_code];
  return lookup_code;
}
