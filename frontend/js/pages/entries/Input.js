import '../components/input/FileDialog/UploadFile.js';
import '../components/input/QueryLineNumbers.js';
import { handleOpenFileDialogClick } from '../components/input/FileDialog/OpenFileDialog.js';
import { handleAnalysisClick } from '../components/input/Analysis.js';

const openFileListBtn = document.querySelector('.open-file-btn');
const analysisBtn = document.querySelector('.analysis-btn');

openFileListBtn.addEventListener('click', handleOpenFileDialogClick);
analysisBtn.addEventListener('click', handleAnalysisClick);
