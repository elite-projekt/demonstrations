<template>
<v-app>
    <!-- <v-app-bar app color="orange"
               dark
               height="120">
      <v-spacer></v-spacer>
      <v-toolbar-title><h1 class="black--text">{{ toolbarTitle }}</h1></v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar> -->

    <v-system-bar app color="orange"
                  height="120">
      <v-spacer></v-spacer>
      <v-toolbar-title> <h1 class="black--text">{{ toolbarTitle }}</h1></v-toolbar-title>
      <v-spacer></v-spacer>
    </v-system-bar>

    <v-app-bar app color="grey" height="100" >
      <v-spacer></v-spacer>
      <h1 class="black--text">{{ appBarTitle }}</h1>
      <v-spacer></v-spacer>
      <div class="locale-changer">
        <select v-model="$i18n.locale">
          <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">{{ lang }}</option>
        </select>
      </div>
    </v-app-bar>


    <router-view @message="setToolbarTitle" @appBarTitle="setappBarTitle"></router-view>


  <v-footer app>
    <!-- -->
  </v-footer>
</v-app>
</template>
<script>
export default {
  name: 'App',
  data () {
    return {
      langs: ['en', 'de'],
      toolbarTitle: '',
      appBarTitle: ''
    }
  },
  methods: {
    setToolbarTitle (toolbarTitle) {
      this.toolbarTitle = toolbarTitle
    },
    setappBarTitle (appBarTitle) {
      this.appBarTitle = appBarTitle
    }
  }
}
</script>
