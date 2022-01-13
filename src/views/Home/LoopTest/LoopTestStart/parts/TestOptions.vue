<template>
  <div :class="$style.wrapper">
    <el-form label-width="180px" label-position="left" size="small">
      <el-form-item :class="$style['form-item']" v-for="(item, key) in optionsData" :key="key" :label="key">
        <el-input-number
          :key="key"
          v-if="item.type === 'number'"
          size="small"
          v-model="item.value"
          :min="'min' in item ? item.min : -Infinity"
          :max="'max' in item ? item.max : Infinity"
          :step="'step' in item ? item.step : 1"
          :controls="'step' in item"
          :precision="'precision' in item ? item.precision : undefined"
          @change="setOption(key, $event)"
        ></el-input-number>
        <el-input
          :key="key"
          v-else-if="item.type === 'input'"
          size="small"
          v-model="item.value"
          @change="setOption(key, $event)"
        ></el-input>
        <el-select
          :key="key"
          v-else-if="item.type === 'select'"
          size="small"
          v-model="item.value"
          @change="setOption(key, $event)"
        >
          <el-option v-for="(option, index) in item.options" :key="index" :label="option" :value="option"></el-option>
        </el-select>
        <el-switch
          :key="key" v-else-if="item.type === 'bool'"
          size="small"
          v-model="item.value"
          @change="setOption(key, $event)"
        ></el-switch>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data () {
    const optionsData = {}
    return {
      optionsData
    }
  },
  methods: {
    loadOptions () {
      this.$rpcClient.request({
        route: ':loop-test:get-options-info'
      }).then((res) => {
        for (const key in res) {
          res[key].value = undefined
        }
        this.optionsData = res
        for (const key in res) {
          this.getOption(key)
        }
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    getOption (key) {
      this.$rpcClient.request({
        route: ':loop-test:get-option',
        args: [key]
      }).then((res) => {
        this.optionsData[key].value = res
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setOption (key, value) {
      this.$rpcClient.request({
        route: ':loop-test:set-option',
        args: [key, value]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    onNextStep () {
      this.$router.push({ name: 'confirm-page' })
    },
    onLastStep () {
      this.$router.push({ name: 'output-params' })
    }
  },
  created () {
    this.$on('next-step', this.onNextStep)
    this.$on('last-step', this.onLastStep)
  },
  activated () {
    this.loadOptions()
  }
}
</script>

<style lang="scss" module>
.wrapper {
  display: flex;
  flex-direction: column;
}
.form-item :global(.el-input) {
  max-width: 400px;
}
.form-item :global(.el-input-number), .form-item :global(.el-select) {
  width: 200px;
}
</style>
