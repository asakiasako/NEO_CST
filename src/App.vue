<template>
  <div v-cloak :id="$style.app">
    <router-view></router-view>
    <app-updater></app-updater>
  </div>
</template>

<script>
import AppUpdater from './components/AppUpdater.vue'
export default {
  name: 'app',
  components: {
    AppUpdater
  }
}
</script>

<style module>
  #app {
    height: 100%;
  }
</style>
