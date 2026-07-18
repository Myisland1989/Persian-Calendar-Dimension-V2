# Persian-Calendar-Dimension-V2
Generate a Persian (Jalali) calendar dimension table with holidays for Excel, Power BI, SQL Server and data warehouses.
# 🇮🇷 Persian Calendar Dimension

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green.svg)
![OpenPyXL](https://img.shields.io/badge/OpenPyXL-Excel-success.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Generate a complete **Persian (Jalali) Calendar Dimension** with official holidays, working-day indexes and rich date attributes for **Excel, Power BI, SQL Server, Power Query, Power Pivot, and Data Warehouses**.

---

# Features

✅ Jalali (Persian) Calendar

✅ Gregorian Calendar

✅ Official Holidays (API)

✅ Manual Holiday Adjustment File

✅ Holiday Name

✅ Working Day Index

✅ Working Day of Year

✅ Week Index

✅ Month Index

✅ Season

✅ Persian Month Name

✅ Persian Weekday Name

✅ Date Dimension Ready

---

# Sample Output

| Jalali_Date | Gregorian_Date | Holiday_Final | Holiday_Name_Final | Index_WorkingDay | Year_WorkingDay |
|-------------|----------------|---------------|--------------------|------------------|-----------------|
|1404/01/01|2025-03-21|TRUE|Nowruz|0|0|
|1404/01/02|2025-03-22|TRUE|Nowruz Holiday|0|0|
|1404/01/03|2025-03-23|FALSE||1|1|
|1404/01/04|2025-03-24|FALSE||2|2|

---

# Calendar Columns

| Column | Description |
|---------|-------------|
|Date_Index|Global Date Index|
|Jalali_Date|Persian Date|
|Gregorian_Date|Gregorian Date|
|Year|Persian Year|
|Season|Season|
|Month_Index|Global Month Index|
|Month_Of_Year|Month Number|
|Month_Name|Persian Month Name|
|Day|Day of Month|
|DayOfYear|Day of Year|
|DayOfWeek|Weekday Name|
|Week_Index|Global Week Index|
|Week_Of_Year|Week Number|
|Holiday_Final|Final Holiday Flag|
|Holiday_Name_Final|Holiday Name|
|Index_WorkingDay|Global Working Day Index|
|Year_WorkingDay|Working Day of Year|

---

# Holiday Adjustment

The project supports manual holiday corrections without changing the Python source code.

Simply create

```
Holiday_Adjustment.xlsx
```

with the following structure.

| Jalali_Date | Holiday_Final | Holiday_Name | ADD/Remove/Change | Note |
|-------------|---------------|--------------|-------------------|------|

Example

| Jalali_Date | Holiday_Final | Holiday_Name | ADD/Remove/Change |
|-------------|---------------|--------------|-------------------|
|1404/05/12|TRUE|Government Holiday|ADD|
|1404/06/15|FALSE||REMOVE|
|1404/07/10|TRUE|Special Holiday|CHANGE|

The program automatically merges the adjustment file with the downloaded calendar.

---

# Installation

Clone the repository

```bash
https://github.com/Myisland1989/Persian-Calendar-Dimension-V2.git
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
python persian_calendar.py
```

---

# Requirements

- Python 3.10+
- pandas
- requests
- openpyxl

---

# Output

The generated Excel file contains:

- Calendar
- Holiday_API
- Holiday_Adjustment (template)

---

# Roadmap

- [x] Holiday Adjustment File
- [x] Working Day Index
- [x] Working Day Of Year
- [ ] Working Day Of Month
- [ ] Working Day Of Week
- [ ] CSV Export
- [ ] SQL Export
- [ ] Power BI Template
- [ ] Command Line Parameters
- [ ] GUI Version

---

# Contributing

Contributions, ideas and pull requests are welcome.

---

# License

# Screenshots

## Calendar

![Calendar](screenshots/calendar.png)
<img width="1920" height="1017" alt="PowerPivot" src="https://github.com/user-attachments/assets/0d0234e2-6073-4bfd-8a3b-41af46d3d0a7" />

## Holiday Adjustment

![Adjustment](screenshots/adjustment.png)

## Power BI Example

![Power BI](screenshots/powerbi.png)

MIT License

---

Made with ❤️ for the Persian data community.
