import injectTapEventPlugin from 'react-tap-event-plugin';
// include global css styles
import 'normalize.css';
import './styles.css';

import theme from './theme';

export { theme };

export function initGlobalTheme() {
  // Needed for material-ui onTouchTap
  // http://stackoverflow.com/a/34015469/988941
  try {
    injectTapEventPlugin();
  } catch (e) {
    // Supress error in case the TapEventPlugin was already injected
  }
  setGlobalFonts();
}


function setGlobalFonts() {
  global.WebFontConfig = {
    google: { families: ['Roboto:400,300,500:latin'] },
  };
  const webFontScriptElement = document.createElement('script');
  webFontScriptElement.src = 'https://ajax.googleapis.com/ajax/libs/webfont/1/webfont.js';
  webFontScriptElement.type = 'text/javascript';
  webFontScriptElement.async = 'true';
  const s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(webFontScriptElement, s);
}
