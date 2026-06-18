import { getCsvFiles } from '../../../api/GetCsvFiles.js';
import { openDialog } from './DialogControl.js';
import { addAnalysisTargetListener } from './AddAnalysisTarget.js';

const openCsvFileListBtn = document.querySelector('.open-csv-btn');
const csvFileList = document.querySelector('.csv-file-list');

openCsvFileListBtn.addEventListener('click', async () => {
  const csvData = await getCsvFiles();
  renderCsvFileList(csvData.csv_files);
  openDialog();
});

function renderCsvFileList(fileNames) {
  csvFileList.innerHTML = '';
  fileNames.forEach((fileName) => {
    const csvFileDiv = document.createElement('div');

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    addAnalysisTargetListener(checkbox, fileName);

    const label = document.createElement('label');
    label.textContent = fileName;
    label.prepend(checkbox);

    csvFileDiv.appendChild(label);
    csvFileList.appendChild(csvFileDiv);
  });
}
