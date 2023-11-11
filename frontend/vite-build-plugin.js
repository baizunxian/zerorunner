import {bold} from "picocolors";

export function viteBuildBanner(env) {
	return {
		name: 'vite:buildInfo',
		buildStart() {
			console.info(bold(env.VITE_BANNER))
		}
	}
}
