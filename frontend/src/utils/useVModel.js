import {computed} from "vue";

export default function useVModel(props, propsName, emit) {
	const event = `update:${propsName.toString()}`
	return computed({
		get() {
			return props[propsName]
			// return new Proxy(props[propsName], {
			// 	get(target, key) {
			// 		return Reflect.get(target, key);
			// 	},
			// 	set(target, key, value, receiver) {
			// 		console.log("receiver", receiver)
			// 		console.log("target", target)
			// 		console.log("target", typeof target)
			// 		Reflect.set(target, key, value);
			// 		console.log("key", key)
			// 		console.log("value", value)
			// 		console.log("value", value)
			// 		emit(event, {...target, [key]: value});
			// 		return true;
			// 	}
			// })
		},
		set(val) {
			emit("update:" + propsName, val);
		}
	})

}