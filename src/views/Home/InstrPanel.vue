<template>
  <div :class="$style.wrapper">
    <inst-item v-for="(type, key) in instrMap" :key="key" :inst-type="type" :label="key"></inst-item>
    <el-card :class="$style['global-control']" shadow="never">
      <span slot="header">Global control</span>
      <div :class="$style['set-target-panel']">
        <div :class="$style['set-line']">
          <el-button type="success" size="small" plain @click="connectAll">Connect All</el-button>
          <el-button type="danger" size="small" plain @click="disconnectAll">Disonnect All</el-button>
        </div>
        <div :class="$style['set-line']">
          <el-input-number size="small" v-model="globalFreq" :controls="false"></el-input-number>
          <el-button size="small" :class="$style['btn-set']" type="primary" plain @click="setAllFrequency">Set All Freq</el-button>
        </div>
        <div :class="$style['set-line']">
          <el-input-number size="small" v-model="osnrValue" controls-position="right" :min="1" :max="50" :step="0.1"></el-input-number>
          <el-button size="small" :loading="loading" :class="$style['btn-set']" @click="setOsnr" type="primary" plain>Set OSNR</el-button>
        </div>
        <div :class="$style['set-line']">
          <el-input-number size="small" v-model="pinValue" controls-position="right" :min="-30" :max="20" :step="0.1"></el-input-number>
          <el-button size="small" :loading="loading" :class="$style['btn-set']" @click="setPin" type="primary" plain>Set Pin</el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import InstItem from '@/components/InstPanel/InstItem.vue'

export default {
  components: {
    InstItem
  },
  data () {
    const instrMap = {
    }
    const loading = false
    const osnrValue = 20
    const pinValue = -7
    const globalFreq = 191.1
    return {
      loading,
      instrMap,
      osnrValue,
      pinValue,
      globalFreq
    }
  },
  methods: {
    setOsnr () {
      this.loading = true
      this.$rpcClient.request({
        route: ':instrument:panel:set-osnr',
        args: [this.osnrValue]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.loading = false
      })
    },
    setPin () {
      this.loading = true
      this.$rpcClient.request({
        route: ':instrument:panel:set-pin',
        args: [this.pinValue]
      }).catch(err => {
        this.$alertError(err)
      }).finally(() => {
        this.loading = false
      })
    },
    connectAll () {
      this.$bus.$emit('inst-panel:connect-all')
    },
    disconnectAll () {
      this.$bus.$emit('inst-panel:disconnect-all')
    },
    setAllFrequency () {
      const freq = this.globalFreq
      this.$bus.$emit('inst-panel:set-all-frequency', freq)
    }
  },
  activated () {
    this.$rpcClient.request({
      route: ':setting:get',
      args: ['OSNR__Set-up']
    }).then((res) => {
      if (res === 'ATT1 and ATT2') {
        this.$set(this.$data, 'instrMap', {
          ATT1: 'VOA',
          ATT2: 'VOA',
          ATT3: 'VOA',
          OPM1: 'OPM',
          OPM2: 'OPM',
          OSA: 'OSA',
          OTF: 'OTF'
        })
      } else if (res === 'ATT1 Only') {
        this.$set(this.$data, 'instrMap', {
          ATT1: 'VOA',
          ATT3: 'VOA',
          OPM1: 'OPM',
          OPM2: 'OPM',
          OSA: 'OSA',
          OTF: 'OTF'
        })
      } else if (res === 'ATT2 Only') {
        this.$set(this.$data, 'instrMap', {
          ATT2: 'VOA',
          ATT3: 'VOA',
          OPM1: 'OPM',
          OPM2: 'OPM',
          OSA: 'OSA',
          OTF: 'OTF'
        })
      } else {
        throw Error(`Invalid OSNR Set-up information: ${res}`)
      }
    }).catch((err) => {
      this.$alertError(err)
    })
  }
}
</script>

<style lang='scss' module>
.wrapper {
  height: 100%;
  padding: 16px;
  display: inline-flex;
  flex-direction: column;
  flex-wrap: wrap;
}
.set-target-panel {
  margin: 8px;
}
.set-line {
  margin-bottom: 10px;
}
.set-line > * {
  margin-right: 5px;
}
.btn-set {
  width: 108px;
}
.global-control:global(.el-card) {
  border-color: $border-color-light;
  width: 320px;
  margin: 8px;
}
.global-control:global(.el-card .el-card__header) {
  padding-top: 10px;
  padding-bottom: 10px;
}
</style>
