<template>
  <div id="datasets">
    <h1 class="my-2 px-4 py-1 border-bottom">{{ $t("Head.datasets") }}</h1>
    <div v-for="e in events" :key="e.year" class="container-fluid px-0">
      <h3 class="m-0 mt-3">{{ $d(new Date().setFullYear(e.year), 'year') }}</h3>
      <div v-for="event in e.e" :key="event.id" class="border-bottom text-justify mb-2 p-2 d-flex flex-column">
        <div class="d-flex flex-wrap justify-content-end">
          <h4 class="mt-auto mb-0 mr-auto"><router-link
            :to="{ name: 'event', params: { id: $_eventURL(event.id) } }"
            class="font-weight-bold"
            v-html="event.title"
          ></router-link></h4>
          <span class="d-md-none w-100"></span>
          <div class="d-flex">
            <span class="align-self-end text-left text-md-right pr-2">({{ $d(new Date(event.created_at * 1000), 'short') }})</span>
            <div class="d-flex justify-content-end" style="min-width: 110px;">
              <button v-if="event.bibtex" @click="event.showbibtex ^= 1" class="btn btn-sm btn-outline-secondary mx-1">BiBTeX</button>
              <a v-if="event.pdflink" :href="event.pdflink" class="btn btn-sm btn-outline-primary mx-1">PDF</a>
              <button @click="event.showDetails ^= 1" class="btn btn-sm btn-outline-info mx-1" :class="{ active: event.showDetails }">{{ $t('Message.details') }}</button>
            </div>
          </div>
        </div>
        <div v-show="event.showDetails" class="mt-2">
          <img :src="event.img" :alt="event.title" style="height: 85px;" class="float-left mr-3 my-2">
          <section v-html="event.description" class="event-description"></section>
        </div>
        <div> <display-bibtex v-show="event.showbibtex" :cite="event.bibtex" :bibtexAlways="true"></display-bibtex> </div>
      </div>
    </div>
  </div>
</template>

<script>
import DisplayBibtex from '@/components/DisplayBibtex.vue';

export default {
  components: { DisplayBibtex },
  computed: {
    events() {
      const thisYear = new Date().getFullYear();
      const result = [];
      this.$store.getters.getEvents.forEach((event) => {
        if (event.category !== 'datasets' || event.lang !== this.$i18n.locale) return;
        const year = new Date(event.created_at * 1000).getFullYear();
        if (thisYear - year >= result.length) {
          result.push(...Array.from({ length: thisYear - year - result.length + 1 }, (x, i) => ({ year: thisYear - result.length - i, e: [] })));
        }
        result[thisYear - year].e.push(Object.assign(event, {
          showDetails: true,
          showbibtex: false,
        }));
      });
      result.forEach((event) => {
        event.e.sort((a, b) => (b.created_at - a.created_at));
      });
      return result;
    },
  },
};
</script>
