const PluginAlertError = {
  install (Vue) {
    Vue.prototype.$alertError = function (err, callback) {
      const errName = err.name
      const errMsg = err.message
      let errStr = null
      if (errName === 'ApiError') {
        errStr = `[${errName}] ${err.errorType}: ${err.errorDescription}`
      } else {
        errStr = `[${errName}] ${errMsg}`
      }
      this.$alert(errStr, 'Error', {
        confirmButtonText: 'OK',
        type: 'error'
      }).then(() => {
        if (callback) {
          callback()
        }
      })
    }
  }
}

export default PluginAlertError
