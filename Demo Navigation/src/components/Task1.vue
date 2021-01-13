<template>
  <!-- Sizes your content based upon application components -->
  <v-main>
    <v-container fluid>
      <v-row>
          <v-col>
            <p>Sie sind angestellt in der XYZ AG und dort als Assistenz der Geschäftsführung eingestellt. 
              Zur Zeit ist die Stimmung im Büro etwas angespannt. Nächste Woche findet ein Treffen mit wichtigen 
              Geschäftspartnern statt und noch immer sind nicht alle Terminzusagen bei Ihnen eingegangen. Und das Geschenk, 
              welches Sie im Namen der Abteilung für eine in Rente gehende Kollegin bestellt hatten, 
              sollte auch schon längst geliefert sein. So beginnen Sie also Ihren Arbeitstag und sehen als erstes nach Ihren E-Mails.
            </p>
            <p><strong>Aufgabe: </strong>E-Mails bearbeiten</p>
            <ul>
              <li>Terminzusagen annehmen und in den Kalender eintragen.</li>
              <li>Wurde das Abschiedsgeschenk versandt?</li>
              <li>Gibt es sonst noch wichtige E-Mails?</li>
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
              color="green" elevation="2" @click="$router.push({name: 'Task1', params: {}})"
            >Erledigt</v-btn>
            <v-btn
              color="red" elevation="2" @click="hidehelp = false"
            >Hilfe</v-btn>
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
    this.$emit("message", "Security Demo");
    this.$emit("appBarTitle", "Aufgabe");
  },
  methods: {
    
  }
}
</script>

<style scoped>

</style>
