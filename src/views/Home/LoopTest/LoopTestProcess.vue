<template>
  <el-container :class="$style.container">
    <el-header :class="$style.header" height="auto">
      <el-steps :active="stepsStatus.active" align-center :finish-status="stepsStatus.finishStatus">
        <el-step title="Loop configure"></el-step>
        <el-step title="Output parameters"></el-step>
        <el-step title="Confirm and run"></el-step>
      </el-steps>
    </el-header>
    <el-main :class="$style.main">
      <keep-alive>
        <router-view ref="currentStep" @start-test="inTest=true" @stop-test="inTest=false"></router-view>
      </keep-alive>
    </el-main>
    <el-footer :class="$style.footer">
      <el-button-group v-if="stepsStatus.active < 3">
        <el-button
          type="info" round icon="el-icon-arrow-left"
          @click="lastStep"
        >Last</el-button>
        <el-button
          :type="stepsStatus.active === 2 ? 'success' : 'info'" round
          @click="nextStep"
        >{{stepsStatus.active === 2 ? 'Run test':'Next'}}<i v-if="stepsStatus.active !== 3" class="el-icon-arrow-right el-icon--right"></i></el-button>
      </el-button-group>
      <template v-else>
        <el-button v-if="inTest" round type="danger" @click="stopTest">Stop</el-button>
        <template v-else>
          <el-button
            type="info" round icon="el-icon-arrow-left"
            @click="toStartPage"
          >Go Back</el-button>
          <el-button
            type="info" round
            @click="openResult"
          >Result Folder</el-button>
        </template>
      </template>
    </el-footer>
  </el-container>
</template>

<script>
export default {
  data () {
    const inTest = false
    return {
      inTest
    }
  },
  computed: {
    stepsStatus () {
      let active = 0
      switch (this.$route.name) {
        case 'loop-config':
          active = 0
          break
        case 'output-params':
          active = 1
          break
        case 'confirm-page':
          active = 2
          break
        case 'running-page':
          active = 3
      }
      return {
        active,
        finishStatus: 'success'
      }
    }
  },
  methods: {
    openResult () {
      this.$electron.shell.openItem('C:/AppData/Coherent System Test/Result/')
    },
    lastStep () {
      this.$refs.currentStep.$emit('last-step')
    },
    nextStep () {
      this.$refs.currentStep.$emit('next-step')
    },
    toStartPage () {
      this.$router.push({ name: 'loop-test' })
    },
    stopTest () {
      this.$refs.currentStep.stopTest()
    }
  }

}
</script>

<style lang="scss" module>
.container {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.header:global(.el-header) {
  padding-top: 24px;
  padding-bottom: 16px;
}
.header :global(.el-step__title.is-process) {
  font-weight: inherit;
}
.main:global(.el-main) {
  padding: 0;
  height: 1px;
  overflow: auto;
}
.footer {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
