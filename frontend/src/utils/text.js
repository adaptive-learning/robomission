/**
 * String template tag removing leading indentation
 * Multiple empty lines will be shrunk to a single empty line.
 */
export function stripIndentation(strings, ...values) {
  const trimmedStrings = strings.map(string =>
    string.split('\n').map(line => line.trimLeft()).join('\n'));
  const interpolatedText = trimmedStrings.reduce((acc, string, i) => acc + values[i - 1] + string);
  const textWithoutExtraEmptyLines = interpolatedText.replace(/\n(\s*\n){2,}/g, '\n\n');
  return textWithoutExtraEmptyLines;
}


export function toTitle(id) {
  const words = id.replace(/[-_]/g, ' ');
  const title = words.replace(/\w+/g, word => word.charAt(0).toUpperCase() + word.slice(1));
  return title;
}
