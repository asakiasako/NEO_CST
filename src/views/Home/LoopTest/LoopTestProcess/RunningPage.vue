<template>
  <div :class="$style.wrapper">
    <div :class="$style['progress-wrapper']">
      <el-progress :percentage="progressCorners" :format="formatProgressCorners"></el-progress>
    </div>
    <div id="msg-wrapper" :class="$style['msg-wrapper']">
      <div v-for="(line, idx) in msgList" :key="idx" :class="[$style['msg-line'], $style[`msg-type-${line.msgType}`], $style[`msg-level-${line.msgLevel}`]]">
        <el-tag :type="getTagType(line.msgLevel)" size="small">{{line.msgType}}</el-tag>
        <span>{{line.msg}}</span>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  data () {
    const progressInfo = [[0, 0], [0, 0]]
    const msgList = []
    const msgLock = false
    const msgIntId = null
    const inTest = false
    return {
      progressInfo,
      msgList,
      msgLock,
      msgIntId,
      inTest
    }
  },
  computed: {
    progressCorners () {
      const [finished, total] = this.progressInfo[0]
      return total ? 100 * finished / total : 0
    },
    progressInCorner () {
      const [finished, total] = this.progressInfo[1]
      return total ? 100 * finished / total : 0
    }
  },
  methods: {
    formatProgressCorners (percentage) {
      return `${this.progressInfo[0][0]}/${this.progressInfo[0][1]} Corners Finished (${percentage.toFixed(0)}%)`
    },
    getTagType (level) {
      switch (level) {
        case 'debug':
          return 'info'
        case 'info':
          return null
        case 'warn':
          return 'warning'
        case 'error':
          return 'danger'
        case 'fatal':
          return 'danger'
      }
    },
    async startTest () {
      this.$emit('start-test')
      this.inTest = true
      this.msgList = []
      this.msgList.push({
        msgType: 'info',
        msgLevel: 'info',
        msg: 'Checking Instruments Connection...'
      })
      try {
        const instrMapping = await this.$rpcClient.request({
          route: ':instrument:mapping:get'
        })
        const failedInstruments = []
        for (const field in instrMapping) {
          const connected = await this.$rpcClient.request({
            route: ':instrument:status:check-connection',
            args: [field]
          })
          if (!connected) failedInstruments.push(field)
        }
        if (failedInstruments.length > 0) {
          const failedInstrumentsString = failedInstruments.join(', ')
          this.$confirm(`These instruments can not be connected: ${failedInstrumentsString}. Continue?`, 'Alert', {
            confirmButtonText: 'Continue',
            cancelButtonText: 'Abort',
            type: 'warning'
          }).then(() => {
            this.runTest()
          }).catch(() => {
            this.inTest = false
            this.$emit('stop-test')
            this.msgList.push({
              msgType: 'info',
              msgLevel: 'info',
              msg: 'Test aborted by user'
            })
          })
        } else {
          this.runTest()
        }
      } catch (err) {
        this.$alertError(err)
        this.inTest = false
        this.$emit('stop-test')
      }
    },
    runTest () {
      this.$rpcClient.request({
        route: ':loop-test:start-test'
      }).then(() => {
        this.refreshMsg()
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getProgress () {
      this.$rpcClient.request({
        route: ':loop-test:progress'
      }).then((result) => {
        this.progressInfo = result
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    stopTest () {
      this.$rpcClient.request({
        route: ':loop-test:stop-test'
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getMsg () {
      console.log('Get Msg')
      if (this.msgLock) return
      console.log('Get Msg Action')
      this.msgLock = true
      this.$rpcClient.request({
        route: ':loop-test:is-running'
      }).then((result) => {
        const id = this.msgIntId
        if (!result) {
          clearInterval(id)
          this.msgIntId = null
          this.inTest = false
          this.$emit('stop-test')
        }
        // log-box params for scroll
        const logBox = document.getElementById('msg-wrapper')
        const clientHeight = logBox.clientHeight
        const scrollTop = logBox.scrollTop
        const scrollHeight = logBox.scrollHeight

        this.getProgress()
        this.$rpcClient.request({
          route: ':loop-test:get-msg'
        }).then(res => {
          this.msgList.push(...res)
          if (this.msgList.length > 100) this.msgList = this.msgList.slice(-100)
          if (res.length > 0) {
            // scroll if log-box is at the end
            this.$nextTick(() => {
              if (scrollTop + clientHeight + 30 >= scrollHeight) {
                logBox.scrollTop = logBox.scrollHeight
              }
            })
          }
        }).catch(err => {
          this.$alertError(err)
        }).finally(() => {
          this.msgLock = false
        })
      }).catch((err) => {
        this.$alertError(err)
        this.msgLock = false
      })
    },
    refreshMsg () {
      if (this.msgIntId !== null) {
        clearInterval(this.msgIntId)
      }
      this.msgIntId = setInterval(() => {
        this.getMsg()
      }, 300)
    }
  },
  activated () {
    this.startTest()
  },
  beforeRouteLeave (to, from, next) {
    if (this.inTest) {
      this.$alert('You can not leave this page when test is running.', 'ERROR', {
        confirmButtonText: 'OK',
        type: 'error'
      })
    } else next()
  }
}
</script>

<style lang='scss' module>
.wrapper {
  margin: 0 20px;
  display: flex;
  flex-direction: column;
  height: 100%;
}
.progress-wrapper {
  margin: 4px 0;
}
.progress-wrapper :global(.el-progress-bar) {
  padding-right: 0;
  margin-right: 0;
}
.progress-wrapper :global(.el-progress__text) {
  margin: 0;
  width: 100%;
  text-align: right;
}
.msg-wrapper {
  padding: 8px;
  background: $background-color-base;
  border: 1px solid $border-color-light;
  border-radius: 3px;
  height: 100%;
  overflow: auto;
  font-family: $code-font-family;
}
.msg-line {
  margin: 8px;
  color: $color-text-regular;
}
.msg-line :global(.el-tag) {
  margin-right: 8px;
}
</style>
