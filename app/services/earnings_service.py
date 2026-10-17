import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.database import get_db
from app.models import EarningCreate, EarningUpdate, EarningResponse, PeriodSummary, EarningsSummaryResponse

def calculate_net_earnings(gross: float, tips_incentives: float, expenses: float) -> float:
    """Strict business logic calculation: Net = Gross + Tips/Incentives - Expenses."""
    return round(float(gross) + float(tips_incentives) - float(expenses), 2)

def create_earning_entry(data: EarningCreate, session_id: str) -> EarningResponse:
    net = calculate_net_earnings(data.gross_earnings, data.tips_incentives, data.expenses)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO earnings (session_id, date, category, platform, gross_earnings, tips_incentives, expenses, net_earnings, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            data.date,
            data.category,
            data.platform,
            round(data.gross_earnings, 2),
            round(data.tips_incentives, 2),
            round(data.expenses, 2),
            net,
            data.notes
        ))
        conn.commit()
        entry_id = cursor.lastrowid
        cursor.execute("SELECT * FROM earnings WHERE id = ? AND session_id = ?", (entry_id, session_id))
        row = cursor.fetchone()
        return EarningResponse(**dict(row))

def get_all_earnings(
    session_id: str,
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    platform: Optional[str] = None
) -> List[EarningResponse]:
    query = "SELECT * FROM earnings WHERE session_id = ?"
    params = [session_id]
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if category:
        query += " AND category = ?"
        params.append(category)
    if platform:
        query += " AND platform = ?"
        params.append(platform)
        
    query += " ORDER BY date DESC, id DESC"
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [EarningResponse(**dict(r)) for r in rows]

def get_earning_by_id(earning_id: int, session_id: str) -> Optional[EarningResponse]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM earnings WHERE id = ? AND session_id = ?", (earning_id, session_id))
        row = cursor.fetchone()
        if not row:
            return None
        return EarningResponse(**dict(row))

def update_earning_entry(earning_id: int, data: EarningUpdate, session_id: str) -> Optional[EarningResponse]:
    existing = get_earning_by_id(earning_id, session_id)
    if not existing:
        return None
        
    new_date = data.date if data.date is not None else existing.date
    new_category = data.category if data.category is not None else existing.category
    new_platform = data.platform if data.platform is not None else existing.platform
    new_gross = data.gross_earnings if data.gross_earnings is not None else existing.gross_earnings
    new_tips = data.tips_incentives if data.tips_incentives is not None else existing.tips_incentives
    new_expenses = data.expenses if data.expenses is not None else existing.expenses
    new_notes = data.notes if data.notes is not None else existing.notes
    
    new_net = calculate_net_earnings(new_gross, new_tips, new_expenses)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE earnings 
            SET date = ?, category = ?, platform = ?, gross_earnings = ?, tips_incentives = ?, expenses = ?, net_earnings = ?, notes = ?
            WHERE id = ? AND session_id = ?
        """, (
            new_date, new_category, new_platform, 
            round(new_gross, 2), round(new_tips, 2), round(new_expenses, 2), 
            new_net, new_notes, earning_id, session_id
        ))
        conn.commit()
        return get_earning_by_id(earning_id, session_id)

def delete_earning_entry(earning_id: int, session_id: str) -> bool:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM earnings WHERE id = ? AND session_id = ?", (earning_id, session_id))
        conn.commit()
        return cursor.rowcount > 0

def get_earnings_summary(session_id: str) -> EarningsSummaryResponse:
    """Calculates summary aggregations scoped strictly to the current worker session."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    week_ago_str = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    month_start_str = datetime.now().strftime("%Y-%m-01")
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        def fetch_period(condition_extra: str, extra_params: list, name: str) -> PeriodSummary:
            sql = f"""
                SELECT 
                    COUNT(*) as count,
                    COALESCE(SUM(gross_earnings), 0.0) as total_gross,
                    COALESCE(SUM(tips_incentives), 0.0) as total_tips,
                    COALESCE(SUM(expenses), 0.0) as total_expenses,
                    COALESCE(SUM(net_earnings), 0.0) as total_net
                FROM earnings
                WHERE session_id = ? {condition_extra}
            """
            cursor.execute(sql, [session_id] + extra_params)
            r = cursor.fetchone()
            return PeriodSummary(
                period=name,
                total_gross=round(r["total_gross"], 2),
                total_tips=round(r["total_tips"], 2),
                total_expenses=round(r["total_expenses"], 2),
                total_net=round(r["total_net"], 2),
                entry_count=r["count"]
            )
            
        today_summary = fetch_period("AND date = ?", [today_str], "Today")
        week_summary = fetch_period("AND date >= ?", [week_ago_str], "Last 7 Days")
        month_summary = fetch_period("AND date >= ?", [month_start_str], "This Month")
        all_time_summary = fetch_period("", [], "All Time")
        
        # Category breakdown
        cursor.execute("""
            SELECT category, COALESCE(SUM(net_earnings), 0.0) as net
            FROM earnings
            WHERE session_id = ?
            GROUP BY category
        """, (session_id,))
        cat_rows = cursor.fetchall()
        category_breakdown = {r["category"]: round(r["net"], 2) for r in cat_rows}
        
        # Platform breakdown
        cursor.execute("""
            SELECT platform, COALESCE(SUM(net_earnings), 0.0) as net
            FROM earnings
            WHERE session_id = ?
            GROUP BY platform
        """, (session_id,))
        plat_rows = cursor.fetchall()
        platform_breakdown = {r["platform"]: round(r["net"], 2) for r in plat_rows}
        
        return EarningsSummaryResponse(
            today=today_summary,
            this_week=week_summary,
            this_month=month_summary,
            all_time=all_time_summary,
            category_breakdown=category_breakdown,
            platform_breakdown=platform_breakdown
        )
