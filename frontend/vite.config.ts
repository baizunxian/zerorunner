import vue from '@vitejs/plugin-vue';
import {resolve} from 'path';
import {defineConfig, loadEnv, ConfigEnv} from 'vite';
import vueSetupExtend from 'vite-plugin-vue-setup-extend';
import monacoEditorPlugin from "vite-plugin-monaco-editor"

// import MonacoEditorNlsPlugin, {esbuildPluginMonacoEditorNls, Languages,} from '/@/components/monaco/nls';

const zh_CN = require('/@/components/monaco/nls/zh-hans.json')


const pathResolve = (dir: string) => {
  return resolve(__dirname, '.', dir);
};

const alias: Record<string, string> = {
  '/@': pathResolve('./src/'),
};

const viteConfig = defineConfig((mode: ConfigEnv) => {
  const env = loadEnv(mode.mode, process.cwd());
  return {
    plugins: [
      vue(),
      vueSetupExtend(), monacoEditorPlugin(),
      // MonacoEditorNlsPlugin({
      //   locale: Languages.zh_hans,
      //   /**
      //    * The weight of `localedata` is higher than that of `locale`
      //    */
      //   localeData: zh_CN.contents
      // })
    ],
    optimizeDeps: {
      /** vite >= 2.3.0 */
      esbuildOptions: {
        plugins: [
          // esbuildPluginMonacoEditorNls({
          //   locale: Languages.zh_hans,
          //   /**
          //    * The weight of `localedata` is higher than that of `locale`
          //    */
          //   localeData: zh_CN.contents
          // }),
        ],
      },
    },
    root: process.cwd(),
    resolve: {alias},
    base: mode.command === 'serve' ? './' : env.VITE_PUBLIC_PATH,
    server: {
      host: '0.0.0.0',
      port: env.VITE_PORT as unknown as number,
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
          manualChunks: {
            vue: ['vue', 'vue-router', 'pinia'],
            echarts: ['echarts'],
          },
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
