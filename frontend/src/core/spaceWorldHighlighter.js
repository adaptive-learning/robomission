/* Custom syntax highlighter for SpaceWorld setting for brace
 * (which is used by react-ace editor).
 * Expects global ace variable to be present.

 * Usage:
 *   ```
 *   import AceEditor from 'react-ace';
 *   import '../core/spaceWorldHighlighter';
 *   ...
 *   <AceEditor mode="spaceworld" />
 *   ```
 */

/* global ace:false */
/* eslint-disable no-param-reassign */

ace.define('ace/mode/spaceworld_highlight_rules',
  ['require', 'exports', 'ace/lib/oop', 'ace/mode/text_highlight_rules'],
  (acequire, exports) => {
    const oop = acequire('../lib/oop');
    const TextHighlightRules = acequire('./text_highlight_rules').TextHighlightRules;
    const colorTokens = {
      black: 'text',
      gray: 'comment',
      red: 'constant.character',
      green: 'keyword',
      blue: 'variable',
      cyan: 'string',
      magenta: 'constant.numeric',
      yellow: 'constant.language.boolean',
    };
    function SpaceWorldHighlightRules() {
      this.$rules = {
        start: [
          {
            token: colorTokens.black,
            regex: 'k',
          }, {
            token: colorTokens.red,
            regex: 'r',
          }, {
            token: colorTokens.green,
            regex: 'g',
          }, {
            token: colorTokens.blue,
            regex: 'b',
          }, {
            token: colorTokens.cyan,
            regex: 'c',
          }, {
            token: colorTokens.magenta,
            regex: 'm',
          }, {
            token: colorTokens.yellow,
            regex: 'y',
          }, {
            token: colorTokens.black,
            regex: '(S|D|A|M|W|X|Y|Z)',
          }, {
          }, {
            token: colorTokens.gray,
            regex: '\\|',
          }, {
            token: colorTokens.gray,
            regex: '.',
          },
        ],
      };
    }
    oop.inherits(SpaceWorldHighlightRules, TextHighlightRules);
    exports.SpaceWorldHighlightRules = SpaceWorldHighlightRules;
  }
);

ace.define('ace/mode/spaceworld',
  ['require', 'exports', 'ace/lib/oop', 'ace/mode/text', 'ace/mode/spaceworld_highlight_rules'],
  (acequire, exports) => {
    const oop = acequire('../lib/oop');
    const TextMode = acequire('./text').Mode;
    const HighlightRules = acequire('./spaceworld_highlight_rules').SpaceWorldHighlightRules;
    function Mode() {
      this.HighlightRules = HighlightRules;
      this.$behaviour = this.$defaultBehaviour;
    }
    oop.inherits(Mode, TextMode);
    (function setId() {
      this.$id = 'ace/mode/spaceworld';
    }).call(Mode.prototype);
    exports.Mode = Mode;
  }
);
