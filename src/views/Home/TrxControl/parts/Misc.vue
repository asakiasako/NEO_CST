<template>
  <div :class="$style.wrapper">
    <el-card :class="$style['operation-card']">
      <div slot="header">Power Supply</div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Setting Vcc</div>
        <el-input-number size="small" :controls="false" :precision="3" v-model="evbData.setVolt"></el-input-number>
        <el-button size="small" type="success" plain @click="getSettingVoltage">Get</el-button>
        <el-button size="small" type="danger" plain @click="setVoltage">Set</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Monitored Vcc</div>
        <div :class="$style['line-display']">{{evbData.monitoredVolt || '- - - - -'}}</div>
        <el-button size="small" type="success" plain @click="getMonitoredVoltage">Get</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Supply Current</div>
        <div :class="$style['line-display']">{{evbData.current || '- - - - -'}}</div>
        <el-button size="small" type="success" plain @click="getCurrent">Get</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Consumption</div>
        <div :class="$style['line-display']">{{evbData.consumption || '- - - - -'}}</div>
        <el-button size="small" type="success" plain @click="getConsumption">Get</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Fan Speed</div>
        <el-input-number size="small" :controls="false" :precision="0" :min="0" :max="100" v-model="evbData.fanSpeed"></el-input-number>
        <el-button size="small" type="danger" plain @click="setFanSpeed">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">DataPath Control</div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">DataPathState</div>
        <div :class="$style['line-display']">{{dataPathData.DataPathState || '- - - - -'}}</div>
        <el-button size="small" type="success" plain @click="getDataPathState">Get</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">DataPathDeinit</div>
        <el-switch size="small" v-model="dataPathData.DataPathDeinit" @change="setDataPathDeinit"></el-switch>
        <el-button size="small" type="success" plain @click="getDataPathDeinit">Get</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Tx1 Disable</div>
        <el-switch size="small" v-model="dataPathData.TxDisable" @change="setTxDisable"></el-switch>
        <el-button size="small" type="success" plain @click="getTxDisable">Get</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">Tunable Laser Control & Status</div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Channel Number</div>
        <el-input-number size="small" :controls="false" :precision="0" v-model="laserControlData.ChannelNumber"></el-input-number>
        <el-button size="small" type="success" plain @click="getChannelNumber">Get</el-button>
        <el-button size="small" type="danger" plain @click="setChannelNumber">Set</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Grid</div>
        <el-select v-model="laserControlData.GridSpacingIdx" size="small">
          <el-option v-for="(item, index) in GRID_SPACING_MAPPING" :key="index" :value="parseInt(index)" :label="item"></el-option>
        </el-select>
        <el-button size="small" type="success" plain @click="getGridSpacing">Get</el-button>
        <el-button size="small" type="danger" plain @click="setGridSpacing">Set</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Fine Tune Enable</div>
        <el-switch size="small" v-model="laserControlData.FineTuneEnable" @change="setFineTuneEnable"></el-switch>
        <el-button size="small" type="success" plain @click="getFineTuneEnable">Get</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Fine Tune (GHz)</div>
        <el-input-number size="small" :controls="false" :precision="3" v-model="laserControlData.FineTuneGHz"></el-input-number>
        <el-button size="small" type="danger" plain @click="setFineTuneFrequency">Set</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['line-label']">Current Laser Freq</div>
        <div :class="$style['line-display']">{{laserControlData.CurrentLaserFreq || '- - - - -'}}</div>
        <el-button size="small" type="success" plain @click="getCurrentLaserFrequency">Get</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  props: {
    trxIdx: Number
  },
  data () {
    const evbData = {
      setVolt: undefined,
      monitoredVolt: undefined,
      current: undefined,
      consumption: undefined,
      fanSpeed: undefined
    }
    const dataPathData = {
      DataPathState: undefined,
      DataPathDeinit: undefined,
      TxDisable: undefined
    }
    const laserControlData = {
      ChannelNumber: undefined,
      GridSpacingIdx: undefined,
      FineTuneEnable: undefined,
      FineTuneGHz: undefined,
      CurrentLaserFreq: undefined
    }
    const GRID_SPACING_MAPPING = {
      0: 3.125,
      1: 6.25,
      2: 12.5,
      3: 25,
      4: 50,
      5: 100,
      6: 75,
      7: 33
    }
    return {
      evbData,
      dataPathData,
      laserControlData,
      GRID_SPACING_MAPPING
    }
  },
  methods: {
    getSettingVoltage () {
      this.$rpcClient.request({
        route: ':trx:host-board:get-setting-voltage',
        args: [this.trxIdx]
      }).then((res) => {
        this.evbData.setVolt = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setVoltage () {
      this.$rpcClient.request({
        route: ':trx:host-board:set-voltage',
        args: [this.trxIdx, this.evbData.setVolt]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getMonitoredVoltage () {
      this.$rpcClient.request({
        route: ':trx:host-board:get-monitored-voltage',
        args: [this.trxIdx]
      }).then((res) => {
        this.evbData.monitoredVolt = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getCurrent () {
      this.$rpcClient.request({
        route: ':trx:host-board:get-current',
        args: [this.trxIdx]
      }).then((res) => {
        this.evbData.current = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getConsumption () {
      this.$rpcClient.request({
        route: ':trx:host-board:get-consumption',
        args: [this.trxIdx]
      }).then((res) => {
        this.evbData.consumption = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setFanSpeed () {
      this.$rpcClient.request({
        route: ':trx:host-board:set-fan-speed',
        args: [this.trxIdx, this.evbData.fanSpeed]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getDataPathState () {
      this.$rpcClient.request({
        route: ':trx:get-data-path-state',
        args: [this.trxIdx]
      }).then((res) => {
        this.dataPathData.DataPathState = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getDataPathDeinit () {
      this.$rpcClient.request({
        route: ':trx:data-path:get-deinit',
        args: [this.trxIdx]
      }).then((res) => {
        this.dataPathData.DataPathDeinit = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setDataPathDeinit () {
      this.$rpcClient.request({
        route: ':trx:data-path:set-deinit',
        args: [this.trxIdx, this.dataPathData.DataPathDeinit]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getTxDisable () {
      this.$rpcClient.request({
        route: ':trx:data-path:get-tx-disable',
        args: [this.trxIdx]
      }).then((res) => {
        this.dataPathData.TxDisable = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setTxDisable () {
      this.$rpcClient.request({
        route: ':trx:data-path:set-tx-disable',
        args: [this.trxIdx, this.dataPathData.TxDisable]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getChannelNumber () {
      this.$rpcClient.request({
        route: ':trx:laser-control:get-channel-number',
        args: [this.trxIdx]
      }).then((res) => {
        this.laserControlData.ChannelNumber = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setChannelNumber () {
      this.$rpcClient.request({
        route: ':trx:laser-control:set-channel-number',
        args: [this.trxIdx, this.laserControlData.ChannelNumber]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getGridSpacing () {
      this.$rpcClient.request({
        route: ':trx:laser-control:get-grid-spacing',
        args: [this.trxIdx]
      }).then((res) => {
        this.laserControlData.GridSpacingIdx = res.toSting() in this.GRID_SPACING_MAPPING ? res : undefined
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setGridSpacing () {
      this.$rpcClient.request({
        route: ':trx:laser-control:set-grid-spacing',
        args: [this.trxIdx, this.laserControlData.GridSpacingIdx]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getFineTuneEnable () {
      this.$rpcClient.request({
        route: ':trx:laser-control:get-fine-tune-enable',
        args: [this.trxIdx]
      }).then((res) => {
        this.laserControlData.FineTuneEnable = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setFineTuneEnable () {
      this.$rpcClient.request({
        route: ':trx:laser-control:set-fine-tune-enable',
        args: [this.trxIdx, this.laserControlData.FineTuneEnable]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getFineTuneFrequency () {
      this.$rpcClient.request({
        route: ':trx:laser-control:get-fine-tune-frequency',
        args: [this.trxIdx]
      }).then((res) => {
        this.laserControlData.FineTuneGHz = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setFineTuneFrequency () {
      this.$rpcClient.request({
        route: ':trx:laser-control:set-fine-tune-frequency',
        args: [this.trxIdx, this.laserControlData.FineTuneGHz]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getCurrentLaserFrequency () {
      this.$rpcClient.request({
        route: ':trx:laser-control:get-current-laser-frequency',
        args: [this.trxIdx]
      }).then((res) => {
        this.laserControlData.CurrentLaserFreq = res
      }).catch((err) => {
        this.$alertError(err)
      })
    }
  }
}
</script>

<style lang="scss" module>
  .wrapper {
    display: flex;
    flex-wrap: wrap;
  }
  .operation-card:global(.el-card.is-always-shadow) {
    width: 360px;
    margin: 8px;
    color: $color-text-regular;
    box-shadow: 0 2px 5px 0 rgba(0,0,0,.05);
  }
  .operation-card :global(.el-card__header) {
    padding: 12px 20px;
  }
  .operation-card :global(.el-card__body) {
    padding-top: 15px;
    padding-bottom: 0;
  }
  .line-wrapper {
    display: flex;
    align-items: center;
    margin: 10px 0;
  }
  .line-label {
    width: 120px;
  }
  .line-wrapper :global(.el-input-number) {
    width: 72px;
  }
  .line-wrapper > *:not(:last-child) {
    margin-right: 8px;
  }
  .card-footer {
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 15px;
  }
</style>
