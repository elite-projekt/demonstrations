<template>
  <v-app>
    <v-system-bar app color="orange"
                  height="120">
      <v-spacer></v-spacer>
      <v-toolbar-title> <h1 class="black--text">Demo Navigation</h1></v-toolbar-title>
      <v-spacer></v-spacer>
    </v-system-bar>

    <v-app-bar app color="grey" height="100" >
      <v-spacer></v-spacer>
      <h1 class="black--text">Welcome</h1>
      <v-spacer></v-spacer>
    </v-app-bar>


    <!-- Sizes your content based upon application components -->
    <v-main>
      <v-overlay :value="loading">
        <v-progress-circular
          indeterminate
          size="64"
        ></v-progress-circular>
      </v-overlay>
      <!-- Provides the application the proper gutter -->
      <v-container container grid-list-xl>
        <v-layout column>
          Phishing Demo
        <v-col d-flex md11>
          <v-btn v-on:click="startDemo('Phishing')">Start
          </v-btn>
          <v-btn  v-on:click="stopDemo('Phishing')">Stop
          </v-btn>
        </v-col>

        <v-spacer></v-spacer>
          Password Demo
          <v-col d-flex md11>
            <v-btn v-on:click="startDemo('Password')">Start
            </v-btn>
            <v-btn  v-on:click="stopDemo('Password')">Stop
            </v-btn>
          </v-col>
        </v-layout>
        <!-- If using vue-router -->
        <router-view></router-view>

      </v-container>
    </v-main>

    <v-footer app>
      <!-- -->
    </v-footer>
  </v-app>
</template>

<script>
import demoService from '@/services/DemoService'

export default {
  name: 'HelloWorld',
  data () {
    return ({
      demoService: demoService,
      loading: false,
      success: false,
      error: false
    })
  },

  methods: {
    async startDemo (demoName) {
      this.loading = true
      await demoService.startDemo(demoName).then((res) => {
        this.success = true
        alert(res)
      })
        .catch((error) => {
          this.error = true
          alert('Oops. Something went wrong!')
          console.log(error)
        })
      this.loading = false
    },
    async stopDemo (demoName) {
      await demoService.stopDemo(demoName)
    }
  }
}
</script>
