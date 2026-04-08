import json
import os
from datetime import datetime, date
from dateutil.parser import parse
from pymongo import MongoClient

# ---------------- CONFIG ---------------- #
ALLOWED_USERS = {"Srinivasulu Mendu", "Sahithya", "Sruthi Devi", "Losherwar Ramdas", "Kalpana B"}
DISPLAY_USERS_ORDER = [
    "Losherwar Ramdas",
    "Sruthi Devi",
    "Sahithya",
    "Srinivasulu Mendu",
    "Kalpana B",
]

DISPLAY_NAME_MAP = {
    "Sruthi Devi": "Sruthi Devi",
    "Losherwar Ramdas": "Losherwar Ramdas",
    "Sahithya": "Sahithya",
    "Srinivasulu Mendu": "Srinivasulu Mendu",
    "Kalpana B": "Kalpana B"
}

AFX_COLLECTIONS = [
    "InputFabriX_YTD",
    "Consultancy_Services",
    "Marketing",
    "CreditFabriX_YTD",
    "Franchise_Stores_YTD",
    "Onboarded_Franchises"
]

CATEGORY_ORDER = [
    "Soil Health",
    "Seeds",
    "Crop Nutrition",
    "Crop Protection",
    "Smart Irrigation",
    "Farm Machinery",
    "Post Harvest Storage",
    "Processing & Value Addition",
]

def calculate_afx_earnings(db, collection_names, start_date=None, end_date=None):
    total = 0.0
    ALLOWED_COLLS = ["InputFabriX_YTD", "CreditFabriX_YTD"]
    EXCLUDE_COLLS = ["Franchise_Stores_YTD", "Onboarded_Franchises"]
    EXCLUDE_USERS = ["pavani_jyothi"]

    for col_name in collection_names:
        records = list(db[col_name].find({"is_pending": {"$ne": True}}))
        
        # Apply Filters
        if col_name in ALLOWED_COLLS:
            records = [r for r in records if r.get("userName") in ALLOWED_USERS]
        elif col_name in EXCLUDE_COLLS:
            records = [r for r in records if r.get("userName") not in EXCLUDE_USERS]

        for r in records:
            commission = to_float(r.get("agrifabrix_commission", 0))

            if start_date and end_date:
                d = parse_date(r.get("Transaction Date") or r.get("Date"))
                if d and start_date <= d <= end_date:
                    total += commission
            else:
                total += commission
    return total

def get_stream_data(db, collection_name, fy_start, today, cum_start, user=None):
    coll = db[collection_name]
    query = {"is_pending": {"$ne": True}}
    if user:
        query["userName"] = user
    recs = list(coll.find(query))
        
    fy_val = 0.0
    cum_val = 0.0
    fy_afx = 0.0
    cum_afx = 0.0
    
    for r in recs:
        if collection_name == "CreditFabriX_YTD":
            val_field = "Loan Amount (INR Lakhs)"
        elif collection_name == "Consultancy_Services":
            val_field = "Amount"
        else:
            val_field = "taxable_sale_value"
        
        val = to_float(r.get(val_field, 0))
        afx = to_float(r.get("agrifabrix_commission", 0))
        
        d = parse_date(r.get("Transaction Date") or r.get("Date"))
        
        # Cumulative (Since Dec 2024 as per user request)
        if d and cum_start <= d <= today:
            cum_val += val
            cum_afx += afx
            
        # Financial Year
        if d and fy_start <= d <= today:
            fy_val += val
            fy_afx += afx
               
    return fy_val, cum_val, fy_afx, cum_afx
def to_float(val):
    try:
        return float(str(val).replace(",", "").strip())
    except:
        return 0.0

def format_indian_currency(amount):
    """Formats a number in Indian currency format (Lakhs, Crores)."""
    try:
        amount = round(float(amount))
        s = str(amount)
        if len(s) <= 3:
            return s
        
        last_three = s[-3:]
        remaining = s[:-3]
        
        groups = []
        while remaining:
            groups.append(remaining[-2:])
            remaining = remaining[:-2]
        
        return ",".join(reversed(groups)) + "," + last_three
    except:
        return str(amount)

def get_fiscal_year_start(today=None):
    if today is None:
        today = datetime.now().date()
    return date(today.year if today.month >= 4 else today.year - 1, 4, 1)

def get_cumulative_start_date():
    return date(2024, 12, 1)

def get_cumulative_label(today=None):
    if today is None:
        today = datetime.now().date()
    fy_end_year = today.year if today.month < 4 else today.year + 1
    return f"Cumulative since Dec 2024–{fy_end_year}"

def get_db_client(mongo_url):
    return MongoClient(mongo_url)

def parse_date(d):
    if isinstance(d, str):
        try:
            return parse(d).date()
        except:
            return None
    elif isinstance(d, datetime):
        return d.date()
    elif isinstance(d, date):
        return d
    return None

def get_raw_agg_vals(db, coll_names, fy_start, today, cum_start, user=None):
    val_sum = fy_val_sum = afx_sum = fy_afx_sum = 0.0
    for cn in coll_names:
        query = {"is_pending": {"$ne": True}}
        if user:
            query["userName"] = user
        recs = list(db[cn].find(query))
        for r in recs:
            if cn == "CreditFabriX_YTD":
                v_f = "Loan Amount (INR Lakhs)"
            elif cn == "Consultancy_Services":
                v_f = "Amount"
            else:
                v_f = "taxable_sale_value"
                
            val = to_float(r.get(v_f, 0))
            afx = to_float(r.get("agrifabrix_commission", 0))
            
            d = parse_date(r.get("Transaction Date") or r.get("Date"))
            
            if d:
                # Cumulative (Since Dec 2024)
                if cum_start <= d <= today:
                    val_sum += val
                    afx_sum += afx
                
                # Financial Year
                if fy_start <= d <= today:
                    fy_val_sum += val
                    fy_afx_sum += afx
                    
    return {"fy": fy_val_sum, "cum": val_sum, "fy_afx": fy_afx_sum, "cum_afx": afx_sum}

def check_if_converted(rec):
    """Checks if a lead record is marked as converted."""
    val = rec.get("is_it_converted")
    if isinstance(val, str):
        low_val = str(val).lower().strip()
        return low_val in ["yes", "true", "partially_yes"]
    return val is True
