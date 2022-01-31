<template>
  <div :class="[isModalOpen ? 'is-active' : '', 'modal']">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{ $t(title) }}</p>
        <button
          class="delete"
          aria-label="close"
          @click="closeModal()"
        ></button>
      </header>
      <section class="modal-card-body">
        <div>{{ $t(text) }}</div>
      </section>
      <footer class="modal-card-foot">
        <nuxt-link
          v-if="showBackToHome"
          class="button is-success"
          :to="localePath({ name: 'index' })"
        >
          {{ $t(backToHomeLabel) }}
        </nuxt-link>
        <button class="button is-success" @click="closeModal()">
          {{ $t(closeLabel) }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: "infomodal",
  data() {
    return {
      backToHomeLabel: "modal.backToHome",
      closeLabel: "modal.close",
    };
  },
  props: {
    isModalOpen: {
      type: Boolean,
      default() {
        false;
      },
    },
    title: {
      type: String,
      default() {
        "";
      },
    },
    text: {
      type: String,
      default() {
        "";
      },
    },
    showBackToHome: {
      type: Boolean,
      default() {
        true;
      },
    },
  },
  methods: {
    closeModal() {
      this.$emit("close-modal");
    },
  },
};
</script>

