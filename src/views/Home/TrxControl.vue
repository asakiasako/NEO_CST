<template>
  <el-container>
    <el-main>
      <el-tabs class="main-top-tab" type="border-card" :before-leave="beforeLeave" v-model="currentTab" @tab-click="emitSelectTab">
        <el-tab-pane label="State Machine" name="state-machine">
          <state-machine :trx-idx="trxIdx"></state-machine>
        </el-tab-pane>
        <el-tab-pane label="ADC" name="adc">
          <adc :trx-idx="trxIdx"></adc>
        </el-tab-pane>
        <el-tab-pane label="DAC" name="dac">
          <dac :trx-idx="trxIdx"></dac>
        </el-tab-pane>
        <el-tab-pane label="DDM/VDM" name="ddm-vdm">
          <ddm-vdm :trx-idx="trxIdx"></ddm-vdm>
        </el-tab-pane>
        <el-tab-pane label="ABC" name="abc">
          <abc :trx-idx="trxIdx"></abc>
        </el-tab-pane>
        <el-tab-pane label="DSP" name="dsp">
          <dsp :trx-idx="trxIdx"></dsp>
        </el-tab-pane>
        <el-tab-pane label="Misc" name="misc">
          <misc :trx-idx="trxIdx"></misc>
        </el-tab-pane>
        <el-tab-pane label="Dpin" name="dpin">
          <dpin :trx-idx="trxIdx"></dpin>
        </el-tab-pane>
      </el-tabs>
    </el-main>
    <el-aside width="246px">
      <control-side-bar :trx-idx.sync="trxIdx"></control-side-bar>
    </el-aside>
  </el-container>
</template>

<script>
import ControlSideBar from './TrxControl/parts/ControlSideBar.vue'
import StateMachine from './TrxControl/parts/StateMachine.vue'
import Adc from './TrxControl/parts/Adc.vue'
import Dac from './TrxControl/parts/Dac.vue'
import DdmVdm from './TrxControl/parts/DdmVdm.vue'
import Misc from './TrxControl/parts/Misc.vue'
import Abc from './TrxControl/parts/Abc.vue'
import Dsp from './TrxControl/parts/Dsp.vue'
import Dpin from './TrxControl/parts/Dpin.vue'

export default {
  name: 'control-center',
  props: [],
  components: {
    ControlSideBar,
    StateMachine,
    Adc,
    Dac,
    DdmVdm,
    Abc,
    Misc,
    Dsp,
    Dpin
  },
  data () {
    return {
      currentTab: 'state-machine',
      enableADRefresh: false,
      trxIdx: undefined
    }
  },
  methods: {
    beforeLeave (activeName) {
      let self = this
      if (activeName === 'a-d-value') {
        self.enableADRefresh = true
      } else {
        self.enableADRefresh = false
      }
    },
    emitSelectTab () {
      console.log(`select-tab:${this.currentTab}`)
      this.$bus.$emit(`select-tab:${this.currentTab}`)
    }
  },
  activated () {
    this.emitSelectTab()
  }
}
</script>

<style lang="scss" scoped>
  .el-container {
    height: 100%;
  }
  .el-main {
    padding: 0;
  }
  .el-aside {
    border-left: 1px solid $border-color-light;
    padding: 14px 16px;
  }
  .main-top-tab {
    overflow: auto;
    display: flex;
    flex-direction: column;
    height: 100%;
    border: none;
  }
  .main-top-tab ::v-deep .el-tabs__content {
    padding: 0;
    height: 100%;
  }
  .main-top-tab ::v-deep .el-tab-pane {
    height: 100%;
    overflow: auto;
  }
</style>

<style>
</style>
