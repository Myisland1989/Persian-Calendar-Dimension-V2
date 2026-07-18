import requests
import pandas as pd
from datetime import datetime


# =========================
# Settings
# =========================

start_year = 1398
end_year = 1400

output_file = "Persian_Calendar_1398_1400.xlsx"



# =========================
# Persian names
# =========================

month_names = {
    1: "فروردین",
    2: "اردیبهشت",
    3: "خرداد",
    4: "تیر",
    5: "مرداد",
    6: "شهریور",
    7: "مهر",
    8: "آبان",
    9: "آذر",
    10: "دی",
    11: "بهمن",
    12: "اسفند"
}


day_names = {

    "ج": "جمعه",
    "ش": "شنبه",
    "ی": "یکشنبه",
    "د": "دوشنبه",
    "س": "سه شنبه",
    "چ": "چهارشنبه",
    "پ": "پنجشنبه"

}


weekday_offset = {

    "ش": 0,
    "ی": 1,
    "د": 2,
    "س": 3,
    "چ": 4,
    "پ": 5,
    "ج": 6

}





def get_season_number(month):
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    return 4

def get_season(month):

    if month <= 3:
        return "بهار"

    elif month <= 6:
        return "تابستان"

    elif month <= 9:
        return "پاییز"

    else:
        return "زمستان"



# =========================
# Storage
# =========================

calendar_rows = []
holiday_rows = []


date_index = 1


# Global indexes
global_week_index = 1
global_month_index = 1
global_season_index = 1



# =========================
# Download
# =========================

for year in range(start_year, end_year + 1):

    print("Downloading", year)


    url = (
        f"https://pnldev.com/api/calender"
        f"?year={year}&holiday=true"
    )


    response = requests.get(url)

    data = response.json()

    months = data["result"]


    day_of_year = 1


    # reset every year
    week_of_year = 1


    month_of_year = 1


    first_day_offset = None


    for month in months:


        # month index increases globally
        current_month_index = global_month_index
        current_season_index = global_season_index


        for day in months[month]:


            item = months[month][day]


            solar = item["solar"]

            greg = item["gregorian"]



            jalali_date = (
                f"{solar['year']}/"
                f"{solar['month']:02d}/"
                f"{solar['day']:02d}"
            )


            gregorian_date = datetime(
                greg["year"],
                greg["month"],
                greg["day"]
            )



            holiday_name = ""

            if item["event"]:

                holiday_name = " - ".join(item["event"])



            # =========================
            # Week calculation
            # =========================


            if day_of_year == 1:

                first_day_offset = (
                    weekday_offset[
                        solar["dayWeek"]
                    ]
                )


            week_of_year = (
                (
                    day_of_year
                    +
                    first_day_offset
                    -
                    1
                )
                // 7
            ) + 1



            # Global week index
            if (
                day_of_year != 1
                and solar["dayWeek"] == "ش"
            ):

                global_week_index += 1



            # =========================
            # Holiday raw
            # =========================

            if item["holiday"]:

                holiday_rows.append({

                    "Jalali_Date":
                    jalali_date,

                "Jalali_Date_Int":
                    int(f"{solar['year']}{solar['month']:02d}{solar['day']:02d}"),

                    "Gregorian_Date":
                        gregorian_date,

                    "Holiday":
                        True,

                    "Holiday_Name":
                        holiday_name

                })




            # =========================
            # Calendar
            # =========================

            calendar_rows.append({

                "Date_Index":
                    date_index,


                "Jalali_Date":
                    jalali_date,

"Jalali_Date_Int":
    int(f"{solar['year']}{solar['month']:02d}{solar['day']:02d}"),


                "Gregorian_Date":
                    gregorian_date,


                "Year":
                    solar["year"],


                "Season":
                    get_season(solar["month"]),

                "Season_Number":
                    get_season_number(solar["month"]),

                "Season_Index":
                    current_season_index,

"Month_Name":
                    month_names[
                        solar["month"]
                    ],


"Year_Month":
                    f"{solar['year']}-{solar['month']:02d}",

                "Month_Of_Year":
                    solar["month"],
                    
                    "Month_Index":
                    current_month_index,


                "DayOfWeek":
                    day_names[
                        solar["dayWeek"]
                    ],
                    
                    "DayOfMonth":
                    solar["day"],



                "DayOfYear":
                    day_of_year,


"Week_Of_Year":
                    week_of_year,
                

                "Week_Index":
                    global_week_index,


                "Holiday_API":
                    item["holiday"],



                "Holiday_Name_API":
                    holiday_name,



                "Holiday_Final":
                    item["holiday"],



                "Holiday_Name_Final":
                    holiday_name

            })



            date_index += 1

            day_of_year += 1



        # after each month
        global_month_index += 1
        if int(month) in (3,6,9,12):
            global_season_index += 1




# =========================
# DataFrames
# =========================

df_calendar = pd.DataFrame(calendar_rows)

df_holiday = pd.DataFrame(holiday_rows)


df_adjustment = pd.DataFrame(
    columns=[
        "Jalali_Date",
        "Holiday_Final",
        "Holiday_Name"
    ]
)

# =========================
# Apply Holiday Adjustments
# =========================

import os

adjustment_file = "Holiday_Adjustment.xlsx"

if os.path.exists(adjustment_file):

    print("Applying Holiday Adjustments...")

    df_adjust = pd.read_excel(adjustment_file)

    # فقط سطرهایی که تاریخ دارند
    df_adjust = df_adjust[df_adjust["Jalali_Date"].notna()]

    # تبدیل Holiday_Final به bool
    df_adjust["Holiday_Final"] = (
        df_adjust["Holiday_Final"]
        .astype(str)
        .str.strip()
        .str.upper()
        .map({
            "TRUE": True,
            "FALSE": False,
            "1": True,
            "0": False
        })
        .fillna(False)
        .astype(bool)
    )

    # Merge
    df_calendar = df_calendar.merge(
        df_adjust,
        on="Jalali_Date",
        how="left",
        suffixes=("", "_Adjust")
    )

    # ---------- ADD ----------
    mask = (
        df_calendar["ADD/Remove/Change"]
        .astype(str)
        .str.strip()
        .str.upper()
        == "ADD"
    )

    df_calendar.loc[mask, "Holiday_Final"] = True

    df_calendar.loc[
        mask,
        "Holiday_Name_Final"
    ] = df_calendar.loc[
        mask,
        "Holiday_Name"
    ]


    # ---------- REMOVE ----------
    mask = (
        df_calendar["ADD/Remove/Change"]
        .astype(str)
        .str.strip()
        .str.upper()
        == "REMOVE"
    )

    df_calendar.loc[mask, "Holiday_Final"] = False

    df_calendar.loc[
        mask,
        "Holiday_Name_Final"
    ] = ""


    # ---------- CHANGE ----------
    mask = (
        df_calendar["ADD/Remove/Change"]
        .astype(str)
        .str.strip()
        .str.upper()
        == "CHANGE"
    )

    df_calendar.loc[
        mask,
        "Holiday_Final"
    ] = (
        df_calendar.loc[
            mask,
            "Holiday_Final_Adjust"
        ]
        .astype(bool)
    )

    df_calendar.loc[
        mask,
        "Holiday_Name_Final"
    ] = df_calendar.loc[
        mask,
        "Holiday_Name"
    ]


    # حذف ستون‌های کمکی
    df_calendar.drop(
        columns=[
            "Holiday_Final_Adjust",
            "Holiday_Name",
            "ADD/Remove/Change",
            "Note"
        ],
        inplace=True,
        errors="ignore"
    )

    print("Holiday Adjustments Applied.")

else:

    print("Holiday_Adjustment.xlsx not found. Skipped.")
    
    # =========================
# Working Day Indexes
# =========================

# روزهای کاری (غیرتعطیل)
working_mask = ~df_calendar["Holiday_Final"]

# شماره روز کاری در کل تقویم
df_calendar["Index_WorkingDay"] = 0
df_calendar.loc[working_mask, "Index_WorkingDay"] = range(
    1,
    working_mask.sum() + 1
)

# شماره روز کاری در هر سال
df_calendar["Year_WorkingDay"] = 0

df_calendar.loc[working_mask, "Year_WorkingDay"] = (
    working_mask[working_mask]
    .groupby(df_calendar.loc[working_mask, "Year"])
    .cumcount()
    + 1
)
    
# =========================
# Export
# =========================

with pd.ExcelWriter(
    output_file,
    engine="openpyxl",
    date_format="yyyy-mm-dd"
) as writer:


    df_calendar.to_excel(
        writer,
        sheet_name="Calendar",
        index=False
    )


    df_holiday.to_excel(
        writer,
        sheet_name="Holiday_API",
        index=False
    )


    df_adjustment.to_excel(
        writer,
        sheet_name="Holiday_Adjustment",
        index=False
    )



print("========================")
print("Finished Successfully")
print(output_file)
print("========================")
