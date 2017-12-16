import axiosDefaults from 'axios/lib/defaults';
import { initGlobalBlockly } from './core/blockly';
import { initGlobalTheme } from './theme';
import { getLocale } from './localization';


export const API_PATH = '/learn/api';


export function globalConfiguration() {
  initGlobalAxios();
  initGlobalTheme();
  initGlobalBlockly();
}


function initGlobalAxios() {
  axiosDefaults.xsrfCookieName = 'csrftoken';
  axiosDefaults.xsrfHeaderName = 'X-CSRFToken';
  axiosDefaults.headers.common['Accept-Language'] = getLocale();
}
