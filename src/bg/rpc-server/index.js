/**
 * Settings of RPC
 */
const electronLog = require('electron-log')

const { DEFAULT_SERVER_PORT, PYTHON_PATH, PROCESS_PATH } = require('./const')
const app = require('electron').app
const portIsOccupied = require('./checkPort')

let rpcServer, rpcPort
let serverProcessAlive = false
const userDataPath = app.getPath('userData')
const appDataPath = app.getPath('appData')

const createRpcServer = async () => {
  const port = await portIsOccupied(DEFAULT_SERVER_PORT)
  if (process.env.NODE_ENV !== 'production') {
    rpcServer = require('child_process').spawn(
      PYTHON_PATH,
      [PROCESS_PATH],
      {
        // add env vars to child process
        env: Object.assign(process.env, {
          userDataPath: userDataPath,
          appDataPath: appDataPath,
          rpcServerPort: port,
          PYTHONUNBUFFERED: true
        })
      }
    )
    // pipe child process stdio to main process if in dev env
    rpcServer.stdout.pipe(process.stdout)
    rpcServer.stderr.pipe(process.stderr)
  } else {
    rpcServer = require('child_process').execFile(
      PROCESS_PATH,
      undefined,
      {
        // add env vars to child process
        env: Object.assign(process.env, {
          userDataPath: userDataPath,
          appDataPath: appDataPath,
          rpcServerPort: port,
          PYTHONUNBUFFERED: true
        })
      },
      (err) => {
        if (err) {
          require('electron').dialog.showErrorBox('RPC Server Crashed.', `${err}`)
          electronLog.error(err)
        }
      }
    )
  }
  if (rpcServer !== null) {
    console.log(`RPC server running on port ${port}`)
    console.log(`userData dir: ${userDataPath}`)
    serverProcessAlive = true
    rpcPort = port
    rpcServer.on('close', () => {
      rpcPort = undefined
      serverProcessAlive = false
      rpcServer = null
    })
  }
}

const exitRpcServer = () => {
  if (rpcServer && isServerProcessAlive()) {
    // remove listeners or there is a chance that error will be raised because rpcServer is already killed
    rpcServer.removeAllListeners().kill()
  }
}

const getRpcPort = () => {
  return rpcPort
}

const isServerProcessAlive = () => {
  return serverProcessAlive
}

module.exports = {
  createRpcServer,
  exitRpcServer,
  getRpcPort,
  isServerProcessAlive
}
