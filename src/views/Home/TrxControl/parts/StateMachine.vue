<template>
  <div class="outline">
    <div id="state-diagram">
      <div class="state-diagram-header">
        <el-radio-group v-model="states.stateMachineSel" size="small">
          <el-radio-button label="Module State Machine"></el-radio-button>
          <el-radio-button label="Data Path State Machine"></el-radio-button>
        </el-radio-group>
        <el-button type="primary" plain size="small" icon="el-icon-refresh" @click="refreshStateMachine">Refresh State</el-button>
      </div>
      <div class="state-diagram-wrapper">
        <div class="state-diagram-inner" :class="states.stateMachineSel === 'Data Path State Machine' ? 'shifted' : ''">
          <div id="module-state-diagram" class="state-diagram-item">
            <div class="line-wrap">
              <div id="Reset" class="state-item">Reset</div>
              <div id="MgmtInit" class="state-item transient">MgmtInit</div>
              <div id="ModuleLowPwr" class="state-item" :class="states.currentModuleState==='ModuleLowPwr'?'active-state':''">ModuleLowPwr</div>
              <div id="ModulePwrUp" class="state-item transient" :class="states.currentModuleState==='ModulePwrUp'?'active-state':''">ModulePwrUp</div>
              <div id="ModuleReady" class="state-item" :class="states.currentModuleState==='ModuleReady'?'active-state':''">ModuleReady</div>
            </div>
            <div class="line-wrap">
              <div class="placeholder"></div>
              <div id="Resetting" class="state-item transient">Resetting</div>
              <div class="placeholder"></div>
              <div id="ModulePwrDn" class="state-item transient" :class="states.currentModuleState==='ModulePwrDn'?'active-state':''">ModulePwrDn</div>
              <div class="placeholder"></div>
            </div>
            <div class="line-wrap last">
              <div id="Fault" class="state-item" :class="states.currentModuleState==='Fault'?'active-state':''">Fault</div>
            </div>
          </div>
          <div id="data-path-state-diagram" class="state-diagram-item">
            <div class="line-wrap">
              <div id="DataPathDeactivated" class="state-item" :class="states.currentDataPathState==='DataPathDeactivated'?'active-state':''">DataPath Deactivated</div>
              <div id="DataPathInit" class="state-item transient" :class="states.currentDataPathState==='DataPathInit'?'active-state':''">DataPathInit</div>
              <div id="DataPathInitialized" class="state-item" :class="states.currentDataPathState==='DataPathInitialized'?'active-state':''">DataPath Initialized</div>
              <div id="DataPathTxTurnOn" class="state-item transient" :class="states.currentDataPathState==='DataPathTxTurnOn'?'active-state':''">DataPath TxTurnOn</div>
              <div id="DataPathActivated" class="state-item" :class="states.currentDataPathState==='DataPathActivated'?'active-state':''">DataPath Activated</div>
            </div>
            <div class="line-wrap">
              <div class="placeholder"></div>
              <div id="DataPathDeinit" class="state-item transient" :class="states.currentDataPathState==='DataPathDeinit'?'active-state':''">DataPathDeinit</div>
              <div class="placeholder"></div>
              <div id="DataPathTxTurnOff" class="state-item transient" :class="states.currentDataPathState==='DataPathTxTurnOff'?'active-state':''">DataPath TxTurnOff</div>
              <div class="placeholder"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="control-section">
      <div class="control-section-wrapper">
        <div class="pin-section">
          <div class="pin-title">
            Signal Pins
            <span class="pin-legend-section">
              <span class="pin-legend flag-low"></span>
              <span>Low</span>
              <span class="pin-legend flag-high"></span>
              <span>High</span>
            </span>
          </div>
          <div class="pin-wrapper">
            <div class="control-pins">
              <div
                v-for="(item, key) in controlPinState"
                :key="key"
                class="pin-with-label"
              >
                <el-switch
                  :width="32"
                  active-color="#67c23a"
                  v-model="controlPinState[key]"
                  @change="setControlPin(key, $event)"
                >
                </el-switch>
                <span class="pin-label">{{key}}</span>
              </div>
            </div>
            <div class="alarm-pins">
              <div
                v-for="(item, key) in alarmPinState"
                :key="key"
                class="pin-with-label"
              >
                <span class="pin-flag" :class="alarmPinState[key]?'flag-high':'flag-low'"></span>
                <span class="pin-label">{{key}}</span>
              </div>
            </div>
          </div>
          <el-button size="small" plain type="primary" @click="getPinState" icon="el-icon-refresh" style="margin-top: 5px;">Refresh Pin State</el-button>
        </div>
        <div class="refresh-buttons">
          <el-button size="small" plain type="info" @click="getTrxFwVer">Get TRx Active FW Ver.</el-button>
          <el-button size="small" plain type="info" @click="getDspFwVer">Get DSP FW Ver.</el-button>
          <el-button size="small" plain type="info" @click="getTrxInfo">Get TRx Info</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { jsPlumb } from 'jsplumb'
import { setPinState, getPinState } from '@/utils/dut_control'

export default {
  props: {
    trxIdx: Number
  },
  data () {
    const states = {
      stateMachineSel: 'Module State Machine',
      currentModuleState: '',
      currentDataPathState: '',
      dialogInfoVisible: false
    }
    const controlPinState = {
      LPWn: false,
      RSTn: false
    }
    const alarmPinState = {
      PRSn: false,
      INT: false
    }
    return {
      states,
      controlPinState,
      alarmPinState
    }
  },
  mounted () {
    const commonStyle = {
      connector: ['Flowchart'],
      endpoint: 'Blank',
      paintStyle: { stroke: '#d3d4d6', strokeWidth: 1 },
      overlays: [['Arrow', { width: 10, length: 10, location: 1 }]]
    }
    // Module State diagram generate
    const plumbInsModState = jsPlumb.getInstance({ Container: 'module-state-diagram' })
    plumbInsModState.ready(function () {
      const stateTransitions = [
        [['Reset', 'MgmtInit'], ['Right', 'Left']],
        [['MgmtInit', 'ModuleLowPwr'], ['Right', 'Left']],
        [['ModuleLowPwr', 'ModulePwrUp'], ['Right', 'Left']],
        [['ModulePwrUp', 'ModuleReady'], ['Right', 'Left']],
        [['ModuleReady', 'ModulePwrDn'], ['Bottom', 'Right']],
        [['ModulePwrDn', 'ModuleLowPwr'], ['Left', [0.7, 1, 0, 1]]],
        [['ModuleLowPwr', 'Resetting'], [[0.3, 1, 0, 1], 'Right']],
        [['Resetting', 'Reset'], ['Left', 'Bottom']],
        [['ModulePwrUp', 'ModulePwrDn'], ['Bottom', 'Top']],
        [['MgmtInit', 'Resetting'], ['Bottom', 'Top']]
      ]
      for (const item of stateTransitions) {
        plumbInsModState.connect({
          source: item[0][0],
          target: item[0][1],
          anchor: item[1]
        }, commonStyle)
      }
    })
    // Data Path State diagram generate
    const plumbInsDPathState = jsPlumb.getInstance({ Container: 'data-path-state-diagram' })
    plumbInsDPathState.ready(function () {
      const stateTransitions = [
        [['DataPathDeactivated', 'DataPathInit'], ['Right', 'Left']],
        [['DataPathInit', 'DataPathInitialized'], ['Right', 'Left']],
        [['DataPathInitialized', 'DataPathTxTurnOn'], ['Right', 'Left']],
        [['DataPathTxTurnOn', 'DataPathActivated'], ['Right', 'Left']],
        [['DataPathActivated', 'DataPathTxTurnOff'], ['Bottom', 'Right']],
        [['DataPathTxTurnOff', 'DataPathInitialized'], ['Left', [0.7, 1, 0, 1]]],
        [['DataPathInitialized', 'DataPathDeinit'], [[0.3, 1, 0, 1], 'Right']],
        [['DataPathDeinit', 'DataPathDeactivated'], ['Left', 'Bottom']],
        [['DataPathTxTurnOn', 'DataPathTxTurnOff'], ['Bottom', 'Top']],
        [['DataPathInit', 'DataPathDeinit'], ['Bottom', 'Top']]
      ]
      for (const item of stateTransitions) {
        plumbInsDPathState.connect({
          source: item[0][0],
          target: item[0][1],
          anchor: item[1]
        }, commonStyle)
      }
    })
  },
  methods: {
    getModuleState () {
      this.$rpcClient.request({
        route: ':trx:get-module-state',
        args: [this.trxIdx]
      }).then(res => {
        console.log(res)
        this.states.currentModuleState = res
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getDataPathState () {
      this.$rpcClient.request({
        route: ':trx:get-data-path-state',
        args: [this.trxIdx]
      }).then(res => {
        this.states.currentDataPathState = res
      }).catch(err => {
        this.$alertError(err)
      })
    },
    refreshStateMachine () {
      console.log(this.states.stateMachineSel)
      if (this.states.stateMachineSel === 'Module State Machine') {
        this.getModuleState()
      } else if (this.states.stateMachineSel === 'Data Path State Machine') {
        this.getDataPathState()
      }
      console.log(3)
    },
    getPinState () {
      const self = this
      const promises = []
      for (const key in self.controlPinState) {
        promises.push(
          getPinState(this.trxIdx, key).then(res => {
            self.controlPinState[key] = res
          })
        )
      }
      for (const key in self.alarmPinState) {
        promises.push(
          getPinState(this.trxIdx, key).then(res => {
            self.alarmPinState[key] = res
          })
        )
      }
      Promise.all(promises).catch(err => {
        this.$alertError(err)
      })
    },
    setControlPin (pinName, isHigh) {
      const self = this
      setPinState(this.trxIdx, pinName, isHigh).catch(err => {
        this.$alertError(err)
        self.controlPinState[pinName] = !isHigh
      })
    },
    getTrxFwVer () {
      this.$rpcClient.request({
        route: ':trx:information:module-active-firmware-version',
        args: [this.trxIdx]
      }).then((result) => {
        this.$alert(`${result}`, 'Trx Active FW Ver.', {
          confirmButtonText: 'OK',
          type: 'info'
        })
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getTrxInfo () {
      this.$rpcClient.request({
        route: ':trx:information:module-information',
        args: [this.trxIdx]
      }).then((result) => {
        let resStr = ''
        for (const key in result) {
          resStr += `<p><span style="display: inline-block;width: 156px;">${key}:</span><span>${result[key]}</span></p>`
        }
        this.$alert(resStr, 'TRx Information', {
          confirmButtonText: 'OK',
          type: 'info',
          dangerouslyUseHTMLString: true
        })
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getDspFwVer () {
      this.$rpcClient.request({
        route: ':trx:information:dsp-firmware-version',
        args: [this.trxIdx]
      }).then((result) => {
        this.$alert(`${result}`, 'DSP FW Ver.', {
          confirmButtonText: 'OK',
          type: 'info'
        })
      }).catch((err) => {
        this.$alertError(err)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
  .outline {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  #state-diagram {
    display: flex;
    flex-direction: column;
    padding: 20px 20px 16px;
    position: relative;
    flex-grow: 1;
    max-height: 360px;
  }
  .state-diagram-header {
    width: 610px;
    margin-bottom: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .state-diagram-wrapper {
    width: 610px;
    overflow: hidden;
  }
  .state-diagram-inner {
    width: 1300px;
    display: flex;
    transition: all .3s ease-in-out;
  }
  .state-diagram-inner.shifted {
    margin-left: -630px;
  }
  .state-diagram-item {
    width: 610px;
    margin-right: 20px;
    position: relative;
  }
  .line-wrap {
    display: flex;
    justify-content: space-between;
    margin-bottom: 45px;
  }
  .line-wrap.last {
    margin-bottom: 0;
  }
  .line-wrap.around {
    justify-content: space-around;
    padding: 0 55px;
  }
  .state-item {
    color: $color-text-secondary;
    background: #f4f4f5;
    border: 1px solid #d3d4d6;
    width: 96px;
    height: 42px;
    font-size: 12px;
    white-space: pre-line;
    display: flex;
    flex-direction: column;
    text-align: center;
    justify-content: center;
  }
  .state-item.transient {
    border-radius: 18px;
  }
  .state-item.active-state {
    color: $color-success;
    background: #f0f9eb;
    border-color: #c2e7b0;
  }
  .placeholder {
    width: 96px;
    height: 0;
  }
  #fault {
    position: absolute;
    left: 0;
  }
  .control-section {
    width: 100%;
    display: flex;
    background: $color-light;
  }
  .control-section-wrapper {
    width: 650px;
    display: flex;
    padding: 14px 20px;
    justify-content: space-between;
  }
  .pin-section {
    display: flex;
    flex-direction: column;
  }
  .pin-title {
    display: flex;
    align-items: flex-end;
    color: $color-text-secondary;
    font-size: 14px;
    margin-bottom: 12px;
  }
  .pin-legend {
    width: 12px;
    height:12px;
  }
  .flag-low {
    background: $border-color-base;
    border: 1px solid #d3d4d6;
  }
  .flag-high {
    background: $color-success;
    border: 1px solid $color-success;
  }
  .pin-legend-section {
    font-size: 12px;
    display: flex;
    align-items: center;
    margin-left: 10px;
  }
  .pin-legend-section span {
    margin-left: 4px;
  }
  .pin-wrapper {
    display: flex;
  }
  .control-pins {
    margin-right: 20px;
    border-radius: 4px;
  }
  .refresh-buttons {
    display: flex;
    flex-direction: column;
    margin-top: 8px;
  }
  .refresh-buttons .el-button {
    width: 150px;
    margin: 0 0 6px !important;
  }
  .pin-with-label {
    width: 102px;
    padding: 3px 0;
    font-size: 12px;
    color: $color-text-regular;
    display: flex;
    align-items: center;
  }
  .pin-label {
    width: 50px;
    margin-left: 12px;
    display: inline-block;
  }
  .el-switch ::v-deep .el-switch__core {
    height: 18px;
  }
  .el-switch ::v-deep .el-switch__core:after {
    width: 14px;
    height: 14px;
  }
  .el-switch.is-checked ::v-deep .el-switch__core::after {
    margin-left: -15px;
  }
  .pin-flag {
    display: inline-block;
    width: 30px;
    height: 14px;
    margin: 3px;
  }
</style>
