<template>
  <div>
    <div class="card-image">
      <figure class="image">
        <img :src="product.image" alt="Placeholder image" />
      </figure>
    </div>
    <div class="card-content">
      <div class="media">
        <div class="media-content">
          <p class="title is-4">{{ product.title }}</p>
        </div>
      </div>
      <div class="content is-clearfix">
        <p>{{ $t(product.category) }}</p>
        <p class="price">
          <span class="title is-4">
            <strong
              >&euro; {{ getPrice(product.price, product.discount) }}</strong
            >
            <span v-if="product.discount" class="discount"
              >&euro; {{ product.price }}</span
            >
          </span>
        </p>
        <label-container
          :discount="product.discount"
          :labels="product.labels"
        />
      </div>
    </div>
    <nuxt-link
      class="details"
      :to="
        localePath({
          name: 'products-id',
          params: {
            id: product.id,
          },
        })
      "
    >
    </nuxt-link>
  </div>
</template>

<script>
import { getDiscountPrice } from "@/assets/methods";
import labelContainer from "./product_label/labelContainer.vue";
export default {
  components: { labelContainer },
  name: "products",
  props: ["product"],
  methods: {
    getPrice(price, discount) {
      return getDiscountPrice(price, discount);
    },
  },
};
</script>

<style lang="scss" scoped>
.details {
  cursor: pointer;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;

  &:hover {
    border: 1px solid #51bafc;
  }
}
.button,
.select {
  z-index: 2;
}
.select {
  position: absolute;
  right: 15px;
  bottom: 35px;
}
.card-content {
  padding: 0;
  .media {
    margin-bottom: 0.5rem;
    min-height: 3.5rem;
  }
  .content {
    margin-bottom: 3rem;
  }
}
.buttons {
  margin: 0;
}

.media {
  .media-content {
    overflow-x: unset;
  }
}

.price {
  bottom: 1rem;
  right: 1rem;
  position: absolute;
}

.discount {
  font-weight: 100;
  text-decoration: line-through;
}

.content p:not(:last-child) {
  margin-bottom: 2rem;
}
</style>


