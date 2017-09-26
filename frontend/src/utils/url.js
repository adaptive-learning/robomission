export function getDomainLabels() {
  const hostname = getHostName();
  const allLabels = hostname.split('.');
  const [firstLabel, ...otherLabels] = allLabels;
  const labelsWithoutWWW = (firstLabel === 'www') ? otherLabels : allLabels;
  return labelsWithoutWWW;
}

function getHostName() {
  return window.location.hostname;
}
