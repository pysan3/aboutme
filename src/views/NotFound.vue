<template>
  <div id="notfound" class="d-flex justify-content-center align-items-center text-center">
    <div class="notfound">
      <div class="notfound-404">
        <h1>4<span><img src="@/assets/crying.png" alt="0"></span>4</h1>
      </div>
      <h2>{{ $t('Notfound.title') }}</h2>
      <p>{{ $t('Notfound.msg') }}</p>
      <router-link to="/">{{ $t('Notfound.return') }}</router-link>
    </div>
  </div>
</template>

<style lang="stylus" scoped>
#notfound
  height 80vh
.notfound .notfound-404
  height 190px
.notfound .notfound-404 h1
  font-family 'Montserrat', sans-serif
  font-size 140px
  font-weight 700
  margin 0px
  color #232323
.notfound .notfound-404 h1 span img
  width 120px
  height 120px
  margin 0 2px
.notfound h2
  font-family 'Montserrat', sans-serif
  font-size 22px
  font-weight 700
  margin 0
  text-transform uppercase
  color #232323
.notfound p
  font-family 'Montserrat', sans-serif
  color #787878
  font-weight 300
.notfound a
  font-family 'Montserrat', sans-serif!important
  display inline-block
  padding 12px 30px
  font-weight 700
  background-color #f99827
  color #fff
  border-radius 40px
  text-decoration none
  -webkit-transition 0.2s all
  transition 0.2s all
.notfound ahover
  opacity 0.8
</style>
