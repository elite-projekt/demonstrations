// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import App from './App'
import router from './router'
import axios from 'axios'
import i18n from './i18n'

Vue.config.productionTip = false

axios.defaults.baseUrl = 'http://localhost:5000'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  vuetify,
  components: { App },
  i18n,
  template: '<App/>'
}).$mount('#app')
