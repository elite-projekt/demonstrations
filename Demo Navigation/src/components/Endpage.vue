<template>
  <!-- Sizes your content based upon application components -->
  <v-main>
    <v-container fluid>
      <v-row>
          <v-col>
            <p>{{ $t('endpage.introtext') }}
            </p>
            <v-btn
                  :href="this.teachingIp" target="_blank">
                  {{ $t('endpage.link_to_teaching')}}
                </v-btn>
          </v-col>
        </v-row>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: 'endpage',
  data() {
    return {
      teachingIp: process.env.VUE_APP_TEACHINGIP,
    }
  },
  mounted() {
    this.$emit("message", this.$t('endpage.toolbartitle'));
    this.$emit("appBarTitle", this.$t('endpage.appbartitle'));
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
