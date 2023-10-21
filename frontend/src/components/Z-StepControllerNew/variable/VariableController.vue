<template>
  <!-- data - table -->
  <div class="content">
    <el-row justify="space-between"
            v-for="(variable, index) in data"
            :key="index"
            align="middle"
            class="el-row--flex"
            style="padding: 5px 0"
    >
      <el-col :span="7">
        <el-input type="primary"
                  size="small"
                  maxlength="200"
                  placeholder="变量名"
                  v-model="variable.key">
          <template #suffix>
            {{ variable.key.length }}/200
          </template>
        </el-input>
      </el-col>
      <el-col :span="7">
        <el-input type="primary"
                  size="small"
                  placeholder="值"
                  v-model="variable.value">
        </el-input>
      </el-col>

      <el-col :span="7">
        <el-input type="primary"
                  size="small"
                  placeholder="备注"
                  v-model="variable.remarks">
        </el-input>
      </el-col>

      <el-col :span="1">
        <el-button type="danger"
                   circle
                   @click="deleteVariables(index)"
                   :disabled="data.length === index  + 1 ">
          <el-icon>
            <ele-Delete/>
          </el-icon>
        </el-button>
      </el-col>

    </el-row>

  </div>
</template>

<script setup name="VariableController">
import {watch} from "vue";
const props = defineProps({
  data: {
    type: Array,
    default: () => {
      return [{key: '', value: '', remarks: ""}]
    }
  },
})

// variables
const addVariables = () => {
  props.data.push({key: '', value: '', remarks: ''})
}
const deleteVariables = (index) => {
  props.data.splice(index, 1)
}


const variableBlur = () => {
  if (props.data) {
    let endData = props.data[props.data.length - 1]
    if (!endData) {
      addVariables()
    } else if (endData.key !== "" || endData.value !== "") {
      addVariables()
    }
  }
}

watch(
    () => props.data,
    (val) => {
      if (val) {
        variableBlur()
      }
    },
    {
      deep: true,
      immediate: true,
    }
);

</script>
