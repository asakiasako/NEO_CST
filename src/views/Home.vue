<template>
  <div style="height: 100%; width: 100%;">
    <el-container :class="$style['top-container']">
      <el-header :class="$style.header" height="auto">
        <top-header></top-header>
      </el-header>
      <el-container style="height: 100%;">
        <el-aside :class="$style.aside" width="auto">
          <top-nav></top-nav>
        </el-aside>
        <el-main :class="$style.main">
          <keep-alive>
            <router-view></router-view>
          </keep-alive>
        </el-main>
      </el-container>
      <el-footer :class="$style.footer" height="26px">
        <top-footer></top-footer>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import TopHeader from './Home/parts/TopHeader.vue'
import TopFooter from './Home/parts/TopFooter.vue'
import TopNav from './Home/parts/TopNav.vue'

export default {
  components: {
    TopHeader,
    TopFooter,
    TopNav
  },
  props: [],
  data: function () {
    return {}
  },
  methods: {
  },
  created () {
  }
}
</script>

<style lang="scss" module>
  .header:global(.el-header) {
    padding: 0;
  }
  .top-container {
    height: 100%;
  }
  .footer:global(.el-footer) {
    padding: 0;
  }
  .main:global(.el-main) {
    height: 100%;
    padding: 0;
  }
</style>

<style>
</style>
