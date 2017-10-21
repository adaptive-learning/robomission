import axios from 'axios';
import { API_PATH } from './config';


export function fetchWorld() {
  const entityNames = ['blocks', 'toolboxes', 'tasks', 'levels', 'instructions'];
  const urls = entityNames.map(name => `${API_PATH}/${name}`);
  const requests = urls.map(url => axios.get(url));
  return axios.all(requests).then(results => {
    const namedResults = {};
    for (const [i, name] of entityNames.entries()) {
      namedResults[name] = results[i].data;
    }
    return namedResults;
  });
}
