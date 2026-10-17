// KaamSaathi AI - Unified Client Application Controller
const App = {
  state: {
    currentTab: 'assistant',
    language: 'en',
    workerRole: 'Food Delivery',
    activeDocContext: null,
    activeEarningContext: null,
    apiKeyConfigured: false,
    editingEarningId: null
  },

  init() {
    this.bindEvents();
    this.detectLanguagePreference();
    this.checkSystemStatus();
    this.loadEarnings();
    this.loadSafetyGuide();
    this.loadWelfareSchemes();
    this.applyTranslations();
  },

  // --- HTML Entity Escaping for XSS Prevention ---
  escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  },

  formatMarkdown(text) {
    if (!text) return '';

    // Split into lines for block-level processing
    const lines = text.split('\n');
    const outputBlocks = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];

      // --- Fenced code blocks (``` ... ```) ---
      if (line.trim().startsWith('```')) {
        const codeLines = [];
        i++;
        while (i < lines.length && !lines[i].trim().startsWith('```')) {
          codeLines.push(this.escapeHtml(lines[i]));
          i++;
        }
        i++; // skip closing ```
        outputBlocks.push('<pre style="background:var(--bg-tertiary,#1e1e2e);color:var(--text-primary,#cdd6f4);padding:0.85rem 1rem;border-radius:8px;overflow-x:auto;font-size:0.85rem;margin:0.5rem 0;"><code>' + codeLines.join('\n') + '</code></pre>');
        continue;
      }

      // --- Horizontal rule ---
      if (/^[-*_]{3,}\s*$/.test(line.trim())) {
        outputBlocks.push('<hr style="border:none;border-top:1px solid var(--border-color,#e2e8f0);margin:0.75rem 0;">');
        i++;
        continue;
      }

      // --- Headers (# to ####) ---
      const headerMatch = line.match(/^(#{1,4})\s+(.+)$/);
      if (headerMatch) {
        const level = headerMatch[1].length;
        const sizes = { 1: '1.4rem', 2: '1.2rem', 3: '1.05rem', 4: '0.95rem' };
        const content = this._inlineMd(this.escapeHtml(headerMatch[2]));
        outputBlocks.push('<div style="font-size:' + sizes[level] + ';font-weight:700;margin:0.6rem 0 0.35rem 0;line-height:1.4;">' + content + '</div>');
        i++;
        continue;
      }

      // --- Blockquote (> ...) ---
      if (line.trim().startsWith('> ')) {
        const quoteLines = [];
        while (i < lines.length && lines[i].trim().startsWith('> ')) {
          quoteLines.push(this.escapeHtml(lines[i].trim().slice(2)));
          i++;
        }
        outputBlocks.push('<blockquote style="border-left:3px solid var(--primary,#6366f1);padding:0.4rem 0.8rem;margin:0.5rem 0;color:var(--text-secondary,#94a3b8);font-style:italic;">' + quoteLines.map(l => this._inlineMd(l)).join('<br>') + '</blockquote>');
        continue;
      }

      // --- Unordered list (- or * at start) ---
      if (/^\s*[-*]\s+/.test(line)) {
        const listItems = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
          const itemText = lines[i].replace(/^\s*[-*]\s+/, '');
          listItems.push('<li style="margin-bottom:0.3rem;">' + this._inlineMd(this.escapeHtml(itemText)) + '</li>');
          i++;
        }
        outputBlocks.push('<ul style="margin:0.4rem 0 0.4rem 1.2rem;padding:0;list-style:disc;">' + listItems.join('') + '</ul>');
        continue;
      }

      // --- Ordered list (1. 2. etc.) ---
      if (/^\s*\d+[.)]\s+/.test(line)) {
        const listItems = [];
        while (i < lines.length && /^\s*\d+[.)]\s+/.test(lines[i])) {
          const itemText = lines[i].replace(/^\s*\d+[.)]\s+/, '');
          listItems.push('<li style="margin-bottom:0.3rem;">' + this._inlineMd(this.escapeHtml(itemText)) + '</li>');
          i++;
        }
        outputBlocks.push('<ol style="margin:0.4rem 0 0.4rem 1.2rem;padding:0;">' + listItems.join('') + '</ol>');
        continue;
      }

      // --- Empty line spacer ---
      if (line.trim() === '') {
        outputBlocks.push('<div style="height:0.4rem;"></div>');
        i++;
        continue;
      }

      // --- Regular paragraph ---
      outputBlocks.push('<p style="margin:0.25rem 0;line-height:1.6;">' + this._inlineMd(this.escapeHtml(line)) + '</p>');
      i++;
    }

    return outputBlocks.join('');
  },

  // Process inline markdown tokens (bold, italic, code, links)
  _inlineMd(safe) {
    return safe
      // Bold-italic (***text***)
      .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
      // Bold (**text**)
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      // Italic (*text*)
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      // Inline code (`text`)
      .replace(/`([^`]+)`/g, '<code style="background:var(--bg-tertiary,#f1f5f9);padding:0.1rem 0.35rem;border-radius:4px;font-size:0.88em;">$1</code>')
      // Links [text](url)
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color:var(--primary,#6366f1);text-decoration:underline;">$1</a>');
  },

  // --- Translation & Language ---
  detectLanguagePreference() {
    const saved = localStorage.getItem('kaamsaathi_lang');
    if (saved && (saved === 'hi' || saved === 'en')) {
      this.state.language = saved;
      document.getElementById('langSelect').value = saved;
    }
  },

  setLanguage(lang) {
    this.state.language = lang;
    localStorage.setItem('kaamsaathi_lang', lang);
    this.applyTranslations();
    this.loadSafetyGuide();
    this.showToast(lang === 'hi' ? 'भाषा बदलकर हिंदी कर दी गई है' : 'Language set to English', 'info');
  },

  t(key) {
    const dict = I18N[this.state.language] || I18N.en;
    return dict[key] || I18N.en[key] || key;
  },

  applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (key) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.placeholder = this.t(key);
        } else {
          el.textContent = this.t(key);
        }
      }
    });
  },

  // --- Navigation & Workflow Switching ---
  navigate(tabName, context = null) {
    this.state.currentTab = tabName;
    
    // Update Sidebar & Mobile Nav active states
    document.querySelectorAll('.nav-item, .mobile-nav-item').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });

    // Show/hide sections
    document.querySelectorAll('.tab-content').forEach(sec => {
      sec.style.display = sec.id === `tab-${tabName}` ? 'block' : 'none';
    });

    // Handle deep-linked context
    if (tabName === 'grievance' && context && context.earning) {
      this.populateGrievanceFromEarning(context.earning);
    } else if (tabName === 'assistant' && context && context.prompt) {
      document.getElementById('chatInput').value = context.prompt;
      this.sendChatMessage(context.prompt, context.data);
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  // --- Toast Notifications ---
  showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  },

  // --- System Status & Live Connection Verification ---
  async checkSystemStatus() {
    try {
      const res = await fetch('/api/ai/status');
      const data = await res.json();
      this.state.apiKeyConfigured = data.api_key_configured;
      this.state.modelVerified = data.model_verified;
      
      const banner = document.getElementById('apiKeyBanner');
      if (banner) {
        banner.style.display = data.api_key_configured ? 'none' : 'flex';
      }
      
      const statusBadge = document.getElementById('systemStatusBadge');
      if (statusBadge) {
        if (data.model_verified) {
          const timeStr = data.last_verified_at ? ` (${data.last_verified_at.split('T')[1].substr(0, 5)} UTC)` : '';
          statusBadge.textContent = `AI: Verified (${data.model_name})${timeStr}`;
          statusBadge.className = 'badge badge-success';
        } else if (data.api_key_configured) {
          statusBadge.textContent = 'AI: Key Configured (Unverified)';
          statusBadge.className = 'badge badge-warning';
        } else {
          statusBadge.textContent = 'AI: Key Not Configured';
          statusBadge.className = 'badge badge-danger';
        }
      }

      const settingsKeyBadge = document.getElementById('settingsKeyStatus');
      if (settingsKeyBadge) {
        settingsKeyBadge.textContent = data.api_key_configured ? 'Configured (Server Env)' : 'Not Set';
        settingsKeyBadge.className = data.api_key_configured ? 'badge badge-success' : 'badge badge-warning';
      }

      const settingsModelBadge = document.getElementById('settingsModelStatus');
      if (settingsModelBadge) {
        if (data.model_verified) {
          settingsModelBadge.textContent = `Verified Live (${data.model_name})`;
          settingsModelBadge.className = 'badge badge-success';
        } else if (data.api_key_configured) {
          settingsModelBadge.textContent = 'Unverified (Run Test Below)';
          settingsModelBadge.className = 'badge badge-warning';
        } else {
          settingsModelBadge.textContent = 'Unavailable (No Key)';
          settingsModelBadge.className = 'badge badge-danger';
        }
      }

      const settingsDbBadge = document.getElementById('settingsDbStatus');
      if (settingsDbBadge) {
        settingsDbBadge.textContent = data.database_connected ? 'Connected' : 'Unavailable';
        settingsDbBadge.className = data.database_connected ? 'badge badge-success' : 'badge badge-danger';
      }
    } catch (err) {
      console.error('Status check failed:', err);
    }
  },

  async testAiConnection() {
    const btn = document.getElementById('btnTestConnection');
    const resultBox = document.getElementById('testConnectionResult');
    btn.disabled = true;
    btn.textContent = 'Testing connection to Gemini 3.8 Flash...';
    resultBox.style.display = 'block';
    resultBox.innerHTML = '<span style="color: var(--text-muted);">Making live call to Gemini 3.8 Flash API...</span>';

    try {
      const res = await fetch('/api/ai/test-connection', { method: 'POST' });
      const data = await res.json();

      if (data.verified) {
        resultBox.innerHTML = `
          <div class="badge badge-success" style="padding: 0.5rem; width: 100%; text-align: left; margin-top: 0.5rem;">
            ✅ <strong>Verified Live!</strong> Connected to <code>${this.escapeHtml(data.model)}</code> in ${data.latency_ms}ms.<br>
            <span style="font-size: 0.775rem;">${this.escapeHtml(data.message)}</span>
          </div>
        `;
        this.showToast('Gemini 3.8 Flash connection verified!', 'success');
      } else {
        resultBox.innerHTML = `
          <div class="badge badge-danger" style="padding: 0.5rem; width: 100%; text-align: left; margin-top: 0.5rem;">
            ❌ <strong>Connection Unsuccessful:</strong> ${this.escapeHtml(data.error || 'Unknown error')}<br>
            <span style="font-size: 0.775rem;">Set GEMINI_API_KEY in server environment / Cloud Run secrets.</span>
          </div>
        `;
        this.showToast('Model verification failed', 'error');
      }
      // Re-check system status to update UI badges honestly
      this.checkSystemStatus();
    } catch (err) {
      resultBox.innerHTML = `
        <div class="badge badge-danger" style="padding: 0.5rem; width: 100%; text-align: left;">
          ❌ Network error connecting to backend API: ${this.escapeHtml(err.message)}
        </div>
      `;
    } finally {
      btn.disabled = false;
      btn.textContent = '⚡ Re-test Live Gemini Connection';
    }
  },

  // --- MODULE A: AI Assistant ---
  async sendChatMessage(customText = null, customContext = null) {
    const input = document.getElementById('chatInput');
    const text = customText || input.value.trim();
    if (!text) return;

    if (!customText) input.value = '';

    // Append User Message Bubble (safely escaped)
    this.appendChatBubble('user', text);

    // Typing pulse indicator
    const typingId = this.appendChatBubble('assistant', '...', true);

    try {
      const payload = {
        message: text,
        language: this.state.language,
        context_data: customContext || (this.state.activeDocContext ? { document_analysis: this.state.activeDocContext } : null)
      };

      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      const bubble = document.getElementById(typingId);
      if (!bubble) return;

      // Honest Error Handling: Never treat HTTP error as a successful AI reply
      if (!res.ok) {
        const errorDetail = data && data.detail 
          ? data.detail 
          : (this.state.language.startsWith('hi') ? 'AI सेवा उपलब्ध नहीं है। कृपया पुनः प्रयास करें।' : 'AI service is temporarily unavailable. Please try again.');
        
        bubble.className = 'chat-bubble error';
        bubble.style.background = '#fef2f2';
        bubble.style.border = '1px solid #f87171';
        bubble.style.color = '#991b1b';
        bubble.innerHTML = `
          <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
            <span style="font-size: 1.1rem;">⚠️</span>
            <div>
              <strong>${this.state.language.startsWith('hi') ? 'अनुरोध विफल रहा' : 'Request Failed'}</strong>
              <div style="font-size: 0.85rem; margin-top: 0.25rem;">${this.escapeHtml(errorDetail)}</div>
            </div>
          </div>
        `;
        
        const retryBtn = document.createElement('button');
        retryBtn.className = 'btn btn-sm btn-outline';
        retryBtn.style.marginTop = '0.65rem';
        retryBtn.style.fontSize = '0.75rem';
        retryBtn.textContent = this.state.language.startsWith('hi') ? 'पुनः प्रयास करें 🔄' : 'Retry 🔄';
        retryBtn.addEventListener('click', () => {
          bubble.remove();
          App.sendChatMessage(text, customContext);
        });
        bubble.appendChild(retryBtn);
        this.scrollChatBottom();
        return;
      }

      // Success branch: genuine model response
      bubble.innerHTML = this.formatMarkdown(data.reply);
      
      // Suggested action buttons (routing to earnings/grievance)
      if (data.suggested_actions && data.suggested_actions.length > 0) {
        const actionRow = document.createElement('div');
        actionRow.style.marginTop = '0.75rem';
        actionRow.style.display = 'flex';
        actionRow.style.gap = '0.5rem';
        actionRow.style.flexWrap = 'wrap';

        data.suggested_actions.forEach(act => {
          const btn = document.createElement('button');
          btn.className = 'btn btn-sm btn-secondary';
          btn.textContent = act.text;
          btn.addEventListener('click', () => {
            if (act.action === 'navigate_earnings') App.navigate('earnings');
            else if (act.action === 'navigate_safety') App.navigate('safety');
            else if (act.action === 'navigate_welfare') App.navigate('welfare');
            else if (act.action === 'navigate_document') App.navigate('documents');
            else if (act.action === 'navigate_grievance') App.navigate('grievance');
            else if (act.action === 'open_settings') App.openModal('settingsModal');
          });
          actionRow.appendChild(btn);
        });
        bubble.appendChild(actionRow);
      }

      // Voice Readout Button for Accessibility
      const speakBtn = document.createElement('button');
      speakBtn.className = 'btn btn-sm btn-outline';
      speakBtn.style.marginTop = '0.5rem';
      speakBtn.innerHTML = '🔊 Read Aloud';
      speakBtn.addEventListener('click', () => App.speakText(data.reply));
      bubble.appendChild(speakBtn);

    } catch (err) {
      const bubble = document.getElementById(typingId);
      if (bubble) {
        bubble.className = 'chat-bubble error';
        bubble.style.background = '#fef2f2';
        bubble.style.border = '1px solid #f87171';
        bubble.style.color = '#991b1b';
        bubble.innerHTML = `
          <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
            <span style="font-size: 1.1rem;">⚠️</span>
            <div>
              <strong>${this.state.language.startsWith('hi') ? 'नेटवर्क त्रुटि' : 'Network Error'}</strong>
              <div style="font-size: 0.85rem; margin-top: 0.25rem;">${this.state.language.startsWith('hi') ? 'सर्वर से संपर्क करने में समस्या हुई। कृपया इंटरनेट जांचें।' : 'Could not contact the server. Please check your connection.'}</div>
            </div>
          </div>
        `;
        const retryBtn = document.createElement('button');
        retryBtn.className = 'btn btn-sm btn-outline';
        retryBtn.style.marginTop = '0.65rem';
        retryBtn.style.fontSize = '0.75rem';
        retryBtn.textContent = this.state.language.startsWith('hi') ? 'पुनः प्रयास करें 🔄' : 'Retry 🔄';
        retryBtn.addEventListener('click', () => {
          bubble.remove();
          App.sendChatMessage(text, customContext);
        });
        bubble.appendChild(retryBtn);
      }
    }

    this.scrollChatBottom();
  },

  appendChatBubble(role, content, isTyping = false) {
    const container = document.getElementById('chatMessages');
    const id = `bubble-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`;
    const bubble = document.createElement('div');
    bubble.id = id;
    bubble.className = `chat-bubble ${role}`;
    if (isTyping) {
      bubble.innerHTML = '<span class="typing-indicator">Analyzing with Gemini 3.8 Flash...</span>';
    } else {
      bubble.innerHTML = this.formatMarkdown(content);
    }
    container.appendChild(bubble);
    this.scrollChatBottom();
    return id;
  },

  scrollChatBottom() {
    const container = document.getElementById('chatMessages');
    container.scrollTop = container.scrollHeight;
  },

  // Web Speech API Voice Recognition & Speech Synthesis
  startVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      this.showToast('Voice speech recognition not supported in this browser. Please use Chrome.', 'warning');
      return;
    }
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognizer = new SpeechRec();
    recognizer.lang = this.state.language.startsWith('hi') ? 'hi-IN' : 'en-IN';
    recognizer.interimResults = false;

    const micBtn = document.getElementById('micBtn');
    micBtn.classList.add('btn-danger');
    micBtn.innerHTML = '🔴 Listening...';

    recognizer.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      document.getElementById('chatInput').value = transcript;
      App.sendChatMessage();
    };

    recognizer.onerror = (e) => {
      console.error(e);
      App.showToast('Voice input error or permission denied', 'error');
    };

    recognizer.onend = () => {
      micBtn.classList.remove('btn-danger');
      micBtn.innerHTML = '🎤';
    };

    recognizer.start();
  },

  speakText(text) {
    if (!('speechSynthesis' in window)) {
      this.showToast('Speech synthesis not supported in this browser', 'warning');
      return;
    }
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*_#`]/g, '').replace(/<[^>]*>/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = this.state.language.startsWith('hi') ? 'hi-IN' : 'en-IN';
    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  },

  // --- MODULE B: Earnings Tracker ---
  async loadEarnings() {
    try {
      // 1. Fetch summary (scoped to session)
      const sumRes = await fetch('/api/earnings/summary');
      if (sumRes.ok) {
        const sumData = await sumRes.json();
        document.getElementById('statToday').textContent = `₹${sumData.today.total_net.toFixed(2)}`;
        document.getElementById('statTodayGross').textContent = `Gross: ₹${sumData.today.total_gross} | Exp: ₹${sumData.today.total_expenses}`;

        document.getElementById('statWeek').textContent = `₹${sumData.this_week.total_net.toFixed(2)}`;
        document.getElementById('statWeekGross').textContent = `Gross: ₹${sumData.this_week.total_gross} | Exp: ₹${sumData.this_week.total_expenses}`;

        document.getElementById('statMonth').textContent = `₹${sumData.this_month.total_net.toFixed(2)}`;
        document.getElementById('statMonthGross').textContent = `Gross: ₹${sumData.this_month.total_gross} | Exp: ₹${sumData.this_month.total_expenses}`;

        document.getElementById('statAllTime').textContent = `₹${sumData.all_time.total_net.toFixed(2)}`;
        document.getElementById('statAllTimeCount').textContent = `${sumData.all_time.entry_count} total entries logged`;
      }

      // 2. Fetch list (scoped to session)
      const listRes = await fetch('/api/earnings');
      if (listRes.ok) {
        const list = await listRes.json();
        this.renderEarningsTable(list);
      }
    } catch (e) {
      console.error('Failed to load earnings:', e);
    }
  },

  renderEarningsTable(records) {
    const tbody = document.getElementById('earningsTableBody');
    const emptyState = document.getElementById('earningsEmptyState');
    tbody.innerHTML = '';

    if (!records || records.length === 0) {
      emptyState.style.display = 'block';
      document.getElementById('earningsTableContainer').style.display = 'none';
      return;
    }

    emptyState.style.display = 'none';
    document.getElementById('earningsTableContainer').style.display = 'block';

    records.forEach(r => {
      const tr = document.createElement('tr');

      const tdDate = document.createElement('td');
      const strongDate = document.createElement('strong');
      strongDate.textContent = r.date;
      tdDate.appendChild(strongDate);
      tr.appendChild(tdDate);

      const tdCat = document.createElement('td');
      const spanCat = document.createElement('span');
      spanCat.className = 'badge badge-secondary';
      spanCat.textContent = r.category;
      tdCat.appendChild(spanCat);
      tr.appendChild(tdCat);

      const tdPlat = document.createElement('td');
      tdPlat.textContent = r.platform;
      tr.appendChild(tdPlat);

      const tdGross = document.createElement('td');
      tdGross.textContent = `₹${Number(r.gross_earnings).toFixed(2)}`;
      tr.appendChild(tdGross);

      const tdTips = document.createElement('td');
      tdTips.style.color = 'var(--success)';
      tdTips.textContent = `+₹${Number(r.tips_incentives).toFixed(2)}`;
      tr.appendChild(tdTips);

      const tdExp = document.createElement('td');
      tdExp.style.color = 'var(--danger)';
      tdExp.textContent = `-₹${Number(r.expenses).toFixed(2)}`;
      tr.appendChild(tdExp);

      const tdNet = document.createElement('td');
      const strongNet = document.createElement('strong');
      strongNet.style.color = 'var(--primary)';
      strongNet.textContent = `₹${Number(r.net_earnings).toFixed(2)}`;
      tdNet.appendChild(strongNet);
      tr.appendChild(tdNet);

      const tdActions = document.createElement('td');
      const actionDiv = document.createElement('div');
      actionDiv.style.display = 'flex';
      actionDiv.style.gap = '0.35rem';

      const disputeBtn = document.createElement('button');
      disputeBtn.className = 'btn btn-sm btn-outline';
      disputeBtn.textContent = '⚖️ Dispute';
      disputeBtn.title = 'Dispute this entry in Grievance module';
      disputeBtn.addEventListener('click', () => App.disputeEarning(r));

      const editBtn = document.createElement('button');
      editBtn.className = 'btn btn-sm btn-outline';
      editBtn.textContent = '✏️';
      editBtn.title = 'Edit entry';
      editBtn.addEventListener('click', () => App.editEarning(r));

      const delBtn = document.createElement('button');
      delBtn.className = 'btn btn-sm btn-danger';
      delBtn.textContent = '🗑️';
      delBtn.title = 'Delete entry';
      delBtn.addEventListener('click', () => App.deleteEarning(r.id));

      actionDiv.appendChild(disputeBtn);
      actionDiv.appendChild(editBtn);
      actionDiv.appendChild(delBtn);
      tdActions.appendChild(actionDiv);
      tr.appendChild(tdActions);

      tbody.appendChild(tr);
    });
  },

  openAddEarningModal() {
    this.state.editingEarningId = null;
    document.getElementById('earningModalTitle').textContent = this.t('add_entry');
    document.getElementById('earningForm').reset();
    document.getElementById('earningDate').value = new Date().toISOString().split('T')[0];
    this.openModal('earningModal');
  },

  editEarning(record) {
    this.state.editingEarningId = record.id;
    document.getElementById('earningModalTitle').textContent = 'Edit Earning Record';
    document.getElementById('earningDate').value = record.date;
    document.getElementById('earningCategory').value = record.category;
    document.getElementById('earningPlatform').value = record.platform;
    document.getElementById('earningGross').value = record.gross_earnings;
    document.getElementById('earningTips').value = record.tips_incentives;
    document.getElementById('earningExpenses').value = record.expenses;
    document.getElementById('earningNotes').value = record.notes || '';
    this.openModal('earningModal');
  },

  async saveEarning() {
    const payload = {
      date: document.getElementById('earningDate').value,
      category: document.getElementById('earningCategory').value,
      platform: document.getElementById('earningPlatform').value.trim() || 'General',
      gross_earnings: parseFloat(document.getElementById('earningGross').value) || 0,
      tips_incentives: parseFloat(document.getElementById('earningTips').value) || 0,
      expenses: parseFloat(document.getElementById('earningExpenses').value) || 0,
      notes: document.getElementById('earningNotes').value.trim()
    };

    if (!payload.date) {
      this.showToast('Please select a valid date', 'error');
      return;
    }

    try {
      const isEdit = this.state.editingEarningId !== null;
      const url = isEdit ? `/api/earnings/${this.state.editingEarningId}` : '/api/earnings';
      const method = isEdit ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        this.showToast(isEdit ? 'Earning record updated!' : 'Earning record saved!', 'success');
        this.closeModal('earningModal');
        this.loadEarnings();
      } else {
        const err = await res.json();
        this.showToast(err.detail || 'Failed to save earning', 'error');
      }
    } catch (e) {
      this.showToast('Network error while saving earning', 'error');
    }
  },

  async deleteEarning(id) {
    if (!confirm('Are you sure you want to delete this earning entry?')) return;
    try {
      const res = await fetch(`/api/earnings/${id}`, { method: 'DELETE' });
      if (res.ok) {
        this.showToast('Record deleted', 'info');
        this.loadEarnings();
      } else {
        const err = await res.json();
        this.showToast(err.detail || 'Failed to delete entry', 'error');
      }
    } catch (e) {
      this.showToast('Failed to delete', 'error');
    }
  },

  // JOURNEY 1: Explain My Earnings with AI
  async explainEarningsWithAi() {
    this.showToast('Generating AI explanation of your real recorded earnings with Gemini 3.8 Flash...', 'info');
    try {
      const res = await fetch('/api/ai/explain-earnings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: this.state.language })
      });
      const data = await res.json();

      if (!res.ok) {
        this.showToast(data.detail || 'AI explanation error', 'error');
        return;
      }

      document.getElementById('earningsExplanationText').innerHTML = this.formatMarkdown(data.explanation);
      this.openModal('earningsExplanationModal');
    } catch (e) {
      this.showToast('Error explaining earnings with AI', 'error');
    }
  },

  // JOURNEY 2: Navigate from Earnings Discrepancy to Grievance Assistant
  disputeEarning(earning) {
    this.navigate('grievance', { earning: earning });
  },

  populateGrievanceFromEarning(earning) {
    document.getElementById('grievanceCategory').value = 'Missing incentives or payment discrepancies';
    document.getElementById('grievanceEmployer').value = earning.platform;
    document.getElementById('grievanceDate').value = earning.date;
    document.getElementById('grievanceAmount').value = earning.gross_earnings;
    document.getElementById('grievanceDetails').value = `Discrepancy identified in recorded earnings for ${earning.date} on ${earning.platform}. Recorded gross was ₹${earning.gross_earnings}, but payout differed. Notes: ${earning.notes || 'None'}`;
    this.state.activeEarningContext = earning;
    
    const banner = document.getElementById('linkedEarningBanner');
    banner.style.display = 'block';
    banner.textContent = `🔗 Linked with Earnings Record #${earning.id} (${earning.platform} - ₹${earning.gross_earnings})`;
    
    this.showToast('Earnings details populated into Grievance Drafter!', 'success');
  },

  // --- MODULE C: Safety Guidance ---
  async loadSafetyGuide(category = null) {
    const cat = category || this.state.workerRole;
    try {
      const res = await fetch(`/api/safety/${encodeURIComponent(cat)}`);
      const data = await res.json();
      
      const titleEl = document.getElementById('safetyCategoryTitle');
      titleEl.textContent = this.state.language.startsWith('hi') ? data.title_hi : data.title;

      // Render Emergency Numbers safely
      const sosGrid = document.getElementById('safetySosGrid');
      sosGrid.innerHTML = '';
      data.emergency_numbers.forEach(em => {
        const div = document.createElement('div');
        div.className = 'sos-card';
        
        const infoDiv = document.createElement('div');
        const svcDiv = document.createElement('div');
        svcDiv.style.fontWeight = '700';
        svcDiv.style.fontSize = '0.9rem';
        svcDiv.textContent = this.state.language.startsWith('hi') ? em.service_hi : em.service;
        
        const subDiv = document.createElement('div');
        subDiv.style.fontSize = '0.75rem';
        subDiv.style.color = 'var(--text-muted)';
        subDiv.textContent = 'Instant Emergency Support';
        infoDiv.appendChild(svcDiv);
        infoDiv.appendChild(subDiv);

        const callLink = document.createElement('a');
        callLink.className = 'btn btn-sm btn-danger';
        callLink.style.fontWeight = '800';
        callLink.href = `tel:${em.number.split('/')[0].trim()}`;
        callLink.textContent = `📞 ${em.number}`;

        div.appendChild(infoDiv);
        div.appendChild(callLink);
        sosGrid.appendChild(div);
      });

      // Render Checklist Topics safely
      const topicContainer = document.getElementById('safetyTopicsContainer');
      topicContainer.innerHTML = '';
      data.categories.forEach((catItem, idx) => {
        const topicCard = document.createElement('div');
        topicCard.className = 'card';
        const topicTitle = this.state.language.startsWith('hi') ? catItem.topic_hi : catItem.topic;
        const checkList = this.state.language.startsWith('hi') ? catItem.checkpoints_hi : catItem.checkpoints;

        const titleDiv = document.createElement('div');
        titleDiv.className = 'card-title';
        titleDiv.textContent = `🛡️ ${topicTitle}`;
        topicCard.appendChild(titleDiv);

        const listDiv = document.createElement('div');
        listDiv.style.marginTop = '0.75rem';

        checkList.forEach((pt, pIdx) => {
          const checkKey = `safety_${cat}_${idx}_${pIdx}`;
          const isChecked = localStorage.getItem(checkKey) === 'true';

          const label = document.createElement('label');
          label.style.display = 'flex';
          label.style.alignItems = 'flex-start';
          label.style.gap = '0.65rem';
          label.style.marginBottom = '0.6rem';
          label.style.cursor = 'pointer';
          label.style.fontSize = '0.925rem';

          const chk = document.createElement('input');
          chk.type = 'checkbox';
          chk.checked = isChecked;
          chk.style.marginTop = '0.25rem';
          chk.style.accentColor = 'var(--primary)';
          chk.addEventListener('change', () => localStorage.setItem(checkKey, chk.checked));

          const span = document.createElement('span');
          span.textContent = pt;

          label.appendChild(chk);
          label.appendChild(span);
          listDiv.appendChild(label);
        });

        topicCard.appendChild(listDiv);

        const actionDiv = document.createElement('div');
        actionDiv.style.marginTop = '0.5rem';
        actionDiv.style.textAlign = 'right';

        const aiBtn = document.createElement('button');
        aiBtn.className = 'btn btn-sm btn-outline';
        aiBtn.textContent = 'Ask AI About This Topic 🤖';
        aiBtn.addEventListener('click', () => App.askAiSafety(topicTitle));
        actionDiv.appendChild(aiBtn);
        topicCard.appendChild(actionDiv);

        topicContainer.appendChild(topicCard);
      });
    } catch (e) {
      console.error('Failed to load safety guide:', e);
    }
  },

  // JOURNEY 5: Contextual Safety AI Advice
  askAiSafety(topic) {
    const prompt = this.state.language.startsWith('hi')
      ? `मुझे '${topic}' के बारे में व्यावहारिक सुरक्षा टिप्स और दिशा-निर्देश बताएं।`
      : `Provide me with practical, step-by-step safety guidance regarding '${topic}'.`;
    this.navigate('assistant', { prompt: prompt });
  },

  // --- MODULE D: Welfare & Rights Explorer ---
  async loadWelfareSchemes() {
    const cat = document.getElementById('welfareCatFilter').value;
    const loc = document.getElementById('welfareLocFilter').value;
    const query = document.getElementById('welfareSearchInput').value.trim();

    let url = '/api/welfare?';
    if (cat && cat !== 'All') url += `category=${encodeURIComponent(cat)}&`;
    if (loc && loc !== 'All') url += `location=${encodeURIComponent(loc)}&`;
    if (query) url += `query=${encodeURIComponent(query)}&`;

    try {
      const res = await fetch(url);
      const schemes = await res.json();
      this.renderWelfareCards(schemes);
    } catch (e) {
      console.error('Failed to load schemes:', e);
    }
  },

  renderWelfareCards(schemes) {
    const container = document.getElementById('welfareCardsContainer');
    container.innerHTML = '';

    if (!schemes || schemes.length === 0) {
      container.innerHTML = `
        <div class="card" style="text-align: center; padding: 2rem;">
          <p style="color: var(--text-muted);">No schemes found matching the selected filters. Try broadening your criteria.</p>
        </div>
      `;
      return;
    }

    schemes.forEach(s => {
      const card = document.createElement('div');
      card.className = 'card';
      const name = this.state.language.startsWith('hi') && s.name_hi ? s.name_hi : s.name;
      const benefits = this.state.language.startsWith('hi') && s.benefits_hi ? s.benefits_hi : s.benefits;

      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 0.5rem; flex-wrap: wrap;">
          <div>
            <div class="card-title" style="margin-bottom: 0.25rem;">🏛️ ${this.escapeHtml(name)}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted);">${this.escapeHtml(s.authority)}</div>
          </div>
          <div style="display: flex; gap: 0.35rem;">
            <span class="badge badge-primary">${this.escapeHtml(s.location)}</span>
          </div>
        </div>

        <div style="margin: 0.85rem 0; font-size: 0.925rem; line-height: 1.5;">
          <strong>Benefits:</strong> ${this.escapeHtml(benefits)}
        </div>

        <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.75rem;">
          <div><strong>Eligibility:</strong> ${this.escapeHtml(s.eligibility_criteria)}</div>
          <div style="margin-top: 0.25rem;"><strong>Required:</strong> ${this.escapeHtml(s.documents_required.join(', '))}</div>
          <div style="margin-top: 0.25rem; font-size: 0.75rem;"><em>Source: ${this.escapeHtml(s.source)} (Verified: ${this.escapeHtml(s.last_verified)})</em></div>
        </div>

        <div class="welfare-footer" style="display: flex; gap: 0.5rem; justify-content: space-between; align-items: center; flex-wrap: wrap; border-top: 1px solid var(--border-color); padding-top: 0.75rem;">
          <a href="${this.escapeHtml(s.official_url)}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline">
            🌐 Official Portal (${this.escapeHtml(s.contact_helpline || 'Website')})
          </a>
        </div>
      `;

      // Attach AI Explain button safely
      const footer = card.querySelector('.welfare-footer');
      const aiBtn = document.createElement('button');
      aiBtn.className = 'btn btn-sm btn-secondary';
      aiBtn.textContent = '🤖 Explain with AI';
      aiBtn.addEventListener('click', () => App.explainSchemeWithAi(s));
      footer.appendChild(aiBtn);

      container.appendChild(card);
    });
  },

  // JOURNEY 4: Explain Scheme Requirements in AI Chat
  explainSchemeWithAi(scheme) {
    const prompt = this.state.language.startsWith('hi')
      ? `मुझे '${scheme.name_hi || scheme.name}' योजना के बारे में विस्तार से बताएं। इसके लिए कौन से कागजात चाहिए और मैं आवेदन कैसे कर सकता हूं?`
      : `Explain the '${scheme.name}' welfare scheme to me. What are the key eligibility conditions and steps to apply?`;
    this.navigate('assistant', { prompt: prompt, data: { scheme: scheme } });
  },

  // --- MODULE E: Document Assistant ---
  async analyzeDocumentText() {
    const text = document.getElementById('docPasteInput').value.trim();
    if (!text) {
      this.showToast('Please paste document text to analyze', 'warning');
      return;
    }

    const btn = document.getElementById('btnAnalyzeDoc');
    btn.disabled = true;
    btn.textContent = 'Analyzing Document with Gemini 3.8 Flash...';

    try {
      const res = await fetch('/api/documents/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          document_text: text,
          document_type: 'Pasted Document',
          language: this.state.language
        })
      });
      const data = await res.json();
      if (res.ok) {
        this.renderDocumentAnalysis(data);
        this.showToast('Document analyzed successfully with Gemini 3.8 Flash!', 'success');
      } else {
        this.showToast(data.detail || 'Failed to analyze document', 'error');
      }
    } catch (e) {
      this.showToast('Failed to contact document analysis service', 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = this.t('analyze_btn');
    }
  },

  async uploadDocumentFile(file) {
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      this.showToast('File too large. Maximum supported size is 5 MB.', 'error');
      return;
    }

    const btn = document.getElementById('btnUploadDoc');
    btn.disabled = true;
    btn.textContent = 'Extracting & Analyzing with Gemini...';

    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', this.state.language);

    try {
      const res = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      if (res.ok) {
        this.renderDocumentAnalysis(data.analysis);
        this.showToast(`Analyzed ${file.name} successfully with Gemini 3.8 Flash!`, 'success');
      } else {
        this.showToast(data.detail || 'Failed to read document', 'error');
      }
    } catch (e) {
      this.showToast('Network error during file upload', 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = 'Analyze Uploaded File';
    }
  },

  renderDocumentAnalysis(analysis) {
    this.state.activeDocContext = analysis;
    const resultBox = document.getElementById('docAnalysisResult');
    resultBox.style.display = 'block';

    document.getElementById('docSummaryText').textContent = analysis.summary;

    const fillList = (elId, items) => {
      const el = document.getElementById(elId);
      el.innerHTML = '';
      if (!items || items.length === 0) {
        const li = document.createElement('li');
        li.style.color = 'var(--text-muted)';
        li.textContent = 'None detected in document text.';
        el.appendChild(li);
      } else {
        items.forEach(it => {
          const li = document.createElement('li');
          li.textContent = it;
          el.appendChild(li);
        });
      }
    };

    fillList('docAmountsList', analysis.key_amounts);
    fillList('docDatesList', analysis.important_dates);
    fillList('docConditionsList', analysis.conditions_and_clauses);
    fillList('docMissingList', analysis.missing_info_checklist);

    // Render recommended questions with interactive "Ask in Chat" action
    const questionsEl = document.getElementById('docQuestionsList');
    questionsEl.innerHTML = '';
    const qItems = analysis.questions_to_ask || [];
    if (qItems.length === 0) {
      const li = document.createElement('li');
      li.style.color = 'var(--text-muted)';
      li.textContent = 'None detected in document text.';
      questionsEl.appendChild(li);
    } else {
      qItems.forEach(q => {
        const li = document.createElement('li');
        li.style.marginBottom = '0.5rem';
        
        const span = document.createElement('span');
        span.textContent = q;
        li.appendChild(span);

        const askBtn = document.createElement('button');
        askBtn.className = 'btn btn-sm btn-outline';
        askBtn.style.padding = '0.15rem 0.5rem';
        askBtn.style.fontSize = '0.75rem';
        askBtn.style.marginLeft = '0.5rem';
        askBtn.textContent = 'Ask Support in Chat 💬';
        askBtn.addEventListener('click', () => {
          const prompt = App.state.language.startsWith('hi')
            ? `मेरे दस्तावेज़ के आधार पर सपोर्ट से यह प्रश्न कैसे पूछूं: "${q}"? कृपया एक संक्षिप्त और विनम्र संदेश का मसौदा तैयार करें।`
            : `Based on my document, how should I ask support: "${q}"? Please draft a concise and polite message I can send them.`;
          App.navigate('assistant', { prompt: prompt, data: { document_summary: App.state.activeDocContext ? App.state.activeDocContext.summary : '' } });
        });
        li.appendChild(askBtn);
        questionsEl.appendChild(li);
      });
    }

    document.getElementById('docDisclaimerText').textContent = analysis.disclaimer;
    resultBox.scrollIntoView({ behavior: 'smooth' });
  },

  // JOURNEY 3: Ask Follow-up Questions in AI Chat about Document
  askAiAboutCurrentDoc() {
    if (!this.state.activeDocContext) return;
    const prompt = this.state.language.startsWith('hi')
      ? `मैंने जो दस्तावेज़ अपलोड किया है, उसके बारे में मुझे और जानकारी चाहिए। इसमें क्या जोखिम या छिपी हुई शर्तें हैं?`
      : `I have a follow-up question regarding the document I just analyzed. What potential risks or conditions should I look out for?`;
    this.navigate('assistant', { prompt: prompt, data: { document_summary: this.state.activeDocContext.summary } });
  },

  // --- MODULE F: Grievance & Dispute Drafting ---
  async generateGrievanceDraft() {
    const category = document.getElementById('grievanceCategory').value;
    const employer = document.getElementById('grievanceEmployer').value.trim();
    const date = document.getElementById('grievanceDate').value;
    const amountVal = document.getElementById('grievanceAmount').value;
    const amount = amountVal ? parseFloat(amountVal) : null;
    const details = document.getElementById('grievanceDetails').value.trim();
    const evidence = document.getElementById('grievanceEvidence').value.trim();

    if (!employer || !details) {
      this.showToast('Please enter platform name and details of incident', 'warning');
      return;
    }

    const btn = document.getElementById('btnGenerateDraft');
    btn.disabled = true;
    btn.textContent = 'Generating with Gemini 3.8 Flash...';

    const payload = {
      category: category,
      employer_platform: employer,
      incident_date: date || new Date().toISOString().split('T')[0],
      amount_disputed: amount,
      incident_details: details,
      evidence_available: evidence,
      language: this.state.language,
      linked_earning_id: this.state.activeEarningContext ? this.state.activeEarningContext.id : null
    };

    try {
      const res = await fetch('/api/grievances/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      
      if (res.ok) {
        this.renderGrievanceDraft(data);
        this.showToast('Grievance draft generated with Gemini 3.8 Flash!', 'success');
      } else {
        this.showToast(data.detail || 'Failed to generate draft', 'error');
      }
    } catch (e) {
      this.showToast('Failed to contact grievance generation service', 'error');
    } finally {
      btn.disabled = false;
      btn.textContent = this.t('generate_draft_btn');
    }
  },

  renderGrievanceDraft(draftData) {
    const resultBox = document.getElementById('grievanceResultBox');
    resultBox.style.display = 'block';

    const textarea = document.getElementById('grievanceDraftEditor');
    textarea.value = draftData.generated_draft;

    const checklistEl = document.getElementById('grievanceChecklist');
    checklistEl.innerHTML = '';
    (draftData.checklist || []).forEach(it => {
      const li = document.createElement('li');
      li.textContent = it;
      checklistEl.appendChild(li);
    });

    const nextStepsEl = document.getElementById('grievanceNextSteps');
    nextStepsEl.innerHTML = '';
    (draftData.next_steps || []).forEach(it => {
      const li = document.createElement('li');
      li.textContent = it;
      nextStepsEl.appendChild(li);
    });

    resultBox.scrollIntoView({ behavior: 'smooth' });
  },

  async saveGrievanceToDb() {
    const text = document.getElementById('grievanceDraftEditor').value.trim();
    if (!text) return;

    const payload = {
      category: document.getElementById('grievanceCategory').value,
      employer_platform: document.getElementById('grievanceEmployer').value.trim(),
      incident_date: document.getElementById('grievanceDate').value || new Date().toISOString().split('T')[0],
      amount_disputed: parseFloat(document.getElementById('grievanceAmount').value) || null,
      incident_details: document.getElementById('grievanceDetails').value.trim(),
      evidence_available: document.getElementById('grievanceEvidence').value.trim(),
      generated_draft: text,
      language: this.state.language,
      linked_earning_id: this.state.activeEarningContext ? this.state.activeEarningContext.id : null
    };

    try {
      const res = await fetch('/api/grievances/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        this.showToast('Grievance saved to your records!', 'success');
      } else {
        const err = await res.json();
        this.showToast(err.detail || 'Failed to save to database', 'error');
      }
    } catch (e) {
      this.showToast('Network error while saving to database', 'error');
    }
  },

  copyGrievanceDraft() {
    const text = document.getElementById('grievanceDraftEditor').value;
    navigator.clipboard.writeText(text).then(() => {
      this.showToast('Draft copied to clipboard!', 'success');
    }).catch(() => {
      this.showToast('Could not copy automatically', 'warning');
    });
  },

  downloadGrievanceDraft() {
    const text = document.getElementById('grievanceDraftEditor').value;
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `grievance_${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  },

  // --- Modal Helpers ---
  openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
  },

  closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
  },

  // --- Event Bindings ---
  bindEvents() {
    // Navigation items
    document.querySelectorAll('[data-tab]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tab = e.currentTarget.dataset.tab;
        this.navigate(tab);
      });
    });

    // Language Selector
    document.getElementById('langSelect').addEventListener('change', (e) => {
      this.setLanguage(e.target.value);
    });

    // Worker Role Switcher
    document.getElementById('workerRoleSelect').addEventListener('change', (e) => {
      this.state.workerRole = e.target.value;
      this.loadSafetyGuide(e.target.value);
      this.showToast(`Active profile: ${e.target.value}`, 'info');
    });

    // Theme Toggle
    const themeBtn = document.getElementById('themeToggleBtn');
    themeBtn.addEventListener('click', () => {
      const isDark = document.body.getAttribute('data-theme') === 'dark';
      document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
      themeBtn.textContent = isDark ? '🌙' : '☀️';
    });

    // Chat enter key
    document.getElementById('chatInput').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        this.sendChatMessage();
      }
    });

    // File Drag & Drop
    const dropArea = document.getElementById('docDropArea');
    if (dropArea) {
      ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, (e) => {
          e.preventDefault();
          dropArea.style.borderColor = 'var(--primary)';
        });
      });
      ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, (e) => {
          e.preventDefault();
          dropArea.style.borderColor = 'var(--border-color)';
        });
      });
      dropArea.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        if (file) {
          document.getElementById('docFileInput').files = e.dataTransfer.files;
          document.getElementById('selectedFileName').textContent = `Selected: ${file.name}`;
        }
      });
    }

    const fileInput = document.getElementById('docFileInput');
    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          document.getElementById('selectedFileName').textContent = `Selected: ${file.name}`;
        }
      });
    }
  }
};

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
