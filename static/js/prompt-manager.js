let sortable = null;
const translations = new Map(); // 存储翻译
let currentEditingBlock = null; // 跟踪当前正在编辑的块

function initSortable() {
    if (sortable) {
        sortable.destroy();
    }
    sortable = new Sortable(blockContainer, {
        animation: 150,
        ghostClass: 'sortable-ghost',
        chosenClass: 'sortable-chosen',
        dragClass: 'sortable-drag',
        filter: '.edit-translation', // 防止拖动输入框
        onEnd: function () {
            updatePromptInput();
        }
    });
}

function createTranslationInput(blockElement, text) {
    const translationDiv = document.createElement('div');
    translationDiv.className = 'edit-translation';

    const input = document.createElement('input');
    input.type = 'text';
    input.value = translations.get(text) || '';
    input.placeholder = '输入翻译，按Enter保存，Delete清除...';

    // 处理各种事件
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            saveTranslation(blockElement, text, input.value);
            blockElement.classList.remove('editing');
            currentEditingBlock = null;
        } else if (e.key === 'Escape') {
            blockElement.classList.remove('editing');
            currentEditingBlock = null;
        } else if (e.key === 'Delete' && input.selectionStart === 0 && input.selectionEnd === input.value.length) {
            // 当全选内容并按Delete时，删除翻译
            e.preventDefault();
            translations.delete(text);
            updateTranslationDisplay(blockElement, text);
            blockElement.classList.remove('editing');
            currentEditingBlock = null;
        }
    });

    input.addEventListener('blur', () => {
        // 给一个小延时，避免点击其他块时立即关闭
        setTimeout(() => {
            if (input.value.trim()) {
                saveTranslation(blockElement, text, input.value);
            } else {
                // 如果输入框为空，删除翻译
                translations.delete(text);
                updateTranslationDisplay(blockElement, text);
            }
            blockElement.classList.remove('editing');
            currentEditingBlock = null;
        }, 100);
    });

    translationDiv.appendChild(input);
    return translationDiv;
}

function saveTranslation(blockElement, text, translation) {
    if (translation.trim()) {
        translations.set(text, translation.trim());
    } else {
        translations.delete(text);
    }
    updateTranslationDisplay(blockElement, text);
}

function updateTranslationDisplay(blockElement, text) {
    let translationSpan = blockElement.querySelector('.translation');
    if (!translationSpan) {
        translationSpan = document.createElement('div');
        translationSpan.className = 'translation';
        blockElement.appendChild(translationSpan);
    }
    const translation = translations.get(text);
    if (translation) {
        translationSpan.textContent = translation;
        translationSpan.style.display = 'block';
    } else {
        translationSpan.textContent = '';
        translationSpan.style.display = 'none';
    }
}

function splitIntoBlocks(text) {
    const container = document.getElementById('blockContainer');
    container.innerHTML = '';

    if (!text.trim()) return;

    const blocks = text.split(',')
        .map(block => block.trim())
        .filter(block => block);

    blocks.forEach(block => {
        const blockElement = document.createElement('div');
        blockElement.className = 'prompt-block';

        const textSpan = document.createElement('div');
        textSpan.className = 'prompt-text';
        textSpan.textContent = block;
        blockElement.appendChild(textSpan);

        // 添加翻译显示
        if (translations.has(block)) {
            updateTranslationDisplay(blockElement, block);
        }

        // 双击编辑翻译
        blockElement.addEventListener('dblclick', (e) => {
            if (e.target.classList.contains('edit-translation')) return;

            // 如果有其他正在编辑的块，先关闭它
            if (currentEditingBlock && currentEditingBlock !== blockElement) {
                currentEditingBlock.classList.remove('editing');
            }

            currentEditingBlock = blockElement;
            blockElement.classList.add('editing');

            // 移除已存在的输入框（如果有）
            const existingInput = blockElement.querySelector('.edit-translation');
            if (existingInput) {
                existingInput.remove();
            }

            const translationInput = createTranslationInput(blockElement, block);
            blockElement.appendChild(translationInput);
            translationInput.querySelector('input').focus();
        });

        container.appendChild(blockElement);
    });

    initSortable();
}

function updatePromptInput() {
    const blocks = Array.from(document.querySelectorAll('.prompt-block'));
    const text = blocks.map(block => {
        const textContent = block.firstChild.textContent;
        return textContent.trim();
    }).join(', ');
    document.querySelector('.prompt-input').value = text;
}

// 初始化时分割现有文本
window.onload = function () {
    const textarea = document.querySelector('.prompt-input');
    if (textarea.value) {
        splitIntoBlocks(textarea.value);
    }
};