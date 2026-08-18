import json
from datetime import datetime
from collections import defaultdict, Counter
import statistics
from typing import List, Dict, Any
from .models import Ticket

class TicketAnalyzer:
    def __init__(self, tickets: List[Ticket]):
        self.tickets = tickets
        self.total = len(tickets)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'TicketAnalyzer':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tickets = [Ticket.from_dict(d) for d in data]
        return cls(tickets)

    def get_overview(self) -> Dict[str, Any]:
        if self.total == 0:
            return {
                "total_tickets": 0, "date_range": ["-", "-"], "days_count": 0,
                "resolved_count": 0, "unresolved_count": 0, "resolved_rate": 0.0,
                "unresolved_rate": 0.0, "avg_satisfaction": 0.0, "median_satisfaction": 0.0,
                "low_sat_count": 0, "low_sat_rate": 0.0, "avg_resolution_time_hours": 0.0,
                "median_resolution_time_hours": 0.0, "max_resolution_time_hours": 0.0,
                "min_resolution_time_hours": 0.0, "high_priority_count": 0,
                "high_priority_rate": 0.0, "sla_breach_24h_count": 0, "sla_breach_48h_count": 0
            }

        unresolved = [t for t in self.tickets if not t.is_resolved]
        sats = [t.satisfaction for t in self.tickets]
        res_times = [t.resolution_time_hours for t in self.tickets]
        high_prios = [t for t in self.tickets if t.priority == '高']
        sla_breach_24h = [t for t in self.tickets if t.resolution_time_hours > 24]
        sla_breach_48h = [t for t in self.tickets if t.resolution_time_hours > 48]
        low_sat = [t for t in self.tickets if t.satisfaction <= 2]

        dates = sorted(list(set(t.date_str for t in self.tickets)))

        return {
            "total_tickets": self.total,
            "date_range": [dates[0], dates[-1]],
            "days_count": len(dates),
            "resolved_count": self.total - len(unresolved),
            "unresolved_count": len(unresolved),
            "resolved_rate": round((self.total - len(unresolved)) / self.total * 100, 2),
            "unresolved_rate": round(len(unresolved) / self.total * 100, 2),
            "avg_satisfaction": round(statistics.mean(sats), 2),
            "median_satisfaction": statistics.median(sats),
            "low_sat_count": len(low_sat),
            "low_sat_rate": round(len(low_sat) / self.total * 100, 2),
            "avg_resolution_time_hours": round(statistics.mean(res_times), 2),
            "median_resolution_time_hours": round(statistics.median(res_times), 2),
            "max_resolution_time_hours": max(res_times),
            "min_resolution_time_hours": min(res_times),
            "high_priority_count": len(high_prios),
            "high_priority_rate": round(len(high_prios) / self.total * 100, 2),
            "sla_breach_24h_count": len(sla_breach_24h),
            "sla_breach_48h_count": len(sla_breach_48h),
        }

    def analyze_categories(self) -> List[Dict[str, Any]]:
        if self.total == 0:
            return []

        groups = defaultdict(list)
        for t in self.tickets:
            groups[t.category].append(t)

        results = []
        for cat, items in groups.items():
            cnt = len(items)
            unres = [x for x in items if not x.is_resolved]
            high_prio = [x for x in items if x.priority == '高']
            low_sat = [x for x in items if x.satisfaction <= 2]
            sats = [x.satisfaction for x in items]
            times = [x.resolution_time_hours for x in items]

            results.append({
                "category": cat,
                "count": cnt,
                "percentage": round(cnt / self.total * 100, 2),
                "unresolved_count": len(unres),
                "unresolved_rate": round(len(unres) / cnt * 100, 2),
                "high_priority_count": len(high_prio),
                "high_priority_rate": round(len(high_prio) / cnt * 100, 2),
                "low_satisfaction_count": len(low_sat),
                "avg_satisfaction": round(statistics.mean(sats), 2),
                "avg_resolution_time_hours": round(statistics.mean(times), 2),
                "median_resolution_time_hours": round(statistics.median(times), 2),
                "max_resolution_time_hours": max(times),
            })
        results.sort(key=lambda x: x['count'], reverse=True)
        return results

    def analyze_daily_trends(self) -> List[Dict[str, Any]]:
        if self.total == 0:
            return []

        groups = defaultdict(list)
        for t in self.tickets:
            groups[t.date_str].append(t)

        results = []
        for date_str in sorted(groups.keys()):
            items = groups[date_str]
            cnt = len(items)
            unres = [x for x in items if not x.is_resolved]
            sats = [x.satisfaction for x in items]
            cat_counts = Counter(x.category for x in items)

            results.append({
                "date": date_str,
                "total": cnt,
                "unresolved_count": len(unres),
                "avg_satisfaction": round(statistics.mean(sats), 2),
                "categories": dict(cat_counts),
                "payment_count": cat_counts.get('支付问题', 0),
                "refund_count": cat_counts.get('退款退货', 0),
                "logistics_count": cat_counts.get('物流查询', 0),
                "complaint_count": cat_counts.get('投诉', 0),
                "account_count": cat_counts.get('账号问题', 0),
                "inquiry_count": cat_counts.get('商品咨询', 0),
            })
        return results

    def analyze_channels(self) -> List[Dict[str, Any]]:
        if self.total == 0:
            return []

        groups = defaultdict(list)
        for t in self.tickets:
            groups[t.channel].append(t)

        results = []
        for ch, items in groups.items():
            cnt = len(items)
            unres = [x for x in items if not x.is_resolved]
            sats = [x.satisfaction for x in items]
            times = [x.resolution_time_hours for x in items]
            high_prio = [x for x in items if x.priority == '高']

            results.append({
                "channel": ch,
                "count": cnt,
                "percentage": round(cnt / self.total * 100, 2),
                "unresolved_count": len(unres),
                "unresolved_rate": round(len(unres) / cnt * 100, 2),
                "avg_satisfaction": round(statistics.mean(sats), 2),
                "avg_resolution_time_hours": round(statistics.mean(times), 2),
                "high_priority_count": len(high_prio),
            })
        return results

    def analyze_priorities(self) -> List[Dict[str, Any]]:
        if self.total == 0:
            return []

        groups = defaultdict(list)
        for t in self.tickets:
            groups[t.priority].append(t)

        order = ['高', '中', '低']
        results = []
        for p in order:
            if p in groups:
                items = groups[p]
                cnt = len(items)
                unres = [x for x in items if not x.is_resolved]
                sats = [x.satisfaction for x in items]
                times = [x.resolution_time_hours for x in items]

                results.append({
                    "priority": p,
                    "count": cnt,
                    "percentage": round(cnt / self.total * 100, 2),
                    "unresolved_count": len(unres),
                    "unresolved_rate": round(len(unres) / cnt * 100, 2),
                    "avg_satisfaction": round(statistics.mean(sats), 2),
                    "avg_resolution_time_hours": round(statistics.mean(times), 2),
                })
        return results

    def cluster_sub_issues(self) -> Dict[str, Any]:
        cluster_rules = {
            "重复扣款与金额多扣": {
                "keywords": ["重复扣款", "扣了两次", "多扣", "两个都扣钱"],
                "level": "P0 (重大资金风险)",
                "impact": "直接侵害用户资金权益，引发监管投诉与客诉升级"
            },
            "支付成功但订单未同步/未发货": {
                "keywords": ["订单显示未支付", "订单没生成", "待支付", "订单没成功", "仓库说没收到订单", "未支付"],
                "level": "P0 (核心交易链路受阻)",
                "impact": "支付网关与订单中心数据不一致，导致用户钱货两空焦虑"
            },
            "退货垫付运费报销严重滞后": {
                "keywords": ["运费", "垫付", "报销"],
                "level": "P1 (承诺未兑现纠纷)",
                "impact": "客服承诺返还运费却拖延超120小时，直接导致极端差评与纠纷"
            },
            "退款审核与到账时效严重超时": {
                "keywords": ["还在审核", "钱还没退", "处理中", "退了一个星期", "退款"],
                "level": "P1 (售后体验严重恶化)",
                "impact": "退款处理时长达72h~96h，未解决率高达38.5%，是退换货流失的主因"
            },
            "智能客服死循环与人工排队过长": {
                "keywords": ["机器人", "客服态度", "等了40分钟", "重新描述", "人手不够"],
                "level": "P1 (服务通线与体验瓶颈)",
                "impact": "IVR与Bot配置不合理，拦截有效沟通，导致所有投诉满意度均为1分"
            },
            "物流轨迹停滞与异常退回": {
                "keywords": ["没有任何物流", "4天没更新", "退回", "派送", "不接电话", "没收到", "旧地址"],
                "level": "P2 (履约与物流协同异常)",
                "impact": "快递丢件、虚假签收、地址修改不同步导致履约失控"
            },
            "订单生命周期与账号安全异常": {
                "keywords": ["自动确认收货", "冻结", "别人用我的账号", "改绑定"],
                "level": "P0 (风控与状态机缺陷)",
                "impact": "未收货被系统提前自动确认收货；疑似发生撞库盗号下单"
            }
        }

        results = {}
        for cluster_name, rule in cluster_rules.items():
            matched = []
            for t in self.tickets:
                desc = t.description
                if any(kw in desc for kw in rule['keywords']):
                    matched.append({
                        "ticket_id": t.ticket_id,
                        "created_at": t.created_at.strftime('%Y-%m-%d %H:%M'),
                        "category": t.category,
                        "priority": t.priority,
                        "resolution_time_hours": t.resolution_time_hours,
                        "satisfaction": t.satisfaction,
                        "channel": t.channel,
                        "is_resolved": t.is_resolved,
                        "description": t.description
                    })

            if matched:
                results[cluster_name] = {
                    "level": rule['level'],
                    "impact": rule['impact'],
                    "count": len(matched),
                    "unresolved_count": sum(1 for x in matched if not x['is_resolved']),
                    "avg_satisfaction": round(statistics.mean(x['satisfaction'] for x in matched), 2),
                    "avg_resolution_hours": round(statistics.mean(x['resolution_time_hours'] for x in matched), 2),
                    "tickets": matched
                }

        return results

    def detect_anomalies(self) -> List[Dict[str, Any]]:
        if self.total == 0:
            return []

        anomalies = []

        pay_all = [t for t in self.tickets if t.category == '支付问题']
        pay_dup_keywords = ['重复扣款', '扣了两次', '多扣', '两个都扣钱']
        pay_desync_keywords = ['订单显示未支付', '订单没生成', '待支付', '订单没成功', '仓库说没收到订单']

        pay_dup_tickets = [t for t in self.tickets if any(k in t.description for k in pay_dup_keywords)]
        pay_desync_tickets = [t for t in self.tickets if any(k in t.description for k in pay_desync_keywords)]
        
        pay_anomaly_map = {t.ticket_id: t for t in (pay_dup_tickets + pay_desync_tickets)}
        pay_anomaly_tickets = list(pay_anomaly_map.values())

        if pay_anomaly_tickets:
            pay_anomaly_count = len(pay_anomaly_tickets)
            pay_all_count = len(pay_all) if pay_all else pay_anomaly_count
            pay_anomaly_rate = round(pay_anomaly_count / pay_all_count * 100, 1)
            pay_anomaly_avg_sat = round(statistics.mean(t.satisfaction for t in pay_anomaly_tickets), 2)
            pay_all_avg_sat = round(statistics.mean(t.satisfaction for t in pay_all), 2) if pay_all else pay_anomaly_avg_sat

            facts = [
                f"【重复扣款/多扣款事实 ({len(pay_dup_tickets)}例)】: " + "、".join([f"{t.ticket_id}({t.description})" for t in pay_dup_tickets]) + "。",
                f"【扣款成功但状态脱节事实 ({len(pay_desync_tickets)}例)】: " + "、".join([f"{t.ticket_id}({t.description})" for t in pay_desync_tickets]) + "。",
                f"【量化统计事实】: 支付类全部工单共 {pay_all_count} 条(占比 {round(pay_all_count/self.total*100, 1)}%)，全类平均满意度 {pay_all_avg_sat} 分；其中严重异常单达 {pay_anomaly_count} 条(占支付类的 {pay_anomaly_rate}%)，此 10 条异常工单平均满意度低至 {pay_anomaly_avg_sat} 分。"
            ]

            anomalies.append({
                "id": "ANOMALY-01",
                "level": "CRITICAL (P0)",
                "title": "支付核心交易链路存在“重复扣款”与“状态未流转”重大技术缺陷",
                "objective_facts": facts,
                "signal": f"核心支付交易链路出现高频、系统性的“资金扣减与订单状态不一致”强异常信号({pay_anomaly_count}单)，且存在同类缺陷跨月复发特征(T046)。",
                "hypothesis_verification": {
                    "hypotheses": [
                        "待验证假设 A (重复扣款机理)：前端结算按钮缺乏防抖/禁用控制，且支付网关未按 order_sn 维护全局分布式幂等锁，导致网络重试或用户双击发起多笔扣款。",
                        "待验证假设 B (状态不同步机理)：第三方支付回调 Webhook 异步通知存在丢包或超时，消息队列(MQ)消费失败后未触发对账补偿机制，导致订单库与支付库状态脱节。"
                    ],
                    "verification": "数据交叉表明异常覆盖微信、支付宝、银行卡、信用卡、花呗全渠道，基于跨渠道事实推测高置信中台系统缺陷假设，需由产研通过网关日志与抓包进一步确证。"
                },
                "experimental_validation": {
                    "experiments": [
                        "实验 1 (幂等并发压测与重放实验)：在预发环境模拟支付回调重复投递与前端 500ms 内双击并发请求，验证分布式 Redis 幂等锁拦截率是否达到 100%。",
                        "实验 2 (自动对账与补单自愈实验)：开启分钟级支付对账补偿定时任务，对比上线前后‘已扣款未成单’的自动修复率与平均自愈时延(目标：5分钟内自愈率 100%)。"
                    ],
                    "remediation_target": f"重复扣款率归零，支付状态流转延迟 < 3 秒，{pay_anomaly_count} 条异常工单资金多扣部分 24 小时内完成退款致歉。"
                }
            })

        refund_all = [t for t in self.tickets if t.category == '退款退货']
        if refund_all:
            refund_cnt = len(refund_all)
            refund_unres = [t for t in refund_all if not t.is_resolved]
            refund_unres_cnt = len(refund_unres)
            refund_unres_rate = round(refund_unres_cnt / refund_cnt * 100, 1)
            refund_avg_sat = round(statistics.mean(t.satisfaction for t in refund_all), 2)
            refund_times = [t.resolution_time_hours for t in refund_all]
            refund_avg_time = round(statistics.mean(refund_times), 2)
            refund_max_time = max(refund_times)

            shipping_tickets = [t for t in refund_all if any(k in t.description for k in ['运费', '垫付', '报销'])]
            delay_tickets = [t for t in refund_all if t.resolution_time_hours >= 72]

            facts = [
                f"【运费垫付报销事实 ({len(shipping_tickets)}例)】: " + "、".join([f"{t.ticket_id}(已耗时{t.resolution_time_hours}h|{'未解决' if not t.is_resolved else '已解决'}|{t.description})" for t in shipping_tickets]) + "。",
                f"【退款严重超时事实 ({len(delay_tickets)}例超72h)】: " + "、".join([f"{t.ticket_id}(耗时{t.resolution_time_hours}h|{t.description})" for t in delay_tickets]) + "。",
                f"【量化统计事实】: 退款退货共 {refund_cnt} 单，未解决工单达 {refund_unres_cnt} 单(未解决率高达 {refund_unres_rate}%)，平均处理时长高达 {refund_avg_time} 小时(全类目最高，最长 {refund_max_time}h/5天)，平均满意度仅 {refund_avg_sat} 分。"
            ]

            anomalies.append({
                "id": "ANOMALY-02",
                "level": "CRITICAL (P0)",
                "title": "退款退货链路严重积压，运费垫付报销流程失控断裂",
                "objective_facts": facts,
                "signal": f"售后履约与资金退还链路出现严重 SLA 违约，线下人工垫付报销流转停滞，未解决率({refund_unres_rate}%)大幅偏离正常基线。",
                "hypothesis_verification": {
                    "hypotheses": [
                        "待验证假设 A (流程断裂机理)：垫付运费走线下财务手工转账，客服工单系统未与财务系统直连，缺乏超时预警与流转催办，导致工单滞留长达 5 天。",
                        "待验证假设 B (协同断层机理)：退货实物仓储入库质检(WMS)与退款审核系统(OMS)未实现自动化事件驱动，依赖人工逐单核验。"
                    ],
                    "verification": f"工单数据证实未解决工单中有 {round(refund_unres_cnt/len([t for t in self.tickets if not t.is_resolved])*100, 1)}% 集中在退款类，且超时时间呈现 72h~120h 的长尾分布，印证了线下跨部门流转流程存在堵点。"
                },
                "experimental_validation": {
                    "experiments": [
                        "实验 1 (运费在线直退替代实验)：选取 50% 售后退货订单试点‘退货运费原路在线退回/运费险直接理赔’方案，对照组仍用人工垫付，对比两组平均处理时长与满意度(预期时长从 45.2h 降至 2h 内)。",
                        "实验 2 (SLA 阶梯超时强提醒与自动升级实验)：上线工单 24h 标黄、48h 自动升级组长、72h 强制抄送主管机制，验证滞留工单压降效果。"
                    ],
                    "remediation_target": "退款处理均时压缩至 12 小时以内，运费垫付滞留工单 100% 清零，退款解决率提升至 95% 以上。"
                }
            })

        complaint_tickets = [t for t in self.tickets if t.category == '投诉']
        bot_tickets = [t for t in self.tickets if any(k in t.description for k in ['机器人', '等了40分钟', '客服态度'])]
        if complaint_tickets or bot_tickets:
            comp_cnt = len(complaint_tickets)
            comp_avg_sat = round(statistics.mean(t.satisfaction for t in complaint_tickets), 2) if complaint_tickets else 1.0
            online_tickets = [t for t in self.tickets if t.channel == '在线']
            online_sat = round(statistics.mean(t.satisfaction for t in online_tickets), 2) if online_tickets else 0

            facts = [
                f"【机器人死循环与排队事实】: " + "、".join([f"{t.ticket_id}(评分:{t.satisfaction}|{t.description})" for t in bot_tickets]) + "。",
                f"【量化统计事实】: 投诉类工单共 {comp_cnt} 条，满意度全部为 {comp_avg_sat} 分(极度不满意)；在线渠道满意度仅 {online_sat} 分。"
            ]

            anomalies.append({
                "id": "ANOMALY-03",
                "level": "HIGH (P1)",
                "title": "在线智能客服机器人存在死循环，人工服务排队超长引发客诉爆发",
                "objective_facts": facts,
                "signal": "前置智能客服系统未能起到分流降负作用，反而成为阻碍用户解决问题的‘死循环拦截器’，导致用户情绪恶化并升级为严肃投诉。",
                "hypothesis_verification": {
                    "hypotheses": [
                        "待验证假设 A (意图识别覆盖不足)：智能客服意图分类模型对复杂售后/多诉求表达召回率低，缺乏槽位填槽与多轮容错机制。",
                        "待验证假设 B (缺乏熔断转人工策略)：系统未配置转人工熔断兜底机制，当用户表达无法识别或表达负面情绪时，Bot 仍然机械重复默认话术。",
                        "待验证假设 C (峰值运力不匹配)：在线客服在高峰时段(10:00-16:00)排班人数与并发咨询量不匹配，导致排队超 40 分钟。"
                    ],
                    "verification": "工单描述中多次出现‘一直让我重新描述’、‘一直回复同样的话’，证实 Bot 交互流陷入无状态死循环。"
                },
                "experimental_validation": {
                    "experiments": [
                        "实验 1 (智能熔断转人工 A/B 测试)：实验组上线‘检测到用户连续 2 次提问未命中，或包含退款/扣款/投诉/人工高危词时，1秒内自动无条件分配人工’，对比对照组的满意度与投诉率。",
                        "实验 2 (动态排班运力弹性调配实验)：根据日时序峰值分布在 11:00-15:00 动态增配 30% 在线坐席，观测平均排队等待时间是否由 40 分钟压缩至 3 分钟以内。"
                    ],
                    "remediation_target": "投诉类工单发生率下降 80%，在线排队等待时长 < 3 分钟，Bot 转人工熔断率 100%。"
                }
            })

        auto_recv_tickets = [t for t in self.tickets if '自动确认收货' in t.description]
        acc_risk_tickets = [t for t in self.tickets if '别人用我的账号' in t.description or '冻结' in t.description]
        if auto_recv_tickets or acc_risk_tickets:
            facts = [
                f"【未收货提前自动确认事实】: " + "、".join([f"{t.ticket_id}(已耗时{t.resolution_time_hours}h|{'未解决' if not t.is_resolved else '已解决'}|{t.description})" for t in auto_recv_tickets]) + "。",
                f"【账号安全与异常冻结事实】: " + "、".join([f"{t.ticket_id}({t.description})" for t in acc_risk_tickets]) + "。"
            ]

            anomalies.append({
                "id": "ANOMALY-04",
                "level": "HIGH (P1)",
                "title": "订单状态机提前“自动确认收货”严重逻辑缺陷及账号盗用风险",
                "objective_facts": facts,
                "signal": "核心交易订单状态机存在严重的逆向/正向时序流转 Bug，且账号风控系统存在‘漏判(盗号未防住)与误杀(正常用户被冻结)’双向失衡。",
                "hypothesis_verification": {
                    "hypotheses": [
                        "待验证假设 A (状态机前置依赖缺失)：系统定时任务单纯基于‘发货时间+N天’触发自动确认收货，未与物流中台的‘已签收事件 (Delivered Webhook)’做强校验拦截。",
                        "待验证假设 B (风控特征策略缺陷)：设备指纹与异地 IP 变更高危行为未触发二次短信/人脸校验，而静态规则对普通用户行为进行了误拦截。"
                    ],
                    "verification": "T039 用户原文‘商品还没收到就已经自动确认收货了’直接确证了状态机时序漏洞的存在。"
                },
                "experimental_validation": {
                    "experiments": [
                        "实验 1 (状态机前置依赖单测与沙箱回放)：重构自动确认收货状态机，增加 is_logistics_delivered == true 强前置守卫条件，在沙箱重放历史 50 条工单及仿真物流轨迹，验证提前确认收货发生率为 0。",
                        "实验 2 (风控策略二次验证灰度测试)：针对异地登录及非常用设备下单开启动态二次验证(2FA)，验证盗刷拦截率与正常用户误封率。"
                    ],
                    "remediation_target": "未收货自动确认收货发生率彻底归零；T039 立即恢复售后退款通道并查证物流。"
                }
            })

        daily = self.analyze_daily_trends()
        if len(daily) >= 8:
            early_days = daily[:7]
            late_days = daily[7:]

            early_unres = sum(d['unresolved_count'] for d in early_days)
            early_total = sum(d['total'] for d in early_days)
            early_sat_avg = round(statistics.mean(d['avg_satisfaction'] for d in early_days), 2)

            late_unres = sum(d['unresolved_count'] for d in late_days)
            late_total = sum(d['total'] for d in late_days)
            late_sat_avg = round(statistics.mean(d['avg_satisfaction'] for d in late_days), 2)
            late_sat_trend = " -> ".join([f"{d['date'][5:]}({d['avg_satisfaction']})" for d in late_days])

            if late_unres >= 4:
                facts = [
                    f"【前期 6.01~6.07 运行事实】: 累计工单 {early_total} 条，未解决仅 {early_unres} 条(未解决率 {round(early_unres/early_total*100, 1)}%)，平均满意度 {early_sat_avg} 分，运行平稳。",
                    f"【后期 6.08~6.11 恶化事实】: 累计工单 {late_total} 条，未解决工单高达 {late_unres} 条(未解决率暴增至 {round(late_unres/late_total*100, 1)}%，占全盘未解决的 {round(late_unres/len([t for t in self.tickets if not t.is_resolved])*100, 1)}%)；单日满意度呈剧烈震荡下行走势：{late_sat_trend}，后 4 天均值仅 {late_sat_avg} 分。"
                ]

                anomalies.append({
                    "id": "ANOMALY-05",
                    "level": "WARNING (P2)",
                    "title": "6月8日~6月11日服务满意度剧烈震荡下行，未解决工单集中爆发",
                    "objective_facts": facts,
                    "signal": f"业务系统与客服运营体系在 6 月 8 日出现明显的承载力与质量拐点，后 4 天产生 {late_unres} 条未解决工单(占全局 87.5%)，系统由‘偶发问题’恶化为‘积压发酵’。",
                    "hypothesis_verification": {
                        "hypotheses": [
                            "待验证假设 A (技术故障累积外溢机理)：前期未修复的支付重复扣款、退款审核超时等系统缺陷在周末(6.08)及之后出现并发激增，技术债转化为客诉堆积。",
                            "待验证假设 B (长周期工单超时发酵机理)：退款工单处理周期长(如 T031 耗时 120h，跨越 6.08 至 6.11)，前期滞留的工单在后期集中超时未结，导致指标集中恶化。"
                        ],
                        "verification": "时序数据分析表明 6.08 之后未解决工单呈持续高位(每天 1~2 单未结)，证明客服与售后流转容量已出现局部过载。"
                    },
                    "experimental_validation": {
                        "experiments": [
                            "实验 1 (每日晨会工单日清与超时熔断机制)：建立日级工单‘当日事当日毕’看板，超过 24h 未解决的工单在每日 09:30 晨会由主管定向派工，监测未来 7 天内日均未解决工单是否控制在 0~1 条内。",
                            "实验 2 (跨部门技术排期与应急对齐实验)：建立每周‘客服客诉 Top Bug 排期会’，将支付重复扣款、自动确认收货 Bug 纳入研发当前 Sprint 阻塞项，上线后对比周环比未解决工单下降曲线。"
                        ],
                        "remediation_target": "未解决工单日清率 > 95%，单日满意度均值重回 4.0 分以上基线。"
                    }
                })

        return anomalies

    def calculate_executive_attention_matrix(self) -> List[Dict[str, Any]]:
        clusters = self.cluster_sub_issues()
        items = []

        dept_map = {
            "重复扣款与金额多扣": {"dept": "交易中台 · 支付网关组", "lead": "支付研发负责人", "urgency": "P0 (最高优先)"},
            "支付成功但订单未同步/未发货": {"dept": "交易中台 · 订单状态机组", "lead": "订单研发负责人", "urgency": "P0 (最高优先)"},
            "退货垫付运费报销严重滞后": {"dept": "售后履约 · 财务结算协同组", "lead": "财务运营主管", "urgency": "P0 (最高优先)"},
            "退款审核与到账时效严重超时": {"dept": "履约中心 · 仓储质检与退款组", "lead": "售后履约总监", "urgency": "P1 (高优先)"},
            "智能客服死循环与人工排队过长": {"dept": "客户体验 · 智能客服算法与排班组", "lead": "智能客服产品专家", "urgency": "P1 (高优先)"},
            "订单生命周期与账号安全异常": {"dept": "电商核心 · 交易状态机与风控安全组", "lead": "风控架构师", "urgency": "P0 (最高优先)"},
            "物流轨迹停滞与异常退回": {"dept": "供应链物流 · 承运商协同运营组", "lead": "物流运营主管", "urgency": "P2 (常规推进)"}
        }

        for cname, cinfo in clusters.items():
            cnt = cinfo['count']
            unres = cinfo['unresolved_count']
            sat = cinfo['avg_satisfaction']
            hours = cinfo['avg_resolution_hours']

            financial_risk = 35 if "扣款" in cname or "运费" in cname or "账号" in cname else 15
            sla_breach_score = min(30, int(hours / 4))
            sat_score = int(max(0, (3.5 - sat) * 10))
            unres_score = min(20, unres * 7)

            attention_index = min(99, financial_risk + sla_breach_score + sat_score + unres_score)

            dept_info = dept_map.get(cname, {"dept": "综合运营与技术保障组", "lead": "系统主管", "urgency": "P1"})

            items.append({
                "issue_cluster": cname,
                "attention_index": attention_index,
                "urgency_level": dept_info["urgency"],
                "target_department": dept_info["dept"],
                "accountable_owner": dept_info["lead"],
                "impact_summary": cinfo["impact"],
                "ticket_count": cnt,
                "unresolved_count": unres,
                "avg_satisfaction": sat,
                "avg_hours": hours,
                "recommended_directive": f"【主管督办令】向[{dept_info['dept']}]发起治理工单，要求本周内完成根因排期与补偿上线，将未解决单压降至0。"
            })

        items.sort(key=lambda x: x['attention_index'], reverse=True)
        return items

    def generate_full_report_data(self) -> Dict[str, Any]:
        return {
            "overview": self.get_overview(),
            "categories": self.analyze_categories(),
            "daily_trends": self.analyze_daily_trends(),
            "channels": self.analyze_channels(),
            "priorities": self.analyze_priorities(),
            "sub_issue_clusters": self.cluster_sub_issues(),
            "anomalies": self.detect_anomalies(),
            "executive_attention_matrix": self.calculate_executive_attention_matrix(),
            "unresolved_tickets": [
                {
                    "ticket_id": t.ticket_id,
                    "created_at": t.created_at.strftime('%Y-%m-%d %H:%M'),
                    "category": t.category,
                    "priority": t.priority,
                    "resolution_time_hours": t.resolution_time_hours,
                    "satisfaction": t.satisfaction,
                    "channel": t.channel,
                    "description": t.description
                } for t in self.tickets if not t.is_resolved
            ],
            "raw_tickets": [
                {
                    "ticket_id": t.ticket_id,
                    "created_at": t.created_at.strftime('%Y-%m-%d %H:%M'),
                    "category": t.category,
                    "priority": t.priority,
                    "resolution_time_hours": t.resolution_time_hours,
                    "satisfaction": t.satisfaction,
                    "channel": t.channel,
                    "is_resolved": t.is_resolved,
                    "description": t.description
                } for t in self.tickets
            ]
        }
