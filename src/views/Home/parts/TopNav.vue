<template>
  <el-menu :class="$style['top-nav']" :default-active="defaultActive" :collapse="true" router>
    <el-tooltip v-for="item in menuItems" :key="item.index" :popper-class="$style['top-nav-popup']" effect="light" :content="item.title" placement="right" :enterable="false">
      <el-menu-item :index="item.index">
        <i :class="item.icon"></i>
      </el-menu-item>
    </el-tooltip>
  </el-menu>
</template>

<script>
export default {
  name: 'top-nav',
  data: function () {
    let defaultActive = '/home/loop-test'
    let menuItems = [
      {
        index: '/home/loop-test',
        title: 'Loop Test',
        icon: 'el-icon-fas fa-circle-notch'
      },
      {
        index: '/home/instr-panel',
        title: 'Instrument Panel',
        icon: 'el-icon-fas fa-tachometer-alt'
      },
      {
        index: '/home/trx-control',
        title: 'Transceiver Control',
        icon: 'el-icon-fas fa-gamepad'
      },
      {
        index: '/home/station-setup',
        title: 'Station Setup',
        icon: 'el-icon-fas fa-network-wired'
      },
      {
        index: '/home/instr-res',
        title: 'Instrument Resource',
        icon: 'el-icon-fas fa-server'
      },
      {
        index: '/home/settings',
        title: 'Settings',
        icon: 'el-icon-fas fa-cog'
      }
    ]
    return {
      defaultActive,
      menuItems
    }
  }
}
</script>

<style lang='scss' module>
  .top-nav {
    min-height: 100%;
    border-right: solid 1px #dcdfe6;
  }
  .top-nav :global(.el-menu-item.is-active::after) {
    content: '';
    position: absolute;
    left: 0;
    width: 4px;
    height: 100%;
    background: $color-primary;
  }
  .top-nav-popup:global(.el-tooltip__popper.is-light) {
    border-color: transparent;
    border-radius: 3px;
    box-shadow: 0 0 4px rgba(0,0,0,0.15);
    background: $color-primary;
    color: rgba(255,255,255,0.95);
    font-weight: bold;
    font-size: 15px;
    margin-left: 0;
  }
  .top-nav-popup :global(.popper__arrow) {
    border-right-color: $color-primary !important;
  }
  .top-nav-popup :global(.popper__arrow::after) {
    border-right-color: $color-primary !important;
  }
</style>
