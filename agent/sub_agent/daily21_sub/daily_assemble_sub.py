class DailyAssembleSub:
    async def assemble(self, data):
        """Format rich daily report from structured data"""
        date = data.get("date", "")
        summary = data.get("summary", {})
        today_due = data.get("today_due", [])
        overdue = data.get("overdue", [])
        upcoming = data.get("upcoming", [])
        completed = data.get("completed", [])
        by_user = data.get("grouped_by_user", {})

        lines = []
        lines.append(f"📋 **21点日报 | {date}**")
        lines.append("")

        # Summary
        lines.append("📊 **总览**")
        stats = []
        if summary.get("today_due"):
            stats.append(f"今日到期：**{summary['today_due']}条**")
        if summary.get("overdue"):
            stats.append(f"已延期：**{summary['overdue']}条**")
        if summary.get("upcoming"):
            stats.append(f"即将到期：**{summary['upcoming']}条**")
        if summary.get("completed_today"):
            stats.append(f"今日完成：**{summary['completed_today']}件**")
        stats.append(f"未完成总计：**{summary.get('total_uncompleted', 0)}条**")
        for s in stats:
            lines.append(f"- {s}")
        lines.append("")

        # Today due
        if today_due:
            lines.append("🔴 **今日到期 ⚠️**")
            for t in today_due:
                p = "🔴P0" if "P0" in (t.get("priority") or "") else "🟡P1"
                lines.append(f"1. **{t['title']}** → {t['user']} | {p}")
            lines.append("")

        # Overdue
        if overdue:
            lines.append("⏰ **已延期（逾期未完成）**")
            for t in overdue:
                p = "🔴P0" if "P0" in (t.get("priority") or "") else "🟡P1"
                lines.append(f"- **{t['title']}** → {t['user']} | {p} | 原定{t['deadline']}")
            lines.append("")

        # Upcoming
        if upcoming:
            lines.append("📅 **即将到期**")
            for t in upcoming[:10]:  # top 10
                p = "🔴P0" if "P0" in (t.get("priority") or "") else "🟡P1"
                lines.append(f"- **{t['title']}** → {t['user']} | {p} | 还有{t['days_until']}天")
            if len(upcoming) > 10:
                lines.append(f"- ...还有 {len(upcoming) - 10} 条")
            lines.append("")

        # By user aggregation
        if by_user:
            lines.append("👤 **按负责人统计**")
            for name, v in sorted(by_user.items(), key=lambda x: -x[1]["overdue"]):
                parts = []
                if v["overdue"]:
                    parts.append(f"延期{v['overdue']}条")
                if v["pending"]:
                    parts.append(f"待办{v['pending']}条")
                if v["high_priority"]:
                    parts.append(f"高优{v['high_priority']}条")
                lines.append(f"- {name}：{'，'.join(parts)}")
            lines.append("")

        # Completed today
        if completed:
            lines.append("✅ **近期完成**")
            for t in completed:
                lines.append(f"- {t['title']} ✅{'（' + t['user'] + '）' if t.get('user') else ''}")
            lines.append("")

        # Suggestion
        long_overdue_users = [n for n, v in by_user.items() if v.get("overdue", 0) >= 3]
        if long_overdue_users:
            lines.append("💡 **建议：** " +
                         f"{'、'.join(long_overdue_users)}有大量已延期任务，建议清点后删除或重新设定截止日期。")

        content = "\n".join(lines)
        return {"success": True, "data": content}
