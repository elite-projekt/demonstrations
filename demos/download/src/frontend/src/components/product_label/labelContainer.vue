<template>
  <div class="labelContainer">
    <div class="labelContainer__items">
      <div v-for="productLabel in labels">
        <productLabel :productLabel="productLabel" :discount="discount" />
      </div>
    </div>
  </div>
</template>

<script>
import productLabel from "./productLabel.vue";
export default {
  name: "labelContainer",
  components: {
    productLabel,
  },
  props: {
    labels: {
      type: Array,
      default() {
        return [];
      },
    },
    discount: {
      type: Number,
      default() {
        return 0;
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.labelContainer {
  position: absolute;
  left: 0.2rem;
  bottom: 0.2rem;

  &__items {
    display: flex;
    flex-direction: row;
  }
}
</style>