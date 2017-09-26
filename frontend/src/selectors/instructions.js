export function getScheduledInstructions(state) {
  const scheduledIds = state.instructions.scheduled;
  const instructions = scheduledIds.map(id => state.instructions.byId[id]);
  return instructions;
}
