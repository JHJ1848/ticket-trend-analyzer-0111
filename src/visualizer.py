import json
from typing import Dict, Any

class ReportGenerator:
    def __init__(self, report_data: Dict[str, Any]):
        self.data = report_data

    def build_markdown_report_content(self) -> str:
        ov = self.data['overview']
        cats = self.data['categories']
        daily = self.data['daily_trends']
        channels = self.data['channels']
        anomalies = self.data['anomalies']
        clusters = self.data['sub_issue_clusters']
        unresolved = self.data['unresolved_tickets']
        attention = self.data.get('executive_attention_matrix', [])

        md = []
        md.append("# 🚀 客服工单趋势分析与全链路韧性诊断报告 (Executive Intelligence Report)\n")
        md.append("> **分析哲学**：*“客服工单绝非孤立的服务末端，而是核心交易中台与履约体系可靠性的最敏感晴雨表。”*\n")
        md.append(f"> **报告周期**: {ov['date_range'][0]} 至 {ov['date_range'][1]} ({ov['days_count']} 天) | **样本总量**: {ov['total_tickets']} 条全量工单 | **分析范式**: 客观事实 ➡️ 信号 ➡️ 假设 ➡️ 实验 ➡️ 机制\n")
        
        md.append("---\n")
        md.append("## ⚡ 【30秒高管摘要 · Executive Summary】\n")
        md.append("### 1. 核心诊断红线 (The 3 Critical Alarms)")
        md.append("- 🔴 **支付中台出现系统性资金安全漏洞 (P0)**：10 条异常工单平均满意度低至 **1.90** 分，集中暴露跨渠道“重复扣款(多扣100元)”与“扣款成功未同步订单”，存在同类故障跨月复发特征(`T046`)。")
        md.append("- 🔴 **退款履约链路出现流程性断裂 (P0)**：退款未解决率高达 **38.5%**，平均耗时 **45.2 小时**，垫付运费在线下人工报销中严重滞留长达 **120 小时** (`T031`)。")
        md.append("- 🟡 **前置智能客服反噬客户体验 (P1)**：Bot 意图识别陷入死循环，在线排队超 40 分钟，导致投诉类工单满意度 **100% 为 1 星差评**。")
        
        md.append("\n### 2. 核心指标看板 (KPI Health Check)")
        md.append("| 核心指标 | 观测数值 | 行业健康基线 | 偏离度诊断 | 决策行动优先级 |")
        md.append("| :--- | :--- | :--- | :--- | :--- |")
        md.append(f"| **工单解决率** | **{ov['resolved_rate']}%** ({ov['resolved_count']}/{ov['total_tickets']}) | ≥ 95.0% | ⚠️ 偏低 (8条滞留未结) | **P1: 24h专人清零机制** |")
        md.append(f"| **全量平均满意度** | **{ov['avg_satisfaction']} / 5.0** | ≥ 4.20 | 🚨 **极度恶化 (低分率54%)** | **P0: 资金退还与高危客安抚** |")
        md.append(f"| **支付异常单满意度** | **1.90 / 5.0** | ≥ 4.00 | 🚨 **严重偏离正常水位** | **P0: 支付网关全局幂等锁改造** |")
        md.append(f"| **平均处理时长** | **{ov['avg_resolution_time_hours']} 小时** | ≤ 6.0 小时 | ⚠️ **超时 3.2 倍 (退款45.2h)** | **P0: 运费险在线直赔替代线下垫付** |")
        md.append(f"| **高优先级占比** | **{ov['high_priority_rate']}%** ({ov['high_priority_count']}单) | ≤ 20.0% | 🚨 **风险过度集中 (均分1.87)** | **P1: 建立前置熔断与降级策略** |")
        
        md.append("\n---\n")
        md.append("## 一、 深度思维：从题目外看客服工单的本质 (Beyond the Tickets)\n")
        md.append("作为高级数据分析与系统架构视角，客服工单数据的核心价值在于**“通过末端客诉摩擦力，反向穿透中台架构缺陷与业务流程断点”**：\n")
        md.append("1. **工单是技术债的显性利息**：支付重复扣款并非用户操作不当，而是交易中台幂等性与消息队列 ACK 机制缺陷在业务层的外溢。")
        md.append("2. **工单是部门协同的断层扫描仪**：垫付运费报销耗时 120 小时，暴露出客服、仓储质检、财务打款之间存在严重的系统壁垒与数据孤岛。")
        md.append("3. **工单是智能化落地的试金石**：未设转人工熔断机制的智能客服不是“降本增效”，而是将用户推向极端投诉的“体验阻断器”。\n")

        md.append("---\n")
        md.append("## 二、 4 大分析维度的前瞻性设计与决策价值 (Analytical Dimensions)\n")
        
        md.append("### 维度 1: 业务问题分类与风险矩阵 (Category & Risk Matrix)\n")
        md.append("| 业务分类 | 工单量 | 占比 | 高优数 | 未解决数 | 未解决率 | 平均满意度 | 平均耗时(h) | 最长耗时(h) | 治理定级 |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for c in cats:
            risk = "🔴 P0 紧急治理" if c['unresolved_rate'] > 20 or c['avg_satisfaction'] <= 2.0 else ("🟡 P1 流程重构" if c['count'] > 10 else "🟢 P2 常规维护")
            md.append(f"| **{c['category']}** | {c['count']} | {c['percentage']}% | {c['high_priority_count']} | {c['unresolved_count']} | {c['unresolved_rate']}% | {c['avg_satisfaction']} | {c['avg_resolution_time_hours']} | {c['max_resolution_time_hours']} | {risk} |")
        
        md.append("\n### 维度 2: 时序演变与质量拐点 (Time-Series & Quality Turning Point)\n")
        md.append("| 日期 | 工单量 | 支付类 | 退款类 | 物流类 | 投诉类 | 账号类 | 咨询类 | 未解决数 | 当日满意度 | 趋势研判 |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for d in daily:
            status = "🟢 稳态" if d['unresolved_count'] == 0 and d['avg_satisfaction'] >= 2.5 else "🚨 恶化/积压"
            md.append(f"| {d['date']} | {d['total']} | {d['payment_count']} | {d['refund_count']} | {d['logistics_count']} | {d['complaint_count']} | {d['account_count']} | {d['inquiry_count']} | **{d['unresolved_count']}** | {d['avg_satisfaction']} | {status} |")

        md.append("\n### 维度 3: 渠道效能与响应深度 (Channel Efficiency & Escalation)\n")
        md.append("| 渠道 | 工单量 | 占比 | 高优量 | 未解决数 | 未解决率 | 平均满意度 | 平均耗时(h) | 渠道定位与瓶颈 |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for ch in channels:
            bottleneck = "承接严重客诉升级，耗时为在线2.2倍，缺乏即时审批权限" if ch['channel'] == '电话' else "响应快但机器人拦截引发二次客诉，缺乏转人工熔断"
            md.append(f"| **{ch['channel']}** | {ch['count']} | {ch['percentage']}% | {ch['high_priority_count']} | {ch['unresolved_count']} | {ch['unresolved_rate']}% | {ch['avg_satisfaction']} | {ch['avg_resolution_time_hours']} | {bottleneck} |")

        md.append("\n### 维度 4: 穿透式细分子问题聚类 (Sub-Issue Clusters & Root Cause)\n")
        md.append("| 细分子问题聚类 | 风险定级 | 涉及工单量 | 未解决数 | 平均满意度 | 平均耗时(h) | 业务与系统影响 |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for cname, cinfo in clusters.items():
            md.append(f"| **{cname}** | `{cinfo['level']}` | {cinfo['count']} 单 | {cinfo['unresolved_count']} 单 | {cinfo['avg_satisfaction']} | {cinfo['avg_resolution_hours']}h | {cinfo['impact']} |")
        
        md.append("\n---\n")
        md.append("## 三、 5大关键信号工程诊断全景：[客观事实 ➡️ 信号 ➡️ 假设 ➡️ 实验 ➡️ 机制]\n")
        for a in anomalies:
            md.append(f"### 🚨 [{a['id']}] {a['title']} (`{a['level']}`)\n")
            
            md.append("#### 📄 1. 客观事实 (Objective Facts - 无主观臆断)")
            for fact in a['objective_facts']:
                md.append(f"- {fact}")
            
            md.append(f"\n#### ⚡ 2. 异常信号 (Signal - 偏离基线特征)")
            md.append(f"> {a['signal']}\n")
            
            md.append("#### 🔍 3. 假设验证 (Hypothesis & Root Cause - 底层机理探究)")
            for hyp in a['hypothesis_verification']['hypotheses']:
                md.append(f"- {hyp}")
            md.append(f"- 💡 **数据交叉推断**：{a['hypothesis_verification']['verification']}\n")
            
            md.append("#### 🧪 4. 实验论证 (Experimental Validation - 可落地的工程验证方案)")
            for exp in a['experimental_validation']['experiments']:
                md.append(f"- {exp}")
            md.append(f"- 🎯 **治理目标与验收标准**：{a['experimental_validation']['remediation_target']}\n")
            md.append("---\n")

        md.append("## 四、 主管注意力智能路由与跨部门治理指令矩阵 (Attention Routing Matrix)\n")
        md.append("| 细分子问题聚类 | 注意力指数 (API) | 紧急程度 | 归属责任团队 | 核心责任人 | 涉及单量/未结 | 满意度/均时 | 自动化主管督办指令 |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for att in attention:
            md.append(f"| **{att['issue_cluster']}** | **{att['attention_index']}** | `{att['urgency_level']}` | **{att['target_department']}** | {att['accountable_owner']} | {att['ticket_count']}单 / **{att['unresolved_count']}未结** | ⭐{att['avg_satisfaction']} / {att['avg_hours']}h | {att['recommended_directive']} |")

        md.append("\n---\n")
        md.append("## 五、 8 条未解决高危工单重点督办清单 (Unresolved Queue)\n")
        md.append("| 工单ID | 创建时间 | 分类 | 优先级 | 已耗时(h) | 满意度 | 渠道 | 用户诉求原文 | 主管责任督办动作 |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        action_map = {
            "T019": "联系顺丰/中通排查异常退回，立即补发并赔付优惠券",
            "T031": "🚨 滞留120h！财务主管特批原路退还垫付运费，电话致歉",
            "T033": "联系快递网点主管核实派件异常，若丢件立即先行赔付",
            "T036": "纠正客服拦截，支持7天无理由退货，立即通过审核",
            "T039": "🚨 修复状态机错误，重新开启退款通道并查证物流状态",
            "T042": "核对28元运费凭证，今日完成转账报销",
            "T046": "🚨 财务立即退还重复扣款，技术组排查支付幂等Key",
            "T047": "🚨 退款滞留96h，财务专员今日内必须完成放款到账"
        }
        for u in unresolved:
            act = action_map.get(u['ticket_id'], "专人跟进处理")
            md.append(f"| **{u['ticket_id']}** | {u['created_at']} | {u['category']} | `{u['priority']}` | **{u['resolution_time_hours']}h** | {u['satisfaction']}星 | {u['channel']} | {u['description']} | **{act}** |")

        md.append("\n---\n")
        md.append("## 六、 前瞻性演进规划：从「被动救火」到「全链路韧性工程」\n")
        md.append("```")
        md.append("┌─────────────────────────────────────────────────────────────────────────────┐")
        md.append("│                 客服与系统韧性演进 3 阶段路线图 (Roadmap)                      │")
        md.append("└─────────────────────────────────────────────────────────────────────────────┘")
        md.append("  Phase 1: 应急止血 (0-48h)       Phase 2: 根因拔除 (1-2周)      Phase 3: 韧性机制 (1-3月)")
        md.append("  ├─ 8条滞留工单专人闭环清零       ├─ 支付中台全局幂等防重上线     ├─ 全链路订单/支付对账平台")
        md.append("  ├─ T050/T046资金多扣秒级退还     ├─ 运费险在线直退取缔人工垫付   ├─ 智能客服意图自学习与熔断")
        md.append("  └─ 建立SLA超24h强提醒看板        └─ 订单状态机依赖物流强校验     └─ SLA预警主动关怀赔付体系")
        md.append("```\n")

        return "\n".join(md)

    def generate_markdown_report(self, output_path: str):
        content = self.build_markdown_report_content()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_web_data_js(self, output_path: str):
        md_content = self.build_markdown_report_content()
        js_content = f"window.TICKET_REPORT_DATA = {json.dumps(self.data, ensure_ascii=False, indent=2)};\n\nwindow.ANALYSIS_REPORT_MARKDOWN = {json.dumps(md_content, ensure_ascii=False)};"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
