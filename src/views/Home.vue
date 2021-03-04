<template>
  <div id="home" class="row">
    <div id="profile" class="h-card col-12 col-lg-3 col-md-4 d-flex flex-column flex-sm-row flex-md-column flex-nowrap justify-content-center align-items-center">
      <div class="u-photo d-block m-2">
        <img id="protrait" src="@/assets/profile.jpg" alt="売れない俳優" title="売れない俳優" class="rounded">
      </div>
      <div id="myinfos" class="my-2">
        <h2 class="vcard-names mx-3">
          <span class="p-name vcard-fullname d-block" itemprop="name">{{ $t("Profile.name") }}</span>
          <span class="p-nickname vcard-username d-block" itemprop="additionalName">HN: {{ $t('Profile.hn') }}</span>
        </h2>
        <div class="d-none d-sm-block overflow-hidden">
          <svg id="git_calendar" ref="git_calendar" height="122" width="100%"></svg>
        </div>
      </div>
    </div>
    <div class="col-12 col-lg-9 col-md-8 px-md-2">
      <HighLights/>
      <br>
      <Notifications/>
    </div>
  </div>
</template>

<script>
import HighLights from '@/components/HighLights.vue';
import Notifications from '@/components/Notifications.vue';

const zeroPad = (num, length) => (`0000000000${num}`).slice(-length);
class Color {
  constructor(c) {
    if (c instanceof Array) {
      this.color = c;
    } else {
      this.color = [parseInt(c.slice(1, 3), 16), parseInt(c.slice(3, 5), 16), parseInt(c.slice(5, 7), 16)];
    }
  }

  getRGB() {
    return this.color;
  }

  getColorCode() {
    return `#${zeroPad(this.color[0].toString(16), 2)}${zeroPad(this.color[1].toString(16), 2)}${zeroPad(this.color[2].toString(16), 2)}`;
  }

  darken(stage) {
    for (let i = 0; i < stage; i++) {
      this.color = this.color.map((x) => Math.round(x * 0.9));
    }
  }
}

export default {
  components: {
    HighLights,
    Notifications,
  },
  data() {
    return {
      gitCalendar: undefined,
    };
  },
  methods: {
    async fillGitCalendar() {
      if (this.gitCalendar === undefined) return;
      const color = (contributions) => {
        const defaultColors = ['#ebedf0', '#c6e48b', '#b5dc8f', '#9bd17b', '#7bc96f'];
        if (contributions < 5) return defaultColors[contributions];

        const c = new Color(defaultColors[4]);
        c.darken(contributions - 4);
        return c.getColorCode();
      };
      const fullWidth = this.gitCalendar.clientWidth - 30;
      if (Object.keys(this.$store.getters.getGitData).length === 0) await this.$store.dispatch('fetchGitData', 'takuto');
      const today = new Date();
      const date = new Date();
      date.setDate(date.getDate() - Math.floor(fullWidth / 13) * 7 - date.getDay());
      let html = '';
      for (let column = 7, month = -1; date <= today; date.setDate(date.getDate() + 1)) {
        if (date.getDay() === 0) {
          column += 13;
          if (date.getMonth() !== month) {
            month = date.getMonth();
            html += `<text width="10" height="10" x="${column}" y="18">${month + 1}</text>`;
          }
        }
        const contributions = this.$store.getters.getGitData[`${date.getFullYear()}-${zeroPad(date.getMonth() + 1, 2)}-${zeroPad(date.getDate(), 2)}`] || 0;
        html += `<rect fill="${color(contributions)}" width="10" height="10" x="${column}" y="${date.getDay() * 13 + 19}"><title>${contributions} contributions on ${date.toDateString()}</title></rect>`;
      }
      if (this.gitCalendar) {
        this.gitCalendar.innerHTML += `${html }
        <text width="10" height="10" x="10" y="45" text-anchor="middle">M</text>
        <text width="10" height="10" x="10" y="71" text-anchor="middle">W</text>
        <text width="10" height="10" x="10" y="97" text-anchor="middle">F</text>`;
      }
    },
  },
  mounted() {
    this.gitCalendar = this.$refs.git_calendar;
    this.fillGitCalendar();
  },
};
</script>

<style lang="stylus" scoped>
img
  width 216px
  height 308px
  object-fit cover
.overflow-hidden
  overflow hidden!important
#git_calendar
  @media (prefers-color-scheme: dark)
    fill green
</style>
