<template>
  <div :class="$style.wrapper">
    <el-checkbox :class="$style['check-all']" :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">Check All</el-checkbox>
    <div :class="$style['wrapper-params']" ref="wrapper-params" @mousewheel="onParamsScroll">
      <el-checkbox-group :class="$style['output-param-group']" v-model="checkedParams" @change="handleCheckedParamsChange">
        <el-checkbox :class="$style['output-param']" v-for="p in outputParams" :label="p" :key="p">{{p}}</el-checkbox>
      </el-checkbox-group>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    let checkAll
    const outputParams = []
    const checkedParams = []
    return {
      checkAll,
      outputParams,
      checkedParams
    }
  },
  computed: {
    isIndeterminate () {
      const checkedCount = this.checkedParams.length
      const allCount = this.outputParams.length
      return (checkedCount > 0) && (checkedCount < allCount)
    }
  },
  methods: {
    onParamsScroll (event) {
      const deltaY = event.deltaY
      this.$refs['wrapper-params'].scrollLeft += deltaY
    },
    handleCheckAllChange (val) {
      this.checkedParams = val ? this.outputParams : []
    },
    handleCheckedParamsChange (value) {
      this.checkAll = value.length === this.outputParams.length
    },
    getOutputList () {
      this.$rpcClient.request({
        route: ':loop-test:get-output-list'
      }).then((result) => {
        this.outputParams = result
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    loadOutputParams () {
      this.$rpcClient.request({
        route: ':loop-test:get-output-params'
      }).then(res => {
        if (res) {
          const params = []
          for (const i of res) {
            if (this.outputParams.includes(i)) params.push(i)
          }
          this.checkedParams = params
        }
      }).catch(err => {
        console.log(err)
      })
    },
    saveOutputParams () {
      this.$rpcClient.request({
        route: ':loop-test:save-output-params',
        args: [this.checkedParams]
      }).catch(err => {
        console.log(err)
      })
    },
    onNextStep () {
      if (this.checkedParams.length === 0) {
        this.$alert('You should select at least 1 output param.', 'ERROR', {
          confirmButtonText: 'OK',
          type: 'error'
        })
      } else {
        this.saveOutputParams()
        this.$router.push({ name: 'confirm-page' })
      }
    },
    onLastStep () {
      this.saveOutputParams()
      this.$router.push({ name: 'loop-config' })
    }
  },
  created () {
    this.$on('next-step', this.onNextStep)
    this.$on('last-step', this.onLastStep)
  },
  activated () {
    console.log('activated')
    this.getOutputList()
    this.loadOutputParams()
  }
}
</script>

<style lang="scss" module>
.wrapper {
  padding: 0 30px;
  display: flex;
  height: 100%;
  flex-direction: column;
}
.check-all {
  width: 96px;
  margin-bottom: 10px;
  margin-left: 10px;
}
.wrapper-params {
  height: 10px;
  flex-grow: 1;
  overflow: auto;
  border-top: 1px solid $border-color-light;
  border-bottom: 1px solid $border-color-light;
}
.output-param-group {
  height: 100%;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  padding: 10px 0;
}
.output-param {
  min-width: 300px;
  margin: 2px 0 !important;
  padding: 5px 10px;
}
.output-param:hover {
  background: $background-color-base;
}
</style>
