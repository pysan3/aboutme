import $store from '@/store';

export default {
  methods: {
    $_eventURL(eventID) {
      const event = $store.getters.getEvents.find((e) => e.id === Math.abs(eventID));
      if (event === undefined) return '0';
      return `${eventID}_${event.title.replace(/<.*?>/g, '')}`;
    },
  },
};
