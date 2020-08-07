module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  publicPath: './',
  assetsDir: 'static',
  devServer: {
    proxy: 'http://localhost:5000'
  }
}
