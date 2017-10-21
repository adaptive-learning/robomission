export const completeToolbox = [
  // TODO: rewrite as a selector on state.toolboxes
  {
    type: 'fly',
    fields: { direction: 'ahead' },
  },
  {
    type: 'fly',
    fields: { direction: 'left' },
  },
  {
    type: 'fly',
    fields: { direction: 'right' },
  },
  { type: 'shoot' },
  { type: 'repeat' },
  { type: 'while' },
  { type: 'color' },
  { type: 'position' },
  { type: 'if' },
  { type: 'if-else' },
];


export function expandBlocks(toolbox) {
  const expandedBlockLists = toolbox.map(block => expandBlock(block));
  const expandedBlocks = [].concat.apply([], expandedBlockLists);
  return expandedBlocks;
}


function expandBlock(block) {
  switch (block) {
    case 'fly': {
      return [
        {
          type: 'fly',
          fields: { direction: 'ahead' },
        },
        {
          type: 'fly',
          fields: { direction: 'left' },
        },
        {
          type: 'fly',
          fields: { direction: 'right' },
        },
      ];
    }
    default: {
      return { type: block };
    }
  }
}
