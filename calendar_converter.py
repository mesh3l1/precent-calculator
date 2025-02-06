import customtkinter as ctk
from datetime import date
from hijri_converter import convert
from events import EventManager
import tkinter.messagebox as messagebox

class DateConverterApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("محول التقويم الهجري/الميلادي")
        self.root.geometry("390x844")  # حجم شاشة آيفون النموذجي
        
        # تهيئة مدير الأحداث
        self.event_manager = EventManager()
        
        # المتغيرات
        self.current_selected_date = None
        self.current_page = "gregorian"
        
        # إنشاء واجهة المستخدم
        self.setup_ui()
        
        # تحديث التقويم مباشرة
        self.refresh_calendar_display()

    def setup_ui(self):
        # الإطار الرئيسي
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # شريط التنقل
        nav_frame = ctk.CTkFrame(self.main_frame)
        nav_frame.pack(fill="x", padx=5, pady=(5, 10))
        
        # أزرار التنقل بين التقويمين
        button_font = ("Arial", 14)
        
        self.gregorian_btn = ctk.CTkButton(
            nav_frame,
            text="الميلادي",
            command=lambda: self.show_page("gregorian"),
            fg_color="#1f538d",
            hover_color="#006064",
            font=button_font,
            width=80,
            height=35
        )
        self.gregorian_btn.pack(side="left", padx=2)
        
        self.hijri_btn = ctk.CTkButton(
            nav_frame,
            text="الهجري",
            command=lambda: self.show_page("hijri"),
            fg_color="#2B2B2B",
            hover_color="#006064",
            font=button_font,
            width=80,
            height=35
        )
        self.hijri_btn.pack(side="left", padx=2)
        
        # أزرار الأحداث
        self.add_event_btn = ctk.CTkButton(
            nav_frame,
            text="➕",
            command=self.show_add_event_dialog,
            state="disabled",
            fg_color="#1f538d",
            hover_color="#006064",
            font=("Arial", 20),
            width=40,
            height=35
        )
        self.add_event_btn.pack(side="right", padx=2)
        
        self.delete_event_btn = ctk.CTkButton(
            nav_frame,
            text="🗑️",
            command=self.show_delete_event_dialog,
            state="disabled",
            fg_color="#1f538d",
            hover_color="#006064",
            font=("Arial", 16),
            width=40,
            height=35
        )
        self.delete_event_btn.pack(side="right", padx=2)

        # إنشاء الصفحات
        self.pages = {
            "gregorian": self.create_gregorian_page(),
            "hijri": self.create_hijri_page()
        }
        
        # عرض الصفحة الافتراضية
        self.show_page("gregorian")

    def create_gregorian_page(self):
        page = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # عنوان الصفحة والتاريخ
        self.gregorian_title = ctk.CTkLabel(
            page,
            text="التقويم الميلادي",
            font=("Arial", 20, "bold")
        )
        self.gregorian_title.pack(pady=(10, 5))
        
        # عرض التاريخ والحدث
        self.gregorian_date_label = ctk.CTkLabel(
            page,
            text="",
            font=("Arial", 14)
        )
        self.gregorian_date_label.pack(pady=(0, 10))
        
        # إنشاء التقويم
        self.gregorian_calendar = self.create_calendar(page, "gregorian")
        self.gregorian_calendar.pack(expand=True, fill="both", padx=10, pady=10)
        
        return page
    
    def create_hijri_page(self):
        page = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # عنوان الصفحة والتاريخ
        self.hijri_title = ctk.CTkLabel(
            page,
            text="التقويم الهجري",
            font=("Arial", 20, "bold")
        )
        self.hijri_title.pack(pady=(10, 5))
        
        # عرض التاريخ والحدث
        self.hijri_date_label = ctk.CTkLabel(
            page,
            text="",
            font=("Arial", 14)
        )
        self.hijri_date_label.pack(pady=(0, 10))
        
        # إنشاء التقويم
        self.hijri_calendar = self.create_calendar(page, "hijri")
        self.hijri_calendar.pack(expand=True, fill="both", padx=10, pady=10)
        
        return page

    def show_page(self, page_name):
        # إخفاء كل الصفحات
        for page in self.pages.values():
            page.pack_forget()
        
        # عرض الصفحة المطلوبة
        self.pages[page_name].pack(fill="both", expand=True)
        self.current_page = page_name
        
        # تحديث أزرار التنقل
        self.gregorian_btn.configure(
            fg_color="#1f538d" if page_name == "gregorian" else "#2B2B2B"
        )
        self.hijri_btn.configure(
            fg_color="#1f538d" if page_name == "hijri" else "#2B2B2B"
        )
        
        # تحديث التقويم
        self.refresh_calendar_display()

    def create_calendar(self, parent, calendar_type):
        calendar_frame = ctk.CTkFrame(parent)
        
        # أيام الأسبوع
        days = ["أحد", "إثن", "ثلا", "أرب", "خمي", "جمع", "سبت"]
        for i, day in enumerate(days):
            label = ctk.CTkLabel(
                calendar_frame,
                text=day,
                font=("Arial", 12, "bold"),
                width=40
            )
            label.grid(row=0, column=i, padx=2, pady=5)
        
        # إنشاء أزرار الأيام
        for week in range(6):
            for day in range(7):
                btn = ctk.CTkButton(
                    calendar_frame,
                    text="",
                    width=45,
                    height=45,
                    command=lambda d=(week*7 + day + 1): self.on_date_select(d, calendar_type),
                    fg_color="#2B2B2B",
                    hover_color="#1f538d",
                    font=("Arial", 14)
                )
                btn.grid(row=week+1, column=day, padx=1, pady=1)
                
                # حفظ معلومات الزر
                btn.calendar_type = calendar_type
                btn.day_number = week*7 + day + 1
        
        return calendar_frame

    def on_date_select(self, day, calendar_type):
        """معالجة حدث اختيار التاريخ"""
        self.current_page = calendar_type
        
        if calendar_type == "gregorian":
            today = date.today()
            self.current_selected_date = (today.year, today.month, day)
        else:
            hijri = convert.Gregorian(date.today().year, date.today().month, date.today().day).to_hijri()
            self.current_selected_date = (hijri.year, hijri.month, day)
        
        print(f"تم اختيار التاريخ: {self.current_selected_date} في التقويم {calendar_type}")
        
        # تحديث حالة الأزرار
        self.add_event_btn.configure(state="normal")
        self.delete_event_btn.configure(state="normal")
        
        # تحديث عنوان التاريخ والتقويم
        self.refresh_calendar_display()

    def show_add_event_dialog(self):
        """عرض نافذة إضافة حدث"""
        if not self.current_selected_date:
            messagebox.showwarning("تنبيه", "الرجاء اختيار تاريخ أولاً")
            return
        
        # إنشاء نافذة حوار مخصصة
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("إضافة حدث")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # عنوان التاريخ
        date_label = ctk.CTkLabel(
            dialog,
            text=f"التاريخ: {self.current_selected_date[2]}/{self.current_selected_date[1]}/{self.current_selected_date[0]}",
            font=("Arial", 14, "bold")
        )
        date_label.pack(pady=(20, 10))
        
        # حقل إدخال الحدث
        event_entry = ctk.CTkEntry(
            dialog,
            width=250,
            font=("Arial", 14),
            placeholder_text="أدخل الحدث هنا"
        )
        event_entry.pack(pady=10, padx=20)
        
        def add_event():
            event_text = event_entry.get().strip()
            if event_text:
                # إضافة الحدث
                self.event_manager.add_event(
                    self.current_page,
                    self.current_selected_date,
                    event_text
                )
                
                # تحديث التقويم مباشرة
                self.refresh_calendar_display()
                
                # إغلاق النافذة
                dialog.destroy()
        
        # زر الإضافة
        add_btn = ctk.CTkButton(
            dialog,
            text="إضافة",
            command=add_event,
            font=("Arial", 14),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        add_btn.pack(pady=10)
        
        # زر الإلغاء
        cancel_btn = ctk.CTkButton(
            dialog,
            text="إلغاء",
            command=dialog.destroy,
            font=("Arial", 14),
            fg_color="#FF5252",
            hover_color="#FF1744"
        )
        cancel_btn.pack(pady=5)
        
        # تركيز على حقل الإدخال
        event_entry.focus()
        
        # ربط مفتاح Enter مع زر الإضافة
        dialog.bind("<Return>", lambda e: add_event())

    def show_delete_event_dialog(self):
        if self.current_selected_date:
            events = self.event_manager.get_events(self.current_page, self.current_selected_date)
            if events:
                dialog = ctk.CTkToplevel(self.root)
                dialog.title("حذف حدث")
                dialog.geometry("350x500")
                dialog.transient(self.root)
                dialog.grab_set()
                
                # عنوان التاريخ
                date_label = ctk.CTkLabel(
                    dialog,
                    text=f"{self.current_selected_date[2]}/{self.current_selected_date[1]}/{self.current_selected_date[0]}",
                    font=("Arial", 16, "bold")
                )
                date_label.pack(pady=(20, 10))
                
                # قائمة الأحداث
                events_frame = ctk.CTkScrollableFrame(dialog, width=300, height=350)
                events_frame.pack(pady=5, padx=10, fill="both", expand=True)
                
                for event in events:
                    event_frame = ctk.CTkFrame(events_frame, fg_color="#2B2B2B")
                    event_frame.pack(fill="x", pady=3, padx=3)
                    
                    event_label = ctk.CTkLabel(
                        event_frame,
                        text=event,
                        font=("Arial", 14),
                        wraplength=200
                    )
                    event_label.pack(side="left", padx=8, pady=5)
                    
                    delete_btn = ctk.CTkButton(
                        event_frame,
                        text="🗑️",
                        width=30,
                        height=30,
                        command=lambda e=event: self.delete_event(e, dialog),
                        fg_color="#FF5252",
                        hover_color="#FF1744",
                        font=("Arial", 14)
                    )
                    delete_btn.pack(side="right", padx=5, pady=5)
                
                # زر إغلاق
                close_btn = ctk.CTkButton(
                    dialog,
                    text="إغلاق",
                    command=dialog.destroy,
                    width=100,
                    font=("Arial", 14)
                )
                close_btn.pack(pady=10)
            else:
                messagebox.showinfo("معلومات", "لا توجد أحداث في هذا التاريخ")
        else:
            messagebox.showwarning("تنبيه", "الرجاء اختيار تاريخ أولاً")

    def delete_event(self, event_text, dialog):
        """حذف الحدث وتحديث واجهة المستخدم"""
        if self.current_selected_date and event_text:
            # حذف الحدث
            self.event_manager.delete_event(
                self.current_page,
                self.current_selected_date,
                event_text
            )
            
            # تحديث عنوان التاريخ
            self.update_date_label()
            
            # تحديث كلا التقويمين
            for page_name, page in self.pages.items():
                calendar_frame = [child for child in page.winfo_children() if isinstance(child, ctk.CTkFrame)][0]
                self.update_calendar_display(calendar_frame, page_name)
            
            # إغلاق نافذة الحذف
            if dialog:
                dialog.destroy()

    def update_date_label(self):
        """تحديث عنوان التاريخ والحدث"""
        if self.current_selected_date:
            year, month, day = self.current_selected_date
            
            if self.current_page == "gregorian":
                # تحويل التاريخ الميلادي إلى هجري
                hijri_date = convert.Gregorian(year, month, day).to_hijri()
                gregorian_text = f"{day}/{month}/{year}"
                hijri_text = f"{hijri_date.day}/{hijri_date.month}/{hijri_date.year}"
            else:
                # تحويل التاريخ الهجري إلى ميلادي
                gregorian_date = convert.Hijri(year, month, day).to_gregorian()
                gregorian_text = f"{gregorian_date.day}/{gregorian_date.month}/{gregorian_date.year}"
                hijri_text = f"{day}/{month}/{year}"
            
            # عرض التاريخين
            date_text = f"التاريخ الميلادي: {gregorian_text}\nالتاريخ الهجري: {hijri_text}"
            
            # عرض الأحداث
            events = self.event_manager.get_events(self.current_page, self.current_selected_date)
            if events:
                date_text += "\n\nالأحداث:\n" + "\n".join([f"📅 {event}" for event in events])
            
            # تحديث النص في كلا التقويمين
            for page_name, page in self.pages.items():
                date_label = page.winfo_children()[0]  # الليبل الأول في الصفحة
                date_label.configure(text=date_text)

    def update_calendar_display(self, calendar_frame, calendar_type):
        """تحديث عرض التقويم"""
        days_in_month = self.get_days_in_month(calendar_type)
        buttons = [child for child in calendar_frame.winfo_children() if isinstance(child, ctk.CTkButton)]
        
        # الحصول على تاريخ اليوم
        today = date.today()
        if calendar_type == "hijri":
            today_hijri = convert.Gregorian(today.year, today.month, today.day).to_hijri()
            today_date = (today_hijri.year, today_hijri.month, today_hijri.day)
        else:
            today_date = (today.year, today.month, today.day)
        
        for btn in buttons:
            day_num = getattr(btn, 'day_number', 0)
            if day_num <= days_in_month:
                date_tuple = self.get_date_tuple(day_num, calendar_type)
                has_events = bool(self.event_manager.get_events(calendar_type, date_tuple))
                
                # تحديد نص الزر
                btn_text = str(day_num)
                if has_events:
                    btn_text += " 📅"
                btn.configure(text=btn_text)
                
                # تحديد اليوم المحدد حالياً
                is_selected = (self.current_selected_date and 
                             self.current_selected_date[0] == date_tuple[0] and
                             self.current_selected_date[1] == date_tuple[1] and
                             self.current_selected_date[2] == day_num and
                             self.current_page == calendar_type)
                
                # تحديد ما إذا كان هذا اليوم هو تاريخ اليوم
                is_today = (date_tuple[0] == today_date[0] and 
                          date_tuple[1] == today_date[1] and 
                          day_num == today_date[2])
                
                # تحديث لون الزر
                if is_selected:
                    btn.configure(fg_color="#1f538d", hover_color="#006064")
                elif is_today:
                    btn.configure(fg_color="#006064", hover_color="#1f538d")
                elif has_events:
                    btn.configure(fg_color="#4CAF50", hover_color="#1f538d")
                else:
                    btn.configure(fg_color="#2B2B2B", hover_color="#1f538d")
                
                btn.configure(state="normal")
            else:
                btn.configure(text="", state="disabled", fg_color="#1E1E1E", hover_color="#1E1E1E")

    def get_date_tuple(self, day, calendar_type):
        """الحصول على التاريخ كمجموعة"""
        today = date.today()
        if calendar_type == "gregorian":
            return (today.year, today.month, day)
        else:
            hijri = convert.Gregorian(today.year, today.month, today.day).to_hijri()
            return (hijri.year, hijri.month, day)

    def get_days_in_month(self, calendar_type):
        """الحصول على عدد أيام الشهر"""
        today = date.today()
        if calendar_type == "gregorian":
            if today.month == 12:
                next_month = date(today.year + 1, 1, 1)
            else:
                next_month = date(today.year, today.month + 1, 1)
            return (next_month - date(today.year, today.month, 1)).days
        else:
            # تقريباً للشهور الهجرية
            return 30

    def refresh_calendar_display(self):
        """تحديث عرض التقويم والعنوان"""
        # تحديث عنوان التاريخ
        self.update_date_label()
        
        # تحديث كلا التقويمين
        for page_name, page in self.pages.items():
            calendar_frame = [child for child in page.winfo_children() if isinstance(child, ctk.CTkFrame)][0]
            self.update_calendar_display(calendar_frame, page_name)
            
        # تحديث الواجهة
        self.root.update()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DateConverterApp()
    app.run()
