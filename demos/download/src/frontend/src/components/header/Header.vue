<template>
  <div>
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <nuxt-link :to="localePath({ name: 'index' })" class="navbar-item">
          <h1 class="title is-3 is-flex-mobile"></h1>
        </nuxt-link>
      </div>

      <div class="navbar-menu is-active">
        <div class="navbar-start">
          <div class="navbar-item field">
            <VmSearch></VmSearch>
          </div>
        </div>
        <div class="navbar-end">
          <LangDropdown />
          <div class="navbar-item social">
            <a href="#" class="icon" :title="facebookTooltip">
              <i class="fab fa-facebook"></i>
            </a>
            <a href="#" class="icon" :title="twitterTooltip">
              <i class="fab fa-twitter"></i>
            </a>
            <a href="#" class="icon" :title="instagramTooltip">
              <i class="fab fa-instagram"></i>
            </a>
            <a href="#" class="icon" :title="linkedinTooltip">
              <i class="fab fa-linkedin"></i>
            </a>
          </div>
          <!-- <div class="navbar-item shopping-cart" @click="showCheckoutModal">
            <span class="icon">
              <i class="fa fa-shopping-cart"></i>
            </span>
            <span :class="[numProductsAdded > 0 ? 'tag is-info' : '']">{{
              numProductsAdded
            }}</span>
          </div> -->
        </div>
      </div>

      <!-- For mobile and tablet -->
      <!-- <div v-show="isMenuOpen" class="navbar-end">
        <VmMenu></VmMenu>
      </div> -->

      <!-- For desktop -->
      <!-- <div class="navbar-end is-hidden-mobile">
        <VmMenu></VmMenu>
      </div> -->
    </nav>
  </div>
</template>

<script>
import VmMenu from "../menu/Menu";
import VmSearch from "../search/Search";
import LangDropdown from "./languageDropdown.vue";
export default {
  name: "VmHeader",

  data() {
    return {
      linkedinTooltip: "Follow us on Linkedin",
      facebookTooltip: "Follow us on Facebook",
      twitterTooltip: "Follow us on Twitter",
      instagramTooltip: "Follow us on Instagram",
      isCheckoutActive: false,
      isMenuOpen: false,
    };
  },

  components: {
    VmSearch,
    VmMenu,
    LangDropdown,
  },

  computed: {
    numProductsAdded() {
      return this.$store.getters.productsAdded.length;
    },
  },

  methods: {
    showCheckoutModal() {
      this.$store.commit("showCheckoutModal", true);
    },
  },
};
</script>

<style lang="scss" scoped>
.title {
  background: url("../../static/printerio_cover.png") no-repeat;
  background-size: cover;
  width: 140px;
  height: 55px;
}
.shopping-cart {
  cursor: pointer;
}
.navbar-brand {
  a {
    color: grey;
    padding: 0;
  }
}
@media (min-width: 768px) {
  .navbar {
    min-height: 3.25rem !important;
    display: flex;
    align-items: stretch;
    .navbar-item,
    .navbar-link {
      align-items: center;
      display: flex;
    }
    .navbar-menu {
      -webkit-box-flex: 1;
      flex-grow: 1;
      flex-shrink: 0;
      display: flex;
      .navbar-start {
        justify-content: flex-start;
        margin-right: auto;
        display: flex;
      }
      .navbar-end {
        justify-content: flex-end;
        margin-left: auto;
      }
    }
  }
}

.navbar-end {
  display: flex;
  flex-wrap: wrap;
  align-items: center;

  @media (max-width: 768px) {
    justify-content: center;
  }
}
</style>
