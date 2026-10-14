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
let currentView = 'roadmap';  // Default is 'roadmap'
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

    // Khôi phục bài tập và đoạn code học sinh đang làm dở nếu có (sẵn sàng trong bộ nhớ/giao diện)
    const lastStageId = localStorage.getItem('hsg_last_stage_id');
    const lastProblemId = localStorage.getItem('hsg_last_problem_id');
    if (lastStageId && lastProblemId) {
        await selectProblem(parseInt(lastStageId), lastProblemId);
    }

    // Luôn hiển thị giao diện mặc định (Roadmap) khi vừa vào web
    switchView('roadmap');
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
    // Click logo TDat ở góc trên cùng bên trái -> Trở về giao diện mặc định (Roadmap)
    const handleLogoClick = () => {
        switchView('roadmap');
        window.scrollTo({ top: 0, behavior: 'smooth' });
        const rView = document.getElementById('roadmap-view');
        if (rView) rView.scrollTo({ top: 0, behavior: 'smooth' });
    };
    document.getElementById('site-logo')?.addEventListener('click', handleLogoClick);
    document.getElementById('logo-tdat')?.addEventListener('click', handleLogoClick);

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

async function apiDelete(path) {
    const headers = {};
    if (authToken) headers['Authorization'] = `Bearer ${authToken}`;
    const res = await fetch(`${API_BASE}${path}`, {
        method: 'DELETE',
        headers,
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

const STAGE_PRACTICE_TITLES = {
    1: "Bài tập về Nhập xuất & Biến cơ bản",
    2: "Bài tập về Cấu trúc Rẽ nhánh & Toán học",
    3: "Bài tập về Vòng lặp & Khử vòng lặp",
    4: "Bài tập về Xử lý Xâu ký tự (String)",
    5: "Bài tập về Danh sách (List) & Set/Dict",
    6: "Bài tập về Số học & Thuật toán thi HSG",
    7: "Bài tập về Sắp xếp & Tìm kiếm nhị phân",
    8: "Bài tập về Prefix Sum, Hai con trỏ & Đệ quy"
};

function getPracticeTitle(stageId) {
    return STAGE_PRACTICE_TITLES[stageId] || `Bài tập Chặng ${stageId}`;
}

// ============================================================================
// SIDEBAR RENDERING
// ============================================================================

function renderSidebar() {
    const container = document.getElementById('sidebar-stages');

    // Lưu lại trạng thái các folder / subfolder mà người dùng đã tự tay bấm mở
    const openLabels = new Set();
    container.querySelectorAll('.folder-header.open, .subfolder-header.open').forEach(el => {
        const text = el.querySelector('.folder-label, .subfolder-label')?.textContent?.trim();
        if (text) openLabels.add(text);
    });

    container.innerHTML = '';

    // ---- Helper: tạo folder Level-1 ----
    function makeFolder({ icon, label, defaultOpen = false, content }) {
        const group = document.createElement('div');
        group.className = 'folder-group';

        const isOpen = openLabels.has(label) || defaultOpen;
        const header = document.createElement('button');
        header.className = `folder-header${isOpen ? ' open' : ''}`;
        header.innerHTML = `
            <span class="folder-icon">${icon}</span>
            <span class="folder-label">${label}</span>
            <span class="folder-arrow">▶</span>
        `;

        const body = document.createElement('div');
        body.className = `folder-content${isOpen ? ' open' : ''}`;
        content(body);

        header.addEventListener('click', () => {
            header.classList.toggle('open');
            body.classList.toggle('open');
        });

        group.appendChild(header);
        group.appendChild(body);
        container.appendChild(group);
    }

    // ---- Helper: tạo subfolder Level-2 (Lí Thuyết, Bài tập...) ----
    function makeSubFolder(parentEl, { icon, label, defaultOpen = false, content }) {
        const subGroup = document.createElement('div');
        subGroup.className = 'subfolder-group';

        const isOpen = openLabels.has(label) || defaultOpen;
        const header = document.createElement('button');
        header.className = `subfolder-header${isOpen ? ' open' : ''}`;
        header.innerHTML = `
            <span class="subfolder-icon">${icon}</span>
            <span class="subfolder-label">${label}</span>
            <span class="subfolder-arrow">▶</span>
        `;

        const subBody = document.createElement('div');
        subBody.className = `subfolder-content${isOpen ? ' open' : ''}`;
        content(subBody);

        header.addEventListener('click', (e) => {
            e.stopPropagation();
            header.classList.toggle('open');
            subBody.classList.toggle('open');
        });

        subGroup.appendChild(header);
        subGroup.appendChild(subBody);
        parentEl.appendChild(subGroup);
    }

    // ---- Folder 1: Ôn HSG (đóng mặc định) ----
    makeFolder({
        icon: '🏆',
        label: 'Ôn HSG',
        defaultOpen: false,
        content(body) {
            // Mục nhỏ 1: Lí Thuyết (Mặc định ĐÓNG cho đến khi người dùng bấm mở)
            makeSubFolder(body, {
                icon: '📖',
                label: 'Lí Thuyết',
                defaultOpen: false,
                content(subBody) {
                    stagesData.forEach(stage => {
                        const link = document.createElement('button');
                        const isTheoryActive = (currentStageId === stage.id && !document.getElementById('theory-content')?.classList.contains('hidden'));
                        link.className = `problem-link ${isTheoryActive ? 'active' : ''}`;
                        link.innerHTML = `
                            <span class="problem-status"></span>
                            <span>${stage.icon} Chặng ${stage.id}: ${stage.title}</span>
                        `;
                        link.addEventListener('click', (e) => {
                            e.stopPropagation();
                            selectStage(stage.id);
                            switchTab('theory');
                        });
                        subBody.appendChild(link);
                    });
                }
            });

            // Mục nhỏ 2: Bài tập (Mặc định ĐÓNG cho đến khi người dùng bấm mở)
            makeSubFolder(body, {
                icon: '📝',
                label: 'Bài tập',
                defaultOpen: false,
                content(subBody) {
                    stagesData.forEach(stage => {
                        const group = document.createElement('div');
                        group.className = 'stage-group';

                        const completedCount = stage.problems.filter(p =>
                            progressData[p.id]?.completed
                        ).length;
                        const totalCount = stage.problems.length;

                        const header = document.createElement('button');
                        const isStageActive = (currentStageId === stage.id && !document.getElementById('problem-content')?.classList.contains('hidden'));
                        header.className = `stage-header ${isStageActive ? 'active' : ''}`;
                        header.innerHTML = `
                            <span class="stage-icon">${stage.icon}</span>
                            <span class="stage-title">${getPracticeTitle(stage.id)}</span>
                            <span class="stage-progress">${completedCount}/${totalCount}</span>
                        `;

                        const problems = document.createElement('div');
                        problems.className = 'stage-problems';

                        header.addEventListener('click', (e) => {
                            e.stopPropagation();
                            header.classList.toggle('active');
                            problems.classList.toggle('open');
                        });

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
                        subBody.appendChild(group);
                    });
                }
            });
        }
    });

    // ---- Folder 2: Ôn TN THPT QGia ----
    makeFolder({
        icon: '📑',
        label: 'Ôn TN THPT QGia',
        defaultOpen: false,
        content(body) {
            const topics = [
                { id: "1", title: "1. Mạng máy tính" },
                { id: "2", title: "2. Trí tuệ nhân tạo (AI)" },
                { id: "3", title: "3. Cơ sở dữ liệu (CSDL)" },
                { id: "4", title: "4. HTML & CSS" },
                { id: "5", title: "5. Bảo mật & An toàn" }
            ];
            
            topics.forEach(topic => {
                const link = document.createElement('button');
                link.className = `problem-link`;
                link.innerHTML = `<span class="problem-status"></span> 📖 ${topic.title}`;
                link.addEventListener('click', (e) => {
                    e.stopPropagation();
                    selectTHPTTheory(topic.id);
                });
                body.appendChild(link);
            });
        }
    });

    // ---- Folder 3: BTap GV giao ----
    makeFolder({
        icon: '🖊️',
        label: 'BTap GV giao',
        defaultOpen: false,
        content(body) {
            renderSidebarClassroomFolder(body);
        }
    });
}


// ============================================================================
// STAGE & PROBLEM SELECTION
// ============================================================================

function configureEditorForTopic(topicId) {
    const tabProblem = document.getElementById('tab-problem');
    const tabAi = document.getElementById('tab-ai');
    const expandBtn = document.getElementById('editor-expand-btn');
    const panelRight = document.getElementById('panel-right');
    
    const editorTitleText = document.getElementById('editor-title-text');
    const editorLangBadge = document.getElementById('editor-lang-badge');
    const runBtn = document.getElementById('run-code');
    const debugBtn = document.getElementById('debug-code');

    // Reset everything to default first
    if (tabProblem) tabProblem.style.display = '';
    if (tabAi) tabAi.style.display = '';
    if (expandBtn) {
        expandBtn.style.display = '';
        expandBtn.innerHTML = '▶ Code';
    }
    if (editorTitleText) editorTitleText.innerText = 'Code Editor';
    if (editorLangBadge) editorLangBadge.style.display = '';
    if (runBtn) runBtn.style.display = '';
    if (debugBtn) debugBtn.style.display = '';

    const defaultPyCode = '# Viết code Python ở đây\nimport sys\ninput = sys.stdin.readline\n\n';

    if (topicId === "3") {
        if (expandBtn) expandBtn.innerHTML = '▲ Làm Bài';
        if (editorTitleText) editorTitleText.innerText = 'Làm Bài';
        if (editorLangBadge) editorLangBadge.style.display = 'none';
        if (runBtn) runBtn.style.display = 'none';
        if (debugBtn) debugBtn.style.display = 'none';
        if (editor && editor.getValue().trim() === defaultPyCode.trim()) {
            editor.setValue('');
        }
    } else if (topicId === "4") {
        // Keeps defaults for HTML/CSS
    } else if (topicId) { // topicId is 1, 2, 5
        if (tabProblem) tabProblem.style.display = 'none';
        if (tabAi) tabAi.style.display = 'none';
        if (expandBtn) expandBtn.style.display = 'none';
        if (panelRight && !panelRight.classList.contains('collapsed')) {
            const toggleBtn = document.getElementById('toggle-editor-panel');
            if (toggleBtn) toggleBtn.click();
        }
    }

    if (!topicId || topicId === "4") {
         if (editor && editor.getValue().trim() === '') {
             editor.setValue(defaultPyCode);
         }
    }
}

async function selectTHPTTheory(topicId) {
    currentStageId = 'thpt_' + topicId;
    currentProblemId = null;

    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('problem-content').classList.add('hidden');
    document.getElementById('ai-content').classList.add('hidden');
    document.getElementById('theory-content').classList.remove('hidden');

    document.getElementById('theory-content').innerHTML = '<div style="text-align: center; color: #a6adc8;">Đang tải dữ liệu...</div>';
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === 'theory');
    });

    configureEditorForTopic(topicId);

    try {
        const data = await apiGet(`/api/thpt/${topicId}`);
        const thptHtml = renderMarkdown(data.theory);
        document.getElementById('theory-content').innerHTML = thptHtml;
        renderMath(document.getElementById('theory-content'));
        
        if (topicId === "3") {
            currentProblemId = "thpt_3_sql"; // enable submitting
            const exData = await apiGet(`/api/thpt/3_exercises`);
            const exHtml = renderMarkdown(exData.theory);
            document.getElementById('problem-content').innerHTML = `
                <div style="padding: 0 10px 40px 10px; line-height: 1.6; color: var(--text-color);">
                    ${exHtml}
                </div>
            `;
            renderMath(document.getElementById('problem-content'));
        }
    } catch (e) {
        document.getElementById('theory-content').innerHTML = `<div style="color:red; text-align:center;">Lỗi tải dữ liệu: ${e.message}</div>`;
    }
    
    switchView('learn');
    renderSidebar();
}

async function selectStage(stageId) {
    currentStageId = stageId;

    configureEditorForTopic(null);

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

    configureEditorForTopic(null);

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
        let result;
        if (currentProblemId.startsWith('assignment_')) {
            const assignmentId = currentProblemId.replace('assignment_', '');
            result = await apiPost(`/api/classroom/student/assignment/${assignmentId}/submit`, {
                code,
                api_key: customApiKey,
                model_name: customModel,
            });
        } else {
            result = await apiPost('/api/submit', {
                problem_id: currentProblemId,
                code,
                api_key: customApiKey,
                model_name: customModel,
            });
        }

        if (currentProblemId === 'thpt_3_sql') {
            document.getElementById('results-content').innerHTML = `
                <div class="score-summary perfect" style="text-align: center; padding: 20px;">
                    <span class="score-number">✅ Hệ thống đã tiếp nhận SQL</span>
                    <span class="score-label" style="display: block; margin-top: 10px;">AI Mentor đã đọc code và đưa ra nhận xét. Hãy nhấn sang tab <b>AI Mentor</b> để xem nhé!</span>
                </div>
            `;
            // Switch to AI tab automatically for SQL exercises
            switchTab('ai-feedback');
        } else {
            renderTestResults(result);
        }

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
        <h1 class="roadmap-title">📖 Lộ Trình Học Tập & Ôn Luyện Tin Học</h1>
        <p class="roadmap-subtitle">Từ con số 0 → Tự tin chinh phục mọi kỳ thi (HSG, THPT Quốc Gia & Bài tập trên lớp)</p>
    `;
    container.appendChild(titleEl);

    // ---- Folder 1: Ôn HSG (đóng mặc định) ----
    makeRoadmapFolder({
        icon: '🏆',
        label: 'Ôn HSG',
        defaultOpen: false,
        content(body) {
            // Section 1: Lí Thuyết (8 chặng)
            const theorySec = document.createElement('div');
            theorySec.className = 'roadmap-subsection';
            theorySec.innerHTML = `
                <div class="roadmap-subsection-header">
                    <span class="rss-icon">📖</span>
                    <span class="rss-title">Lí Thuyết 8 Chặng</span>
                    <span class="rss-desc">Nền tảng kiến thức & Góc Vũ Khí Python</span>
                </div>
            `;
            const theoryGrid = document.createElement('div');
            stagesData.forEach(stage => {
                const stageEl = document.createElement('div');
                stageEl.className = 'roadmap-stage';
                stageEl.innerHTML = `
                    <div class="stage-number">${stage.id}</div>
                    <div class="stage-card" onclick="goToStageTheory(${stage.id})">
                        <div class="stage-card-title">${stage.icon} Chặng ${stage.id}: ${stage.title}</div>
                        <div class="stage-card-desc">📖 Đọc lý thuyết chi tiết & vũ khí thi HSG</div>
                    </div>
                `;
                theoryGrid.appendChild(stageEl);
            });
            theorySec.appendChild(theoryGrid);
            body.appendChild(theorySec);

            // Section 2: Bài tập (24 bài tập thực hành)
            const practiceSec = document.createElement('div');
            practiceSec.className = 'roadmap-subsection';
            practiceSec.style.marginTop = '28px';
            practiceSec.innerHTML = `
                <div class="roadmap-subsection-header">
                    <span class="rss-icon">📝</span>
                    <span class="rss-title">Bài Tập Thực Hành</span>
                    <span class="rss-desc">24 bài tập chia theo 8 chặng — Chấm 10 test tự động</span>
                </div>
            `;
            const practiceGrid = document.createElement('div');
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
                        <div class="stage-card-title">${stage.icon} Chặng ${stage.id}: ${getPracticeTitle(stage.id)}</div>
                        <div class="stage-card-desc">${completedCount}/${totalCount} bài hoàn thành</div>
                        <div class="stage-card-problems">${problemTags}</div>
                    </div>
                `;
                practiceGrid.appendChild(stageEl);
            });
            practiceSec.appendChild(practiceGrid);
            body.appendChild(practiceSec);
        }
    });

    // ---- Folder 2: Ôn TN THPT QGia ----
    makeRoadmapFolder({
        icon: '📑',
        label: 'Ôn TN THPT QGia',
        defaultOpen: false,
        content(body) {
            const topics = [
                { id: "1", title: "Mạng máy tính và Internet" },
                { id: "2", title: "Trí tuệ nhân tạo (AI) và Học máy" },
                { id: "3", title: "Cơ sở dữ liệu (CSDL) và SQL" },
                { id: "4", title: "HTML và CSS căn bản" },
                { id: "5", title: "Bảo mật, an toàn hệ thống và khắc phục sự cố" }
            ];
            
            topics.forEach(topic => {
                const stageEl = document.createElement('div');
                stageEl.className = 'roadmap-stage';
                stageEl.innerHTML = `
                    <div class="stage-number">${topic.id}</div>
                    <div class="stage-card" onclick="goToTHPTTheory('${topic.id}')">
                        <div class="stage-card-title">📖 Chuyên đề ${topic.id}: ${topic.title}</div>
                        <div class="stage-card-desc">Lý thuyết trọng tâm & bẫy trắc nghiệm</div>
                    </div>
                `;
                body.appendChild(stageEl);
            });
        }
    });

    // ---- Folder 3: BTap GV giao ----
    makeRoadmapFolder({
        icon: '🖊️',
        label: 'BTap GV giao',
        defaultOpen: false,
        content(body) {
            renderRoadmapClassroomFolder(body);
        }
    });
}

function goToStageTheory(stageId) {
    switchView('learn');
    selectStage(stageId);
    switchTab('theory');
}

function goToStage(stageId) {
    switchView('learn');
    selectStage(stageId);
    const stage = stagesData.find(s => s.id === stageId);
    if (stage && stage.problems.length > 0) {
        selectProblem(stageId, stage.problems[0].id);
    }
}

function goToTHPTTheory(topicId) {
    switchView('learn');
    selectTHPTTheory(topicId);
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

// Make functions globally accessible
window.toggleTestDetail = toggleTestDetail;
window.goToStage = goToStage;
window.goToTHPTTheory = goToTHPTTheory;

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
    const btnClassroom = document.getElementById('btn-classroom');

    if (authToken) {
        try {
            currentUser = await apiGet('/api/auth/profile');
            btnLogin.style.display = 'none';
            btnProfile.style.display = 'flex';
            nameDisplay.textContent = currentUser.full_name;
            if (btnClassroom) btnClassroom.style.display = 'inline-block';
            if (currentUser.role === 'Owner') {
                btnAdmin.style.display = 'inline-block';
            }
            // Reload user progress and update folders
            await loadProgress();
            renderSidebar();
            if (currentView === 'roadmap') renderRoadmap();
        } catch (e) {
            console.warn("Phiên đăng nhập hết hạn hoặc lỗi:", e);
            logout(false);
        }
    } else {
        btnLogin.style.display = 'inline-block';
        btnProfile.style.display = 'none';
        btnAdmin.style.display = 'none';
        if (btnClassroom) btnClassroom.style.display = 'none';
    }

    // Modal toggles
    btnLogin.addEventListener('click', () => openModal('modal-login'));
    document.getElementById('link-to-register').addEventListener('click', (e) => { e.preventDefault(); closeModals(); openModal('modal-register'); });
    document.getElementById('link-to-login').addEventListener('click', (e) => { e.preventDefault(); closeModals(); openModal('modal-login'); });
    btnProfile.addEventListener('click', showProfileModal);
    document.getElementById('btn-logout').addEventListener('click', () => logout(true));
    btnAdmin.addEventListener('click', showAdminDashboard);
    if (btnClassroom) btnClassroom.addEventListener('click', openClassroomModal);

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
    const btnClassroom = document.getElementById('btn-classroom');
    if (btnClassroom) btnClassroom.style.display = 'none';
    if (showAlert) alert("Đã đăng xuất.");
    loadProgress();
    renderSidebar();
    switchView('roadmap');
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


// ============================================================================
// CLASSROOM LMS MODULE (QUẢN LÝ LỚP HỌC & BÀI TẬP GIÁO VIÊN GIAO)
// ============================================================================

let teacherClass = null;
let studentClass = null;
let currentAssignment = null;

function setTeacherActiveTab(activeBtn) {
    document.querySelectorAll('.classroom-tab-btn').forEach(b => b.classList.remove('active'));
    activeBtn.classList.add('active');
}

function closeStudentDetailModal() {
    document.getElementById('modal-student-detail').classList.add('hidden');
}

function closeSubmissionDetailModal() {
    document.getElementById('modal-submission-detail').classList.add('hidden');
}

// ---- SIDEBAR & ROADMAP FOLDER 3 (BTAP GV GIAO) ----

async function renderSidebarClassroomFolder(body) {
    if (!currentUser) {
        body.innerHTML = `
            <div class="folder-placeholder" style="cursor:pointer; color:var(--text-muted);" onclick="openModal('modal-login')">
                🔒 Đăng nhập để xem bài tập GV giao
            </div>
        `;
        return;
    }

    if (currentUser.role === 'Giáo Viên' || currentUser.role === 'Owner') {
        body.innerHTML = `
            <div class="folder-placeholder" style="cursor:pointer; color:var(--accent-secondary); font-weight:600; padding:10px 14px; text-align:left;" onclick="openClassroomModal()">
                🏫 Quản lý lớp học & Giao bài ➔
            </div>
        `;
        return;
    }

    body.innerHTML = `<div class="folder-placeholder">⏳ Đang tải bài tập lớp...</div>`;
    try {
        const myClass = await apiGet('/api/classroom/student/my-class');
        if (!myClass.has_class) {
            body.innerHTML = `
                <div class="folder-placeholder" style="cursor:pointer; color:var(--accent-primary); font-weight:600; padding:10px 14px; text-align:left;" onclick="openClassroomModal()">
                    🏫 Chưa vào lớp. Nhấn để nhập mã lớp ➔
                </div>
            `;
            return;
        }

        const data = await apiGet('/api/classroom/student/assignments');
        const assignments = data.assignments || [];
        if (assignments.length === 0) {
            body.innerHTML = `<div class="folder-placeholder">🎉 Lớp chưa có bài tập mới nào!</div>`;
            return;
        }

        body.innerHTML = '';
        assignments.forEach(a => {
            const btn = document.createElement('button');
            const isAc = a.has_submitted && a.status === 'AC';
            const isWa = a.has_submitted && a.status !== 'AC';
            btn.className = 'problem-link';
            if (currentProblemId === 'assignment_' + a.id) btn.classList.add('active');
            
            let statusIcon = '⭕';
            let statusClass = '';
            if (isAc) {
                statusIcon = '✅';
                statusClass = 'completed';
            } else if (isWa) {
                statusIcon = '⚠️';
                statusClass = 'attempted';
            }

            btn.innerHTML = `<span class="problem-status ${statusClass}">${statusIcon}</span> ${escapeHtml(a.title)}`;
            btn.title = `Hạn nộp: ${a.deadline || 'Không giới hạn'} | Điểm: ${a.has_submitted ? a.score + '/' + a.total_tests : 'Chưa nộp'}`;
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                openAssignmentProblem(a);
            });
            body.appendChild(btn);
        });
    } catch (e) {
        body.innerHTML = `<div class="folder-placeholder" style="color:#ef4444;">Lỗi: ${e.message}</div>`;
    }
}

async function renderRoadmapClassroomFolder(body) {
    if (!currentUser) {
        body.innerHTML = `
            <div class="roadmap-placeholder" style="cursor:pointer; padding: 24px;" onclick="openModal('modal-login')">
                🔒 Vui lòng <b>Đăng nhập</b> để xem các bài tập do Giáo Viên giao riêng cho lớp của bạn.
            </div>
        `;
        return;
    }

    if (currentUser.role === 'Giáo Viên' || currentUser.role === 'Owner') {
        body.innerHTML = `
            <div class="roadmap-placeholder" style="cursor:pointer; padding: 24px; color:var(--accent-secondary);" onclick="openClassroomModal()">
                🏫 <b>Tài khoản Giáo viên:</b> Nhấn vào đây để mở Bảng điều khiển Lớp học, tạo bài tập & theo dõi tiến độ học sinh ➔
            </div>
        `;
        return;
    }

    body.innerHTML = `<div class="roadmap-placeholder">⏳ Đang tải bài tập lớp...</div>`;
    try {
        const myClass = await apiGet('/api/classroom/student/my-class');
        if (!myClass.has_class) {
            body.innerHTML = `
                <div class="roadmap-placeholder" style="cursor:pointer; padding: 24px; color:var(--accent-primary);" onclick="openClassroomModal()">
                    🏫 Bạn chưa tham gia lớp học nào. Nhấn vào đây để <b>nhập mã lớp do Thầy/Cô cung cấp</b> ➔
                </div>
            `;
            return;
        }

        const data = await apiGet('/api/classroom/student/assignments');
        const assignments = data.assignments || [];
        if (assignments.length === 0) {
            body.innerHTML = `<div class="roadmap-placeholder">🎉 Thầy cô chưa giao bài mới nào cho lớp <b>${escapeHtml(myClass.class.class_name)}</b>. Hãy chăm chỉ luyện các chặng HSG nhé!</div>`;
            return;
        }

        body.innerHTML = '';
        assignments.forEach(a => {
            const card = document.createElement('div');
            card.className = 'stage-card';
            const isAc = a.has_submitted && a.status === 'AC';
            const isWa = a.has_submitted && a.status !== 'AC';
            const statusBadge = isAc 
                ? '<span style="color:#10b981;font-weight:700;">✅ Đã nộp: ' + a.score + '/' + a.total_tests + ' AC</span>'
                : isWa 
                ? '<span style="color:#f59e0b;font-weight:700;">⚠️ Đã nộp: ' + a.score + '/' + a.total_tests + ' (Chưa hoàn thành)</span>'
                : '<span style="color:var(--text-muted);">⭕ Chưa làm</span>';

            card.innerHTML = `
                <div class="stage-card-icon">🖊️</div>
                <div class="stage-card-body">
                    <div class="stage-card-title">${escapeHtml(a.title)}</div>
                    <div class="stage-card-desc">
                        ${statusBadge} • ⏱️ ${a.time_limit || 1.0}s • 📅 ${a.deadline ? 'Hạn: ' + new Date(a.deadline).toLocaleDateString('vi-VN') : 'Không giới hạn hạn nộp'}
                    </div>
                </div>
            `;
            card.addEventListener('click', () => openAssignmentProblem(a));
            body.appendChild(card);
        });
    } catch (e) {
        body.innerHTML = `<div class="roadmap-placeholder" style="color:#ef4444;">Lỗi: ${e.message}</div>`;
    }
}

// ---- OPEN ASSIGNMENT PROBLEM IN EDITOR & PROBLEM PANEL ----

async function openAssignmentProblem(assignment) {
    currentProblemId = 'assignment_' + assignment.id;
    currentStageId = null;
    currentAssignment = assignment;

    try {
        localStorage.setItem('hsg_last_stage_id', '');
        localStorage.setItem('hsg_last_problem_id', currentProblemId);
    } catch (e) {}

    closeModals();
    switchView('learn');
    configureEditorForTopic(null);

    const editorTitleText = document.getElementById('editor-title-text');
    if (editorTitleText) editorTitleText.innerText = `Bài tập GV: ${assignment.title}`;

    const deadlineText = assignment.deadline 
        ? `📅 Hạn nộp: ${new Date(assignment.deadline).toLocaleString('vi-VN')}` 
        : '📅 Hạn nộp: Không giới hạn';

    const sampleTestsHtml = (assignment.sample_tests && assignment.sample_tests.length > 0)
        ? `
            <div style="margin-top: 16px; background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: 6px; padding: 12px;">
                <h4 style="margin: 0 0 8px; color: var(--accent-secondary); font-size: 0.9rem;">Ví dụ Test mẫu:</h4>
                ${assignment.sample_tests.map((tc, idx) => `
                    <div style="margin-bottom: 8px; font-size: 0.82rem;">
                        <b>Test ${idx + 1}:</b>
                        <div style="background:#0d1117; padding:6px; border-radius:4px; font-family:monospace; margin-top:2px;">
                            Input: ${escapeHtml(tc.input || '(trống)')}<br>
                            Expected: ${escapeHtml(tc.expected_output || '(trống)')}
                        </div>
                    </div>
                `).join('')}
            </div>
        `
        : '';

    document.getElementById('problem-content').innerHTML = `
        <div class="problem-meta" style="display:flex;gap:8px;margin-bottom:16px;align-items:center;flex-wrap:wrap;">
            <span class="difficulty-badge medium" style="font-size:0.8rem;padding:3px 10px;">
                🖊️ Bài tập Giáo viên giao
            </span>
            <span style="color:var(--text-muted);font-size:0.8rem;">
                ⏱️ Giới hạn: ${assignment.time_limit || 1.0}s/test
            </span>
            <span style="color:var(--text-muted);font-size:0.8rem;">
                ${deadlineText}
            </span>
        </div>
        <h2 style="margin-bottom: 12px; color: var(--text-primary); font-size: 1.3rem;">${escapeHtml(assignment.title)}</h2>
        <div class="assignment-desc-markdown">
            ${renderMarkdown(assignment.description)}
        </div>
        ${sampleTestsHtml}
    `;
    renderMath(document.getElementById('problem-content'));

    // Switch to problem tab
    document.getElementById('welcome-screen').classList.add('hidden');
    document.getElementById('theory-content').classList.add('hidden');
    document.getElementById('problem-content').classList.remove('hidden');
    document.getElementById('ai-content').classList.add('hidden');

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === 'problem');
    });

    // Load saved code for this assignment or default python starter
    const savedCode = localStorage.getItem('code_problem_' + currentProblemId);
    if (savedCode && savedCode.trim()) {
        editor.setValue(savedCode);
    } else {
        editor.setValue('# Viết code Python giải bài tập giáo viên giao tại đây\nimport sys\ninput = sys.stdin.readline\n\n');
    }

    // Reset results and AI placeholder
    document.getElementById('results-content').innerHTML = `
        <div class="results-placeholder"><p>Nhấn <strong>🚀 Nộp bài</strong> để chấm với bộ test của giáo viên & nhận xét từ AI Mentor.</p></div>
    `;
    document.getElementById('ai-content').innerHTML = `
        <div class="ai-placeholder">
            <span class="ai-icon">🤖</span>
            <p>Nhận xét từ AI Mentor sẽ hiển thị ở đây sau khi em nộp bài.</p>
        </div>
    `;

    renderSidebar();
}

// ---- CLASSROOM MAIN MODAL CONTROLLER ----

async function openClassroomModal() {
    if (!currentUser) {
        showToast('⚠️ Vui lòng đăng nhập để sử dụng tính năng Lớp học!');
        openModal('modal-login');
        return;
    }

    openModal('modal-classroom');
    const body = document.getElementById('classroom-modal-body');
    body.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--text-muted);">⏳ Đang tải dữ liệu lớp học...</div>';

    if (currentUser.role === 'Giáo Viên' || currentUser.role === 'Owner') {
        document.getElementById('classroom-main-title').textContent = '🏫 Bảng Điều Khiển Lớp Học (Giáo Viên)';
        document.getElementById('classroom-main-sub').textContent = 'Quản lý mã lớp, học sinh, giao bài tập và theo dõi lộ trình làm bài';
        await renderTeacherClassroom(body);
    } else {
        document.getElementById('classroom-main-title').textContent = '🏫 Lớp Học Của Bạn';
        document.getElementById('classroom-main-sub').textContent = 'Tham gia lớp của Thầy/Cô để nhận đề bài tập và theo dõi tiến độ';
        await renderStudentClassroom(body);
    }
}

// ---- TEACHER CLASSROOM WORKSPACE ----

async function renderTeacherClassroom(body) {
    try {
        const res = await apiGet('/api/classroom/teacher/class');
        if (!res.has_class) {
            body.innerHTML = `
                <div class="class-banner-card" style="text-align: center; padding: 30px;">
                    <div style="font-size: 3rem; margin-bottom: 10px;">🎓</div>
                    <h3 style="font-size: 1.3rem; margin-bottom: 8px;">Bạn Chưa Tạo Lớp Học</h3>
                    <p style="color: var(--text-muted); max-width: 500px; margin: 0 auto 20px;">
                        Mỗi tài khoản Giáo Viên được quản lý tối đa 1 mã lớp học. Hãy tạo lớp để học sinh nhập mã tham gia và bắt đầu giao bài tập!
                    </p>
                    <div style="max-width: 420px; margin: 0 auto; text-align: left;">
                        <div class="form-group">
                            <label>Tên lớp học *</label>
                            <input type="text" id="new-class-name" placeholder="Ví dụ: Đội Tuyển HSG Tin Học 12" style="font-weight: 600;">
                        </div>
                        <div class="form-group">
                            <label>Mã lớp tùy chỉnh (Không bắt buộc - để trống hệ thống tự tạo)</label>
                            <input type="text" id="new-class-code" placeholder="Ví dụ: TIN12A, HSG839" maxlength="10" style="font-family: monospace; letter-spacing: 2px;">
                        </div>
                        <button class="btn-primary" id="btn-create-class" style="margin-top: 15px;">🚀 Tạo Lớp Học Ngay</button>
                    </div>
                </div>
            `;
            document.getElementById('btn-create-class').addEventListener('click', handleCreateClass);
            return;
        }

        const cls = res.class;
        teacherClass = cls;

        body.innerHTML = `
            <!-- Banner -->
            <div class="class-banner-card">
                <div class="class-banner-top">
                    <div>
                        <div class="class-title-tag">
                            <span>🏫 ${escapeHtml(cls.class_name)}</span>
                        </div>
                        <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 4px;">
                            Khởi tạo ngày: ${new Date(cls.created_at).toLocaleDateString('vi-VN')}
                        </div>
                    </div>
                    <div class="class-code-badge-wrap" id="btn-copy-code" title="Nhấn để sao chép mã lớp">
                        <span style="font-size: 0.85rem; color: var(--text-muted);">Mã lớp:</span>
                        <span class="class-code-text">${cls.class_code}</span>
                        <span style="font-size: 1rem;">📋</span>
                    </div>
                </div>
                <div class="class-stats-grid">
                    <div class="class-stat-box">
                        <div class="class-stat-val">${cls.student_count}</div>
                        <div class="class-stat-lbl">Học sinh trong lớp</div>
                    </div>
                    <div class="class-stat-box">
                        <div class="class-stat-val">${cls.assignment_count}</div>
                        <div class="class-stat-lbl">Bài tập đã giao</div>
                    </div>
                </div>
            </div>

            <!-- Tabs -->
            <div class="classroom-tabs">
                <button class="classroom-tab-btn active" data-tab="students" id="tab-teacher-students">
                    👥 Học sinh & Lộ trình (${cls.student_count})
                </button>
                <button class="classroom-tab-btn" data-tab="assignments" id="tab-teacher-assignments">
                    📝 Giao bài & Quản lý (${cls.assignment_count})
                </button>
                <button class="classroom-tab-btn" data-tab="live" id="tab-teacher-live">
                    ⚡ Hoạt động trực tiếp
                </button>
            </div>

            <!-- Tab Content Pane -->
            <div id="teacher-tab-content">
                <!-- Populated by tab selection -->
            </div>
        `;

        document.getElementById('btn-copy-code').addEventListener('click', () => {
            navigator.clipboard.writeText(cls.class_code);
            showToast(`📋 Đã sao chép mã lớp: ${cls.class_code}`);
        });

        const tabStudents = document.getElementById('tab-teacher-students');
        const tabAssignments = document.getElementById('tab-teacher-assignments');
        const tabLive = document.getElementById('tab-teacher-live');

        tabStudents.addEventListener('click', () => {
            setTeacherActiveTab(tabStudents);
            loadTeacherStudentsPane();
        });
        tabAssignments.addEventListener('click', () => {
            setTeacherActiveTab(tabAssignments);
            loadTeacherAssignmentsPane(cls);
        });
        tabLive.addEventListener('click', () => {
            setTeacherActiveTab(tabLive);
            loadTeacherLivePane();
        });

        // Default open students pane
        loadTeacherStudentsPane();

    } catch (e) {
        body.innerHTML = `<div style="color: #ef4444; padding: 20px;">Lỗi tải dữ liệu lớp học: ${e.message}</div>`;
    }
}

async function handleCreateClass() {
    const className = document.getElementById('new-class-name').value.trim();
    const classCode = document.getElementById('new-class-code').value.trim();

    if (!className) {
        alert("Vui lòng nhập tên lớp học.");
        return;
    }

    try {
        const payload = { class_name: className };
        if (classCode) payload.class_code = classCode;
        await apiPost('/api/classroom/teacher/class', payload);
        showToast('🎉 Tạo lớp học thành công!');
        openClassroomModal();
    } catch (e) {
        alert("Lỗi tạo lớp học: " + e.message);
    }
}

async function loadTeacherStudentsPane() {
    const pane = document.getElementById('teacher-tab-content');
    pane.innerHTML = '<div style="text-align:center; padding: 30px; color: var(--text-muted);">⏳ Đang tải danh sách học sinh & tiến độ...</div>';
    try {
        const res = await apiGet('/api/classroom/teacher/students');
        const students = res.students || [];

        if (students.length === 0) {
            pane.innerHTML = `
                <div class="folder-placeholder" style="padding: 40px; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">👥</div>
                    <h4>Chưa có học sinh nào tham gia lớp</h4>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 6px;">
                        Hãy gửi mã lớp cho các em học sinh. Khi các em nhập mã trên tài khoản học sinh, danh sách và tiến độ sẽ hiển thị tại đây!
                    </p>
                </div>
            `;
            return;
        }

        pane.innerHTML = `
            <div class="classroom-table-wrap">
                <table class="classroom-table">
                    <thead>
                        <tr>
                            <th>STT</th>
                            <th>Họ và tên</th>
                            <th>Email</th>
                            <th>Ngày vào lớp</th>
                            <th>Tiến độ 8 chặng HSG</th>
                            <th>Lượt nộp bài</th>
                            <th>Thao tác</th>
                        </tr>
                    </thead>
                    <tbody id="teacher-students-tbody">
                        ${students.map((st, i) => {
                            const totalProblems = 24; // 8 chặng x 3 bài
                            const percent = Math.min(100, Math.round((st.completed_count / totalProblems) * 100));
                            return `
                                <tr>
                                    <td>${i + 1}</td>
                                    <td style="font-weight: 600; color: var(--text-primary);">${escapeHtml(st.full_name)}</td>
                                    <td>${escapeHtml(st.email)}</td>
                                    <td>${new Date(st.joined_at).toLocaleDateString('vi-VN')}</td>
                                    <td>
                                        <div class="student-progress-bar-wrap" title="Hoàn thành ${st.completed_count}/${totalProblems} bài tập">
                                            <div class="student-progress-bar-track">
                                                <div class="student-progress-bar-fill" style="width: ${percent}%;"></div>
                                            </div>
                                            <span class="student-progress-text">${percent}% (${st.completed_count}/${totalProblems})</span>
                                        </div>
                                    </td>
                                    <td>${st.total_submissions} lần</td>
                                    <td>
                                        <button class="btn-secondary" style="padding: 5px 12px; font-size: 0.82rem;" onclick="viewStudentDetail(${st.id}, '${escapeHtml(st.full_name)}', '${escapeHtml(st.email)}')">
                                            👁️ Xem Lộ Trình & Bài Nộp
                                        </button>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } catch (e) {
        pane.innerHTML = `<div style="color: #ef4444; padding: 20px;">Lỗi tải học sinh: ${e.message}</div>`;
    }
}

async function viewStudentDetail(studentId, name, email) {
    document.getElementById('student-detail-name').textContent = `Học sinh: ${name}`;
    document.getElementById('student-detail-meta').textContent = `Email: ${email} • Theo dõi chi tiết 8 chặng HSG và bài nộp`;
    const body = document.getElementById('student-detail-body');
    body.innerHTML = '<div style="text-align:center; padding: 30px; color: var(--text-muted);">⏳ Đang tải chi tiết lộ trình học sinh...</div>';
    openModal('modal-student-detail');

    try {
        const res = await apiGet(`/api/classroom/teacher/student/${studentId}`);
        const roadmap = res.roadmap;
        const submissions = res.submissions || [];

        // Build stages HTML
        const stagesHtml = roadmap.stages.map(stg => {
            const isCompleted = stg.completed === stg.total;
            return `
                <div class="stage-breakdown-card ${isCompleted ? 'completed' : ''}">
                    <div class="stage-breakdown-header">
                        <span>Chặng ${stg.id}: ${escapeHtml(stg.title)}</span>
                        <span style="color: ${isCompleted ? '#10b981' : 'var(--text-muted)'};">${stg.completed}/${stg.total}</span>
                    </div>
                    <div class="stage-breakdown-problems">
                        ${stg.problems.map(p => {
                            let badge = '<span class="prob-badge-empty">⭕ Chưa làm</span>';
                            if (p.completed) {
                                badge = `<span class="prob-badge-ac">✅ AC (${p.best_score}/10)</span>`;
                            } else if (p.attempts > 0) {
                                badge = `<span class="prob-badge-wa">⚠️ WA (${p.best_score}/10)</span>`;
                            }
                            return `
                                <div class="stage-prob-row">
                                    <span>${escapeHtml(p.title)}</span>
                                    ${badge}
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        }).join('');

        // Build submissions table
        const subsTableHtml = submissions.length === 0
            ? '<p style="color: var(--text-muted); padding: 10px;">Học sinh chưa nộp bài tập nào.</p>'
            : `
                <div class="classroom-table-wrap">
                    <table class="classroom-table">
                        <thead>
                            <tr>
                                <th>Thời gian</th>
                                <th>Bài tập / Chặng</th>
                                <th>Điểm số</th>
                                <th>Trạng thái</th>
                                <th>Hành động</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${submissions.map(sub => `
                                <tr>
                                    <td>${new Date(sub.submitted_at).toLocaleString('vi-VN')}</td>
                                    <td style="font-weight: 600;">${escapeHtml(sub.problem_id)}</td>
                                    <td><b>${sub.score}</b> / ${sub.total_tests}</td>
                                    <td>
                                        <span class="difficulty-badge ${sub.status === 'AC' ? 'easy' : 'hard'}" style="padding: 2px 8px; font-size: 0.75rem;">
                                            ${sub.status}
                                        </span>
                                    </td>
                                    <td>
                                        <button class="btn-secondary" style="padding: 4px 10px; font-size: 0.8rem;" onclick="viewSubmissionDetail('${escapeHtml(name)}', '${escapeHtml(sub.problem_id)}', ${JSON.stringify(sub.code || '').replace(/"/g, '&quot;')}, ${sub.score}, ${sub.total_tests}, '${sub.status}', ${JSON.stringify(sub.ai_feedback || '').replace(/"/g, '&quot;')}, '${sub.submitted_at}')">
                                            🔍 Xem Code & AI
                                        </button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;

        body.innerHTML = `
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 14px 18px; margin-bottom: 16px;">
                <h4 style="margin: 0; color: #10b981;">📊 Tổng quan tiến độ lộ trình HSG:</h4>
                <p style="margin: 4px 0 0; font-size: 0.9rem; color: var(--text-secondary);">
                    Đã hoàn thành <b>${roadmap.completed_problems} / ${roadmap.total_problems}</b> bài tập (${Math.round((roadmap.completed_problems / roadmap.total_problems) * 100)}%) qua ${roadmap.completed_stages} / ${roadmap.total_stages} chặng học tập.
                </p>
            </div>

            <h3 style="font-size: 1.1rem; margin-bottom: 12px; color: var(--text-primary);">📖 Chi Tiết 8 Chặng Lộ Trình:</h3>
            <div class="stages-grid-breakdown">
                ${stagesHtml}
            </div>

            <h3 style="font-size: 1.1rem; margin-top: 20px; margin-bottom: 12px; color: var(--text-primary);">📝 Lịch Sử Nộp Bài & Nhận Xét AI:</h3>
            ${subsTableHtml}
        `;

    } catch (e) {
        body.innerHTML = `<div style="color: #ef4444; padding: 20px;">Lỗi: ${e.message}</div>`;
    }
}

async function loadTeacherAssignmentsPane(cls) {
    const pane = document.getElementById('teacher-tab-content');
    pane.innerHTML = '<div style="text-align:center; padding: 30px; color: var(--text-muted);">⏳ Đang tải danh sách bài tập đã giao...</div>';

    try {
        const res = await apiGet('/api/classroom/teacher/assignments');
        const assignments = res.assignments || [];

        pane.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <h3 style="margin:0; font-size:1.15rem; color:var(--text-primary);">Bài tập đã giao cho lớp (${assignments.length})</h3>
                <button class="btn-primary" id="btn-toggle-create-assignment" style="width:auto; padding:8px 18px; margin:0;">
                    ➕ Giao Bài Tập Mới
                </button>
            </div>

            <!-- Form tạo bài tập mới (toggleable) -->
            <div class="create-assignment-box hidden" id="box-create-assignment">
                <h3 style="margin:0 0 14px; color:var(--accent-secondary); font-size:1.1rem;">📝 Giao Bài Tập Mới Cho Lớp</h3>
                <div class="form-group">
                    <label>Tiêu đề bài tập *</label>
                    <input type="text" id="asg-title" placeholder="Ví dụ: Đếm số lượng số nguyên tố trong dãy số">
                </div>
                <div class="form-group">
                    <label>Đề bài chi tiết (Hỗ trợ Markdown & Math) *</label>
                    <textarea id="asg-desc" style="width:100%; min-height:100px; background:var(--bg-secondary); border:1px solid var(--border-subtle); border-radius:var(--radius-sm); color:var(--text-primary); padding:10px;" placeholder="Mô tả đề bài, giới hạn dữ liệu (N <= 10^5)..."></textarea>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                    <div class="form-group">
                        <label>Giới hạn thời gian (giây) *</label>
                        <input type="number" id="asg-time-limit" value="1.0" step="0.5" min="0.5" max="5.0">
                    </div>
                    <div class="form-group">
                        <label>Hạn nộp (Không bắt buộc)</label>
                        <input type="datetime-local" id="asg-deadline">
                    </div>
                </div>

                <div style="margin: 16px 0;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <label style="font-weight:600; color:var(--text-secondary);">Bộ Test Cases Chấm Điểm *</label>
                        <button type="button" class="btn-secondary" id="btn-add-testcase" style="padding:4px 10px; font-size:0.8rem;">+ Thêm Test Case</button>
                    </div>
                    <div id="test-cases-container">
                        <div class="test-case-item" data-idx="0">
                            <div class="test-case-grid">
                                <div>
                                    <small style="color:var(--text-muted); display:block; margin-bottom:4px;">Input (Đầu vào):</small>
                                    <textarea class="tc-input" placeholder="Ví dụ: 5\n1 2 3 4 5"></textarea>
                                </div>
                                <div>
                                    <small style="color:var(--text-muted); display:block; margin-bottom:4px;">Expected Output (Đầu ra kỳ vọng):</small>
                                    <textarea class="tc-output" placeholder="Ví dụ: 3"></textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="display:flex; gap:10px; margin-top:16px;">
                    <button class="btn-primary" id="btn-submit-create-assignment" style="flex:1;">🚀 Giao Cho Cả Lớp</button>
                    <button class="btn-secondary" id="btn-cancel-create-assignment" style="flex:none; padding:10px 20px;">Hủy</button>
                </div>
            </div>

            <!-- Danh sách bài tập -->
            <div class="assignments-list-container" id="teacher-assignments-list">
                ${assignments.length === 0 ? `
                    <div class="folder-placeholder" style="padding:30px; text-align:center;">
                        Chưa có bài tập nào được giao. Hãy nhấn nút <b>➕ Giao Bài Tập Mới</b> ở trên để tạo bài!
                    </div>
                ` : assignments.map(a => {
                    const isExpired = a.deadline && new Date(a.deadline) < new Date();
                    const deadlineBadge = a.deadline 
                        ? `<span class="deadline-badge ${isExpired ? 'deadline-expired' : 'deadline-active'}">
                            ${isExpired ? 'Đã hết hạn' : 'Hạn: ' + new Date(a.deadline).toLocaleString('vi-VN')}
                           </span>`
                        : `<span class="deadline-badge deadline-active">Không giới hạn thời gian</span>`;

                    return `
                        <div class="assignment-card">
                            <div class="assignment-main-info">
                                <div class="assignment-card-title">
                                    <span>${escapeHtml(a.title)}</span>
                                    ${deadlineBadge}
                                </div>
                                <div class="assignment-meta-row">
                                    <span>⏱️ Giới hạn: ${a.time_limit || 1.0}s</span>
                                    <span>🧪 ${a.test_case_count || 'Nhiều'} Test cases</span>
                                    <span style="color:#10b981; font-weight:600;">📊 Đã nộp: ${a.submission_count} học sinh</span>
                                </div>
                            </div>
                            <div style="display:flex; gap:8px;">
                                <button class="btn-secondary" style="padding:6px 14px; font-size:0.85rem;" onclick="viewAssignmentSubmissions(${a.id}, '${escapeHtml(a.title)}')">
                                    📊 Xem Bài Nộp
                                </button>
                                <button class="btn-danger" style="padding:6px 12px; font-size:0.85rem;" onclick="deleteAssignment(${a.id}, '${escapeHtml(a.title)}')">
                                    🗑️
                                </button>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        // Wire Create Form Events
        const boxCreate = document.getElementById('box-create-assignment');
        const btnToggle = document.getElementById('btn-toggle-create-assignment');
        const btnCancel = document.getElementById('btn-cancel-create-assignment');
        const btnAddTc = document.getElementById('btn-add-testcase');
        const btnSubmitAsg = document.getElementById('btn-submit-create-assignment');

        btnToggle.addEventListener('click', () => boxCreate.classList.toggle('hidden'));
        btnCancel.addEventListener('click', () => boxCreate.classList.add('hidden'));

        btnAddTc.addEventListener('click', () => {
            const container = document.getElementById('test-cases-container');
            const item = document.createElement('div');
            item.className = 'test-case-item';
            item.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span style="font-size:0.8rem; color:var(--text-muted);">Test case tiếp theo:</span>
                    <button type="button" style="background:none; border:none; color:#ef4444; cursor:pointer; font-size:0.8rem;" onclick="this.closest('.test-case-item').remove()">Xóa test</button>
                </div>
                <div class="test-case-grid">
                    <div>
                        <textarea class="tc-input" placeholder="Input..."></textarea>
                    </div>
                    <div>
                        <textarea class="tc-output" placeholder="Expected Output..."></textarea>
                    </div>
                </div>
            `;
            container.appendChild(item);
        });

        btnSubmitAsg.addEventListener('click', () => submitCreateAssignment(cls));

    } catch (e) {
        pane.innerHTML = `<div style="color: #ef4444; padding: 20px;">Lỗi: ${e.message}</div>`;
    }
}

async function submitCreateAssignment(cls) {
    const title = document.getElementById('asg-title').value.trim();
    const description = document.getElementById('asg-desc').value.trim();
    const time_limit = parseFloat(document.getElementById('asg-time-limit').value) || 1.0;
    const deadline = document.getElementById('asg-deadline').value || null;

    if (!title || !description) {
        alert("Vui lòng nhập tiêu đề và đề bài.");
        return;
    }

    const test_cases = [];
    document.querySelectorAll('#test-cases-container .test-case-item').forEach(item => {
        const inp = item.querySelector('.tc-input').value;
        const out = item.querySelector('.tc-output').value;
        if (inp.trim() || out.trim()) {
            test_cases.push({ input: inp, expected_output: out });
        }
    });

    if (test_cases.length === 0) {
        alert("Vui lòng nhập ít nhất 1 test case để chấm bài.");
        return;
    }

    try {
        await apiPost('/api/classroom/teacher/assignments', {
            title,
            description,
            time_limit,
            deadline,
            test_cases
        });
        showToast('🎉 Đã giao bài tập thành công cho cả lớp!');
        loadTeacherAssignmentsPane(cls);
        renderSidebar();
    } catch (e) {
        alert("Lỗi giao bài tập: " + e.message);
    }
}

async function viewAssignmentSubmissions(assignmentId, title) {
    document.getElementById('student-detail-name').textContent = `Bài nộp: ${title}`;
    document.getElementById('student-detail-meta').textContent = `Danh sách học sinh đã nộp bài tập này`;
    const body = document.getElementById('student-detail-body');
    body.innerHTML = '<div style="text-align:center; padding: 30px; color: var(--text-muted);">⏳ Đang tải bài nộp của học sinh...</div>';
    openModal('modal-student-detail');

    try {
        const res = await apiGet(`/api/classroom/teacher/assignment/${assignmentId}/submissions`);
        const submissions = res.submissions || [];

        if (submissions.length === 0) {
            body.innerHTML = `
                <div class="folder-placeholder" style="padding: 40px; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">📝</div>
                    <h4>Chưa có học sinh nào nộp bài tập này</h4>
                    <p style="color: var(--text-muted); font-size: 0.9rem;">
                        Các bài nộp của học sinh kèm theo điểm số và code sẽ hiển thị tại đây ngay khi các em nộp.
                    </p>
                </div>
            `;
            return;
        }

        body.innerHTML = `
            <div class="classroom-table-wrap">
                <table class="classroom-table">
                    <thead>
                        <tr>
                            <th>STT</th>
                            <th>Học sinh</th>
                            <th>Thời gian nộp</th>
                            <th>Điểm số</th>
                            <th>Trạng thái</th>
                            <th>Hành động</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${submissions.map((sub, i) => `
                            <tr>
                                <td>${i + 1}</td>
                                <td style="font-weight: 600; color: var(--text-primary);">${escapeHtml(sub.student_name)}</td>
                                <td>${new Date(sub.submitted_at).toLocaleString('vi-VN')}</td>
                                <td><b>${sub.score}</b> / ${sub.total_tests}</td>
                                <td>
                                    <span class="difficulty-badge ${sub.status === 'AC' ? 'easy' : 'hard'}" style="padding: 2px 8px; font-size: 0.75rem;">
                                        ${sub.status}
                                    </span>
                                </td>
                                <td>
                                    <button class="btn-secondary" style="padding: 4px 12px; font-size: 0.8rem;" onclick="viewSubmissionDetail('${escapeHtml(sub.student_name)}', '${escapeHtml(title)}', ${JSON.stringify(sub.code || '').replace(/"/g, '&quot;')}, ${sub.score}, ${sub.total_tests}, '${sub.status}', ${JSON.stringify(sub.ai_feedback || '').replace(/"/g, '&quot;')}, '${sub.submitted_at}')">
                                        🔍 Xem Code & AI
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    } catch (e) {
        body.innerHTML = `<div style="color: #ef4444; padding: 20px;">Lỗi: ${e.message}</div>`;
    }
}

async function deleteAssignment(assignmentId, title) {
    if (!confirm(`Bạn có chắc chắn muốn xóa bài tập "${title}"? Toàn bộ bài nộp của học sinh cho bài này cũng sẽ bị xóa.`)) {
        return;
    }
    try {
        await apiDelete(`/api/classroom/teacher/assignment/${assignmentId}`);
        showToast('🗑️ Đã xóa bài tập thành công');
        const res = await apiGet('/api/classroom/teacher/class');
        if (res.has_class) {
            loadTeacherAssignmentsPane(res.class);
        }
        renderSidebar();
    } catch (e) {
        alert("Lỗi khi xóa bài: " + e.message);
    }
}

async function loadTeacherLivePane() {
    const pane = document.getElementById('teacher-tab-content');
    pane.innerHTML = '<div style="text-align:center; padding: 30px; color: var(--text-muted);">⏳ Đang tải hoạt động trực tiếp...</div>';
    try {
        const res = await apiGet('/api/classroom/teacher/live-feed');
        const feed = res.feed || [];

        if (feed.length === 0) {
            pane.innerHTML = `
                <div class="folder-placeholder" style="padding: 40px; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">⚡</div>
                    <h4>Chưa có hoạt động mới</h4>
                    <p style="color: var(--text-muted); font-size: 0.9rem;">
                        Hoạt động nộp bài và làm bài của học sinh trong lớp sẽ xuất hiện theo thời gian thực tại đây.
                    </p>
                </div>
            `;
            return;
        }

        pane.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:10px;">
                ${feed.map(item => `
                    <div class="assignment-card" style="padding:12px 18px;">
                        <div class="assignment-main-info">
                            <div style="font-weight:600; color:var(--text-primary); font-size:0.95rem;">
                                👤 <b>${escapeHtml(item.student_name)}</b> vừa nộp bài <b>${escapeHtml(item.problem_id)}</b>
                            </div>
                            <div class="assignment-meta-row" style="margin-top:4px;">
                                <span>Kết quả: <b>${item.score}/${item.total_tests}</b></span>
                                <span class="difficulty-badge ${item.status === 'AC' ? 'easy' : 'hard'}" style="padding:1px 6px; font-size:0.75rem;">${item.status}</span>
                                <span>🕒 ${new Date(item.submitted_at).toLocaleString('vi-VN')}</span>
                            </div>
                        </div>
                        <button class="btn-secondary" style="padding:4px 10px; font-size:0.8rem;" onclick="viewSubmissionDetail('${escapeHtml(item.student_name)}', '${escapeHtml(item.problem_id)}', ${JSON.stringify(item.code || '').replace(/"/g, '&quot;')}, ${item.score}, ${item.total_tests}, '${item.status}', ${JSON.stringify(item.ai_feedback || '').replace(/"/g, '&quot;')}, '${item.submitted_at}')">
                            🔍 Xem Code & AI
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (e) {
        pane.innerHTML = `<div style="color: #ef4444; padding: 20px;">Lỗi: ${e.message}</div>`;
    }
}

// ---- STUDENT CLASSROOM WORKSPACE ----

async function renderStudentClassroom(body) {
    try {
        const res = await apiGet('/api/classroom/student/my-class');
        if (!res.has_class) {
            body.innerHTML = `
                <div class="student-join-hero">
                    <div class="hero-icon">🏫</div>
                    <h2 style="font-size: 1.4rem; color: var(--text-primary); margin-bottom: 8px;">Tham Gia Lớp Học Của Bạn</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 24px;">
                        Nhập mã lớp do Thầy/Cô cung cấp (Ví dụ: <code>HSG839</code>, <code>TIN12A</code>) để nhận bài tập riêng và được AI Mentor cùng Thầy Cô đồng hành!
                    </p>
                    <div class="form-group">
                        <input type="text" id="input-join-class-code" class="class-code-input-lg" placeholder="HSG..." maxlength="10">
                    </div>
                    <button class="btn-primary" id="btn-submit-join-class" style="padding: 14px; font-size: 1rem;">
                        🚀 Vào Lớp Học Ngay
                    </button>
                </div>
            `;
            document.getElementById('btn-submit-join-class').addEventListener('click', handleJoinClass);
            return;
        }

        const cls = res.class;
        studentClass = cls;

        body.innerHTML = `
            <div class="class-banner-card">
                <div class="class-banner-top">
                    <div>
                        <div class="class-title-tag">
                            <span>🏫 ${escapeHtml(cls.class_name)}</span>
                        </div>
                        <div style="color: var(--text-muted); font-size: 0.9rem; margin-top: 4px;">
                            👨‍🏫 Giáo viên phụ trách: <b style="color: #fff;">${escapeHtml(cls.teacher_name)}</b>
                        </div>
                    </div>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div class="class-code-badge-wrap" title="Mã lớp">
                            <span style="font-size:0.85rem; color:var(--text-muted);">Mã lớp:</span>
                            <span class="class-code-text">${cls.class_code}</span>
                        </div>
                        <button class="btn-danger" id="btn-leave-class" style="padding:6px 12px; font-size:0.8rem;" title="Rời khỏi lớp học này">
                            Rời lớp
                        </button>
                    </div>
                </div>
            </div>

            <div style="margin-top: 10px;">
                <h3 style="font-size: 1.15rem; color: var(--text-primary); margin-bottom: 14px;">
                    📝 Bài Tập Được Giáo Viên Giao Cho Lớp
                </h3>
                <div class="assignments-list-container" id="student-assignments-list">
                    <div style="text-align:center; padding: 20px; color: var(--text-muted);">⏳ Đang tải bài tập...</div>
                </div>
            </div>
        `;

        document.getElementById('btn-leave-class').addEventListener('click', handleLeaveClass);

        // Load assignments
        loadStudentAssignmentsList();

    } catch (e) {
        body.innerHTML = `<div style="color: #ef4444; padding: 20px;">Lỗi tải lớp học: ${e.message}</div>`;
    }
}

async function loadStudentAssignmentsList() {
    const container = document.getElementById('student-assignments-list');
    try {
        const res = await apiGet('/api/classroom/student/assignments');
        const assignments = res.assignments || [];

        if (assignments.length === 0) {
            container.innerHTML = `
                <div class="folder-placeholder" style="padding: 30px; text-align: center;">
                    🎉 Hiện tại Thầy/Cô chưa giao bài tập mới nào. Hãy tiếp tục luyện thi 8 chặng HSG nhé!
                </div>
            `;
            return;
        }

        container.innerHTML = assignments.map(a => {
            const isAc = a.has_submitted && a.status === 'AC';
            const isWa = a.has_submitted && a.status !== 'AC';
            const isExpired = a.deadline && new Date(a.deadline) < new Date();

            let statusHtml = '<span style="color:var(--text-muted);">⭕ Chưa làm</span>';
            if (isAc) {
                statusHtml = `<span style="color:#10b981; font-weight:700;">✅ Đã nộp: ${a.score}/${a.total_tests} AC</span>`;
            } else if (isWa) {
                statusHtml = `<span style="color:#f59e0b; font-weight:700;">⚠️ Đã nộp: ${a.score}/${a.total_tests} (Chưa hoàn thành)</span>`;
            }

            const deadlineBadge = a.deadline 
                ? `<span class="deadline-badge ${isExpired ? 'deadline-expired' : 'deadline-active'}">
                    ${isExpired ? 'Đã hết hạn' : 'Hạn: ' + new Date(a.deadline).toLocaleString('vi-VN')}
                   </span>`
                : `<span class="deadline-badge deadline-active">Không giới hạn</span>`;

            return `
                <div class="assignment-card">
                    <div class="assignment-main-info">
                        <div class="assignment-card-title">
                            <span>${escapeHtml(a.title)}</span>
                            ${deadlineBadge}
                        </div>
                        <div class="assignment-meta-row">
                            <span>${statusHtml}</span>
                            <span>⏱️ ${a.time_limit || 1.0}s/test</span>
                            <span>🧪 ${a.test_case_count || 1} Tests</span>
                        </div>
                    </div>
                    <button class="btn-primary" style="width:auto; padding:8px 20px; margin:0;" onclick="openAssignmentProblem(${JSON.stringify(a).replace(/"/g, '&quot;')})">
                        🚀 Làm Bài Ngay
                    </button>
                </div>
            `;
        }).join('');

    } catch (e) {
        container.innerHTML = `<div style="color: #ef4444; padding: 15px;">Lỗi: ${e.message}</div>`;
    }
}

async function handleJoinClass() {
    const input = document.getElementById('input-join-class-code');
    const code = input.value.trim().toUpperCase();
    if (!code) {
        alert("Vui lòng nhập mã lớp.");
        return;
    }

    try {
        await apiPost('/api/classroom/student/join', { class_code: code });
        showToast('🎉 Đã tham gia lớp học thành công!');
        openClassroomModal();
        renderSidebar();
    } catch (e) {
        alert("Lỗi tham gia lớp: " + e.message);
    }
}

async function handleLeaveClass() {
    if (!confirm("Bạn có chắc chắn muốn rời khỏi lớp học này?")) return;
    try {
        await apiPost('/api/classroom/student/leave', {});
        showToast('Đã rời khỏi lớp học.');
        openClassroomModal();
        renderSidebar();
    } catch (e) {
        alert("Lỗi: " + e.message);
    }
}

// ---- CODE & AI MENTOR INSPECTION MODAL ----

function viewSubmissionDetail(studentName, problemId, code, score, totalTests, status, aiFeedback, submittedAt) {
    document.getElementById('submission-viewer-title').textContent = `Bài nộp: ${problemId}`;
    document.getElementById('submission-viewer-meta').textContent = `Học sinh: ${studentName} • Điểm: ${score}/${totalTests} (${status}) • Lúc: ${new Date(submittedAt).toLocaleString('vi-VN')}`;
    const body = document.getElementById('submission-viewer-body');

    body.innerHTML = `
        <div style="margin-bottom: 12px; display:flex; justify-content:space-between; align-items:center;">
            <h4 style="margin:0; color:var(--text-primary); font-size:0.95rem;">💻 Mã nguồn (Code) đã nộp:</h4>
        </div>
        <div class="code-viewer-box">
            <button class="copy-code-float-btn" id="btn-copy-submitted-code">Sao chép</button>
            <code>${escapeHtml(code || '')}</code>
        </div>

        <h4 style="margin:20px 0 8px; color:var(--accent-secondary); font-size:0.95rem;">🤖 Nhận xét từ AI Mentor:</h4>
        <div class="ai-critique-box">
            ${aiFeedback ? renderMarkdown(aiFeedback) : '<p style="color:var(--text-muted);margin:0;">Chưa có nhận xét từ AI cho bài này.</p>'}
        </div>
    `;

    document.getElementById('btn-copy-submitted-code').addEventListener('click', () => {
        navigator.clipboard.writeText(code || '');
        showToast('📋 Đã sao chép mã nguồn!');
    });

    renderMath(body);
    openModal('modal-submission-detail');
}
