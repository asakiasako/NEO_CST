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
      <div :class="$style['cfg-item-value']">
        <div>
          <el-input-number :disabled="!isConnected" v-model="attValue" size="small" :min="thWithOffset[0]" :max="thWithOffset[1]" :step="0.1" @change="setAttValue"></el-input-number>
          <span :class="$style['inst-field-unit']">dB</span>
        </div>
        <div>
          <span :class="$style['panel-label']">Output</span>
          <el-switch :disabled="!isConnected" active-color="#13ce66" v-model="enabled" @change="setEnable"></el-switch>
        </div>
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
    let isConnected = false
    let cfgDlgVisible = false
    let attValue = null
    let maxAtt = Infinity
    let enabled = false
    let configs = {
      'Center Frequency': {
        type: 'number',
        controls: false,
        min: -Infinity,
        max: Infinity,
        value: null,
        unit: 'THz'
      },
      'Att Offset': {
        type: 'number',
        min: -Infinity,
        max: Infinity,
        step: 0.1,
        value: null,
        unit: 'dB'
      }
    }
    return {
      isConnected,
      cfgDlgVisible,
      attValue,
      maxAtt,
      enabled,
      configs
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
    thWithOffset () {
      let offset = this.configs['Att Offset'].value
      if (!offset) {
        offset = 0
      }
      return [0 + offset, this.maxAtt + offset]
    }
  },
  methods: {
    getAttStatus () {
      let self = this
      let promises = []
      let methodKeys = [
        'get_att',
        'is_enabled'
      ]
      for (let i of methodKeys) {
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
      return Promise.all(promises).then((result) => {
        self.attValue = this.lodash.round(result[0], 3)
        self.enabled = result[1]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    setAttValue (val) {
      let self = this
      this.$rpcClient.request({
        route: ':instrument:operation:call-method',
        kwargs: {
          field: self.label,
          method_name: 'set_att',
          args: [val]
        }
      }).catch(err => {
        this.$alertError(err)
      })
    },
    setEnable (isEn) {
      let self = this
      this.$rpcClient.request({
        route: ':instrument:operation:call-method',
        kwargs: {
          field: self.label,
          method_name: 'enable',
          args: [isEn]
        }
      }).then(res => {
        // set delay to avoid incorrect att value after enable
        setTimeout(() => {
          self.getAttStatus().catch(err => {
            this.$alertError(err)
          })
        }, 50)
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
      let self = this
      try {
        // check connection
        let connected = await this.$rpcClient.request({
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
        await self.getAttStatus()
        // update states after connected
        this.isConnected = true
        this.refreshOn = true
      } catch (err) {
        this.$alertError(err)
        this.disconnect()
      }
    },
    disconnect () {
      let self = this
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
      let self = this
      let promises = []
      let cfgList = [
        'get_frequency',
        'get_offset'
      ]
      for (let i of cfgList) {
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
      let attrList = [
        'min_frequency',
        'max_frequency',
        'min_offset',
        'max_offset'
      ]
      for (let i of attrList) {
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
        self.configs['Att Offset'].value = this.lodash.round(result[1], 3)
        self.configs['Center Frequency'].min = result[2]
        self.configs['Center Frequency'].max = result[3]
        self.configs['Att Offset'].min = result[4]
        self.configs['Att Offset'].max = result[5]
      })
    },
    setConfigs () {
      let self = this
      let centerFreq = this.configs['Center Frequency'].value
      let offset = this.configs['Att Offset'].value
      let configMap = {
        'set_frequency': centerFreq,
        'set_offset': offset
      }
      let promises = []
      for (let k in configMap) {
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
        self.getAttStatus().catch(err => {
          this.$alertError(err)
        })
        self.cfgDlgVisible = false
      }).catch(err => {
        this.$alertError(err)
      })
    },
    setFrequency (freq) {
      let self = this
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
    let self = this
    this.$bus.$on('inst-panel:connect-all', self.connect)
    this.$bus.$on('inst-panel:disconnect-all', self.disconnect)
    this.$bus.$on('inst-panel:set-all-frequency', self.setFrequency)
  },
  beforeDestroy () {
    let self = this
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
  .panel-label {
    display: inline-block;
    padding-right: 5px;
    color: $color-text-secondary;
  }
  .cfg-item-value {
    display: flex;
    align-items: center;
    justify-content: space-between
  }
  .inst-field-unit {
    padding-left: 5px;
    color: $color-text-secondary;
  }
</stylesc>
