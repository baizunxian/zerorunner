import {computed} from "vue";

export default function useVModel(props, propsName, emit) {
	return computed({
		get() {
			return new Proxy(props[propsName], {
				get(target, key) {
					return Reflect.get(target, key);
				},
				set(target, key, value, receiver) {
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