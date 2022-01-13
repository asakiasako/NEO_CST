<template>
  <el-container :class="$style.container">
    <el-main :class="$style.main">
      <img src="@/assets/setup.png"/>
    </el-main>
    <el-aside :class="$style.aside" width="320px">
      <div :class="$style['config-panel']">
        <div :class="$style['config-panel-main']">
          <el-divider content-position="center">Transceivers</el-divider>
          <el-form ref="form-trx" label-position="left" label-width="100px">
            <el-form-item v-for="(trx, idx) in trxList" :key="idx">
              <div slot="label">
                <div :class="$style['inst-state-wrapper']">
                  <el-icon
                    v-if="trx.status === 'unavailable'"
                    :class="[$style['inst-state'], $style['inst-state-unavailable'], 'el-icon-fas', 'fa-times-circle']"
                  ></el-icon>
                  <el-icon
                    v-else-if="trx.status === 'available'"
                    :class="[$style['inst-state'], $style['inst-state-available'], 'el-icon-fas', 'fa-check-circle']"
                  ></el-icon>
                  <el-icon
                    v-else-if="trx.status === 'checking'"
                    :class="[$style['inst-state'], $style['inst-state-checking'], 'el-icon-fas', 'fa-spinner', 'fa-spin']"
                  ></el-icon>
                  <el-icon
                    v-else
                    :class="[$style['inst-state'], $style['inst-state-unknown'], 'el-icon-fas', 'fa-question-circle']"
                  ></el-icon>
                </div>
                <span>{{`TRX${idx+1}`}}</span>
              </div>
              <el-input :disabled="isCheckingConnection" size="medium" :class="$style['input-trx']" v-model="trxList[idx].address" placeholder="IP:port" @change="saveTrxList"></el-input>
            </el-form-item>
            <div :class="$style['line-wrapper']">
              <el-button :class="$style['line-button']" :disabled="isCheckingConnection" size="medium" type="success" plain @click="addTrx">Add TRX</el-button>
              <el-button :class="$style['line-button']" :disabled="(trxList.length <= 1) || isCheckingConnection" size="medium" type="danger" plain @click="removeTrx">Remove TRX</el-button>
            </div>
            <el-form-item v-for="(item, key) in trxConfig" :key="key" :label="key">
              <el-select size="medium" v-model="trxConfig[key]" @change="setTrxConfig(key, $event)">
                <el-option v-for="(trx, i) in trxList" :key="i" :label="`TRX${i+1}`" :value="i+1"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <el-divider content-position="center">Instruments</el-divider>
          <el-form ref="form-ins" label-position="left" label-width="100px">
            <el-form-item v-for="(item, key) in instrMapping" :key="key">
              <div slot="label">
                <div :class="$style['inst-state-wrapper']">
                  <el-icon
                    v-if="item.status === 'unavailable'"
                    :class="[$style['inst-state'], $style['inst-state-unavailable'], 'el-icon-fas', 'fa-times-circle']"
                  ></el-icon>
                  <el-icon
                    v-else-if="item.status === 'available'"
                    :class="[$style['inst-state'], $style['inst-state-available'], 'el-icon-fas', 'fa-check-circle']"
                  ></el-icon>
                  <el-icon
                    v-else-if="item.status === 'checking'"
                    :class="[$style['inst-state'], $style['inst-state-checking'], 'el-icon-fas', 'fa-spinner', 'fa-spin']"
                  ></el-icon>
                  <el-icon
                    v-else
                    :class="[$style['inst-state'], $style['inst-state-unknown'], 'el-icon-fas', 'fa-question-circle']"
                  ></el-icon>
                </div>
                <span>{{key}}</span>
              </div>
              <el-select :disabled="isCheckingConnection" @change="onSelectInstRes($event, key)" size="medium" v-model="instrMapping[key].label">
                <el-option
                  v-for="option in item.choices"
                  :key="option"
                  :label="option"
                  :value="option"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </div>
        <div :class="$style['config-panel-footer']">
          <el-button :class="$style['btn-check-connection']" type="primary" round @click="checkConnection">Check Connection</el-button>
        </div>
      </div>
    </el-aside>
  </el-container>
</template>

<script>
export default {
  data () {
    const trxList = [{
      address: null,
      status: 'unknown'
    }]
    const trxConfig = {}
    const instrMapping = {
    }
    const isCheckingConnection = false
    return {
      trxList,
      trxConfig,
      instrMapping,
      isCheckingConnection
    }
  },
  methods: {
    loadTrxList () {
      this.$rpcClient.request({
        route: ':config:get',
        args: [':transceiver:list']
      }).then(res => {
        if (res) {
          for (const idx in res) {
            res[idx].status = 'unknown'
          }
          this.trxList = res
        }
      }).catch(err => {
        this.$alertError(err)
      })
    },
    saveTrxList () {
      const trxList = this.trxList
      const saveList = []
      for (const i of trxList) {
        saveList.push({ address: i.address })
      }
      this.$rpcClient.request({
        route: ':config:set',
        args: [':transceiver:list', saveList]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    getTrxFields () {
      this.$rpcClient.request({
        route: ':loop-test:get-trx-config-fields'
      }).then((result) => {
        console.log(result)
        const mapping = {}
        for (const i of result) {
          mapping[i] = null
        }
        this.trxConfig = mapping
        for (const i in this.trxConfig) {
          this.getTrxConfig(i)
        }
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getTrxConfig (field) {
      this.$rpcClient.request({
        route: ':config:get',
        args: [`:transceiver:${field}`]
      }).then((result) => {
        this.trxConfig[field] = result
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setTrxConfig (field, value) {
      this.$rpcClient.request({
        route: ':config:set',
        args: [`:transceiver:${field}`, value]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    addTrx () {
      this.trxList.push({ address: null })
      this.saveTrxList()
    },
    removeTrx () {
      this.trxList.pop()
      this.saveTrxList()
    },
    refreshInstMap () {
      this.$rpcClient.request({
        route: ':instrument:mapping:get'
      }).then((result) => {
        const instMap = result
        for (const key in instMap) {
          instMap[key].status = 'unknown'
        }
        this.instrMapping = instMap
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    onSelectInstRes (value, key) {
      this.$rpcClient.request({
        route: ':instrument:mapping:set',
        args: [key, value]
      }).then(() => {
        this.refreshInstMap()
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    checkConnection () {
      this.isCheckingConnection = true

      for (const info of this.trxList) {
        info.status = 'unknown'
      }
      for (const key in this.instrMapping) {
        this.instrMapping[key].status = 'unknown'
      }

      const self = this
      async function checkConnectionAction () {
        for (const i in self.trxList) {
          const idx = parseInt(i)
          try {
            self.trxList[idx].status = 'checking'
            const value = await self.$rpcClient.request({
              route: ':trx:check-connection',
              args: [idx + 1]
            })
            self.trxList[idx].status = value ? 'available' : 'unavailable'
          } catch (err) {
            self.trxList[idx].status = 'unknown'
            self.$alertError(err)
          }
        }
        for (const key in self.instrMapping) {
          try {
            self.instrMapping[key].status = 'checking'
            const value = await self.$rpcClient.request({
              route: ':instrument:status:check-connection',
              args: [key]
            })
            self.instrMapping[key].status = value ? 'available' : 'unavailable'
          } catch (err) {
            self.instrMapping[key].status = 'unknown'
            self.$alertError(err)
          }
        }

        self.isCheckingConnection = false
      }
      checkConnectionAction()
    }
  },
  activated () {
    this.loadTrxList()
    this.getTrxFields()
    this.refreshInstMap()
  }
}
</script>

<style lang='scss' module>
.container {
  height: 100%;
}
.main:global(.el-main) {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0;
}
.main img {
  max-width: 100%;
}
.aside {
  border-left: 1px solid $border-color-base;
}
.aside :global(.el-divider--horizontal) {
  background: $color-white;
  border-bottom: 1px solid $border-color-base;
}
.config-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.config-panel-main {
  flex-grow: 1;
  overflow: auto;
  height: 10px;
  padding: 0 16px;
}
.line-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}
.line-button {
  flex-grow: 1;
}
.config-panel-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  background: $color-white;
  padding: 8px;
  border-top: 1px solid $border-color-light;
}
.input-trx-ip {
  width: 100px;
}
.input-trx-port {
  width: 100px;
}
.inst-state-wrapper {
  display: inline-block;
  margin-right: 8px;
}
.inst-state-available {
  color: $color-success;
}
.inst-state-unavailable {
  color: $color-danger;
}
.inst-state-checking {
  color: $color-primary
}
.inst-state-unknown {
  color: $color-warning;
}
.config-panel :global(.el-form-item) {
  margin-bottom: 16px;
}
.btn-check-connection {
  width: 100%;
}
</style>
