<template>
  <div>
    <div :class="$style['inst-title']">
      <span>{{instTitle}}</span>
      <span>
        <el-button :class="$style['inst-conf-btn']" title="config" :disabled="!isConnected" @click="onOpenCfg" type="text">
          <i :class="[$style['btn'], 'el-icon-fas fa-cog']"></i>
        </el-button>
        <i v-if="isConnected" :class="[$style['btn'], $style['toggle-on'], 'el-icon-success']" title="Connected" @click="disconnect"></i>
        <i v-else :class="[$style['btn'], $style['toggle-off'], 'el-icon-remove']" title="Not Connected" @click="connect"></i>
      </span>
    </div>
    <div :class="$style['inst-main']">
      <div :class="$style['info-line']">
        <div :class="$style['ip-monitor']">
          <span :class="$style['ip-monitor-name']">OSNR</span>
          <span :class="$style['ip-monitor-value']">{{fmtOsnrValue}}</span>
          <span :class="$style['ip-monitor-unit']">dB</span>
        </div>
        <el-button @click="getOsnrValue">Get</el-button>
      </div>
      <el-dialog :title="`Config - ${instTitle}`" :visible.sync="cfgDlgVisible" width="400px">
        <div :class="$style['cfg-dlg-wrapper']" v-loading="cfgLoading" element-loading-text="Configuring OSA..." element-loading-spinner="el-icon-loading">
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
    const osnrValue = null
    const configs = {
      'Center Frequency': {
        type: 'number',
        controls: false,
        min: 0,
        max: Infinity,
        value: null,
        unit: 'THz'
      },
      'Resolution BW': {
        type: 'number',
        min: 0,
        max: Infinity,
        value: null,
        unit: 'nm'
      },
      'Mask Area': {
        type: 'number',
        min: 0,
        max: Infinity,
        step: 0.1,
        value: null,
        unit: 'dB'
      },
      'Noise Area': {
        type: 'number',
        min: 0,
        max: Infinity,
        step: 0.1,
        value: null,
        unit: 'dB'
      }
    }
    const cfgLoading = false
    return {
      isConnected,
      cfgDlgVisible,
      osnrValue,
      configs,
      cfgLoading
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
    fmtOsnrValue () {
      return (this.osnrValue !== null) ? this.lodash.round(this.osnrValue, 2).toFixed(2) : 'N/A'
    }
  },
  methods: {
    getOsnrValue () {
      const self = this
      this.$rpcClient.request({
        route: ':instrument:operation:call-method',
        kwargs: {
          field: self.label,
          method_name: 'sweep',
          args: ['SINGLE']
        }
      }).then((res) => {
        setTimeout(() => {
          this.$rpcClient.request({
            route: ':instrument:operation:call-method',
            kwargs: {
              field: self.label,
              method_name: 'get_analysis_data'
            }
          }).then(res => {
            const strList = this.lodash.split(res, ',')
            const strValue = strList[strList.length - 1]
            const numValue = parseFloat(strValue)
            this.osnrValue = numValue
          }).catch(err => {
            this.$alertError(err)
          }, 1000)
        })
      }).catch((err) => {
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
        // initialize OSA @ run
        await self.initOsaForOsnr()
        // get origin configs
        await self.getConfigs()
        // update states after connected
        this.isConnected = true
        this.refreshOn = true
      } catch (err) {
        this.$alertError(err)
        this.disconnect()
      }
    },
    async initOsaForOsnr () {
      const self = this
      const configList = [
        ['sweep', ['STOP']],
        ['analysis_setting', ['WDM', 'TH', '20.00db']],
        ['analysis_setting', ['WDM', 'MDIFF', '3.00DB']],
        ['analysis_setting', ['WDM', 'DMASK', '-999']],
        ['analysis_setting', ['WDM', 'NALGO', 'MFIX']],
        ['analysis_setting', ['WDM', 'FALGO', '5TH']],
        ['set_analysis_cat', ['WDM']],
        ['set_span', [10]],
        ['sweep', ['SINGLE']],
        ['auto_analysis', [true]],
        ['set_auto_ref_level', [true]]
      ]
      for (const i of configList) {
        const methodName = i[0]
        const paramList = i[1]
        await self.$rpcClient.request({
          route: ':instrument:operation:call-method',
          kwargs: {
            field: self.label,
            method_name: methodName,
            args: paramList
          }
        })
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
      let promises = []
      const configList = [
        ['get_frequency', []],
        ['get_setup', ['BWIDTH:RES']],
        ['get_analysis_setting', ['WDM', 'NAREA']],
        ['get_analysis_setting', ['WDM', 'MAREA']]
      ]
      promises = []
      for (const i of configList) {
        promises.push(
          self.$rpcClient.request({
            route: ':instrument:operation:call-method',
            kwargs: {
              field: self.label,
              method_name: i[0],
              args: i[1]
            }
          })
        )
      }
      return Promise.all(promises).then((result) => {
        self.configs['Center Frequency'].value = this.lodash.round(result[0], 4)
        self.configs['Resolution BW'].value = this.lodash.round(parseFloat(result[1]) * 1E+9, 4)
        self.configs['Noise Area'].value = this.lodash.round(parseFloat(result[2]) * 1E+9, 4)
        self.configs['Mask Area'].value = this.lodash.round(parseFloat(result[3]) * 1E+9, 4)
      })
    },
    setConfigs () {
      const self = this
      this.cfgLoading = true
      const centerFreq = this.configs['Center Frequency'].value
      const resBW = this.configs['Resolution BW'].value
      const nArea = this.configs['Noise Area'].value
      const mArea = this.configs['Mask Area'].value
      const configList = [
        ['set_frequency', [centerFreq]],
        ['setup', ['BWIDTH:RES', `${resBW.toFixed(4)}NM`]],
        ['analysis_setting', ['WDM', 'NAREA', `${nArea.toFixed(4)}NM`]],
        ['analysis_setting', ['WDM', 'MAREA', `${mArea.toFixed(4)}NM`]]
      ]
      const promises = []
      for (const i of configList) {
        promises.push(
          self.$rpcClient.request({
            route: ':instrument:operation:call-method',
            kwargs: {
              field: self.label,
              method_name: i[0],
              args: i[1]
            }
          })
        )
      }
      Promise.all(promises).catch(err => {
        this.$alertError(err)
        setTimeout(() => {
          self.cfgLoading = false
        }, 3000)
      }).then(() => {
        setTimeout(() => {
          self.cfgLoading = false
          self.cfgDlgVisible = false
        }, 3000)
      })
    },
    setFrequency (freq) {
      const self = this
      self.refreshOn = false
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
        }).finally(() => {
          setInterval(() => {
            self.refreshOn = true
          }, 3000)
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
  .cfg-dlg-wrapper {
    width: 100%;
    height: 100%;
  }
  .cfg-dlg-wrapper :global(.el-loading-spinner) {
    margin-top: -45px;
  }
  .cfg-dlg-wrapper :global(.el-loading-spinner) i {
    font-size: 24px;
  }
  .cfg-dlg-wrapper :global(.el-loading-spinner) .el-loading-text {
    margin-top: 10px;
  }
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
