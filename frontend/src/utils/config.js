export function getEnv() {
	return import.meta.env.ENV
}

export function getApiBaseUrl() {
	return import.meta.env.VITE_API_BASE_URL + import.meta.env.VITE_API_PREFIX || "http://localhost:8080" + import.meta.env.VITE_API_PREFIX
}

export function getWebSocketUrl() {
	return ((window.location.protocol === 'https:') ? 'wss' : 'ws') + '://' + import.meta.env.VITE_WBE_SOCKET_URL
}


export function getBaseApiUrl() {
	return import.meta.env.VITE_API_BASE_URL
}
