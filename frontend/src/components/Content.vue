<template>
  <v-container>
    <v-card class="mx-auto" width="500" outlined>
      <v-progress-linear v-if="progress" absolute indeterminate color="success"/>
      <v-card-text>
        
        <!--URL入力-->
        <v-text-field
                v-model="inputUrl"
                color="success"
                label="Twitter Video URL"
                hint="https://twitter.com/i/status/{TweetID}"
                append-icon="mdi-magnify"
                outlined
                @click:append="search"
                v-on:keyup.enter="search"
        />

        <v-btn v-if="displayVideoUrl" color="success" @click="sheet=true" bottom text block>Tweet info</v-btn>

        <!--動画-->
        <div v-if="displayVideoUrl" class="text-center mt-4">
          <iframe width="320" height="300" :src="displayVideoUrl" allowfullscreen/>
        </div>

        <!--ダウンロードボタン-->
        <div v-show="downloadVideoUrls[1]" class="text-center">
          <p class="mt-4 mb-3">Download</p>
          <v-divider/>
          <v-btn
                  class="mr-2 ml-2 mt-4"
                  color="success"
                  style="text-transform: none"
                  v-for="key in Object.keys(downloadVideoUrls)"
                  :key="key"
                  @click="download(downloadVideoUrls[key]['url'])"
                  :disabled="progress"
                  small
                  outlined
                  >{{ downloadVideoUrls[key]['size'] }}
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <!--Snackbar-->
    <v-snackbar v-model="snackbar.active" timeout="3000" :color="snackbar.color" bottom absolute>
      {{ snackbar.text }}
    </v-snackbar>

    <!--TweetInfo-->
    <v-bottom-sheet v-model="sheet">
      <v-sheet class="text-center" height="auto" outlined>
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <v-avatar class="mt-4 mb-4" v-on="on" @click="jumpTwitter(tweetInfo['screen_name'])">
              <img :src="tweetInfo['profile_image_url']" alt="icon">
            </v-avatar>
          </template>
          <span>Open Twitter!</span>
        </v-tooltip>

        <p>{{ tweetInfo['name'] }} {{ '@' + tweetInfo['screen_name'] }}</p>
        <v-divider/>
        <p class="mt-3">{{ tweetInfo['tweet_text'] }}</p>
        <p class="grey--text">created at {{ tweetInfo['created_at'] | dayjs}}</p>
      </v-sheet>
    </v-bottom-sheet>

  </v-container>
</template>

<script>
import axios from 'axios'
import dayjs from 'dayjs'

dayjs.locale('ja')

export default {
  name: 'Content',

  data() {
    return {
      sheet: false,
      progress: false,
      snackbar: {},
      inputUrl: '',
      displayVideoUrl: '',
      downloadVideoUrls: {},
      mediaUrl: '',
      tweetInfo: {}
    }
  },

  filters: {
    dayjs(value) {
      return dayjs(value).format('YYYY-M-D hh:mm:ss')
    }
  },

  methods: {
    showSnackbar(text, color) {
      this.snackbar = {
        text: text,
        color: color,
        active: true
      }
    },

    jumpTwitter(screenName) {
      window.open('https://twitter.com/' + screenName)
    },

    search() {
      if (!this.inputUrl) {
        this.showSnackbar('URlを入力してください。', 'warning')
        return
      }
      this.progress = true
      axios({
        method: 'post',
        url: '/search',
        headers: {'Content-Type': "application/json"},
        data: JSON.stringify({inputUrl: this.inputUrl})
      })
        .then(res => {
          this.inputUrl = ''
          this.progress = false
          if (res.data['status']) {
            this.showSnackbar(res.data.message, 'success')
            this.displayVideoUrl = res.data['display_video_url']
            this.downloadVideoUrls = res.data['download_video_urls']
            this.mediaUrl = res.data['media_url']
            this.tweetInfo = res.data["tweet_info"]
          } else {
            this.showSnackbar(res.data.message, 'warning')
          }
        })
        .catch(() => {
          this.inputUrl = ''
          this.progress = false
          this.showSnackbar('サーバーエラーが発生しました。', 'red')
        })
    },

    download(videoUrl) {
      this.progress = true
      axios({
        method: 'post',
        responseType: 'blob',
        url: '/download',
        headers: {'Content-Type': "application/json"},
        data: JSON.stringify({downloadUrl: videoUrl})
      })
        .then(res => {
          this.progress = false
          const blob = new Blob([res.data], {type: 'video/mp4'})
          const link = document.createElement('a')
          link.download = this.createFileName()
          link.href = window.URL.createObjectURL(blob)
          link.click()
        })
        .catch(() => {
          this.progress = false
          this.showSnackbar('サーバーエラーが発生しました。', 'red')
        })
    },

    createFileName() {
      const base = 'abcdefghijklmnopqrstuvwxyz0123456789'
      let result = ''
      for(let i=0; i<10; i++){
        result += base[Math.floor(Math.random() * base.length)]
      }
      return result + '.mp4'
    }
  }
}
</script>
