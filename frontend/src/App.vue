<template>
  <v-app>
    <v-main>
      <Header/>
      <Contents/>
    </v-main>
  </v-app>
</template>

<script>
import Header from './components/Header'
import Contents from './components/Content'

export default {
  name: 'App',

  components: {
    Header,
    Contents
  },

  data: () => ({
    //
  }),
};
</script>
