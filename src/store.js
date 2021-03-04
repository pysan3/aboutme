import { createStore } from 'vuex';
import axios from '@/axios';
import bibtexParse from 'bibtex-parse';

const state = {
  events: [],
  topicGroup: [],
  bibtex: {},
  gitData: {},
};

String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

const gettersDefault = Object.fromEntries(Object.keys(state).map((key) => (
  [`get${key.capitalize()}`, (state) => state[key]]
)));
const getters = Object.assign(gettersDefault, {

});

const mutationsDefault = Object.fromEntries(Object.keys(state).map((key) => (
  [`set${key.capitalize()}`, (state, value) => { state[key] = value; }]
)));
const mutations = Object.assign(mutationsDefault, {

});

const actions = {
  async fetchAllEvents({ commit }) {
    await axios.get('events/events.json').then(async (response) => {
      commit('setEvents', response.data.events);
      commit('setTopicGroup', response.data.topic_group);
      // bibtex
      commit('setBibtex', bibtexParse.parse(await Promise.all(
        response.data.biblist.map(
          (bibpath) => axios.get(bibpath).then((e) => e.data),
        ),
      ).then((e) => e.join('\n'))));
    });
  },
  async fetchGitData({ getters, commit }, gitName) {
    if (Object.keys(getters.getGitData).length === 0) {
      await axios.get(`https://freeroomfinder.herokuapp.com/api/gitcalendar/${gitName}`).then((response) => {
        commit('setGitData', response.data);
      });
    }
  },
};

export default createStore({
  state,
  getters,
  mutations,
  actions,
});
