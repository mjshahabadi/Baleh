from datetime import date


JALALI_MONTH_NAMES = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
]

WEEKDAY_LABELS = {
    "sat": "ش",
    "sun": "ی",
    "mon": "د",
    "tue": "س",
    "wed": "چ",
    "thu": "پ",
    "fri": "ج",
}

PYTHON_WEEKDAY_BY_KEY = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}


class JalaliCalendar:
    """Render Jalali month calendars as Bale inline keyboards."""

    @staticmethod
    def build_month_keyboard(
        year,
        month,
        action_code,
        week_start="sat",
        select_callback_prefix=None,
        min_year=None,
        max_year=None,
    ):
        year = int(year)
        month = int(month)
        week_start = str(week_start or "sat").lower()
        if week_start not in PYTHON_WEEKDAY_BY_KEY:
            week_start = "sat"

        select_callback_prefix = select_callback_prefix or f"CALSELECT:{action_code}:"
        min_year = int(min_year or year)
        max_year = int(max_year or year)

        keyboard = []
        keyboard.append([
            {
                "text": f"{JALALI_MONTH_NAMES[month - 1]} {JalaliCalendar.to_persian_digits(year)}",
                "callback_data": "CAL:NOOP",
            }
        ])

        keyboard.append([
            {"text": WEEKDAY_LABELS[key], "callback_data": "CAL:NOOP"}
            for key in JalaliCalendar._ordered_weekdays(week_start)
        ])

        first_weekday = JalaliCalendar._python_weekday(year, month, 1)
        leading_blanks = JalaliCalendar._weekday_offset(first_weekday, week_start)
        days_in_month = JalaliCalendar.days_in_month(year, month)

        row = [{"text": " ", "callback_data": "CAL:NOOP"} for _ in range(leading_blanks)]

        for day in range(1, days_in_month + 1):
            callback_data = f"{select_callback_prefix}{year:04d}-{month:02d}-{day:02d}"
            row.append({
                "text": JalaliCalendar.to_persian_digits(day),
                "callback_data": callback_data,
            })

            if len(row) == 7:
                keyboard.append(row)
                row = []

        if row:
            row.extend({"text": " ", "callback_data": "CAL:NOOP"} for _ in range(7 - len(row)))
            keyboard.append(row)

        previous_year, previous_month = JalaliCalendar._shift_month(year, month, -1)
        next_year, next_month = JalaliCalendar._shift_month(year, month, 1)

        nav_row = []
        if previous_year >= min_year:
            nav_row.append({
                "text": "◀️ ماه قبل",
                "callback_data": f"CAL:{action_code}:{previous_year:04d}:{previous_month:02d}",
            })

        nav_row.append({"text": "بستن", "callback_data": "CAL:CLOSE"})

        if next_year <= max_year:
            nav_row.append({
                "text": "ماه بعد ▶️",
                "callback_data": f"CAL:{action_code}:{next_year:04d}:{next_month:02d}",
            })

        keyboard.append(nav_row)

        return {"inline_keyboard": keyboard}

    @staticmethod
    def days_in_month(year, month):
        month = int(month)
        if month <= 6:
            return 31
        if month <= 11:
            return 30
        return 30 if JalaliCalendar.is_leap_year(int(year)) else 29

    @staticmethod
    def is_leap_year(year):
        return (JalaliCalendar.jalali_to_gregorian(year + 1, 1, 1) - JalaliCalendar.jalali_to_gregorian(year, 1, 1)).days == 366

    @staticmethod
    def jalali_to_gregorian(jy, jm, jd):
        jy = int(jy) - 979
        jm = int(jm) - 1
        jd = int(jd) - 1

        jalali_day_no = 365 * jy + (jy // 33) * 8 + ((jy % 33) + 3) // 4
        for index in range(jm):
            jalali_day_no += 31 if index < 6 else 30
        jalali_day_no += jd

        gregorian_day_no = jalali_day_no + 79

        gy = 1600 + 400 * (gregorian_day_no // 146097)
        gregorian_day_no %= 146097

        leap = True
        if gregorian_day_no >= 36525:
            gregorian_day_no -= 1
            gy += 100 * (gregorian_day_no // 36524)
            gregorian_day_no %= 36524

            if gregorian_day_no >= 365:
                gregorian_day_no += 1
            else:
                leap = False

        gy += 4 * (gregorian_day_no // 1461)
        gregorian_day_no %= 1461

        if gregorian_day_no >= 366:
            leap = False
            gregorian_day_no -= 1
            gy += gregorian_day_no // 365
            gregorian_day_no %= 365

        gregorian_month_days = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0
        while gm < 12 and gregorian_day_no >= gregorian_month_days[gm]:
            gregorian_day_no -= gregorian_month_days[gm]
            gm += 1

        return date(gy, gm + 1, gregorian_day_no + 1)

    @staticmethod
    def to_persian_digits(value):
        translation = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
        return str(value).translate(translation)

    @staticmethod
    def _python_weekday(year, month, day):
        return JalaliCalendar.jalali_to_gregorian(year, month, day).weekday()

    @staticmethod
    def _ordered_weekdays(week_start):
        keys = ["sat", "sun", "mon", "tue", "wed", "thu", "fri"]
        if week_start == "sat":
            return keys

        start_index = keys.index(week_start)
        return keys[start_index:] + keys[:start_index]

    @staticmethod
    def _weekday_offset(python_weekday, week_start):
        start_weekday = PYTHON_WEEKDAY_BY_KEY[week_start]
        return (python_weekday - start_weekday) % 7

    @staticmethod
    def _shift_month(year, month, offset):
        month_index = (int(year) * 12) + (int(month) - 1) + int(offset)
        return month_index // 12, (month_index % 12) + 1
