// include global css styles
import 'normalize.css';
import './styles.css';

import theme from './theme';

export { theme };

export function initGlobalTheme() {
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
