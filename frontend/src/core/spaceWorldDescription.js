/**
 * Bidirection parsing/generating of SpaceWorld description
 */

export const fieldBackgrounds = {
  black: 'k',
  red: 'r',
  green: 'g',
  blue: 'b',
  yellow: 'y',
  cyan: 'c',
  magenta: 'm',
};


export const gameObjects = {
  spaceship: 'S',
  asteroid: 'A',
  meteoroid: 'M',
  diamond: 'D',
  wormhole: 'W',
  wormhole2: 'X',
  wormhole3: 'Y',
  wormhole4: 'Z',
};


const fieldBackgroundsSet = new Set(Object.values(fieldBackgrounds));
const gameObjectsSet = new Set(Object.values(gameObjects));

//// TODO: Remove if not needed.
//export function generateSpaceWorldText(fields) {
//  const text = fields.map(row => `|${row.map(fieldToText).join('|')}|`).join('\n');
//  return text;
//}
//
//function fieldToText(field) {
//  const [background, objects] = field;
//  const objectsText = (objects.length > 0) ? objects.join('') : ' ';
//  const fieldText = background + objectsText;
//  return fieldText;
//}


export function parseSpaceWorld(text) {
  text = text.replace(' ', '').trimRight().replace(';', '\n');
  const lines = text.split('\n');
  let fields = [];
  let errors = [];
  for (let [iLine, line] of lines.entries()) {
    let rowFields = [];
    for (let fieldText of line.trim().split('|').filter(f => f !== '')) {
      let { field, error } = parseField(fieldText, iLine);
      rowFields.push(field);
      if (error != null) {
        errors.push(error);
      }
    }
    fields.push(rowFields);
  }
  alignRows(fields);
  // const fields = lines.map(line => line.trim().split('|').filter(f => f !== '').map(parseField));
  return { fields, errors };
}


function parseField(fieldText, row) {
  let error = null;
  const trimmedFieldText = fieldText.trim();
  let background = 'k';
  let objects = [];
  if (trimmedFieldText.length === 0) {
    error = editorError(`Invalid field: ${fieldText}`, row);
  } else {
    [background, ...objects] = trimmedFieldText;
    if (!fieldBackgroundsSet.has(background)) {
      error = editorError(`Invalid background: ${background}`, row);
      background = 'k';
    }
    objects.forEach(object => {
      if (!gameObjectsSet.has(object)) {
        error = editorError(`Invalid object: ${object}`, row);
        objects = [];
      }
    });
  }
  const field = [background, objects];
  return { field, error };
}


function editorError(message, row=0, col=0) {
  return {
    name: 'EditorSyntaxError',
    message: message,
    row: row,
    col: col,
  };
}


function alignRows(fields) {
  const cols = Math.max(...fields.map(row => row.length));
  for (let row of fields) {
    row.push(...Array(cols - row.length).fill(['k', []]));
  }
}
