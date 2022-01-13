<template>
  <div :class="$style.wrapper">
    <h2>PID Params</h2>
    <el-table
      :class="$style['pid-table']"
      :data="pidParams"
      style="width: 100%"
      size="small"
    >
      <el-table-column
        prop="name"
        label="Name"
        width="60"
        fixed
      ></el-table-column>
      <el-table-column
        label="P"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].p" :controls="false" :min="-3.4E38" :max="3.4E38"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="I"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].i" :controls="false" :min="-3.4E38" :max="3.4E38"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="D"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].d" :controls="false" :min="-3.4E38" :max="3.4E38"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="I_Min"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].iMin" :controls="false" :min="-3.4E38" :max="3.4E38"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="I_Max"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].iMax" :controls="false" :min="-3.4E38" :max="3.4E38"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="Polarity"
        width="108"
      >
        <template slot-scope="scope">
          <el-select size="small" v-model="pidParams[scope.$index].polarity">
            <el-option :value="1" label="Pos"></el-option>
            <el-option :value="0" label="Neg"></el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column
        label="Method"
        width="108"
      >
        <template slot-scope="scope">
          <el-select size="small" v-model="pidParams[scope.$index].method">
            <el-option :value="0" label="0"></el-option>
            <el-option :value="1" label="1"></el-option>
            <el-option :value="2" label="2"></el-option>
          </el-select>
        </template>
      </el-table-column>
      <el-table-column
        label="Step"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].step" :controls="false" :min="-3.4E38" :max="3.4E38"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="Target"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].target" :controls="false" :min="-3.4E38" :max="3.4E38"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="Theta"
        width="80"
      >
        <template slot-scope="scope">
          <el-input-number :class="$style['pid-input']" size="small" v-model="pidParams[scope.$index].theta" :controls="false" :min="0" :max="359" :precision="0"></el-input-number>
        </template>
      </el-table-column>
      <el-table-column
        label="Controls"
        width="150"
      >
        <template slot-scope="scope">
          <el-button size="small" type="success" plain @click="getParams(scope.$index)">Get</el-button>
          <el-button size="small" type="danger" plain @click="setParams(scope.$index)">Set</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div :class="$style['card-wrapper']">
      <el-card :class="$style['operation-card']">
        <div slot="header">Basic ABC Control</div>
        <el-form label-width="120px" label-position="left">
          <el-form-item label="ABC Service">
            <el-switch :class="$style['line-item']" active-color="#24C84B" v-model="abcService" @change="setServiceState"></el-switch>
            <el-button :class="$style['line-item']" type="success" plain size="small" @click="getServiceState">Get state</el-button>
          </el-form-item>
          <el-form-item label="Algo">
            <el-select :class="$style['line-item']" v-model="algo" @change="setAlgo" size="small">
              <el-option :value="0" label="PID"></el-option>
              <el-option :value="1" label="Butterfly"></el-option>
            </el-select>
            <el-button :class="$style['line-item']" type="success" plain size="small" @click="getAlgo">Get</el-button>
          </el-form-item>
          <el-form-item label="Dither Status">
            <el-switch :class="$style['line-item']" active-color="#24C84B" @change="setDitherState" v-model="ditherStatus"></el-switch>
            <el-button :class="$style['line-item']" type="success" plain size="small" @click="getDitherState">Get state</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      <el-card :class="$style['operation-card']">
        <div slot="header">ABC Settings</div>
        <el-form label-width="120px" label-position="left">
          <el-form-item label="Freq Idx">
            <el-select size="small" v-model="abcSettings.freqIdx">
              <el-option :value="0" label="28, 21, 12, 84"></el-option>
              <el-option :value="1" label="35, 14, 10, 70"></el-option>
              <el-option :value="2" label="40, 24, 15, 120"></el-option>
              <el-option :value="3" label="45, 30, 18, 90"></el-option>
              <el-option :value="4" label="45, 36, 20, 180"></el-option>
              <el-option :value="5" label="56, 42, 24, 168"></el-option>
              <el-option :value="6" label="63, 18, 14, 212"></el-option>
              <el-option :value="7" label="70, 28, 20, 140"></el-option>
              <el-option :value="8" label="70, 30, 21, 210"></el-option>
              <el-option :value="9" label="75, 50, 30, 150"></el-option>
              <el-option :value="10" label="80, 48, 30, 240"></el-option>
              <el-option :value="11" label="84, 63, 36, 252"></el-option>
              <el-option :value="12" label="90, 60, 36, 180"></el-option>
              <el-option :value="13" label="99, 22, 18, 198"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Amplitude">
            <el-input-number size="small" v-model="abcSettings.amplitude" :controls="false" :precision="0"></el-input-number>
          </el-form-item>
          <el-form-item label="Theta">
            <el-input-number size="small" v-model="abcSettings.theta" :controls="false" :precision="0"></el-input-number>
          </el-form-item>
          <el-form-item label="Iter">
            <el-input-number size="small" v-model="abcSettings.iter" :controls="false" :precision="0"></el-input-number>
          </el-form-item>
          <div :class="$style['card-footer']">
            <el-button size="small" type="success" plain @click="getSettings">Get settings</el-button>
            <el-button size="small" type="danger" plain @click="setSettings">Set settings</el-button>
          </div>
        </el-form>
      </el-card>
      <el-card :class="$style['operation-card']">
        <div slot="header">ABC Method</div>
        <div v-for="(item, idx) in abcMethod" :class="$style['rw-control']" :key="idx">
          <div :class="$style['rw-label']">{{abcPhaseMapping[idx]}}</div>
          <el-select :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value">
            <el-option v-for="(method, methodIdx) in abcMethodMapping" :key="methodIdx" :value="parseInt(methodIdx)" :label="method"></el-option>
          </el-select>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getAbcMethod(idx)">Get</el-button>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setAbcMethod(idx)">Set</el-button>
        </div>
        <div :class="$style['card-footer']">
        </div>
      </el-card>
      <el-card :class="$style['operation-card']">
        <div slot="header">Demod</div>
        <div v-for="(item, idx) in demod" :class="$style['rw-control']" :key="idx">
          <div :class="$style['rw-label']">{{abcPhaseMapping[idx]}}</div>
          <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :precision="3" :controls="false"></el-input-number>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getDemod(idx)">Get</el-button>
        </div>
        <div :class="$style['card-footer']">
        </div>
      </el-card>
      <el-card :class="$style['operation-card']">
        <div slot="header">Theta</div>
        <div v-for="(item, idx) in theta" :class="$style['rw-control']" :key="idx">
          <div :class="$style['rw-label']">{{abcPhaseMapping[idx]}}</div>
          <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :min="0" :max="359" :precision="0" :controls="false"></el-input-number>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getTheta(idx)">Get</el-button>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setTheta(idx)">Set</el-button>
        </div>
        <div :class="$style['card-footer']">
        </div>
      </el-card>
      <el-card :class="$style['operation-card']">
        <div slot="header">ABC Target [-1600, 1600]</div>
        <div v-for="(item, idx) in target" :class="$style['rw-control']" :key="idx">
          <div :class="$style['rw-label']">{{abcPhaseMapping[idx]}}</div>
          <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :min="-1600" :max="1600" :precision="3" :controls="false"></el-input-number>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getTarget(idx)">Get</el-button>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setTarget(idx)">Set</el-button>
        </div>
        <div :class="$style['card-footer']">
        </div>
      </el-card>
      <el-card :class="$style['operation-card']">
        <div slot="header">ABC Dither Amplitude [0, 2047]</div>
        <div v-for="(item, idx) in ditherAmplitude" :class="$style['rw-control']" :key="idx">
          <div :class="$style['rw-label']">{{abcPhaseMapping[idx]}}</div>
          <el-input-number :disabled="item.loading" :class="$style['rw-input']" size="small" v-model="item.value" :min="0" :max="2047" :precision="0" :controls="false"></el-input-number>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="success" plain @click="getDitherAmplitude(idx)">Get</el-button>
          <el-button :loading="item.loading" :class="$style['btn-rw']" size="small" type="danger" plain @click="setDitherAmplitude(idx)">Set</el-button>
        </div>
        <div :class="$style['card-footer']">
        </div>
      </el-card>
      <el-card :class="$style['operation-card']">
        <div slot="header">Dither Settings</div>
        <el-form label-width="120px" label-position="left">
          <el-form-item label="CH">
            <el-select size="small" v-model="ditherSettings.ch">
              <el-option :value="0"></el-option>
              <el-option :value="1"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Phase">
            <el-select size="small" v-model="ditherSettings.phIdx">
              <el-option v-for="(item, idx) in abcPhaseMapping" :key="idx" :value="parseInt(idx)" :label="abcPhaseMapping[idx]"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Frequency">
            <el-input-number size="small" v-model="ditherSettings.freq" :controls="false" :precision="0"></el-input-number>
          </el-form-item>
          <el-form-item label="Amplitude">
            <el-input-number size="small" v-model="ditherSettings.amplitude" :controls="false" :precision="0"></el-input-number>
          </el-form-item>
          <div :class="$style['card-footer']">
            <el-button :loading="ditherSettings.loading" size="small" type="danger" plain @click="setDitherSettings">Set settings</el-button>
          </div>
        </el-form>
      </el-card>
      <!-- <el-card :class="$style['operation-card']">
        <div slot="header">Fine</div>
        <el-checkbox :class="$style['check-box-fine']" v-for="(item, idx) in theta" :key="idx" :disabled="fineLoading" v-model="fine[idx].value" :label="abcPhaseMapping[idx]"></el-checkbox>
        <div :class="$style['card-footer']">
          <el-button :loading="fineLoading" size="small" type="success" plain @click="getFine">Get</el-button>
          <el-button :loading="fineLoading" size="small" type="danger" plain @click="setFine">Set</el-button>
        </div>
      </el-card> -->
    </div>
  </div>
</template>

<script>
export default {
  props: {
    trxIdx: Number
  },
  data () {
    const pidNames = ['XP', 'XI', 'XQ', 'YP', 'YI', 'YQ']
    const pidParams = []
    for (const name of pidNames) {
      pidParams.push({
        name: name,
        p: undefined,
        i: undefined,
        d: undefined,
        iMin: undefined,
        iMax: undefined,
        polarity: undefined,
        method: undefined,
        step: undefined,
        target: undefined,
        theta: undefined
      })
    }
    let abcService
    let algo
    let ditherStatus
    const abcMethod = {
      0: { value: undefined, loading: undefined },
      1: { value: undefined, loading: undefined },
      2: { value: undefined, loading: undefined },
      3: { value: undefined, loading: undefined },
      4: { value: undefined, loading: undefined },
      5: { value: undefined, loading: undefined }
    }
    const abcMethodMapping = {
      0: 'Beating',
      1: 'Fund 1st',
      2: 'Fund 2nd'
    }
    const abcSettings = {
      freqIdx: undefined,
      amplitude: undefined,
      theta: undefined,
      iter: undefined
    }
    const demod = {
      0: { value: undefined, loading: undefined },
      1: { value: undefined, loading: undefined },
      2: { value: undefined, loading: undefined },
      3: { value: undefined, loading: undefined },
      4: { value: undefined, loading: undefined },
      5: { value: undefined, loading: undefined }
    }
    const theta = {
      0: { value: undefined, loading: undefined },
      1: { value: undefined, loading: undefined },
      2: { value: undefined, loading: undefined },
      3: { value: undefined, loading: undefined },
      4: { value: undefined, loading: undefined },
      5: { value: undefined, loading: undefined }
    }
    const target = {
      0: { value: undefined, loading: undefined },
      1: { value: undefined, loading: undefined },
      2: { value: undefined, loading: undefined },
      3: { value: undefined, loading: undefined },
      4: { value: undefined, loading: undefined },
      5: { value: undefined, loading: undefined }
    }
    const ditherAmplitude = {
      0: { value: undefined, loading: undefined },
      1: { value: undefined, loading: undefined },
      2: { value: undefined, loading: undefined },
      3: { value: undefined, loading: undefined },
      4: { value: undefined, loading: undefined },
      5: { value: undefined, loading: undefined }
    }
    const fine = {
      0: { value: undefined },
      1: { value: undefined },
      2: { value: undefined },
      3: { value: undefined },
      4: { value: undefined },
      5: { value: undefined }
    }
    const fineLoading = false
    const ditherSettings = {
      ch: undefined,
      phIdx: undefined,
      freq: undefined,
      amplitude: undefined,
      loading: false
    }
    const abcPhaseMapping = {
      0: 'XP',
      1: 'XI',
      2: 'XQ',
      3: 'YP',
      4: 'YI',
      5: 'YQ'
    }
    return {
      pidParams,
      abcService,
      algo,
      ditherStatus,
      abcMethod,
      abcMethodMapping,
      abcSettings,
      demod,
      theta,
      target,
      ditherAmplitude,
      fine,
      fineLoading,
      ditherSettings,
      abcPhaseMapping
    }
  },
  methods: {
    getParams (pidIdx) {
      this.$rpcClient.request({
        route: ':trx:abc:get-params',
        args: [this.trxIdx, pidIdx]
      }).then((result) => {
        [
          this.pidParams[pidIdx].p,
          this.pidParams[pidIdx].i,
          this.pidParams[pidIdx].d,
          this.pidParams[pidIdx].iMin,
          this.pidParams[pidIdx].iMax,
          this.pidParams[pidIdx].polarity,
          this.pidParams[pidIdx].step,
          this.pidParams[pidIdx].method,
          this.pidParams[pidIdx].target,
          this.pidParams[pidIdx].theta
        ] = result
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setParams (pidIdx) {
      const [p, i, d, iMin, iMax, polarity, step, method, target, theta] = [
        this.pidParams[pidIdx].p,
        this.pidParams[pidIdx].i,
        this.pidParams[pidIdx].d,
        this.pidParams[pidIdx].iMin,
        this.pidParams[pidIdx].iMax,
        parseInt(this.pidParams[pidIdx].polarity),
        this.pidParams[pidIdx].step,
        parseInt(this.pidParams[pidIdx].method),
        this.pidParams[pidIdx].target,
        parseInt(this.pidParams[pidIdx].theta)
      ]
      this.$rpcClient.request({
        route: ':trx:abc:set-params',
        args: [this.trxIdx, pidIdx, p, i, d, iMin, iMax, polarity, step, method, target, theta]
      })
    },
    getServiceState () {
      this.$rpcClient.request({
        route: ':trx:abc:get-service-state',
        args: [this.trxIdx]
      }).then((res) => {
        this.abcService = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setServiceState () {
      this.$rpcClient.request({
        route: ':trx:abc:set-service-state',
        args: [this.trxIdx, this.abcService]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getAlgo () {
      this.$rpcClient.request({
        route: ':trx:abc:get-algo',
        args: [this.trxIdx]
      }).then((res) => {
        this.algo = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setAlgo () {
      this.$rpcClient.request({
        route: ':trx:abc:set-algo',
        args: [this.trxIdx, this.algo]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getDitherState () {
      this.$rpcClient.request({
        route: ':trx:abc:get-dither-state',
        args: [this.trxIdx]
      }).then((res) => {
        this.ditherStatus = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setDitherState () {
      this.$rpcClient.request({
        route: ':trx:abc:set-dither-state',
        args: [this.trxIdx, this.ditherStatus]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getAbcMethod (idx) {
      this.abcMethod[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:get-method',
        args: [this.trxIdx, parseInt(idx)]
      }).then((res) => {
        this.abcMethod[idx].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.abcMethod[idx].loading = false
      })
    },
    setAbcMethod (idx) {
      this.abcMethod[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:set-method',
        args: [this.trxIdx, parseInt(idx), this.abcMethod[idx].value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.abcMethod[idx].loading = false
      })
    },
    getSettings () {
      this.$rpcClient.request({
        route: ':trx:abc:get-settings',
        args: [this.trxIdx]
      }).then((res) => {
        [this.abcSettings.freqIdx, this.abcSettings.amplitude, this.abcSettings.theta, this.abcSettings.iter] = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setSettings () {
      this.$rpcClient.request({
        route: ':trx:abc:set-settings',
        args: [this.trxIdx, this.abcSettings.freqIdx, this.abcSettings.amplitude, this.abcSettings.theta, this.abcSettings.iter]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getFine () {
      this.fineLoading = true
      this.$rpcClient.request({
        route: ':trx:abc:get-fine',
        args: [this.trxIdx]
      }).then((res) => {
        console.log(res)
        for (const i in this.fine) {
          this.fine[i].value = res[i]
        }
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.fineLoading = false
      })
    },
    setFine () {
      this.fineLoading = true
      const fineVals = []
      for (const i in this.fine) {
        fineVals.push(this.fine[i].value)
      }
      this.$rpcClient.request({
        route: ':trx:abc:set-fine',
        args: [this.trxIdx, fineVals]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.fineLoading = false
      })
    },
    getDemod (idx) {
      this.demod[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:get-demod',
        args: [this.trxIdx, parseInt(idx)]
      }).then((res) => {
        this.demod[idx].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.demod[idx].loading = false
      })
    },
    getTheta (idx) {
      this.theta[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:get-theta',
        args: [this.trxIdx, parseInt(idx)]
      }).then((res) => {
        this.theta[idx].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.theta[idx].loading = false
      })
    },
    setTheta (idx) {
      this.theta[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:set-theta',
        args: [this.trxIdx, parseInt(idx), this.theta[idx].value]
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.theta[idx].loading = false
      })
    },
    getTarget (idx) {
      this.target[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:get-target',
        args: [this.trxIdx, parseInt(idx)]
      }).then((res) => {
        this.target[idx].value = res
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.target[idx].loading = false
      })
    },
    setTarget (idx) {
      this.target[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:set-target',
        args: [this.trxIdx, parseInt(idx), this.target[idx].value]
      }).catch((err) => {
        this.$alertError(err)
      }).finally(() => {
        this.target[idx].loading = false
      })
    },
    getDitherAmplitude (idx) {
      this.ditherAmplitude[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:get-dither-amplitude',
        args: [this.trxIdx, parseInt(idx)]
      }).then(res => {
        this.ditherAmplitude[idx].value = res
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.ditherAmplitude[idx].loading = false
      })
    },
    setDitherAmplitude (idx) {
      this.ditherAmplitude[idx].loading = true
      this.$rpcClient.request({
        route: ':trx:abc:set-dither-amplitude',
        args: [this.trxIdx, parseInt(idx), this.ditherAmplitude[idx].value]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.ditherAmplitude[idx].loading = false
      })
    },
    setDitherSettings () {
      this.ditherSettings.loading = true
      this.$rpcClient.request({
        route: ':trx:abc:set-dither-setting',
        args: [this.trxIdx, this.ditherSettings.ch, this.ditherSettings.phIdx, this.ditherSettings.freq, this.ditherSettings.amplitude]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.ditherSettings.loading = false
      })
    }
  }
}
</script>

<style lang="scss" module>
  .wrapper {
    padding: 8px;
    margin-right: -8px;
  }
  .pid-table {
    margin: 8px;
  }
  .pid-table :global(.el-table__fixed) {
    // fix that el-table fixed column covers the horizontal scroll bar
    height: auto !important;
    bottom: 8px;
  }
  .pid-table :global(.el-table__body-wrapper[class*=is-scrolling-none]+.el-table__fixed) {
    // fix that el-table fixed column covers the horizontal scroll bar
    bottom: 0;
  }
  .pid-table :global(.el-table__fixed .el-table__fixed-body-wrapper) {
    // fix that el-table fixed column covers the horizontal scroll bar
    height: auto !important;
    bottom: 0;
  }
  .pid-table::before {
    display: none;
  }
  .pid-input:global(.el-input-number--small) {
    width: 60px;
  }
  .pid-input:global(.el-input-number.is-without-controls .el-input__inner) {
    padding-left: 8px;
    padding-right: 8px;
  }
  .wrapper :global(.el-form-item) {
    margin: 10px 0;
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
  .line-item {
    margin-right: 8px;
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
  .card-wrapper {
    display: flex;
    flex-wrap: wrap;
  }
  .check-box-fine {
    margin-top: 5px;
    margin-bottom: 5px;
  }
  .card-footer {
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 15px;
  }
  .operation-card :global(.el-form-item) {
    margin: 2px 0;
  }
</style>
