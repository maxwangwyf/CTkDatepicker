import customtkinter as ctk
import calendar
import tkinter as tk
from datetime import datetime
month_map = {
        "January": "一月",
        "February": "二月",
        "March": "三月",
        "April": "四月",
        "May": "五月",
        "June": "六月",
        "July": "七月",
        "August": "八月",
        "September": "九月",
        "October": "十月",
        "November": "十一月",
        "December": "十二月"
    }
class CTkCalendar(ctk.CTkFrame):
    """
    Calendar widget to display certain month, each day is rendered as Label.
    """
    def __init__(self, master,
                 width=250,
                 height=250,
                 fg_color=None,
                 text_color=None,
                 font=None,
                 corner_radius=None,
                 hover_color=None,
                 hover=True,
                 select_color=None,
                 command=None,
                 header_color=None,
                 header_text_color=None,
                 **kwargs):

        super().__init__(master=master,
                         width=width,
                         height=height, **kwargs)

        self.text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else text_color
        self.fg_color = self.cget("fg_color") if fg_color is None else fg_color
        if not font:
            self.font = ctk.CTkFont(ctk.ThemeManager.theme["CTkFont"]["family"],ctk.ThemeManager.theme["CTkFont"]["size"])
        else:
            if isinstance(font, ctk.CTkFont):
                self.font = font
            else:
                self.font = ctk.CTkFont(*font)
        self.hover_color = ctk.ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else hover_color
        self.hover = hover
        self.corner_radius = super().cget("corner_radius") if corner_radius is None else corner_radius
        self.select_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"] if select_color is None else select_color
        self.header_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"] if header_color is None else header_color
        self.header_text_color = ctk.ThemeManager.theme["CTkButton"]["text_color"] if header_text_color is None else header_text_color
        
        self.today = self.current_date()
        self.day, self.month, self.year = self.today[:]
        self.month_label = ctk.StringVar(value=month_map[calendar.month_name[self.month]])
        self.year_label = ctk.IntVar(value=self.year)
        self.labels = {}
        self.command = command
        self.markings = {}
        # creating header and calendar frames
        self.setup_header_frame()
        self.create_calendar_frame()

    def _set_scaling(self, *args, **kwargs):
        super()._set_scaling(*args, **kwargs)
        self.create_calendar_frame()

    def _set_appearance_mode(self, mode_string):
        super()._set_appearance_mode(mode_string)
        self.create_calendar_frame()
        
    # setting up the header frame
    def setup_header_frame(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=self.header_color, corner_radius=self.corner_radius,
                                         border_width=0)

        self.left = ctk.CTkButton(self.header_frame, text="◀", width=25, fg_color="transparent", 
                      hover=False, font=self.font, text_color=self.header_text_color,
                      command=lambda: self.change_month(-1))
        self.left.pack(side="left", padx=10)
        self.display_month = ctk.CTkLabel(self.header_frame, textvariable=self.month_label, font=self.font, text_color=self.header_text_color,
                         fg_color="transparent")
        self.display_month.pack(side="left", fill="x", expand=True)
        self.display_year = ctk.CTkLabel(self.header_frame, textvariable=self.year_label, font=self.font, text_color=self.header_text_color,
                         fg_color="transparent")
        self.display_year.pack(side="left", fill="x")
        self.right = ctk.CTkButton(self.header_frame, text="▶", width=25, fg_color="transparent",
                      hover=False, font=self.font, text_color=self.header_text_color,
                      command=lambda: self.change_month(1))
        self.right.pack(side="right", padx=10)

        self.header_frame.place(relx=0.5, rely=0.02, anchor="n", relheight=0.18, relwidth=0.95)
        self.calendar_frame = ctk.CTkFrame(self, fg_color=self.fg_color,
                                           corner_radius=self.corner_radius, border_width=0)
        
    def create_calendar_frame(self):
        # "updating" frames
        for i in self.labels:
            self.labels[i].destroy()
        self.labels = {}
    
        current_month = calendar.monthcalendar(self.year, self.month)

        # grid
        self.calendar_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="b")
        self.calendar_frame.place(relx=0.5, rely=0.96, anchor="s", relheight=0.75, relwidth=0.95)
        rows = tuple([i for i in range(len(current_month)+1)])
    
        
        self.calendar_frame.rowconfigure(rows, weight=1)
        
        weeks = ["一", "二", "三", "四", "五", "六", "日"]
        # labels for days
        label_num = 0 
        for row in range(len(current_month)):
            
            for column in range(7):
                label_num +=1
                if column==6:
                    fg = "red"
                else:
                    fg = self._apply_appearance_mode(self.text_color)
                self.labels[label_num] = tk.Label(self.calendar_frame, text=weeks[column], 
                                             bg=self._apply_appearance_mode(self.fg_color), font=self.font,
                                             fg=fg)
                self.labels[label_num].grid(row=0, column=column, sticky="nsew")
                
            for column in range(7):
                label_num +=1
                if current_month[row][column] != 0:
 
                    if self.year == self.today[2] and self.month == self.today[1] \
                            and current_month[row][column] == self.today[0]:
                        self.labels[label_num] = tk.Label(self.calendar_frame, text=str(current_month[row][column]), 
                                             bg=self._apply_appearance_mode(self.select_color), font=self.font,
                                             fg=self._apply_appearance_mode(self.text_color))
                    else:
                        self.labels[label_num] = tk.Label(self.calendar_frame, text=str(current_month[row][column]), 
                                             bg=self._apply_appearance_mode(self.fg_color), font=self.font,
                                             fg=self._apply_appearance_mode(self.text_color))
                    if (current_month[row][column], self.month, self.year) in list(self.markings.keys()):
                        self.labels[label_num].config(bg=self._apply_appearance_mode(self.markings[(current_month[row][column], self.month, self.year)]))
                    if self.hover:
                        self.labels[label_num].bind("<Enter>", lambda e, label = self.labels[label_num]: label.config(bg=self._apply_appearance_mode(self.hover_color)))
                        self.labels[label_num].bind("<Leave>", lambda e, label = self.labels[label_num], bg=self.labels[label_num].cget("bg"): label.config(bg=self._apply_appearance_mode(bg)))
                    if self.command:
                        self.labels[label_num].bind("<1>", lambda e, row=row, column=column: self.command((current_month[row][column], self.month, self.year)), add="+")
                    self.labels[label_num].grid(row=row+1, column=column, sticky="nsew")

    def change_month(self, amount):
        self.month += amount
        if self.month < 1:
            self.year -= 1
            self.month = 12
            self.day = 1
        elif self.month > 12:
            self.year += 1
            self.month = 1
            self.day = 1
        
        eng_month = calendar.month_name[self.month]
        self.month_label.set(month_map[eng_month])
        
        self.year_label.set(self.year)

        self.create_calendar_frame()

    def current_date(self):
        date = str(datetime.now()).split()
        year, month, day = date[0].split("-")
        return int(day), int(month), int(year)
    
    def mark(self, date, color=None):
        if color is not None:
            self.markings.update({date: color})
        else:
            if date in list(self.markings.keys()):
                del self.markings[date]
        self.create_calendar_frame()

    def set(self, date):
        self.day = date[0]
        self.month = date[1]
        self.year = date[2]
        self.month_label.set(calendar.month_name[self.month])
        self.year_label.set(self.year)
        self.create_calendar_frame()
        if self.command:
            self.command(date)
            
    def select(self, date):
        self.day = date[0]
        self.month = date[1]
        self.year = date[2]
        self.month_label.set(calendar.month_name[self.month])
        self.year_label.set(self.year)
        self.mark(date, color=self.select_color)
        self.create_calendar_frame()
                  
    def configure(self, **kwargs):
        if "corner_radius" in kwargs:
            self.corner_radius = kwargs["corner_radius"]
            self.header_frame.configure(corner_radius=self.corner_radius)
            self.calendar_frame.configure(corner_radius=self.corner_radius)
            
        if "text_color" in kwargs:
            self.text_color = kwargs.pop("text_color")
        if "header_color" in kwargs:
            self.header_color = kwargs.pop("header_color")
            self.header_frame.configure(fg_color=self.header_color)
        if "font" in kwargs:
            self.font = kwargs.pop("font")
            self.display_month.configure(font=self.font)
            self.display_year.configure(font=self.font)
            self.left.configure(font=self.font)
            self.right.configure(font=self.font)
        if "header_text_color" in kwargs:
            self.header_text_color = kwargs.pop("header_text_color")
            self.display_month.configure(text_color=self.header_text_color)
            self.display_year.configure(text_color=self.header_text_color)
            self.left.configure(text_color=self.header_text_color)
            self.right.configure(text_color=self.header_text_color)
        if "select_color" in kwargs:
            self.select_color = kwargs.pop("select_color")
        if "hover_color" in kwargs:
            self.hover_color = kwargs.pop("hover_color")
        if "hover" in kwargs:
            self.hover = kwargs.pop("hover")
            
        super().configure(**kwargs)
        self.create_calendar_frame()
        
    def cget(self, param):
        if param=="text_color":
            return self.text_color
        if param=="header_color":
            return self.header_color
        if param=="header_text_color":
            return self.header_text_color
        if param=="font":
            return self.font
        if param=="hover_color":
            return self.hover_color
        if param=="select_color":
            return self.select_color
        if param=="hover":
            return self.hover
        return super().cget(param)

    def bind(self, sequence=None, command=None, add="+"):
        super().bind(sequence, command, add)
        self.header_frame.bind(sequence, command, add)
        self.calendar_frame.bind(sequence, command, add)
        self.display_month.bind(sequence, command, add)
        self.display_year.bind(sequence, command, add)
        self.left.bind(sequence, command, add)
        self.right.bind(sequence, command, add)
        
    def unbind(self, sequence=None):
        super().unbind(sequence)
        self.header_frame_canvas.unbind(sequence)
        self.calendar_frame.unbind(sequence)
        self.display_month.unbind(sequence)
        self.display_year.unbind(sequence)
        self.left.unbind(sequence)
        self.right.unbind(sequence)
        
