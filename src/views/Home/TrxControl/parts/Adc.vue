/* eslint-disable vue/no-unused-vars */
<template>
  <div :class="$style.wrapper">
    <el-table
      size="small"
      :data="adcData"
      style="width: 100%;"
      height="100%"
    >
      <el-table-column
        prop="key"
        label="ADC Key"
        width="180"
      ></el-table-column>
      <el-table-column
        label="Analog"
        align="center"
        width="100"
      >
        <template slot-scope="scope">
          <div :class="$style['data-wrapper']">
            <div :class="$style['data-display']">{{typeof(adcData[scope.$index].rAval) === 'number' ? adcData[scope.$index].rAval.toPrecision(4) : ''}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="Digital"
        align="center"
        width="100"
      >
        <template slot-scope="scope">
          <div :class="$style['data-wrapper']">
            <div :class="$style['data-display']">{{adcData[scope.$index].rDval}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="Raw analog"
        align="center"
        width="100"
      >
        <template slot-scope="scope">
          <div :class="$style['data-wrapper']">
            <div :class="$style['data-display']">{{typeof(adcData[scope.$index].rRval) === 'number' ? adcData[scope.$index].rRval.toPrecision(4) : ''}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column min-width="100">
        <!-- eslint-disable-next-line vue/no-unused-vars -->
        <template slot="header" slot-scope="scope">
          <el-button :class="$style['btn-get']" :loading="loading" :disabled="loading" type="success" plain size="small" @click="getAllAdc">Get All</el-button>
        </template>
        <template slot-scope="scope">
          <el-button :class="$style['btn-get']" :loading="adcData[scope.$index].loading" :disabled="loading || adcData[scope.$index].loading" type="primary" plain size="small" @click="getAdc(scope.$index)">Get</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  props: {
    trxIdx: Number
  },
  data () {
    const adcData = []
    const loading = false
    return {
      adcData,
      loading
    }
  },
  methods: {
    initAdcData () {
      this.$rpcClient.request({
        route: ':trx:adc:list'
      }).then((result) => {
        const adcData = []
        for (const key of result) {
          adcData.push({
            key: key,
            rAval: undefined,
            rDval: undefined,
            rRval: undefined,
            loading: false
          })
        }
        this.adcData = adcData
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    promiseGetAdc (idx) {
      this.adcData[idx].loading = true
      const adcKey = this.adcData[idx].key
      return this.$rpcClient.request({
        route: ':trx:adc:get',
        args: [this.trxIdx, adcKey, 'all']
      }).then((result) => {
        [this.adcData[idx].rAval, this.adcData[idx].rDval, this.adcData[idx].rRval] = result
      }).finally(() => {
        this.adcData[idx].loading = false
      })
    },
    getAdc (idx) {
      this.promiseGetAdc(idx).catch((err) => {
        this.$alertError(err)
      })
    },
    async getAllAdc () {
      this.loading = true
      try {
        for (const idx in this.adcData) {
          await this.promiseGetAdc(idx)
        }
      } catch (err) {
        this.$alertError(err)
      } finally {
        this.loading = false
      }
    }
  },
  created () {
    this.$bus.$on('select-tab:adc', () => {
      if (this.adcData.length === 0) {
        this.initAdcData()
      }
    })
  }
}
</script>

<style lang='scss' module>
  .wrapper {
    height: 100%;
  }
  .wrapper :global(.el-table::before) {
    height: 0;
  }
  .btn-get:global(.el-button--small) {
    width: 68px;
    padding: 0;
    height: 32px;
  }
  .data-wrapper {
    display: flex;
    align-items: center;
    height: 32px;
    border: 1px solid;
    color: $color-text-secondary;
    border-color: $border-color-base;
    border-radius: 3px;
    overflow: hidden;
  }
  .data-display {
    text-align: center;
    flex-grow: 1;
    color: $color-text-regular;
    width: 1px;
    height: 30px;
    line-height: 30px;
    background: #FFF;
    padding: 0 5px;
    white-space: nowrap;
    overflow: auto;
  }
  .data-display:global(::-webkit-scrollbar) {
    display: none !important;
    width: 0px;
    height: 0px;
  }
</style>
