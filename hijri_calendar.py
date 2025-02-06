import customtkinter as ctk
from datetime import date
from hijri_converter import convert

class HijriCalendar(ctk.CTkFrame):
    def __init__(self, master, event_manager=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.selected_date = None
        self.callback = None
        self.event_manager = event_manager
        
        # تحويل التاريخ الحالي إلى هجري
        today = date.today()
        hijri_date = convert.Gregorian(today.year, today.month, today.day).to_hijri()
        self.current_year = hijri_date.year
        self.current_month = hijri_date.month
        
        self.create_calendar_widgets()
        self.update_calendar()
    
    def create_calendar_widgets(self):
        # إطار التنقل
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 10))
        
        # أزرار التنقل
        prev_btn = ctk.CTkButton(
            nav_frame,
            text="<",
            width=30,
            command=self.prev_month,
            fg_color="#1f538d",
            hover_color="#006064"
        )
        prev_btn.pack(side="left", padx=5)
        
        self.month_label = ctk.CTkLabel(
            nav_frame,
            text="",
            font=("Arial", 14)
        )
        self.month_label.pack(side="left", expand=True)
        
        next_btn = ctk.CTkButton(
            nav_frame,
            text=">",
            width=30,
            command=self.next_month,
            fg_color="#1f538d",
            hover_color="#006064"
        )
        next_btn.pack(side="right", padx=5)
        
        # أيام الأسبوع
        days_frame = ctk.CTkFrame(self, fg_color="transparent")
        days_frame.pack(fill="x", pady=(0, 10))
        
        days = ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
        for day in days:
            label = ctk.CTkLabel(
                days_frame,
                text=day,
                font=("Arial", 12),
                width=40
            )
            label.pack(side="right", padx=2)
        
        # إطار أيام الشهر
        self.days_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.days_frame.pack(fill="both", expand=True)
    
    def update_calendar(self):
        # تحديث عنوان الشهر
        self.month_label.configure(text=f"{self.current_month}/{self.current_year}")
        
        # مسح الأيام السابقة
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        # حساب عدد أيام الشهر الهجري
        if self.current_month in [1, 3, 5, 7, 9, 11]:
            days_in_month = 30
        elif self.current_month == 12:
            # ذو الحجة يمكن أن يكون 29 أو 30 يوماً
            days_in_month = 30 if self.is_long_dhulhijjah() else 29
        else:
            days_in_month = 29
        
        # حساب يوم بداية الشهر
        first_day_greg = convert.Hijri(self.current_year, self.current_month, 1).to_gregorian()
        weekday = first_day_greg.weekday()
        
        # إضافة الأيام الفارغة
        for i in range(weekday + 1):
            empty = ctk.CTkLabel(self.days_frame, text="", width=40)
            empty.grid(row=0, column=6-i)
        
        # إضافة أيام الشهر
        day = 1
        row = 0
        col = 6 - weekday
        
        # تحويل التاريخ الحالي إلى هجري للمقارنة
        today = date.today()
        current_hijri = convert.Gregorian(today.year, today.month, today.day).to_hijri()
        
        while day <= days_in_month:
            is_today = (day == current_hijri.day and 
                       self.current_month == current_hijri.month and 
                       self.current_year == current_hijri.year)
            
            # التحقق من وجود أحداث
            has_events = False
            if self.event_manager:
                date_key = (self.current_year, self.current_month, day)
                has_events = bool(self.event_manager.get_events("hijri", date_key))
            
            frame = ctk.CTkFrame(self.days_frame, fg_color="transparent", width=40, height=40)
            frame.grid(row=row, column=col, padx=2, pady=2)
            frame.grid_propagate(False)
            
            btn = ctk.CTkButton(
                frame,
                text=str(day),
                width=40,
                height=30,
                fg_color="#1f538d" if is_today else "#2B2B2B",
                hover_color="#006064",
                command=lambda d=day: self.select_date(d)
            )
            btn.place(relx=0.5, rely=0.5, anchor="center")
            
            if has_events:
                event_marker = ctk.CTkLabel(
                    frame,
                    text="📅",  
                    text_color="#4CAF50",  
                    font=("Arial", 12)
                )
                event_marker.place(relx=0.5, rely=0.85, anchor="center")
            
            day += 1
            col -= 1
            if col < 0:
                col = 6
                row += 1
    
    def is_long_dhulhijjah(self):
        # تقريب بسيط لتحديد ما إذا كان شهر ذو الحجة 30 يوماً
        next_month = convert.Hijri(self.current_year + 1 if self.current_month == 12 else self.current_year,
                                 1 if self.current_month == 12 else self.current_month + 1,
                                 1).to_gregorian()
        current_month = convert.Hijri(self.current_year, self.current_month, 1).to_gregorian()
        days_between = (next_month - current_month).days
        return days_between == 30
    
    def select_date(self, day):
        self.selected_date = (self.current_year, self.current_month, day)
        if self.callback:
            self.callback(self.selected_date)
            
            # تحديث لون الزر المحدد
            for widget in self.days_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    btn = next((child for child in widget.winfo_children() 
                              if isinstance(child, ctk.CTkButton)), None)
                    if btn and btn.cget("text") == str(day):
                        btn.configure(fg_color="#1f538d")
                    elif btn:
                        btn.configure(fg_color="#2B2B2B")
    
    def bind_selection(self, callback):
        self.callback = callback
    
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()
    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()
