<template>
  <div>
    <el-dialog title="更换头像"
               destroy-on-close
               v-model="state.isShowDialog"
               width="769px">
      <template #header>
        <div style="display:flex;">
          <span style="margin-right: 10px">更换头像</span>
          <slot>
            <el-upload :before-upload="beforeUpload" :showUploadList='false'>
              <el-button type="primary">选择图片</el-button>
            </el-upload>
          </slot>
        </div>
      </template>
      <div class="cropper-warp">
        <div class="cropper-warp-left">
          <img :src="state.cropperImg" class="cropper-warp-left-img" id="AvatarRef"/>
        </div>
        <div class="cropper-warp-right">
          <div class="cropper-warp-right-title">预览</div>
          <div class="cropper-warp-right-item">
            <div class="cropper-warp-right-value">
              <img :src="state.cropperImgBase64" class="cropper-warp-right-value-img"/>
            </div>
            <div class="cropper-warp-right-label">100 x 100</div>
          </div>
          <div class="cropper-warp-right-item">
            <div class="cropper-warp-right-value">
              <img :src="state.cropperImgBase64" class="cropper-warp-right-value-img cropper-size"/>
            </div>
            <div class="cropper-warp-right-label">50 x 50</div>
          </div>
        </div>
      </div>
      <template #footer>
				<span class="dialog-footer">
					<el-button @click="onCancel" size="default">取 消</el-button>
					<el-button type="primary" @click="onSubmit" size="default">更 换</el-button>
				</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="cropper">
import {reactive, nextTick} from 'vue';
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';

const emit = defineEmits(['updateAvatar'])

// 定义变量内容
const state = reactive({
  isShowDialog: false,
  cropperImg: '',
  blobUrl: '',
  cropperImgBase64: '',
  cropper: '',
});

// 打开弹窗
const openDialog = (imgs) => {
  // if (!imgs) {
  //   return
  // }
  state.cropperImg = imgs;
  state.isShowDialog = true;
  nextTick(() => {
    initCropper();
  });
};
// 关闭弹窗
const closeDialog = () => {
  state.isShowDialog = false;
};
// 取消
const onCancel = () => {
  closeDialog();
};
// 更换
const onSubmit = () => {
  state.cropperImgBase64 = state.cropper.getCroppedCanvas().toDataURL('image/jpeg');
  emit("updateAvatar", state.cropperImgBase64)

};
// 初始化cropperjs图片裁剪
const initCropper = () => {
  const letImg = document.getElementById("AvatarRef");
  state.cropper = new Cropper(letImg, {
    viewMode: 1,
    dragMode: 'none',
    initialAspectRatio: 1,
    aspectRatio: 1,
    preview: '.cropper-warp-right-value',
    background: false,
    autoCropArea: 1,
    zoomOnWheel: true,
    crop: () => {
      // preview()
      // state.cropperImgBase64 = state.cropper.getCroppedCanvas().toDataURL('image/jpeg');
    },
  });
};

const preview = () => {
  state.cropperImgBase64 = state.cropper.getCroppedCanvas().toDataURL('image/jpeg');
}

const beforeUpload = (file) => {
  const reader = new FileReader()
  reader.readAsDataURL(file)
  reader.onload = () => {
    state.cropper.replace(URL.createObjectURL(file))
  }
  return false
}
// 暴露变量
defineExpose({
  openDialog,
  state,
});
</script>

<style scoped lang="scss">
.cropper-warp {
  display: flex;

  .cropper-warp-left {
    position: relative;
    display: inline-block;
    height: 350px;
    flex: 1;
    border: 1px solid var(--el-border-color);
    background: var(--el-color-white);
    overflow: hidden;
    background-repeat: no-repeat;
    cursor: move;
    border-radius: var(--el-border-radius-base);

    .cropper-warp-left-img {
      width: 100%;
      height: 100%;
    }
  }

  .cropper-warp-right {
    width: 150px;
    height: 350px;

    .cropper-warp-right-title {
      text-align: center;
      height: 20px;
      line-height: 20px;
    }

    .cropper-warp-right-item {
      margin: 15px 0;

      .cropper-warp-right-value {
        overflow: hidden;
        margin: auto;
        border-radius: var(--el-border-radius-circle);

        .cropper-warp-right-value-img {
          margin: auto;
          width: 100px;
          height: 100px;
        }

        .cropper-size {
          width: 50px;
          height: 50px;
        }
      }

      .cropper-warp-right-label {
        text-align: center;
        font-size: 12px;
        color: var(--el-text-color-primary);
        height: 30px;
        line-height: 30px;
      }
    }
  }
}
</style>
