export function getToolboxId(state, chunkId) {
  return state.chunks[chunkId].setting.toolbox;
}


export function getChunkLevel(state, chunkId) {
  // TODO: Unify terminology order vs. level.
  return state.chunks[chunkId].order;
}
