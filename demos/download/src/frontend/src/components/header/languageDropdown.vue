<template>
  <div>
    <div class="locale-changer">
      <select class="lang-dropdown" v-model="$i18n.locale">
        <option
          v-for="lang in $i18n.locales"
          :key="lang.code"
          :value="lang.code"
        >
          {{ lang.name }}
        </option>
      </select>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      defaultVal: { name: "English", code: "en" },
    };
  },
  methods: {
    selectLocale(locale) {
      this.$i18n.locale = locale.code;
    },
  },
};
</script>
<style lang="scss">
.lang-dropdown {
  min-width: 6rem;
  padding: 0.3rem;
  border-radius: 5px;
}
</style>
