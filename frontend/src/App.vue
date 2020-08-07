<template>
  <v-app>
    <v-main>
      <Header/>
      <Content/>
    </v-main>
  </v-app>
</template>

<script>
import Header from './components/Header'
import Content from './components/Content'

export default {
  name: 'App',

  components: {
    Header,
    Content
  },

  data: () => ({
    //
  }),
};
</script>
