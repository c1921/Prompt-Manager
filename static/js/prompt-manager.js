let sortable = null;
const translations = new Map(); // 存储翻译
let currentEditingBlock = null; // 跟踪当前正在编辑的块
let lastTranslationTime = 0;  // 记录上次翻译时间
const MIN_INTERVAL = 1000;    // 最小间隔（毫秒）

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

async function getTranslation(text, toEnglish = false) {
    try {
        // 检查时间间隔
        const currentTime = Date.now();
        const timeElapsed = currentTime - lastTranslationTime;
        
        if (timeElapsed < MIN_INTERVAL) {
            throw new Error(`请求过于频繁，请等待 ${((MIN_INTERVAL - timeElapsed) / 1000).toFixed(1)} 秒`);
        }
        
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                to_english: toEnglish
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || '翻译请求失败');
        }
        
        lastTranslationTime = Date.now();  // 更新最后翻译时间
        return data.translation;
    } catch (error) {
        // 显示错误消息给用户
        showTranslationError(error.message);
        console.error('翻译错误:', error);
        return null;
    }
}

function createTranslationInput(blockElement, text) {
    const translationDiv = document.createElement('div');
    translationDiv.className = 'edit-translation';

    const input = document.createElement('input');
    input.type = 'text';
    input.value = translations.get(text) || '';
    input.placeholder = '输入翻译，按Enter保存，Delete清除，T自动翻译...';

    // 处理各种事件
    input.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            saveTranslation(blockElement, text, input.value);
            blockElement.classList.remove('editing');
            currentEditingBlock = null;
        } else if (e.key === 'Escape') {
            blockElement.classList.remove('editing');
            currentEditingBlock = null;
        } else if (e.key === 'Delete' && input.selectionStart === 0 && input.selectionEnd === input.value.length) {
            e.preventDefault();
            translations.delete(text);
            updateTranslationDisplay(blockElement, text);
            blockElement.classList.remove('editing');
            currentEditingBlock = null;
        } else if (e.key.toLowerCase() === 't' && !input.value.trim()) {
            // 按T键自动翻译
            e.preventDefault();
            const translation = await getTranslation(text);
            if (translation) {
                input.value = translation;
                saveTranslation(blockElement, text, translation);
            }
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

async function splitIntoBlocks(text) {
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

        // 添加翻译显示（如果已有翻译）
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

// 修改 textarea 的 oninput 事件
document.querySelector('.prompt-input').addEventListener('input', function() {
    splitIntoBlocks(this.value);
});

// 修改初始化代码
window.onload = function() {
    const textarea = document.querySelector('.prompt-input');
    if (textarea.value) {
        splitIntoBlocks(textarea.value);
    }
};

async function translateAllPrompts() {
    const blocks = Array.from(document.querySelectorAll('.prompt-block'))
        .map(block => block.querySelector('.prompt-text').textContent.trim());
    
    if (blocks.length === 0) return;

    try {
        // 将所有提示词合并为一个字符串，使用特殊分隔符
        const combinedText = blocks.join(' | ');  // 使用 | 作为分隔符
        
        // 获取整体翻译
        const translation = await getTranslation(combinedText);
        
        if (translation) {
            // 使用相同的分隔符分割翻译结果
            const translatedBlocks = translation.split('|').map(t => t.trim());
            
            // 确保翻译结果和原文数量匹配
            if (translatedBlocks.length === blocks.length) {
                // 更新每个块的翻译
                blocks.forEach((block, index) => {
                    translations.set(block, translatedBlocks[index]);
                });
                
                // 更新显示
                document.querySelectorAll('.prompt-block').forEach((blockElement, index) => {
                    updateTranslationDisplay(blockElement, blocks[index]);
                });
            } else {
                // 如果数量不匹配，改为逐个翻译
                console.log('切换到逐个翻译模式');
                for (let i = 0; i < blocks.length; i++) {
                    const translation = await getTranslation(blocks[i]);
                    if (translation) {
                        translations.set(blocks[i], translation);
                        const blockElement = document.querySelectorAll('.prompt-block')[i];
                        updateTranslationDisplay(blockElement, blocks[i]);
                    }
                }
            }
        }
    } catch (error) {
        console.error('整体翻译失败:', error);
    }
}

// 添加错误提示函数
function showTranslationError(message) {
    // 创建或获取错误提示元素
    let errorDiv = document.getElementById('translation-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'translation-error';
        document.querySelector('.prompt-form').appendChild(errorDiv);
    }
    
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // 3秒后自动隐藏
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 3000);
}