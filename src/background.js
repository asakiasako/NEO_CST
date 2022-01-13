/* global __static */
'use strict'

import { app, protocol, session, BrowserWindow, globalShortcut, ipcMain, dialog } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import '@/bg/app-path' // change app paths before other imports
import { createRpcServer, exitRpcServer, getRpcPort, isServerProcessAlive } from '@/bg/rpc-server'
import { acceleratorMap } from '@/bg/accelerator'
import path from 'path'
import '@/bg/menu'
import { addUpdaterListeners } from '@/bg/auto-update'

const isDevelopment = process.env.NODE_ENV !== 'production'
const vueDevtoolsPath = path.join(__static, 'vue-devtools')

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

let mainWindow = null

// Single instance
const gotTheLock = app.requestSingleInstanceLock()

if (!gotTheLock) {
  app.quit()
} else {
  app.on('second-instance', (event, commandLine, workingDirectory) => {
    // Someone tried to run a second instance, we should focus our window.
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore()
      mainWindow.focus()
    }
  })
}

// Add listeners
ipcMain.on('app-restart', (event) => {
  app.relaunch()
  app.quit()
})

ipcMain.on('app-quit', (event) => {
  app.quit()
})

ipcMain.handle('get-rpc-port', (event) => {
  return getRpcPort()
})

ipcMain.handle('check-server-alive', (event) => {
  const alive = isServerProcessAlive()
  if (!alive) {
    dialog.showErrorBox('Fatal Error', `Unable to launch RPC server process. Get more information with logs in:\n${app.getPath('logs')}`)
    app.quit()
  }
})

ipcMain.handle('get-version', (event) => {
  return app.getVersion()
})

ipcMain.on('get-app-path', (event, name) => {
  event.returnValue = app.getPath(name)
})

async function createWindow () {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 960,
    height: 600,
    minWidth: 960,
    minHeight: 600,
    useContentSize: true,
    webPreferences: {
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
    },
    show: false
  })

  addUpdaterListeners(win)

  ipcMain.handle('show-open-dialog', (event, options) => {
    return dialog.showOpenDialog(win, options)
  })

  ipcMain.handle('show-save-dialog', (event, options) => {
    return dialog.showSaveDialog(win, options)
  })

  ipcMain.handle('set-closable', (event, closable) => {
    win.setClosable(closable)
  })

  // bug that main browser window cannot close, if devtools window is showing
  // https://github.com/electron/electron/issues/25012
  win.once('ready-to-show', () => {
    win.show()
  })

  win.on('closed', () => {
    mainWindow = null
  })

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }

  registerAccelerators(win)

  return win
}

function registerAccelerators (win) {
  // eslint-disable-next-line prefer-const
  for (let key in acceleratorMap) {
    globalShortcut.register(key, () => {
      acceleratorMap[key](win)
    })
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await session.defaultSession.loadExtension(vueDevtoolsPath, { allowFileAccess: true })
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  await createRpcServer()
  mainWindow = await createWindow()
})

app.on('will-quit', () => {
  // exitRpcServer before app closed
  exitRpcServer()
})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
