<template>
  <div :class="$style.wrapper">
    <div :class="$style.section">
      <el-button size="small" type="primary" plain @click="saveParametersToFile">Save Parameters to File</el-button>
      <div :class="$style.title">Loops</div>
      <el-table
        :data="loopConfigData"
        size="small"
        border
      >
        <el-table-column
          align="center"
          type="index"
          width="45"
        ></el-table-column>
        <el-table-column
          prop="loopSelect"
          label="Loop"
          min-width="180"
        ></el-table-column>
        <el-table-column
          prop="start"
          label="Start"
          min-width="60"
        ></el-table-column>
        <el-table-column
          prop="stop"
          label="Stop"
          min-width="60"
        ></el-table-column>
        <el-table-column
          prop="step"
          label="Step"
          min-width="60"
        ></el-table-column>
        <el-table-column
          prop="additional"
          label="Additional"
          min-width="150"
        ></el-table-column>
        <el-table-column
          prop="mode"
          label="Mode"
          min-width="72"
        ></el-table-column>
        <el-table-column
          prop="cycles"
          label="Cycles"
          min-width="72"
        ></el-table-column>
        <el-table-column
          prop="delay"
          label="Delay (sec)"
          min-width="80"
        ></el-table-column>
      </el-table>
    </div>
    <div :class="$style.section">
      <div :class="$style.title">Output Params</div>
      <div :class="$style['tag-wrapper']">
        <el-tag :class="$style['param-tag']" size="medium" v-for="param in outputParams" :key="param">{{param}}</el-tag>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    const loopConfigData = []
    const outputParams = []
    return {
      loopConfigData,
      outputParams
    }
  },
  methods: {
    saveParametersToFile () {
      this.$electron.ipcRenderer.invoke('show-save-dialog', {
        filters: [
          { name: 'Json', extensions: ['json'] }
        ]
      }).then(({ path }) => {
        if (path) {
          this.$rpcClient.request({
            route: ':loop-test:save-params-to-file',
            args: [path]
          }).then((res) => {
            this.$alert('Save to file success.')
          }).catch((err) => {
            this.$alertError(err)
          })
        }
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    loadConfigurations () {
      const promises = [
        this.$rpcClient.request({
          route: ':loop-test:get-loop-config'
        }),
        this.$rpcClient.request({
          route: ':loop-test:get-output-params'
        })
      ]
      Promise.all(promises).then(res => {
        [this.loopConfigData, this.outputParams] = res
      }).catch(err => {
        this.$alertError(err)
      })
    },
    onNextStep () {
      console.log('next-step')
      this.$router.push({ name: 'running-page' })
    },
    onLastStep () {
      console.log('last-step')
      this.$router.push({ name: 'output-params' })
    }
  },
  created () {
    this.$on('next-step', this.onNextStep)
    this.$on('last-step', this.onLastStep)
  },
  activated () {
    this.loadConfigurations()
    console.log([this.loopConfigData, this.outputParams])
  }
}
</script>

<style lang='scss' module>
.wrapper {
  padding: 0 20px;
}
.section {
  margin-bottom: 20px;
}
.title {
  color: $color-text-secondary;
  font-size: 1.2em;
  margin: 12px 0;
}
.tag-wrapper {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -5px;
}
.param-tag {
  margin: 5px;
}
.section :global(.el-table th.gutter) {
    display: table-cell!important;
}
.section :global(.el-table colgroup.gutter) {
    display: table-cell!important;
}
.section :global(.el-table--group::after), .section :global(.el-table--border::after) {
  width: 0;
}
</style>
