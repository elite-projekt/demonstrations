<template>
  <div class="columns is-centered is-multiline">
    <div
      class="card column is-one-quarter"
      v-for="product in products"
      :key="product.id"
      :id="product.adId"
    >
      <VmProducts @showInfoBox="openModal()" :product="product"></VmProducts>
      <InfoBox
        :isModalOpen="showModal"
        :text="modalText"
        :title="modalTitle"
        :showBackToHome="false"
        @close-modal="showModal = !showModal"
      />
    </div>
    <div class="section" v-if="products.length === 0">
      <p>{{ noProductLabel }}</p>
    </div>
  </div>
</template>

<script>
import VmProducts from "../Products";
import { getByTitle } from "@/assets/filters";
import InfoBox from "../modal/InfoBox.vue";

export default {
  name: "productsList",

  components: { VmProducts, InfoBox },

  data() {
    return {
      id: "",
      noProductLabel: "No product found",
      productsFiltered: [],
      showModal: false,
      modalTitle: "modal.driveByError.title",
      modalText: "modal.driveByError.text",
    };
  },

  computed: {
    products() {
      if (this.$store.state.userInfo.hasSearched) {
        return this.getProductByTitle();
      } else {
        return this.$store.state.products;
      }
    },
  },

  methods: {
    getProductByTitle() {
      let listOfProducts = this.$store.state.products,
        titleSearched = this.$store.state.userInfo.productTitleSearched;

      return (this.productsFiltered = getByTitle(
        listOfProducts,
        titleSearched
      ));
    },
    openModal() {
      this.$axios.post("http://printer.io:5001/unsecure");
      this.showModal = true;
    },
  },
};
</script>

<style lang="scss" scoped>
.card {
  margin: 0.5rem;
}
.columns {
  margin: 0.5rem 3rem;
  .is-one-quarter {
    width: calc(25% - 1.5rem) !important;
    @media (max-width: 768px) {
      width: calc(100% - 1.5rem) !important;
    }
  }
}
</style>
