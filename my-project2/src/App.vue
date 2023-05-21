<template>
  <v-app>
    <div id="app">
      <!--    <div id="nav">-->
      <!--      <router-link to="/">Home</router-link>-->
      <!--    </div>-->

      <router-view/>
    </div>
  </v-app>
</template>

<style lang="scss">
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    background: url('https://photo69.mac89.com/2021/01/15/10/15102628_fe285d5845_small.jpg')
    no-repeat center center;
    background-size: 100% 100%;
  }

  #nav {
    padding: 30px;

    a {
      font-weight: bold;
      color: #2c3e50;

      &.router-link-exact-active {
        color: #42b983;
      }
      }
  }
</style>
