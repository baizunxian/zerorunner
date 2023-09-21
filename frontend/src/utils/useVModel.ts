import {computed} from "vue";

export default function useVModel(props: any, propsName: string, emit: any) {
	return computed({
		get() {
			return new Proxy(props[propsName], {
				get(target: any, key: string | symbol): any {
					return Reflect.get(target, key);
				},
				set(target: any, key: string | symbol, value: any, receiver: any): boolean {
					Reflect.set(target, key, value, receiver);
					emit("update:" + propsName, {...target, [key]: value});
					return true;
				}
			})
		},
		set(val) {
			emit("update:" + propsName, val);
		}
	})

}