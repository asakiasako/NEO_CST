export function intArrayToAscii (intArray) {
  let outStr = ''
  if (!intArray) {
    return
  }
  if (typeof intArray === 'number') {
    intArray = [intArray]
  }
  for (let item of intArray) {
    let str0 = ''
    let int0 = item
    while (int0 > 0) {
      str0 = String.fromCharCode(int0 % 256) + str0
      int0 = int0 >> 8
    }
    outStr += str0
  }
  return outStr
}
