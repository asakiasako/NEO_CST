<template>
  <div :class="$style.wrapper">
    <el-table
      :class="$style['dac-table']"
      size="small"
      :data="dacData"
      height="100%"
    >
      <el-table-column
        prop="key"
        label="DAC Key"
        width="180"
        fixed
      ></el-table-column>
      <el-table-column
        label="Analog"
        align="center"
        width="100"
      >
        <template slot-scope="scope">
          <div :class="$style['data-wrapper']">
            <div :class="$style['data-display']">{{typeof(dacData[scope.$index].rAval) === 'number' ? dacData[scope.$index].rAval.toPrecision(4) : ''}}</div>
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
            <div :class="$style['data-display']">{{dacData[scope.$index].rDval}}</div>
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
            <div :class="$style['data-display']">{{typeof(dacData[scope.$index].rRval) === 'number' ? dacData[scope.$index].rRval.toPrecision(4) : ''}}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column width="88">
        <!-- eslint-disable-next-line vue/no-unused-vars -->
        <template slot="header" slot-scope="scope">
          <el-button :class="$style['btn-get']" :loading="loading" :disabled="loading" type="success" plain size="small" @click="getAllDac">Get All</el-button>
        </template>
        <template slot-scope="scope">
          <el-button :class="$style['btn-get']" :loading="dacData[scope.$index].loading" :disabled="loading || dacData[scope.$index].loading" type="primary" plain size="small" @click="getDac(scope.$index)">Get</el-button>
        </template>
      </el-table-column>
      <el-table-column
        label="Set analog"
        align="center"
        width="176"
      >
        <template slot-scope="scope">
          <el-input :class="$style['input-set-val']" size="small" placeholder="Analog" v-model="dacData[scope.$index].wAval">
            <el-button slot="append" @click="setDacAval(scope.$index)">Set AVal</el-button>
          </el-input>
        </template>
      </el-table-column>
      <el-table-column
        label="Set digital"
        align="center"
        width="176"
      >
        <template slot-scope="scope">
          <el-input :class="$style['input-set-val']" size="small" placeholder="Digital" v-model="dacData[scope.$index].wDval">
            <el-button slot="append" @click="setDacDval(scope.$index)">Set DVal</el-button>
          </el-input>
        </template>
      </el-table-column>
      <el-table-column
        min-width="1"
      >
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
    const dacData = []
    const loading = false
    return {
      dacData,
      loading
    }
  },
  methods: {
    initDacData () {
      this.$rpcClient.request({
        route: ':trx:dac:list'
      }).then((result) => {
        const dacData = []
        for (const key of result) {
          dacData.push({
            key: key,
            rAval: undefined,
            rDval: undefined,
            rRval: undefined,
            wAval: undefined,
            wDval: undefined,
            loading: false
          })
        }
        this.dacData = dacData
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    promiseGetDac (idx) {
      this.dacData[idx].loading = true
      const dacKey = this.dacData[idx].key
      return this.$rpcClient.request({
        route: ':trx:dac:get',
        args: [this.trxIdx, dacKey, 'all']
      }).then((result) => {
        [this.dacData[idx].rAval, this.dacData[idx].rDval, this.dacData[idx].rRval] = result
      }).finally(() => {
        this.dacData[idx].loading = false
      })
    },
    getDac (idx) {
      this.promiseGetDac(idx).catch((err) => {
        this.$alertError(err)
      })
    },
    async getAllDac () {
      this.loading = true
      try {
        for (const idx in this.dacData) {
          await this.promiseGetDac(idx)
        }
      } catch (err) {
        this.$alertError(err)
      } finally {
        this.loading = false
      }
    },
    checkAval (val) {
      const reg = /^\d+(\.\d+)?$/
      val = val ? val.trim() : ''
      return reg.test(val)
    },
    setDacAval (idx) {
      const value = this.dacData[idx].wAval
      if (this.checkAval(value)) {
        const aval = parseFloat(value)
        const dacKey = this.dacData[idx].key
        this.$rpcClient.request({
          route: ':trx:dac:set',
          args: [this.trxIdx, dacKey, aval, 'a']
        }).catch(err => {
          this.$alertError(err)
        })
      } else {
        this.$alert('Invalid analog value. Should be float or decimal.', 'ERROR', {
          confirmButtonText: 'OK',
          type: 'error'
        })
      }
    },
    checkDval (val) {
      const reg = /^((\d+)|(0(X|x)[\dA-Fa-f]+))$/
      val = val ? val.trim() : ''
      return reg.test(val)
    },
    setDacDval (idx) {
      const value = this.dacData[idx].wDval
      if (this.checkDval(value)) {
        const dval = parseInt(value)
        const dacKey = this.dacData[idx].key
        this.$rpcClient.request({
          route: ':trx:dac:set',
          args: [this.trxIdx, dacKey, dval, 'd']
        }).catch(err => {
          this.$alertError(err)
        })
      } else {
        this.$alert('Invalid digital value. Should be a decimal or heximal integer.', 'ERROR', {
          confirmButtonText: 'OK',
          type: 'error'
        })
      }
    }
  },
  created () {
    this.$bus.$on('select-tab:dac', () => {
      if (this.dacData.length === 0) {
        this.initDacData()
      }
    })
  }
}
</script>

<style lang='scss' module>
  .wrapper {
    height: 100%;
  }
  .dac-table :global(.el-table__fixed) {
    // fix that el-table fixed column covers the horizontal scroll bar
    height: auto !important;
    bottom: 8px;
  }
  .dac-table :global(.el-table__body-wrapper[class*=is-scrolling-none]+.el-table__fixed) {
    // fix that el-table fixed column covers the horizontal scroll bar
    bottom: 0;
  }
  .dac-table :global(.el-table__fixed .el-table__fixed-body-wrapper) {
    // fix that el-table fixed column covers the horizontal scroll bar
    height: auto !important;
    bottom: 0;
  }
  .dac-table :global(.el-table__fixed::before) {
    display: none;
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
  }
  .input-set-val:global(.el-input-group) {
    width: 156px;
  }
  .input-set-val :global(.el-input-group__append button.el-button) {
    padding: 8px;
  }
  .input-set-val :global(.el-input__inner) {
    padding: 0 12px;
  }
</style>
