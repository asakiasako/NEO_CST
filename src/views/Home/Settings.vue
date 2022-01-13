<template>
  <div :class="$style.wrapper">
    <el-form label-position="left">
      <el-form-item v-for="(item, key) in settingsList" label-width="240px" :label="key.replace(/__/g, ' ')" :key="key">
        <el-select :class="$style['setting-item']" v-if="item.type === 'select'" size="medium" v-model="settingsList[key].value" @change="setSetting(key, $event)">
          <el-option v-for="opt in item.options" :key="opt" :label="opt" :value="opt"></el-option>
        </el-select>
        <el-switch v-else-if="item.type === 'bool'" v-model="settingsList[key].value" @change="setSetting(key, $event)"></el-switch>
        <el-input :class="$style['setting-item']" v-else size="medium" v-model="settingsList[key].value" @change="setSetting(key, $event)"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button size="small" plain type="info" @click="showInformation">About</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data () {
    const settingsList = {}
    const information = {
      version: ''
    }
    return {
      settingsList,
      information
    }
  },
  computed: {
    htmlInformation () {
      let htmlInfo = ''
      const information = this.information
      for (const key in information) {
        htmlInfo += `<p>${key}: ${information[key]}</p>`
      }
      return htmlInfo
    }
  },
  methods: {
    getSetting (key) {
      this.$rpcClient.request({
        route: ':setting:get',
        args: [key]
      }).then((result) => {
        this.settingsList[key].value = result
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    setSetting (key, value) {
      this.$rpcClient.request({
        route: ':setting:set',
        args: [key, value]
      }).catch((err) => {
        this.$alertError(err)
      })
    },
    showInformation () {
      this.$alert(this.htmlInformation, 'Information', {
        confirmButtonText: 'OK',
        dangerouslyUseHTMLString: true
      })
    },
    getVersion () {
      this.$electron.ipcRenderer.invoke('get-version').then((result) => {
        this.information.version = result
      }).catch((err) => {
        this.$alertError(err)
      })
    }
  },
  created () {
    this.getVersion()
  },
  activated () {
    this.$rpcClient.request({
      route: ':setting:list'
    }).then((result) => {
      if (result) {
        for (const key in result) {
          result[key].value = null
        }
      }
      this.settingsList = result
      for (const key in result) {
        this.getSetting(key)
      }
    }).catch((err) => {
      this.$alertError(err)
    })
  }
}
</script>

<style module>
  .wrapper {
    padding: 20px 40px;
    display: flex;
  }
  .setting-item {
    width: 200px;
  }
</style>
