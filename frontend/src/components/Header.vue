<template>
    <v-app-bar rounded dense shaped>
      <v-img max-width="30" max-height="30" src="../assets/logo.png" alt="logo" contain/>
      <v-toolbar-title class="ml-3 ">twiv-dl</v-toolbar-title>

      <v-spacer/>

      <!--Buttons-->
      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="dialog=true">
            <v-icon>mdi-help</v-icon>
          </v-btn>
        </template>
        <span>How To Use</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="openTwitter">
            <v-icon>mdi-twitter</v-icon>
          </v-btn>
        </template>
        <span>Share twiv-dl!</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on" @click="openGithub">
            <v-icon>mdi-github</v-icon>
          </v-btn>
        </template>
        <span>Source code is here!</span>
      </v-tooltip>

      <!--使い方ダイアログ-->
      <v-dialog v-model="dialog" width="500">
        <v-card>
          <v-card-title>How To Use</v-card-title>
          <v-card-text>
            <p>①</p>
            <p>②</p>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-app-bar>
</template>

<script>
export default {
  name: 'Header',

  data() {
    return {
      dialog: false
    }
  },

  methods: {
    openTwitter() {
      window.open('https://twitter.com/share?url=https://twivdl.appspot.com&text=twiv-dl%20Twitter%E3%81%AE%E5%8B%95%E7%94%BB%E3%82%92%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89%E3%81%A7%E3%81%8D%E3%82%8BWeb%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%EF%BC%81%20', '_blank')
    },

    openGithub() {
      window.open('https://github.com/miya/twiv-dl-vue', '_blank')
    }
  }
}
</script>
