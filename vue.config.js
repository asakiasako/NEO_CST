/* eslint-disable no-template-curly-in-string */
module.exports = {
  configureWebpack: {
    devtool: 'source-map' // We do this so that our debugger has a way to map the code within a compressed file back to its position in the original file.
  },
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        appId: 'com.coherent-system-test.app',
        copyright: 'Copyright © ' + new Date().getFullYear() + ' NeoPhotonics',
        win: {
          icon: 'build/icon.ico'
        },
        asar: true,
        asarUnpack: 'ElectronPythonSubProcess',
        nsis: {
          oneClick: false,
          perMachine: false,
          allowToChangeInstallationDirectory: true
        },
        publish: [
          {
            provider: 'generic',
            url: 'http://10.20.22.13:8181/coherent-system-test/tot-cmis/',
            channel: 'latest'
          }
        ]
      }
    }
  },
  css: {
    loaderOptions: {
      // pass options to sass-loader
      sass: {
        prependData: '@import "~@/styles/global-variables.scss"'
      },
      // for scss files
      scss: {
        prependData: '@import "~@/styles/global-variables.scss";'
      }
    }
  }
}
