// TAB NAVIGATION SYSTEM
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        // Update button states
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update content visibility
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        document.getElementById(tabName).classList.add('active');

        lucide.createIcons();
    });
});

document.getElementById('runButton').addEventListener('click', async () => {
    const topic = document.getElementById('topicInput').value.trim();
    const notes = document.getElementById('notesInput').value.trim();
    const difficulty = document.getElementById('difficultyLevel').value;
    const studyTime = document.getElementById('studyTime').value;

    if (!topic) {
        alert("⚠️ Please enter a study topic");
        return;
    }

    const btn = document.getElementById('runButton');
    const landing = document.getElementById('landingHero');
    const dashboard = document.getElementById('studyDashboard');
    const telemetry = document.getElementById('telemetryLog');
    const statusText = document.getElementById('currentStatus');
    const activeAgentDisp = document.getElementById('activeAgent');

    const now = new Date().toLocaleString();
    document.getElementById('createdDate').textContent = now;
    document.getElementById('studyDuration').textContent = studyTime;
    document.getElementById('difficultyTag').textContent = difficulty;
    btn.disabled = true;
    btn.innerHTML = '<span class="status-pulse"></span> Orchestrating Agents...';

    landing.classList.add('hidden');
    dashboard.classList.remove('hidden');
    document.getElementById('downloadPdfBtn').classList.remove('hidden');
    document.getElementById('newSessionBtn').classList.remove('hidden');

    telemetry.innerHTML = `<div class="log-line">> MISSION INITIATED: ${topic.toUpperCase()}</div>`;
    telemetry.innerHTML += `<div class="log-line">> DIFFICULTY: ${difficulty}</div>`;
    telemetry.innerHTML += `<div class="log-line">> DEPLOYING: Multi-Agent Fleet...</div>`;

    statusText.textContent = "🚀 Agent Fleet Active";
    activeAgentDisp.textContent = "Coordinating...";

    // Reset all output areas
    document.querySelectorAll('.markdown-body').forEach(body => {
        body.innerHTML = '<p class="placeholder-text">⏳ Processing...</p>';
    });

    try {
        const response = await fetch('http://localhost:8081/generate-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic, notes })
        });

        if (!response.ok) throw new Error("API connection failed");

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let fullReport = "";
        let memoryData = "";
        let inFinalReport = false;
        let inMemory = false;

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });

            // Check for final report marker
            if (chunk.includes("[FINAL_REPORT]")) {
                inFinalReport = true;
                inMemory = false;
                const parts = chunk.split("[FINAL_REPORT]");
                if (parts[0]) processLogs(parts[0], telemetry, activeAgentDisp);
                fullReport = parts[1] || "";
                updateSections(fullReport);
                continue;
            }

            // Check for memory summary marker
            if (chunk.includes("[MEMORY_SUMMARY]")) {
                inMemory = true;
                inFinalReport = false;
                const parts = chunk.split("[MEMORY_SUMMARY]");
                if (parts[0] && !inFinalReport) processLogs(parts[0], telemetry, activeAgentDisp);
                memoryData = parts[1] || "";
                updateMemoryDisplay(memoryData);
                continue;
            }

            // Accumulate data
            if (inFinalReport) {
                fullReport += chunk;
                updateSections(fullReport);
            } else if (inMemory) {
                memoryData += chunk;
                updateMemoryDisplay(memoryData);
            } else {
                processLogs(chunk, telemetry, activeAgentDisp);
            }
        }

        // Success state
        statusText.textContent = "✅ Mission Complete";
        activeAgentDisp.textContent = "Fleet Idle";

        // Store in local storage
        saveToHistory(topic, fullReport, difficulty, studyTime);

    } catch (error) {
        telemetry.innerHTML += `<div class="log-line" style="color:#f44336">> ❌ ERROR: ${error.message}</div>`;
        statusText.textContent = "❌ System Error";
        activeAgentDisp.textContent = "Failed";
    } finally {
        btn.disabled = false;
        btn.innerHTML = '🚀 Generate Smart Study Plan';
        lucide.createIcons();
    }
});

// FILE UPLOAD HANDLER
document.getElementById('fileUpload').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const statusSpan = document.getElementById('uploadStatus');
    statusSpan.textContent = `⏳ Uploading ${file.name}...`;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:8081/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.text) {
            document.getElementById('notesInput').value = data.text;
            statusSpan.textContent = `✅ ${file.name} loaded`;
            statusSpan.style.color = "#4caf50";
            setTimeout(() => {
                statusSpan.textContent = "Upload Documents (PDF/DOC/PPT/TXT)";
                statusSpan.style.color = "";
            }, 3000);
        } else {
            statusSpan.textContent = `❌ Upload failed`;
            statusSpan.style.color = "#f44336";
        }
    } catch (error) {
        statusSpan.textContent = `❌ Error: ${error.message}`;
        statusSpan.style.color = "#f44336";
    }
});


// LOG PROCESSING
function processLogs(chunk, telemetryEl, agentEl) {
    const lines = chunk.split('\n');
    lines.forEach(line => {
        if (!line.trim()) return;

        const logEntry = document.createElement('div');
        logEntry.className = 'log-line';
        logEntry.textContent = `> ${line.trim()}`;
        telemetryEl.appendChild(logEntry);

        // Extract agent name
        if (line.includes("Agent:")) {
            const agentName = line.split("Agent:")[1].trim();
            agentEl.textContent = agentName;
        }

        telemetryEl.scrollTop = telemetryEl.scrollHeight;
    });
}

function updateSections(markdown) {
    const sections = {
        summaryOutput: [/^#\s*High-Yield Content Analysis/im, /^#\s*Content Analysis/im],
        scheduleOutput: [/^#\s*Optimized Roadmap/im, /^#\s*Study Roadmap/im],
        quizOutput: [/^#\s*Active Recall Assessment/im, /^#\s*Practice Questions/im],
        resourcesOutput: [/^#\s*External Resource Vault/im, /^#\s*Recommended Resources/im],
        evaluationOutput: [/^#\s*Performance Forecasting/im, /^#\s*Performance Analysis/im]
    };

    // Robust splitting: matches newline before header OR start of string before header
    // But split() logic with lookaheads can be tricky.
    // Simpler: Split by newlines, identify header lines, rebuild blocks.

    const lines = markdown.split('\n');
    let currentSection = null;
    let sectionContent = {};

    // Initialize standard keys
    Object.keys(sections).forEach(k => sectionContent[k] = []);
    let defaultaccumulator = [];

    lines.forEach(line => {
        let isHeader = false;
        if (line.match(/^#+\s+/)) {
            // Check if this header matches any known section
            for (const [key, regexes] of Object.entries(sections)) {
                if (regexes.some(r => r.test(line))) {
                    currentSection = key;
                    isHeader = true;
                    break;
                }
            }
        }

        if (isHeader) {
            // It's a header line, start valid section
            // We include the header in the content so Markdown renders it as H1/H2
            if (currentSection) {
                sectionContent[currentSection].push(line);
            }
        } else {
            // Content line
            if (currentSection) {
                sectionContent[currentSection].push(line);
            } else {
                defaultaccumulator.push(line);
            }
        }
    });

    // Render each section
    for (const [key, lines] of Object.entries(sectionContent)) {
        if (lines.length > 0) {
            const el = document.getElementById(key);
            if (el) {
                el.innerHTML = marked.parse(lines.join('\n'));
            }
        }
    }

    // Handle content before first header (usually empty or intro)
    if (defaultaccumulator.length > 0 && !sectionContent['summaryOutput'].length) {
        const summaryEl = document.getElementById('summaryOutput');
        if (summaryEl && summaryEl.innerHTML.includes('Processing')) {
            summaryEl.innerHTML = marked.parse(defaultaccumulator.join('\n'));
        }
    }

    // ENHANCE UI & FORMULAS
    enhanceUI();
    if (window.MathJax) MathJax.typesetPromise();
}

function enhanceUI() {
    document.querySelectorAll('.markdown-body a').forEach(a => {
        a.target = "_blank";
        a.classList.add('resource-link');
        if (!a.innerHTML.includes('external-link')) {
            a.innerHTML = `<i data-lucide="external-link" style="width:14px;display:inline;margin-right:4px;"></i>${a.innerHTML}`;
        }
    });
    document.querySelectorAll('.markdown-body table').forEach(t => t.classList.add('styled-table'));
    lucide.createIcons();
}

// UPDATE MEMORY DISPLAY
function updateMemoryDisplay(memoryText) {
    const memoryEl = document.getElementById('memoryDisplay');
    if (memoryEl && memoryText.trim()) {
        memoryEl.innerHTML = `<pre>${memoryText}</pre>`;
    }
}

// SAVE TO LOCAL HISTORY
function saveToHistory(topic, report, difficulty, studyTime) {
    const history = JSON.parse(localStorage.getItem('studyHistory') || '[]');
    const entry = {
        topic,
        report,
        difficulty,
        studyTime,
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString()
    };

    history.unshift(entry);
    localStorage.setItem('studyHistory', JSON.stringify(history.slice(0, 10)));
    loadHistory();
}

function loadHistory() {
    const history = JSON.parse(localStorage.getItem('studyHistory') || '[]');
    const historyEl = document.getElementById('sessionHistory');

    if (history.length === 0) {
        historyEl.innerHTML = '<p class="placeholder-text">No previous sessions</p>';
        return;
    }

    historyEl.innerHTML = history.map((session, idx) => `
        <div class="history-item" onclick="loadSession(${idx})">
            <strong>${session.topic}</strong>
            <span>${session.date} ${session.time}</span>
        </div>
    `).join('');
}

window.loadSession = function (idx) {
    const history = JSON.parse(localStorage.getItem('studyHistory') || '[]');
    const session = history[idx];
    if (session) {
        document.getElementById('landingHero').classList.add('hidden');
        document.getElementById('studyDashboard').classList.remove('hidden');
        document.getElementById('topicInput').value = session.topic;
        updateSections(session.report);
        document.getElementById('difficultyTag').textContent = session.difficulty;
        document.getElementById('studyDuration').textContent = session.studyTime;
    }
};

// POMODORO TIMER
let pomoInterval;
let pomoTime = 1500;
let pomoRunning = false;

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

document.getElementById('startPomo')?.addEventListener('click', () => {
    if (pomoRunning) return;
    pomoRunning = true;

    pomoInterval = setInterval(() => {
        pomoTime--;
        document.getElementById('pomoTimer').textContent = formatTime(pomoTime);

        if (pomoTime <= 0) {
            clearInterval(pomoInterval);
            alert("⏰ Pomodoro session complete!");
            pomoTime = parseInt(document.getElementById('timerMode').value) * 60;
            document.getElementById('pomoTimer').textContent = formatTime(pomoTime);
            pomoRunning = false;
        }
    }, 1000);
});

document.getElementById('pausePomo')?.addEventListener('click', () => {
    clearInterval(pomoInterval);
    pomoRunning = false;
});

document.getElementById('resetPomo')?.addEventListener('click', () => {
    clearInterval(pomoInterval);
    pomoRunning = false;
    const mode = parseInt(document.getElementById('timerMode').value);
    pomoTime = mode * 60;
    document.getElementById('pomoTimer').textContent = formatTime(pomoTime);
});

document.getElementById('timerMode')?.addEventListener('change', (e) => {
    const mode = parseInt(e.target.value);
    pomoTime = mode * 60;
    document.getElementById('pomoTimer').textContent = formatTime(pomoTime);
});

// QUICK NOTES
document.getElementById('saveNote')?.addEventListener('click', () => {
    const note = document.getElementById('quickNotes').value.trim();
    if (!note) return;

    const notes = JSON.parse(localStorage.getItem('quickNotes') || '[]');
    notes.unshift({ text: note, date: new Date().toLocaleString() });
    localStorage.setItem('quickNotes', JSON.stringify(notes.slice(0, 20)));

    document.getElementById('quickNotes').value = '';
    displaySavedNotes();
});

function displaySavedNotes() {
    const notes = JSON.parse(localStorage.getItem('quickNotes') || '[]');
    const container = document.getElementById('savedNotes');

    if (!container) return;

    if (notes.length === 0) {
        container.innerHTML = '<p class="placeholder-text">No saved notes</p>';
        return;
    }

    container.innerHTML = notes.slice(0, 5).map(note => `
        <div class="note-item">
            <p>${note.text}</p>
            <small>${note.date}</small>
        </div>
    `).join('');
}

// GOALS SYSTEM
document.getElementById('addGoal')?.addEventListener('click', () => {
    const goal = document.getElementById('goalInput').value.trim();
    if (!goal) return;

    const goals = JSON.parse(localStorage.getItem('studyGoals') || '[]');
    goals.push({ text: goal, completed: false, date: new Date().toLocaleDateString() });
    localStorage.setItem('studyGoals', JSON.stringify(goals));

    document.getElementById('goalInput').value = '';
    displayGoals();
});

function displayGoals() {
    const goals = JSON.parse(localStorage.getItem('studyGoals') || '[]');
    const container = document.getElementById('goalsList');

    if (!container) return;

    if (goals.length === 0) {
        container.innerHTML = '<li class="placeholder-text">No goals set</li>';
        return;
    }

    container.innerHTML = goals.map((goal, idx) => `
        <li>
            <input type="checkbox" ${goal.completed ? 'checked' : ''} onchange="toggleGoal(${idx})">
            <span style="${goal.completed ? 'text-decoration:line-through;opacity:0.6' : ''}">${goal.text}</span>
        </li>
    `).join('');
}

window.toggleGoal = function (idx) {
    const goals = JSON.parse(localStorage.getItem('studyGoals') || '[]');
    goals[idx].completed = !goals[idx].completed;
    localStorage.setItem('studyGoals', JSON.stringify(goals));
    displayGoals();
};

// ======================
// CONFIDENCE SLIDER
// ======================
document.getElementById('confidenceSlider')?.addEventListener('input', (e) => {
    const value = e.target.value;
    document.getElementById('confidenceValue').textContent = value;
    document.getElementById('confidenceBar').style.width = `${value}%`;
});

// ======================
// PDF EXPORT
// ======================
document.getElementById('downloadPdfBtn')?.addEventListener('click', () => {
    const topic = document.getElementById('topicInput').value || 'Study_Plan';
    const element = document.getElementById('studyDashboard');

    const opt = {
        margin: [0.5, 0.5],
        filename: `SmartStudy_${topic.replace(/\s+/g, '_')}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };

    html2pdf().set(opt).from(element).save();
});

// ======================
// NEW SESSION BUTTON
// ======================
document.getElementById('newSessionBtn')?.addEventListener('click', () => {
    if (confirm("Start a new study session? Current progress will be saved to history.")) {
        document.getElementById('landingHero').classList.remove('hidden');
        document.getElementById('studyDashboard').classList.add('hidden');
        document.getElementById('topicInput').value = '';
        document.getElementById('notesInput').value = '';
        document.getElementById('currentStatus').textContent = 'System Ready';
        document.getElementById('activeAgent').textContent = 'Idle';
        document.getElementById('telemetryLog').innerHTML = '<div class="log-line">> System reset. Ready for mission...</div>';
    }
});

// ======================
// SIDEBAR TOGGLE
// ======================
document.getElementById('sidebarToggle')?.addEventListener('click', () => {
    const sidebar = document.querySelector('.sidebar');
    const main = document.querySelector('.main-content');
    const icon = document.querySelector('#sidebarToggle i');

    sidebar.classList.toggle('collapsed');
    main.classList.toggle('expanded');

    if (sidebar.classList.contains('collapsed')) {
        icon.setAttribute('data-lucide', 'panel-left-open');
    } else {
        icon.setAttribute('data-lucide', 'panel-left-close');
    }
    lucide.createIcons();
});

// ======================
// INITIALIZATION
// ======================
window.addEventListener('DOMContentLoaded', () => {
    loadHistory();
    displaySavedNotes();
    displayGoals();
    lucide.createIcons();
});
