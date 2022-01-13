/**
 * Define Application Menu
 */
const template = [
  {
    label: 'File',
    submenu: [
      {
        label: 'Just an Example For Menu',
        click: function () {
          console.log('Menu item clicked')
        }
      }
    ]
  },
  {
    label: 'Control',
    submenu: [
      {
        label: 'Just another Example',
        click: function () {
          console.log('Menu item clicked')
        }
      }
    ]
  }
]

module.exports = template
