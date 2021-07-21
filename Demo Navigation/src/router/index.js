import Vue from 'vue'
import Router from 'vue-router'
import WelcomePage from '../components/WelcomePage'
import Task1 from '../components/Task1'
import Endpage from '../components/Endpage'


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'WelcomePage',
      component: WelcomePage
    }, {
      path: '/Task1',
      name: 'Task1',
      component: Task1
    }, {
      path: '/Endpage',
      name: 'Endpage',
      component: Endpage
    }, {
      path: '/pathMatch(.*)',
      name: 'catchall',
      component: WelcomePage
    }
  ]
})
