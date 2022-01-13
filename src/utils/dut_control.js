import rpcClient from '@/plugins/rpc-client/client'

export function readTWIRegister (trxIdx, address) {
  return rpcClient.request({
    route: ':trx:read-twi-register',
    args: [trxIdx, address]
  })
}

export function writeTWIRegister (trxIdx, address, data) {
  return rpcClient.request({
    route: ':trx:write-twi-register',
    args: [trxIdx, address, data]
  })
}

export function readTWIRegisterBit (trxIdx, address, index) {
  return rpcClient.request({
    route: ':trx:read-twi-register-bit',
    args: [trxIdx, address, index]
  })
}

export function writeTWIRegisterBit (trxIdx, address, index, data) {
  return rpcClient.request({
    route: ':trx:write-twi-register-bit',
    args: [trxIdx, address, index, data]
  })
}

export function readTWIRegisterBits (trxIdx, address, start, stop) {
  return rpcClient.request({
    route: ':trx:read-twi-register-bits',
    args: [trxIdx, address, start, stop]
  })
}

export function writeTWIRegisterBits (trxIdx, address, start, stop, data) {
  return rpcClient.request({
    route: ':trx:write-twi-register-bits',
    args: [trxIdx, address, start, stop, data]
  })
}

export function getPinState (trxIdx, pinName) {
  return rpcClient.request({
    route: ':trx:get-pin-state',
    args: [trxIdx, pinName]
  })
}

export function setPinState (trxIdx, pinName, isHigh) {
  return rpcClient.request({
    route: ':trx:set-pin-state',
    args: [trxIdx, pinName, isHigh]
  })
}

export function sequentialReadRegisters (trxIdx, startAddr, stopAddr, mode) {
  return rpcClient.request({
    route: ':trx:sequential-read-registers',
    args: [trxIdx, startAddr, stopAddr, mode]
  })
}

export function selectTWIRegisterPage (trxIdx, page) {
  return rpcClient.request({
    route: ':trx:select-page',
    args: [trxIdx, page]
  })
}

export function selectTWIRegisterBankPage (trxIdx, bank, page) {
  return rpcClient.request({
    route: ':trx:select-bank-page',
    args: [trxIdx, bank, page]
  })
}

export function callDutMethod (trxIdx, methodName, args, kwargs) {
  return rpcClient.request({
    route: ':trx:call',
    args: [trxIdx, methodName, args, kwargs]
  })
}
