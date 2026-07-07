import { createTable } from '../../../api/CreateTable.js';
import { getCsvFiles } from '../../../api/GetCsvFiles.js';
import { openDialog } from './DialogControl.js';
import { addDeleteListener } from './DeleteCsv.js';

const openCsvFileListBtn = document.querySelector('.open-csv-btn');
const csvFileList = document.querySelector('.csv-file-list');

openCsvFileListBtn.addEventListener('click', async () => {
  await reloadCsvFileList();
  openDialog();
});

export async function reloadCsvFileList() {
  const csvData = await getCsvFiles();
  await Promise.all(csvData.untabled_files.map((fileName) => createTable(fileName)));
  renderCsvFileList(csvData.csv_files);
}

function renderCsvFileList(fileNames) {
  csvFileList.innerHTML = '';
  fileNames.forEach((fileName) => {
    const csvFileDiv = document.createElement('div');
    csvFileDiv.classList.add('csv-file-row');

    const nameSpan = document.createElement('span');
    nameSpan.textContent = fileName;

    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.classList.add('delete-csv-btn');
    deleteBtn.textContent = '削除';
    addDeleteListener(deleteBtn, fileName);

    csvFileDiv.appendChild(nameSpan);
    csvFileDiv.appendChild(deleteBtn);
    csvFileList.appendChild(csvFileDiv);
  });
}
