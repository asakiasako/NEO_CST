<template>
  <div :class="$style.wrapper">
    <el-card :class="$style['operation-card']">
      <div slot="header">MSE</div>
      <div :class="$style['display-wrapper']">
        <div v-for="(item, key) in mse" :class="$style['display']" :key="key">
          <div :class="$style['d-label']">{{key}}</div>
          <div :class="$style['d-value']">{{item.value ? item.value.toFixed(4) : undefined}}</div>
        </div>
        <div :class="$style['card-footer']">
          <el-button :loading="mseLoading" :class="$style['btn-single-line']" size="small" round type="success" plain @click="getMse">Get</el-button>
        </div>
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">Die Temperature</div>
      <div :class="$style['display-wrapper']">
        <div v-for="(item, key) in dieTemperature" :class="$style['display']" :key="key">
          <div :class="$style['d-label']">{{key}}</div>
          <div :class="$style['d-value']">{{item.value ? item.value.toFixed(1) : undefined}}</div>
        </div>
        <div :class="$style['card-footer']">
          <el-button :loading="dieTemperatureLoading" :class="$style['btn-single-line']" size="small" round type="success" plain @click="getDieTemperature">Get</el-button>
        </div>
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">PreAGC Amp.</div>
      <div :class="$style['display-wrapper']">
        <div v-for="(item, key) in preAgcAmp" :class="$style['display']" :key="key">
          <div :class="$style['d-label']">{{key}}</div>
          <div :class="$style['d-value']">{{item.value ? item.value.toFixed(4) : undefined}}</div>
        </div>
        <div :class="$style['card-footer']">
          <el-button :loading="preAgcAmpLoading" :class="$style['btn-single-line']" size="small" round type="success" plain @click="getPreAgcAmp">Get</el-button>
        </div>
      </div>
    </el-card>

    <el-card :class="$style['operation-card']">
      <div slot="header">AGC Gain</div>
      <div :class="$style['display-wrapper']">
        <div v-for="(item, key) in agcGain" :class="$style['display']" :key="key">
          <div :class="$style['d-label']">{{key}}</div>
          <div :class="$style['d-value']">{{item.value ? item.value.toFixed(4) : undefined}}</div>
        </div>
        <div :class="$style['card-footer']">
          <el-button :loading="agcGainLoading" :class="$style['btn-single-line']" size="small" round type="success" plain @click="getAgcGain">Get</el-button>
        </div>
      </div>
    </el-card>

    <el-card :class="$style['operation-card']">
      <div slot="header">Tx Skew</div>
      <div v-for="(item, key) in txSkew" :class="$style['rw-control']" :key="key">
        <div :class="$style['rw-label']">{{egressLaneMapping[key]}}</div>
        <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :precision="5" :controls="false"></el-input-number>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getTxSkew(key)">Get</el-button>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setTxSkew(key)">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">Rx Skew</div>
      <div v-for="(item, key) in rxSkew" :class="$style['rw-control']" :key="key">
        <div :class="$style['rw-label']">{{ingressLaneMapping[key]}}</div>
        <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :precision="0" :controls="false"></el-input-number>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getRxSkew(key)">Get</el-button>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setRxSkew(key)">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">DSP Tx ATT</div>
      <div v-for="(item, key) in dspTxAtt" :class="$style['rw-control']" :key="key">
        <div :class="$style['rw-label']">{{egressLaneMapping[key]}}</div>
        <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :precision="0" :controls="false"></el-input-number>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getDspTxAtt(key)">Get</el-button>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setDspTxAtt(key)">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">DSP Tx Analog ATT (0~4)</div>
      <div v-for="(item, key) in dspTxAnalogAtt" :class="$style['rw-control']" :key="key">
        <div :class="$style['rw-label']">{{egressLaneMapping[key]}}</div>
        <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :precision="0" :min="0" :max="4" :controls="false"></el-input-number>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setDspTxAnalogAtt(key)">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">Mute DSP Egress</div>
      <div v-for="(item, key) in muteDspEgress" :class="$style['rw-control']" :key="key">
        <div :class="$style['rw-label']">{{egressLaneMapping[key]}}</div>
        <el-select :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value">
          <el-option label="Mute" :value="true"></el-option>
          <el-option label="Unmute" :value="false"></el-option>
        </el-select>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getDspEgressMute(key)">Get</el-button>
        <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setDspEgressMute(key)">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">CFec Pattern</div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['set-label']">Generator</div>
        <el-select size="small" v-model="pattern.generator.enable" placeholder="Enable/Disable">
          <el-option label="Enable" :value="true"></el-option>
          <el-option label="Disable" :value="false"></el-option>
        </el-select>
        <el-select size="small" v-model="pattern.generator.patternIndex" placeholder="PRBS Pattern">
          <el-option v-for="(item, idx) in patternMapping" :key="idx" :label="item" :value="parseInt(idx)"></el-option>
        </el-select>
        <el-button :loading="pattern.generator.loading" :class="$style['btn-single-line']" size="small" type="success" plain @click="getCfecGenerator">Get</el-button>
        <el-button :loading="pattern.generator.loading" :class="$style['btn-single-line']" size="small" type="danger" plain @click="setCfecGenerator">Set</el-button>
      </div>
      <div :class="$style['line-wrapper']">
        <div :class="$style['set-label']">Checker</div>
        <el-select size="small" v-model="pattern.checker.enable" placeholder="Enable/Disable">
          <el-option label="Enable" :value="true"></el-option>
          <el-option label="Disable" :value="false"></el-option>
        </el-select>
        <el-select size="small" v-model="pattern.checker.patternIndex" placeholder="PRBS Pattern">
          <el-option v-for="(item, idx) in patternMapping" :key="idx" :label="item" :value="parseInt(idx)"></el-option>
        </el-select>
        <el-button :loading="pattern.checker.loading" :class="$style['btn-single-line']" size="small" type="success" plain @click="getCfecChecker">Get</el-button>
        <el-button :loading="pattern.checker.loading" :class="$style['btn-single-line']" size="small" type="danger" plain @click="setCfecChecker">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">Estimated Ber</div>
      <div v-for="(item, key) in estimatedBer" :key="key" :class="$style['fec-control']">
        <div :class="$style['fec-label']">{{key}} Estimated BER</div>
        <div :class="$style['fec-display']">{{estimatedBer[key] !== undefined ? estimatedBer[key].toExponential(2) : ''}}</div>
      </div>
      <el-button :loading="estimatedBerLoading" :class="$style['btn-fec']" size="small" type="success" plain @click="getPreFecBER">Get Estimated BER</el-button>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">Error Correction</div>
      <div :class="$style['fec-control']">
        <div :class="$style['fec-label']">Framer</div>
        <el-select :class="$style['fec-select']" size="small" v-model="fecFramer">
          <el-option :value="0" label="CH_A"></el-option>
          <el-option :value="1" label="CH_B"></el-option>
          <el-option :value="2" label="CH_C"></el-option>
          <el-option :value="3" label="CH_D"></el-option>
          <el-option :value="4" label="X00GE"></el-option>
        </el-select>
      </div>
      <div :class="$style['fec-control']">
        <div :class="$style['fec-label']">Direction</div>
        <el-select :class="$style['fec-select']" size="small" v-model="fecDirecton">
          <el-option :value="1" label="INGRESS"></el-option>
          <el-option :value="2" label="EGRESS"></el-option>
        </el-select>
      </div>
      <div v-for="(value, key) in errorCorrectionStatistics" :key="key" :class="$style['fec-control']">
        <div :class="$style['fec-label']">{{key}}</div>
        <div :class="$style['fec-display']">{{value !== undefined ? value.toExponential(2) : '' }}</div>
      </div>
      <el-button :loading="errorCorrectionStatisticsLoading" :class="$style['btn-fec']" size="small" type="success" plain @click="getErrorCorrection">GetErrorCorrectionStatistics</el-button>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">CFecPatternCheckerStatistics</div>
      <div v-for="(item, key) in cfecCheckerStatistics" :key="key" :class="$style['fec-control']">
        <div :class="$style['fec-label']">{{key}}</div>
        <div :class="$style['fec-display']">{{cfecCheckerStatistics[key] !== undefined ? cfecCheckerStatistics[key].toExponential(2) : ''}}</div>
      </div>
      <el-button :loading="cfecCheckerStatisticsLoading" :class="$style['btn-fec']" size="small" type="success" plain @click="getCfecCheckerStatistics">Get cfecCheckerStatistics</el-button>
      <div :class="$style['card-footer']">
      </div>
    </el-card>

    <el-card :class="$style['operation-card']">
      <div slot="header">PCS Test Pattern</div>
      <el-select size="small" v-model="pcsPatternDirection">
        <el-option label="Ingress" :value="1"></el-option>
        <el-option label="Egress" :value="2"></el-option>
      </el-select>
      <div style="display: flex; margin-top: 8px">
        <el-button size="small" @click="enablePcsGenerator(pcsPatternDirection)" type="info" plain :loading="pcsCheckerStatisticsLoading">Enable Generator</el-button>
        <el-button size="small" @click="enablePcsChecker(pcsPatternDirection)" type="info" plain :loading="pcsCheckerStatisticsLoading">Enable Checker</el-button>
      </div>
      <div v-for="(item, key) in pcsCheckerStatistics" :key="key" :class="$style['fec-control']">
        <div :class="$style['fec-label']">{{key}}</div>
        <div :class="$style['fec-display']">{{pcsCheckerStatistics[key] !== undefined ? pcsCheckerStatistics[key].toExponential(2) : ''}}</div>
      </div>
      <el-button :loading="pcsCheckerStatisticsLoading" :class="$style['btn-fec']" size="small" type="success" plain @click="getPcsCheckerStatistics">Get PCS Checker Statistics</el-button>
      <div :class="$style['card-footer']">
      </div>
    </el-card>

    <el-card :class="$style['operation-card']">
      <div slot="header">DSP FIR Filter</div>
      <div v-for="(item, key) in dspFirFilter" :class="$style['long-rw-control']" :key="key">
        <div :class="$style['long-rw-label']">{{egressLaneMapping[key]}}</div>
        <el-input :disabled="item.loading" :class="$style['long-rw-input']" size="small" v-model="item.value"></el-input>
        <div :class="$style['long-rw-btn-wrapper']">
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getDspFirFilter(key)">Get</el-button>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setDspFirFilter(key)">Set</el-button>
        </div>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">DSP Ingress AGC [0-1]</div>
      <div :class="$style['rw-control']">
        <el-input-number :class="$style['rw-input']" size="small" :controls="false" v-model="ingressAgc.value" :min="0" :max="1" :precision="3"></el-input-number>
        <el-button :loading="ingressAgc.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getIngressAgc">Get</el-button>
        <el-button :loading="ingressAgc.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setIngressAgc">Set</el-button>
      </div>
      <div :class="$style['card-footer']">
      </div>
    </el-card>
    <el-card :class="$style['operation-card']">
      <div slot="header">AVS [0, 15.5]</div>
      <div :class="$style['rw-control']">
        <div :class="$style['rw-label']">Enable</div>
        <el-select :class="$style['rw-select']" size="small" v-model="avs.enable.value" placeholder="En/Dis">
          <el-option :value="true" label="Enable"></el-option>
          <el-option :value="false" label="Disable"></el-option>
        </el-select>
        <el-button :loading="avs.enable.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getAvsEnable">Get</el-button>
        <el-button :loading="avs.enable.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setAvsEnable">Set</el-button>
      </div>
      <div :class="$style['rw-control']">
        <div :class="$style['rw-label']">Ratio</div>
        <el-input-number :disabled="avs.ratio.loading" :class="$style['rw-input']" size="small" v-model="avs.ratio.value" :min="0" :max="15.5" :precision="1" :controls="false"></el-input-number>
        <el-button :loading="avs.ratio.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getAvsRatio">Get</el-button>
        <el-button :loading="avs.ratio.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setAvsRatio">Set</el-button>
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
    const mse = {
      HI: { value: undefined },
      HQ: { value: undefined },
      VI: { value: undefined },
      VQ: { value: undefined }
    }
    const mseLoading = false
    const dieTemperature = {
      hrx2: { value: undefined },
      lrx: { value: undefined },
      ltx_v: { value: undefined },
      htx_top0: { value: undefined }
    }
    const dieTemperatureLoading = false
    const preAgcAmp = {
      HI: { value: undefined },
      HQ: { value: undefined },
      VI: { value: undefined },
      VQ: { value: undefined }
    }
    const preAgcAmpLoading = false
    const agcGain = {
      HI: { value: undefined },
      HQ: { value: undefined },
      VI: { value: undefined },
      VQ: { value: undefined }
    }
    const agcGainLoading = false
    const txSkew = {
      0: { value: undefined, loading: false },
      1: { value: undefined, loading: false },
      2: { value: undefined, loading: false },
      3: { value: undefined, loading: false }
    }
    const rxSkew = {
      0: { value: undefined, loading: false },
      1: { value: undefined, loading: false }
    }
    const dspTxAtt = {
      0: { value: undefined, loading: false },
      1: { value: undefined, loading: false },
      2: { value: undefined, loading: false },
      3: { value: undefined, loading: false }
    }
    const dspTxAnalogAtt = {
      0: { value: undefined, loading: false },
      1: { value: undefined, loading: false },
      2: { value: undefined, loading: false },
      3: { value: undefined, loading: false }
    }
    const muteDspEgress = {
      0: { value: undefined, loading: false },
      1: { value: undefined, loading: false },
      2: { value: undefined, loading: false },
      3: { value: undefined, loading: false }
    }
    const dspFirFilter = {
      0: { value: undefined, loading: false },
      1: { value: undefined, loading: false },
      2: { value: undefined, loading: false },
      3: { value: undefined, loading: false }
    }
    const pattern = {
      generator: { enable: undefined, patternIndex: undefined, loading: false },
      checker: { enable: undefined, patternIndex: undefined, loading: false }
    }
    const egressLaneMapping = {
      0: 'HI',
      1: 'HQ',
      2: 'VI',
      3: 'VQ'
    }
    const ingressLaneMapping = {
      0: 'H',
      1: 'V'
    }
    const patternMapping = {
      0: 'PRBS7',
      1: 'PRBS9',
      2: 'PRBS11',
      3: 'PRBS13',
      4: 'PRBS15',
      5: 'PRBS23',
      6: 'PRBS31'
    }
    const ingressAgc = {
      value: undefined,
      loading: false
    }
    const errorCorrectionStatistics = {
      BitCount: undefined,
      CorrErr: undefined,
      CorrBER: undefined,
      UncorrCW: undefined
    }
    const errorCorrectionStatisticsLoading = false
    const estimatedBer = {
      Staircaise: undefined,
      Hamming: undefined,
      Total: undefined
    }
    const estimatedBerLoading = false
    let fecFramer
    let fecDirecton
    const cfecCheckerStatistics = {
      BitCount: undefined,
      ErrorCount: undefined,
      BER: undefined
    }
    const cfecCheckerStatisticsLoading = false
    const pcsPatternDirection = null
    const pcsCheckerStatistics = {
      BitCount: undefined,
      ErrorCount: undefined,
      BER: undefined
    }
    const pcsCheckerStatisticsLoading = false
    const avs = {
      enable: { value: undefined, loading: false },
      ratio: { value: undefined, loading: false }
    }
    return {
      mse,
      mseLoading,
      dieTemperature,
      dieTemperatureLoading,
      preAgcAmp,
      preAgcAmpLoading,
      agcGain,
      agcGainLoading,
      txSkew,
      rxSkew,
      dspTxAtt,
      dspTxAnalogAtt,
      muteDspEgress,
      dspFirFilter,
      pattern,
      egressLaneMapping,
      ingressLaneMapping,
      patternMapping,
      ingressAgc,
      errorCorrectionStatistics,
      errorCorrectionStatisticsLoading,
      estimatedBer,
      estimatedBerLoading,
      fecFramer,
      fecDirecton,
      cfecCheckerStatistics,
      cfecCheckerStatisticsLoading,
      pcsPatternDirection,
      pcsCheckerStatistics,
      pcsCheckerStatisticsLoading,
      avs
    }
  },
  methods: {
    getMse () {
      this.mseLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-mse',
        args: [this.trxIdx]
      }).then((val) => {
        this.mse.HI.value = val.HI
        this.mse.HQ.value = val.HQ
        this.mse.VI.value = val.VI
        this.mse.VQ.value = val.VQ
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.mseLoading = false
      })
    },
    getDieTemperature () {
      this.dieTemperatureLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-die-temperature',
        args: [this.trxIdx]
      }).then(val => {
        this.dieTemperature.hrx2 = val[0]
        this.dieTemperature.lrx = val[1]
        this.dieTemperature.ltx_v = val[2]
        this.dieTemperature.htx_top0 = val[3]
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.dieTemperatureLoading = false
      })
    },
    getPreAgcAmp () {
      this.preAgcAmpLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-pre-agc-amp',
        args: [this.trxIdx]
      }).then((res) => {
        this.preAgcAmp.HI.value = res.HI
        this.preAgcAmp.HQ.value = res.HQ
        this.preAgcAmp.VI.value = res.VI
        this.preAgcAmp.VQ.value = res.VQ
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.preAgcAmpLoading = false
      })
    },
    getAgcGain () {
      this.agcGainLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-agc-gain',
        args: [this.trxIdx]
      }).then(res => {
        this.agcGain.HI.value = res.HI
        this.agcGain.HQ.value = res.HQ
        this.agcGain.VI.value = res.VI
        this.agcGain.VQ.value = res.VQ
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.agcGainLoading = false
      })
    },
    getTxSkew (lane) {
      this.txSkew[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:get-tx-skew',
        args: [this.trxIdx, lane]
      }).then((res) => {
        this.txSkew[lane].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.txSkew[lane].loading = false
      })
    },
    setTxSkew (lane) {
      this.txSkew[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:set-tx-skew',
        args: [this.trxIdx, lane, this.txSkew[lane].value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.txSkew[lane].loading = false
      })
    },
    getRxSkew (lane) {
      this.rxSkew[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:get-rx-skew',
        args: [this.trxIdx, lane]
      }).then((res) => {
        this.rxSkew[lane].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.rxSkew[lane].loading = false
      })
    },
    setRxSkew (lane) {
      this.rxSkew[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:set-rx-skew',
        args: [this.trxIdx, lane, this.rxSkew[lane].value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.rxSkew[lane].loading = false
      })
    },
    getDspTxAtt (lane) {
      this.dspTxAtt[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:get-dsp-tx-att',
        args: [this.trxIdx, lane]
      }).then((res) => {
        this.dspTxAtt[lane].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.dspTxAtt[lane].loading = false
      })
    },
    setDspTxAtt (lane) {
      this.dspTxAtt[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:set-dsp-tx-att',
        args: [this.trxIdx, lane, this.dspTxAtt[lane].value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.dspTxAtt[lane].loading = false
      })
    },
    setDspTxAnalogAtt (lane) {
      this.dspTxAnalogAtt[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:set-dsp-tx-analog-att',
        args: [this.trxIdx, lane, this.dspTxAnalogAtt[lane].value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.dspTxAnalogAtt[lane].loading = false
      })
    },
    getCfecGenerator () {
      this.pattern.generator.loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-cfec-generator',
        args: [this.trxIdx]
      }).then(res => {
        [this.pattern.generator.patternIndex, this.pattern.generator.enable] = res
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.pattern.generator.loading = false
      })
    },
    setCfecGenerator () {
      this.pattern.generator.loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:set-cfec-generator',
        args: [this.trxIdx, this.pattern.generator.patternIndex, this.pattern.generator.enable]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.pattern.generator.loading = false
      })
    },
    getCfecChecker () {
      this.pattern.checker.loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-cfec-checker',
        args: [this.trxIdx]
      }).then(res => {
        [this.pattern.checker.patternIndex, this.pattern.checker.enable] = res
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.pattern.checker.loading = false
      })
    },
    setCfecChecker () {
      this.pattern.checker.loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:set-cfec-checker',
        args: [this.trxIdx, this.pattern.checker.patternIndex, this.pattern.checker.enable]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.pattern.checker.loading = false
      })
    },
    getDspFirFilter (lane) {
      this.dspFirFilter[lane].loading = true
      lane = parseInt(lane)
      this.$rpcClient.request({
        route: ':trx:dsp:get-dsp-fir-filter',
        args: [this.trxIdx, lane]
      }).then((res) => {
        const rRes = []
        for (const i of res) rRes.push(Math.round(i * 1000) / 1000)
        this.dspFirFilter[lane].value = rRes.join(', ')
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.dspFirFilter[lane].loading = false
      })
    },
    checkFirFilterFormat (lane) {
      lane = parseInt(lane)
      const reg = /^(\s*-?\d+(\.\d+)?\s*,){6}(\s*-?\d+(\.\d+)?\s*)$/
      const val = this.dspFirFilter[lane].value
      if (typeof val !== 'string') return false
      else return reg.test(val)
    },
    setDspFirFilter (lane) {
      this.dspFirFilter[lane].loading = true
      lane = parseInt(lane)
      if (!this.checkFirFilterFormat(lane)) {
        this.$alert('Invald format of FirFilter: should be 7 numbers seperated by comma.', 'ERROR', {
          confirmButtonText: 'OK',
          type: 'error'
        })
        return
      }
      const sList = this.dspFirFilter[lane].value.split(',')
      const vList = []
      for (const s of sList) {
        vList.push(parseFloat(s))
      }
      this.$rpcClient.request({
        route: ':trx:dsp:set-dsp-fir-filter',
        args: [this.trxIdx, lane, vList]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.dspFirFilter[lane].loading = false
      })
    },
    getDspEgressMute (lane) {
      this.muteDspEgress[lane].loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-egress-lane-mute',
        args: [this.trxIdx, parseInt(lane)]
      }).then((res) => {
        this.muteDspEgress[lane].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.muteDspEgress[lane].loading = false
      })
    },
    setDspEgressMute (lane) {
      this.muteDspEgress[lane].loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:set-egress-lane-mute',
        args: [this.trxIdx, parseInt(lane), this.muteDspEgress[lane].value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.muteDspEgress[lane].loading = false
      })
    },
    getIngressAgc () {
      this.ingressAgc.loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-ingress-agc',
        args: [this.trxIdx]
      }).then((res) => {
        this.ingressAgc.value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.ingressAgc.loading = false
      })
    },
    setIngressAgc () {
      this.ingressAgc.loading = true
      this.$rpcClient.request({
        route: ':trx:dsp:set-ingress-agc',
        args: [this.trxIdx, this.ingressAgc.value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.ingressAgc.loading = false
      })
    },
    getErrorCorrection () {
      if (this.fecFramer === undefined || this.fecDirecton === undefined) {
        this.$alert('Empty framer or direction.', 'Error')
        return
      }
      this.errorCorrectionStatisticsLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-error-correction-statistics',
        args: [this.trxIdx, this.fecFramer, this.fecDirecton]
      }).then((res) => {
        this.errorCorrectionStatistics.BitCount = res.accum_bit_count
        this.errorCorrectionStatistics.CorrErr = res.accum_corrected_error_count
        this.errorCorrectionStatistics.CorrBER = res.accum_bit_count ? res.accum_corrected_error_count / res.accum_bit_count : 1
        this.errorCorrectionStatistics.UncorrCW = res.accum_uncorrected_codeword_count
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.errorCorrectionStatisticsLoading = false
      })
    },
    getPreFecBER () {
      this.estimatedBerLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-pre-fec-ber',
        args: [this.trxIdx]
      }).then((res) => {
        console.log(res)
        this.estimatedBer.Staircaise = res.staircaise_estimated_ber
        this.estimatedBer.Hamming = res.hamming_estimated_ber
        this.estimatedBer.Total = res.staircaise_estimated_ber + res.hamming_estimated_ber
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.estimatedBerLoading = false
      })
    },
    getCfecCheckerStatistics () {
      this.cfecCheckerStatisticsLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-core-cfec-test-pattern-checker-statistics',
        args: [this.trxIdx]
      }).then((res) => {
        this.cfecCheckerStatistics.BitCount = res[0]
        this.cfecCheckerStatistics.ErrorCount = res[1]
        this.cfecCheckerStatistics.BER = res[0] ? res[1] / res[0] : 1
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.cfecCheckerStatisticsLoading = false
      })
    },
    enablePcsGenerator (direction) {
      if (!direction) {
        this.$alertError(TypeError('Please select PCS pattern direction'))
        return
      }
      this.pcsCheckerStatisticsLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:enable-pcs-pattern-generator',
        args: [this.trxIdx, direction]
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.pcsCheckerStatisticsLoading = false
      })
    },
    enablePcsChecker (direction) {
      if (!direction) {
        this.$alertError(TypeError('Please select PCS pattern direction'))
        return
      }
      this.pcsCheckerStatisticsLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:enable-pcs-pattern-checker',
        args: [this.trxIdx, direction]
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.pcsCheckerStatisticsLoading = false
      })
    },
    getPcsCheckerStatistics () {
      this.pcsCheckerStatisticsLoading = true
      this.$rpcClient.request({
        route: ':trx:dsp:get-pcs-test-pattern-checker-statistics',
        args: [this.trxIdx]
      }).then((res) => {
        this.pcsCheckerStatistics.BitCount = res[0]
        this.pcsCheckerStatistics.ErrorCount = res[1]
        this.pcsCheckerStatistics.BER = res[0] ? res[1] / res[0] : 1
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.pcsCheckerStatisticsLoading = false
      })
    },
    getAvsEnable () {
      this.avs.enable.loading = true
      this.$rpcClient.request({
        route: ':trx:avs:get-enable',
        args: [this.trxIdx]
      }).then((res) => {
        this.avs.enable.value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.avs.enable.loading = false
      })
    },
    setAvsEnable () {
      this.avs.enable.loading = true
      this.$rpcClient.request({
        route: ':trx:avs:set-enable',
        args: [this.trxIdx, this.avs.enable.value]
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.avs.enable.loading = false
      })
    },
    getAvsRatio () {
      this.avs.ratio.loading = true
      this.$rpcClient.request({
        route: ':trx:avs:get-ratio',
        args: [this.trxIdx]
      }).then((res) => {
        this.avs.ratio.value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.avs.ratio.loading = false
      })
    },
    setAvsRatio () {
      this.avs.ratio.loading = true
      this.$rpcClient.request({
        route: ':trx:avs:set-ratio',
        args: [this.trxIdx, this.avs.ratio.value]
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.avs.ratio.loading = false
      })
    }
  }
}
</script>

<style lang='scss' module>
  .wrapper {
    padding: 8px;
    display: flex;
    flex-wrap: wrap;
    margin-right: -8px;
  }
  .operation-card:global(.el-card.is-always-shadow) {
    width: 300px;
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
  .display-wrapper {
    display: flex;
    flex-wrap: wrap;
  }
  .display {
    padding: 5px 0;
    display: flex;
    align-items: center;
    width: 50%;
  }
  .d-label {
    width: 30px;
    color: $color-text-secondary;
  }
  .d-value {
    border: 1px solid $border-color-base;
    border-radius: 3px;
    padding: 5px 12px;
    width: 80px;
    height: 30px;
  }
  .card-footer {
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 15px;
  }
  .btn-single-line {
    width: 100px;
  }
  .rw-control {
    display: flex;
    align-items: center;
    margin: 8px 0;
  }
  .rw-label {
    width: 80px;
    color: $color-text-secondary;
  }
  .rw-input {
    margin-right: 10px;
  }
  .rw-control :global(.el-button) {
    width: 80px;
    padding: 0;
    height: 32px;
  }
  .long-rw-control {
    margin-bottom: 15px;
  }
  .long-rw-control > * {
    margin-bottom: 8px;
  }
  .long-rw-label {
    width: 50px;
    display: inline-block;
    color: $color-text-secondary;
  }
  .long-rw-input:global(.el-input) {
    width: 207px;
  }
  .long-rw-btn-wrapper {
    display: flex;
    justify-content: flex-end;
  }
  .set-control {
    display: flex;
    align-items: center;
    margin: 8px 0;
  }
  .set-label {
    width: 80px;
    color: $color-text-secondary;
  }
  .set-control :global(.el-select) {
    width: 1px;
    flex-grow: 1;
    margin-right: 10px;
  }
  .line-wrapper > * {
    margin: 8px 0;
  }
  .rw-select {
    width: 130px;
    margin-right: 10px;
  }
  .fec-control {
    display: flex;
    align-items: center;
    margin: 8px 0;
  }
  .fec-label {
    width: 120px;
    color: $color-text-secondary;
  }
  .btn-fec {
    height: 32px;
    margin: 10px 0;
  }
  .fec-display {
    height: 32px;
    width: 130px;
    border: 1px solid $border-color-base;
    border-radius: 3px;
  }
  .fec-select {
    margin: 0;
    width: 130px;
  }
</style>
