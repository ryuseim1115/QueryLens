import '../components/input/FileDialog/UploadFile.js';
import { handleOpenFileDialogClick } from '../components/input/FileDialog/OpenFileDialog.js';
import { handleAnalysisClick } from '../components/input/Analysis.js';
import { updateLineNumbers, syncScroll } from '../components/input/QueryLineNumbers.js';

const openFileListBtn = document.querySelector('.open-file-btn');
const analysisBtn = document.querySelector('.analysis-btn');
const queryTextarea = document.querySelector('textarea[name="query"]');

openFileListBtn.addEventListener('click', handleOpenFileDialogClick);
analysisBtn.addEventListener('click', handleAnalysisClick);
queryTextarea.addEventListener('input', updateLineNumbers);
queryTextarea.addEventListener('scroll', syncScroll);

// 戻る/進むナビゲーションでtextareaの値だけがinputイベントなしに復元されることがあるため、
// 読み込み時点の実際の値に合わせてガターを初期化する
updateLineNumbers();
