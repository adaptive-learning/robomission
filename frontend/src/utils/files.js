export function downloadTextFile(name, content) {
  const element = document.createElement('a');
  element.setAttribute('href', `data:text/plain;charset=utf-8,${encodeURIComponent(content)}`);
  element.setAttribute('download', name);
  element.style.display = 'none';
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}


export function loadTextFile() {
  const contentPromise = new Promise(resolve => {
    const element = document.createElement('input');
    element.setAttribute('type', 'file');
    element.style.display = 'none';
    const handleFileSelect = evt => {
      const file = evt.target.files[0];
      const reader = new FileReader();
      reader.onload = innerEvt => {
        const content = innerEvt.target.result;
        resolve(content);
      };
      reader.readAsText(file);
      document.body.removeChild(element);
    };
    element.addEventListener('change', handleFileSelect, false);
    document.body.appendChild(element);
    element.click();
  });
  return contentPromise;
}
