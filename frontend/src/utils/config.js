export function getEnv() {
	return import.meta.env.ENV
}


export function getWebSocketUrl() {
	return ((window.location.protocol === 'https:') ? 'wss' : 'ws') + '://' + import.meta.env.VITE_WBE_SOCKET_URL
}


export function getBaseApiUrl() {
	return import.meta.env.VITE_API_BASE_URL
}