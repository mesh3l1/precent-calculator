import json
from datetime import date
from hijri_converter import convert

class EventManager:
    def __init__(self):
        self.events = {"gregorian": {}, "hijri": {}}
        self.load_events()
    
    def load_events(self):
        try:
            with open("events.json", "r", encoding="utf-8") as f:
                self.events = json.load(f)
        except FileNotFoundError:
            self.events = {"gregorian": {}, "hijri": {}}
            self.save_events()
    
    def save_events(self):
        with open("events.json", "w", encoding="utf-8") as f:
            json.dump(self.events, f, ensure_ascii=False, indent=4)
    
    def make_date_key(self, year, month, day):
        """تحويل التاريخ إلى مفتاح للتخزين"""
        return f"{year}-{month}-{day}"
    
    def convert_gregorian_to_hijri(self, year, month, day):
        """تحويل من ميلادي إلى هجري"""
        try:
            hijri = convert.Gregorian(year, month, day).to_hijri()
            return (hijri.year, hijri.month, hijri.day)
        except Exception as e:
            print(f"خطأ في التحويل من ميلادي إلى هجري: {e}")
            return None
    
    def convert_hijri_to_gregorian(self, year, month, day):
        """تحويل من هجري إلى ميلادي"""
        try:
            greg = convert.Hijri(year, month, day).to_gregorian()
            return (greg.year, greg.month, greg.day)
        except Exception as e:
            print(f"خطأ في التحويل من هجري إلى ميلادي: {e}")
            return None
    
    def add_event(self, calendar_type, date_tuple, event_text):
        """إضافة حدث جديد"""
        year, month, day = date_tuple
        
        # إضافة الحدث في التقويم الأصلي
        original_key = self.make_date_key(year, month, day)
        if original_key not in self.events[calendar_type]:
            self.events[calendar_type][original_key] = []
        self.events[calendar_type][original_key].append(event_text)
        
        # تحويل التاريخ وإضافة الحدث في التقويم الآخر
        if calendar_type == "gregorian":
            hijri_date = self.convert_gregorian_to_hijri(year, month, day)
            if hijri_date:
                hijri_key = self.make_date_key(*hijri_date)
                if hijri_key not in self.events["hijri"]:
                    self.events["hijri"][hijri_key] = []
                self.events["hijri"][hijri_key].append(event_text)
        else:  # calendar_type == "hijri"
            greg_date = self.convert_hijri_to_gregorian(year, month, day)
            if greg_date:
                greg_key = self.make_date_key(*greg_date)
                if greg_key not in self.events["gregorian"]:
                    self.events["gregorian"][greg_key] = []
                self.events["gregorian"][greg_key].append(event_text)
        
        self.save_events()
        print(f"تم إضافة الحدث: {event_text}")
        print(f"في التقويم {calendar_type}: {original_key}")
    
    def delete_event(self, calendar_type, date_tuple, event_text):
        """حذف حدث محدد"""
        year, month, day = date_tuple
        original_key = self.make_date_key(year, month, day)
        
        # حذف من التقويم الأصلي
        if original_key in self.events[calendar_type]:
            if event_text in self.events[calendar_type][original_key]:
                self.events[calendar_type][original_key].remove(event_text)
                if not self.events[calendar_type][original_key]:
                    del self.events[calendar_type][original_key]
        
        # حذف من التقويم الآخر
        if calendar_type == "gregorian":
            hijri_date = self.convert_gregorian_to_hijri(year, month, day)
            if hijri_date:
                hijri_key = self.make_date_key(*hijri_date)
                if hijri_key in self.events["hijri"]:
                    if event_text in self.events["hijri"][hijri_key]:
                        self.events["hijri"][hijri_key].remove(event_text)
                        if not self.events["hijri"][hijri_key]:
                            del self.events["hijri"][hijri_key]
        else:
            greg_date = self.convert_hijri_to_gregorian(year, month, day)
            if greg_date:
                greg_key = self.make_date_key(*greg_date)
                if greg_key in self.events["gregorian"]:
                    if event_text in self.events["gregorian"][greg_key]:
                        self.events["gregorian"][greg_key].remove(event_text)
                        if not self.events["gregorian"][greg_key]:
                            del self.events["gregorian"][greg_key]
        
        # حفظ التغييرات
        self.save_events()
    
    def get_events(self, calendar_type, date_tuple):
        """الحصول على الأحداث لتاريخ معين"""
        year, month, day = date_tuple
        date_key = self.make_date_key(year, month, day)
        return self.events[calendar_type].get(date_key, [])
