<template>
  <div id="app" class="bg-light">
    <!-- <header class="sticky-top"><HeaderTmp :key="this.$i18n.locale"/></header> -->
    <header class="sticky-top"><HeaderTmp/></header>
    <div class="desktop pt-3 container"><router-view :key="$route.fullPath"/></div>
  </div>
</template>

<script>
// import HeaderDefault from '@/components/HeaderDefault.vue';
import HeaderTmp from '@/components/HeaderTmp.vue';

export default {
  components: {
    // HeaderDefault,
    HeaderTmp,
  },
  watch: {
    '$i18n.locale': function () {
      document.title = this.$t('Profile.name');
    },
  },
  async created() {
    this.$store.dispatch('fetchAllEvents');
    this.$store.dispatch('fetchGitData', 'takuto');
  },
};
</script>

<style lang="stylus">
html
  min-height 100vh
  overflow-y scroll
body
  min-height inherit
#app
  @extend body
  font-family Avenir, Helvetica, Arial, sans-serif
  -webkit-font-smoothing antialiased
  -moz-osx-font-smoothing grayscale
$header_height = 61px
.sticky-top
  min-height $header_height
.desktop
  min-height "-o-calc(100% - %s - 1px)" % $header_height // opera
  min-height "-webkit-calc(100% - %s - 1px)" % $header_height // google, safari
  min-height "-moz-calc(100% - %s - 1px)" % $header_height // firefox
  min-height "calc(100% - %s - 1px)" % $header_height // firefox
*[style*="display: none"]
  display none!important
.event-description > *
  display inline
img.emoji
  height 1em
  width 1em
  vertical-align -0.1em
.pointer
  cursor pointer
</style>
