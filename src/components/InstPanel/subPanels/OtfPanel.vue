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
      <!-- <span :class="$style['inst-field-title']">Bandwidth</span>
      <el-input-number :disabled="!isConnected" v-model="bwValue" size="small" :min="minBw" :max="maxBw" :step="0.01" @change="setBw"></el-input-number>
      <span :class="$style['inst-field-unit']">nm</span> -->
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
    const bwValue = null
    const maxBw = Infinity
    const minBw = 0
    const configs = {
      'Center Frequency': {
        type: 'number',
        controls: false,
        min: -Infinity,
        max: Infinity,
        value: null,
        unit: 'THz'
      }
    }
    const refreshLock = false
    const refreshOn = false

    return {
      isConnected,
      cfgDlgVisible,
      bwValue,
      maxBw,
      minBw,
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
    }
  },
  methods: {
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
        this.refreshOn = true
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
        'get_frequency'
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
        'max_frequency'
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
        self.configs['Center Frequency'].min = result[1]
        self.configs['Center Frequency'].max = result[2]
      })
    },
    setBw (bw) {
      const self = this
      self.$rpcClient.request({
        route: ':instrument:operation:call-method',
        kwargs: {
          field: self.label,
          method_name: 'set_bandwidth',
          args: [bw]
        }
      }).catch(err => {
        this.$alertError(err)
      })
    },
    setConfigs () {
      const self = this
      const centerFreq = this.configs['Center Frequency'].value
      const configMap = {
        set_frequency: centerFreq
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
  .inst-field-title {
    padding-right: 5px;
    color: $color-text-secondary;
  }
  .inst-field-unit {
    padding-left: 5px;
    color: $color-text-secondary;
  }
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
</style>
