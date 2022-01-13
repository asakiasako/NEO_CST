<template>
  <div :class="$style.wrapper">
    <draggable
      v-model="loopConfigData"
      v-bind="dragOptions"
      :handle="'.'+$style['drag-region']"
      @start="drag = true"
      @end="drag = false"
    >
      <transition-group type="transition" :name="!drag ? 'flip-list' : null">
        <div v-for="(item, idx) in loopConfigData" :key="item.id" :class="$style['loop-config-line']">
          <div :class="$style['drag-region']">
            <i :class="$style['drag-bar']" class="el-icon-fas fa-bars"></i>
            <span :class="$style['index']">{{idx+1}}</span></div>
          <el-select :class="$style['select-loop']" :popper-class="$style['select-options']" size="small" v-model="item.loopSelect" placeholder="Select loop">
            <el-option
              v-for="opt in loopOptions"
              :key="opt"
              :label="opt"
              :value="opt"
            >
            </el-option>
          </el-select>
          <el-input-number :class="$style['input-range']" size="small" v-model="item.start" placeholder="Start" :controls="false" :min="-Infinity" :max="Infinity"></el-input-number>
          <el-input-number :class="$style['input-range']" size="small" v-model="item.stop" placeholder="Stop" :controls="false" :min="-Infinity" :max="Infinity"></el-input-number>
          <el-input-number :class="$style['input-range']" size="small" v-model="item.step" placeholder="Step" :controls="false" :min="-Infinity" :max="Infinity"></el-input-number>
          <el-input :class="$style['input-additional']" size="small" v-model="item.additional" placeholder="Additional"></el-input>
          <el-select :class="$style['select-mode']" size="small" v-model="item.mode" placeholder="Mode">
            <el-option value="obverse" label="Min->Max"></el-option>
            <el-option value="reverse" label="Max->Min"></el-option>
            <el-option value="random" label="Random"></el-option>
          </el-select>
          <el-input-number :class="$style['input-cycles']" size="small" v-model="item.cycles" placeholder="Cycles" controls-position="right" :min="1" :precision="0"></el-input-number>
          <el-input-number :class="$style['input-delay']" size="small" v-model="item.delay" placeholder="Delay(s)" :controls="false" :min="-Infinity" :max="Infinity"></el-input-number>
          <el-button
            size="small" :class="$style['btn-remove']" type="text"
            icon="el-icon-fas fa-minus-circle"
            :disabled="loopConfigData.length<=1"
            @click="removeConfigLine(idx)"
          ></el-button>
        </div>
      </transition-group>
    </draggable>
    <div :class="$style['button-region']"><el-button
      type="info" plain size="small"
      @click="addNewConfigLine"
    >Add new line</el-button></div>
  </div>

</template>

<script>
import draggable from 'vuedraggable'

export default {
  components: {
    draggable
  },
  data () {
    const createConfigLine = () => {
      return {
        id: new Date().getTime(),
        loopSelect: null,
        start: undefined,
        stop: undefined,
        step: undefined,
        additional: null,
        mode: 'obverse',
        cycles: 1,
        delay: undefined
      }
    }
    const loopConfigData = [
      createConfigLine()
    ]
    const loopOptions = []
    return {
      drag: false,
      createConfigLine,
      loopConfigData,
      loopOptions
    }
  },
  computed: {
    dragOptions () {
      return {
        animation: 200,
        group: 'description',
        disabled: false,
        ghostClass: 'ghost'
      }
    }
  },
  methods: {
    getLoopList () {
      this.$rpcClient.request({
        route: ':loop-test:get-loop-list'
      }).then((result) => {
        this.loopOptions = result
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    addNewConfigLine () {
      this.loopConfigData.push(this.createConfigLine())
    },
    removeConfigLine (idx) {
      this.loopConfigData.splice(idx, 1)
    },
    loadLoopConfig () {
      this.$rpcClient.request({
        route: ':loop-test:get-loop-config'
      }).then(res => {
        // replace null with undefined, so empty config will not turn to number
        if (res) {
          for (const line of res) {
            for (const k in line) {
              if (line[k] === null) {
                line[k] = undefined
              }
            }
          }
          this.loopConfigData = res
        }
      }).catch(err => {
        this.$alertError(err)
      })
    },
    checkLoopConfig () {
      const loopConfigData = this.loopConfigData
      for (const idx in loopConfigData) {
        const configLine = loopConfigData[idx]
        const { loopSelect, start, stop, step, additional } = configLine
        if (!loopSelect) {
          this.$alert(`Please select parameter for loop ${parseInt(idx) + 1}`, 'ERROR', {
            confirmButtonText: 'OK',
            type: 'error'
          })
          return false
        }

        if (start !== undefined || stop !== undefined || step !== undefined) {
          if (start === undefined || stop === undefined || step === undefined || ((stop - start) * step < 0) || step === 0) {
            this.$alert(`Invalid start, stop, step value for loop ${parseInt(idx) + 1}`, 'ERROR', {
              confirmButtonText: 'OK',
              type: 'error'
            })
            return false
          }
        }

        if (additional && additional.trim()) {
          const reg = /^(\s*-?\d+(\.\d+)?\s*,)*(\s*-?\d+(\.\d+)?\s*)$/
          if (!reg.test(additional)) {
            this.$alert(`Invalid additional field value for loop ${parseInt(idx) + 1}. Should be numbers seperated by comma.`, 'ERROR', {
              confirmButtonText: 'OK',
              type: 'error'
            })
            return false
          }
        }
        if (!((additional && additional.trim()) || (start !== undefined))) {
          this.$alert(`No valid input values for loop ${parseInt(idx) + 1}.`, 'ERROR', {
            confirmButtonText: 'OK',
            type: 'error'
          })
          return false
        }
      }
      return true
    },
    saveLoopConfig () {
      this.$rpcClient.request({
        route: ':loop-test:save-loop-config',
        args: [this.loopConfigData]
      }).catch(err => {
        this.$alertError(err)
      })
    },
    onLastStep () {
      this.$router.push({ name: 'loop-test' })
    },
    onNextStep () {
      if (this.checkLoopConfig()) {
        console.log('next-step')
        this.saveLoopConfig()
        this.$router.push({ name: 'output-params' })
      }
    }
  },
  created () {
    this.$on('last-step', this.onLastStep)
    this.$on('next-step', this.onNextStep)
  },
  activated () {
    console.log('activated')
    this.getLoopList()
    this.loadLoopConfig()
  }
}
</script>

<style lang="scss" module>
  .wrapper {
    padding: 10px 0;
  }
  .loop-config-line {
    display: flex;
    padding: 6px 20px;
    margin-bottom: 6px;
    background: $color-white;
  }
  .loop-config-line:global(.sortable-chosen) {
    box-shadow: 0 0 6px $color-text-placeholder;
  }
  .drag-region {
    display: flex;
    color: $color-text-secondary;
    justify-content: center;
    align-items: center;
    cursor: grab;
  }
  .drag-bar {
    padding-right: 5px;
    flex-grow: 0;
    width: 20px;
    font-size: 1em;
  }
  .drag-region .index {
    width: 20px;
    flex-grow: 0;
    text-align: center;
  }
  .select-loop {
    width: 240px;
  }
  .input-range:global(.el-input-number) {
    width: 90px;
  }
  .input-delay:global(.el-input-number) {
    width: 120px;
  }
  .input-additional:global(.el-input) {
    width: 240px;
  }
  .btn-reverse :global(.el-checkbox-button__inner) {
    padding: 8px 20px;
    width: 94px;
    border: 1px solid #a7e9b7;
    background: #e9faed;
    color: $color-success;
    border-radius: 4px;
    transition: none;
  }
  .btn-reverse :global(.el-checkbox-button__inner:hover) {
    color: $color-success;
  }
  .btn-reverse:global(.el-checkbox-button.is-focus .el-checkbox-button__inner) {
    border: 1px solid #a7e9b7;
  }
  .btn-reverse:global(.el-checkbox-button.is-checked .el-checkbox-button__inner) {
    border: 1px solid #fcbdbb;
    background: #feeeee;
    color: $color-danger;
    box-shadow: none;
  }
  .loop-config-line > * {
    margin-right: 10px;
  }
  .loop-config-line > *:last-child {
    margin-right: 0;
  }
  .btn-remove {
    width: 40px;
    flex-shrink: 0;
  }
  .btn-remove:global(.el-button--text) {
    color: $color-danger;
  }
  .btn-remove:global(.el-button--text):hover,
  .btn-remove:global(.el-button--text):focus {
    color: $color-danger;
    opacity: 0.8;
    background: $color-danger-light;
  }
  .button-region {
    padding: 6px 20px;
  }
  .select-options {
    width: 760px;
  }
  .select-options :global(.el-scrollbar__wrap) {
    height: 274px;
  }
  .select-options :global(.el-select-dropdown__list) {
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    height: 100%;
  }
  .select-options :global(.el-select-dropdown__item) {
    width: 25%;
  }
  .input-cycles:global(.el-input-number.is-controls-right .el-input__inner) {
    padding-left: 5px;
    padding-right: 40px;
  }
</style>
