<template>
  <div :class="['json-view-container',theme,`deep-${currentDeep}`]" v-if="state.visible">
    <div :class="['json-view', length ? 'closeable' : '']"
         :style="{fontSize:fontSize+'px',lineHeight:lineHeight+'px'}">
      <!--icon-style-square-->
      <span @click="toggleClose" class="angle" v-if="length && iconStyle==='square'">
                <svg v-if="state.innerclosed" :fill="iconColors[0]" width="1em" height="1em" viewBox="0 0 1792 1792"
                     style="vertical-align: middle; color: rgb(42, 161, 152); height: 1em; width: 1em;">
                    <path
                        d="M1344 800v64q0 14-9 23t-23 9h-352v352q0 14-9 23t-23 9h-64q-14 0-23-9t-9-23v-352h-352q-14 0-23-9t-9-23v-64q0-14 9-23t23-9h352v-352q0-14 9-23t23-9h64q14 0 23 9t9 23v352h352q14 0 23 9t9 23zm128 448v-832q0-66-47-113t-113-47h-832q-66 0-113 47t-47 113v832q0 66 47 113t113 47h832q66 0 113-47t47-113zm128-832v832q0 119-84.5 203.5t-203.5 84.5h-832q-119 0-203.5-84.5t-84.5-203.5v-832q0-119 84.5-203.5t203.5-84.5h832q119 0 203.5 84.5t84.5 203.5z">
                    </path>
                </svg>
                <svg v-if="!state.innerclosed" :fill="iconColors[1]" width="1em" height="1em" viewBox="0 0 1792 1792"
                     style="vertical-align: middle; color: rgb(88, 110, 117); height: 1em; width: 1em;">
                    <path
                        d="M1344 800v64q0 14-9 23t-23 9h-832q-14 0-23-9t-9-23v-64q0-14 9-23t23-9h832q14 0 23 9t9 23zm128 448v-832q0-66-47-113t-113-47h-832q-66 0-113 47t-47 113v832q0 66 47 113t113 47h832q66 0 113-47t47-113zm128-832v832q0 119-84.5 203.5t-203.5 84.5h-832q-119 0-203.5-84.5t-84.5-203.5v-832q0-119 84.5-203.5t203.5-84.5h832q119 0 203.5 84.5t84.5 203.5z">
                    </path>
                </svg>
            </span>
      <!--icon-style-circle-->
      <span @click="toggleClose" class="angle" v-if="length&& iconStyle==='circle'">
                <svg v-if="!state.innerclosed" viewBox="0 0 24 24" :fill="iconColors[0]"
                     preserveAspectRatio="xMidYMid meet"
                     style="vertical-align: middle; color: rgb(1, 160, 228); height: 1em; width: 1em;">
                    <path
                        d="M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M7,13H17V11H7"></path>
                </svg>
                <svg v-if="state.innerclosed" viewBox="0 0 24 24" :fill="iconColors[1]"
                     preserveAspectRatio="xMidYMid meet"
                     style="vertical-align: middle; color: rgb(161, 106, 148); height: 1em; width: 1em;">
                    <path
                        d="M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M13,7H11V11H7V13H11V17H13V13H17V11H13V7Z"></path>
                </svg>
            </span>
      <!--icon-style-triangle-->
      <span @click="toggleClose" class="angle" v-if="length&& iconStyle==='triangle'">
                <svg
                    v-if="!state.innerclosed"
                    viewBox="0 0 15 15"
                    :fill="iconColors[0]"
                    style="vertical-align: top; color: #3c4047; height: 1em; width: 1em; padding-left: 2px;">
                    <path d="M0 5l6 6 6-6z"></path>
                </svg>
                <svg v-if="state.innerclosed" viewBox="0 0 15 15" :fill="iconColors[1]"
                     style="vertical-align: top; color: #3c4047; height: 1em; width: 1em; padding-left: 2px;">
                    <path d="M0 14l6-6-6-6z"></path>
                </svg>
            </span>
      <div class="content-wrap">
        <p :class="['first-line',length>0?'pointer':'']" @click="toggleClose">
          <span v-if="jsonKey" class="json-key">"{{ jsonKey }}": </span>
          <span v-if="length">{{ prefix }}{{ state.innerclosed ? ('...' + subfix) : '' }}
                        <span class="json-note">{{ state.innerclosed ? (length + ' items') : '' }}</span>
                    </span>
          <span v-if="!length">{{ `${isArray ? '[]' : '{}'}${isLast ? '' : ','}` }}</span>
        </p>
        <div v-if="!state.innerclosed && length" class="json-body">
          <template v-for="(item, index) in items" :key="index">
            <JsonViews
                v-if="item.isJSON"
                :closed="isClose()"
                :key="index"
                :data="item.value"
                :jsonKey="item.key"
                :currentDeep="state.templateDeep+1"
                :deep="deep"
                :iconStyle="iconStyle"
                :theme="theme"
                :fontSize="fontSize"
                :lineHeight="lineHeight"
                :iconColor="iconColors"
                :isLast="index === items.length - 1"
                :hasSiblings="item.hasSiblings"
            />
            <p class="json-item" v-else>
              <span class="json-key">{{ (isArray ? '' : '"' + item.key + '":') }}</span>
              <span :class="['json-value',getDataType(item.value)]">
                                {{
                  `${getDataType(item.value) === 'string' ? '"' : ''}${formatValue(item.value)}${getDataType(item.value) === 'string' ? '"' : ''}${index === items.length - 1 ? '' : ','}`
                }}
                            </span>
            </p>
          </template>
          <span v-if="!state.innerclosed" class="base-line"></span>
        </div>
        <p v-if="!state.innerclosed " class="last-line">
          <span>{{ subfix }}</span>
        </p>
      </div>
    </div>

  </div>
</template>

<script setup name="JsonViews">
import {computed, onMounted, reactive, watch} from 'vue';

const props = defineProps({
  data: { // 传入的json数据
    type: Object || Array || null || undefined,
    default: () => {
    },
  },
  jsonKey: { // json的key值，用于第二层及二层以上的组件的key值
    type: String,
    default: ''
  },
  closed: { // 是否折叠
    type: Boolean,
    default: false
  },
  isLast: { //是否是最后一行
    type: Boolean,
    default: true
  },
  fontSize: { //字体大小
    type: Number,
    default: 14
  },
  lineHeight: { //行高
    type: Number,
    default: 24
  },
  deep: { // 展开深度
    type: Number,
    default: 3
  },
  currentDeep: { // 当前为递归的第几层
    type: Number,
    default: 1
  },
  iconStyle: { // 折叠icon样式
    type: String,
    default: 'square'
  },
  iconColor: { //icon颜色
    type: Array,
    default() {
      return []
    }
  },
  theme: { // 主题
    type: String,
    default: ''
  },
  hasSiblings: { // 是否有兄弟节点
    type: Boolean,
    default: true
  }
})


const state = reactive({
  innerclosed: props.closed,
  templateDeep: props.currentDeep,
  visible: false,
});

const isArray = computed(() => {
  return getDataType(props.data) === 'array'
})

const length = computed(() => {
  try {
    return isArray.value ? props.data.length : Object.keys(props.data).length
  } catch (e) {
    return 0
  }
})

const subfix = computed(() => {
  const data = props.data
  if (isEmptyArrayOrObject(data)) { // 如果是空数组或空对象
    return ''
  } else {
    return (isArray.value ? ']' : '}') + (props.isLast ? '' : ',')
  }
})

const prefix = computed(() => {
  return isArray.value ? '[' : '{'
})

const items = computed(() => {
  const json = props.data
  if (isArray.value) {
    return json.map((item) => {
      const isJSON = isObjectOrArray(item)
      return {
        value: item,
        isJSON,
        key: ''
      }
    })
  }
  return Object.keys(json).map(key => {
    const item = json[key]
    const isJSON = isObjectOrArray(item)
    return {
      value: item,
      isJSON,
      key
    }
  })
})

const iconColors = computed(() => {
  const {theme, iconColor} = props
  if (iconColor.length === 2) {
    return iconColor
  } else {
    if (theme === 'one-dark') {
      return ['#747983', '#747983']
    } else if (theme === 'vs-code') {
      return ['#c6c6c6', '#c6c6c6']
    } else {
      return ['#747983', '#747983']
    }
  }
})

const formatValue = (data) => {
  if (data && data._isBigNumber) {
    return data.toString(10)
  }
  return data;
}

const getDataType = (data) => {
  return data && data._isBigNumber ? 'number' : Object.prototype.toString.call(data).slice(8, -1).toLowerCase()
}

const isObjectOrArray = (source) => {
  return ['array', 'object'].includes(getDataType(source))
}

const toggleClose = () => {
  if (length.value === 0) {
    return
  }
  if (state.innerclosed) {
    state.innerclosed = false
  } else {
    state.innerclosed = true
  }
}

const isClose = () => {
  return state.templateDeep + 1 > props.deep
}

const isEmptyArrayOrObject = (data) => {
  return [{}, []].map(item => JSON.stringify(item)).includes(JSON.stringify(data))
}

watch(
    () => props.closed,
    () => {
      state.innerclosed = props.closed
    },
    {deep: true}
)

watch(
    () => props.data,
    () => {
    },
    {deep: true}
)

onMounted(() => {
  setTimeout(() => {
    state.visible = true
  }, 0)
})


</script>

<style lang="scss" scoped>
@import "./style/index";
@import "./style/on-dark";
@import "./style/vs-code";
</style>