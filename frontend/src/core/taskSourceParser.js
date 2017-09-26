import pegTaskSourceParser from './pegTaskSourceParser';
import { parseRoboCode } from './roboCodeParser';
import { parseSpaceWorld } from './spaceWorldDescription';

/**
 * Parse task source text (markdown) and returned js object representing the
 * task
 */
export function parseTaskSourceText(sourceText) {
  const chunkedTaskSource = pegTaskSourceParser.parse(sourceText);
  const task = {
    id: chunkedTaskSource.taskId,
    category: chunkedTaskSource.category || 'uncategorized',
    setting: {
      ...chunkedTaskSource.setting,
      fields: parseSpaceWorld(chunkedTaskSource.setting.fields),
    },
    solution: parseRoboCode(chunkedTaskSource.solution),
  };
  return task;
}
