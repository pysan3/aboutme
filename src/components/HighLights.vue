<template>
  <div id="highlights" class="border p-2 rounded">
    <h2 class="px-4 py-1 border-bottom">{{ $t("Message.highlights") }}</h2>
    <div class="row m-0">
      <div v-for="event in event_list" :key="event.id" class="col-12 col-sm-6 col-lg-4 p-1">
        <div class="border rounded text-justify px-2" style="max-height: 150px; overflow: hidden;">
          <!-- <object :data="event['src_location']" type="text/html"></object> -->
          <h5 class="font-weight-bold mt-2 mb-0">
            <span v-show="event.version > 0 && (Date.now() - event.created_at * 1000) / 86400000 < 14">[{{ $t('Message.updated') }}]</span>
            <span><router-link
              :to="{ name: 'event', params: { id: $_eventURL(event.id) } }"
              v-html="event.title"
            ></router-link></span>
          </h5>
          <p class="text-secondary m-1" @click="$router.push({ name: event.category })" style="cursor: pointer">
            {{ $t(`Head.${event.category}`) }}・{{ $d(new Date(event.created_at * 1000), 'short') }}
          </p>
          <hr class="my-1">
          <section v-html="event.description" class="event-description"></section>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    event_list() {
      if (!this.$store.getters.getEvents) return [];
      return this.$store.getters.getEvents.filter((e) => e.lang === this.$i18n.locale).sort((a, b) => b.created_at - a.created_at).slice(0, 7);
    },
  },
};
</script>
