import { autoUpdater } from 'electron-updater'
import { ipcMain } from 'electron'
import electronLog from 'electron-log'

autoUpdater.autoDownload = false
autoUpdater.autoInstallOnAppQuit = false
autoUpdater.logger = electronLog

export const addUpdaterListeners = function (win) {
  autoUpdater.on('error', err => {
    win.webContents.send('update-error', err)
  })
  autoUpdater.on('update-available', info => {
    win.webContents.send('update-available', info)
  })
  autoUpdater.on('update-not-available', info => {
    win.webContents.send('update-not-available', info)
  })
  autoUpdater.on('download-progress', (progress, bytesPerSecond, percent, total, transferred) => {
    win.webContents.send('download-progress', progress, bytesPerSecond, percent, total, transferred)
  })
  autoUpdater.on('update-downloaded', info => {
    win.webContents.send('update-downloaded', info)
  })
}

ipcMain.handle('check-for-update', () => {
  if (process.env.NODE_ENV === 'production') {
    return autoUpdater.checkForUpdates()
  } else {
    console.log('Not in production. Skip check for update.')
  }
})

ipcMain.on('download-update', () => {
  autoUpdater.downloadUpdate()
})

ipcMain.on('quit-and-install', () => {
  autoUpdater.quitAndInstall(true, true)
})
