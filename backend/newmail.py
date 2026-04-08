import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date
from pymongo import MongoClient
from dateutil.parser import parse
from celery import shared_task
from daily_utils import (
    ALLOWED_USERS, DISPLAY_USERS_ORDER, DISPLAY_NAME_MAP, CATEGORY_ORDER,
    to_float, format_indian_currency, get_fiscal_year_start, get_cumulative_start_date,
    get_cumulative_label, calculate_afx_earnings, get_stream_data, parse_date, get_raw_agg_vals,
    check_if_converted,AFX_COLLECTIONS 
)

REPORTED_IDS_FILE = os.path.join(os.path.dirname(__file__), ".reported_leads.json")

def load_reported_ids(key="default"):
    filename = f".reported_leads_{key}.json"
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {str(i): "2000-01-01" for i in data}
                return data
        except:
            return {}
    return {}

def save_reported_ids(ids_dict, key="default"):
    filename = f".reported_leads_{key}.json"
    try:
        with open(filename, "w") as f:
            json.dump(ids_dict, f)
    except:
        pass

# CC for Executive Reports
EXECUTIVE_CC = ["Srinivas.Mendu@agrifabrix.com", "associate@agrifabrix.com","Kumarvinod15452@gmail.com"]
SUPERADMIN_EMAILS = ["priya.kota@agrifabrix.com", "devendar.mallelli@agrifabrix.com","Srinivas.Mendu@agrifabrix.com"]
EXECUTIVE_EMAILS = {"Sruthi Devi": "sruthi.bandi@agrifabrix.com", "Losherwar Ramdas": "losherwar.ramdas@agrifabrix.com","Kalpana B": "kalpana.b@agrifabrix.com"}



# ---------------- EMAIL ---------------- #
def send_pipeline_email(to_email, html, cc_emails=None):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email

    if cc_emails:
        msg["Cc"] = ", ".join(cc_emails)

    today_label = datetime.now().strftime("%b %d, %Y %I:%M %p")
    msg["Subject"] = f"Sales Pipeline Report - {today_label}"
    msg.attach(MIMEText(html, "html"))

    recipients = [to_email] + (cc_emails if cc_emails else [])

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.sendmail(EMAIL, recipients, msg.as_string())
    server.quit()
    print(f"✅ Pipeline email sent to {to_email}")



# ---------------- CONFIG ---------------- #
EMAIL = "agrifabrix@gmail.com"
EMAIL_PASSWORD = "qlrp xwhd elde ufxs"
PORTAL_URL = "https://admin.agrifabrix.in/"
MONGO_URL = "mongodb://root:admin1234@127.0.0.1:27018/agrifabrix?authSource=admin"



# ⚡ ================= ADMIN FULL REPORT ================= #
 
def send_today_pipeline_report(to_email):
    client = MongoClient(MONGO_URL)
    db = client["agrifabrix"]
 
    def get_sorted_users(summary_dict):
        return sorted(summary_dict.keys(), key=lambda u: DISPLAY_USERS_ORDER.index(u) if u in DISPLAY_USERS_ORDER else 999)
 

     # ----------- CATEGORY DISPLAY ORDER ----------- #
 
    today = datetime.now().date()
    month_start = today.replace(day=1)
    fy_start = get_fiscal_year_start(today)
    cum_start = get_cumulative_start_date()
    cum_label = get_cumulative_label(today)

    fy_start_label = fy_start.strftime("%b %d, %Y")
    fy_end_label = f"Mar 31, {fy_start.year + 1}"
 
    all_raw_leads = list(db["InputFabriX_PL"].find())
    leads = all_raw_leads
    all_raw_trans = list(db["InputFabriX_YTD"].find({"is_pending": {"$ne": True}}))
    trans = all_raw_trans
   
    # --- FRANCHISE STORE DATA ---
    all_raw_fs_leads = list(db["Franchise_Stores_PL"].find())
    fs_leads = all_raw_fs_leads
    all_raw_fs_trans = list(db["Franchise_Stores_YTD"].find({"is_pending": {"$ne": True}}))
    fs_trans = all_raw_fs_trans
    
    # Merge YTD transactions for the unified Input Sales table
    merged_trans = trans + fs_trans
   
    # --- NEW FRANCHISE DATA ---
    all_raw_f_leads = list(db["Franchise_Leads"].find())
    f_leads = all_raw_f_leads
    all_raw_f_onboarded = list(db["Onboarded_Franchises"].find())
    f_onboarded = all_raw_f_onboarded
   
    # --- CREDIT PL DATA ---
    cred_leads = list(db["CreditFabriX_PL"].find())
   
    # --- FILTER DATA BY USER TYPES ---
    # 1. HARDCODED: Only these users for InputFabrix and CreditFabrix
    leads = [r for r in leads if r.get("userName") in ALLOWED_USERS]
    trans = [r for r in trans if r.get("userName") in ALLOWED_USERS]
    cred_leads = [r for r in cred_leads if r.get("userName") in ALLOWED_USERS]
 
    # 2. DYNAMIC: All users for Franchise (except pavani_jyothi)
    EXCLUDE_USERS = ["pavani_jyothi"]
    fs_leads = [r for r in fs_leads if r.get("userName") not in EXCLUDE_USERS]
    fs_trans = [r for r in fs_trans if r.get("userName") not in EXCLUDE_USERS]
    f_leads = [r for r in f_leads if r.get("userName") not in EXCLUDE_USERS]
    f_onboarded = [r for r in f_onboarded if r.get("userName") not in EXCLUDE_USERS]
    
    # Check for discrepancy
    raw_total_count = len(all_raw_trans) + len(all_raw_fs_trans)
    filtered_total_count = len(trans) + len(fs_trans)
    user_discrepancy = raw_total_count - filtered_total_count
   
    # ----------- BUYER DATA ----------- #
    db_dev = client["agrifabrixdev"]
    all_buyers = list(db_dev["buyers"].find({"isVerified": True, "isActive": True, "isDelete": False}))
   
    today_added_buyers = []
    before_today_buyers = []
    for b in all_buyers:
        ca = b.get("createdAt")
        if isinstance(ca, str):
            try: ca = parse(ca)
            except: continue
        if hasattr(ca, "date") and ca.date() == today:
            today_added_buyers.append(b)
        else:
            before_today_buyers.append(b)

    total_buyer_count_before_today = len(before_today_buyers)

    def get_buyer_html_pair(buyers_list):
        if not buyers_list: return "", ""
        from collections import Counter
        counts = Counter()
        for b in buyers_list:
            bt = str(b.get("selectBuyerType") or "Unknown").strip()
            counts[bt] += 1
        total = len(buyers_list)
        sorted_counts = counts.most_common()
        labels = [f"&nbsp;&nbsp;→ {bt}" for bt, _ in sorted_counts]
        vals = [f"{count} ({(count / total * 100):.1f}%)" for _, count in sorted_counts]
        l_str = "<br><span style='font-size:0.85em; font-weight:normal; color:#555;'>" + "<br>".join(labels) + "</span>"
        v_str = "<br><span style='font-size:0.85em; font-weight:normal; color:#555;'>" + "<br>".join(vals) + "</span>"
        return l_str, v_str

    before_today_lbl, before_today_val = get_buyer_html_pair(before_today_buyers)
    today_lbl, today_val = get_buyer_html_pair(today_added_buyers)
 
    # ----------- FINANCIAL YEAR TOTALS ----------- #
    # (Moved to daily_utils)
 
    streams = {
        "InputFabriX": "InputFabriX_YTD",
        "Consultancy Fee": "Consultancy_Services",
        "Marketing Fee": "Marketing",
        "CreditFabriX": "CreditFabriX_YTD",
        "Franchise Stores": "Franchise_Stores_YTD",
        "Onboarded Franchises": "Onboarded_Franchises"
    }
 
    stream_results = {}
    fy_sale_value = 0.0
    cumulative_sale_value = 0.0
 
    for name, coll_name in streams.items():
        fy_v, cum_v, fy_a, cum_a = get_stream_data(db, coll_name, fy_start, today, cum_start)
        stream_results[name] = {"fy": fy_v, "cum": cum_v, "fy_afx": fy_a, "cum_afx": cum_a}
        fy_sale_value += fy_v
        cumulative_sale_value += cum_v

    fy_afx_earnings = calculate_afx_earnings(
        db=db,
        collection_names=AFX_COLLECTIONS,
        start_date=fy_start,
        end_date=today
    )

    # ----------- CUMULATIVE TOTALS ----------- #
    cumulative_afx_earnings = calculate_afx_earnings(
        db=db,
        collection_names=AFX_COLLECTIONS,
        start_date=cum_start,
        end_date=today
    )
    print(cumulative_afx_earnings)
 
    # ----------- CONVERSION TIME CALCULATION ----------- #
    total_gap_days = 0
    valid_conversion_count = 0
    for r in trans:
        ld = r.get("Lead Date")
        td = r.get("Transaction Date")
       
        if isinstance(ld, str):
            try: ld = parse(ld)
            except: ld = None
        if isinstance(td, str):
            try: td = parse(td)
            except: td = None
           
        if ld and td and hasattr(ld, "date") and hasattr(td, "date"):
            gap = (td.date() - ld.date()).days
            if gap >= 0:
                total_gap_days += gap
                valid_conversion_count += 1
   
    avg_conversion_days = total_gap_days / valid_conversion_count if valid_conversion_count > 0 else 0
 
 
    # ----------- CATEGORY SUMMARY (FY + CUMULATIVE) ----------- #
    category_summary = {
        cat: {"fy": 0.0, "cum": 0.0, "count": 0, "fy_afx": 0.0, "cum_afx": 0.0}
        for cat in CATEGORY_ORDER
    }

    # Use UNFILTERED transactions for category summary to match portal counts
    for r in all_raw_trans + all_raw_fs_trans:
        cat = r.get("Category", "Unknown")
        if cat not in category_summary:
            category_summary[cat] = {"fy": 0.0, "cum": 0.0, "count": 0, "fy_afx": 0.0, "cum_afx": 0.0}

        category_summary[cat]["count"] += 1
        val = to_float(r.get("taxable_sale_value", 0))
        comm = to_float(r.get("agrifabrix_commission", 0))
        category_summary[cat]["cum"] += val
        category_summary[cat]["cum_afx"] += comm

        d = r.get("Transaction Date")
        if isinstance(d, str):
            try: d = parse(d).date()
            except: d = None
        elif isinstance(d, datetime):
            d = d.date()

        if d and isinstance(d, date) and fy_start <= d <= today:
            category_summary[cat]["fy"] += val
            category_summary[cat]["fy_afx"] += comm
 
    # ----------- LEAD SUMMARY ----------- #
    lead_summary = {
        u: {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "total": 0, "total_v": 0}
        for u in DISPLAY_USERS_ORDER
    }
 
    # -------- LEADS CREATED (INPUTFABRIX & FRANCHISE STORES) -------- #
    for rec in leads:
        user = rec.get("userName")
        if not user: continue
        if user not in lead_summary:
            lead_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "total": 0, "total_v": 0}
 
        conv_val = str(rec.get("is_it_converted") or "No").lower().strip()
        if conv_val in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue
 
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        if not hasattr(d, "date"): continue
 
        dt = d.date()
        val = to_float(rec.get("taxable_sale_value", 0))
        
        # TOTAL (CUMULATIVE)
        lead_summary[user]["total"] += 1
        lead_summary[user]["total_v"] += val
 
        if dt == today:
            lead_summary[user]["today"] += 1
            lead_summary[user]["today_v"] += val
 
        if month_start <= dt <= today:
            lead_summary[user]["month"] += 1
            lead_summary[user]["month_v"] += val

    for rec in fs_leads:
        user = rec.get("userName")
        if not user: continue
        if user not in lead_summary:
            lead_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "total": 0, "total_v": 0}
 
        conv_val = str(rec.get("is_it_converted") or "No").lower().strip()
        if conv_val in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue
 
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: d = None
        
        val = to_float(rec.get("taxable_sale_value", 0))
        
        # TOTAL (CUMULATIVE)
        lead_summary[user]["total"] += 1
        lead_summary[user]["total_v"] += val
 
        if not d or not hasattr(d, "date"): continue
        dt = d.date()
 
        if dt == today:
            lead_summary[user]["today"] += 1
            lead_summary[user]["today_v"] += val
 
        if month_start <= dt <= today:
            lead_summary[user]["month"] += 1
            lead_summary[user]["month_v"] += val
 
 
    # -------- INPUTFABRIX_YTD / FS_YTD (EXCLUDED FROM LEADS SUMMARY) -------- #
    # Converted records should not be counted as leads anymore
 
 
    # ----------- LEAD CONVERSION ANALYSIS ----------- #
    # User Request: Non-Converted Leads breakdown
    # Using raw unfiltered lists so it matches systemic totals (like 155)
    nc_ifx = sum(1 for r in all_raw_leads if not check_if_converted(r))
    nc_fsp = sum(1 for r in all_raw_fs_leads if not check_if_converted(r))
    nc_fl = sum(1 for r in all_raw_f_leads if not check_if_converted(r))
    non_converted_leads_count = nc_ifx + nc_fsp + nc_fl
    
    # User Request: Converted Leads breakdown (Sales metrics directly from YTD collections)
    c_ifx = len(all_raw_trans)
    c_fsp = len(all_raw_fs_trans)
    c_fob = len(all_raw_f_onboarded)
    converted_leads_count = c_ifx + c_fsp + c_fob

    total_leads_count = non_converted_leads_count + converted_leads_count
    
    conversion_ratio = (converted_leads_count / total_leads_count * 100) if total_leads_count > 0 else 0
    non_conversion_ratio = (non_converted_leads_count / total_leads_count * 100) if total_leads_count > 0 else 0

    p_c_ifx = f" ({c_ifx / total_leads_count * 100:.1f}%)" if total_leads_count > 0 else " (0.0%)"
    p_c_fsp = f" ({c_fsp / total_leads_count * 100:.1f}%)" if total_leads_count > 0 else " (0.0%)"
    p_c_fob = f" ({c_fob / total_leads_count * 100:.1f}%)" if total_leads_count > 0 else " (0.0%)"

    p_nc_ifx = f" ({nc_ifx / total_leads_count * 100:.1f}%)" if total_leads_count > 0 else " (0.0%)"
    p_nc_fsp = f" ({nc_fsp / total_leads_count * 100:.1f}%)" if total_leads_count > 0 else " (0.0%)"
    p_nc_fl = f" ({nc_fl / total_leads_count * 100:.1f}%)" if total_leads_count > 0 else " (0.0%)"

    # -------- CONSOLIDATED TODAY LEADS (DETAIL TABLE) -------- #
    today_combined_leads = []
    
    for rec in leads:
        conv_val = str(rec.get("is_it_converted") or "No").lower().strip()
        if conv_val in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        if d and hasattr(d, "date") and d.date() == today:
            today_combined_leads.append(rec)

    for rec in fs_leads:
        conv_val = str(rec.get("is_it_converted") or "No").lower().strip()
        if conv_val in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        if d and hasattr(d, "date") and d.date() == today:
            today_combined_leads.append(rec)
 
 
 
    # ----------- FRANCHISE STORE LEADS (DETAIL TABLE) ----------- #
    all_fs_leads = []
    for rec in fs_leads:
        # EXCLUDE CONVERTED
        conv_val = str(rec.get("is_it_converted") or "No").lower().strip()
        if conv_val in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue
        all_fs_leads.append(rec)
 
    # ----------- FRANCHISE TRANSACTION SUMMARY (BY USER) ----------- #
    fs_trans_summary = {}
 
    for rec in fs_trans:
        user = rec.get("userName")
        if not user: continue
        if user not in fs_trans_summary:
            fs_trans_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "fy": 0, "fy_v": 0, "total": 0, "total_v": 0}
 
        d = rec.get("Transaction Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        
        val = to_float(rec.get("taxable_sale_value", 0))
        
        # Cumulative
        fs_trans_summary[user]["total"] += 1
        fs_trans_summary[user]["total_v"] += val

        if d and hasattr(d, "date"):
            dt = d.date()
            if dt == today:
                fs_trans_summary[user]["today"] += 1
                fs_trans_summary[user]["today_v"] += val
            if month_start <= dt <= today:
                fs_trans_summary[user]["month"] += 1
                fs_trans_summary[user]["month_v"] += val
            if fy_start <= dt <= today:
                fs_trans_summary[user]["fy"] += 1
                fs_trans_summary[user]["fy_v"] += val
 
 
    # ----------- TODAY LEADS (DETAIL TABLE) ----------- #
    today_leads = []
 
    for rec in leads:
        # EXCLUDE CONVERTED
        conv_val = str(rec.get("is_it_converted") or "No").lower().strip()
        if conv_val in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue
 
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try:
                d = parse(d)
            except:
                continue
        if not hasattr(d, "date"):
            continue
 
        if d.date() == today:
            today_leads.append(rec)
 
    # ----------- FRANCHISE LEADS SUMMARY ----------- #
    f_lead_summary = {}
    all_f_leads = []
 
    for rec in f_leads:
        user = rec.get("userName")
        if not user: continue
        if user not in f_lead_summary:
            f_lead_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "total": 0, "total_v": 0}
           
        # INTEREST FILTER
        inst = str(rec.get("interested", rec.get("Interested", rec.get("Intrested", "")))).lower().strip()
        if inst == "no":
            continue
 
        # EXCLUDE CONVERTED
        if str(rec.get("is_it_converted") or "No").lower().strip() in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue

        all_f_leads.append(rec)
 
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: d = None
       
        # TOTAL (CUMULATIVE)
        f_lead_summary[user]["total"] += 1
        f_lead_summary[user]["total_v"] += to_float(rec.get("taxable_sale_value", 0))
 
        if not d or not hasattr(d, "date"): continue
        dt = d.date()
        val = to_float(rec.get("taxable_sale_value", 0))
 
        if dt == today:
            f_lead_summary[user]["today"] += 1
            f_lead_summary[user]["today_v"] += val
        if month_start <= dt <= today:
            f_lead_summary[user]["month"] += 1
            f_lead_summary[user]["month_v"] += val
 
    # ----------- ONBOARDED FRANCHISE SUMMARY ----------- #
    f_onboarded_summary = {}
    today_f_onboarded = []
 
    for rec in f_onboarded:
        user = rec.get("userName")
        if not user: continue
        if user not in f_onboarded_summary:
            f_onboarded_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "total": 0, "total_v": 0}
        d = rec.get("Transaction Date") or rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        if not hasattr(d, "date"): continue
        dt = d.date()
        val = to_float(rec.get("taxable_sale_value", 0))
 
        if dt == today:
            f_onboarded_summary[user]["today"] += 1
            f_onboarded_summary[user]["today_v"] += val
            today_f_onboarded.append(rec)
        if month_start <= dt <= today:
            f_onboarded_summary[user]["month"] += 1
            f_onboarded_summary[user]["month_v"] += val
        
        f_onboarded_summary[user]["total"] += 1
        f_onboarded_summary[user]["total_v"] += val
 
    # ----------- TRANSACTIONS SUMMARY ----------- #
    trans_summary = {}
 
    for rec in trans:
        user = rec.get("userName")
        if not user: continue
        if user not in trans_summary:
            trans_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "fy": 0, "fy_v": 0, "total": 0, "total_v": 0}
        
        d = rec.get("Transaction Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        
        val = to_float(rec.get("taxable_sale_value", 0))
        
        # Cumulative
        trans_summary[user]["total"] += 1
        trans_summary[user]["total_v"] += val

        if d and hasattr(d, "date"):
            dt = d.date()
            if dt == today:
                trans_summary[user]["today"] += 1
                trans_summary[user]["today_v"] += val
            if month_start <= dt <= today:
                trans_summary[user]["month"] += 1
                trans_summary[user]["month_v"] += val
            if fy_start <= dt <= today:
                trans_summary[user]["fy"] += 1
                trans_summary[user]["fy_v"] += val
    
    # Merge InputFabriX and Franchise Store transaction summaries
    for user, data in fs_trans_summary.items():
        if user not in trans_summary:
            trans_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0, "fy": 0, "fy_v": 0, "total": 0, "total_v": 0}
        for k in data: trans_summary[user][k] += data[k]

    # ----------- CREDIT FABRIX DATA ----------- #
    cred_summary = {u: {"today": 0, "today_v": 0, "month": 0, "month_v": 0} for u in DISPLAY_USERS_ORDER}
    cred_docs = list(db["CreditFabriX_YTD"].find({"is_pending": {"$ne": True}}))
   
    today_cred_transactions = []
    for rec in cred_docs:
        user = rec.get("userName")
        if user and user in ALLOWED_USERS:
            d = rec.get("Transaction Date")
            if isinstance(d, str):
                try: d = parse(d).date()
                except: d = None
            elif hasattr(d, "date"):
                d = d.date()
               
            if isinstance(d, date):
                val = to_float(rec.get("Loan Amount (INR Lakhs)", 0))
                if user not in cred_summary:
                    cred_summary[user] = {"today": 0, "today_v": 0, "month": 0, "month_v": 0}
                       
                if d == today:
                    cred_summary[user]["today"] += 1
                    cred_summary[user]["today_v"] += val
                if month_start <= d <= today:
                    cred_summary[user]["month"] += 1
                cred_summary[user]["month_v"] += val
           
            if d == today:
                today_cred_transactions.append(rec)
 
    # ----------- EXPECTED & OVERDUE (COMBINED) ----------- #
    # Combine all potential leads for follow-up tables
    combined_leads = leads + fs_leads + cred_leads
   
    expected_today, expected_overdue = [], []
 
    reported_data = load_reported_ids(to_email)
    today_str = today.strftime("%Y-%m-%d")
 
    for rec in combined_leads:
        # --- NEW FILTERS ---
        # Exclude if is_it_converted is anything other than 'No', empty, or None
        is_it_converted_val = str(rec.get("is_it_converted") or "No").lower().strip()
        is_converted = is_it_converted_val in ["yes", "true", "partially_yes"]
        val = to_float(rec.get("taxable_sale_value") or rec.get("actual_taxable_sale_value") or rec.get("Loan Amount (INR Lakhs)", 0))
       
        if is_converted or val <= 2000:
            continue
 
        d = rec.get("Expected Date of Conversion")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        if not hasattr(d, "date"): continue
 
        exp = d.date()
        rec["_exp"] = exp.strftime("%Y-%m-%d")
 
        # --- HIGHLIGHT LOGIC (MOVED UP FOR FILTERING) ---
        rem = str(rec.get("remarks", "")).lower().strip()
        inst = str(rec.get("interested", rec.get("Interested", rec.get("Intrested", "")))).lower().strip()
        is_no = rem == "no" or inst == "no"
        is_not_interested = "not interest" in rem or "not intrest" in rem or "not interest" in inst or "not intrest" in inst
        is_red = is_no or is_not_interested
 
        # --- ONLY ONCE FILTER ---
        rec_id = str(rec.get("_id"))
        last_reported = reported_data.get(rec_id)
       
        # USER REQUEST: If red (No/Not Interested), report ONLY ONCE EVER
        if is_red and last_reported:
            continue
           
        # For non-red leads, we report them every day they are expected/overdue.
        # We removed the 'if last_reported == today_str: continue' to allow multiple runs in a day during testing.
 
        if exp == today:
            expected_today.append(rec)
            reported_data[rec_id] = today_str
        else:
            diff = (today - exp).days
            if exp < today and diff <= 45:
                if is_no: continue # USER REQUEST: Exclude 'No' interest from overdue table
                rec["_days"] = diff
                expected_overdue.append(rec)
                reported_data[rec_id] = today_str
   
    save_reported_ids(reported_data, to_email)
 
 
    # (Moved to daily_utils)

    input_data = get_raw_agg_vals(db, ["InputFabriX_YTD", "Franchise_Stores_YTD", "Onboarded_Franchises", "Marketing", "Consultancy_Services"], fy_start, today, cum_start)
    credit_data = get_raw_agg_vals(db, ["CreditFabriX_YTD"], fy_start, today, cum_start)
    
    # Raw total for the bottom total line
    raw_total = {k: input_data[k] + credit_data[k] for k in input_data}

    # Percentages for InputFabriX (Financial Year)
    if_sv_p_fy = (input_data['fy'] / raw_total['fy'] * 100) if raw_total['fy'] > 0 else 0
    if_afx_p_fy = (input_data['fy_afx'] / raw_total['fy_afx'] * 100) if raw_total['fy_afx'] > 0 else 0
    
    # Percentages for CreditFabriX (Financial Year)
    cf_sv_p_fy = (credit_data['fy'] / raw_total['fy'] * 100) if raw_total['fy'] > 0 else 0
    cf_afx_p_fy = (credit_data['fy_afx'] / raw_total['fy_afx'] * 100) if raw_total['fy_afx'] > 0 else 0

    # Percentages for InputFabriX (Cumulative Year)
    if_sv_p_cum = (input_data['cum'] / raw_total['cum'] * 100) if raw_total['cum'] > 0 else 0
    if_afx_p_cum = (input_data['cum_afx'] / raw_total['cum_afx'] * 100) if raw_total['cum_afx'] > 0 else 0

    # Percentages for CreditFabriX (Cumulative Year)
    cf_sv_p_cum = (credit_data['cum'] / raw_total['cum'] * 100) if raw_total['cum'] > 0 else 0
    cf_afx_p_cum = (credit_data['cum_afx'] / raw_total['cum_afx'] * 100) if raw_total['cum_afx'] > 0 else 0

    sys_lead_pct = 100.0

    html = f"""<!DOCTYPE html><html><head><style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f7fa; }}
    .c {{ max-width: 95%; margin: 20px auto; background: white; padding: 20px; border-radius: 10px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
    th, td {{ padding: 8px; border: 1px solid #ccc; text-align: left; }}
    th {{ background-color: #f4f6f8; }}
    .gf {{ background-color: #f0f8ff; font-weight: bold; }}
    .gb {{ background-color: #e8f5e9; font-weight: bold; }}
    .gb .fy-bg, .gb .cy-bg {{ background-color: #e8f5e9; }}
    .gt {{ background-color: #f5f5f5; font-weight: bold; }}
    .fy-bg {{ background-color: #f0f7ff; }}
    .cy-bg {{ background-color: #fffaf0; }}
    .tc {{ text-align: center; }}
    .tr {{ text-align: right; }}
    .btn {{ display: inline-block; background: #1a73e8; color: white !important; padding: 12px 22px; text-decoration: none; border-radius: 6px; font-weight: bold; }}
    h2, h3 {{ color: #333; }}
    .ca {{ color: #004a99; }}
    .cl {{ color: #006400; }}
    .cb {{ color: #2e7d32; }}
    .ce {{ color: red; }}
    .co {{ color: #8b0000; }}
    .metric-val {{ font-size: 1.1em; font-weight: bold; color: #1a73e8; }}
    </style></head><body><div class="c">
    <h2>AFX Daily Performance Report – {today.strftime("%B %d %Y")}</h2>
    <h3 class="ca">Performance Summary ({fy_start_label} → {fy_end_label})</h3>
    <table>
        <tr class="gt">
            <th rowspan="2">Category</th>
            <th colspan="4" class="tc fy-bg">Financial Year-2025-2026</th>
            <th colspan="4" class="tc cy-bg">{cum_label}</th>
        </tr>
        <tr class="gt">
            <th class="fy-bg">Sale Value ₹</th><th class="fy-bg">SV %</th><th class="fy-bg">AFX Fee ₹</th><th class="fy-bg">AFX %</th>
            <th class="cy-bg">Sale Value ₹</th><th class="cy-bg">SV %</th><th class="cy-bg">AFX Fee ₹</th><th class="cy-bg">AFX %</th>
        </tr>
        <tr>
            <td>InputFabriX</td>
            <td class="fy-bg">₹ {format_indian_currency(input_data['fy'])}</td><td class="fy-bg">{if_sv_p_fy:.1f}%</td><td class="fy-bg">₹ {format_indian_currency(input_data['fy_afx'])}</td><td class="fy-bg">{if_afx_p_fy:.1f}%</td>
            <td class="cy-bg">₹ {format_indian_currency(input_data['cum'])}</td><td class="cy-bg">{if_sv_p_cum:.1f}%</td><td class="cy-bg">₹ {format_indian_currency(input_data['cum_afx'])}</td><td class="cy-bg">{if_afx_p_cum:.1f}%</td>
        </tr>
        <tr>
            <td>CreditFabriX</td>
            <td class="fy-bg">₹ {format_indian_currency(credit_data['fy'])}</td><td class="fy-bg">{cf_sv_p_fy:.1f}%</td><td class="fy-bg">₹ {format_indian_currency(credit_data['fy_afx'])}</td><td class="fy-bg">{cf_afx_p_fy:.1f}%</td>
            <td class="cy-bg">₹ {format_indian_currency(credit_data['cum'])}</td><td class="cy-bg">{cf_sv_p_cum:.1f}%</td><td class="cy-bg">₹ {format_indian_currency(credit_data['cum_afx'])}</td><td class="cy-bg">{cf_afx_p_cum:.1f}%</td>
        </tr>
        <tr class="gb">
            <td>Total</td>
            <td class="fy-bg">₹ {format_indian_currency(raw_total['fy'])}</td><td class="fy-bg">100.0%</td><td class="fy-bg">₹ {format_indian_currency(raw_total['fy_afx'])}</td><td class="fy-bg">100.0%</td>
            <td class="cy-bg">₹ {format_indian_currency(raw_total['cum'])}</td><td class="cy-bg">100.0%</td><td class="cy-bg">₹ {format_indian_currency(raw_total['cum_afx'])}</td><td class="cy-bg">100.0%</td>
        </tr>
    </table>
    
    <h3>Key Metrics</h3>
    <table>
        <tr>
            <th colspan="2" style="width: 50%;">System Health & Buyer Metrics</th>
            <th colspan="2" style="width: 50%;">Lead Conversion Analysis (All Time)</th>
        </tr>
        <tr>
            <td>Average Lead Conversion Time</td>
            <td class="tr metric-val">{avg_conversion_days:.1f} Days</td>
            <td class="gt">Total System Leads</td>
            <td class="tr metric-val gt" style="font-size:1.1em; color:#1a73e8;">{total_leads_count} ({sys_lead_pct:.1f}%)</td>
        </tr>
        <tr>
            <td>Total Buyers Onboarded (till date){before_today_lbl}</td>
            <td class="tr metric-val">{total_buyer_count_before_today} (100.0%){before_today_val}</td>
            <td style="color: #2e7d32; font-weight: bold;">Converted Leads (Sales)<br><span style="font-size:0.85em; font-weight:normal; color:#555;">&nbsp;&nbsp;→ InputFabriX_YTD<br>&nbsp;&nbsp;→ Franchise_Stores_YTD<br>&nbsp;&nbsp;→ Onboarded_Franchises</span></td>
            <td class="tr metric-val" style="color: #2e7d32; font-weight: bold;">{converted_leads_count} ({conversion_ratio:.1f}%)<br><span style="font-size:0.85em; font-weight:normal; color:#555;">{c_ifx}{p_c_ifx}<br>{c_fsp}{p_c_fsp}<br>{c_fob}{p_c_fob}</span></td>
        </tr>
        <tr>
            <td>Buyers Onboarded today{today_lbl}</td>
            <td class="tr metric-val">{len(today_added_buyers)}{f" (100.0%)" if len(today_added_buyers) > 0 else ""}{today_val}</td>
            <td style="color: #d32f2f; font-weight: bold;">Non-Converted Leads<br><span style="font-size:0.85em; font-weight:normal; color:#555;">&nbsp;&nbsp;→ InputFabriX_PL<br>&nbsp;&nbsp;→ Franchise_Stores_PL<br>&nbsp;&nbsp;→ Franchise_Leads</span></td>
            <td class="tr metric-val" style="color: #d32f2f; font-weight: bold;">{non_converted_leads_count} ({non_conversion_ratio:.1f}%)<br><span style="font-size:0.85em; font-weight:normal; color:#555;">{nc_ifx}{p_nc_ifx}<br>{nc_fsp}{p_nc_fsp}<br>{nc_fl}{p_nc_fl}</span></td>
        </tr>
    </table>"""
    # ----------- REVENUE STREAMS TABLES ----------- #
    # Table 1: InputFabriX Group
    input_group_keys = {
        "InputFabriX": "1.1 InputFabriX - Non Franchise Sales",
        "Franchise Stores": "1.2 InputFabriX - Franchise Sales",
        "Onboarded Franchises": "1.3 Franchise Registration Fee",
        "Consultancy Fee": "1.4 Consultancy Fee",
        "Marketing Fee": "1.5 Marketing Fee"
    }
    
    # Calculate group totals for percentages
    ig_fy_total = sum(stream_results[k]["fy"] for k in input_group_keys if k in stream_results)
    ig_cum_total = sum(stream_results[k]["cum"] for k in input_group_keys if k in stream_results)
    ig_fy_afx_total = sum(stream_results[k]["fy_afx"] for k in input_group_keys if k in stream_results)
    ig_cum_afx_total = sum(stream_results[k]["cum_afx"] for k in input_group_keys if k in stream_results)
    
    html += "<h3>1. InputFabriX Performance Breakdown</h3>"
    html += f"""<table>
        <tr class="gt">
            <th rowspan='2'>Revenue Stream</th>
            <th colspan='4' class='tc fy-bg'>Financial Year-2025-2026</th>
            <th colspan='4' class='tc cy-bg'>{cum_label}</th>
        </tr>
        <tr class="gt">
            <th class="fy-bg">Sale Value ₹</th><th class="fy-bg">SV %</th><th class="fy-bg">AFX Fee ₹</th><th class="fy-bg">AFX %</th>
            <th class="cy-bg">Sale Value ₹</th><th class="cy-bg">SV %</th><th class="cy-bg">AFX Fee ₹</th><th class="cy-bg">AFX %</th>
        </tr>"""
    
    for k, label in input_group_keys.items():
        if k not in stream_results: continue
        vals = stream_results[k]
        fy_p = (vals["fy"] / ig_fy_total * 100) if ig_fy_total > 0 else 0
        cum_p = (vals["cum"] / ig_cum_total * 100) if ig_cum_total > 0 else 0
        fy_afx_p = (vals["fy_afx"] / ig_fy_afx_total * 100) if ig_fy_afx_total > 0 else 0
        cum_afx_p = (vals["cum_afx"] / ig_cum_afx_total * 100) if ig_cum_afx_total > 0 else 0
        html += f"""<tr>
            <td>{label}</td>
            <td class="fy-bg">₹ {format_indian_currency(vals['fy'])}</td><td class="fy-bg">{fy_p:.1f}%</td><td class="fy-bg">₹ {format_indian_currency(vals['fy_afx'])}</td><td class="fy-bg">{fy_afx_p:.1f}%</td>
            <td class="cy-bg">₹ {format_indian_currency(vals['cum'])}</td><td class="cy-bg">{cum_p:.1f}%</td><td class="cy-bg">₹ {format_indian_currency(vals['cum_afx'])}</td><td class="cy-bg">{cum_afx_p:.1f}%</td>
        </tr>"""
    
    # Total Row for InputFabriX Breakdown
    html += f"""<tr class="gb">
        <td>Total</td>
        <td class="fy-bg">₹ {format_indian_currency(ig_fy_total)}</td><td class="fy-bg">100.0%</td><td class="fy-bg">₹ {format_indian_currency(ig_fy_afx_total)}</td><td class="fy-bg">100.0%</td>
        <td class="cy-bg">₹ {format_indian_currency(ig_cum_total)}</td><td class="cy-bg">100.0%</td><td class="cy-bg">₹ {format_indian_currency(ig_cum_afx_total)}</td><td class="cy-bg">100.0%</td>
    </tr>"""
    html += "</table>"

    # Table 2: CreditFabriX Group
    html += "<h3>2. CreditFabriX Performance Breakdown</h3>"
    html += f"""<table>
        <tr class="gt">
            <th rowspan='2'>Revenue Stream</th>
            <th colspan='4' class='tc fy-bg'>Financial Year-2025-2026</th>
            <th colspan='4' class='tc cy-bg'>{cum_label}</th>
        </tr>
        <tr class="gt">
            <th class="fy-bg">Sale Value ₹</th><th class="fy-bg">SV %</th><th class="fy-bg">AFX Fee ₹</th><th class="fy-bg">AFX %</th>
            <th class="cy-bg">Sale Value ₹</th><th class="cy-bg">SV %</th><th class="cy-bg">AFX Fee ₹</th><th class="cy-bg">AFX %</th>
        </tr>"""
    
    if "CreditFabriX" in stream_results:
        vals = stream_results["CreditFabriX"]
        html += f"""<tr>
            <td>2.1 CreditFabriX</td>
            <td class="fy-bg">₹ {format_indian_currency(vals['fy'])}</td><td class="fy-bg">100.0%</td><td class="fy-bg">₹ {format_indian_currency(vals['fy_afx'])}</td><td class="fy-bg">100.0%</td>
            <td class="cy-bg">₹ {format_indian_currency(vals['cum'])}</td><td class="cy-bg">100.0%</td><td class="cy-bg">₹ {format_indian_currency(vals['cum_afx'])}</td><td class="cy-bg">100.0%</td>
        </tr>"""
        
        # Total Row for CreditFabriX Breakdown (even if it's identical to the row above)
        html += f"""<tr class="gb">
            <td>Total</td>
            <td class="fy-bg">₹ {format_indian_currency(vals['fy'])}</td><td class="fy-bg">100.0%</td><td class="fy-bg">₹ {format_indian_currency(vals['fy_afx'])}</td><td class="fy-bg">100.0%</td>
            <td class="cy-bg">₹ {format_indian_currency(vals['cum'])}</td><td class="cy-bg">100.0%</td><td class="cy-bg">₹ {format_indian_currency(vals['cum_afx'])}</td><td class="cy-bg">100.0%</td>
        </tr>"""
    html += "</table>"
    html += f"""<h3>Category Summary</h3>
    <table>
        <tr class="gt">
            <th rowspan="2">Category</th>
            <th rowspan="2">Count</th>
            <th colspan="4" class="tc fy-bg">Financial Year-2025-2026</th>
            <th colspan="4" class="tc cy-bg">{cum_label}</th>
        </tr>
        <tr class="gt">
            <th class="fy-bg">Value ₹</th>
            <th class="fy-bg">SV %</th>
            <th class="fy-bg">AFX Fee ₹</th>
            <th class="fy-bg">AFX %</th>
            <th class="cy-bg">Value ₹</th>
            <th class="cy-bg">SV %</th>
            <th class="cy-bg">AFX Fee ₹</th>
            <th class="cy-bg">AFX %</th>
        </tr>
    """
 
    total_cat_count = sum(vals["count"] for vals in category_summary.values())
    total_cat_fy = sum(vals["fy"] for vals in category_summary.values())
    total_cat_cum = sum(vals["cum"] for vals in category_summary.values())
    total_cat_fy_afx = sum(vals["fy_afx"] for vals in category_summary.values())
    total_cat_cum_afx = sum(vals["cum_afx"] for vals in category_summary.values())

    # Helper to generate a table row
    def add_cat_row(cat, vals):
        nonlocal html
        fy_p = (vals["fy"] / total_cat_fy * 100) if total_cat_fy > 0 else 0
        cum_p = (vals["cum"] / total_cat_cum * 100) if total_cat_cum > 0 else 0
        fy_afx_p = (vals["fy_afx"] / total_cat_fy_afx * 100) if total_cat_fy_afx > 0 else 0
        cum_afx_p = (vals["cum_afx"] / total_cat_cum_afx * 100) if total_cat_cum_afx > 0 else 0
        
        html += f"""<tr>
            <td>{cat}</td>
            <td>{vals['count']}</td>
            <td class="fy-bg">₹ {format_indian_currency(vals['fy'])}</td>
            <td class="fy-bg">{fy_p:.1f}%</td>
            <td class="fy-bg">₹ {format_indian_currency(vals['fy_afx'])}</td>
            <td class="fy-bg">{fy_afx_p:.1f}%</td>
            <td class="cy-bg">₹ {format_indian_currency(vals['cum'])}</td>
            <td class="cy-bg">{cum_p:.1f}%</td>
            <td class="cy-bg">₹ {format_indian_currency(vals['cum_afx'])}</td>
            <td class="cy-bg">{cum_afx_p:.1f}%</td>
        </tr>"""

    # 1. Show all specified categories in order
    for cat in CATEGORY_ORDER:
        vals = category_summary.get(cat, {"fy": 0.0, "cum": 0.0, "count": 0, "fy_afx": 0.0, "cum_afx": 0.0})
        add_cat_row(cat, vals)
            
    # 2. Show 'Others' for remaining categories
    others_vals = {"fy": 0.0, "cum": 0.0, "count": 0, "fy_afx": 0.0, "cum_afx": 0.0}
    found_others = False
    for cat, vals in category_summary.items():
        if cat not in CATEGORY_ORDER and vals["count"] > 0:
            found_others = True
            for k in others_vals: others_vals[k] += vals[k]
            
    if found_others:
        add_cat_row("Others", others_vals)
 
    html += f"""<tr class='gb'>
        <td>TOTAL</td>
        <td>{total_cat_count}</td>
        <td class="fy-bg">₹ {format_indian_currency(total_cat_fy)}</td>
        <td class="fy-bg">100%</td>
        <td class="fy-bg">₹ {format_indian_currency(total_cat_fy_afx)}</td>
        <td class="fy-bg">100%</td>
        <td class="cy-bg">₹ {format_indian_currency(total_cat_cum)}</td>
        <td class="cy-bg">100%</td>
        <td class="cy-bg">₹ {format_indian_currency(total_cat_cum_afx)}</td>
        <td class="cy-bg">100%</td>
    </tr></table>"""
 
    # ---------------- INPUT SALES TRANSACTIONS SUMMARY ---------------- #
    html += """<h3>Input Sales Transactions Summary</h3><table><tr><th>Team Member</th><th>Today Sales</th><th>Value ₹</th><th>Month Sales</th><th>Value ₹</th></tr>"""
    
    s1 = s2 = s3 = s4 = 0
    for u in get_sorted_users(trans_summary):
        d = trans_summary[u]
        s1 += d["today"]; s2 += d["today_v"]; s3 += d["month"]; s4 += d["month_v"]
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(u, u)}</td><td>{d['today']}</td><td>₹ {format_indian_currency(d['today_v'])}</td><td>{d['month']}</td><td>₹ {format_indian_currency(d['month_v'])}</td></tr>"
 
    html += f"<tr class='gt'><td>TOTAL</td><td>{s1}</td><td>₹ {format_indian_currency(s2)}</td><td>{s3}</td><td>₹ {format_indian_currency(s4)}</td></tr></table>"
 
    # ---------------- TODAY INPUT SALES TRANSACTIONS (DETAIL) ---------------- #
    today_trans_detail = []
    for rec in merged_trans:
        d = rec.get("Transaction Date")
        if isinstance(d, str):
            try: d = parse(d).date()
            except: d = None
        elif hasattr(d, "date"):
            d = d.date()
        if d == today:
            today_trans_detail.append(rec)

    html += """<h3 class='cl'>Today Input Sales Transaction Summary</h3><table><tr><th>Team Member</th><th>Client</th><th>Phone</th><th>Type</th><th>District</th><th>Location</th><th>Product</th><th>Value</th></tr>"""
   
    today_trans_value = 0
    for r in today_trans_detail:
        val = to_float(r.get("taxable_sale_value", 0))
        today_trans_value += val
        client_name = r.get('Client Name') or r.get('franchise_name') or 'N/A'
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(r.get('userName'), r.get('userName'))}</td><td>{client_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type')}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>{r.get('Product Name')}</td><td>₹ {format_indian_currency(val)}</td></tr>"
 
    html += f"<tr class='gt'><td colspan='7'>TOTAL</td><td>₹ {format_indian_currency(today_trans_value)}</td></tr></table>"
   
    # ---------------- INPUT LEADS SUMMARY ---------------- #
    html += """<h3>Input Leads Summary</h3><table><tr><th>Team Member</th><th>Today Leads</th><th>Today Value ₹</th><th>Month Leads</th><th>Month Value ₹</th><th>Total Leads</th><th>Total Value ₹</th></tr>"""
  
    ls1 = ls2 = ls3 = ls4 = ls5 = ls6 = 0
    for u in get_sorted_users(lead_summary):
        d = lead_summary[u]
        ls1 += d["today"]; ls2 += d["today_v"]; ls3 += d["month"]; ls4 += d["month_v"]; ls5 += d["total"]; ls6 += d["total_v"]
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(u, u)}</td><td>{d['today']}</td><td>₹ {format_indian_currency(d['today_v'])}</td><td>{d['month']}</td><td>₹ {format_indian_currency(d['month_v'])}</td><td>{d['total']}</td><td>₹ {format_indian_currency(d['total_v'])}</td></tr>"
 
    html += f"<tr class='gt'><td>TOTAL</td><td>{ls1}</td><td>₹ {format_indian_currency(ls2)}</td><td>{ls3}</td><td>₹ {format_indian_currency(ls4)}</td><td>{ls5}</td><td>₹ {format_indian_currency(ls6)}</td></tr></table>"
 
    # ---------------- TODAY INPUT LEADS (DETAIL) ---------------- #
    html += """<h3 class='cl'>Today Input Leads</h3><table><tr><th>Team Member</th><th>Client</th><th>Phone</th><th>Type</th><th>District</th><th>Location</th><th>Product</th><th>Value</th></tr>"""
    
    today_leads_value = 0
    for r in today_combined_leads:
        val = to_float(r.get("taxable_sale_value", 0))
        today_leads_value += val
        client_name = r.get('Client Name') or r.get('franchise_name') or 'N/A'
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(r.get('userName'), r.get('userName'))}</td><td>{client_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type')}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>{r.get('Product Name')}</td><td>₹ {format_indian_currency(val)}</td></tr>"

    html += f"<tr class='gt'><td colspan='7'>TOTAL</td><td>₹ {format_indian_currency(today_leads_value)}</td></tr></table>"

    # ---------------- ONBOARDED FRANCHISE SUMMARY ---------------- #
    html += """<h3>Onboarded Franchise Summary</h3><table><tr><th>Team Member</th><th>Today Count</th><th>Value ₹</th><th>Month Count</th><th>Value ₹</th><th>Total Count</th><th>Total Value ₹</th></tr>"""
    ob1 = ob2 = ob3 = ob4 = ob5 = ob6 = 0
    for u in get_sorted_users(f_onboarded_summary):
        d = f_onboarded_summary[u]
        ob1 += d["today"]; ob2 += d["today_v"]; ob3 += d["month"]; ob4 += d["month_v"]; ob5 += d["total"]; ob6 += d["total_v"]
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(u, u)}</td><td>{d['today']}</td><td>₹ {format_indian_currency(d['today_v'])}</td><td>{d['month']}</td><td>₹ {format_indian_currency(d['month_v'])}</td><td>{d['total']}</td><td>₹ {format_indian_currency(d['total_v'])}</td></tr>"
    html += f"<tr class='gt'><td>TOTAL</td><td>{ob1}</td><td>₹ {format_indian_currency(ob2)}</td><td>{ob3}</td><td>₹ {format_indian_currency(ob4)}</td><td>{ob5}</td><td>₹ {format_indian_currency(ob6)}</td></tr></table>"

    # ---------------- TODAY ONBOARDED FRANCHISES (DETAIL) ---------------- #
    html += """<h3 class='cl'>Today Onboarded Franchises</h3><table><tr><th>Team Member</th><th>Franchise Name</th><th>Phone</th><th>Type</th><th>State</th><th>District</th><th>Location</th><th>Value</th></tr>"""
    today_ob_value = 0
    for r in today_f_onboarded:
        val = to_float(r.get("taxable_sale_value", 0))
        today_ob_value += val
        franchise_name = r.get('franchise_name') or 'N/A'
        state = r.get('State') or r.get('state') or 'N/A'
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(r.get('userName'), r.get('userName'))}</td><td>{franchise_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type')}</td><td>{state}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>₹ {format_indian_currency(val)}</td></tr>"
    html += f"<tr class='gt'><td colspan='7'>TOTAL</td><td>₹ {format_indian_currency(today_ob_value)}</td></tr></table>"

    # ---------------- FRANCHISE LEADS SUMMARY ---------------- #
    html += """<h3>Franchise Leads Summary</h3><table><tr><th>Team Member</th><th>Today Leads</th><th>Value ₹</th><th>Month Leads</th><th>Value ₹</th><th>Total Leads</th><th>Total Value ₹</th></tr>"""
    fl1 = fl2 = fl3 = fl4 = fl5 = fl6 = 0
    for u in get_sorted_users(f_lead_summary):
        d = f_lead_summary[u]
        fl1 += d["today"]; fl2 += d["today_v"]; fl3 += d["month"]; fl4 += d["month_v"]; fl5 += d["total"]; fl6 += d["total_v"]
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(u, u)}</td><td>{d['today']}</td><td>₹ {format_indian_currency(d['today_v'])}</td><td>{d['month']}</td><td>₹ {format_indian_currency(d['month_v'])}</td><td>{d['total']}</td><td>₹ {format_indian_currency(d['total_v'])}</td></tr>"
    html += f"<tr class='gt'><td>TOTAL</td><td>{fl1}</td><td>₹ {format_indian_currency(fl2)}</td><td>{fl3}</td><td>₹ {format_indian_currency(fl4)}</td><td>{fl5}</td><td>₹ {format_indian_currency(fl6)}</td></tr></table>"

    # ---------------- FRANCHISE LEADS (DETAIL) ---------------- #
    html += """<h3 class='cl'>Franchise Leads</h3><table><tr><th>S.No.</th><th>Team Member</th><th>Franchise Name</th><th>Phone</th><th>Type</th><th>State</th><th>District</th><th>Location</th><th>Value</th></tr>"""
    today_fl_value = 0
    for idx, r in enumerate(all_f_leads, 1):
        val = to_float(r.get("taxable_sale_value", 0))
        today_fl_value += val
        franchise_name = r.get('franchise_name') or 'N/A'
        state = r.get('State') or r.get('state') or 'N/A'
        html += f"<tr><td>{idx}</td><td>{DISPLAY_NAME_MAP.get(r.get('userName'), r.get('userName'))}</td><td>{franchise_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type')}</td><td>{state}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>₹ {format_indian_currency(val)}</td></tr>"
    html += f"<tr class='gt'><td colspan='8'>TOTAL</td><td>₹ {format_indian_currency(today_fl_value)}</td></tr></table>"

    # ---------------- TODAY ADDED BUYERS ---------------- #
    html += """<h3 class='cb'>Today Added Buyers</h3><table><tr><th>S.No.</th><th>Buyer Name</th><th>Phone</th><th>Buyer Type</th><th>Pincode</th><th>District</th><th>Location</th></tr>"""
    if not today_added_buyers:
        html += "<tr><td colspan='7' class='tc'>No buyers added today</td></tr>"
    else:
        for idx, b in enumerate(today_added_buyers, 1):
            pincode = b.get('pincode') or b.get('pinCode') or 'N/A'
            html += f"<tr><td>{idx}</td><td>{b.get('buyerName', 'N/A')}</td><td>{b.get('phone', 'N/A')}</td><td>{b.get('selectBuyerType', 'N/A')}</td><td>{pincode}</td><td>{b.get('district', 'N/A')}</td><td>{b.get('cityName', 'N/A')}</td></tr>"
    html += "</table>"

    # ---------------- CREDIT FABRIX TRANSACTION SUMMARY ---------------- #
    html += """<h3>CreditFabriX Transaction Summary</h3><table><tr><th>Team Member</th><th>Today Count</th><th>Today Value ₹</th><th>Month Count</th><th>Month Value ₹</th></tr>"""
    c1 = c2 = c3 = c4 = 0
    for u in get_sorted_users(cred_summary):
        d = cred_summary[u]
        c1 += d["today"]; c2 += d["today_v"]; c3 += d["month"]; c4 += d["month_v"]
        html += f"<tr><td>{DISPLAY_NAME_MAP.get(u, u)}</td><td>{d['today']}</td><td>₹ {format_indian_currency(d['today_v'])}</td><td>{d['month']}</td><td>₹ {format_indian_currency(d['month_v'])}</td></tr>"
    html += f"<tr class='gt'><td>TOTAL</td><td>{c1}</td><td>₹ {format_indian_currency(c2)}</td><td>{c3}</td><td>₹ {format_indian_currency(c4)}</td></tr></table>"

    # ---------------- TODAY'S CREDIT FABRIX TRANSACTIONS ---------------- #
    html += """<h3>Today's CreditFabriX Transactions</h3><table><tr><th>Team Member</th><th>FPO Name</th><th>Loan Amount (INR)</th><th>Legal Status</th><th>District</th><th>Location</th></tr>"""
    if not today_cred_transactions:
        html += "<tr><td colspan='6' class='tc'>No updates today</td></tr>"
    else:
        tot_loan = 0
        for rec in today_cred_transactions:
            val = to_float(rec.get("Loan Amount (INR Lakhs)", 0))
            tot_loan += val
            html += f"<tr><td>{DISPLAY_NAME_MAP.get(rec.get('userName'), rec.get('userName'))}</td><td>{rec.get('FPO Name')}</td><td>₹ {format_indian_currency(val)}</td><td>{rec.get('Legal Status')}</td><td>{rec.get('District')}</td><td>{rec.get('Location')}</td></tr>"
        html += f"<tr class='gt'><td colspan='2'>TOTAL</td><td>₹ {format_indian_currency(tot_loan)}</td><td colspan='3'></td></tr>"
    html += "</table>"

    # ---------------- EXPECTED TODAY ---------------- #
    html += """<h3 class='ce'>Expected Today</h3><table><tr><th>S.No.</th><th>Team Member</th><th>Client</th><th>Phone</th><th>Type</th><th>District</th><th>Location</th><th>Exp Date</th><th>Product</th><th>Value</th></tr>"""
    
    total_expected_value = 0
    for idx, r in enumerate(expected_today, 1):
        val = to_float(r.get("taxable_sale_value"))
        total_expected_value += val
        rem = str(r.get("remarks", "")).lower().strip()
        inst = str(r.get("interested", r.get("Interested", r.get("Intrested", "")))).lower().strip()
        row_style = ""
        if rem == "no" or inst == "no" or "not interest" in rem or "not intrest" in rem or "not interest" in inst or "not intrest" in inst:
            row_style = ' style="background-color: #ffebee; color: red;"'
        client_name = r.get('Client Name') or r.get('customer_name') or r.get('franchise_name') or r.get('FPO Name') or 'N/A'
        html += f"<tr{row_style}><td>{idx}</td><td>{DISPLAY_NAME_MAP.get(r.get('userName'), r.get('userName'))}</td><td>{client_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type') or r.get('Business_Type')}</td><td>{r.get('District') or 'N/A'}</td><td>{r.get('Location') or 'N/A'}</td><td>{r.get('_exp')}</td><td>{r.get('Product Name') or 'Credit/Consultancy'}</td><td>₹ {format_indian_currency(val)}</td></tr>"
    html += f"<tr class='gt'><td colspan='9'>TOTAL</td><td>₹ {format_indian_currency(total_expected_value)}</td></tr></table>"

    # ---------------- OVERDUE (LAST 45 DAYS) ---------------- #
    html += """<h3 class='co'>Overdue (Last 45 Days)</h3><table><tr><th>S.No.</th><th>Team Member</th><th>Client</th><th>Phone</th><th>Type</th><th>District</th><th>Location</th><th>Exp Date</th><th>Product</th><th>Value</th><th>Days</th></tr>"""
    
    total_overdue_value = 0
    for idx, r in enumerate(expected_overdue, 1):
        val = to_float(r.get("taxable_sale_value"))
        total_overdue_value += val
        rem = str(r.get("remarks", "")).lower().strip()
        inst = str(r.get("interested", r.get("Interested", r.get("Intrested", "")))).lower().strip()
        row_style = ""
        if rem == "no" or inst == "no" or "not interest" in rem or "not intrest" in rem or "not interest" in inst or "not intrest" in inst:
            row_style = ' style="background-color: #ffebee; color: red;"'
        client_name = r.get('Client Name') or r.get('customer_name') or r.get('franchise_name') or r.get('FPO Name') or 'N/A'
        html += f"<tr{row_style}><td>{idx}</td><td>{DISPLAY_NAME_MAP.get(r.get('userName'), r.get('userName'))}</td><td>{client_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type') or r.get('Business_Type')}</td><td>{r.get('District') or 'N/A'}</td><td>{r.get('Location') or 'N/A'}</td><td>{r.get('_exp')}</td><td>{r.get('Product Name') or 'Credit/Consultancy'}</td><td>₹ {format_indian_currency(val)}</td><td>{r.get('_days')}</td></tr>"
    html += f"<tr class='gt'><td colspan='9'>TOTAL</td><td>₹ {format_indian_currency(total_overdue_value)}</td><td></td></tr></table>"
 
    # ---------------- FOOTER ---------------- #
    html += f"""<div style="text-align:center;margin-top:30px;"><a href="{PORTAL_URL}" class="btn">Open AFX Portal</a></div></div></body></html>"""
    send_pipeline_email(to_email, html)
 
 
 


# ⚡ ================= EXECUTIVE REPORT ================= #
def send_executive_pipeline_report(user, to_email, cc_list):
    client = MongoClient(MONGO_URL)
    db = client["agrifabrix"]
    display_user = DISPLAY_NAME_MAP.get(user, user)
 
    today = datetime.now().date()
    month_start = today.replace(day=1)
    fy_start = get_fiscal_year_start(today)
    cum_start = get_cumulative_start_date()

    # Fetch only this executive's data
    leads = list(db["InputFabriX_PL"].find({"userName": user}))
    trans = list(db["InputFabriX_YTD"].find({"userName": user, "is_pending": {"$ne": True}}))
 
    # --- FRANCHISE STORE DATA (EXECUTIVE) ---
    fs_leads = list(db["Franchise_Stores_PL"].find({"userName": user}))
    fs_trans = list(db["Franchise_Stores_YTD"].find({"userName": user, "is_pending": {"$ne": True}}))
   
    # --- NEW FRANCHISE DATA (EXECUTIVE) ---
    f_leads = list(db["Franchise_Leads"].find({"userName": user}))
    f_onboarded = list(db["Onboarded_Franchises"].find({"userName": user}))
 
    # ----------- BUYER DATA ----------- #
    db_dev = client["agrifabrixdev"]
    all_buyers = list(db_dev["buyers"].find({"isVerified": True, "isActive": True, "isDelete": False}))
   
    today_added_buyers = []
    for b in all_buyers:
        ca = b.get("createdAt")
        if isinstance(ca, str):
            try: ca = parse(ca)
            except: continue
        if hasattr(ca, "date") and ca.date() == today:
            today_added_buyers.append(b)
 
    total_buyer_count_before_today = len(all_buyers) - len(today_added_buyers)
 
    # ========================= LEADS SUMMARY =========================
    lead_today = lead_today_v = lead_month = lead_month_v = 0
 
    # -------- INPUTFABRIX_PL (LEADS CREATED) -------- #
    for rec in leads:
        # USER REQUEST: If converted, don't show in leads summary
        if str(rec.get("is_it_converted") or "No").lower().strip() in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue
 
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try:
                d = parse(d)
            except:
                continue
 
        if not hasattr(d, "date"):
            continue
 
        dt = d.date()
        val = to_float(rec.get("taxable_sale_value", 0))
 
        # TODAY → PL ONLY
        if dt == today:
            lead_today += 1
            lead_today_v += val
 
        # MONTH → PL CONTRIBUTION
        if month_start <= dt <= today:
            lead_month += 1
            lead_month_v += val
 
    # -------- INPUTFABRIX_YTD (CONVERTED LEADS) -------- #
    for rec in trans:
        d = rec.get("Transaction Date")
        if isinstance(d, str):
            try:
                d = parse(d)
            except:
                continue
 
        if not hasattr(d, "date"):
            continue
 
        dt = d.date()
        val = to_float(rec.get("taxable_sale_value", 0))
 
        # MONTH → YTD CONTRIBUTION
        if month_start <= dt <= today:
            lead_month += 1
            lead_month_v += val
 
    # ----------- CONVERSION TIME CALCULATION ----------- #
    total_gap_days = 0
    valid_conversion_count = 0
    for r in trans:
        ld = r.get("Lead Date")
        td = r.get("Transaction Date")
       
        if isinstance(ld, str):
            try: ld = parse(ld)
            except: ld = None
        if isinstance(td, str):
            try: td = parse(td)
            except: td = None
           
        if ld and td and hasattr(ld, "date") and hasattr(td, "date"):
            gap = (td.date() - ld.date()).days
            if gap >= 0:
                total_gap_days += gap
                valid_conversion_count += 1
   
    avg_conversion_days = total_gap_days / valid_conversion_count if valid_conversion_count > 0 else 0
 
    # ========================= TRANSACTION SUMMARY =========================
    trans_today = trans_today_v = trans_month = trans_month_v = 0
    today_trans_exec = []
 
    for rec in trans:
        d = rec.get("Transaction Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
 
        if not hasattr(d, "date"):
            continue
 
        dt = d.date()
        val = to_float(rec.get("taxable_sale_value", 0))
 
        if dt == today:
            trans_today += 1
            trans_today_v += val
            today_trans_exec.append(rec)
 
        if month_start <= dt <= today:
            trans_month += 1
            trans_month_v += val
 
    fs_trans_today = fs_trans_today_v = fs_trans_month = fs_trans_month_v = 0
    today_fs_trans_exec = []
    
    for rec in fs_trans:
        d = rec.get("Transaction Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        if not hasattr(d, "date"): continue
        dt = d.date()
        val = to_float(rec.get("taxable_sale_value", 0))
 
        if dt == today:
            fs_trans_today += 1
            fs_trans_today_v += val
            today_fs_trans_exec.append(rec)
        if month_start <= dt <= today:
            fs_trans_month += 1
            fs_trans_month_v += val
 
    # --- FS TRANSACTIONS FY/CUM ---
    fs_trans_fy = fs_trans_cum = 0
    for rec in fs_trans:
        val = to_float(rec.get("taxable_sale_value", 0))
        d = parse_date(rec.get("Transaction Date"))
        
        if d:
            if fy_start <= d <= today:
                fs_trans_fy += val
            if cum_start <= d <= today:
                fs_trans_cum += val
 
    # ========================= NEW FRANCHISE SUMMARY (EXECUTIVE) =========================
    f_lead_today = f_lead_today_v = f_lead_month = f_lead_month_v = f_lead_total = f_lead_total_v = 0
    f_onboarded_today = f_onboarded_today_v = f_onboarded_month = f_onboarded_month_v = f_onboarded_fy = f_onboarded_cum = 0
    all_f_leads_exec = []
    all_f_onboarded_exec = []
    
    # --- FRANCHISE LEADS (EXECUTIVE) ---
    for rec in f_leads:
        # INTEREST FILTER
        inst = str(rec.get("interested", rec.get("Interested", rec.get("Intrested", "")))).lower().strip()
        if inst == "no":
            continue

        # EXCLUDE CONVERTED
        if str(rec.get("is_it_converted") or "No").lower().strip() in ["yes", "true", "partially_yes"] or rec.get("is_it_converted") is True:
            continue

        all_f_leads_exec.append(rec)
        val = to_float(rec.get("taxable_sale_value", 0))
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d).date()
            except: d = None
        elif hasattr(d, "date"):
            d = d.date()

        f_lead_total += 1
        f_lead_total_v += val
        if d == today:
            f_lead_today += 1
            f_lead_today_v += val
        if d and month_start <= d <= today:
            f_lead_month += 1
            f_lead_month_v += val

    # --- ONBOARDED FRANCHISE (EXECUTIVE) ---
    for rec in f_onboarded:
        all_f_onboarded_exec.append(rec)
        val = to_float(rec.get("taxable_sale_value", 0))
        d = parse_date(rec.get("Transaction Date") or rec.get("Lead Date"))

        if d:
            if fy_start <= d <= today:
                f_onboarded_fy += val
            if cum_start <= d <= today:
                f_onboarded_cum += val
            if d == today:
                f_onboarded_today += 1
                f_onboarded_today_v += val
            if month_start <= d <= today:
                f_onboarded_month += 1
                f_onboarded_month_v += val
 
 
    # ========================= CREDIT FABRIX DATA (EXECUTIVE) =========================
    cred_today = cred_today_v = cred_month = cred_month_v = 0
    cred_docs = list(db["CreditFabriX_YTD"].find({"userName": user, "is_pending": {"$ne": True}}))
    cred_leads = list(db["CreditFabriX_PL"].find({"userName": user}))
   
    today_cred_transactions = []
    for rec in cred_docs:
        d = rec.get("Transaction Date")
        if isinstance(d, str):
            try: d = parse(d).date()
            except: d = None
        elif hasattr(d, "date"):
            d = d.date()
           
        if isinstance(d, date):
            val = to_float(rec.get("Loan Amount (INR Lakhs)", 0))
            if d == today:
                cred_today += 1
                cred_today_v += val
                today_cred_transactions.append(rec)
            if month_start <= d <= today:
                cred_month += 1
                cred_month_v += val
 
    # ========================= EXPECTED & OVERDUE (COMBINED EXECUTIVE) =========================
    combined_leads = leads + fs_leads + cred_leads
   
    expected_today_list = []
    expected_overdue = []
   
    exec_reported_data = load_reported_ids(to_email)
    today_str = today.strftime("%Y-%m-%d")
 
    for rec in combined_leads:
        # --- NEW FILTERS (EXECUTIVE) ---
        # Exclude if is_it_converted is anything other than 'No', empty, or None
        is_it_converted_val = str(rec.get("is_it_converted") or "No").lower().strip()
        is_converted = is_it_converted_val != "no"
        val = to_float(rec.get("taxable_sale_value") or rec.get("actual_taxable_sale_value") or rec.get("Loan Amount (INR Lakhs)", 0))
       
        if is_converted or val <= 2000:
            continue
 
        d = rec.get("Expected Date of Conversion")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
 
        if not hasattr(d, "date"):
            continue
 
        exp = d.date()
        rec["_exp"] = exp.strftime("%Y-%m-%d")
 
        # --- HIGHLIGHT LOGIC (EXECUTIVE) ---
        rem = str(rec.get("remarks", "")).lower().strip()
        inst = str(rec.get("interested", rec.get("Interested", rec.get("Intrested", "")))).lower().strip()
        is_no = rem == "no" or inst == "no"
        is_not_interested = "not interest" in rem or "not intrest" in rem or "not interest" in inst or "not intrest" in inst
        is_red = is_no or is_not_interested
 
        # --- ONLY ONCE FILTER ---
        rec_id = str(rec.get("_id"))
        last_reported = exec_reported_data.get(rec_id)
 
        # USER REQUEST: If red, report ONLY ONCE EVER
        if is_red and last_reported:
            continue
 
        if exp == today:
            expected_today_list.append(rec)
            exec_reported_data[rec_id] = today_str
        else:
            diff = (today - exp).days
            if exp < today and diff <= 45:
                if is_no: continue # USER REQUEST: Exclude 'No' interest from overdue table
                rec["_days"] = diff
                expected_overdue.append(rec)
                exec_reported_data[rec_id] = today_str
   
    save_reported_ids(exec_reported_data, to_email)
 
    # ----------- TODAY LEADS DETAIL ----------- #
    today_leads_detail = []
    for rec in leads:
        d = rec.get("Lead Date")
        if isinstance(d, str):
            try: d = parse(d)
            except: continue
        if hasattr(d, "date") and d.date() == today:
            today_leads_detail.append(rec)
 
    # ========================= HTML =========================
    html = f"""<!DOCTYPE html><html><head><style>
    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f7fa; }}
    .c {{ max-width: 95%; margin: 20px auto; background: white; padding: 20px; border-radius: 10px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
    th, td {{ padding: 8px; border: 1px solid #ccc; text-align: left; }}
    th {{ background-color: #f4f6f8; }}
    .gb {{ background-color: #e8f5e9; font-weight: bold; }}
    .gt {{ background-color: #f5f5f5; font-weight: bold; }}
    .tc {{ text-align: center; }}
    .btn {{ display: inline-block; background: #1a73e8; color: white !important; padding: 12px 22px; text-decoration: none; border-radius: 6px; font-weight: bold; }}
    h2, h3 {{ color: #333; }}
    .cl {{ color: #006400; }}
    .cb {{ color: #2e7d32; }}
    .ce {{ color: red; }}
    .co {{ color: #8b0000; }}
    </style></head><body><div class="c">
    <h2>AFX Daily Performance Report – {today.strftime("%B %d %Y")}</h2>
    <h3>Hi, {display_user}</h3>
    <h3 class="ca">Cumulative since Dec 2024–{today.year if today.month < 4 else today.year + 1}</h3>
    
    """
   
    # ---------------- INPUT SALES TRANSACTIONS SUMMARY (EXECUTIVE) ---------------- #
    html += f"""<h3>Input Sales Transactions Summary</h3><table><tr><th>Today Sales</th><th>Value ₹</th><th>Month Sales</th><th>Value ₹</th></tr>
    <tr><td>{trans_today}</td><td>₹ {format_indian_currency(trans_today_v)}</td><td>{trans_month}</td><td>₹ {format_indian_currency(trans_month_v)}</td></tr></table>"""
 
    # ---------------- TODAY INPUT SALES TRANSACTIONS (EXECUTIVE - DETAIL) ---------------- #
    html += """<h3 class='cl'>Today Input Sales Transaction Summary</h3><table><tr><th>Client</th><th>Phone</th><th>Type</th><th>District</th><th>Location</th><th>Product</th><th>Value</th></tr>"""
    if not today_trans_exec:
        html += "<tr><td colspan='7' class='tc'>No sales today</td></tr>"
    else:
        tot_trans_v = 0
        for r in today_trans_exec:
            val = to_float(r.get("taxable_sale_value", 0))
            tot_trans_v += val
            client_name = r.get('Client Name') or r.get('franchise_name') or 'N/A'
            html += f"<tr><td>{client_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type')}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>{r.get('Product Name')}</td><td>₹ {format_indian_currency(val)}</td></tr>"
        html += f"<tr class='gt'><td colspan='6'>TOTAL</td><td>₹ {format_indian_currency(tot_trans_v)}</td></tr>"
    html += "</table>"

    # ---------------- INPUTFABRIX LEADS SUMMARY ---------------- #
    html += f"""<h3>Input Leads Summary</h3><table><tr><th>Today Leads</th><th>Value ₹</th><th>Month Leads</th><th>Value ₹</th></tr><tr><td>{lead_today}</td><td>₹ {format_indian_currency(lead_today_v)}</td><td>{lead_month}</td><td>₹ {format_indian_currency(lead_month_v)}</td></tr><tr><td colspan="2">Average Lead Conversion Time</td><td colspan="2">{avg_conversion_days:.1f} Days</td></tr></table>"""
 
    # ---------------- TODAY INPUTFABRIX LEADS (DETAIL) ---------------- #
    html += """<h3 class='cl'>Today Input Leads</h3><table><tr><th>Client</th><th>Type</th><th>Phone</th><th>District</th><th>Location</th><th>Product</th><th>Value</th></tr>"""
   
    today_leads_value = 0
    for r in today_leads_detail:
        val = to_float(r.get("taxable_sale_value", 0))
        today_leads_value += val
        html += f"<tr><td>{r.get('Client Name')}</td><td>{r.get('Client_Type')}</td><td>{r.get('contact_number')}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>{r.get('Product Name')}</td><td>₹ {format_indian_currency(val)}</td></tr>"
 
    html += f"<tr class='gt'><td colspan='6'>TOTAL</td><td>₹ {format_indian_currency(today_leads_value)}</td></tr></table>"
 
    # ---------------- ONBOARDED FRANCHISE SUMMARY (EXECUTIVE) ---------------- #
    html += f"""<h3>Onboarded Franchise Summary</h3><table><tr><th>Today Count</th><th>Value ₹</th><th>Month Count</th><th>Value ₹</th><th>FY Value ₹</th><th>Cumulative ₹</th></tr>
    <tr><td>{f_onboarded_today}</td><td>₹ {format_indian_currency(f_onboarded_today_v)}</td><td>{f_onboarded_month}</td><td>₹ {format_indian_currency(f_onboarded_month_v)}</td><td>₹ {format_indian_currency(f_onboarded_fy)}</td><td>₹ {format_indian_currency(f_onboarded_cum)}</td></tr></table>"""
 
    # ---------------- ONBOARDED FRANCHISES (EXECUTIVE - DETAIL) ---------------- #
    html += """<h3 class='cl'>Onboarded Franchises</h3><table><tr><th>Franchise Name</th><th>Phone</th><th>Type</th><th>State</th><th>District</th><th>Location</th><th>Value</th></tr>"""
    if not all_f_onboarded_exec:
        html += "<tr><td colspan='7' class='tc'>No franchises onboarded</td></tr>"
    else:
        tot_ob_v = 0
        for r in all_f_onboarded_exec:
            val = to_float(r.get("taxable_sale_value", 0))
            tot_ob_v += val
            franchise_name = r.get('franchise_name') or 'N/A'
            state = r.get('State') or r.get('state') or 'N/A'
            html += f"<tr><td>{franchise_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type')}</td><td>{state}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>₹ {format_indian_currency(val)}</td></tr>"
        html += f"<tr class='gt'><td colspan='6'>TOTAL</td><td>₹ {format_indian_currency(tot_ob_v)}</td></tr>"
    html += "</table>"
 
    # ---------------- FRANCHISE LEADS SUMMARY (EXECUTIVE) ---------------- #
    html += f"""<h3>Franchise Leads Summary</h3><table><tr><th>Today Leads</th><th>Value ₹</th><th>Month Leads</th><th>Value ₹</th><th>Total Leads</th><th>Total Value ₹</th></tr>
    <tr><td>{f_lead_today}</td><td>₹ {format_indian_currency(f_lead_today_v)}</td><td>{f_lead_month}</td><td>₹ {format_indian_currency(f_lead_month_v)}</td><td>{f_lead_total}</td><td>₹ {format_indian_currency(f_lead_total_v)}</td></tr></table>"""
 
    # ---------------- FRANCHISE LEADS (EXECUTIVE - DETAIL) ---------------- #
    html += """<h3 class='cl'>Franchise Leads</h3><table><tr><th>S.No.</th><th>Franchise Name</th><th>Phone</th><th>Type</th><th>State</th><th>District</th><th>Location</th><th>Value</th></tr>"""
    if not all_f_leads_exec:
        html += "<tr><td colspan='8' class='tc'>No leads found</td></tr>"
    else:
        tot_f_v = 0
        for idx, r in enumerate(all_f_leads_exec, 1):
            val = to_float(r.get("taxable_sale_value", 0))
            tot_f_v += val
            franchise_name = r.get('franchise_name') or 'N/A'
            state = r.get('State') or r.get('state') or 'N/A'
            html += f"<tr><td>{idx}</td><td>{franchise_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type')}</td><td>{state}</td><td>{r.get('District')}</td><td>{r.get('Location')}</td><td>₹ {format_indian_currency(val)}</td></tr>"
        html += f"<tr class='gt'><td colspan='7'>TOTAL</td><td>₹ {format_indian_currency(tot_f_v)}</td></tr>"
    html += "</table>"
 
    # ---------------- TODAY ADDED BUYERS (EXECUTIVE) ---------------- #
    html += """<h3 class='cb'>Today Added Buyers</h3><table><tr><th>S.No.</th><th>Buyer Name</th><th>Phone</th><th>Buyer Type</th><th>Pincode</th><th>District</th><th>Location</th></tr>"""
    if not today_added_buyers:
        html += "<tr><td colspan='7' class='tc'>No buyers added today</td></tr>"
    else:
        for idx, b in enumerate(today_added_buyers, 1):
            pincode = b.get('pincode') or b.get('pinCode') or 'N/A'
            html += f"<tr><td>{idx}</td><td>{b.get('buyerName', 'N/A')}</td><td>{b.get('phone', 'N/A')}</td><td>{b.get('selectBuyerType', 'N/A')}</td><td>{pincode}</td><td>{b.get('district', 'N/A')}</td><td>{b.get('cityName', 'N/A')}</td></tr>"
    html += "</table>"

    # ---------------- CREDIT FABRIX TRANSACTION SUMMARY (EXECUTIVE) ---------------- #
    html += f"""<h3>CreditFabriX Transaction Summary</h3><table><tr><th>Today Count</th><th>Today Value ₹</th><th>Month Count</th><th>Month Value ₹</th></tr>
    <tr><td>{cred_today}</td><td>₹ {format_indian_currency(cred_today_v)}</td><td>{cred_month}</td><td>₹ {format_indian_currency(cred_month_v)}</td></tr></table>"""
 
    # ---------------- TODAY'S CREDIT FABRIX TRANSACTIONS (EXECUTIVE) ---------------- #
    html += """<h3>Today's CreditFabriX Transactions</h3><table><tr><th>FPO Name</th><th>Loan Amount (INR)</th><th>Legal Status</th><th>District</th><th>Location</th></tr>"""
    if not today_cred_transactions:
        html += "<tr><td colspan='5' class='tc'>No updates today</td></tr>"
    else:
        tot_loan = 0
        for rec in today_cred_transactions:
            val = to_float(rec.get("Loan Amount (INR Lakhs)", 0))
            tot_loan += val
            html += f"<tr><td>{rec.get('FPO Name')}</td><td>₹ {format_indian_currency(val)}</td><td>{rec.get('Legal Status')}</td><td>{rec.get('District')}</td><td>{rec.get('Location')}</td></tr>"
        html += f"<tr class='gt'><td colspan='2'>TOTAL</td><td>₹ {format_indian_currency(tot_loan)}</td><td colspan='2'></td></tr>"
    html += "</table>"
 
    # ---------------- EXPECTED TODAY ---------------- #
    html += """<h3 class='ce'>Expected Today</h3><table><tr><th>S.No.</th><th>Client</th><th>Type</th><th>Phone</th><th>District</th><th>Location</th><th>Exp Date</th><th>Product</th><th>Value</th></tr>"""
   
    total_expected_value = 0
    for idx, r in enumerate(expected_today_list, 1):
        val = to_float(r.get("taxable_sale_value"))
        total_expected_value += val
       
        # Highlight Logic (Robust)
        rem = r.get("remarks", "")
        if rem is None: rem = ""
        rem = str(rem).lower().strip()
        
        inst = r.get("interested", r.get("Interested", r.get("Intrested", "")))
        if inst is None: inst = ""
        inst = str(inst).lower().strip()
       
        row_style = ""
        # Check if any field contains "No" or "Not Interested" (including common typos)
        is_no = rem == "no" or inst == "no"
        is_not_interested = "not interest" in rem or "not intrest" in rem or "not interest" in inst or "not intrest" in inst
       
        if is_no or is_not_interested:
            row_style = ' style="background-color: #ffebee; color: red;"'
           
        client_name = r.get('Client Name') or r.get('customer_name') or r.get('franchise_name') or r.get('FPO Name') or 'N/A'
        html += f"<tr{row_style}><td>{idx}</td><td>{client_name}</td><td>{r.get('Client_Type') or r.get('Business_Type')}</td><td>{r.get('contact_number')}</td><td>{r.get('District') or 'N/A'}</td><td>{r.get('Location') or 'N/A'}</td><td>{r.get('_exp')}</td><td>{r.get('Product Name') or 'Credit/Consultancy'}</td><td>₹ {format_indian_currency(val)}</td></tr>"
 
    html += f"<tr class='gt'><td colspan='8'>TOTAL</td><td>₹ {format_indian_currency(total_expected_value)}</td></tr></table>"
 
    # ---------------- OVERDUE (LAST 45 DAYS) ---------------- #
    html += """<h3 class='co'>Overdue (Last 45 Days)</h3><table><tr><th>S.No.</th><th>Client</th><th>Phone</th><th>Type</th><th>District</th><th>Location</th><th>Exp Date</th><th>Product</th><th>Value</th><th>Days</th></tr>"""
   
    total_overdue_value = 0
    for idx, r in enumerate(expected_overdue, 1):
        val = to_float(r.get("taxable_sale_value"))
        total_overdue_value += val
       
        # Highlight Logic (Robust)
        rem = r.get("remarks", "")
        if rem is None: rem = ""
        rem = str(rem).lower().strip()
        
        inst = r.get("interested", r.get("Interested", r.get("Intrested", "")))
        if inst is None: inst = ""
        inst = str(inst).lower().strip()
       
        row_style = ""
        # Check if any field contains "No" or "Not Interested" (including common typos)
        is_no = rem == "no" or inst == "no"
        is_not_interested = "not interest" in rem or "not intrest" in rem or "not interest" in inst or "not intrest" in inst
       
        if is_no or is_not_interested:
            row_style = ' style="background-color: #ffebee; color: red;"'
           
        client_name = r.get('Client Name') or r.get('customer_name') or r.get('franchise_name') or r.get('FPO Name') or 'N/A'
        html += f"<tr{row_style}><td>{idx}</td><td>{client_name}</td><td>{r.get('contact_number')}</td><td>{r.get('Client_Type') or r.get('Business_Type')}</td><td>{r.get('District') or 'N/A'}</td><td>{r.get('Location') or 'N/A'}</td><td>{r.get('_exp')}</td><td>{r.get('Product Name') or 'Credit/Consultancy'}</td><td>₹ {format_indian_currency(val)}</td><td>{r.get('_days')}</td></tr>"
 
    html += f"<tr class='gt'><td colspan='8'>TOTAL</td><td>₹ {format_indian_currency(total_overdue_value)}</td><td></td></tr></table>"
 
 
 
    # ---------------- FOOTER ---------------- #
    html += f"""<div style="text-align:center;margin-top:30px;"><a href="{PORTAL_URL}" class="btn">Open AFX Portal</a></div></div></body></html>"""
    send_pipeline_email(to_email, html, cc_list)
 
 

# def send_morning_executive_report(user, to_email, cc_emails=None):
#     client = MongoClient(MONGO_URL)
#     db = client["agrifabrix"]
#     display_user = DISPLAY_NAME_MAP.get(user, user)
#     today = datetime.now().date()
    
#     # Fetch leads
#     leads = list(db["InputFabriX_PL"].find({"userName": user}))
    
#     expected_today = []
    
#     for rec in leads:
#         d = rec.get("Expected Date of Conversion")
#         if isinstance(d, str):
#             try: d = parse(d)
#             except: continue
#         if not hasattr(d, "date"): continue

#         if d.date() == today:
#             expected_today.append(rec)
            
#     if not expected_today:
#         print(f"No leads expected today for {user}. Skipping email.")
#         return

#     # Generate HTML
#     total_val = 0
#     html = f"""<!DOCTYPE html><html><head><style>
#     body {{ font-family: Arial, sans-serif; background-color: #f5f7fa; padding: 20px; }}
#     .c {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; border: 1px solid #ddd; }}
#     h2 {{ color: #2c3e50; text-align: center; }}
#     table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
#     th, td {{ padding: 10px; border: 1px solid #ddd; text-align: left; font-size: 14px; }}
#     th {{ background-color: #f8f9fa; }}
#     .hl {{ background-color: #ffebee; }} /* Highlight row */
#     .btn {{ display: block; width: 200px; margin: 20px auto; padding: 10px; background: #007bff; color: white; text-align: center; text-decoration: none; border-radius: 5px; }}
#     </style></head><body><div class="c">
#     <h2>🌅 Morning Follow-up: Leads Expected Today</h2>
#     <p>Hi {display_user}, here are the leads expected to convert today ({today}). Please follow up!</p>
#     <table><tr><th>Client</th><th>Phone</th><th>Product</th><th>Value</th></tr>"""

#     for r in expected_today:
#         val = to_float(r.get("taxable_sale_value", 0))
#         total_val += val
        
#         # Highlight logic (same as daily report)
#         rem = str(r.get("remarks", "")).lower()
#         inst = str(r.get("interested", r.get("Interested", r.get("Intrested", "")))).lower()
#         row_class = ""
#         if any(x in rem or x in inst for x in ["no", "not interested"]):
#             row_class = " class='hl'"
            
#         html += f"<tr{row_class}><td>{r.get('Client Name')}</td><td>{r.get('contact_number')}</td><td>{r.get('Product Name')}</td><td>₹ {format_indian_currency(val)}</td></tr>"

#     html += f"<tr><td colspan='3'><b>TOTAL</b></td><td><b>₹ {format_indian_currency(total_val)}</b></td></tr></table>"
#     html += f"""<a href="{PORTAL_URL}" class="btn">Open Portal</a></div></body></html>"""

#     # Email Sending
#     msg = MIMEMultipart()
#     msg["From"] = EMAIL
#     msg["To"] = to_email
#     if cc_emails:
#         msg["Cc"] = ", ".join(cc_emails)
    
#     msg["Subject"] = f"🔔 Action Required: {len(expected_today)} Leads Expected Today - {today}"
#     msg.attach(MIMEText(html, "html"))
    
#     recipients = [to_email] + (cc_emails if cc_emails else [])
    
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(EMAIL, EMAIL_PASSWORD)
#     server.sendmail(EMAIL, recipients, msg.as_string())
#     server.quit()
#     print(f"✅ Context email sent to {to_email}")

# ---------------- ADMIN LIST ---------------- #
def get_admin_emails():
    # return ["priya.kota@agrifabrix.com","kumarvinod15452@gmail.com","devendar.mallelli@agrifabrix.com"]
    return ["associate@agrifabrix.com","nagasaiyaswanthbandaru@gmail.com", "Kumarvinod15452@gmail.com", "suresh.naraparaju@agrifabrix.com", "srinimiriyala@gmail.com"]


# ---------------- MAIN EXECUTION ---------------- #
if __name__ == "__main__":
    # Deduplicate Admin Recipients
    admin_recipients = list(set(get_admin_emails() + SUPERADMIN_EMAILS))
    for email in admin_recipients:
        send_today_pipeline_report(email)

    # Executive Reports
    for user, email in EXECUTIVE_EMAILS.items():
        send_executive_pipeline_report(user, email, EXECUTIVE_CC)
