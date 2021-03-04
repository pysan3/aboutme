<template>
  <div id="nofitications" class="border p-2 rounded">
    <h2 class="px-4 py-1 border-bottom">{{ $t('Message.notifications') }}</h2>
    <div class="container-fluid mt-3">
      <div v-for="n in notifications" :key="n.created_at" class="row">
        <div class="col-auto align-self-start"><p>{{ $d(new Date(n.date * 1000), 'date') }}</p></div>
        <div class="col row no-gutters">
          <div class="col"><h5 v-html="n.content[$i18n.locale]"></h5></div>
          <div class="col-auto ml-auto" v-if="n.link[$i18n.locale]"><a :href="n.link[$i18n.locale]">[{{ $t('Message.details') }}]</a></div>
          <div class="w-100"></div>
          <div class="col-12" v-if="n.description[$i18n.locale]"><p v-html="n.description[$i18n.locale]"></p></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      notifications: [],
    };
  },
  created() {
    this.$axios.get(`events/notifications.json?nocache=${ new Date().getTime()}`).then((response) => {
      this.notifications = response.data.sort((a, b) => (b.date - a.date));
    });
  },
};
</script>
