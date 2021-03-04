<template>
  <div
    v-if="bibtex !== undefined"
    @mouseover="rawBibtex = true"
    @mouseleave="rawBibtex = false; copied = 'Copy'"
    class="displaybibtex text-align-left d-flex"
  >
    <div class="flex-shrink-1 px-2">
      <h5>
      <i class="fas fa-quote-right"></i>
      </h5>
    </div>
    <div>
      <h5><b>{{ getField('title') }}</b></h5>
      <div>{{ getField('author') }}</div>
      <div>
        <i v-if="getField('journal')">{{ getField('journal') }}</i>
        <a v-else :href="getField('howpublished').slice(3)">Article</a>
        , {{ getField('year') }}
      </div>
      <transition>
        <div v-show="rawBibtex || bibtexAlways" class="rawbibtex rounded border p-2" style="position: relative">
          <a
            id="clipboard"
            @click="copyBibtex()"
            class="clipboard h4 leader"
            style="cursor: pointer;"
          ><i class="fas fa-clipboard"></i></a>
          <!-- TODO: after bootstrap-vue.v3 -->
          <!-- <b-tooltip target="clipboard" triggers="hover">{{ copied }}!</b-tooltip> -->
          <pre class="m-0">{{ bibtex.raw }}</pre>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  props: ['cite', 'bibtexAlways'],
  computed: {
    bibtex() {
      return this.$store.getters.getBibtex[this.cite];
    },
  },
  data() {
    return {
      rawBibtex: false,
      copied: 'Copy',
    };
  },
  methods: {
    getField(name) {
      if (this.bibtex === undefined) return undefined;
      const field = this.bibtex.fields.find((e) => e.name === name);
      return field !== undefined ? field.value.replaceAll(/[{\\}]/g, '') : undefined;
    },
    copyBibtex() {
      navigator.clipboard.writeText(this.bibtex.raw);
      this.copied = 'Copied';
    },
  },
};
</script>

<style lang="stylus" scoped>
.rawbibtex
  background-color lightgrey

pre
  overflow auto
  white-space pre-wrap
.clipboard
  position absolute
  right .5rem
.v-enter-active, .v-leave-active
  transition opacity .5s
.v-enter, .v-leave-to
  opacity 0
</style>
