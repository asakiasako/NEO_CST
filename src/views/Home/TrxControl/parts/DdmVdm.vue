<template>
  <div :class="$style.wrapper">
    <el-form :class="$style['form-monitors']" v-model="monitorData" label-position="left" label-width="180px">
      <el-form-item v-for="(item, key) in monitorData" :key="key" :label="item.name">
        <div :class="$style['monitor-line']">
          <div :class="$style['monitor-display']">
            <span :class="$style['monitor-value']">{{item.value}}</span>
            <span :class="$style['monitor-unit']">{{item.unit}}</span>
          </div>
          <el-input-number :class="$style['input-period']" v-if="'period' in item" placeholder="period (s)" :max="5" :min="0" :controls="false" v-model="item.period"></el-input-number>
          <el-button :class="$style['btn-get']" :loading="item.loading" type="primary" plain @click="item.method">Get</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  props: {
    trxIdx: Number
  },
  data () {
    const monitorData = {
      temperature: {
        name: 'Module Temperature',
        value: 'N/A',
        unit: '°C',
        method: this.getTemperature,
        loading: false
      },
      vcc: {
        name: 'Module Supply Voltage',
        value: 'N/A',
        unit: 'V',
        method: this.getVcc,
        loading: false
      },
      'laser-temperature': {
        name: 'Laser Temperature',
        value: 'N/A',
        unit: '°C',
        method: this.getLaserTemperature,
        loading: false
      },
      'Media Pre-FEC Average': {
        name: 'Media Pre-FEC Average',
        value: 'N/A',
        unit: '',
        method: this.getVdmMediaPre,
        loading: false
      },
      'Media Post-FEC Average': {
        name: 'Media Post-FEC Average',
        value: 'N/A',
        unit: '',
        method: this.getVdmMediaPost,
        loading: false
      },
      'Host Pre-FEC Average': {
        name: 'Host Pre-FEC Average',
        value: 'N/A',
        unit: '',
        method: this.getVdmHostPre,
        loading: false
      },
      'Host Post-FEC Average': {
        name: 'Host Post-FEC Average',
        value: 'N/A',
        unit: '',
        method: this.getVdmHostPost,
        loading: false
      },
      CD: {
        name: 'CD',
        value: 'N/A',
        unit: 'ps/nm',
        method: this.getVdmCD,
        loading: false
      },
      DGD: {
        name: 'DGD',
        value: 'N/A',
        unit: 'ps/nm',
        method: this.getVdmDGD,
        loading: false
      },
      PDL: {
        name: 'PDL',
        value: 'N/A',
        unit: 'ps/nm',
        method: this.getVdmPDL,
        loading: false
      },
      CFO: {
        name: 'CFO',
        value: 'N/A',
        unit: 'MHz',
        method: this.getVdmCFO,
        loading: false
      },
      EVM: {
        name: 'EVM',
        value: 'N/A',
        unit: '',
        method: this.getVdmEVM,
        loading: false
      },
      OSNR: {
        name: 'OSNR',
        value: 'N/A',
        unit: 'dB',
        method: this.getVdmOSNR,
        loading: false
      },
      ESNR: {
        name: 'ESNR',
        value: 'N/A',
        unit: '',
        method: this.getVdmESNR,
        loading: false
      },
      'Tx Power': {
        name: 'Tx Power',
        value: 'N/A',
        unit: 'dBm',
        method: this.getVdmTxP,
        loading: false
      },
      'Rx Total Power': {
        name: 'Rx Total Power',
        value: 'N/A',
        unit: 'dBm',
        method: this.getVdmRxTotal,
        loading: false
      },
      'Rx Signal Power': {
        name: 'Rx Signal Power',
        value: 'N/A',
        unit: 'dBm',
        method: this.getVdmRxSignal,
        loading: false
      }
    }
    return {
      monitorData
    }
  },
  methods: {
    formatValue (val, format) {
      if (typeof val === 'undefined' || val === null) return 'N/A'
      if (format === 'decimal') return val.toFixed(2)
      if (format === 'exponential') return val.toExponential(2)
      this.$alert('Invalid format number.', 'ERROR', {
        confirmButtonText: 'OK',
        type: 'error'
      })
    },
    getTemperature () {
      this.monitorData.temperature.loading = true
      this.$rpcClient.request({
        route: ':trx:monitor:temperature',
        args: [this.trxIdx]
      }).then((result) => {
        this.monitorData.temperature.value = this.formatValue(result, 'decimal')
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.monitorData.temperature.loading = false
      })
    },
    getLaserTemperature () {
      this.monitorData['laser-temperature'].loading = true
      this.$rpcClient.request({
        route: ':trx:monitor:laser-temperature',
        args: [this.trxIdx]
      }).then((result) => {
        this.monitorData['laser-temperature'].value = this.formatValue(result, 'decimal')
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.monitorData['laser-temperature'].loading = false
      })
    },
    getVcc () {
      this.monitorData.vcc.loading = true
      this.$rpcClient.request({
        route: ':trx:monitor:vcc',
        args: [this.trxIdx]
      }).then((result) => {
        this.monitorData.vcc.value = this.formatValue(result, 'decimal')
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.monitorData.vcc.loading = false
      })
    },
    getVdm (key, exponential) {
      this.monitorData[key].loading = true
      this.$rpcClient.request({
        route: ':trx:monitor:vdm',
        args: [this.trxIdx, key]
      }).then(result => {
        if (exponential) {
          this.monitorData[key].value = this.formatValue(result, 'exponential')
        } else {
          this.monitorData[key].value = this.formatValue(result, 'decimal')
        }
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.monitorData[key].loading = false
      })
    },
    getVdmMediaPre () {
      this.getVdm('Media Pre-FEC Average', true)
    },
    getVdmMediaPost () {
      this.getVdm('Media Post-FEC Average', true)
    },
    getVdmHostPre () {
      this.getVdm('Host Pre-FEC Average', true)
    },
    getVdmHostPost () {
      this.getVdm('Host Post-FEC Average', true)
    },
    getVdmCD () {
      this.getVdm('CD')
    },
    getVdmDGD () {
      this.getVdm('DGD')
    },
    getVdmPDL () {
      this.getVdm('PDL')
    },
    getVdmCFO () {
      this.getVdm('CFO')
    },
    getVdmEVM () {
      this.getVdm('EVM')
    },
    getVdmOSNR () {
      this.getVdm('OSNR')
    },
    getVdmESNR () {
      this.getVdm('ESNR')
    },
    getVdmTxP () {
      this.getVdm('Tx Power')
    },
    getVdmRxTotal () {
      this.getVdm('Rx Total Power')
    },
    getVdmRxSignal () {
      this.getVdm('Rx Signal Power')
    }
  }
}
</script>

<style lang='scss' module>
  .wrapper {
    padding: 20px 40px;
  }
  .monitor-line {
    display: flex;
  }
  .monitor-display {
    width: 220px;
    margin-right: 10px;
    padding: 0 12px;
    border-radius: 4px;
    font-size: 24px;
    color: $color-text-regular;
    background: $background-color-base;
    border: 1px solid $border-color-light;
    display: flex;
    justify-content: space-between;
  }
  .monitor-unit {
    color: $color-text-secondary;
  }
  .btn-get {
    width: 80px;
    padding-left: 0;
    padding-right: 0;
  }
  .input-period {
    margin-right: 8px;
  }
  .input-period :global(.el-input .el-input__inner) {
    height: 42px;
  }
</style>
