module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  assetsDir: 'static',
  devServer: {
    proxy: 'http://localhost:5000'
  }
}
