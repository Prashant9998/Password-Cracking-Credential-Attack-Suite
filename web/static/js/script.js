// Password Cracking Suite - Frontend JavaScript

// Tab Navigation
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.getAttribute('data-tab');
        
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Remove active class from all buttons
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('border-red-500', 'text-white');
            b.classList.add('border-transparent', 'text-gray-400');
        });
        
        // Show selected tab
        document.getElementById(tabName).classList.add('active');
        
        // Add active class to clicked button
        btn.classList.remove('border-transparent', 'text-gray-400');
        btn.classList.add('border-red-500', 'text-white');
    });
});

// Hash Identification
document.getElementById('identifyBtn').addEventListener('click', async () => {
    const hash = document.getElementById('hashInput').value.trim();
    
    if (!hash) {
        showError('Please enter a hash string');
        return;
    }
    
    try {
        const response = await fetch('/api/identify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ hash })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('resultHashType').textContent = data.type;
            document.getElementById('resultHash').textContent = data.hash;
            document.getElementById('identifyResult').classList.remove('hidden');
            showSuccess('Hash identified successfully!');
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Error identifying hash: ' + error.message);
    }
});

// Wordlist Generation
document.getElementById('generateBtn').addEventListener('click', async () => {
    const name = document.getElementById('nameInput').value.trim();
    const dob = document.getElementById('dobInput').value.trim();
    const keywordsStr = document.getElementById('keywordsInput').value.trim();
    const keywords = keywordsStr ? keywordsStr.split(',').map(k => k.trim()) : [];
    
    if (!name && !dob && !keywords.length) {
        showError('Please enter at least one piece of information');
        return;
    }
    
    try {
        const response = await fetch('/api/generate-wordlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, dob, keywords })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('wordlistCount').textContent = data.count;
            document.getElementById('wordlistOutput').value = data.wordlist.join('\n');
            document.getElementById('wordlistResult').classList.remove('hidden');
            showSuccess(`Wordlist generated with ${data.count} words!`);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Error generating wordlist: ' + error.message);
    }
});

// Copy Wordlist to Clipboard
document.getElementById('copyWordlistBtn').addEventListener('click', () => {
    const textarea = document.getElementById('wordlistOutput');
    textarea.select();
    document.execCommand('copy');
    showSuccess('Wordlist copied to clipboard!');
});

// Attack Type Selection
document.getElementById('attackTypeSelect').addEventListener('change', (e) => {
    const isDictionary = e.target.value === 'dictionary';
    document.getElementById('dictionaryOptions').classList.toggle('hidden', !isDictionary);
    document.getElementById('bruteForceOptions').classList.toggle('hidden', isDictionary);
});

// Wordlist Source Selection
document.getElementById('wordlistSourceSelect').addEventListener('change', (e) => {
    const isGenerate = e.target.value === 'generate';
    document.getElementById('generateFromDataOptions').classList.toggle('hidden', !isGenerate);
    document.getElementById('uploadFileOptions').classList.toggle('hidden', isGenerate);
});

// Run Attack
document.getElementById('attackBtn').addEventListener('click', async () => {
    const hash = document.getElementById('attackHashInput').value.trim();
    const attackType = document.getElementById('attackTypeSelect').value;
    
    if (!hash) {
        showError('Please enter a target hash');
        return;
    }
    
    document.getElementById('attackProgress').classList.remove('hidden');
    document.getElementById('attackResult').classList.add('hidden');
    
    try {
        const payload = {
            hash,
            type: attackType
        };
        
        if (attackType === 'dictionary') {
            const wordlistSource = document.getElementById('wordlistSourceSelect').value;
            
            if (wordlistSource === 'generate') {
                payload.name = document.getElementById('attackNameInput').value.trim();
                payload.dob = document.getElementById('attackDobInput').value.trim();
                const keywordsStr = document.getElementById('attackKeywordsInput').value.trim();
                payload.keywords = keywordsStr ? keywordsStr.split(',').map(k => k.trim()) : [];
            } else {
                const fileInput = document.getElementById('wordlistFileInput');
                if (!fileInput.files.length) {
                    showError('Please select a wordlist file');
                    document.getElementById('attackProgress').classList.add('hidden');
                    return;
                }
                const text = await fileInput.files[0].text();
                payload.wordlist = text.split('\n').map(w => w.trim()).filter(w => w);
            }
            
            payload.use_mutations = document.getElementById('mutateCheckbox').checked;
        } else {
            payload.max_length = parseInt(document.getElementById('maxLengthInput').value);
            const charsetSelect = document.getElementById('charsetSelect').value;
            if (charsetSelect) {
                payload.charset = charsetSelect;
            }
        }
        
        const response = await fetch('/api/attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        document.getElementById('attackProgress').classList.add('hidden');
        
        if (data.success) {
            displayAttackResult(data);
            showSuccess('Attack completed!');
        } else {
            showError(data.error);
        }
    } catch (error) {
        document.getElementById('attackProgress').classList.add('hidden');
        showError('Error running attack: ' + error.message);
    }
});

// Display Attack Result
function displayAttackResult(data) {
    const resultDiv = document.getElementById('attackResult');
    const status = data.password ? 'Password Found!' : 'Password Not Found';
    const statusColor = data.password ? 'text-green-400' : 'text-red-400';
    
    document.getElementById('resultStatus').textContent = status;
    document.getElementById('resultStatus').className = statusColor;
    document.getElementById('resultAttackHashType').textContent = data.hash_type;
    
    if (data.password) {
        document.getElementById('resultPassword').textContent = data.password;
        document.getElementById('passwordFoundDiv').classList.remove('hidden');
        
        if (data.strength) {
            document.getElementById('resultScore').textContent = data.strength.score;
            document.getElementById('resultEntropy').textContent = data.strength.entropy + ' bits';
            document.getElementById('resultCrackTime').textContent = data.strength.crack_times_display.offline_fast_hashing_1e10_per_second;
            document.getElementById('strengthAnalysis').classList.remove('hidden');
        }
    } else {
        document.getElementById('passwordFoundDiv').classList.add('hidden');
        document.getElementById('strengthAnalysis').classList.add('hidden');
    }
    
    resultDiv.classList.remove('hidden');
}

// Reports Management
document.getElementById('refreshReportsBtn').addEventListener('click', loadReports);

async function loadReports() {
    try {
        const response = await fetch('/api/reports');
        const data = await response.json();
        
        const reportsList = document.getElementById('reportsList');
        
        if (!data.success) {
            reportsList.innerHTML = '<p class="text-red-400">Error loading reports</p>';
            return;
        }
        
        if (data.reports.length === 0) {
            reportsList.innerHTML = '<p class="text-gray-400">No reports generated yet</p>';
            return;
        }
        
        reportsList.innerHTML = data.reports.map(report => `
            <div class="report-item bg-gray-700 rounded-lg p-4 border border-gray-600 flex justify-between items-center">
                <div class="flex-1">
                    <p class="text-white font-semibold">${report}</p>
                    <p class="text-gray-400 text-sm">${report.endsWith('.pdf') ? 'PDF Report' : 'Text Report'}</p>
                </div>
                <button onclick="downloadReport('${report}')" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition">
                    <i class="fas fa-download"></i> Download
                </button>
            </div>
        `).join('');
    } catch (error) {
        document.getElementById('reportsList').innerHTML = '<p class="text-red-400">Error loading reports: ' + error.message + '</p>';
    }
}

// Download Report
function downloadReport(filename) {
    window.location.href = `/api/download-report/${filename}`;
}

// Notification Functions
function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = type === 'success' ? 'success-message' : 'error-message';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        animation: slideIn 0.3s ease-in-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Load reports on page load
window.addEventListener('load', () => {
    loadReports();
});
