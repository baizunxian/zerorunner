import vue from '@vitejs/plugin-vue';
import {resolve} from 'path';
import {defineConfig, loadEnv, ConfigEnv} from 'vite';
import monacoEditorPlugin from "vite-plugin-monaco-editor"

const pathResolve = (dir: string): any => {
  return resolve(__dirname, '.', dir);
};
import MonacoEditorNlsPlugin, {esbuildPluginMonacoEditorNls, Languages,} from '/@/components/monaco/nls';

const zh_CN = require('/@/components/monaco/nls/zh-hans.json')

const alias: Record<string, string> = {
  '/@': pathResolve('./src/'),
};

const viteConfig = defineConfig((mode: ConfigEnv) => {
  const env = loadEnv(mode.mode, process.cwd());
  return {
    plugins: [
      vue(),
      monacoEditorPlugin(),
      MonacoEditorNlsPlugin({
        locale: Languages.zh_hans,
        /**
         * The weight of `localedata` is higher than that of `locale`
         */
        localeData: zh_CN.contents
      })
    ],
    optimizeDeps: {
      /** vite >= 2.3.0 */
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
    root: process.cwd(),
    resolve: {alias},
    base: mode.command === 'serve' ? '/' : env.VITE_PUBLIC_PATH,
    server: {
      host: '0.0.0.0',
      port: env.VITE_PORT as unknown as number,
      open: env.VITE_OPEN,
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
      sourcemap: false,
      chunkSizeWarningLimit: 1500,
      rollupOptions: {
        output: {
          entryFileNames: `assets/[name].${new Date().getTime()}.js`,
          chunkFileNames: `assets/[name].${new Date().getTime()}.js`,
          assetFileNames: `assets/[name].${new Date().getTime()}.[ext]`,
          compact: true,
          manualChunks: {
            vue: ['vue', 'vue-router', 'vuex'],
            echarts: ['echarts'],
          },
        },
      },
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true,
        },
        ie8: true,
        output: {
          comments: true,
        },
      },
    },
    css: {
      preprocessorOptions: {
        // less: {
        //   charset: false,
        //   additionalData: '@import "./src/components/fabButton/style/vars.less";',
        // },
      },
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
  };
});

export default viteConfig;
