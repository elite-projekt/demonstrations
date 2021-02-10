<template>
  <!-- Sizes your content based upon application components -->
  <v-main>
    <v-container fluid>
      <v-row>
          <v-col>
            <p>{{ $t('task1.introtext') }}
            </p>
            <p><strong>{{ $t('task1.exercise') }} </strong>{{ $t('task1.edit_emails') }}</p>
            <ul>
              <li>{{ $t('task1.accept_appointment') }}</li>
              <li>{{ $t('task1.sent_present') }}</li>
              <li>{{ $t('task1.important_emails') }}</li>
            </ul>
          </v-col>
        </v-row>

        <v-row v-if="!hidehelp">
          <v-col>
            Help
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-btn
              color="green" elevation="2" @click="$router.push({name: 'Endpage', params: {}})"
            >{{ $t('task1.done') }}</v-btn>
            <!--  Use this button to display help if necessary
              <v-btn
              color="red" elevation="2" @click="hidehelp = false"
            >{{ $t('task1.help') }}</v-btn>
            -->
          </v-col>
          <v-col>

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
    this.$emit("message", this.$t('task1.toolbartitle'));
    this.$emit("appBarTitle", this.$t('task1.appbartitle'));
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
