<template>
  <div class="main">
    <VmHero></VmHero>
    <VmProductsList></VmProductsList>
  </div>
</template>

<script>
import VmProductsList from "@/components/products_list/ProductsListContainer";
import VmHero from "@/components/hero/Hero";

export default {
  name: "index",
  components: {
    VmProductsList,
    VmHero,
  },
};
</script>

<style>
@import "bootstrap-icons/font/bootstrap-icons";
.main {
  min-height: calc(100vh - 15.5rem);
}
</style>
