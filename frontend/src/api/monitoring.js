/**
 * Defines the interface between the monitoring BE app and the frontend.
 */
import axios from 'axios';

const API_PATH = '/monitoring/api';


export function fetchMetrics() {
  const path = `${API_PATH}/metrics/`;
  return axios.get(path).then(response => response.data.map(data => ({
    name: data['name'],
    group: data['group'],
    time: data['time'],
    value: data['value'],
  })));
}
