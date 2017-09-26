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


export function generateSpaceWorldText(fields) {
  const text = fields.map(row => `|${row.map(fieldToText).join('|')}|`).join('\n');
  return text;
}


export function parseSpaceWorld(text) {
  const lines = text.trim().split('\n');
  const fields = lines.map(line => line.trim().split('|').filter(f => f !== '').map(parseField));
  return fields;
}


function fieldToText(field) {
  const [background, objects] = field;
  const objectsText = (objects.length > 0) ? objects.join('') : ' ';
  const fieldText = background + objectsText;
  return fieldText;
}


function parseField(fieldText) {
  const trimmedFieldText = fieldText.trim();
  if (trimmedFieldText.length === 0) {
    throw new Error(`Invalid field: ${fieldText}`);
  }
  const [background, ...objects] = trimmedFieldText;
  if (!fieldBackgroundsSet.has(background)) {
    throw new Error(`Invalid background: ${background}`);
  }
  objects.forEach(object => {
    if (!gameObjectsSet.has(object)) {
      throw new Error(`Invalid object: ${object}`);
    }
  });
  const field = [background, objects];
  return field;
}
