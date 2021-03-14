<template>
  <div id="headertmp">
    <nav class="navbar navbar-expand-sm navbar-dark bg-dark">
      <router-link to='/' class="navbar-brand">
        <img src="favicon.ico" :alt="$t('Profile.name')" class="top-icon mx-1">
        {{ $t("Profile.name") }}
      </router-link>
      <button class="navbar-toggler" type="button"
        data-toggle="collapse"
        data-target="#nav-collapse"
        aria-controls="nav-collapse"
        aria-expanded="false"
        aria-label="Toggle Navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="nav-collapse">
        <div class="navbar-nav">
          <a class="nav-item nav-link" :href="`https://esslab.jp/${$i18n.locale}`">{{ $t("Head.lab") }}</a>
          <router-link class="nav-item nav-link" to="/resume">{{ $t("Head.resume") }}</router-link>
          <router-link class="nav-item nav-link" to="/researches">{{ $t("Head.researches") }}</router-link>
          <router-link class="nav-item nav-link" to="/papers">{{ $t("Head.papers") }}</router-link>
          <router-link class="nav-item nav-link" to="/datasets">{{ $t("Head.datasets") }}</router-link>
          <router-link class="nav-item nav-link" to="/codes">{{ $t("Head.codes") }}</router-link>
        </div>
        <div class="ml-auto navbar-nav">
          <div class="d-flex justify-content-around">
            <a v-for="l of $i18n.availableLocales" :key="l" @click="$i18n.locale = l">
              <img :src="`img/languages/${l}.jpg`" class="language-flag mx-2 pointer"/>
            </a>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<style lang="stylus" scoped>
img
  height 1.1em
  vertical-align bottom
.top-icon
  height 30px
</style>
