'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  VUE_APP_ORCHESTRATIONIP: '"http://localhost:5000/orchestration"',
  VUE_APP_NATIVEIP: '"http://localhost:5000/platform"',
  VUE_APP_TEACHINGIP:'"http://localhost:8080"',
  VUE_APP_NAVIGATIONIP:'"http://localhost:80"',
  VUE_APP_I18N_LOCALE: '"en"',
  VUE_APP_I18N_FALLBACK_LOCALE: '"en"'
})
