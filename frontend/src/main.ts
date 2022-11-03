import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import {key, store} from './store';
import {directive} from '/@/utils/directive';
import other from '/@/utils/other';
import 'element-plus/theme-chalk/dark/css-vars.css'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '/@/theme/index.scss';
import mitt from 'mitt';

const app = createApp(App);

directive(app);
other.elSvg(app);
other.apiPublicAssembly(app)

app.use(router).use(store, key).use(ElementPlus, {size: 'small'}).mount('#app');

app.config.globalProperties.mittBus = mitt();
