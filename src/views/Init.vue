<!--
Put time costing initializing tasks here, so they will not block app launching, whitch might confusing users.
-->
<template>
  <div id="app" style="height: 100%">
    <div :class="$style['app-wrapper']">
      <img style="max-width: 70%;max-height: 84%;margin-bottom: 20px;" src="@/assets/logo.png">
      <div :class="$style['progress-bar']">
        <div :class="$style['loading-wrapper']">
          <div :class="[$style['loading-rotate'], $style.lazy]"></div>
        </div>
        <div class="tips">{{tips}}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      tips: 'Initializing...'
    }
  },
  methods: {
    async initRpcClient () {
      this.tips = 'Initializing RPC client...'
      await this.$rpcClient.initialize()
    },
    async waitForRpcReady () {
      this.tips = 'Connecting RPC server...'
      await this.$rpcClient.waitForReady(20000) // timeout in milliseconds
    }
  },
  async mounted () {
    await this.initRpcClient()
    await this.waitForRpcReady()
    this.$router.push({ name: 'home' })
  }
}
</script>

<style module>
  .app-wrapper {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .progress-bar {
    display: flex;
    align-items: center;
    position: fixed;
    bottom: 30px;
  }
  .loading-wrapper {
    height: 20px;
    padding-right: 8px;
  }
  .loading-rotate {
    position: relative;
    width: 20px;
    height: 20px;
    -webkit-animation: rotate 1s linear infinite;
    animation: rotate linear 1s infinite;
    transform-origin:center center;
    box-sizing: border-box;
  }
  .loading-rotate:before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    border: 2px solid transparent;
    border-top-color: #ff4500;
    border-radius: 50%;
    z-index: 10;
  }
  .loading-rotate:after {
    content: "";
    position: absolute;
    left: 0; top: 0;
    width: 20px;
    height: 20px;
    border: 2px solid #d0d5dd;
    box-sizing: border-box;
    border-radius: 50%;
  }

  .loading-rotate.lazy {
      animation: rotate-lazy ease-in-out 6s infinite;
  }
  @keyframes rotate-lazy{
    0 {
      transform: rotate(0);
    }
    25% {
      transform: rotate(450deg);
    }
    50% {
      transform: rotate(900deg);
    }
    75%{
      transform: rotate(1350deg);
    }
    100%{
      transform: rotate(1800deg);
    }
  }
  .tips {
    color: #909399;
  }
</style>
