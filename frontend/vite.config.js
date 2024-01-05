import vue from '@vitejs/plugin-vue';
import {resolve} from 'path';
import {defineConfig, loadEnv} from 'vite';
import vueSetupExtend from 'vite-plugin-vue-setup-extend';
import monacoEditorPlugin from "vite-plugin-monaco-editor"
import {viteBuildBanner} from "./vite-build-plugin";


import MonacoEditorNlsPlugin, {esbuildPluginMonacoEditorNls, Languages,} from '/@/components/monaco/nls';

const zh_CN = require('/@/components/monaco/nls/zh-hans.json')


const pathResolve = (dir) => {
	return resolve(__dirname, '.', dir);
};

const alias = {
	'/@': pathResolve('./src/'),
};

const viteConfig = defineConfig((mode) => {
	const env = loadEnv(mode.mode, process.cwd());
	return {
		plugins: [
			vue(),
			vueSetupExtend(), monacoEditorPlugin(),
			MonacoEditorNlsPlugin({
				locale: Languages.zh_hans,
				/**
				 * The weight of `localedata` is higher than that of `locale`
				 */
				localeData: zh_CN.contents
			}),
			viteBuildBanner(env),
		],
		optimizeDeps: {
			/** vite >= 2.3.0 */
			include: [
				'vue',
				'vue-router',
				'@vueuse/core',
				'pinia',
				'axios',
				'monaco-editor',
				'element-plus/es',
				'element-plus/es/components/form/style/index',
				'element-plus/es/components/radio-group/style/index',
				'element-plus/es/components/radio/style/index',
				'element-plus/es/components/checkbox/style/index',
				'element-plus/es/components/checkbox-group/style/index',
				'element-plus/es/components/switch/style/index',
				'element-plus/es/components/time-picker/style/index',
				'element-plus/es/components/date-picker/style/index',
				'element-plus/es/components/col/style/index',
				'element-plus/es/components/form-item/style/index',
				'element-plus/es/components/alert/style/index',
				'element-plus/es/components/breadcrumb/style/index',
				'element-plus/es/components/select/style/index',
				'element-plus/es/components/input/style/index',
				'element-plus/es/components/breadcrumb-item/style/index',
				'element-plus/es/components/tag/style/index',
				'element-plus/es/components/pagination/style/index',
				'element-plus/es/components/table/style/index',
				'element-plus/es/components/table-column/style/index',
				'element-plus/es/components/card/style/index',
				'element-plus/es/components/row/style/index',
				'element-plus/es/components/button/style/index',
				'element-plus/es/components/menu/style/index',
				'element-plus/es/components/sub-menu/style/index',
				'element-plus/es/components/menu-item/style/index',
				'element-plus/es/components/option/style/index',
				'@element-plus/icons-vue',
			],
			esbuildOptions: {
				plugins: [
					esbuildPluginMonacoEditorNls({
						locale: Languages.zh_hans,
						/**
						 * The weight of `localedata` is higher than that of `locale`
						 */
						localeData: zh_CN.contents
					}),
				],
			},
		},
		esbuild: {
			drop: ["console", "debugger"],
		},
		root: process.cwd(),
		resolve: {alias},
		base: mode.command === 'serve' ? './' : env.VITE_PUBLIC_PATH,
		server: {
			host: '0.0.0.0',
			port: env.VITE_PORT,
			open: env.VITE_OPEN,
			hmr: true,
			proxy: {
				// '/gitee': {
				// 	target: 'https://gitee.com',
				// 	ws: true,
				// 	changeOrigin: true,
				// 	rewrite: (path) => path.replace(/^\/gitee/, ''),
				// },
			},
		},
		build: {
			outDir: 'dist',
			chunkSizeWarningLimit: 1500,
			rollupOptions: {
				output: {
					entryFileNames: `assets/[name].[hash].js`,
					chunkFileNames: `assets/[name].[hash].js`,
					assetFileNames: `assets/[name].[hash].[ext]`,
					compact: true,
					manualChunks(id) {
						if (id.includes('node_modules')) {
							return id.toString().match(/\/node_modules\/(?!.pnpm)(?<moduleName>[^\/]*)\//).groups.moduleName ?? 'vender';
						}
					},
					// manualChunks: {
					// 	vue: ['vue', 'vue-router', 'pinia'],
					// 	echarts: ['echarts'],
					// },
				},
			},
		},
		css: {
			preprocessorOptions: {css: {charset: false}},
			postcss: {
				plugins: [
					{
						postcssPlugin: 'internal:charset-removal',
						AtRule: {
							charset: (atRule) => {
								if (atRule.name === 'charset') {
									atRule.remove();
								}
							},
						},
					},
				],

			},
		},
		define: {
			__VERSION__: JSON.stringify(process.env.npm_package_version),
		},
	};
});

export default viteConfig;
