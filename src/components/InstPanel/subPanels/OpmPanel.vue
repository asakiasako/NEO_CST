<template>
  <div>
    <div :class="$style['inst-title']">
      <span>{{instTitle}}</span>
      <span>
        <el-button :class="$style['inst-conf-btn']" title="config" :disabled="!isConnected" @click="onOpenCfg" type="text">
          <i :class="[$style['btn'], 'el-icon-fas fa-cog']"></i>
        </el-button>
        <i v-if="isConnected" :class="[$style['btn'], $style['toggle-on'], 'el-icon-success']" title="Connected" @click="disconnect"></i>
        <i v-else :class="[$style.btn, $style['toggle-off'], 'el-icon-remove']" title="Not Connected" @click="connect"></i>
      </span>
    </div>
    <div :class="$style['inst-main']">
      <div :class="$style['info-line']">
        <div :class="$style['ip-monitor']">
          <span :class="$style['ip-monitor-name']">Power</span>
          <span :class="$style['ip-monitor-value']">{{fmtOpmValue}}</span>
          <span :class="$style['ip-monitor-unit']">dBm</span>
        </div>
        <el-button @click="getOpmValue">Get</el-button>
      </div>
      <el-dialog :title="`Config - ${instTitle}`" :visible.sync="cfgDlgVisible" width="400px">
        <el-form :model="configs" label-width="160px" label-position="left">
          <el-form-item v-for="(item, key) in configs" :key="key" :label="key">
            <div :class="$style['cfg-item-wrapper']">
              <div :class="$style['cfg-item-value']">
                <el-input-number v-if="item.type === 'number'" v-model="item.value" size="small" :min="item.min" :max="item.max" :controls="item.controls" :step="item.step"></el-input-number>
                <el-select v-if="item.type === 'select'" v-model="item.value" size="small">
                  <el-option v-for="i in item.options" :key="i" :label="i" :value="i"></el-option>
                </el-select>
              </div>
              <div :class="$style['cfg-item-unit']">
                {{item.unit ? item.unit : ''}}
              </div>
            </div>
          </el-form-item>
        </el-form>
        <div slot="footer" :class="$style['dialog-footer']">
          <el-button @click="cfgDlgVisible=false">Cancel</el-button>
          <el-button type="primary" @click="setConfigs">OK</el-button>
        </div>
      </el-dialog>
    </div>
  </div>

</template>

<script>
export default {
  props: ['alias', 'instType', 'label'],
  data () {
    const isConnected = false
    const cfgDlgVisible = false
    const opmValue = null
    const configs = {
      'Center Frequency': {
        type: 'number',
        controls: false,
        min: -Infinity,
        max: Infinity,
        value: null,
        unit: 'THz'
      },
      'Average Time': {
        type: 'number',
        min: -Infinity,
        max: Infinity,
        value: null,
        unit: 'ms'
      },
      Calibration: {
        type: 'number',
        min: -Infinity,
        max: Infinity,
        step: 0.1,
        value: null,
        unit: 'dB'
      }
    }
    const refreshLock = false
    const refreshOn = false
    return {
      isConnected,
      cfgDlgVisible,
      opmValue,
      configs,
      refreshLock,
      refreshOn
    }
  },
  computed: {
    instTitle () {
      if (this.alias) {
        return `${this.alias} (${this.label})`
      } else {
        return `${this.label}`
      }
    },
    fmtOpmValue () {
      return (this.opmValue !== null) ? this.lodash.round(this.opmValue, 2).toFixed(2) : 'N/A'
    }
  },
  methods: {
    getOpmValue () {
      const self = this
      return this.$rpcClient.request({
        route: ':instrument:operation:call-method',
        kwargs: {
          field: self.label,
          method_name: 'get_dbm_value'
        }
      }).then(res => {
        this.opmValue = res
      }).catch(err => {
        this.$alertError(err)
      })
    },
    onOpenCfg () {
      this.getConfigs().catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.cfgDlgVisible = true
      })
    },
    async connect () {
      if (this.isConnected) {
        return
      }
      const self = this
      try {
        // check connection
        const connected = await this.$rpcClient.request({
          route: ':instrument:status:check-connection',
          kwargs: {
            field: self.label
          }
        })
        if (!connected) {
          throw new Error(`Connection failed: ${self.label}`)
        }
        // connect instrument
        await this.$rpcClient.request({
          route: ':instrument:operation:connect',
          kwargs: {
            field: self.label
          }
        })
        // get origin configs
        await self.getConfigs()
        // update states after connected
        this.isConnected = true
      } catch (err) {
        this.$alertError(err)
        this.disconnect()
      }
    },
    disconnect () {
      const self = this
      if (!this.isConnected) return
      this.refreshOn = false
      this.isConnected = false
      this.$rpcClient.request({
        route: ':instrument:operation:disconnect',
        kwargs: {
          field: self.label
        }
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getConfigs () {
      // get origin configs, max/min, and options
      const self = this
      const promises = []
      const cfgList = [
        'get_frequency',
        'get_avg_time',
        'get_cal'
      ]
      for (const i of cfgList) {
        promises.push(
          this.$rpcClient.request({
            route: ':instrument:operation:call-method',
            kwargs: {
              field: self.label,
              method_name: i
            }
          })
        )
      }
      const attrList = [
        'min_frequency',
        'max_frequency',
        'min_avg_time',
        'max_avg_time',
        'min_cal',
        'max_cal'
      ]
      for (const i of attrList) {
        promises.push(
          this.$rpcClient.request({
            route: ':instrument:operation:get-attr',
            kwargs: {
              field: self.label,
              attr_name: i
            }
          })
        )
      }
      return Promise.all(promises).then((result) => {
        self.configs['Center Frequency'].value = this.lodash.round(result[0], 3)
        self.configs['Average Time'].value = this.lodash.round(result[1], 3)
        self.configs.Calibration.value = this.lodash.round(result[2], 2)
        self.configs['Center Frequency'].min = result[3]
        self.configs['Center Frequency'].max = result[4]
        self.configs['Average Time'].min = result[5]
        self.configs['Average Time'].max = result[6]
        self.configs.Calibration.min = result[7]
        self.configs.Calibration.max = result[8]
      })
    },
    setConfigs () {
      const self = this
      const centerFreq = this.configs['Center Frequency'].value
      const avgTime = this.configs['Average Time'].value
      const cal = this.configs.Calibration.value
      const configMap = {
        set_frequency: centerFreq,
        set_avg_time: avgTime,
        set_cal: cal
      }
      const promises = []
      for (const k in configMap) {
        promises.push(
          self.$rpcClient.request({
            route: ':instrument:operation:call-method',
            kwargs: {
              field: self.label,
              method_name: k,
              args: [configMap[k]]
            }
          })
        )
      }
      Promise.all(promises).then(res => {
        self.cfgDlgVisible = false
      }).catch(err => {
        this.$alertError(err)
      })
    },
    setFrequency (freq) {
      const self = this
      if (!this.isConnected) {
        this.$alert(`${self.instTitle} - Instrument is not connected.`, 'ERROR', {
          confirmButtonText: 'OK',
          type: 'error'
        })
      } else if (!(self.configs['Center Frequency'].min <= freq <= self.configs['Center Frequency'].max)) {
        this.$alert(`${self.instTitle} - Out of frequency range.`, 'ERROR', {
          confirmButtonText: 'OK',
          type: 'error'
        })
      } else {
        this.$rpcClient.request({
          route: ':instrument:operation:call-method',
          kwargs: {
            field: self.label,
            method_name: 'set_frequency',
            args: [freq]
          }
        }).catch(err => {
          this.$alert(`${self.instTitle} - [${err.name}] ${err.message}`, 'ERROR', {
            confirmButtonText: 'OK',
            type: 'error'
          })
        })
      }
    }
  },
  created () {
    const self = this
    this.$bus.$on('inst-panel:connect-all', self.connect)
    this.$bus.$on('inst-panel:disconnect-all', self.disconnect)
    this.$bus.$on('inst-panel:set-all-frequency', self.setFrequency)
  },
  beforeDestroy () {
    const self = this
    this.$bus.$off('inst-panel:connect-all', self.connect)
    this.$bus.$off('inst-panel:disconnect-all', self.disconnect)
    this.$bus.$off('inst-panel:set-all-frequency', self.setFrequency)
  }
}
</script>

<style lang="scss" module>

  .inst-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 4px;
    border-bottom: 1px solid $border-color-light;
    color: $color-text-secondary;
  }
  .inst-title span {
    display: flex;
    align-items: center;
  }
  .inst-title .inst-conf-btn {
    padding: 0;
  }
  .inst-conf-btn:global(.el-button--text) {
    color: $color-text-secondary;
  }
  .inst-conf-btn:global(.el-button--text:hover), .inst-conf-btn:global(.el-button--text:focus) {
    color: $color-text-secondary;
    opacity: 0.8;
  }
  .inst-title .btn {
    font-size: 16px;
    margin-left: 8px;
  }
  .inst-title .btn.toggle-on, .inst-title .btn.toggle-off {
    cursor: pointer;
  }
  .inst-title .toggle-on {
    color: $color-success;
  }
  .inst-title .toggle-off {
    color: $color-warning;
  }
  .inst-title .btn.toggle-on:hover, .inst-title .btn.toggle-off:hover {
    opacity: 0.8;
  }
  .inst-main {
    padding-top: 8px;
    color: $color-text-regular;
  }
  // specified
  .info-line {
    display: flex;
  }
  .ip-monitor {
    display: flex;
    flex-grow: 1;
    margin-right: 5px;
    justify-content: space-between;
    align-items: center;
    font-size: 1.6em;
    color: $color-text-regular;
    padding: 4px 12px;
    background: #f5f7fa;
    border-radius: 4px;
    border: 1px solid #e4e7ed;
  }
  .ip-monitor-name {
    flex-grow: 1;
    font-size: 0.8em;
    color: $color-text-secondary;
  }
  .ip-monitor-unit {
    padding-left: 10px;
    font-size: 0.8em;
    padding-top: 0.2em;
    color: $color-text-secondary;
    width: 48px;
    text-align: right;
  }
</style>
