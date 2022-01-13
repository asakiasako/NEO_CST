import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Init from '@/views/Init.vue'
import LoopTest from '@/views/Home/LoopTest.vue'
import TrxControl from '@/views/Home/TrxControl.vue'
import InstrPanel from '@/views/Home/InstrPanel.vue'
import StationSetup from '@/views/Home/StationSetup.vue'
import InstrRes from '@/views/Home/InstrRes.vue'
import Settings from '@/views/Home/Settings.vue'
import LoopTestStart from '@/views/Home/LoopTest/LoopTestStart.vue'
import LoopTestProcess from '@/views/Home/LoopTest/LoopTestProcess.vue'
import MultiFileTestConfig from '@/views/Home/LoopTest/MultiFileTestConfig.vue'
import LoopConfig from '@/views/Home/LoopTest/LoopTestProcess/LoopConfig.vue'
import OutputParams from '@/views/Home/LoopTest/LoopTestProcess/OutputParams.vue'
import ConfirmPage from '@/views/Home/LoopTest/LoopTestProcess/ConfirmPage.vue'
import RunningPage from '@/views/Home/LoopTest/LoopTestProcess/RunningPage.vue'
import MultiRunningPage from '@/views/Home/LoopTest/MultiRunningPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    name: 'entry',
    path: '/',
    redirect: { name: 'init' }
  },
  {
    name: 'init',
    path: '/init',
    component: Init
  },
  {
    name: 'home',
    path: '/home',
    component: Home,
    redirect: { name: 'loop-test' },
    children: [
      {
        name: 'loop-test',
        path: 'loop-test',
        component: LoopTest,
        redirect: { name: 'loop-test-start' },
        children: [
          {
            name: 'loop-test-start',
            path: 'start',
            component: LoopTestStart
          },
          {
            name: 'loop-test-process',
            path: 'process',
            component: LoopTestProcess,
            redirect: { name: 'loop-config' },
            children: [
              {
                name: 'loop-config',
                path: 'loop-config',
                component: LoopConfig
              },
              {
                name: 'output-params',
                path: 'output-params',
                component: OutputParams
              },
              {
                name: 'confirm-page',
                path: 'confirm-page',
                component: ConfirmPage
              },
              {
                name: 'running-page',
                path: 'running-page',
                component: RunningPage
              }
            ]
          },
          {
            name: 'multi-file-test-config',
            path: 'multi-file-test-config',
            component: MultiFileTestConfig
          },
          {
            name: 'multi-running-page',
            path: 'multi-running-page',
            component: MultiRunningPage
          }
        ]
      },
      {
        name: 'instr-panel',
        path: 'instr-panel',
        component: InstrPanel
      },
      {
        name: 'trx-control',
        path: 'trx-control',
        component: TrxControl
      },
      {
        name: 'station-setup',
        path: 'station-setup',
        component: StationSetup
      },
      {
        name: 'instr-res',
        path: 'instr-res',
        component: InstrRes
      },
      {
        name: 'settings',
        path: 'settings',
        component: Settings
      }
    ]
  },
  {
    path: '*',
    redirect: { name: 'home' }
  }
]

const router = new VueRouter({
  scrollBehavior: () => ({ y: 0 }),
  routes
})

export default router
