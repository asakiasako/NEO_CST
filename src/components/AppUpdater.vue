<template>
    <el-dialog
      title="Update"
      width="800px"
      :custom-class="$style['dialog-update']"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :visible.sync="dialogUpdateVisible"
    >
      <el-card shadow="never">
        <p :class="$style['download-title']">Download Version {{updateVersion}}</p>
        <el-progress :percentage="downloadProgress.percent" :stroke-width="9" :status="downloaded ? 'success' : null"></el-progress>
        <p :class="$style['download-info']">{{`transferred/total: ${progressStr}`}}</p>
      </el-card>
    </el-dialog>
</template>

<script>
export default {
  data () {
    return {
      downloadProgress: {
        bytesPerSecond: 0,
        delta: 0,
        percent: 0,
        total: 0,
        transferred: 0
      },
      dialogUpdateVisible: false,
      updateVersion: undefined
    }
  },
  computed: {
    progressStr () {
      const transferred = (this.downloadProgress.transferred / 1000000).toFixed(1)
      const total = (this.downloadProgress.total / 1000000).toFixed(1)
      return `${transferred} MB / ${total} MB`
    }
  },
  methods: {
    initStates () {
      this.downloadProgress = {
        bytesPerSecond: 0,
        delta: 0,
        percent: 0,
        total: 0,
        transferred: 0
      }
      this.updateVersion = undefined
    },
    downloadUpdate () {
      this.$electron.ipcRenderer.send('download-update')
    },
    quitAndInstall () {
      this.$electron.ipcRenderer.send('quit-and-install')
    },
    checkForUpdates () {
      this.$electron.ipcRenderer.invoke('check-for-update')
    }
  },
  created () {
    this.$electron.ipcRenderer.on('update-available', (event, info) => {
      this.initStates()
      this.updateVersion = info.version
      this.$confirm(`An update is available. Version: ${info.version}. Update now?`, 'Update', {
        type: 'info',
        closeOnClickModal: false,
        closeOnPressEscape: false
      }).then(() => {
        this.dialogUpdateVisible = true
        this.downloadUpdate()
      }).catch((err) => {
        console.log(err)
      })
    })
    this.$electron.ipcRenderer.on('update-error', (event, err) => {
      this.$alertError(err, () => {
        this.dialogUpdateVisible = false
      })
    })
    this.$electron.ipcRenderer.on('download-progress', (event, progress) => {
      this.downloadProgress = progress
    })
    this.$electron.ipcRenderer.on('update-downloaded', (event, info) => {
      this.downloadProgress.percent = 100
      this.downloaded = true
      this.$alert(`Version ${info.version} has been downloaded. App will restart automatically after update.`, 'Ready for update').finally(() => {
        this.quitAndInstall()
      })
    })
    this.checkForUpdates()
  }
}
</script>

<style module lang="scss">
  .download-title {
    margin-top: 0;
    margin-bottom: 16px;
    color: $color-text-regular;
  }
  .dialog-update :global(.el-dialog__body) {
    padding-top: 15px;
  }
</style>
