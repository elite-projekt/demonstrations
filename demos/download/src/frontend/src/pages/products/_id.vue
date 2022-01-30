<template>
  <div class="section">
    <div class="card is-clearfix columns">
      <figure class="card-image column">
        <img :src="product.image" alt="Placeholder image" />
      </figure>
      <div class="card-content column is-two-thirds">
        <div class="card-content__title">
          <h2 class="title is-4">
            {{ product.title }}
          </h2>
        </div>
        <div class="card-content__text">
          <p v-html="$t(product.description)"></p>
        </div>
        <div class="card-content__price">
          <span class="title is-3">
            <strong
              >&euro; {{ getPrice(product.price, product.discount) }}</strong
            >
            <span v-if="product.discount" class="discount"
              >&euro; {{ product.price }}</span
            >
          </span>
        </div>
        <div class="card-content__specs">
          <p class="" v-t="'text.specs'" />
          <div v-for="prop in product.props">
            <span> {{ $t(prop.item) + ": " }}</span>
            {{ prop.val ? $t("text.yes") : $t("text.no") }}
          </div>
        </div>
        <div class="card-content__btn">
          <button
            class="button is-primary"
            @click="openModal(product.props, product.isAdvertisment)"
          >
            {{ $t("buttons.buy") }}
          </button>
        </div>
        <label-container
          :discount="product.discount"
          :labels="product.labels"
        />
      </div>
    </div>
    <InfoBox
      :isModalOpen="showModal"
      :text="modalText"
      :title="modalTitle"
      @close-modal="showModal = !showModal"
    />
  </div>
</template>

<script>
import InfoBox from "../../components/modal/InfoBox.vue";
import { MULTISCAN } from "@/assets/constant";
import { getDiscountPrice } from "@/assets/methods";
import LabelContainer from "../../components/product_label/labelContainer.vue";
export default {
  name: "products-id",
  validate({ params }) {
    return /^\d+$/.test(params.id);
  },
  components: {
    InfoBox,
    LabelContainer,
  },
  data() {
    return {
      product: {},
      showModal: false,
      modalText: null,
      modalTitle: null,
    };
  },

  mounted() {
    this.product = this.$store.getters.getProductById(this.$route.params.id);
    this.notifyBackend(this.product.isAdvertisment);
  },
  methods: {
    openModal(props, isAd) {
      let prop = props.filter((p) => p.item === MULTISCAN);
      if (prop && !isAd) {
        this.showModal = true;
        this.modalTitle = prop[0].val
          ? "modal.correctProduct.title"
          : "modal.wrongProduct.title";
        this.modalText = prop[0].val
          ? "modal.correctProduct.text"
          : "modal.wrongProduct.text";
      }
      if (isAd) {
        this.showModal = true;
        this.modalTitle = "modal.driveByError.title";
        this.modalText = "modal.driveByError.text";
      }
    },
    getPrice(price, discount) {
      return getDiscountPrice(price, discount);
    },
    notifyBackend(isAd) {
      if (isAd) {
        this.$axios.post("http://localhost:5001/unsecure");
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.card-content {
  &__text,
  &__specs {
    margin: 15px 0;
  }
  &__btn {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
  }
  &__specs {
    p {
      font-size: 1.3rem;
      font-weight: 300;
    }
  }
}

.card-image {
  .bubble {
    right: 1.5rem;
    top: 1.5rem;
  }
  img {
    margin: auto;
    display: block;
  }
  @media (max-width: 768px) {
    text-align: center;
  }
}

.column {
  padding: 1.75rem;
}

.discount {
  font-weight: 100;
  text-decoration: line-through;
}

.section {
  min-height: calc(100vh - 15.5rem);
}
</style>

