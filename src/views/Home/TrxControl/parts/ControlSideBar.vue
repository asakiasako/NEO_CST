<template>
  <div>
    <div class="aside-label"><span>TRx Connect</span></div>
    <div id="dut-port-address">
      <div class="label-input">
        <span class="label">TRX</span>
        <el-select :disabled="isChecking" :value="trxIdx" @change="onTrxIdxChange" size="small" placeholder="IP Address">
          <el-option v-for="info in trxOptions" :key="info[1]" :label="info[0]" :value="info[1]"></el-option>
        </el-select>
      </div>
      <el-button :loading="isChecking" size="small" type="primary" @click="checkConnection">Check Connection</el-button>
    </div>
    <div class="aside-label"><span>Password Control</span></div>
    <div id="cdb-password">
      <el-button plain type="success" size="small" @click="onWriteCdbPassword">Write CDB Password</el-button>
    </div>
    <div class="aside-label"><span>Page & Bank Select</span></div>
    <div class="label-input">
      <span class="label">Bank</span>
      <el-input class="data-input hex-number-input" size="small" :maxlength="2" v-model="pageSel.regBank">
        <template slot="prepend">0x</template>
        <div class="spin" slot="append">
          <div :disabled="parseInt(`0x${pageSel.regBank}`) >= 0xFF" @click="onHexSpin('add', 'regBank')"><i class="el-icon-arrow-up"></i></div>
          <div :disabled="parseInt(`0x${pageSel.regBank}`) <= 0" @click="onHexSpin('minus', 'regBank')"><i class="el-icon-arrow-down"></i></div>
        </div>
      </el-input>
    </div>
    <div class="label-input">
      <span class="label">Page</span>
      <el-input class="data-input hex-number-input" size="small" :maxlength="2" v-model="pageSel.regPage">
        <template slot="prepend">0x</template>
        <div class="spin" slot="append">
          <div :disabled="parseInt(`0x${pageSel.regPage}`) >= 0xFF" @click="onHexSpin('add', 'regPage')"><i class="el-icon-arrow-up"></i></div>
          <div :disabled="parseInt(`0x${pageSel.regPage}`) <= 0" @click="onHexSpin('minus', 'regPage')"><i class="el-icon-arrow-down"></i></div>
        </div>
      </el-input>
    </div>
    <div class="aside-label"><span>Read TWI Reg</span></div>
    <div class="label-input">
      <span class="label">Address</span>
      <el-input-number
        class="data-input" size="small" :min="0" :max="255" controls-position="right"
        v-model="readSection.address"
      >
      </el-input-number>
    </div>
    <div class="label-input">
      <span class="label">Data(Hex)</span>
      <div class="data-show">{{readSection.dataHex}}</div>
    </div>
    <div class="label-input">
      <span class="label">Data(Bin)</span>
      <div class="data-show">{{readSection.dataBin}}</div>
    </div>
    <el-button class="all-width-button" size="small" type="primary" plain @click="onReadTWI">Read TWI Register</el-button>
    <div class="aside-label"><span>Write TWI Reg</span></div>
    <div class="label-input">
      <span class="label">Address</span>
      <el-input-number
        class="data-input" size="small" :min="0" :max="255" controls-position="right"
        v-model="writeSection.address"
      >
      </el-input-number>
    </div>
    <div class="label-input">
      <span class="label">Data(Hex)</span>
      <el-input class="data-input" size="small" :maxlength="2" v-model="writeSection.dataHex">
        <template slot="prepend">0x</template>
      </el-input>
    </div>
    <el-button class="all-width-button" size="small" type="primary" plain @click="onWriteTWI">Write TWI Register</el-button>
  </div>
</template>

<script>
import { readTWIRegister, writeTWIRegister, selectTWIRegisterBankPage } from '@/utils/dut_control'

export default {
  props: {
    trxIdx: Number
  },
  data () {
    const trxList = []
    const pageSel = {
      regPage: '00',
      regBank: '00'
    }
    const isChecking = false
    const readSection = {
      address: 0,
      dataHex: '',
      dataBin: ''
    }
    const writeSection = {
      address: 0,
      dataHex: ''
    }
    return {
      trxList,
      isChecking,
      pageSel,
      readSection,
      writeSection
    }
  },
  computed: {
    trxOptions () {
      const options = []
      const trxList = this.trxList
      for (const i in trxList) {
        options.push([`TRX${parseInt(i) + 1}@${trxList[i].address}`, parseInt(i) + 1])
      }
      return options
    }
  },
  methods: {
    onTrxIdxChange (val) {
      this.$emit('update:trx-idx', val)
    },
    getTrxList () {
      this.$rpcClient.request({
        route: ':config:get',
        args: [':transceiver:list']
      }).then((result) => {
        if (result) {
          this.trxList = result
        }
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    checkConnection () {
      const self = this
      if (!this.trxIdx) {
        this.$alert('Please select a transceiver.', 'Check Connection', {
          confirmButtonText: 'OK',
          type: 'error'
        })
      } else {
        this.isChecking = true
        self.$rpcClient.request({
          route: ':trx:check-connection',
          args: [this.trxIdx]
        }).then(res => {
          this.$alert(`Check TRx connection ${res ? 'SUCCESS' : 'FAIL'}`, 'Check Connection', {
            confirmButtonText: 'OK',
            type: res ? 'success' : 'error'
          })
        }).catch(err => {
          self.$alertError(err)
        }).finally(() => {
          this.isChecking = false
        })
      }
    },
    onWriteCdbPassword () {
      this.$rpcClient.request({
        route: ':trx:write-cdb-password',
        args: [this.trxIdx]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    onHexSpin (addOrMinus, target) {
      const reg = /^[0-9a-fA-F]+$/
      if (!reg.test(this.pageSel[target])) {
        return
      }
      let value = parseInt(`0x${this.pageSel[target]}`)
      if (addOrMinus === 'add') {
        if (value < 0xFF) {
          value += 1
          this.pageSel[target] = this.lodash.toUpper(`${this.lodash.padStart(value.toString(16), 2, '0')}`)
        }
      }
      if (addOrMinus === 'minus') {
        if (value > 0) {
          value -= 1
          this.pageSel[target] = this.lodash.toUpper(`${this.lodash.padStart(value.toString(16), 2, '0')}`)
        }
      }
    },
    async onReadTWI () {
      const bank = parseInt(`0x${this.pageSel.regBank}`)
      const page = parseInt(`0x${this.pageSel.regPage}`)
      const address = this.readSection.address
      try {
        await selectTWIRegisterBankPage(this.trxIdx, bank, page)
        const res = await readTWIRegister(this.trxIdx, address)
        this.readSection.dataBin = this.lodash.padStart(res.toString(2), 8, '0').replace(/(\d)(?=(\d{4})+$)/g, '$1 ')
        this.readSection.dataHex = `0x${this.lodash.toUpper(this.lodash.padStart(res.toString(16), 2, '0'))}`
      } catch (err) {
        this.$alertError(err)
      }
    },
    async onWriteTWI () {
      const bank = parseInt(`0x${this.pageSel.regBank}`)
      const page = parseInt(`0x${this.pageSel.regPage}`)
      const address = this.writeSection.address
      const data = parseInt(`0x${this.writeSection.dataHex}`)
      if (!this.checkHexString(this.writeSection.dataHex)) {
        return
      }
      try {
        await selectTWIRegisterBankPage(this.trxIdx, bank, page)
        await writeTWIRegister(this.trxIdx, address, data)
      } catch (err) {
        this.$alertError(err)
      }
    },
    checkHexString (hexString) {
      const self = this
      // 2-bytes needed
      if (hexString.length !== 2) {
        self.$alert('TWI Address/Data has 1 byte (consists with 2 hex numbers)', 'Format Error', {
          confirmButtonText: 'OK'
        })
        return false
      }
      const reg = /^[0-9A-Fa-f]{2}$/
      if (!reg.test(hexString)) {
        self.$alert('Not a valid hex number. Hex number consists with 0-9 & A-F.', 'Format Error', {
          confirmButtonText: 'OK'
        })
        return false
      }
      return true
    }
  },
  activated () {
    this.getTrxList()
  }
}
</script>

<style lang="scss" scoped>
  .aside-label {
    margin: 18px 0;
    color: $color-text-secondary;
    text-align: center;
    position: relative;
    width: 100%;
  }
  .aside-label:first-child {
    margin-top: 0;
  }
  .aside-label span {
    font-size: 13px;
    padding: 0 12px;
    background: $color-white;
    position: relative;
    z-index: 2;
  }
  .aside-label:after {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    width: 100%;
    border-bottom: 1px solid $border-color-light;
    z-index: 1;
  }
  .el-input--small {
    font-size: 12px;
  }
  #dut-port-address {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 16px;
  }
  #dut-port-address ::v-deep .el-button {
    margin-left: 10px;
    padding: 9px 12px;
    width: 85px;
    flex-shrink: 0;
  }
  #dut-port-address ::v-deep .el-input--small {
    font-size: 12px;
  }
  #cdb-password {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
  }
  #cdb-password ::v-deep .el-button {
    flex-grow: 1;
  }
  #cdb-password i {
    font-size: 16px;
    padding: 6px;
    margin-left: 4px;
    color: $color-text-secondary;
    cursor: pointer;
  }
  .data-input ::v-deep .el-input-group__prepend {
    padding-right: 8px;
    padding-left: 12px;
  }
  .el-input ::v-deep .el-input-group__append {
    padding: 0;
  }
  .hex-number-input ::v-deep input {
    text-align: center;
  }
  .spin {
    padding: 0;
  }
  .spin div {
    font-size: 13px;
    color: $color-text-regular;
    line-height: 15px;
    height: 15px;
    width: 32px;
    text-align: center;
    border-top: 1px solid #dcdfe6;
    cursor: pointer;
  }
  .spin div i {
    transform: scale(0.8);
  }
  .spin div[disabled] {
    color: $color-text-placeholder !important;
    cursor: not-allowed;
  }
  .spin div:hover {
    color: $color-primary;
  }
  .spin div:first-child {
    border: none;
  }
  .data-show {
    width: 150px;
    height: 32px;
    border: 1px solid $border-color-base;
    border-radius: 4px;
    background-color: $background-color-base;
    font-size: 12px;
    line-height: 30px;
    padding: 0 15px;
    cursor: text;
    color: $color-text-regular;
    white-space: nowrap;
  }
  .label-input {
    display: flex;
    align-items: center;
    margin-bottom: 9px;
  }
  .label {
    font-size: 12px;
    width: 60px;
    flex-grow: 1;
    color: $color-text-secondary;
  }
  .label-input .el-input {
    width: 150px;
  }
  .label-input .data-input {
    width: 150px;
  }
  #dut-port-address .el-button {
    width: 100%;
    margin-left: 0;
  }
  .all-width-button {
    width: 100%;
  }
</style>
