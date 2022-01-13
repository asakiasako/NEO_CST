<template>
  <el-container :class="$style.wrapper">
    <el-header :class="$style.header" height="120px">
      <div :class="$style['start-tip']">Start Loop Test</div>
      <div :class="$style['button-wrapper']">
        <el-button size="small" type="primary" round @click="selectParams">Select Params</el-button>
        <el-button size="small" type="primary" round @click="loadParamsFromFile">Load From Config File</el-button>
        <el-button size="small" type="primary" round @click="multiFilesTest">Multi Config File Test</el-button>
      </div>
    </el-header>
    <el-main :class="$style.main">
      <h1 :class="$style.title">Options</h1>
      <test-options></test-options></el-main>
  </el-container>
</template>

<script>
import TestOptions from '@/views/Home/LoopTest/LoopTestStart/parts/TestOptions.vue'

export default {
  components: {
    TestOptions
  },
  methods: {
    selectParams () {
      this.$router.push({ name: 'loop-config' })
    },
    loadParamsFromFile () {
      this.$electron.ipcRenderer.invoke('show-open-dialog', {
        filters: [
          { name: 'JSON', extensions: ['json'] }
        ],
        properties: ['openFile']
      }).then(({ filepaths }) => {
        if (filepaths) {
          this.$rpcClient.request({
            route: ':loop-test:load-params-from-file',
            args: [filepaths[0]]
          }).then((res) => {
            this.$router.push({ name: 'confirm-page' })
          }).catch((err) => {
            this.$alertError(err)
          })
        }
      }).catch(err => {
        this.$alertError(err)
      })
    },
    multiFilesTest () {
      this.$router.push({ name: 'multi-file-test-config' })
    }
  }
}
</script>

<style lang='scss' module>
  .wrapper {
    height: 100%;
  }
  .main:global(.el-main) {
    padding: 0 30px;
  }
  .title {
    color: $color-text-secondary;
    font-weight: normal;
    font-size: 16px;
  }
  .header:global(.el-header) {
    border-bottom: 1px solid $border-color-lighter;
    padding: 0 30px;
  }
  .button-wrapper {
    display: flex;
    align-items: center;
  }
  .start-tip {
    margin: 20px 0;
    color: $color-text-secondary;
    font-size: 16px;
  }
</style>
