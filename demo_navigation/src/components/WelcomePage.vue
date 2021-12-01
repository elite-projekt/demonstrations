<template>
  <!-- Sizes your content based upon application components -->
  <v-main>
    <v-container fluid>
        <v-row>
            <v-col>
                <p>{{ $t('welcome_page.introtext') }}
                </p>
                <p><strong>{{ $t('welcome_page.exercise') }} </strong>{{ $t('welcome_page.open_thunderbird') }} </p>
            </v-col>
        </v-row>

        <v-row v-if="!hidehelp">
            <v-col>
                <ul>
                    <li>{{ $t('welcome_page.arrange_browser') }}</li>
                    <li>{{ $t('welcome_page.press_start') }}</li>
                    <li>{{ $t('welcome_page.thunderbird_search') }}</li>
                    <img style ="display: block; margin-left: 0px; margin-right: auto;" :src="require('@/assets/help-thunderbird.png')">
                    <li>{{ $t('welcome_page.arrange_thunderbird') }}</li>
                    <img style ="display: block; margin-left: 0px; margin-right: auto;" :src="require('@/assets/demo-arrangement.png')">
                </ul>
            </v-col>
        </v-row>

        <v-row>
            <v-col>
                <v-btn
                    color="green" elevation="2" @click="$router.push({name: 'Task1', params: {}})"
                >{{ $t('welcome_page.done') }}</v-btn>
                <v-btn
                    color="red" elevation="2" @click="hidehelp = false"
                >{{ $t('welcome_page.help') }}</v-btn>
            </v-col>
        </v-row>
    </v-container>
  </v-main>

</template>

<script>
export default {
  name: 'WelcomePage',
  data() {
      return {
          hidehelp: true
      }
  },
  mounted() {
    this.$emit("message", this.$t('welcome_page.toolbartitle'))
    this.$emit("appBarTitle", this.$t('welcome_page.appbartitle'))
  },
  methods: {
      async startDemo() {

      }
  }
}
</script>

<style scoped>

</style>
