import store from '@/store'

const notification = {
  push (msg, type) {
    // type: info, warning, danger, success
    const id = +new Date()
    const payload = {
      id: id,
      type: type,
      msg: msg,
      read: false
    }
    store.commit('pushNotification', payload)
  }
}

const PluginNotificationCenter = {
  install (Vue, options) {
    Vue.prototype.$notificationCenter = notification
  }
}

export default PluginNotificationCenter
