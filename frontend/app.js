/**
 * app.js - Frontend JavaScript cho HSG Python
 * SPA logic: routing, API calls, code editor, test results, roadmap
 */

// ============================================================================
// CONSTANTS & STATE
// ============================================================================

const API_BASE = '';  // Same origin
let editor = null;    // CodeMirror instance
let currentStageId = null;
let currentProblemId = null;
let stagesData = [];
let progressData = {};
let currentView = 'learn';  // 'learn' or 'roadmap'
let stagesDetailCache = {};

// Auth State
let authToken = localStorage.getItem('auth_token');
let currentUser = null;

// ============================================================================
// INIT
// ============================================================================

let codeAutoSaveTimer = null;
const STORAGE_PREFIX_CODE = 'hsg_code_';

document.addEventListener('DOMContentLoaded', async () => {
    initEditor();
    initEventListeners();
    initEditorPanel();
    initSettings();
    await initAuth();
    await loadStages();
    await loadProgress();
    renderSidebar();

    // Khôi phục bài tập và đoạn code học sinh đang làm dở nếu có
    const lastStageId = localStorage.getItem('hsg_last_stage_id');
    const lastProblemId = localStorage.getItem('hsg_last_problem_id');
    if (lastStageId && lastProblemId) {
        await selectProblem(parseInt(lastStageId), lastProblemId);
    }
});

// ============================================================================
// CODE EDITOR (CodeMirror 5)
// ============================================================================

function initEditor() {
    const textarea = document.getElementById('code-editor');
    editor = CodeMirror.fromTextArea(textarea, {
        mode: 'python',
        theme: 'dracula',
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        matchBrackets: true,
        autoCloseBrackets: true,
        lineWrapping: false,
        extraKeys: {
            'Tab': (cm) => cm.replaceSelection('    ', 'end'),
            'Ctrl-Enter': () => runCode(),
            'Ctrl-Shift-Enter': () => submitCode(),
        },
    });

    editor.setValue('# Viết code Python ở đây\nimport sys\ninput = sys.stdin.readline\n\n');

    // Tự động lưu code đang viết dở của từng bài vào localStorage (chống mất dữ liệu khi Cloud sleep/restart)
    editor.on('change', () => {
        if (currentProblemId) {
            clearTimeout(codeAutoSaveTimer);
            codeAutoSaveTimer = setTimeout(() => {
                const code = editor.getValue();
                saveProblemCodeToStorage(currentProblemId, code);
            }, 300);
        }
    });
}

function getStoredProblemCode(problemId) {
    if (!problemId) return null;
    try {
        return localStorage.getItem(`${STORAGE_PREFIX_CODE}${problemId}`);
    } catch (e) {
        return null;
    }
}

function saveProblemCodeToStorage(problemId, code) {
    if (!problemId || code === undefined || code === null) return;
    try {
        localStorage.setItem(`${STORAGE_PREFIX_CODE}${problemId}`, code);
    } catch (e) {
        console.warn('Lỗi lưu code vào localStorage:', e);
    }
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

function initEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });

    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Run, Debug & Submit
    document.getElementById('run-code').addEventListener('click', runCode);
    document.getElementById('debug-code')?.addEventListener('click', startDebug);
    document.getElementById('submit-code').addEventListener('click', submitCode);

    // Start button
    document.getElementById('start-learning').addEventListener('click', () => {
        if (stagesData.length > 0) {
            selectStage(1);
        }
    });

    // Input toggle
    document.querySelector('.input-header')?.addEventListener('click', toggleInput);
}

function toggleInput() {
    const input = document.getElementById('custom-input');
    const btn = document.getElementById('toggle-input');
    if (input.style.display === 'none') {
        input.style.display = 'block';
        if (btn) btn.textContent = '▲';
    } else {
        input.style.display = 'none';
        if (btn) btn.textContent = '▼';
    }
}

// ============================================================================
// API CALLS
// ============================================================================

async function apiGet(path) {
    const headers = {};
    if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
    const res = await fetch(`${API_BASE}${path}`, { headers });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || `API Error: ${res.status}`);
    return data;
}

async function apiPost(path, data) {
    const headers = { 'Content-Type': 'application/json' };
    if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
    const res = await fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
    });
    const resData = await res.json();
    if (!res.ok) throw new Error(resData.detail || `API Error: ${res.status}`);
    return resData;
}

async function apiPut(path, data) {
    const headers = { 'Content-Type': 'application/json' };
    if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
    const res = await fetch(`${API_BASE}${path}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(data),
    });
    const resData = await res.json();
    if (!res.ok) throw new Error(resData.detail || `API Error: ${res.status}`);
    return resData;
}

// ============================================================================
// DATA LOADING
// ============================================================================

async function loadStages() {
    try {
        const data = await apiGet('/api/stages');
        stagesData = data.stages;
    } catch (e) {
        console.error('Failed to load stages:', e);
    }
}

// ============================================================================
// TIẾN ĐỘ & LOCALSTORAGE SYNC (CHỐNG MẤT TIẾN ĐỘ TRÊN CLOUD MIỄN PHÍ)
// ============================================================================

const STORAGE_KEY_AC_PROBLEMS = 'hsg_ac_problems';

function getStoredACProblems() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY_AC_PROBLEMS);
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        console.warn('Lỗi đọc localStorage:', e);
        return [];
    }
}

function saveACProblemToStorage(problemId) {
    if (!problemId) return;
    try {
        const list = getStoredACProblems();
        if (!list.includes(problemId)) {
            list.push(problemId);
            localStorage.setItem(STORAGE_KEY_AC_PROBLEMS, JSON.stringify(list));
        }
    } catch (e) {
        console.warn('Lỗi ghi localStorage:', e);
    }
}

function syncProgressWithLocalStorage() {
    const storedACList = getStoredACProblems();

    // 1. Phục hồi các bài đã AC từ localStorage vào progressData (đề phòng server bị reset)
    storedACList.forEach(pid => {
        if (!progressData[pid]) {
            progressData[pid] = {
                problem_id: pid,
                completed: 1,
                best_score: 10,
                total_tests: 10,
                attempts: 1,
            };
        } else {
            progressData[pid].completed = 1;
            if ((progressData[pid].best_score || 0) < 10) {
                progressData[pid].best_score = 10;
            }
        }
    });

    // 2. Đồng bộ 2 chiều: nếu SQLite server có bài nào AC mà localStorage chưa có thì lưu thêm vào
    let hasNewAC = false;
    const acSet = new Set(storedACList);
    Object.keys(progressData).forEach(pid => {
        if (progressData[pid]?.completed && !acSet.has(pid)) {
            acSet.add(pid);
            hasNewAC = true;
        }
    });

    if (hasNewAC) {
        try {
            localStorage.setItem(STORAGE_KEY_AC_PROBLEMS, JSON.stringify(Array.from(acSet)));
        } catch (e) {
            console.warn('Lỗi cập nhật localStorage:', e);
        }
    }
}

async function loadProgress() {
    try {
        const data = await apiGet('/api/progress');
        progressData = data.progress || {};
    } catch (e) {
        console.error('Failed to load progress from server:', e);
        progressData = {};
    }
    // Luôn đồng bộ với localStorage trên trình duyệt học sinh
    syncProgressWithLocalStorage();
}

async function loadStageDetail(stageId) {
    if (stagesDetailCache[stageId]) return stagesDetailCache[stageId];
    try {
        const data = await apiGet(`/api/stages/${stageId}`);
        stagesDetailCache[stageId] = data;
        return data;
    } catch (e) {
        console.error('Failed to load stage detail:', e);
        return null;
    }
}

// ============================================================================
// NAVIGATION
// ============================================================================

function switchView(view) {
    currentView = view;

    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });

    // Toggle views
    const main = document.getElementById('app-main');
    const roadmap = document.getElementById('roadmap-view');
    const thptView = document.getElementById('thpt-view');

    if (view === 'learn') {
        main.style.display = 'flex';
        roadmap.classList.add('hidden');
        if (thptView) thptView.classList.add('hidden');
    } else if (view === 'roadmap') {
        main.style.display = 'none';
        roadmap.classList.remove('hidden');
        if (thptView) thptView.classList.add('hidden');
        renderRoadmap();
    } else if (view === 'thpt') {
        main.style.display = 'none';
        roadmap.classList.add('hidden');
        if (thptView) {
            thptView.classList.remove('hidden');
            loadTHPTContent();
        }
    }
}

async function loadTHPTContent() {
    try {
        const data = await apiGet('/api/thpt');
        const thptHtml = renderMarkdown(data.theory);
        document.getElementById('thpt-content').innerHTML = thptHtml;
        renderMath(document.getElementById('thpt-content'));
    } catch (e) {
        document.getElementById('thpt-content').innerHTML = `<div style="color:red; text-align:center;">Lỗi tải dữ liệu: ${e.message}</div>`;
    }
}

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });

    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('theory-content').classList.add('hidden');
    document.getElementById('problem-content').classList.add('hidden');
    document.getElementById('ai-content').classList.add('hidden');

    if (tab === 'theory' && currentStageId) {
        document.getElementById('theory-content').classList.remove('hidden');
    } else if (tab === 'problem' && currentProblemId) {
        document.getElementById('problem-content').classList.remove('hidden');
    } else if (tab === 'ai-feedback') {
        document.getElementById('ai-content').classList.remove('hidden');
    }
}

// ============================================================================
// SIDEBAR RENDERING
// ============================================================================

function renderSidebar() {
    const container = document.getElementById('sidebar-stages');
    container.innerHTML = '';

    // ---- Helper: tạo folder Level-1 ----
    function makeFolder({ icon, label, defaultOpen = false, content }) {
        const group = document.createElement('div');
        group.className = 'folder-group';

        const header = document.createElement('button');
        header.className = `folder-header${defaultOpen ? ' open' : ''}`;
        header.innerHTML = `
            <span class="folder-icon">${icon}</span>
            <span class="folder-label">${label}</span>
            <span class="folder-arrow">▶</span>
        `;

        const body = document.createElement('div');
        body.className = `folder-content${defaultOpen ? ' open' : ''}`;
        content(body);

        header.addEventListener('click', () => {
            header.classList.toggle('open');
            body.classList.toggle('open');
        });

        group.appendChild(header);
        group.appendChild(body);
        container.appendChild(group);
    }

    // ---- Folder: Ôn HSG (đóng mặc định) ----
    makeFolder({
        icon: '🏆',
        label: 'Ôn HSG',
        defaultOpen: false,
        content(body) {
            stagesData.forEach(stage => {
                const group = document.createElement('div');
                group.className = 'stage-group';

                const completedCount = stage.problems.filter(p =>
                    progressData[p.id]?.completed
                ).length;
                const totalCount = stage.problems.length;

                const header = document.createElement('button');
                header.className = `stage-header ${currentStageId === stage.id ? 'active' : ''}`;
                header.innerHTML = `
                    <span class="stage-icon">${stage.icon}</span>
                    <span class="stage-title">${stage.title}</span>
                    <span class="stage-progress">${completedCount}/${totalCount}</span>
                `;
                header.addEventListener('click', () => selectStage(stage.id));

                const problems = document.createElement('div');
                problems.className = `stage-problems ${currentStageId === stage.id ? 'open' : ''}`;

                const theoryLink = document.createElement('button');
                theoryLink.className = 'problem-link';
                theoryLink.innerHTML = `<span class="problem-status"></span> 📖 Lý thuyết`;
                theoryLink.addEventListener('click', (e) => {
                    e.stopPropagation();
                    selectStage(stage.id);
                    switchTab('theory');
                });
                problems.appendChild(theoryLink);

                stage.problems.forEach(p => {
                    const link = document.createElement('button');
                    const progress = progressData[p.id];
                    const statusClass = progress?.completed ? 'completed' : (progress?.attempts > 0 ? 'attempted' : '');
                    const diffClass = p.difficulty === 'Khởi động' ? 'easy' : (p.difficulty === 'Vận dụng' ? 'medium' : 'hard');

                    link.className = `problem-link ${currentProblemId === p.id ? 'active' : ''}`;
                    link.innerHTML = `
                        <span class="problem-status ${statusClass}"></span>
                        <span>${p.title}</span>
                        <span class="difficulty-badge ${diffClass}">${p.difficulty === 'Khởi động' ? '★' : p.difficulty === 'Vận dụng' ? '★★' : '★★★'}</span>
                    `;
                    link.addEventListener('click', (e) => {
                        e.stopPropagation();
                        selectProblem(stage.id, p.id);
                    });
                    problems.appendChild(link);
                });

                group.appendChild(header);
                group.appendChild(problems);
                body.appendChild(group);
            });
        }
    });

    // ---- Folder 2: Ôn TN THPT QGia ----
    makeFolder({
        icon: '📝',
        label: 'Ôn TN THPT QGia',
        defaultOpen: false,
        content(body) {
            const link = document.createElement('button');
            link.className = `problem-link`;
            link.innerHTML = `<span class="problem-status"></span> 📖 Lý thuyết Trọng tâm`;
            link.addEventListener('click', (e) => {
                e.stopPropagation();
                selectTHPTTheory();
            });
            body.appendChild(link);
        }
    });

    // ---- Folder 3: Luyện Đề (placeholder) ----
    makeFolder({
        icon: '📋',
        label: 'Luyện Đề',
        defaultOpen: false,
        content(body) {
            body.innerHTML = `<div class="folder-placeholder">📂 Chưa có đề — Thêm đề thi tại đây</div>`;
        }
    });

    // ---- Folder 4: BTap GV giao (placeholder) ----
    makeFolder({
        icon: '✏️',
        label: 'BTap GV giao',
        defaultOpen: false,
        content(body) {
            body.innerHTML = `<div class="folder-placeholder">📂 Chưa có bài — GV thêm bài tại đây</div>`;
        }
    });
}


// ============================================================================
// STAGE & PROBLEM SELECTION
// ============================================================================

async function selectTHPTTheory() {
    currentStageId = 'thpt';
    currentProblemId = null;

    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('problem-content').classList.add('hidden');
    document.getElementById('ai-content').classList.add('hidden');
    document.getElementById('theory-content').classList.remove('hidden');

    document.getElementById('theory-content').innerHTML = '<div style="text-align: center; color: #a6adc8;">Đang tải dữ liệu...</div>';
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === 'theory');
    });

    try {
        const data = await apiGet('/api/thpt');
        const thptHtml = renderMarkdown(data.theory);
        document.getElementById('theory-content').innerHTML = thptHtml;
        renderMath(document.getElementById('theory-content'));
    } catch (e) {
        document.getElementById('theory-content').innerHTML = `<div style="color:red; text-align:center;">Lỗi tải dữ liệu: ${e.message}</div>`;
    }
    
    switchView('learn');
    renderSidebar();
}

async function selectStage(stageId) {
    currentStageId = stageId;

    // Load stage detail
    const detail = await loadStageDetail(stageId);
    if (!detail) return;

    // Render theory
    const theoryHtml = renderMarkdown(detail.theory + '\n\n' + detail.weapon);
    document.getElementById('theory-content').innerHTML = theoryHtml;
    renderMath(document.getElementById('theory-content'));

    // Show theory tab
    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('theory-content').classList.remove('hidden');
    document.getElementById('problem-content').classList.add('hidden');
    document.getElementById('ai-content').classList.add('hidden');

    // Activate theory tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === 'theory');
    });

    renderSidebar();
}

async function selectProblem(stageId, problemId) {
    currentStageId = stageId;
    currentProblemId = problemId;

    try {
        localStorage.setItem('hsg_last_stage_id', stageId);
        localStorage.setItem('hsg_last_problem_id', problemId);
    } catch (e) {}

    // Load stage detail if needed
    const detail = await loadStageDetail(stageId);
    if (!detail) return;

    // Also ensure theory is loaded
    const theoryHtml = renderMarkdown(detail.theory + '\n\n' + detail.weapon);
    document.getElementById('theory-content').innerHTML = theoryHtml;
    renderMath(document.getElementById('theory-content'));

    // Find problem
    const problem = detail.problems.find(p => p.id === problemId);
    if (!problem) return;

    // Render problem description
    const problemHtml = renderMarkdown(problem.description);
    document.getElementById('problem-content').innerHTML = `
        <div class="problem-meta" style="display:flex;gap:8px;margin-bottom:16px;align-items:center;">
            <span class="difficulty-badge ${problem.difficulty === 'Khởi động' ? 'easy' : problem.difficulty === 'Vận dụng' ? 'medium' : 'hard'}"
                style="font-size:0.8rem;padding:3px 10px;">
                ${problem.difficulty}
            </span>
            <span style="color:var(--text-muted);font-size:0.8rem;">
                ⏱️ Giới hạn: ${problem.time_limit}s/test
            </span>
        </div>
        ${problemHtml}
    `;
    renderMath(document.getElementById('problem-content'));

    // Show problem tab
    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('theory-content').classList.add('hidden');
    document.getElementById('problem-content').classList.remove('hidden');
    document.getElementById('ai-content').classList.add('hidden');

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === 'problem');
    });

    // Clear results and AI
    document.getElementById('results-content').innerHTML = `
        <div class="results-placeholder"><p>Nhấn <strong>🚀 Nộp bài</strong> để chấm 10 test.</p></div>
    `;
    document.getElementById('ai-content').innerHTML = `
        <div class="ai-placeholder">
            <span class="ai-icon">🤖</span>
            <p>Nhận xét từ AI Mentor sẽ hiển thị ở đây sau khi em nộp bài.</p>
        </div>
    `;

    // Restore code: Ưu tiên khôi phục code học sinh đang viết dở từ localStorage
    const savedCode = getStoredProblemCode(problemId);
    if (savedCode !== null && savedCode.trim() !== '') {
        editor.setValue(savedCode);
    } else {
        editor.setValue('# Viết code Python ở đây\nimport sys\ninput = sys.stdin.readline\n\n');
    }
    setTimeout(() => editor && editor.refresh(), 50);

    renderSidebar();
}

// ============================================================================
// CODE EXECUTION
// ============================================================================

async function runCode() {
    const code = editor.getValue();
    const inputData = document.getElementById('custom-input').value;
    const btn = document.getElementById('run-code');

    btn.disabled = true;
    btn.innerHTML = '⏳ Đang chạy...';

    try {
        const result = await apiPost('/api/run', { code, input_data: inputData });

        let html = '<div class="run-output">';
        if (result.output) {
            html += `<div class="output-text">${escapeHtml(result.output)}</div>`;
        }
        if (result.error) {
            html += `<div class="error-text">${escapeHtml(result.error)}</div>`;
        }
        if (!result.output && !result.error) {
            html += '<div class="output-text">(Không có output)</div>';
        }
        html += `<div class="time-text">⏱️ Thời gian: ${result.time_ms}ms</div>`;
        html += '</div>';

        document.getElementById('results-content').innerHTML = html;
    } catch (e) {
        document.getElementById('results-content').innerHTML = `
            <div class="run-output"><div class="error-text">Lỗi: ${e.message}</div></div>
        `;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '▶️ Chạy thử';
    }
}

async function submitCode() {
    if (!currentProblemId) {
        showToast('⚠️ Hãy chọn bài tập trước khi nộp bài!');
        return;
    }

    const code = editor.getValue();
    saveProblemCodeToStorage(currentProblemId, code);

    // Lấy API key riêng nếu học sinh có nhập, hoặc để trống để dùng AI có sẵn của giáo viên
    const customApiKey = (localStorage.getItem('hsg_custom_api_key') || '').trim();
    const customModel = (localStorage.getItem('hsg_custom_model') || 'gemini-3.8-flash').trim();
    const btn = document.getElementById('submit-code');

    btn.disabled = true;
    btn.innerHTML = '⏳ Đang chấm...';
    showLoading('Đang chấm 10 test cases...');

    try {
        const result = await apiPost('/api/submit', {
            problem_id: currentProblemId,
            code,
            api_key: customApiKey,
            model_name: customModel,
        });

        renderTestResults(result);

        // Render AI feedback
        if (result.ai_feedback) {
            const aiHtml = renderMarkdown(result.ai_feedback);
            document.getElementById('ai-content').innerHTML = `
                <div class="ai-feedback-content">${aiHtml}</div>
            `;
            renderMath(document.getElementById('ai-content'));
        }

        // Nếu đạt AC 10/10: Đồng bộ ngay vào localStorage của trình duyệt
        if (result.score === result.total) {
            saveACProblemToStorage(currentProblemId);
            if (!progressData[currentProblemId]) {
                progressData[currentProblemId] = {
                    problem_id: currentProblemId,
                    completed: 1,
                    best_score: result.total,
                    attempts: 1,
                };
            } else {
                progressData[currentProblemId].completed = 1;
                progressData[currentProblemId].best_score = result.total;
            }
            showToast('🎉 Tuyệt vời! AC hoàn hảo 10/10! 🎊');
        }

        // Cập nhật lại tiến độ và sidebar / roadmap
        await loadProgress();
        renderSidebar();
        if (currentView === 'roadmap') {
            renderRoadmap();
        }

    } catch (e) {
        document.getElementById('results-content').innerHTML = `
            <div class="run-output"><div class="error-text">Lỗi: ${e.message}</div></div>
        `;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🚀 Nộp bài';
        hideLoading();
    }
}

// ============================================================================
// DEBUGGER LOGIC
// ============================================================================

let debugSteps = [];
let currentDebugStep = 0;

async function startDebug() {
    if (!currentProblemId) {
        showToast('⚠️ Hãy chọn bài tập trước khi Debug!');
        return;
    }
    const code = editor.getValue();
    const btn = document.getElementById('debug-code');
    
    btn.disabled = true;
    btn.innerHTML = '⏳ Đang nạp...';
    
    // Tìm test_index đầu tiên bị sai, nếu không có thì lấy test 0
    let targetTestIndex = 0;
    if (progressData[currentProblemId] && progressData[currentProblemId].results) {
        const results = progressData[currentProblemId].results;
        const firstFailed = results.findIndex(r => r.status !== 'AC');
        if (firstFailed !== -1) targetTestIndex = firstFailed;
    }

    try {
        const result = await apiPost('/api/debug', {
            problem_id: currentProblemId,
            code: code,
            test_index: targetTestIndex
        });

        if (result.status === 'error') {
            showToast('⚠️ Lỗi Debug: ' + result.message);
            return;
        }

        debugSteps = result.steps;
        currentDebugStep = 0;
        
        if (debugSteps.length === 0) {
            showToast('⚠️ Code không có bước chạy nào (có thể là code rỗng).');
            return;
        }

        openDebuggerModal(code);
        renderDebugStep();
    } catch (e) {
        showToast('⚠️ Lỗi kết nối Debugger: ' + e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🐞 Debug';
    }
}

function openDebuggerModal(code) {
    document.getElementById('debugger-modal').style.display = 'flex';
    
    // Render lines
    const lines = code.split('\\n');
    const codeView = document.getElementById('debugger-code-view');
    codeView.innerHTML = lines.map((line, idx) => 
        `<div class="debugger-line" id="dbg-line-${idx + 1}"><div class="debugger-lineno">${idx + 1}</div><div style="white-space:pre">${escapeHtml(line)}</div></div>`
    ).join('');
    
    // Bind events
    document.getElementById('close-debugger').onclick = () => {
        document.getElementById('debugger-modal').style.display = 'none';
    };
    
    document.getElementById('debugger-prev').onclick = () => {
        if (currentDebugStep > 0) {
            currentDebugStep--;
            renderDebugStep();
        }
    };
    
    document.getElementById('debugger-next').onclick = () => {
        if (currentDebugStep < debugSteps.length - 1) {
            currentDebugStep++;
            renderDebugStep();
        }
    };
}

function renderDebugStep() {
    const step = debugSteps[currentDebugStep];
    
    // Highlight line
    document.querySelectorAll('.debugger-line.active').forEach(el => el.classList.remove('active'));
    const lineEl = document.getElementById(`dbg-line-${step.line}`);
    if (lineEl) {
        lineEl.classList.add('active');
        lineEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    // Update vars
    const varsBody = document.getElementById('debugger-vars-body');
    if (Object.keys(step.locals).length === 0) {
        varsBody.innerHTML = '<tr><td colspan="2" style="text-align:center;color:#6c7086;font-style:italic">Chưa có biến nào</td></tr>';
    } else {
        varsBody.innerHTML = Object.entries(step.locals).map(([k, v]) => 
            `<tr><td>${escapeHtml(k)}</td><td>${escapeHtml(String(v))}</td></tr>`
        ).join('');
    }
    
    // Update stdout
    document.getElementById('debugger-stdout').textContent = step.stdout || '';
    
    // Update explanation
    document.getElementById('debugger-explanation').textContent = step.explanation || 'Đang thực thi dòng này...';
    
    // Update controls
    document.getElementById('debugger-status').textContent = `Bước ${currentDebugStep + 1} / ${debugSteps.length} (Dòng ${step.line})`;
    document.getElementById('debugger-prev').disabled = currentDebugStep === 0;
    document.getElementById('debugger-next').disabled = currentDebugStep === debugSteps.length - 1;
}

// Support hotkeys for debugger
document.addEventListener('keydown', (e) => {
    if (document.getElementById('debugger-modal').style.display === 'flex') {
        if (e.key === 'F6' || e.key === 'ArrowRight') {
            e.preventDefault();
            document.getElementById('debugger-next').click();
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            document.getElementById('debugger-prev').click();
        } else if (e.key === 'Escape') {
            document.getElementById('close-debugger').click();
        }
    }
});

// ============================================================================
// RENDER TEST RESULTS
// ============================================================================

function renderTestResults(result) {
    const { score, total, results } = result;
    const scoreClass = score === total ? 'perfect' : (score > 0 ? 'partial' : 'failed');
    const scoreEmoji = score === total ? '🎉' : (score > 0 ? '💪' : '😢');

    let html = `
        <div class="score-summary ${scoreClass}">
            <span class="score-number">${scoreEmoji} ${score}/${total}</span>
            <span class="score-label">
                ${score === total ? 'Accepted — Hoàn hảo!' :
                  score > 0 ? 'Chưa hoàn hảo — Cố lên!' :
                  'Chưa đúng — Xem lại nhé!'}
            </span>
        </div>
    `;

    // Test badges
    html += '<div class="test-results-grid">';
    results.forEach(r => {
        const timeStr = r.time_ms > 0 ? `${r.time_ms}ms` : '';
        html += `
            <div class="test-badge ${r.status}" onclick="toggleTestDetail('test-${r.test}')" title="Test ${r.test}: ${r.status} ${timeStr}">
                #${r.test} ${r.status} ${timeStr ? `(${timeStr})` : ''}
            </div>
        `;
    });
    html += '</div>';

    // Test details (expandable)
    results.forEach(r => {
        html += `<div class="test-detail" id="test-${r.test}">`;
        html += `<div class="test-detail-label">Test ${r.test} — ${r.status} ${r.time_ms ? `(${r.time_ms}ms)` : ''}</div>`;

        if (r.input && r.input !== '(Ẩn - Test hiệu năng)') {
            html += `<div class="test-detail-label">INPUT:</div>`;
            html += `<div class="test-detail-content">${escapeHtml(r.input)}</div>`;

            html += `<div class="test-detail-label">OUTPUT CỦA EM:</div>`;
            html += `<div class="test-detail-content" style="color:${r.status === 'AC' ? 'var(--success)' : 'var(--error)'}">${escapeHtml(r.student_output || '(trống)')}</div>`;

            html += `<div class="test-detail-label">OUTPUT CHUẨN:</div>`;
            html += `<div class="test-detail-content" style="color:var(--success)">${escapeHtml(r.expected_output || '')}</div>`;
        } else {
            html += `<div class="test-detail-content" style="color:var(--text-muted)">Test hiệu năng — chi tiết được ẩn</div>`;
        }

        if (r.error) {
            html += `<div class="test-detail-label">LỖI:</div>`;
            html += `<div class="test-detail-content" style="color:var(--error)">${escapeHtml(r.error)}</div>`;
        }

        html += '</div>';
    });

    document.getElementById('results-content').innerHTML = html;
}

function toggleTestDetail(id) {
    const el = document.getElementById(id);
    if (el) {
        el.classList.toggle('open');
    }
}

// ============================================================================
// ROADMAP VIEW
// ============================================================================

function renderRoadmap() {
    const container = document.getElementById('roadmap-container');
    container.innerHTML = '';

    // ---- Helper tạo folder accordion trong roadmap ----
    function makeRoadmapFolder({ icon, label, defaultOpen = false, content }) {
        const wrap = document.createElement('div');
        wrap.className = 'roadmap-folder';

        const header = document.createElement('button');
        header.className = `roadmap-folder-header${defaultOpen ? ' open' : ''}`;
        header.innerHTML = `
            <span class="rf-icon">${icon}</span>
            <span class="rf-label">${label}</span>
            <span class="rf-arrow">▶</span>
        `;

        const body = document.createElement('div');
        body.className = `roadmap-folder-body${defaultOpen ? ' open' : ''}`;
        content(body);

        header.addEventListener('click', () => {
            header.classList.toggle('open');
            body.classList.toggle('open');
        });

        wrap.appendChild(header);
        wrap.appendChild(body);
        container.appendChild(wrap);
    }

    const titleEl = document.createElement('div');
    titleEl.innerHTML = `
        <h1 class="roadmap-title">🗺️ Lộ trình Học Tập Python</h1>
        <p class="roadmap-subtitle">Từ con số 0 → Chinh phục mọi kỳ thi</p>
    `;
    container.appendChild(titleEl);

    // ---- Folder 1: Ôn HSG (đóng mặc định) ----
    makeRoadmapFolder({
        icon: '🏆',
        label: 'Ôn HSG',
        defaultOpen: false,
        content(body) {
            stagesData.forEach(stage => {
                const completedCount = stage.problems.filter(p =>
                    progressData[p.id]?.completed
                ).length;
                const totalCount = stage.problems.length;

                let stageClass = '';
                if (completedCount === totalCount) stageClass = 'completed';
                else if (completedCount > 0) stageClass = 'in-progress';

                const stageEl = document.createElement('div');
                stageEl.className = `roadmap-stage ${stageClass}`;
                let problemTags = '';
                stage.problems.forEach(p => {
                    const isCompleted = progressData[p.id]?.completed;
                    problemTags += `<span class="roadmap-problem-tag ${isCompleted ? 'completed' : ''}">${isCompleted ? '✅' : '⬜'} ${p.title}</span>`;
                });
                stageEl.innerHTML = `
                    <div class="stage-number">${stage.id}</div>
                    <div class="stage-card" onclick="goToStage(${stage.id})">
                        <div class="stage-card-title">${stage.icon} Chặng ${stage.id}: ${stage.title}</div>
                        <div class="stage-card-desc">${completedCount}/${totalCount} bài hoàn thành</div>
                        <div class="stage-card-problems">${problemTags}</div>
                    </div>
                `;
                body.appendChild(stageEl);
            });
        }
    });

    // ---- Folder 2: Ôn TN THPT QGia ----
    makeRoadmapFolder({
        icon: '📝',
        label: 'Ôn TN THPT QGia',
        defaultOpen: false,
        content(body) {
            body.innerHTML = `<div class="roadmap-placeholder">📂 Chưa có nội dung — Sẽ cập nhật sau</div>`;
        }
    });

    // ---- Folder 3: Luyện Đề ----
    makeRoadmapFolder({
        icon: '📋',
        label: 'Luyện Đề',
        defaultOpen: false,
        content(body) {
            body.innerHTML = `<div class="roadmap-placeholder">📂 Chưa có đề — Sẽ cập nhật sau</div>`;
        }
    });

    // ---- Folder 4: BTap GV giao ----
    makeRoadmapFolder({
        icon: '✏️',
        label: 'BTap GV giao',
        defaultOpen: false,
        content(body) {
            body.innerHTML = `<div class="roadmap-placeholder">📂 Chưa có bài — GV thêm bài tập tại đây</div>`;
        }
    });
}

function goToStage(stageId) {
    switchView('learn');
    selectStage(stageId);
}

// ============================================================================
// MARKDOWN RENDERING
// ============================================================================

function renderMarkdown(text) {
    if (!text) return '';

    // Configure marked
    marked.setOptions({
        breaks: true,
        gfm: true,
        highlight: function(code, lang) {
            return code;  // Let CSS handle styling
        }
    });

    return marked.parse(text);
}

function renderMath(element) {
    if (typeof renderMathInElement === 'function') {
        renderMathInElement(element, {
            delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
                { left: '\\(', right: '\\)', display: false },
                { left: '\\[', right: '\\]', display: true },
            ],
            throwOnError: false,
        });
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

let loadingProgressInterval = null;
let loadingAnimFrame = null;
let currentLoadingPercent = 0;

function showLoading(initialText = 'Đang chấm 10 test cases...') {
    const overlay = document.getElementById('loading-overlay');
    const tdat3d = document.getElementById('tdat-3d-box');
    const tdatFront = document.getElementById('tdat-front');
    const tdatShadow = document.getElementById('tdat-shadow-layer');
    const fillEl = document.getElementById('loading-progress-fill');
    const percentEl = document.getElementById('loading-percent');
    const subtextEl = document.getElementById('loading-subtext');

    if (!overlay) return;

    overlay.style.display = 'flex';
    currentLoadingPercent = 0;
    if (fillEl) fillEl.style.width = '0%';
    if (percentEl) percentEl.textContent = '0%';
    if (subtextEl) subtextEl.textContent = initialText;

    // === ANIMATION 3D TDat (extrusion thật) ===
    if (tdat3d) {
        let cycleStart = null;
        const CYCLE = 5000; // 5 giây mỗi chu kỳ

        function animateTdat(ts) {
            if (!cycleStart) cycleStart = ts;
            const elapsed = (ts - cycleStart) % CYCLE;
            const p = elapsed / CYCLE; // 0..1

            let scale, rotY, rotX, opacity;

            if (p < 0.30) {
                // Bay từ tâm ra + xoay 2 vòng
                const t = p / 0.30;
                const ease = 1 - Math.pow(1 - t, 3);
                scale = 0.01 + ease * 0.99;
                rotY = -720 + ease * 720;
                rotX = 20 - ease * 35; // bắt đầu từ nhìn xuống, rồi về -15 độ
                opacity = ease;
            } else if (p < 0.60) {
                // Đứng yên — nghiêng nhẹ qua lại quanh -15 độ (góc nhìn từ trên như ảnh)
                const t = (p - 0.30) / 0.30;
                const swing = Math.sin(t * Math.PI * 2) * 10; // dao động ±10 độ
                scale = 1;
                rotY = swing;
                rotX = -15 + Math.sin(t * Math.PI) * 4; // dao động nhẹ quanh -15
                opacity = 1;
            } else if (p < 0.90) {
                // Xoay ngược + nhỏ dần về tâm
                const t = (p - 0.60) / 0.30;
                const ease = t * t * t;
                scale = 1 - ease * 0.99;
                rotY = ease * 720;
                rotX = -15 + ease * 35;
                opacity = 1 - ease;
            } else {
                scale = 0.01; rotY = 720; rotX = 20; opacity = 0;
            }

            tdat3d.style.transform = `scale(${scale}) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
            tdat3d.style.opacity = opacity;

            // Gradient mặt trước chạy nhẹ
            if (tdatFront) {
                const shift = (ts / 40) % 360;
                tdatFront.style.filter = `
                    drop-shadow(0 -2px 1px rgba(255,255,255,.4))
                    drop-shadow(0 0 ${25 + Math.sin(ts/500)*8}px rgba(139,92,246,.8))
                    drop-shadow(0 0 55px rgba(168,85,247,.5))
                `;
            }

            // Đổ bóng extrusion thay đổi theo góc xoay thực tế
            if (tdatShadow) {
                // Tính offset bóng dựa trên rotY và rotX
                const radY = rotY * Math.PI / 180;
                const radX = rotX * Math.PI / 180;
                const dxFactor = Math.sin(radY); // -1..1
                const dyFactor = Math.sin(-radX) * 0.5 + 0.5; // 0..1

                const layers = [];
                for (let i = 1; i <= 15; i++) {
                    const dx = dxFactor * i * 1.5;
                    const dy = i * 2;
                    const dark = Math.max(0, 45 - i * 3);
                    layers.push(`${dx.toFixed(1)}px ${dy}px 0 hsl(265,75%,${dark}%)`);
                }
                layers.push(`${(dxFactor * 18).toFixed(1)}px 36px 8px rgba(0,0,0,.6)`);
                layers.push(`${(dxFactor * 24).toFixed(1)}px 50px 20px rgba(0,0,0,.4)`);
                tdatShadow.style.textShadow = layers.join(',');
            }

            loadingAnimFrame = requestAnimationFrame(animateTdat);
        }

        if (loadingAnimFrame) cancelAnimationFrame(loadingAnimFrame);
        loadingAnimFrame = requestAnimationFrame(animateTdat);
    }

    // === PROGRESS BAR ===
    if (loadingProgressInterval) clearInterval(loadingProgressInterval);

    const milestones = [
        { limit: 25, step: 4, text: 'Đang nạp môi trường Python...' },
        { limit: 60, step: 2.5, text: 'Đang chấm 10 test cases...' },
        { limit: 85, step: 1.5, text: 'Đang đo thời gian thực thi & kiểm tra biên...' },
        { limit: 96, step: 0.8, text: 'AI Mentor đang phân tích và nhận xét code...' }
    ];
    let mi = 0;

    loadingProgressInterval = setInterval(() => {
        if (currentLoadingPercent >= 96) return;
        const stage = milestones[mi];
        if (stage) {
            currentLoadingPercent = Math.min(stage.limit, currentLoadingPercent + stage.step);
            if (subtextEl) subtextEl.textContent = stage.text;
            if (currentLoadingPercent >= stage.limit && mi < milestones.length - 1) mi++;
        } else {
            currentLoadingPercent = Math.min(96, currentLoadingPercent + 0.5);
        }
        const v = Math.floor(currentLoadingPercent);
        if (fillEl) fillEl.style.width = v + '%';
        if (percentEl) percentEl.textContent = v + '%';
    }, 70);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    const tdat = document.getElementById('tdat-3d-box');
    const fillEl = document.getElementById('loading-progress-fill');
    const percentEl = document.getElementById('loading-percent');
    const subtextEl = document.getElementById('loading-subtext');

    if (loadingProgressInterval) { clearInterval(loadingProgressInterval); loadingProgressInterval = null; }
    if (loadingAnimFrame) { cancelAnimationFrame(loadingAnimFrame); loadingAnimFrame = null; }

    if (fillEl) fillEl.style.width = '100%';
    if (percentEl) percentEl.textContent = '100%';
    if (subtextEl) subtextEl.textContent = 'Hoàn tất chấm bài!';

    setTimeout(() => {
        if (overlay) overlay.style.display = 'none';
        if (tdat) { tdat.style.transform = ''; tdat.style.opacity = ''; }
    }, 350);
}

function showToast(message) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: var(--bg-card);
        color: var(--text-primary);
        padding: 12px 24px;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        z-index: 500;
        font-size: 0.9rem;
        font-weight: 500;
        animation: slideUp 0.3s ease-out;
        backdrop-filter: blur(10px);
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from { opacity: 0; transform: translateX(-50%) translateY(20px); }
        to { opacity: 1; transform: translateX(-50%) translateY(0); }
    }
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);

// Make toggleTestDetail globally accessible
window.toggleTestDetail = toggleTestDetail;
window.goToStage = goToStage;

// ============================================================================
// EDITOR PANEL — COLLAPSE / EXPAND & DRAG RESIZE
// ============================================================================

function initEditorPanel() {
    const panelRight = document.getElementById('panel-right');
    const toggleBtn  = document.getElementById('toggle-editor-panel');
    const resizeHandle = document.getElementById('panel-resize-handle');
    const appMain  = document.getElementById('app-main');

    // ── 1. COLLAPSE / EXPAND ──────────────────────────────────────────────
    // Tạo nút mở lại khi panel bị ẩn
    const expandBtn = document.createElement('button');
    expandBtn.className = 'editor-expand-btn';
    expandBtn.id = 'editor-expand-btn';
    expandBtn.title = 'Mở Code Editor';
    expandBtn.innerHTML = '▶ Code';
    document.body.appendChild(expandBtn);

    let isCollapsed = true;  // mặc định ẩn
    let savedWidth  = null;

    function collapsePanel() {
        savedWidth = panelRight.offsetWidth;
        isCollapsed = true;
        panelRight.classList.add('collapsed');
        resizeHandle.style.display = 'none';
        expandBtn.classList.add('visible');
        toggleBtn.innerHTML = '▶ Mở';
    }

    function expandPanel() {
        isCollapsed = false;
        panelRight.classList.remove('collapsed');
        if (savedWidth) {
            panelRight.style.flex = 'none';
            panelRight.style.width = savedWidth + 'px';
        }
        resizeHandle.style.display = '';
        expandBtn.classList.remove('visible');
        toggleBtn.innerHTML = '◀ Ẩn';
        // Refresh CodeMirror
        setTimeout(() => editor && editor.refresh(), 50);
    }

    toggleBtn.addEventListener('click', () => {
        if (isCollapsed) expandPanel();
        else collapsePanel();
    });

    // Auto-collapse khi tải trang
    collapsePanel();


    expandBtn.addEventListener('click', expandPanel);

    // ── 2. DRAG RESIZE ───────────────────────────────────────────────────
    let isDragging = false;
    let startX     = 0;
    let startWidth = 0;

    resizeHandle.addEventListener('mousedown', (e) => {
        if (isCollapsed) return;
        isDragging  = true;
        startX      = e.clientX;
        startWidth  = panelRight.offsetWidth;
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        // Kéo sang trái = panel phải rộng ra, sang phải = thu lại
        const delta    = startX - e.clientX;
        const newWidth = Math.max(280, Math.min(startWidth + delta, window.innerWidth * 0.75));
        panelRight.style.flex  = 'none';
        panelRight.style.width = newWidth + 'px';
        savedWidth = newWidth;
    });

    document.addEventListener('mouseup', () => {
        if (!isDragging) return;
        isDragging = false;
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
        setTimeout(() => editor && editor.refresh(), 50);
    });

    // Double-click handle → reset về 50%
    resizeHandle.addEventListener('dblclick', () => {
        panelRight.style.flex  = '1';
        panelRight.style.width = '';
        savedWidth = null;
        setTimeout(() => editor && editor.refresh(), 50);
        showToast('✅ Đặt lại kích thước mặc định');
    });
}

// ============================================================================
// SETTINGS MODAL (AI API KEY & MODEL)
// ============================================================================

function initSettings() {
    const modal = document.getElementById('settings-modal');
    const openBtn = document.getElementById('open-settings-btn');
    const closeBtn = document.getElementById('close-settings-btn');
    const cancelBtn = document.getElementById('cancel-settings-btn');
    const saveBtn = document.getElementById('save-settings-btn');
    const apiKeyInput = document.getElementById('custom-api-key');
    const modelSelect = document.getElementById('custom-model-name');

    if (!modal) return;

    // Nạp cài đặt đã lưu trong localStorage của trình duyệt học sinh
    const customKey = localStorage.getItem('hsg_custom_api_key') || '';
    const customModel = localStorage.getItem('hsg_custom_model') || 'gemini-3.8-flash';
    if (apiKeyInput) apiKeyInput.value = customKey;
    if (modelSelect) modelSelect.value = customModel;

    function openModal() {
        if (apiKeyInput) apiKeyInput.value = localStorage.getItem('hsg_custom_api_key') || '';
        if (modelSelect) modelSelect.value = localStorage.getItem('hsg_custom_model') || 'gemini-3.8-flash';
        modal.classList.remove('hidden');
    }

    function closeModal() {
        modal.classList.add('hidden');
    }

    if (openBtn) openBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            const key = apiKeyInput ? apiKeyInput.value.trim() : '';
            const model = modelSelect ? modelSelect.value.trim() : 'gemini-3.8-flash';

            localStorage.setItem('hsg_custom_api_key', key);
            localStorage.setItem('hsg_custom_model', model);

            closeModal();
            if (key) {
                showToast('✅ Đã lưu API Key riêng của bạn!');
            } else {
                showToast('✅ Đã kích hoạt AI tích hợp sẵn của giáo viên!');
            }
        });
    }
}

// ============================================================================
// AUTHENTICATION & ADMIN DASHBOARD
// ============================================================================

async function initAuth() {
    const btnLogin = document.getElementById('btn-show-login');
    const btnProfile = document.getElementById('user-profile-btn');
    const nameDisplay = document.getElementById('display-user-name');
    const btnAdmin = document.getElementById('btn-admin-dashboard');

    if (authToken) {
        try {
            currentUser = await apiGet('/api/auth/profile');
            btnLogin.style.display = 'none';
            btnProfile.style.display = 'flex';
            nameDisplay.textContent = currentUser.full_name;
            if (currentUser.role === 'Owner') {
                btnAdmin.style.display = 'inline-block';
            }
        } catch (e) {
            console.warn("Phiên đăng nhập hết hạn hoặc lỗi:", e);
            logout(false);
        }
    } else {
        btnLogin.style.display = 'inline-block';
        btnProfile.style.display = 'none';
        btnAdmin.style.display = 'none';
    }

    // Modal toggles
    btnLogin.addEventListener('click', () => openModal('modal-login'));
    document.getElementById('link-to-register').addEventListener('click', (e) => { e.preventDefault(); closeModals(); openModal('modal-register'); });
    document.getElementById('link-to-login').addEventListener('click', (e) => { e.preventDefault(); closeModals(); openModal('modal-login'); });
    btnProfile.addEventListener('click', showProfileModal);
    document.getElementById('btn-logout').addEventListener('click', () => logout(true));
    btnAdmin.addEventListener('click', showAdminDashboard);

    // Form handlers
    document.getElementById('btn-send-otp').addEventListener('click', sendOtp);
    document.getElementById('btn-submit-register').addEventListener('click', handleRegister);
    document.getElementById('btn-submit-login').addEventListener('click', handleLogin);
}

function openModal(id) {
    document.getElementById(id).classList.remove('hidden');
}

function closeModals() {
    document.querySelectorAll('.modal-overlay').forEach(el => el.classList.add('hidden'));
}

async function sendOtp() {
    const email = document.getElementById('reg-email').value.trim();
    const statusLabel = document.getElementById('otp-status');
    if (!email) return alert("Vui lòng nhập Email trước khi gửi mã.");
    
    statusLabel.textContent = "Đang gửi...";
    try {
        await apiPost('/api/auth/send-otp', { email });
        statusLabel.textContent = "Đã gửi mã! Kiểm tra hộp thư (cả mục Spam).";
        statusLabel.style.color = "#10b981";
    } catch (e) {
        statusLabel.textContent = e.message;
        statusLabel.style.color = "#ef4444";
    }
}

async function handleRegister() {
    const full_name = document.getElementById('reg-name').value.trim();
    const email = document.getElementById('reg-email').value.trim();
    const password = document.getElementById('reg-password').value;
    const repassword = document.getElementById('reg-repassword').value;
    const otp_code = document.getElementById('reg-otp').value.trim();

    if (!full_name || !email || !password || !otp_code) return alert("Vui lòng điền đủ thông tin.");
    if (password !== repassword) return alert("Mật khẩu không khớp.");

    try {
        const res = await apiPost('/api/auth/register', { full_name, email, password, otp_code });
        alert(res.message);
        closeModals();
        openModal('modal-login');
    } catch (e) {
        alert(e.message);
    }
}

async function handleLogin() {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    if (!email || !password) return alert("Vui lòng nhập email và mật khẩu.");

    try {
        const res = await apiPost('/api/auth/login', { email, password });
        authToken = res.access_token;
        localStorage.setItem('auth_token', authToken);
        closeModals();
        await initAuth();
        alert("Đăng nhập thành công!");
    } catch (e) {
        alert(e.message);
    }
}

function logout(showAlert = true) {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('auth_token');
    closeModals();
    document.getElementById('btn-show-login').style.display = 'inline-block';
    document.getElementById('user-profile-btn').style.display = 'none';
    document.getElementById('btn-admin-dashboard').style.display = 'none';
    if (showAlert) alert("Đã đăng xuất.");
    // Trở về trang chủ
    switchView('learn');
}

function showProfileModal() {
    if (!currentUser) return;
    document.getElementById('prof-name').textContent = currentUser.full_name;
    document.getElementById('prof-role').textContent = `Vai trò: ${currentUser.role}`;
    document.getElementById('prof-email').textContent = `Mail: ${currentUser.email}`;
    openModal('modal-profile');
}

// === Admin Dashboard ===
function showAdminDashboard() {
    // Ẩn tất cả views khác
    document.getElementById('app-main').style.display = 'none';
    document.getElementById('roadmap-view').classList.add('hidden');
    document.getElementById('admin-view').classList.remove('hidden');

    // Chuyển nav active state
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('btn-admin-dashboard').classList.add('active');

    loadAdminUsers();
}

// Ghi đè hàm switchView để hỗ trợ ẩn admin-view
const _originalSwitchView = switchView;
switchView = function(view) {
    document.getElementById('admin-view').classList.add('hidden');
    document.getElementById('app-main').style.display = 'flex';
    document.getElementById('btn-admin-dashboard').classList.remove('active');
    _originalSwitchView(view);
};

async function loadAdminUsers() {
    const tbody = document.getElementById('admin-users-list');
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Đang tải dữ liệu...</td></tr>';
    try {
        const res = await apiGet('/api/admin/users');
        tbody.innerHTML = '';
        res.users.forEach(u => {
            const tr = document.createElement('tr');
            
            const roleSelect = document.createElement('select');
            roleSelect.className = 'role-select';
            ['Học Sinh', 'Giáo Viên', 'Owner'].forEach(r => {
                const opt = document.createElement('option');
                opt.value = r; opt.textContent = r;
                if (u.role === r) opt.selected = true;
                roleSelect.appendChild(opt);
            });
            roleSelect.addEventListener('change', (e) => changeUserRole(u.id, e.target.value));

            tr.innerHTML = `
                <td>${u.id}</td>
                <td>${u.full_name}</td>
                <td>${u.email}</td>
                <td class="role-cell"></td>
                <td>${new Date(u.created_at).toLocaleString('vi-VN')}</td>
            `;
            tr.querySelector('.role-cell').appendChild(roleSelect);
            tbody.appendChild(tr);
        });
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="5" style="color:red;">Lỗi: ${e.message}</td></tr>`;
    }
}

async function changeUserRole(userId, newRole) {
    if (!confirm(`Xác nhận đổi quyền của người dùng ID ${userId} thành ${newRole}?`)) {
        loadAdminUsers(); // revert
        return;
    }
    try {
        await apiPut(`/api/admin/users/${userId}/role`, { role: newRole });
        alert(`Đã đổi quyền thành ${newRole}`);
        // Nếu tự đổi quyền bản thân thì cần tải lại auth
        if (currentUser && currentUser.id === userId) {
            initAuth();
        }
    } catch (e) {
        alert("Lỗi: " + e.message);
        loadAdminUsers(); // revert
    }
}
