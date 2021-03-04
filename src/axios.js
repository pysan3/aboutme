import axios from 'axios';

const axiosConfig = {
  baseURL: process.env.VUE_APP_PUBLICPATH,
  timeout: 300000,
};

export default axios.create(axiosConfig);
