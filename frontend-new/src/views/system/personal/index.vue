<template>
  <div class="personal layout-pd">
    <el-row>
      <!-- 个人信息 -->
      <el-col :xs="24" :sm="8" style="padding: 0 10px">
        <el-card>
          <div class="personal-user">
            <div class="personal-user-avatar" @click="onCropperDialogOpen">
              <!--              <el-upload class="h100 personal-user-left-upload" action="https://jsonplaceholder.typicode.com/posts/"-->
              <!--                         multiple :limit="1">-->
              <img :src="state.personalForm.avatar"/>
              <!--              </el-upload>-->
            </div>
            <div class="personal-user-right">
              <el-row>
                <el-col :span="24">
                  <div class="personal-user-name">
                    <strong>{{ state.personalForm.nickname }}</strong>
                  </div>
                </el-col>
                <el-col :span="24">
                  <div class="personal-user-description">
                    <div>
                      <span>{{ state.personalForm.remarks }}</span>
                    </div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <el-divider content-position="left">个人信息</el-divider>
                </el-col>
                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">昵称：</div>
                    <div class="personal-item-value">{{ userStores.userInfos.nickname }}</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">身份：</div>
                    <div class="personal-item-value">超级管理</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">登录IP：</div>
                    <div class="personal-item-value">192.168.1.1</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">登录时间：</div>
                    <div class="personal-item-value">2021-02-05 18:47:26</div>
                  </div>
                </el-col>

                <el-col :span="24">
                  <div class="personal-item">
                    <div class="personal-item-label">密码：</div>
                    <div class="personal-item-value">
                      <el-button text type="primary">修改密码</el-button>
                    </div>
                  </div>
                </el-col>
                <el-col :span="24">
                  <el-button type="primary" @click="state.showEditPage = !state.showEditPage">
                    <el-icon>
                      <ele-Position/>
                    </el-icon>
                    更新个人信息
                  </el-button>
                </el-col>

                <el-col :span="24">
                  <el-divider content-position="left">个性标签</el-divider>
                </el-col>
                <el-col :span="24">
                  <div class="personal-item-tag">
                    <el-tag
                        v-for="tag in state.personalForm.tags"
                        :key="tag"
                        size="default"
                        type="success"
                        style="{margin-left: 0.25rem;margin-right: 0.25rem;}"
                        :disable-transitions="false"
                    >{{ tag }}
                    </el-tag>
                  </div>
                </el-col>

              </el-row>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 消息通知 -->
      <el-col :xs="24" :sm="16" class="pl15 personal-info">
        <el-card shadow="hover">
          <template #header>
            <span>消息通知</span>
          </template>
          <div class="personal-info-box">
            <ul class="personal-info-ul">
              <li v-for="(v, k) in state.newsInfoList" :key="k" class="personal-info-li">
                <a :href="v.link" target="_block" class="personal-info-li-title">{{ v.title }}</a>
              </li>
            </ul>
          </div>
        </el-card>
      </el-col>


    </el-row>
    <!-- 更新信息 -->
    <el-dialog title="更新"
               destroy-on-close
               v-model="state.showEditPage">
      <el-row>
        <el-col :span="24" style="padding: 0 10px">
          <el-card class="personal-edit">
            <div class="personal-edit-title">基本信息</div>
            <el-form :model="state.personalForm" size="default" label-width="auto" class="mt35 mb35">
              <el-row :gutter="35">
                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="昵称">
                    <el-input v-model="state.personalForm.nickname" placeholder="请输入昵称" clearable></el-input>
                  </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="签名">
                    <el-input v-model="state.personalForm.remarks" placeholder="请输入签名" clearable></el-input>
                  </el-form-item>
                </el-col>

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="个性标签">
                    <el-tag
                        v-for="tag in state.personalForm.tags"
                        :key="tag"
                        size="default"
                        type="success"
                        closable
                        style="{margin-left: 0.25rem;margin-right: 0.25rem;}"
                        :disable-transitions="false"
                        @close="removeTag(tag)"
                    >{{ tag }}
                    </el-tag>

                    <el-input
                        v-if="state.editTag"
                        ref="UserTagInputRef"
                        v-model="state.tagValue"
                        class="ml-1 w-20"
                        size="small"
                        @keyup.enter="addTag"
                        @blur="addTag"
                        style="width: 100px"
                    />
                    <el-button v-else size="small" @click="showEditTag">
                      + New Tag
                    </el-button>
                    <!--                  <el-input v-model="state.personalForm.tags" placeholder="请输入签名" clearable></el-input>-->
                  </el-form-item>
                </el-col>

                <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mb20">
                  <el-form-item label="邮箱">
                    <el-input v-model="state.personalForm.email" placeholder="请输入邮箱" clearable></el-input>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
      <template #footer>
        <el-button type="primary" @click="save">
          更新
        </el-button>
      </template>
    </el-dialog>

    <SeePictures ref="SeePicturesRef" @updateAvatar="updateAvatar"></SeePictures>
  </div>
</template>

<script setup lang="ts" name="personal">
import {computed, defineAsyncComponent, nextTick, onMounted, reactive, ref} from 'vue';
import {formatAxis} from '/@/utils/formatTime';
import {useUserInfo} from "/@/stores/userInfo";
import {useUserApi} from "/@/api/useSystemApi/user";
import {ElMessage} from "element-plus";

const SeePictures = defineAsyncComponent(() => import("/@/components/seePictures/index.vue"))
const SeePicturesRef = ref();
const UserTagInputRef = ref()

// 用户信息
const userStores = useUserInfo()


// 定义变量内容
const state = reactive<PersonalState>({
  newsInfoList: [],
  recommendList: [],
  personalForm: {
    username: '',
    nickname: '',
    avatar: '',
    remarks: '',
    email: '',
    tags: '',
  },
  editTag: false,
  tagValue: "",

  showEditPage: false,
  cropperImg: '',
});

const getUserInfo = async () => {
  let {data} = await useUserApi().getUserInfoByToken()
  if (!data.avatar) {
    data.avatar = "data:image/jpeg;base64,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"
  }
  state.personalForm = data
}

// 当前时间提示语
const currentTime = computed(() => {
  return formatAxis(new Date());
});

// 打开裁剪弹窗
const onCropperDialogOpen = () => {
  SeePicturesRef.value.openDialog(state.personalForm.avatar);
};


// tags
const showEditTag = () => {
  state.editTag = true
  nextTick(() => {
    UserTagInputRef.value!.input!.focus()
  })
}

const removeTag = (tag: string) => {
  state.personalForm.tags.splice(state.personalForm.tags.indexOf(tag), 1)
}

const addTag = () => {
  if (state.editTag && state.tagValue) {
    if (!state.personalForm.tags) state.personalForm.tags = []
    state.personalForm.tags.push(state.tagValue)
  }
  state.editTag = false
  state.tagValue = ''
}

const save = async () => {
  let {data} = await useUserApi().saveOrUpdate(state.personalForm)
  await userStores.setUserInfos(data)
  await getUserInfo()
  ElMessage.success("更新成功!")
}

const updateAvatar = (img: String) => {
  state.personalForm.avatar = img
  save()
}

onMounted(() => {
  getUserInfo()
})
</script>

<style scoped lang="scss">
@import '../../../theme/mixins/index.scss';

.personal {
  .personal-user {
    //height: 130px;
    //display: flex;
    align-items: center;
    padding: 20px;


    .personal-user-avatar {
      width: 100px;
      height: 100px;
      margin: auto;
      border-radius: 3px;
      margin-bottom: 20px;

      img {
        cursor: pointer;
        width: 100%;
        height: 100%;
        border-radius: 50%;
      }
    }


    .personal-user-right {
      flex: 1;
      padding: 0 15px;

      .personal-user-name {
        text-align: center;
        font-size: 20px;
        margin-bottom: 10px;
      }

      .personal-user-description {
        text-align: center;
      }

      .personal-title {
        font-size: 18px;
        @include text-ellipsis(1);
      }

      .personal-item {
        display: flex;
        align-items: center;
        font-size: 13px;
        height: 30px;
        width: 100%;
        flex-flow: wrap;

        .personal-item-label {
          color: var(--el-text-color-secondary);
          @include text-ellipsis(1);
        }

        .personal-item-value {
          @include text-ellipsis(1);
        }
      }

      .personal-item-tag {
        .personal-item-tag-item {
          margin: 5px;
          float: left;
        }
      }
    }
  }

  .personal-info {

    .personal-info-box {
      height: 130px;
      overflow: hidden;

      .personal-info-ul {
        list-style: none;

        .personal-info-li {
          font-size: 13px;
          padding-bottom: 10px;

          .personal-info-li-title {
            display: inline-block;
            @include text-ellipsis(1);
            color: var(--el-text-color-secondary);
            text-decoration: none;
          }

          & a:hover {
            color: var(--el-color-primary);
            cursor: pointer;
          }
        }
      }
    }
  }

  .personal-recommend-row {
    .personal-recommend-col {
      .personal-recommend {
        position: relative;
        height: 100px;
        border-radius: 3px;
        overflow: hidden;
        cursor: pointer;

        &:hover {
          i {
            right: 0px !important;
            bottom: 0px !important;
            transition: all ease 0.3s;
          }
        }

        i {
          position: absolute;
          right: -10px;
          bottom: -10px;
          font-size: 70px;
          transform: rotate(-30deg);
          transition: all ease 0.3s;
        }

        .personal-recommend-auto {
          padding: 15px;
          position: absolute;
          left: 0;
          top: 5%;
          color: var(--next-color-white);

          .personal-recommend-msg {
            font-size: 12px;
            margin-top: 10px;
          }
        }
      }
    }
  }

  .personal-edit {
    .personal-edit-title {
      position: relative;
      padding-left: 10px;
      color: var(--el-text-color-regular);

      &::after {
        content: '';
        width: 2px;
        height: 10px;
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        background: var(--el-color-primary);
      }
    }

    .personal-edit-safe-box {
      border-bottom: 1px solid var(--el-border-color-light, #ebeef5);
      padding: 15px 0;

      .personal-edit-safe-item {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;

        .personal-edit-safe-item-left {
          flex: 1;
          overflow: hidden;

          .personal-edit-safe-item-left-label {
            color: var(--el-text-color-regular);
            margin-bottom: 5px;
          }

          .personal-edit-safe-item-left-value {
            color: var(--el-text-color-secondary);
            @include text-ellipsis(1);
            margin-right: 15px;
          }
        }
      }

      &:last-of-type {
        padding-bottom: 0;
        border-bottom: none;
      }
    }
  }
}
</style>
