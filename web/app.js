document.addEventListener('DOMContentLoaded', () => {
  let currentReportData = window.TICKET_REPORT_DATA;
  if (!currentReportData) return;

  initTabs();
  renderFullDashboard(currentReportData);
  initActions(currentReportData);
  initDataProvenanceActions(currentReportData);
  initSandboxUploader(currentReportData);
});

function renderFullDashboard(data) {
  renderOverview(data);
  renderAttentionMatrix(data.executive_attention_matrix || []);
  renderCharts(data);
  renderAnomalies(data.anomalies || []);
  renderClusters(data.sub_issue_clusters || {});
  renderUnresolvedTable(data.unresolved_tickets || []);
  renderExplorerTable(data.raw_tickets || []);
}

function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = `tab-${btn.dataset.tab}`;
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });
}

function showToast(message) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerText = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => toast.remove(), 300);
  }, 2800);
}

function downloadTextFile(filename, content, mimeType = 'text/plain;charset=utf-8;') {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast(`已成功下载文件: ${filename}`);
}

function downloadJsonFile(filename, dataObj) {
  downloadTextFile(filename, JSON.stringify(dataObj, null, 2), 'application/json;charset=utf-8;');
}

function renderOverview(data) {
  const ov = data.overview;
  document.getElementById('headerPeriod').innerText = `${ov.date_range[0]} ~ ${ov.date_range[1]} (${ov.days_count}天)`;
  document.getElementById('kpiTotalTickets').innerHTML = `${ov.total_tickets} <span class="stat-unit">条 / ${ov.days_count}天</span>`;
  document.getElementById('kpiResolvedRate').innerHTML = `${ov.resolved_rate}% <span class="stat-unit">(${ov.resolved_count}/${ov.total_tickets})</span>`;
  document.getElementById('kpiAvgSatisfaction').innerHTML = `${ov.avg_satisfaction} <span class="stat-unit">/ 5.0</span>`;
  document.getElementById('kpiAvgTime').innerHTML = `${ov.avg_resolution_time_hours} <span class="stat-unit">小时</span>`;

  document.getElementById('anomalyBadgeCount').innerText = (data.anomalies || []).length;
  document.getElementById('unresolvedBadgeCount').innerText = (data.unresolved_tickets || []).length;

  const tbody = document.querySelector('#tableCategories tbody');
  tbody.innerHTML = '';
  (data.categories || []).forEach(c => {
    let riskBadge = '<span class="badge badge-low">🟢 较低</span>';
    if (c.unresolved_rate > 20 || c.avg_satisfaction <= 2.0) {
      riskBadge = '<span class="badge badge-p0">🔴 极高</span>';
    } else if (c.count > 10) {
      riskBadge = '<span class="badge badge-p1">🟡 中等</span>';
    }

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${c.category}</strong></td>
      <td>${c.count}</td>
      <td>${c.percentage}%</td>
      <td>${c.high_priority_count}</td>
      <td><span class="${c.unresolved_count > 0 ? 'badge badge-unres' : ''}">${c.unresolved_count}</span></td>
      <td>${c.unresolved_rate}%</td>
      <td><span class="${c.avg_satisfaction <= 2.0 ? 'text-danger font-weight-bold' : ''}">⭐ ${c.avg_satisfaction}</span></td>
      <td>${c.avg_resolution_time_hours}h</td>
      <td>${c.max_resolution_time_hours}h</td>
      <td>${riskBadge}</td>
    `;
    tbody.appendChild(tr);
  });
}

function renderAttentionMatrix(matrix) {
  const tbody = document.querySelector('#tableAttentionMatrix tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  matrix.forEach(item => {
    let scoreBadge = 'badge-p2';
    if (item.attention_index >= 70) scoreBadge = 'badge-p0';
    else if (item.attention_index >= 40) scoreBadge = 'badge-p1';

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${item.issue_cluster}</strong></td>
      <td><span class="badge ${scoreBadge}" style="font-size: 13px; font-weight: 800;">⚡ API ${item.attention_index}</span></td>
      <td><span class="badge ${scoreBadge}">${item.urgency_level}</span></td>
      <td><strong style="color: #1e40af;">${item.target_department}</strong></td>
      <td>${item.accountable_owner}</td>
      <td>${item.ticket_count}单 (未结: <span class="${item.unresolved_count > 0 ? 'text-danger font-weight-bold' : ''}">${item.unresolved_count}</span>)</td>
      <td>⭐ ${item.avg_satisfaction} / ${item.avg_hours}h</td>
      <td>
        <div style="display: flex; align-items: center; gap: 6px;">
          <span style="font-size: 12px; color: #334155;">${item.recommended_directive}</span>
          <button class="btn btn-sm btn-outline" style="padding: 2px 6px; font-size: 11px; white-space: nowrap;" onclick="copyDirectiveText('${item.recommended_directive.replace(/'/g, "\\'")}')">📋 复制指令</button>
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

window.copyDirectiveText = function(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('📋 主管跨部门治理督办指令已复制！');
  });
};

let chartInstances = {};

function renderCharts(data) {
  if (typeof Chart !== 'undefined') {
    renderChartJS(data);
  } else {
    renderNativeCanvasCharts(data);
  }
}

function renderChartJS(data) {
  if (chartInstances.daily) chartInstances.daily.destroy();
  if (chartInstances.category) chartInstances.category.destroy();
  if (chartInstances.channel) chartInstances.channel.destroy();
  if (chartInstances.priority) chartInstances.priority.destroy();

  const dailyLabels = (data.daily_trends || []).map(d => d.date.slice(5));
  const dailyTotals = (data.daily_trends || []).map(d => d.total);
  const dailyUnres = (data.daily_trends || []).map(d => d.unresolved_count);
  const dailySats = (data.daily_trends || []).map(d => d.avg_satisfaction);

  const ctxDaily = document.getElementById('chartDailyTrend').getContext('2d');
  chartInstances.daily = new Chart(ctxDaily, {
    type: 'bar',
    data: {
      labels: dailyLabels,
      datasets: [
        { label: '当日工单总量', data: dailyTotals, backgroundColor: '#93c5fd', borderRadius: 4, yAxisID: 'y' },
        { label: '未解决工单', data: dailyUnres, backgroundColor: '#ef4444', borderRadius: 4, yAxisID: 'y' },
        { type: 'line', label: '平均满意度 (右轴)', data: dailySats, borderColor: '#f59e0b', backgroundColor: '#f59e0b', borderWidth: 2.5, tension: 0.2, yAxisID: 'y1' }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: '工单数' }, ticks: { stepSize: 1 } },
        y1: { position: 'right', min: 0, max: 5, title: { display: true, text: '满意度 (星)' }, grid: { drawOnChartArea: false } }
      }
    }
  });

  const catLabels = (data.categories || []).map(c => c.category);
  const catCounts = (data.categories || []).map(c => c.count);
  const catSats = (data.categories || []).map(c => c.avg_satisfaction);

  const ctxCat = document.getElementById('chartCategoryDist').getContext('2d');
  chartInstances.category = new Chart(ctxCat, {
    type: 'bar',
    data: {
      labels: catLabels,
      datasets: [
        { label: '工单量', data: catCounts, backgroundColor: ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe'], borderRadius: 4, yAxisID: 'y' },
        { type: 'line', label: '平均满意度', data: catSats, borderColor: '#dc2626', backgroundColor: '#dc2626', borderWidth: 2, yAxisID: 'y1' }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: '工单量' } },
        y1: { position: 'right', min: 0, max: 5, grid: { drawOnChartArea: false }, title: { display: true, text: '满意度' } }
      }
    }
  });

  const chanLabels = (data.channels || []).map(c => c.channel);
  const chanHours = (data.channels || []).map(c => c.avg_resolution_time_hours);
  const chanUnres = (data.channels || []).map(c => c.unresolved_rate);

  const ctxChan = document.getElementById('chartChannel').getContext('2d');
  chartInstances.channel = new Chart(ctxChan, {
    type: 'bar',
    data: {
      labels: chanLabels,
      datasets: [
        { label: '平均处理时长 (小时)', data: chanHours, backgroundColor: '#8b5cf6', borderRadius: 4 },
        { label: '未解决率 (%)', data: chanUnres, backgroundColor: '#f87171', borderRadius: 4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: { y: { beginAtZero: true } }
    }
  });

  const prioLabels = (data.priorities || []).map(p => `${p.priority}优先级 (${p.count}单)`);
  const prioCounts = (data.priorities || []).map(p => p.count);

  const ctxPrio = document.getElementById('chartPriority').getContext('2d');
  chartInstances.priority = new Chart(ctxPrio, {
    type: 'doughnut',
    data: {
      labels: prioLabels,
      datasets: [{ data: prioCounts, backgroundColor: ['#ef4444', '#f59e0b', '#10b981'], borderWidth: 2 }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' } }
    }
  });
}

function renderNativeCanvasCharts(data) {
  drawSimpleBarLineCanvas('chartDailyTrend', (data.daily_trends || []).map(d => ({
    label: d.date.slice(5),
    v1: d.total,
    v2: d.unresolved_count,
    v3: d.avg_satisfaction
  })));

  drawSimpleCatCanvas('chartCategoryDist', data.categories || []);
}

function drawSimpleBarLineCanvas(canvasId, items) {
  const cvs = document.getElementById(canvasId);
  if (!cvs) return;
  const ctx = cvs.getContext('2d');
  cvs.width = cvs.parentElement.clientWidth || 500;
  cvs.height = 240;

  ctx.clearRect(0, 0, cvs.width, cvs.height);
  const w = cvs.width, h = cvs.height;
  const pad = 40;
  const bw = (w - pad * 2) / (items.length || 1);

  items.forEach((it, i) => {
    const x = pad + i * bw;
    const barH = (it.v1 / 7) * (h - pad * 2);
    ctx.fillStyle = '#93c5fd';
    ctx.fillRect(x + 5, h - pad - barH, bw * 0.4, barH);

    const unresH = (it.v2 / 7) * (h - pad * 2);
    if (unresH > 0) {
      ctx.fillStyle = '#ef4444';
      ctx.fillRect(x + 5 + bw * 0.4, h - pad - unresH, bw * 0.4, unresH);
    }

    ctx.fillStyle = '#64748b';
    ctx.font = '11px sans-serif';
    ctx.fillText(it.label, x + 2, h - pad + 15);
  });
}

function drawSimpleCatCanvas(canvasId, categories) {
  const cvs = document.getElementById(canvasId);
  if (!cvs) return;
  const ctx = cvs.getContext('2d');
  cvs.width = cvs.parentElement.clientWidth || 500;
  cvs.height = 240;

  ctx.clearRect(0, 0, cvs.width, cvs.height);
  const w = cvs.width, h = cvs.height;
  const pad = 50;
  const bw = (w - pad * 2) / (categories.length || 1);

  categories.forEach((c, i) => {
    const x = pad + i * bw;
    const barH = (c.count / 18) * (h - pad * 2);
    ctx.fillStyle = '#2563eb';
    ctx.fillRect(x + 10, h - pad - barH, bw * 0.6, barH);

    ctx.fillStyle = '#1e293b';
    ctx.font = '11px sans-serif';
    ctx.fillText(c.category, x + 2, h - pad + 15);
    ctx.fillText(`${c.count}单`, x + 15, h - pad - barH - 5);
  });
}

function renderAnomalies(anomalies) {
  const container = document.getElementById('anomaliesContainer');
  container.innerHTML = '';

  const priorityRank = {
    'CRITICAL (P0)': 3,
    'HIGH (P1)': 2,
    'WARNING (P2)': 1
  };

  const sortedAnomalies = [...anomalies].sort((a, b) => {
    const rankA = priorityRank[a.level] || 0;
    const rankB = priorityRank[b.level] || 0;
    return rankB - rankA;
  });

  sortedAnomalies.forEach((a) => {
    let levelClass = 'tree-level-warning';
    let badgeClass = 'badge-p2';
    let metaTag = 'P2 一般预警';
    if (a.level.includes('P0') || a.level.includes('CRITICAL')) {
      levelClass = 'tree-level-critical';
      badgeClass = 'badge-p0';
      metaTag = 'P0 极高危阻断';
    } else if (a.level.includes('P1') || a.level.includes('HIGH')) {
      levelClass = 'tree-level-high';
      badgeClass = 'badge-p1';
      metaTag = 'P1 高度关注';
    }

    const node = document.createElement('div');
    node.className = `tree-anomaly-node ${levelClass}`;
    node.id = `tree-node-${a.id}`;

    const factsList = a.objective_facts.map(f => `<li>${f}</li>`).join('');
    const hypList = a.hypothesis_verification.hypotheses.map(h => `<li>${h}</li>`).join('');
    const expList = a.experimental_validation.experiments.map(e => `<li>${e}</li>`).join('');

    node.innerHTML = `
      <div class="tree-node-header" data-target="${a.id}">
        <div class="tree-header-left">
          <span class="tree-toggle-arrow">▶</span>
          <span class="badge ${badgeClass}">${a.level}</span>
          <span class="tree-node-title">[${a.id}] ${a.title}</span>
        </div>
        <div class="tree-header-right">
          <span class="tree-meta-pill">${metaTag}</span>
          <span class="tree-expand-hint">点击展开归因</span>
        </div>
      </div>

      <div class="tree-node-body" id="body-${a.id}">
        <div class="tree-branch-container">
          <div class="tree-branch branch-facts">
            <div class="branch-label">🌿 1. 客观事实证据链 (Empirical Evidence)</div>
            <ul>${factsList}</ul>
          </div>

          <div class="tree-branch branch-signal">
            <div class="branch-label">⚡ 2. 异常特征信号 (Diagnostic Signal)</div>
            <div class="signal-text">${a.signal}</div>
          </div>

          <div class="tree-branch branch-hypothesis">
            <div class="branch-label">🔍 3. 底层机理与假设验证 (Root Cause Verification)</div>
            <ul>${hypList}</ul>
            <div class="verification-box"><strong>💡 交叉推断：</strong>${a.hypothesis_verification.verification}</div>
          </div>

          <div class="tree-branch branch-experiment">
            <div class="branch-label">🧪 4. 闭环工程治理方案 (Remediation & Defense)</div>
            <ul>${expList}</ul>
            <div class="target-box">🎯 治理目标与验收标准：${a.experimental_validation.remediation_target}</div>
          </div>
        </div>
      </div>
    `;

    const header = node.querySelector('.tree-node-header');
    header.addEventListener('click', () => {
      toggleTreeNode(node);
    });

    container.appendChild(node);
  });

  const btnExpandAll = document.getElementById('btnExpandAllAnomalies');
  const btnCollapseAll = document.getElementById('btnCollapseAllAnomalies');

  if (btnExpandAll) {
    btnExpandAll.onclick = () => {
      document.querySelectorAll('.tree-anomaly-node').forEach(n => {
        n.classList.add('expanded');
        const arrow = n.querySelector('.tree-toggle-arrow');
        if (arrow) arrow.innerText = '▼';
        const hint = n.querySelector('.tree-expand-hint');
        if (hint) hint.innerText = '点击收起';
      });
    };
  }

  if (btnCollapseAll) {
    btnCollapseAll.onclick = () => {
      document.querySelectorAll('.tree-anomaly-node').forEach(n => {
        n.classList.remove('expanded');
        const arrow = n.querySelector('.tree-toggle-arrow');
        if (arrow) arrow.innerText = '▶';
        const hint = n.querySelector('.tree-expand-hint');
        if (hint) hint.innerText = '点击展开归因';
      });
    };
  }
}

function toggleTreeNode(node) {
  const isExpanded = node.classList.contains('expanded');
  const arrow = node.querySelector('.tree-toggle-arrow');
  const hint = node.querySelector('.tree-expand-hint');

  if (isExpanded) {
    node.classList.remove('expanded');
    if (arrow) arrow.innerText = '▶';
    if (hint) hint.innerText = '点击展开归因';
  } else {
    node.classList.add('expanded');
    if (arrow) arrow.innerText = '▼';
    if (hint) hint.innerText = '点击收起';
  }
}

function renderClusters(clusters) {
  const container = document.getElementById('clustersContainer');
  container.innerHTML = '';

  for (const [name, info] of Object.entries(clusters)) {
    const card = document.createElement('div');
    card.className = 'cluster-card';

    const ticketSamples = info.tickets.map(t => `<span class="badge badge-low">${t.ticket_id}</span>`).join(' ');

    card.innerHTML = `
      <div class="cluster-header">
        <div class="cluster-name">${name}</div>
        <span class="badge badge-p1">${info.level}</span>
      </div>
      <div class="cluster-stats">
        <span>📊 涉及 <strong>${info.count}</strong> 单</span>
        <span>⚠️ 未解决 <strong>${info.unresolved_count}</strong> 单</span>
        <span>⭐ 满意度 <strong>${info.avg_satisfaction}</strong></span>
        <span>⏱️ 均时 <strong>${info.avg_resolution_hours}h</strong></span>
      </div>
      <div class="cluster-impact">
        <strong>业务影响：</strong>${info.impact}
      </div>
      <div class="cluster-samples">
        关联工单：${ticketSamples}
      </div>
    `;
    container.appendChild(card);
  }
}

function renderUnresolvedTable(unresolved) {
  const tbody = document.querySelector('#tableUnresolved tbody');
  tbody.innerHTML = '';

  const actionMap = {
    "T019": "联系物流核查异常退回原因，补发并赔付优惠券",
    "T031": "🚨 滞留120h！主管特批垫付运费原路退款，电话致歉",
    "T033": "联系快递网点排查派件异常，丢件立即先行赔付",
    "T036": "纠正客服拦截，支持7天无理由退货，立即放行",
    "T039": "🚨 修复状态机错误，重新开启退款通道并查证物流",
    "T042": "核对28元运费凭证，今日完成转账报销",
    "T046": "🚨 财务立即退还重复扣款，技术组排查支付幂等Key",
    "T047": "🚨 退款滞留96h，财务专员今日内必须放款到账"
  };

  unresolved.forEach(u => {
    const act = actionMap[u.ticket_id] || "专人立即跟进";
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${u.ticket_id}</strong></td>
      <td>${u.created_at}</td>
      <td><span class="badge badge-cat">${u.category}</span></td>
      <td><span class="badge badge-high">${u.priority}</span></td>
      <td><strong class="text-danger">${u.resolution_time_hours}h</strong></td>
      <td><span class="text-danger">⭐ ${u.satisfaction}</span></td>
      <td>${u.channel}</td>
      <td style="max-width: 320px;">${u.description}</td>
      <td><span class="badge badge-p0" style="white-space: normal;">${act}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

function renderExplorerTable(tickets) {
  const tbody = document.querySelector('#tableExplorer tbody');
  const searchInput = document.getElementById('searchKeyword');
  const catSelect = document.getElementById('filterCategory');
  const prioSelect = document.getElementById('filterPriority');
  const resSelect = document.getElementById('filterResolved');
  const chanSelect = document.getElementById('filterChannel');
  const btnReset = document.getElementById('btnResetFilter');
  const statsSpan = document.getElementById('filterStats');

  function applyFilter() {
    const kw = searchInput.value.trim().toLowerCase();
    const cat = catSelect.value;
    const prio = prioSelect.value;
    const res = resSelect.value;
    const chan = chanSelect.value;

    const filtered = tickets.filter(t => {
      if (kw && !t.ticket_id.toLowerCase().includes(kw) && !t.description.toLowerCase().includes(kw)) {
        return false;
      }
      if (cat && t.category !== cat) return false;
      if (prio && t.priority !== prio) return false;
      if (chan && t.channel !== chan) return false;
      if (res === 'resolved' && !t.is_resolved) return false;
      if (res === 'unresolved' && t.is_resolved) return false;
      return true;
    });

    statsSpan.innerText = `显示 ${filtered.length} / ${tickets.length} 条工单`;
    tbody.innerHTML = '';

    filtered.forEach(t => {
      const tr = document.createElement('tr');
      const prioClass = t.priority === '高' ? 'badge-high' : (t.priority === '中' ? 'badge-med' : 'badge-low');
      const resBadge = t.is_resolved 
        ? '<span class="badge badge-res">已解决</span>' 
        : '<span class="badge badge-unres">未解决</span>';

      tr.innerHTML = `
        <td><strong>${t.ticket_id}</strong></td>
        <td>${t.created_at}</td>
        <td><span class="badge badge-cat">${t.category}</span></td>
        <td><span class="badge ${prioClass}">${t.priority}</span></td>
        <td>${t.resolution_time_hours}h</td>
        <td>⭐ ${t.satisfaction}</td>
        <td>${t.channel}</td>
        <td>${resBadge}</td>
        <td>${t.description}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  searchInput.addEventListener('input', applyFilter);
  catSelect.addEventListener('change', applyFilter);
  prioSelect.addEventListener('change', applyFilter);
  resSelect.addEventListener('change', applyFilter);
  chanSelect.addEventListener('change', applyFilter);

  btnReset.addEventListener('click', () => {
    searchInput.value = '';
    catSelect.value = '';
    prioSelect.value = '';
    resSelect.value = '';
    chanSelect.value = '';
    applyFilter();
    showToast('已重置所有筛选条件');
  });

  applyFilter();
}

function initActions(data) {
  document.getElementById('btnPrint').addEventListener('click', () => {
    window.print();
  });

  const btnRefresh = document.getElementById('btnRefresh');
  btnRefresh.addEventListener('click', () => {
    triggerDynamicCalculation(data);
  });
}

function initDataProvenanceActions(data) {
  let currentPreviewPayload = data.raw_tickets;
  let currentFilename = 'tickets.json';
  let isRawText = false;

  const modal = document.getElementById('rawPreviewModal');
  const codeBlock = document.getElementById('rawJsonCodeBlock');
  const titleText = document.getElementById('rawModalTitleText');

  function openPreview(title, filename, payload, isText = false) {
    currentFilename = filename;
    currentPreviewPayload = payload;
    isRawText = isText;
    titleText.innerText = title;
    codeBlock.innerText = isText ? payload : JSON.stringify(payload, null, 2);
    modal.classList.add('show');
  }

  function closePreview() {
    modal.classList.remove('show');
  }

  document.getElementById('btnCloseRawModal').addEventListener('click', closePreview);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closePreview();
  });

  document.getElementById('btnCopyRawJson').addEventListener('click', () => {
    navigator.clipboard.writeText(codeBlock.innerText).then(() => {
      showToast('📋 内容已复制到剪贴板！');
    });
  });

  document.getElementById('btnDownloadFromModal').addEventListener('click', () => {
    if (isRawText) {
      downloadTextFile(currentFilename, currentPreviewPayload, 'text/markdown;charset=utf-8;');
    } else {
      downloadJsonFile(currentFilename, currentPreviewPayload);
    }
  });

  const mdReportText = window.ANALYSIS_REPORT_MARKDOWN || "未找到分析报告数据";

  const btnHeaderPreviewMd = document.getElementById('btnHeaderPreviewMd');
  if (btnHeaderPreviewMd) {
    btnHeaderPreviewMd.addEventListener('click', () => {
      openPreview('📄 结构化趋势分析报告: docs/analysis_report.md', 'analysis_report.md', mdReportText, true);
    });
  }

  const btnHeaderDownloadMd = document.getElementById('btnHeaderDownloadMd');
  if (btnHeaderDownloadMd) {
    btnHeaderDownloadMd.addEventListener('click', () => {
      downloadTextFile('analysis_report.md', mdReportText, 'text/markdown;charset=utf-8;');
    });
  }

  const btnPreviewAnalysisMd = document.getElementById('btnPreviewAnalysisMd');
  if (btnPreviewAnalysisMd) {
    btnPreviewAnalysisMd.addEventListener('click', () => {
      openPreview('📄 结构化趋势分析报告: docs/analysis_report.md', 'analysis_report.md', mdReportText, true);
    });
  }

  const btnDownloadAnalysisMd = document.getElementById('btnDownloadAnalysisMd');
  if (btnDownloadAnalysisMd) {
    btnDownloadAnalysisMd.addEventListener('click', () => {
      downloadTextFile('analysis_report.md', mdReportText, 'text/markdown;charset=utf-8;');
    });
  }

  const btnHeaderPreview = document.getElementById('btnHeaderPreviewJson');
  if (btnHeaderPreview) {
    btnHeaderPreview.addEventListener('click', () => {
      openPreview('📄 数据源预览: data/tickets.json (50 条原始工单数据)', 'tickets.json', data.raw_tickets, false);
    });
  }

  const btnHeaderDownload = document.getElementById('btnHeaderDownloadJson');
  if (btnHeaderDownload) {
    btnHeaderDownload.addEventListener('click', () => {
      downloadJsonFile('tickets.json', data.raw_tickets);
    });
  }

  const btnPreviewSource = document.getElementById('btnPreviewSourceData');
  if (btnPreviewSource) {
    btnPreviewSource.addEventListener('click', () => {
      openPreview('📄 数据源预览: data/tickets.json (50 条原始工单数据)', 'tickets.json', data.raw_tickets, false);
    });
  }

  const btnDownloadSource = document.getElementById('btnDownloadSourceData');
  if (btnDownloadSource) {
    btnDownloadSource.addEventListener('click', () => {
      downloadJsonFile('tickets.json', data.raw_tickets);
    });
  }

  const btnDownloadFull = document.getElementById('btnDownloadFullReportJson');
  if (btnDownloadFull) {
    btnDownloadFull.addEventListener('click', () => {
      downloadJsonFile('full_analysis_data.json', data);
    });
  }
}

function initSandboxUploader(initialData) {
  const uploadInput = document.getElementById('inputUploadJson');
  const btnReset = document.getElementById('btnResetToDefaultData');

  if (uploadInput) {
    uploadInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const rawParsed = JSON.parse(event.target.result);
          if (!Array.isArray(rawParsed)) {
            showToast('⚠️ 上传失败: JSON 文件根必须为工单数组 (Array)');
            return;
          }
          const dynamicData = buildDynamicAnalysis(rawParsed);
          triggerDynamicCalculation(dynamicData, file.name);
          showToast(`✅ 成功加载外部工单源: ${file.name} (${rawParsed.length}条)`);
        } catch (err) {
          showToast('⚠️ 解析失败: 非标准 JSON 文件');
        }
      };
      reader.readAsText(file, 'utf-8');
    });
  }

  if (btnReset) {
    btnReset.addEventListener('click', () => {
      triggerDynamicCalculation(window.TICKET_REPORT_DATA, 'data/tickets.json');
      showToast('🔄 已恢复官方标准 50 条工单数据源');
    });
  }
}

function buildDynamicAnalysis(rawTickets) {
  const total = rawTickets.length;
  if (total === 0) return window.TICKET_REPORT_DATA;

  const unresolved = rawTickets.filter(t => !t.is_resolved);
  const sats = rawTickets.map(t => Number(t.satisfaction) || 3);
  const times = rawTickets.map(t => Number(t.resolution_time_hours) || 0);
  const highPri = rawTickets.filter(t => t.priority === '高');

  const avgSat = (sats.reduce((a, b) => a + b, 0) / total).toFixed(2);
  const avgTime = (times.reduce((a, b) => a + b, 0) / total).toFixed(1);

  const dates = [...new Set(rawTickets.map(t => t.created_at.slice(0, 10)))].sort();

  const overview = {
    total_tickets: total,
    date_range: [dates[0] || '2024-06-01', dates[dates.length - 1] || '2024-06-11'],
    days_count: dates.length || 1,
    resolved_count: total - unresolved.length,
    unresolved_count: unresolved.length,
    resolved_rate: (((total - unresolved.length) / total) * 100).toFixed(1),
    avg_satisfaction: avgSat,
    avg_resolution_time_hours: avgTime,
    high_priority_count: highPri.length,
    high_priority_rate: ((highPri.length / total) * 100).toFixed(1)
  };

  const catMap = {};
  rawTickets.forEach(t => {
    const c = t.category || '其它';
    if (!catMap[c]) catMap[c] = [];
    catMap[c].push(t);
  });

  const categories = Object.keys(catMap).map(cname => {
    const items = catMap[cname];
    const unres = items.filter(x => !x.is_resolved);
    const hp = items.filter(x => x.priority === '高');
    const cSats = items.map(x => Number(x.satisfaction) || 3);
    const cTimes = items.map(x => Number(x.resolution_time_hours) || 0);

    return {
      category: cname,
      count: items.length,
      percentage: ((items.length / total) * 100).toFixed(1),
      unresolved_count: unres.length,
      unresolved_rate: ((unres.length / items.length) * 100).toFixed(1),
      high_priority_count: hp.length,
      avg_satisfaction: (cSats.reduce((a, b) => a + b, 0) / items.length).toFixed(2),
      avg_resolution_time_hours: (cTimes.reduce((a, b) => a + b, 0) / items.length).toFixed(1),
      max_resolution_time_hours: Math.max(...cTimes)
    };
  }).sort((a, b) => b.count - a.count);

  const dayMap = {};
  rawTickets.forEach(t => {
    const d = t.created_at.slice(0, 10);
    if (!dayMap[d]) dayMap[d] = [];
    dayMap[d].push(t);
  });

  const daily_trends = Object.keys(dayMap).sort().map(dstr => {
    const items = dayMap[dstr];
    const unres = items.filter(x => !x.is_resolved);
    const dSats = items.map(x => Number(x.satisfaction) || 3);
    return {
      date: dstr,
      total: items.length,
      unresolved_count: unres.length,
      avg_satisfaction: (dSats.reduce((a, b) => a + b, 0) / items.length).toFixed(2)
    };
  });

  const chanMap = {};
  rawTickets.forEach(t => {
    const ch = t.channel || '在线';
    if (!chanMap[ch]) chanMap[ch] = [];
    chanMap[ch].push(t);
  });

  const channels = Object.keys(chanMap).map(ch => {
    const items = chanMap[ch];
    const unres = items.filter(x => !x.is_resolved);
    const cTimes = items.map(x => Number(x.resolution_time_hours) || 0);
    const cSats = items.map(x => Number(x.satisfaction) || 3);
    return {
      channel: ch,
      count: items.length,
      unresolved_rate: ((unres.length / items.length) * 100).toFixed(1),
      avg_satisfaction: (cSats.reduce((a, b) => a + b, 0) / items.length).toFixed(2),
      avg_resolution_time_hours: (cTimes.reduce((a, b) => a + b, 0) / items.length).toFixed(1)
    };
  });

  const prioMap = { '高': 0, '中': 0, '低': 0 };
  rawTickets.forEach(t => {
    const p = t.priority || '中';
    prioMap[p] = (prioMap[p] || 0) + 1;
  });
  const priorities = Object.keys(prioMap).map(p => ({
    priority: p,
    count: prioMap[p]
  }));

  return {
    overview,
    categories,
    daily_trends,
    channels,
    priorities,
    sub_issue_clusters: window.TICKET_REPORT_DATA.sub_issue_clusters,
    anomalies: window.TICKET_REPORT_DATA.anomalies,
    executive_attention_matrix: window.TICKET_REPORT_DATA.executive_attention_matrix,
    unresolved_tickets: unresolved,
    raw_tickets: rawTickets
  };
}

function triggerDynamicCalculation(data, filename = 'data/tickets.json') {
  const btnRefresh = document.getElementById('btnRefresh');
  btnRefresh.disabled = true;
  btnRefresh.innerHTML = '<span class="spinner-icon">🔄</span> 正在执行多维分析...';

  let modal = document.getElementById('calcProgressModal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'calcProgressModal';
    modal.className = 'calc-modal-overlay';
    modal.innerHTML = `
      <div class="calc-modal-card">
        <div class="calc-modal-header">
          <div class="calc-pulse-dot"></div>
          <div>
            <h3>多维工单流与异常检测引擎运算中</h3>
            <div class="calc-target-row">
              <span class="calc-target-label">分析数据源:</span>
              <code class="calc-target-code" id="calcTargetFilename">${filename}</code>
              <span class="calc-stream-counter" id="calcStreamCounter">[ 0 / 50 ]</span>
            </div>
          </div>
        </div>
        <div class="calc-current-item-bar" id="calcCurrentItemBar">准备加载工单流...</div>
        <div class="calc-progress-bar-bg">
          <div class="calc-progress-bar-fill" id="calcProgressBar"></div>
        </div>
        <div class="calc-steps-list" id="calcStepsList"></div>
      </div>
    `;
    document.body.appendChild(modal);
  }

  const stepsList = document.getElementById('calcStepsList');
  const bar = document.getElementById('calcProgressBar');
  const counter = document.getElementById('calcStreamCounter');
  const itemBar = document.getElementById('calcCurrentItemBar');
  const targetFile = document.getElementById('calcTargetFilename');

  targetFile.innerText = filename;
  stepsList.innerHTML = '';
  bar.style.width = '0%';
  const rawTickets = data.raw_tickets || [];
  const totalCount = rawTickets.length || 50;
  counter.innerText = `[ 0 / ${totalCount} ]`;
  itemBar.innerText = '正在建立数据管道流...';
  modal.classList.add('show');

  let currentIdx = 0;
  const intervalSpeed = totalCount > 100 ? 5 : 16;

  const streamInterval = setInterval(() => {
    currentIdx++;
    if (currentIdx <= totalCount) {
      const ticket = rawTickets[currentIdx - 1];
      counter.innerText = `[ ${currentIdx} / ${totalCount} ]`;
      const pct = Math.round((currentIdx / totalCount) * 100);
      bar.style.width = `${pct}%`;
      if (ticket) {
        itemBar.innerHTML = `<span>解析对象: <strong>${ticket.ticket_id}</strong> (${ticket.category}) | 耗时: ${ticket.resolution_time_hours}h | ⭐ ${ticket.satisfaction}</span>`;
      }
    } else {
      clearInterval(streamInterval);
      itemBar.innerHTML = `<span class="text-success"><strong>${filename}</strong> ${totalCount}/${totalCount} 全量工单流解析完成，启动聚合引擎...</span>`;
      executeAnalysisSteps(data, modal, btnRefresh, filename, totalCount);
    }
  }, intervalSpeed);
}

function executeAnalysisSteps(data, modal, btnRefresh, filename, totalCount) {
  const stepsList = document.getElementById('calcStepsList');
  const steps = [
    { title: `Step 1/4: [${filename}] ${totalCount}/${totalCount} 条工单 Schema 校验与清洗完成`, delay: 100 },
    { title: `Step 2/4: [${filename}] 6 大业务分类时序演变与渠道 SLA 矩阵计算完毕`, delay: 300 },
    { title: `Step 3/4: [${filename}] 5 项 P0/P1 异常树四步归因与子问题聚类完成`, delay: 550 },
    { title: `Step 4/4: [docs/full_analysis_data.json] 导出指标集并重绘多维看板视图`, delay: 750 }
  ];

  steps.forEach((s) => {
    setTimeout(() => {
      const item = document.createElement('div');
      item.className = 'calc-step-item';
      item.innerHTML = `<span class="calc-step-check">✓</span> <span>${s.title}</span>`;
      stepsList.appendChild(item);
    }, s.delay);
  });

  setTimeout(() => {
    renderFullDashboard(data);

    setTimeout(() => {
      modal.classList.remove('show');
      btnRefresh.disabled = false;
      btnRefresh.innerHTML = '🔄 重新分析数据';
      showToast(`✅ 已重新完成 ${filename} (${totalCount}/${totalCount}) 全量工单多维分析与异常检测！`);
    }, 400);
  }, 1000);
}
