import ReactGA from 'react-ga';
import axiosDefaults from 'axios/lib/defaults';
import { initGlobalBlockly } from './core/blockly';
import { initGlobalTheme } from './theme';


export const API_PATH = '/learn/api';


export function globalConfiguration() {
  initGoogleAnalytics();
  initGlobalAxios();
  initGlobalTheme();
  initGlobalBlockly();
}


function initGoogleAnalytics() {
  const trackingId = 'UA-81667720-1';
  ReactGA.initialize(trackingId, { debug: false, titleCase: false });
}


function initGlobalAxios() {
  axiosDefaults.xsrfCookieName = 'csrftoken';
  axiosDefaults.xsrfHeaderName = 'X-CSRFToken';
}
