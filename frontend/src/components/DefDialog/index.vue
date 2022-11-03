<template>
  <VAceEditor
    v-model:value="content"
    lang="json"
    theme="chrome"
    style="height: 100%"
    :options="{ useWorker: true }"
  />
</template>

<script setup data-model-name="app">
import { VAceEditor } from 'vue3-ace-editor';
import 'ace-builds/src-noconflict/mode-json';
import 'ace-builds/src-noconflict/theme-chrome';
import ace from 'ace-builds';
import workerJsonUrl from 'ace-builds/src-noconflict/worker-json?url';
ace.config.setModuleUrl('ace/mode/json_worker', workerJsonUrl);

const content = {kay: 'value'}


</script>


<style>
/*html, body, #app {*/
/*  height: 100%;*/
/*  margin: 0;*/
/*}*/
/*#app {*/
/*  font-family: system-ui;*/
/*  -webkit-font-smoothing: antialiased;*/
/*  -moz-osx-font-smoothing: grayscale;*/
/*}*/
</style>
