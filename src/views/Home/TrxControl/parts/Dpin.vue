<template>
  <el-container :class="$style.container">
    <el-header :class="$style.header" height="56px">
      <el-button :loading="globalLoading" size="small" type="success" @click="getAllPinStates">Get all pin states</el-button>
    </el-header>
    <el-main :class="$style.main">
      <div :class="$style['state-wrapper']" ref="state-wrapper" @mousewheel="onParamsScroll">
        <div :class="$style['control-line']" v-for="(item, key) in pinState" :key="key">
          <el-checkbox v-model="pinState[key].value" @change="setDpinState(key, $event)">{{key}}</el-checkbox>
          <el-button :loading="pinState[key].loading" size="small" type="success" plain @click="getDpinState(key)">Get</el-button>
        </div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
export default {
  props: {
    trxIdx: Number
  },
  data () {
    const pinKeys = [
      'MCU1_DSP_SPI_CS',
      'MCU1_FLASH_SPI_CS',
      'MCU1_ADC3_SPI_CS',
      'ADC4_SPI_CS',
      'DSP_LINE_LOS',
      'DSP_INTN_0',
      'CLK_SEC',
      'DSP_INTN_1',
      'M_LPWN',
      'M_INT',
      'MCU2_MCU1_INTN_I',
      'MCU1_FLASH_RSTN',
      'MCU1_OUT_RST_N',
      'MCU1_DSP_RSTN',
      'P0V55_DSP_EN',
      'P1V8_DSP_EN',
      'P1V2_DSP_EN',
      'PS_EN',
      'COSA_VOFE_EN',
      'TX_DRIVER_VCC_EN',
      'P0V94_DSP_EN',
      'P0V75_DSP_EN',
      'MCU2_MCU1_INTN_O',
      'M_LPWN_ABC',
      'MCU2_ADC12_SPI_CS1',
      'MCU2_ADC12_SPI_CS2',
      'RX_TIA_BWH',
      'RX_TIA_BWL',
      'RX_TIA_SD',
      'RX_TIA_MC',
      'ITLA_OIF_MS_N',
      'ITLA_OIF_SRQ_N',
      'ITLA_OIF_DIS_N',
      'ITLA_OIF_RST_N',
      'RX_TIA_VCC_XY_EN',
      'COSA_VPD_EN',
      'P6V_EN',
      'COSA_PH_BIAS_EN'
    ]
    const pinState = {}
    for (const k of pinKeys) {
      pinState[k] = {
        value: undefined,
        loading: false
      }
    }
    return {
      pinState
    }
  },
  computed: {
    globalLoading () {
      for (const key in this.pinState) {
        if (this.pinState[key].loading) return true
      }
      return false
    }
  },
  methods: {
    onParamsScroll (event) {
      const deltaY = event.deltaY
      this.$refs['state-wrapper'].scrollLeft += deltaY
    },
    setDpinState (key, state) {
      this.$rpcClient.request({
        route: ':trx:dpin:set',
        args: [this.trxIdx, key, state]
      }).catch(err => {
        this.$alertError(err)
        this.pinState[key].value = !state
      })
    },
    getDpinState (key) {
      this.pinState[key].loading = true
      this.$rpcClient.request({
        route: ':trx:dpin:get',
        args: [this.trxIdx, key]
      }).then((res) => {
        this.pinState[key].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.pinState[key].loading = false
      })
    },
    async getAllPinStates () {
      try {
        for (const key in this.pinState) {
          await this.$rpcClient.request({
            route: ':trx:dpin:get',
            args: [this.trxIdx, key]
          }).then((res) => {
            this.pinState[key].value = res
          })
        }
      } catch (error) {
        this.$alertError(error)
      }
    }
  }
}
</script>

<style module>
  .container:global(.el-container) {
    height: 100%;
  }
  .header:global(.el-header) {
    display: flex;
    align-items: center;
    padding-top: 10px;
  }
  .main:global(.el-main) {
    display: flex;
    flex-direction: column;
    padding: 0;
  }
  .state-wrapper {
    height: 2px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    overflow-x: scroll;
  }
  .control-line {
    width: 280px;
    display: flex;
    justify-content: space-between;
    padding: 6px 18px;
    align-items: center;
  }
</style>
