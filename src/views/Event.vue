<template>
  <div id="event">
    <div v-if="pageID < 0">
      <h1>{{ $t('Notready.title') }}</h1>
      <p>{{ $t('Notready.msg') }}</p>
      <hr>
    </div>
    <div v-if="pageData === undefined">
      <not-found></not-found>
    </div>
    <section id="markdown_body" v-html="markdown_body"></section>
    <div v-if="pageData !== undefined" class="mt-4 d-flex align-items-center justify-content-center">
      <div v-if="pageData.bibtex" class="w-auto" style="max-width: 75%;">
        <display-bibtex v-for="b in pageData.bibtex.split(' ')" :key="b" :cite="b"></display-bibtex>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable no-unused-vars */
import DisplayBibtex from '@/components/DisplayBibtex.vue';
import NotFound from '@/views/NotFound.vue';
import markdownIt from '@/plugins/markdown';

export default {
  components: { DisplayBibtex, NotFound },
  computed: {
    pageID() {
      return parseInt(this.$route.params.id, 10);
    },
    pageData() {
      return this.$store.getters.getEvents.find((e) => e.id === Math.abs(this.pageID));
    },
  },
  data() {
    return {
      markdown_body: '',
    };
  },
  methods: {
    fetch_md() {
      if (this.pageData === undefined) return;
      this.$axios.get(this.pageData.markdown).then((response) => {
        this.markdown_body = markdownIt.render(response.data);
      });
    },
    change_lang(lang) {
      if (this.pageData !== undefined) {
        let nextID = this.$store.getters.getTopicGroup[this.pageData.topic_id][lang];
        if (nextID === undefined) nextID = -this.pageID;
        if (this.pageData.lang === lang) nextID = Math.abs(this.pageID);
        if (nextID === this.pageID) return;
        this.$router.push({
          name: 'event',
          params: {
            id: nextID,
          },
        });
      }
    },
  },
  watch: {
    '$i18n.locale': function (to) {
      this.change_lang(to);
    },
  },
  created() {
    this.fetch_md();
  },
};
</script>

<style lang="stylus" scoped>
@import '../plugins/markdown'
</style>

<style scoped>
#markdown_body ::v-deep(img) {
  max-width: 100%;
  align-content: center;
}
</style>
