<template>
  <div class="footer">
    <div class="columns container">
      <div class="column" v-for="column in footerColumns">
        <div class="icon">
          <i :class="'bi ' + column.icon" />
        </div>
        <div class="text">
          <h2 v-t="column.title" />
          <p v-t="column.description" />
        </div>
      </div>
      <div class="column has-text-right">
        <div>
          <span>(C) SS 2021</span>
          <a class="ml-25" href="https://h-da.de/" target="_blank"
            >Hochschule Darmstadt</a
          >
          <span class="d-none d-sm-inline-block">, Projekt ELITE </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "VmFooter",
  data() {
    return {
      footerColumns: this.$store.state.footerItems,
    };
  },
};
</script>

<style lang="scss" scoped>
.footer {
  background: #b9e2fc;
  color: black;
  padding: 2rem;
  min-height: 12rem;

  h2 {
    font-weight: 500;
    font-size: 1.1rem;
  }

  .bi:before {
    font-size: 1.7rem;
  }

  .columns {
    display: flex;

    flex-wrap: wrap;
    max-width: none;
    @media (max-width: 768px) {
      flex-direction: column;
    }

    .column {
      display: flex;
      justify-content: center;
      flex-basis: calc(25% - 1rem);

      .icon {
        margin: 0.8rem;
        @media (max-width: 768px) {
          width: 3rem;
        }
      }

      .text {
        @media (max-width: 768px) {
          width: 12rem;
        }
      }
    }
  }
}
</style>
