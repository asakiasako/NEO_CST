/* add rpcClient to Vue.prototype.$rpcClient */
import { encode, decode } from '@msgpack/msgpack'
import { ipcRenderer } from 'electron'
import services from './rpc_grpc_pb'
import messages from './rpc_pb'
import { credentials } from '@grpc/grpc-js'
import { isUndefined } from 'lodash'

/* run RPC client */
const rpcClient = {
  grpcClient: undefined,
  host: '127.0.0.1',
  port: undefined,
  max_message_length: 1024 * 1024 * 10,
  timeout: 5000,
  async initialize () {
    /* get current port from main process */
    this.port = await ipcRenderer.invoke('get-rpc-port')
    await ipcRenderer.invoke('check-server-alive') // manage case if rpc server is not started normally
    this.grpcClient = new services.ServiceRPCClient(`${this.host}:${this.port}`, credentials.createInsecure(), {
      'grpc.max_send_message_length': this.max_message_length,
      'grpc.max_receive_message_length': this.max_message_length
    })
  },
  waitForReady (timeout = Infinity) {
    // timeout in milliseconds
    const deadline = Date.now() + timeout
    return new Promise((resolve, reject) => {
      this.grpcClient.waitForReady(deadline, (e) => {
        if (e) {
          reject(e)
        } else {
          resolve()
        }
      })
    })
  },
  listApis: function (timeout) {
    timeout = isUndefined(timeout) ? this.timeout : timeout
    return new Promise((resolve, reject) => {
      this.grpcClient.listApis(new messages.Empty(), { deadline: Date.now() + timeout }, (err, response) => {
        if (err) {
          reject(err)
        } else {
          resolve(response.getRpcrouteList())
        }
      })
    })
  },
  request: function (requestOptions) {
    const route = requestOptions.route
    const argData = encode({ args: requestOptions.args, kwargs: requestOptions.kwargs })
    const apiRequest = new messages.ApiRequest([route, argData])
    const timeout = isUndefined(requestOptions.timeout) ? this.timeout : requestOptions.timeout
    return new Promise((resolve, reject) => {
      this.grpcClient.request(apiRequest, { deadline: Date.now() + timeout }, (err, response) => {
        if (err) {
          reject(err)
        } else {
          const replyData = decode(response.getReplydata())
          resolve(replyData)
        }
      })
    })
  }
}

export default rpcClient
