import Vue from 'vue'
import Router from 'vue-router'
import WelcomePage from '../components/WelcomePage'
import Task1 from '../components/Task1'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'WelcomePage',
      component: WelcomePage
    }, {
      path: '/Task1',
      name: 'Task1',
      component: Task1
    }
  ]
})
