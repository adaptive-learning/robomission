export function flatten(arrayOfArrays) {
  return [].concat.apply([], arrayOfArrays);
}
