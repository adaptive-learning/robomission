/* Convert task source from markdown to json
 *
 * Reads:
 * task source from stdin
 *
 * Writes:
 * parsed task in json to stdout
 *
 * Usage:
 * cat three-steps-forward.md | npm run parse-task
 */
import { parseTaskSourceText } from '../src/core/taskSourceParser';

process.stdin.on('data', buffer => {
  const text = buffer.toString();
  const task = parseTaskSourceText(text);
  console.log(JSON.stringify(task));
});
