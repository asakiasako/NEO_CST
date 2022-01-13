<template>
  <div class="inst-item" :class="onRemove ? 'on-remove' : ''">
    <component
      :is="currentTabComponent"
      ref="inst-item-inner"
      :alias="alias"
      :inst-type="instType"
      :label="label"
    ></component>
    <div v-if="onRemove" class="cover-remove">
      <div class="btn-remove" @click="removeInstrument">
        <i class="el-icon-error"></i>
      </div>
    </div>
  </div>
</template>

<script>
import OpmPanel from './subPanels/OpmPanel.vue'
import VoaPanel from './subPanels/VoaPanel.vue'
import OsaPanel from './subPanels/OsaPanel.vue'
import OtfPanel from './subPanels/OtfPanel.vue'

export default {
  props: ['alias', 'instType', 'label', 'onRemove'],
  components: {
    OpmPanel,
    VoaPanel,
    OsaPanel,
    OtfPanel
  },
  data () {
    const instPanelMap = {
      OPM: OpmPanel,
      VOA: VoaPanel,
      OSA: OsaPanel,
      OTF: OtfPanel
    }
    return {
      instPanelMap
    }
  },
  computed: {
    currentTabComponent () {
      if (this.instType) {
        return this.instPanelMap[this.instType]
      } else {
        return null
      }
    }
  },
  methods: {
    async removeInstrument () {
      await this.$refs['inst-item-inner'].disconnect()
      this.$emit('removed')
    }
  }
}
</script>

<style lang="scss" scoped>
  .cover-remove {
    z-index: 10;
    display: flex;
    align-items: center;
    flex-direction: row-reverse;
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    background: rgba(255,255,255,0.8);
    border-radius: 5px;
  }
  .btn-remove {
    color: $color-danger;
    font-size: 20px;
    height: 100%;
    width: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  .btn-remove:hover {
    background: rgba(144,147,153,0.1);
  }
</style>

<style lang="scss">
  .inst-item {
    width: 320px;
    border: 1px solid $border-color-light;
    border-radius: 5px;
    margin: 8px;
    padding: 8px 12px;
    position: relative;
  }
  .inst-item.on-remove {
    border-color: $border-color-lighter;
  }
  .inst-item .cfg-item-wrapper {
    display: flex;
  }
  .inst-item .cfg-item-unit {
    margin-left: 10px;
  }
</style>
