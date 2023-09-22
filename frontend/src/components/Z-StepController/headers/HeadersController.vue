<template>
  <div>
    <el-row justify="space-between"
            v-for="(header, index) in data"
            :key="index"
            align="middle"
            class="el-row--flex"
            style="padding: 5px 0"
    >
      <el-col :span="7">
        <el-input type="primary"
                  size="small"
                  maxlength="200"
                  placeholder="键"
                  v-model="header.key">
          <template #suffix>
            {{ header.key.length }}/200
          </template>
        </el-input>
      </el-col>
      <el-col :span="7">
        <el-input type="primary"
                  size="small"
                  placeholder="值"
                  v-model="header.value">
        </el-input>
      </el-col>

      <el-col :span="7">
        <el-input type="primary"
                  size="small"
                  placeholder="备注"
                  v-model="header.remarks">
        </el-input>
      </el-col>

      <el-col :span="1">
        <el-button type="danger" circle @click="deleteHeaders(index)" :disabled="data.length === index  + 1 ">
          <el-icon>
            <ele-Delete/>
          </el-icon>
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup name="HeadersController">
import {reactive, watch} from 'vue';


const emit = defineEmits(["update:data"])

const props = defineProps({
  data: {
    type: Object,
    default: () => {
      return {}
    }
  },
})

const state = reactive({
  headersBulk: '',  // bulk内容
});

// bulk 转换
const bulkEdit = () => {
  keyValueToBulk()
}

const bulkToKeyValue = (headersBulk => {
  if (headersBulk.length > 0) {
    let snsArr = headersBulk.split(/[(\r\n|\n|\r)]+/)
    let headers = []
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
    emit("update:data", headers)
  }
})

const keyValueToBulk = () => {
  let bulk = ''
  if (props.data.length > 0) {
    props.data.forEach((data) => {
      if (data.key !== '') {
        bulk += `${data.key}:${data.value}\r\n`
      }
    })
  }
  return bulk
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

</script>

<style lang="scss" scoped>

</style>