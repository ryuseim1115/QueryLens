import { handleOpenFileDialogClick } from '../components/input/FileDialog/OpenFileDialog.js';
import { closeDialog } from '../components/input/FileDialog/DialogControl.js';
import {
  handleSelectFileClick,
  handleFileInputChange,
  handleUploadClick,
} from '../components/input/FileDialog/UploadFile.js';
import { handleAnalysisClick } from '../components/input/MainScreen/Analysis.js';
import {
  updateLineNumbers,
  syncScroll,
} from '../components/input/MainScreen/QueryLineNumbers.js';

// メイン画面の要素
const openFileListBtn = document.querySelector('.open-file-btn');
const analysisBtn = document.querySelector('.analysis-btn');
const queryTextarea = document.querySelector('textarea[name="query"]');

// ファイルダイアログの要素
const closeFileListBtn = document.querySelector('.close-btn');
const selectFileBtn = document.querySelector('.select-file-btn');
const nativeFileInput = document.querySelector('.upload-file-input');
const uploadBtn = document.querySelector('.upload-file-btn');

// メイン画面のイベント
openFileListBtn.addEventListener('click', handleOpenFileDialogClick);
analysisBtn.addEventListener('click', handleAnalysisClick);
queryTextarea.addEventListener('input', updateLineNumbers);
queryTextarea.addEventListener('scroll', syncScroll);

// 戻る/進むナビゲーションでtextareaの値だけがinputイベントなしに復元されることがあるため、
// 読み込み時点の実際の値に合わせてガターを初期化する
updateLineNumbers();

// ファイルダイアログのイベント
closeFileListBtn.addEventListener('click', closeDialog);
selectFileBtn.addEventListener('click', handleSelectFileClick);
nativeFileInput.addEventListener('change', handleFileInputChange);
uploadBtn.addEventListener('click', handleUploadClick);
