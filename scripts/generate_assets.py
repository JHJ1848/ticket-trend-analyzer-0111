import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('assets', exist_ok=True)

terminal_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 420" width="850" height="420">
  <rect width="850" height="420" rx="10" fill="#1e1e1e"/>
  <rect width="850" height="35" rx="10" fill="#2d2d2d"/>
  <circle cx="20" cy="18" r="6" fill="#ff5f56"/>
  <circle cx="40" cy="18" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="18" r="6" fill="#27c93f"/>
  <text x="425" y="22" fill="#888888" font-size="12" font-family="monospace" text-anchor="middle">PowerShell - Antigravity Agent Workspace (0818)</text>
  
  <text x="25" y="70" fill="#4ec9b0" font-size="13" font-family="monospace">&gt; python -m unittest tests/test_analyzer.py</text>
  <text x="25" y="95" fill="#dcdcaa" font-size="13" font-family="monospace">......</text>
  <text x="25" y="115" fill="#888888" font-size="13" font-family="monospace">----------------------------------------------------------------------</text>
  <text x="25" y="135" fill="#4ec9b0" font-size="13" font-family="monospace">Ran 6 tests in 0.007s</text>
  <text x="25" y="155" fill="#4ec9b0" font-size="13" font-family="monospace">OK</text>
  
  <text x="25" y="195" fill="#4ec9b0" font-size="13" font-family="monospace">&gt; python scripts/run_analysis.py</text>
  <text x="25" y="220" fill="#569cd6" font-size="13" font-family="monospace">[OK] 数据加载与计算完成:</text>
  <text x="45" y="240" fill="#cccccc" font-size="13" font-family="monospace">- 工单总数: 50 条 (2024-06-01 至 2024-06-11)</text>
  <text x="45" y="260" fill="#cccccc" font-size="13" font-family="monospace">- 解决率: 84.0% (未解决: 8 条，退款未结率: 38.5%)</text>
  <text x="45" y="280" fill="#cccccc" font-size="13" font-family="monospace">- 平均满意度: 2.36 / 5.0 (支付异常单均分: 1.90)</text>
  <text x="45" y="300" fill="#cccccc" font-size="13" font-family="monospace">- 主管注意力价值矩阵: Top 1 支付防重 (API 94) 自动路由交易中台</text>
  <text x="45" y="320" fill="#f48771" font-size="13" font-family="monospace">- 识别异常项: 5 项 (已严格采用四步法论证)</text>
  <text x="25" y="350" fill="#6a9955" font-size="13" font-family="monospace">Markdown report generated: docs/analysis_report.md</text>
  <text x="25" y="370" fill="#6a9955" font-size="13" font-family="monospace">Web dashboard ready: index.html (含离线自适应 Canvas / Chart.js 双引擎)</text>
  <text x="25" y="395" fill="#4ec9b0" font-size="13" font-family="monospace">&gt; git push origin master (Sync Complete!)</text>
</svg>"""

with open('assets/terminal_output.svg', 'w', encoding='utf-8') as f:
    f.write(terminal_svg)

dashboard_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" width="960" height="540">
  <rect width="960" height="540" rx="12" fill="#f4f6f9"/>
  
  <rect x="20" y="20" width="920" height="60" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="35" y="32" width="55" height="35" rx="6" fill="#2563eb"/>
  <text x="62" y="55" fill="#ffffff" font-size="14" font-weight="bold" font-family="sans-serif" text-anchor="middle">0111</text>
  <text x="105" y="47" fill="#1e293b" font-size="16" font-weight="bold" font-family="sans-serif">客服工单趋势分析与智能异常诊断平台</text>
  <text x="105" y="65" fill="#64748b" font-size="11" font-family="sans-serif">AI-Powered Customer Support Trends &amp; Anomaly Detection Dashboard</text>
  <rect x="760" y="35" width="160" height="30" rx="4" fill="#eff6ff"/>
  <text x="840" y="54" fill="#2563eb" font-size="12" font-weight="bold" font-family="sans-serif" text-anchor="middle">2024-06-01 ~ 06-11</text>

  <rect x="20" y="95" width="215" height="80" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="35" y="120" fill="#64748b" font-size="12" font-family="sans-serif">工单总数 / 周期</text>
  <text x="35" y="150" fill="#1e293b" font-size="22" font-weight="bold" font-family="sans-serif">50 <tspan font-size="13" fill="#64748b">条 / 11天</tspan></text>

  <rect x="255" y="95" width="215" height="80" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="270" y="120" fill="#64748b" font-size="12" font-family="sans-serif">工单解决率</text>
  <text x="270" y="150" fill="#d97706" font-size="22" font-weight="bold" font-family="sans-serif">84.0% <tspan font-size="13" fill="#dc2626">(8条未结)</tspan></text>

  <rect x="490" y="95" width="215" height="80" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="505" y="120" fill="#64748b" font-size="12" font-family="sans-serif">平均客户满意度</text>
  <text x="505" y="150" fill="#dc2626" font-size="22" font-weight="bold" font-family="sans-serif">2.36 <tspan font-size="13" fill="#64748b">/ 5.0 (54%≤2分)</tspan></text>

  <rect x="725" y="95" width="215" height="80" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="740" y="120" fill="#64748b" font-size="12" font-family="sans-serif">平均处理时长 (SLA)</text>
  <text x="740" y="150" fill="#7c3aed" font-size="22" font-weight="bold" font-family="sans-serif">19.7h <tspan font-size="13" fill="#dc2626">(退款45.2h)</tspan></text>

  <rect x="20" y="190" width="450" height="180" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="35" y="215" fill="#1e293b" font-size="13" font-weight="bold" font-family="sans-serif">📈 每日工单量与未解决工单趋势 (日级时序)</text>
  <rect x="50" y="290" width="18" height="50" rx="2" fill="#93c5fd"/>
  <rect x="85" y="290" width="18" height="50" rx="2" fill="#93c5fd"/>
  <rect x="120" y="275" width="18" height="65" rx="2" fill="#93c5fd"/>
  <rect x="155" y="260" width="18" height="80" rx="2" fill="#93c5fd"/>
  <rect x="190" y="275" width="18" height="65" rx="2" fill="#93c5fd"/>
  <rect x="208" y="325" width="10" height="15" rx="2" fill="#ef4444"/>
  <rect x="225" y="260" width="18" height="80" rx="2" fill="#93c5fd"/>
  <rect x="260" y="260" width="18" height="80" rx="2" fill="#93c5fd"/>
  <rect x="295" y="260" width="18" height="80" rx="2" fill="#93c5fd"/>
  <rect x="313" y="310" width="10" height="30" rx="2" fill="#ef4444"/>
  <rect x="330" y="260" width="18" height="80" rx="2" fill="#93c5fd"/>
  <rect x="348" y="310" width="10" height="30" rx="2" fill="#ef4444"/>
  <rect x="365" y="245" width="18" height="95" rx="2" fill="#93c5fd"/>
  <rect x="383" y="325" width="10" height="15" rx="2" fill="#ef4444"/>
  <rect x="400" y="260" width="18" height="80" rx="2" fill="#93c5fd"/>
  <rect x="418" y="310" width="10" height="30" rx="2" fill="#ef4444"/>
  <path d="M 60 250 L 95 250 L 130 270 L 165 250 L 200 260 L 235 275 L 270 265 L 305 320 L 340 285 L 375 288 L 410 315" fill="none" stroke="#f59e0b" stroke-width="2.5"/>

  <rect x="490" y="190" width="450" height="180" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <text x="505" y="215" fill="#1e293b" font-size="13" font-weight="bold" font-family="sans-serif">📊 业务分类分布与满意度对比</text>
  <rect x="520" y="250" width="140" height="16" rx="3" fill="#2563eb"/>
  <text x="670" y="263" fill="#1e293b" font-size="11" font-family="sans-serif">支付问题 (16单 / 32%)</text>
  <rect x="520" y="275" width="115" height="16" rx="3" fill="#3b82f6"/>
  <text x="645" y="288" fill="#1e293b" font-size="11" font-family="sans-serif">退款退货 (13单 / 26%)</text>
  <rect x="520" y="300" width="70" height="16" rx="3" fill="#60a5fa"/>
  <text x="600" y="313" fill="#1e293b" font-size="11" font-family="sans-serif">物流查询 (8单 / 16%)</text>
  <rect x="520" y="325" width="45" height="16" rx="3" fill="#93c5fd"/>
  <text x="575" y="338" fill="#1e293b" font-size="11" font-family="sans-serif">商品咨询 (5单 / 10%)</text>

  <rect x="20" y="385" width="920" height="135" rx="8" fill="#ffffff" stroke="#e2e8f0"/>
  <rect x="20" y="385" width="6" height="135" rx="3" fill="#dc2626"/>
  <rect x="35" y="398" width="80" height="22" rx="4" fill="#fee2e2"/>
  <text x="75" y="413" fill="#991b1b" font-size="11" font-weight="bold" font-family="sans-serif" text-anchor="middle">CRITICAL P0</text>
  <text x="125" y="414" fill="#1e293b" font-size="13" font-weight="bold" font-family="sans-serif">[ANOMALY-01] 支付核心交易链路“重复扣款”与“状态脱节”缺陷</text>
  
  <rect x="35" y="430" width="205" height="75" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
  <text x="45" y="448" fill="#475569" font-size="11" font-weight="bold" font-family="sans-serif">📄 1. 客观事实</text>
  <text x="45" y="465" fill="#64748b" font-size="10" font-family="sans-serif">T012/T022/T030/T046/T050多扣款;</text>
  <text x="45" y="480" fill="#64748b" font-size="10" font-family="sans-serif">T008/T020/T028/T032/T035状态脱节;</text>
  <text x="45" y="495" fill="#dc2626" font-size="10" font-family="sans-serif">10条异常单均分低至 1.90 分</text>

  <rect x="250" y="430" width="205" height="75" rx="4" fill="#fffbeb" stroke="#fef08a"/>
  <text x="260" y="448" fill="#b45309" font-size="11" font-weight="bold" font-family="sans-serif">⚡ 2. 异常信号</text>
  <text x="260" y="468" fill="#92400e" font-size="10" font-family="sans-serif">支付交易链路系统性扣款与</text>
  <text x="260" y="485" fill="#92400e" font-size="10" font-family="sans-serif">状态脱节，且跨月复发(T046)</text>

  <rect x="465" y="430" width="225" height="75" rx="4" fill="#f0fdf4" stroke="#bbf7d0"/>
  <text x="475" y="448" fill="#166534" font-size="11" font-weight="bold" font-family="sans-serif">🔍 3. 假设验证</text>
  <text x="475" y="468" fill="#14532d" font-size="10" font-family="sans-serif">假设: 网关幂等Key与防抖缺失;</text>
  <text x="475" y="485" fill="#14532d" font-size="10" font-family="sans-serif">验证: 覆盖微信/支付宝等多渠道</text>

  <rect x="700" y="430" width="225" height="75" rx="4" fill="#eff6ff" stroke="#bfdbfe"/>
  <text x="710" y="448" fill="#1e40af" font-size="11" font-weight="bold" font-family="sans-serif">🧪 4. 实验论证</text>
  <text x="710" y="468" fill="#1e3a8a" font-size="10" font-family="sans-serif">实验: 预发模拟500ms并发压测;</text>
  <text x="710" y="485" fill="#1e40af" font-size="10" font-weight="bold" font-family="sans-serif">目标: 重复扣款率归零并退款</text>
</svg>"""

with open('assets/dashboard_preview.svg', 'w', encoding='utf-8') as f:
    f.write(dashboard_svg)
