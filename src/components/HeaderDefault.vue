<template>
  <div id="headerDefault">
    <b-navbar toggleable="sm" type="dark" variant="dark">
      <b-navbar-brand to="/" class="mr-auto px-2">
        <img src="favicon.ico" class="d-inline-block align-top" :alt="$t('Profile.name')">
        {{ $t("Profile.name") }}
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :href="`https://esslab.jp/${$i18n.locale.value}`">{{ $t("Head.lab") }}</b-nav-item>
          <b-nav-item to="/resume">{{ $t("Head.resume") }}</b-nav-item>
          <b-nav-item to="/researches">{{ $t("Head.researches") }}</b-nav-item>
          <b-nav-item to="/papers">{{ $t("Head.papers") }}</b-nav-item>
          <b-nav-item to="/datasets">{{ $t("Head.datasets") }}</b-nav-item>
          <b-nav-item to="/codes">{{ $t("Head.codes") }}</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <div class="d-flex justify-content-around">
            <img
              v-for="l of $i18n.availableLocales"
              :key="l"
              :src="`img/languages/${l}.jpg`"
              @click="$i18n.locale = l"
              class="language-flag mx-3"
            />
          </div>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>
