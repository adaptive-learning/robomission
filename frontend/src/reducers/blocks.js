import { FETCH_STATIC_DATA_FULFILLED } from '../action-types';

export default function reduceBlocks(state = {}, action) {
  switch (action.type) {
    case FETCH_STATIC_DATA_FULFILLED: {
      const blockList = action.payload.blocks.map(parseBlock);
      const blocks = {};
      for (const block of blockList) {
        blocks[block.id] = block;
      }
      return blocks;
    }
  }
  return state;
}

function parseBlock(data) {
  const block = {
    id: data['block_id'],
  };
  return block;
}
