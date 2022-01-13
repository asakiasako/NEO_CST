<template>
  <div :class="$style.wrapper">
    <div :class="$style['header-wrapper']">
      <div :class="$style['header-inner']">
        <div :class="$style.title">Multi Paramter-Config Files Test</div>
        <el-button icon="el-icon-fas fa-plus" size="small" type="success" plain @click="addFiles">Add parameter configuratin files</el-button>
        <el-button icon="el-icon-fas fa-play" size="small" type="success" @click="runMultiFileTest">Start</el-button>
      </div>
    </div>
    <div :class="$style['file-list']">
      <div :class="$style['file-item']" v-for="(file, idx) in selectedFiles" :key="idx">
        <div :class="$style['file-item-left']">
          <i class="el-icon-fas fa-file-code"></i>
        </div>
        <div :class="$style['file-item-main']">
          <div :class="$style['file-name']">{{parseFileName(file)}}</div>
          <div :class="$style['file-path']">{{file}}</div>
        </div>
        <div :class="$style['file-item-right']">
          <i class="el-icon-fas fa-minus-circle" @click="removeFile(idx)"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    const selectedFiles = []
    return {
      selectedFiles
    }
  },
  methods: {
    parseFileName (path) {
      const splitted = this.lodash.split(path, /\\|\//)
      path = splitted.pop()
      return path
    },
    runMultiFileTest () {
      this.$router.push({ name: 'multi-running-page' })
    },
    getSelectedFiles () {
      this.$rpcClient.request({
        route: ':loop-test:get-multiple-param-files'
      }).then((res) => {
        this.selectedFiles = res || []
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    addFiles () {
      this.$electron.ipcRenderer.invoke('show-open-dialog', {
        filters: [
          { name: 'JSON', extensions: ['json'] }
        ],
        properties: ['multiSelections']
      }).then(({ filepaths }) => {
        if (filepaths) {
          this.$rpcClient.request({
            route: ':loop-test:get-multiple-param-files'
          }).then((res) => {
            let selectedFiles = res || []
            selectedFiles = this.lodash.union(selectedFiles, filepaths)
            this.$rpcClient.request({
              route: ':loop-test:select-multiple-param-files',
              args: [selectedFiles]
            })
            this.getSelectedFiles()
          }).catch((err) => {
            this.$alertError(err)
          })
        }
      }).catch(err => {
        this.$alertError(err)
      })
    },
    removeFile (idx) {
      const selectedFiles = this.selectedFiles.concat()
      this.lodash.pullAt(selectedFiles, idx)
      this.$rpcClient.request({
        route: ':loop-test:select-multiple-param-files',
        args: [selectedFiles]
      }).then(res => {
        this.selectedFiles = selectedFiles
      }).catch(err => {
        this.$alertError(err)
      })
    }
  },
  activated () {
    this.getSelectedFiles()
  }
}
</script>

<style lang='scss' module>
  .wrapper {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  .title {
    font-size: 16px;
    color: $color-text-regular;
    flex-grow: 1;
  }
  .header-wrapper {
    padding: 16px 20px;
    border-bottom: 1px solid $border-color-light;
  }
  .header-inner {
    display: flex;
    align-items: center;
    width: 640px;
  }
  .file-list {
    padding: 10px 20px;
    background: $background-color-base;
    flex-grow: 1;
    overflow: auto;
  }
  .file-item {
    background: $color-white;
    padding: 10px;
    border: 1px solid $border-color-light;
    margin-bottom: 10px;
    border-radius: 5px;
    max-width: 640px;
    display: flex;
    align-items: center;
  }
  .file-item-left {
    color: $color-text-secondary;
    font-size: 20px;
    padding: 10px;
    margin-right: 10px;
  }
  .file-item-main {
    flex-grow: 1;
  }
  .file-item-right {
    color: #F75954;
    padding: 12px;
    cursor: pointer;
    color: $color-danger;
    border-radius: 4px;
  }
  .file-item-right:hover {
    color: $color-danger;
    opacity: 0.8;
    background: $color-danger-light;
  }
  .file-name {
    color: $color-text-regular;
    margin-bottom: 8px;
  }
  .file-path {
    color: $color-text-secondary;
    font-size: 12px;
  }
</style>
