<template>
  <div :class="[getLabelClass(productLabel), 'label']">
    <div>
      <p v-if="typeMatches(productLabel, typeAdvertisement)">
        {{ $t("text.advertisement").toUpperCase() }}
      </p>
      <p v-if="typeMatches(productLabel, typeDiscount)">
        {{ discount + "%" }}
      </p>
      <p v-if="typeMatches(productLabel, typeNew)">
        {{ $t("text.newProduct").toUpperCase() }}
      </p>
    </div>
  </div>
</template>

<script>
import { LABELS } from "@/assets/constant";
export default {
  name: "productLabel",
  props: {
    productLabel: {
      type: String,
      default() {
        return {};
      },
    },
    discount: {
      type: Number,
      default() {
        return 0;
      },
    },
  },
  data() {
    return {
      typeDiscount: LABELS[0].type,
      typeAdvertisement: LABELS[1].type,
      typeNew: LABELS[2].type,
    };
  },
  methods: {
    getLabelClass(type) {
      return LABELS.filter((l) => l.type == type).map((l) => l.class);
    },
    typeMatches(type, expectedType) {
      return type === expectedType;
    },
  },
};
</script>

<style lang="scss" scoped>
.label {
  border-radius: 5px;
  width: 4rem;
  height: 2rem;
  text-align: center;
  padding: 0.3rem;
  color: white;
  font-weight: 200;
  margin: 0.2rem 0.2rem;
}
.discount {
  background-color: #ba1f33;
}
.advertisement {
  background-color: #00b295;
}
.new {
  background-color: #1d3ec3;
}
</style>