// ServiceFlowEngine — SolPunk Design System JavaScript
// Handles timers, photo uploads, and chat functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize chat functionality if present
    if (document.getElementById('chatMessages')) {
        initializeChat();
    }

    // Initialize form validations
    initializeFormValidation();

    // Initialize photo previews
    initializePhotoPreview();
}

// Chat functionality
function initializeChat() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendChatBtn');
    const chatMessages = document.getElementById('chatMessages');

    if (!chatInput || !sendButton || !chatMessages) return;

    sendButton.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });
}

function sendChatMessage() {
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendButton = document.getElementById('sendChatBtn');

    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message to chat
    addChatMessage(message, 'user');
    chatInput.value = '';

    // Show loading state
    sendButton.innerHTML = '\u23F3';
    sendButton.disabled = true;

    // Send to API
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        addChatMessage(data.message, 'ai');
    })
    .catch(error => {
        console.error('Chat error:', error);
        addChatMessage('Sorry, I encountered an error. Please try again.', 'ai');
    })
    .finally(() => {
        // Restore button state
        sendButton.innerHTML = '\u25B6';
        sendButton.disabled = false;
    });
}

function addChatMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'sp-chat-msg ' + sender;

    if (sender === 'user') {
        div.innerHTML = '<div class="sp-chat-avatar user">\uD83D\uDC64</div><div class="sp-chat-bubble user">' + escapeHtml(message) + '</div>';
    } else {
        div.innerHTML = '<div class="sp-chat-avatar ai">\uD83E\uDD16</div><div class="sp-chat-bubble">' + escapeHtml(message) + '</div>';
    }

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
    });
}

// Photo preview functionality
function initializePhotoPreview() {
    const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                previewImageGeneric(file, input);
            }
        });
    });
}

function previewImageGeneric(file, input) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const inputId = input.id;
        let previewContainer = document.getElementById(inputId + '_preview');
        let previewImg = document.getElementById(inputId + '_img');

        if (!previewContainer) {
            previewContainer = document.createElement('div');
            previewContainer.id = inputId + '_preview';
            previewContainer.className = 'sp-photo-preview';
            previewContainer.style.display = 'none';

            previewImg = document.createElement('img');
            previewImg.id = inputId + '_img';
            previewImg.style.maxHeight = '200px';
            previewImg.style.borderRadius = '10px';
            previewImg.style.border = '1px solid rgba(180,100,255,0.15)';
            previewImg.alt = 'Photo preview';

            previewContainer.appendChild(previewImg);
            input.parentNode.appendChild(previewContainer);
        }

        previewImg.src = e.target.result;
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Timer functionality for task pages
let taskTimer = null;
let startTime = null;

function startTaskTimer(estimatedMinutes) {
    startTime = new Date();
    taskTimer = setInterval(() => updateTimer(estimatedMinutes), 1000);
}

function stopTaskTimer() {
    if (taskTimer) {
        clearInterval(taskTimer);
        taskTimer = null;
    }
}

function updateTimer(estimatedMinutes) {
    if (!startTime) return;

    const now = new Date();
    const elapsed = Math.floor((now - startTime) / 1000);
    const elapsedMinutes = Math.floor(elapsed / 60);

    const hours = Math.floor(elapsed / 3600);
    const minutes = Math.floor((elapsed % 3600) / 60);
    const seconds = elapsed % 60;

    const timeString = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');

    const timerDisplays = document.querySelectorAll('#timer-display, #timer-display-running');
    timerDisplays.forEach(display => {
        if (display) display.textContent = timeString;
    });

    if (elapsedMinutes > estimatedMinutes) {
        const overtimeAlerts = document.querySelectorAll('#overtime-alert, #overtime-alert-running');
        overtimeAlerts.forEach(alert => {
            if (alert) alert.style.display = 'flex';
        });
    }

    const actualMinutesInput = document.getElementById('actual_minutes');
    if (actualMinutesInput) {
        actualMinutesInput.value = Math.max(elapsedMinutes, 1);
    }
}

// Photo comparison slider functionality
function initializePhotoComparison() {
    const comparisons = document.querySelectorAll('.photo-comparison-container');

    comparisons.forEach(container => {
        let isResizing = false;

        const slider = container.querySelector('.photo-comparison-slider');
        const afterDiv = container.querySelector('.photo-comparison-after');

        if (!slider || !afterDiv) return;

        slider.addEventListener('mousedown', startResize);
        document.addEventListener('mousemove', doResize);
        document.addEventListener('mouseup', stopResize);

        slider.addEventListener('touchstart', startResize);
        document.addEventListener('touchmove', doResize);
        document.addEventListener('touchend', stopResize);

        function startResize(e) {
            isResizing = true;
            e.preventDefault();
        }

        function doResize(e) {
            if (!isResizing) return;
            const rect = container.getBoundingClientRect();
            const x = (e.type.includes('touch') ? e.touches[0].clientX : e.clientX) - rect.left;
            const percentage = Math.min(Math.max(x / rect.width * 100, 0), 100);
            afterDiv.style.width = percentage + '%';
            slider.style.left = percentage + '%';
        }

        function stopResize() {
            isResizing = false;
        }

        container.addEventListener('click', function(e) {
            if (e.target === slider) return;
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const percentage = Math.min(Math.max(x / rect.width * 100, 0), 100);
            afterDiv.style.width = percentage + '%';
            slider.style.left = percentage + '%';
        });
    });
}

// Utility functions
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + secs.toString().padStart(2, '0');
}

function showLoading(button, text) {
    text = text || 'Processing...';
    if (button) {
        button.innerHTML = '\u23F3 ' + text;
        button.disabled = true;
    }
}

function hideLoading(button, originalText) {
    originalText = originalText || 'Submit';
    if (button) {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// Initialize photo comparison on page load
document.addEventListener('DOMContentLoaded', function() {
    initializePhotoComparison();
});
