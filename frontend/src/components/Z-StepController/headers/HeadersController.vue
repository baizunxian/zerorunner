<template>
  <div>

    <z-table
        v-if="!state.isBulk"
        :columns="state.columns"
        v-model:data="data"
        :show-page="false"
    />

    <div v-show="state.isBulk">
      <div class="bulk-edit-header">
        <el-text>批量编辑</el-text>
        <el-button link
                   type="primary"
                   @click="keyValueEdit">
          <span>Key-Value Edit</span>
        </el-button>
      </div>
      <div>
        <el-input v-model="state.headersContent"
                  type="textarea"
                  ref="headersContentRef"
                  :autosize="{ minRows: 20 }">
        </el-input>
      </div>
    </div>


    <!--    <el-row justify="space-between"-->
    <!--            v-for="(header, index) in data"-->
    <!--            :key="index"-->
    <!--            align="middle"-->
    <!--            class="el-row&#45;&#45;flex"-->
    <!--            style="padding: 5px 0"-->
    <!--    >-->
    <!--      <el-col :span="7">-->
    <!--        <el-input type="primary"-->
    <!--                  size="small"-->
    <!--                  maxlength="200"-->
    <!--                  placeholder="键"-->
    <!--                  v-model="header.key">-->
    <!--          <template #suffix>-->
    <!--            {{ header.key.length }}/200-->
    <!--          </template>-->
    <!--        </el-input>-->
    <!--      </el-col>-->
    <!--      <el-col :span="7">-->
    <!--        <el-input type="primary"-->
    <!--                  size="small"-->
    <!--                  placeholder="值"-->
    <!--                  v-model="header.value">-->
    <!--        </el-input>-->
    <!--      </el-col>-->

    <!--      <el-col :span="7">-->
    <!--        <el-input type="primary"-->
    <!--                  size="small"-->
    <!--                  placeholder="备注"-->
    <!--                  v-model="header.remarks">-->
    <!--        </el-input>-->
    <!--      </el-col>-->

    <!--      <el-col :span="1">-->
    <!--        <el-button type="danger" circle @click="deleteHeaders(index)" :disabled="data.length === index  + 1 ">-->
    <!--          <el-icon>-->
    <!--            <ele-Delete/>-->
    <!--          </el-icon>-->
    <!--        </el-button>-->
    <!--      </el-col>-->
    <!--    </el-row>-->
  </div>
</template>

<script setup name="HeadersController">
import {computed, h, nextTick, reactive, ref, watch} from 'vue';
import {ElButton, ElInput} from "element-plus";
import {Delete} from "@element-plus/icons";

const headersContentRef = ref()

const emit = defineEmits(["update:data"])

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})

const data = computed({
  get: () => props.data,
  set: (val) => emit("update:data", val)
})


const state = reactive({
  headersContent: '',  // bulk内容
  isBulk: false,
  columns: [
    {
      key: 'key', label: 'key', width: '', align: 'center', show: true,
      render: ({row, $index}) => h(ElInput, {
        modelValue: row.key
      })
    },
    {
      key: 'value', label: 'value', width: '', align: 'center', show: true,
      render: ({row, $index}) => h(ElInput, {
        modelValue: row.value
      })
    },
    {
      key: 'remarks', label: '备注', width: '', align: 'center', show: true,
      render: ({row, $index}) => h(ElInput, {
        modelValue: row.remarks
      })
    },
    {
      label: '操作', fixed: 'right', width: '140', align: 'center',
      renderHeader: () => h("div", null, [
        h(ElButton, {
          type: "primary",
          link: true,
          onClick: () => {
            bulkEdit()
          },
        }, () => "Bulk Edit")
      ]),
      render: ({row, $index}) => h("div", null, [
        h(ElButton, {
          type: "danger",
          icon: Delete,
          disabled: props.data.length === $index + 1,
          circle: true,
          onClick: () => {
            deleteHeaders($index)
          }
        },)
      ]),

    },
  ]
});

// bulk 转换
const bulkEdit = () => {
  keyValueToString()
  state.isBulk = true
  nextTick(() => {
    headersContentRef.value.focus()
  })
}
// bulk 转换
const keyValueEdit = () => {
  stringToKeyValue()
  state.isBulk = false
}

const stringToKeyValue = () => {
  let headers = []
  if (state.headersContent.length > 0) {
    let snsArr = state.headersContent.split(/[(\r\n|\n|\r)]+/)
    if (snsArr.length > 0) {
      snsArr.forEach(data => {
        let keyValue = data.split(':')
        if (keyValue.length > 0 && keyValue[0] !== "") {
          let head = {}
          head.key = keyValue[0]
          head.value = keyValue.length > 1 ? keyValue[1] : ""
          headers.push({key: head.key, value: head.value, remarks: ""})
        }
      })
    }
  }
  emit("update:data", headers)
}

const keyValueToString = () => {
  let newHeadersContent = ""
  if (props.data.length > 0) {
    props.data.forEach((data) => {
      if (data.key !== '') {
        newHeadersContent += `${data.key}:${data.value}\n`
      }
    })
  }
  if (state.headersContent === newHeadersContent) {
    return false
  }
  state.headersContent = newHeadersContent
}

// Headers
const addHeaders = () => {
  props.data.push({key: '', value: '', remarks: ""})
}
const deleteHeaders = (index) => {
  props.data.splice(index, 1)
}

const headerBlur = () => {
  if (props.data) {
    let endData = props.data[props.data.length - 1]
    if (!endData) {
      addHeaders()
    } else if (endData.key !== "" || endData.value !== "") {
      addHeaders()
    }
  }
}

watch(
    () => props.data,
    (val) => {
      if (val) {
        headerBlur()
      }
    },
    {
      deep: true,
      immediate: true,
    }
);
watch(
    () => state.headersContent,
    (val) => {
      if (val) {
        stringToKeyValue()
      }
    },
    {
      deep: true,
      immediate: true,
    }
);

</script>

<style lang="scss" scoped>
.bulk-edit-header {
  width: 100%;
  display: flex;
  height: 34px;
  padding: 4px;
  justify-content: space-between;
  line-height: 34px;
  //border-bottom: 1px solid #ebeef5;
  border-top: 1px solid #ebeef5;
}

</style>