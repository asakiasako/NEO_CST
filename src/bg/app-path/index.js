import { appData } from './constants'
import { app } from 'electron'
import path from 'path'

let appName = app.getName()
if (process.env.NODE_ENV === 'development') {
  const fs = require('fs')
  const jsonStr = fs.readFileSync('package.json')
  appName = `[dev] ${JSON.parse(jsonStr).productName}`
}

// add a post-fix if not in production env
const userData = path.join(appData, appName)

app.setPath('appData', appData)
app.setPath('userData', userData)
app.setPath('logs', path.join(userData, 'Logs'))
