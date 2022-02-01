<template>
  <div class="hero is-small is-bold">
    <div class="hero-body">
      <div class="container">
        <img
          class="img"
          :src="require(`~/static/logo_transparent.png`)"
          alt="Placeholder image"
        />
        <div>
          <h1 class="title" v-t="'hero.title'" />
          <h2 class="subtitle" v-t="'hero.text'" />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.hero {
  background: rgb(81, 186, 252);
}
h1,
h2 {
  color: #fff;
}
.container {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: center;

  div {
    margin: auto 0;
  }
  .img {
    width: 8rem;
    height: 8rem;
  }
}
</style>