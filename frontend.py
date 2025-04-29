# TKINTER #
import os
from random import randint
import matplotlib.pyplot as plt
from tkinter import *
from tkcalendar import Calendar
import tkinter.messagebox
import datetime as dt
import backend

win_size = "750x500"
username = username_chk = user_name = None
passcode = passcode_chk = pwd = cal = None
login_window = register_window = search_window = None
entry_type_menu = entries = None
pass_show = True
count = flag = optionmenu = calflag = 0

root = Tk()
root.title("Personal Diary Application")
root.geometry(win_size)
root.configure(bg='aquamarine3')

with open("file_list.txt", 'r+') as check:
    match = check.readlines()
    for entry in match:
        entry = entry.strip('\n')
        if not os.path.exists(f"file/{entry}"):
            match.remove(entry + '\n')

with open('file_list.txt', 'w') as check:
    check.writelines(match)


class Error(Exception):
    pass


def login_win():
    global username_chk, passcode_chk, login_window

    def checkbtn():
        global pass_show
        if pass_show:
            passcode_chk.config(show='')
            pass_show = False
        else:
            passcode_chk.config(show='*')
            pass_show = True

    login_window = Toplevel()
    login_window.title("LOGIN")
    login_window.geometry(win_size)
    data_frame = Frame(login_window)
    user = Label(data_frame, text='Enter Username', font=('Comic Sans MS', 15))
    username_chk = Entry(data_frame, justify='center', width=50)
    password = Label(data_frame, text='Enter password', font=('Comic Sans MS', 15))
    passcode_chk = Entry(data_frame, justify='center', width=50, show='*')
    show_pass = Checkbutton(login_window, text='Show password', font=('Comic Sans MS', 15),
                            relief='raised', bg='aquamarine3', border='2.0',
                            command=checkbtn)  # , borderwidth='10.0')
    submit = Button(login_window, text='LOGIN', font=('Comic Sans Ms', 15, 'bold'),
                    background='aquamarine3', command=check)
    reset = Button(login_window, text='RESET PASSWORD', font=('Comic Sans Ms', 15, 'bold'),
                   background='aquamarine3', command=reset_pass)
    back = Button(login_window, text='BACK', font=('Comic Sans Ms', 15, 'bold'),
                   background='aquamarine3', command=lambda: login_window.destroy())

    data_frame.place(relx=0.5, rely=0.25, anchor='center')
    user.pack()
    username_chk.pack(pady=20, fill='x')
    password.pack()
    passcode_chk.pack(pady=20, fill='x')
    show_pass.place(relx=0.38, rely=0.43)
    submit.place(relx=0.44, rely=0.55)
    reset.place(relx=0.28, rely=0.75)
    back.place(relx=0.60, rely=0.75)

    login_window.mainloop()


def check():
    global count, login_window
    try:
        username_chk.get()
        passcode_chk.get()
        raise Error("")
    except Error:
        pass

    with open("login.csv", "r") as f:
        reader = csv.reader(f)
        for i in reader:
            if username_chk.get() and passcode_chk.get():
                if username_chk.get() == i[0] and passcode_chk.get() == i[1]:
                    login_window.destroy()
                    menu()
                    break
                else:
                    pass

        else:
            count += 1
            if count == 3:
                tkinter.messagebox.showerror('Invalid details', 'ACCESS DENIED')  # Invalid details 3 times
                login_window.destroy()
                return
            tkinter.messagebox.showwarning('Invalid details', 'Invalid username or password entered')
            username_chk.delete(0, END)
            passcode_chk.delete(0, END)
            login_window.destroy()


def reset_pass():
    global flag
    flag = 1
    register_win()


def menu():
    menu_win = Tk()
    menu_win.title("MENU")
    menu_win.geometry(win_size)
    menu_win.configure(bg='lightsalmon')

    top_frame = Frame(menu_win)
    bottom_frame = Frame(menu_win)
    add_btn = Button(top_frame, text='NEW ENTRY', font=('Comic Sans Ms', 20, 'bold'),
                     background='aquamarine3', command=type_entry)
    edit_btn = Button(top_frame, text='EXISTING ENTRIES', font=('Comic Sans Ms', 20, 'bold'),
                      background='aquamarine3', command=edit_entry)
    search_btn = Button(bottom_frame, text='SEARCH ENTRY', font=('Comic Sans Ms', 20, 'bold'),
                        background='aquamarine3', command=search)
    summary_btn = Button(bottom_frame, text='SUMMARY OF DIARY', font=('Comic Sans Ms', 20, 'bold'),
                         background='aquamarine3', command=sum_win)
    back = Button(menu_win, text='BACK', font=('Comic Sans Ms', 20, 'bold'),
                  background='linen', command=lambda: menu_win.destroy())

    top_frame.place(relx=0.5, rely=0.25, anchor='center')
    add_btn.pack(side='left', padx=10, pady=10)
    edit_btn.pack(side='left', padx=10, pady=10)
    bottom_frame.place(relx=0.5, rely=0.5, anchor='center')
    search_btn.pack(side='left', padx=10, pady=10)
    summary_btn.pack(padx=10, pady=10)
    back.place(relx=0.405, rely=0.7)

    menu_win.mainloop()


def type_entry():
    type_entry_win = Tk()
    type_entry_win.title("ENTRY TYPE")
    type_entry_win.geometry(win_size)
    type_entry_win.configure(bg='lightsalmon')

    reflect_btn = Button(type_entry_win, text='DAILY REFLECTION', font=('Comic Sans Ms', 20, 'bold'),
                         background='linen', command=lambda: daily_reflect('', None))
    event_btn = Button(type_entry_win, text='EVENT NOTE', font=('Comic Sans Ms', 20, 'bold'),
                       background='linen', command=event_note)
    mood_log_btn = Button(type_entry_win, text='MOOD LOG', font=('Comic Sans Ms', 20, 'bold'),
                          background='linen', command=mood_log)
    back = Button(type_entry_win, text='BACK', font=('Comic Sans Ms', 20, 'bold'),
                  background='aquamarine3', command=lambda: type_entry_win.destroy())

    reflect_btn.place(relx=0.51, rely=0.25, anchor='center')
    event_btn.place(relx=0.334, rely=0.45, anchor='center')
    mood_log_btn.place(relx=0.7, rely=0.45, anchor='center')
    back.place(relx=0.45, rely=0.7)

    type_entry_win.mainloop()


def daily_reflect(flag_file=None, file=None):
    global bookmark

    def save():
        filename = file_name_fixed.get() + file_name.get()
        content = content_inp.get('1.0', END)
        entry = backend.DiaryEntry(date=dt.date.today().isoformat(), content=content, filename=filename)
        diary_mng = backend.DiaryManager(date=dt.date.today().isoformat(), content=content)
        diary_mng.add_entry(entry=entry)
        tkinter.messagebox.showinfo(message='You have 10 seconds to bookmark this file!!')
        bookmark_btn.place(relx=0.8, rely=0.08)
        clk.place(relx=0.87, rely=0.08)
        timer(10)

    def clear():
        file_name.delete(0, END)
        content_inp.delete('1.0', END)
        bookmark_btn.destroy()
        clk.destroy()

    def book():
        with open("bookmark_list.txt", 'a') as b_mark:
            filename = file_name_fixed.get() + file_name.get()
            b_mark.write(f"{filename}\n")

    def timer(i):
        clk.config(text=f"{i}")
        if i-1==-1:
            clear()
            return
        clk.after(1000, lambda: timer(i-1))

    reflect_win = Toplevel()
    reflect_win.title("DAILY REFLECTION")
    reflect_win.geometry(win_size)
    reflect_win.configure(bg='lightskyblue')

    today = dt.datetime.date(dt.datetime.today()).isoformat()
    datelabel = Label(reflect_win, text=f"{today}", font=('Comic Sans MS', 15))
    bookmark_btn = Button(reflect_win, image=bookmark, font=('Comic Sans MS', 20), background='Yellow',
                      command=book)
    clk = Label(reflect_win, font=('Comic Sans MS', 20))
    file_label = Label(reflect_win, text='ENTER FILENAME', font=('Comic Sans MS', 15))
    file_name_fixed = Entry(reflect_win, font=('Comic Sans MS', 14),
                            justify='left', width=32)  # , state='readonly')
    file_name = Entry(reflect_win, font=('Comic Sans MS', 14), justify='left', width=25)
    file_name_fixed.insert(0, today + " - DailyReflection - ")
    content_label = Label(reflect_win, text='ENTER CONTENT', font=('Comic Sans MS', 15))
    content_inp = Text(reflect_win, font=('Comic Sans MS', 15), width=50, height=5)
    save_btn = Button(reflect_win, text='SAVE', font=('Comic Sans MS', 20), background='gray85',
                      command=save)
    back = Button(reflect_win, text='BACK', font=('Comic Sans Ms', 20),
                  background='gray85', command=lambda: reflect_win.destroy())

    datelabel.pack(pady=10)
    file_label.pack(pady=10)
    file_name_fixed.place(relx=0.12, rely=0.23)
    file_name.place(relx=0.51, rely=0.23)
    content_label.pack(pady=50)
    content_inp.pack()
    save_btn.place(relx=0.3, rely=0.8)
    back.place(relx=0.6, rely=0.8)

    if flag_file == 'editfile':
        file = file.strip('\n')
        file1 = ''.join(file.split()[4:])
        file_name.insert(0, file1)
        with open(f"file/{file}", 'r+') as f:
            data = f.readlines()
            content_inp.insert('1.0', data[2].strip('\n'))

    elif flag_file == 'file':
        file = file.strip('\n')
        file1 = ''.join(file.split()[4:])
        file_name.insert(0, file1)
        with open(f"file/{file}", 'r+') as f:
            data = f.readlines()
            content_inp.insert('1.0', data[2].strip('\n'))
        file_label.destroy()
        content_label.destroy()
        content_inp.place(relx=0.1, rely=0.4)
        save_btn.destroy()
        back.place(relx=0.43, rely=0.77)

    reflect_win.mainloop()


def event_note(flag_file=None, file=None):
    global bookmark

    event_win = Toplevel()
    event_win.title("EVENT NOTE")
    event_win.geometry(win_size)
    event_win.configure(bg='mediumpurple')

    def save():
        filename = file_name_fixed.get() + file_name.get()
        content = content_inp.get('1.0', END)
        entry = backend.DiaryEntry(date=dt.date.today().isoformat(), content=content, filename=filename)
        diary_mng = backend.DiaryManager(date=dt.date.today().isoformat(), content=content)
        diary_mng.add_entry(entry=entry)
        tkinter.messagebox.showinfo(message='You have 10 seconds to bookmark this file!!')
        bookmark_btn.place(relx=0.8, rely=0.08)
        clk.place(relx=0.87, rely=0.08)
        event_win.after(10000, clear)
        timer(10)

    def clear():
        file_name.delete(0, END)
        content_inp.delete('1.0', END)
        bookmark_btn.destroy()
        clk.destroy()

    def book():
        with open("bookmark_list.txt", 'a') as b_mark:
            filename = file_name_fixed.get() + file_name.get()
            b_mark.write(f"{filename}\n")

    def timer(i):
        clk.config(text=f"{i}")
        if i-1==-1:
            clear()
            return
        clk.after(1000, lambda: timer(i-1))


    today = dt.datetime.date(dt.datetime.today()).isoformat()
    datelabel = Label(event_win, text=f"{today}", font=('Comic Sans MS', 15))
    clk = Label(event_win, font=('Comic Sans MS', 20))
    file_label = Label(event_win, text='ENTER FILENAME', font=('Comic Sans MS', 15)) 
    file_name_fixed = Entry(event_win, font=('Comic Sans MS', 14),justify='left', width=32)  # , state='readonly')
    file_name = Entry(event_win, font=('Comic Sans MS', 14), justify='left', width=25)
    file_name_fixed.insert(0, today + " - EventNote - ")
    content_label = Label(event_win, text='EVENT LOCATION AND DETAILS', font=('Comic Sans MS', 15))
    content_inp = Text(event_win, font=('Comic Sans MS', 15), width=50, height=5)
    save_btn = Button(event_win, text='SAVE', font=('Comic Sans MS', 20, 'bold'), background='gray85',
                      command=save)
    bookmark_btn = Button(event_win, image=bookmark, font=('Comic Sans MS', 20), background='Yellow',
                          command=book)
    back = Button(event_win, text='BACK', font=('Comic Sans Ms', 20, 'bold'),
                  background='gray85', command=lambda: event_win.destroy())

    datelabel.pack(pady=10)
    file_label.pack(pady=10)
    file_name_fixed.place(relx=0.12, rely=0.23)
    file_name.place(relx=0.51, rely=0.23)
    content_label.pack(pady=50)
    content_inp.pack()
    save_btn.place(relx=0.3, rely=0.8)
    back.place(relx=0.6, rely=0.8)

    if flag_file == 'editfile':
        file = file.strip('\n')
        file1 = ''.join(file.split()[4:])
        file_name.insert(0, file1)
        with open(f"file/{file}", 'r+') as f:
            data = f.readlines()
            content_inp.insert('1.0', data[2].strip('\n'))

    elif flag_file == 'file':
        file = file.strip('\n')
        file1 = ''.join(file.split()[4:])
        file_name.insert(0, file1)
        with open(f"file/{file}", 'r+') as f:
            data = f.readlines()
            content_inp.insert('1.0', data[2].strip('\n'))
        file_label.destroy()
        content_label.destroy()
        content_inp.place(relx=0.1, rely=0.4)
        save_btn.destroy()
        back.place(relx=0.43, rely=0.77)

    event_win.mainloop()

def mood_log():
    def moodrating(newwindow):
        def selected_button(event):
            if mood_string.get() == moods[3]:
                combo_label.configure(text="I'm so happy for you! It's always wonderful to have a great day.")
            elif mood_string.get() == moods[1]:
                combo_label.configure(
                    text="It's okay to feel sad sometimes.Tomorrow is a new day, and I hope it will be better.")
            elif mood_string.get() == moods[2]:
                combo_label.configure(text="A neutral day can be a nice break sometimes.")
            elif mood_string.get() == moods[4]:
                combo_label.configure(text="That’s amazing! I’m so happy to hear you had such an exciting day!")
            elif mood_string.get() == moods[0]:
                combo_label.configure(text="I get that, sometimes things just don’t go the way we want.")

        mood_rate_win = Toplevel()
        mood_rate_win.title('MOOD RATING')
        mood_rate_win.geometry(win_size)
        mood_rate_win.configure(bg='lightblue')

        moods = ["😠 1", "😢 2", "😐 3", "😊 4", "😃 5"]
        mood_string = StringVar(value='select your mood rating please 😊')
        combo = tkinter.ttk.Combobox(mood_rate_win, values=[
            "😠 1", "😢 2", "😐 3", "😊 4", "😃 5"],
                             font=('Helvetica', 10), width=40, textvariable=mood_string)
        combo.place(relx=0.3, rely=0.2)
        # combo.pack()
        combo_label = Label(mood_rate_win, text='hello', width='40', font=("Times New Roman", 20, "italic"), height='5',
                            wraplength=300)
        back = Button(mood_rate_win, text='BACK', font=('Comic Sans Ms', 20, 'bold'),
                      background='gray85', command=lambda: mood_rate_win.destroy())
        back.place(relx=0.43, rely=0.8)
        combo.bind('<<ComboboxSelected>>', selected_button)
        combo_label.place(relx=0.1, rely=0.35)

    def moodtag(newwindow):
        def save_mood(tag):
            date = dt.datetime.today().isoformat()
            filename = date[:10] + ' ' + '-' + ' ' + 'MoodLog' + ' ' + '-' + ' ' + tag
            backend.MoodLog(date, filename=filename, content=tag)
            btn1.configure(activebackground='green')

        mood_tag_win = tkinter.Toplevel()
        mood_tag_win.title('EMOTION TAGS')
        mood_tag_win.geometry(win_size)
        mood_tag_win.configure(bg='lightblue')

        happy = PhotoImage(file='HAPPY - Copy.png')
        sad = PhotoImage(file='sad - Copy.png')
        neutral = PhotoImage(file='neutral.png')
        angry = PhotoImage(file='angry.png')
        excited = PhotoImage(file='excited1.png')
        lbl1 = Label(mood_tag_win, text='HAPPY', font=('Comic Sans MS', 15), bg='pink')
        btn1 = Button(mood_tag_win, image=happy, width=50, height=50, command=lambda: save_mood('happy'))
        lbl2 = Label(mood_tag_win, text='ANGRY', font=('Comic Sans MS', 15), bg='pink')
        btn2 = Button(mood_tag_win, image=angry, width=50, height=50, command=lambda: save_mood('angry'))
        lbl3 = Label(mood_tag_win, text='EXCITED', font=('Comic Sans MS', 15), bg='pink')
        btn3 = Button(mood_tag_win, image=excited, width=50, height=50, command=lambda: save_mood('excited'))
        lbl4 = Label(mood_tag_win, text='NEUTRAL', font=('Comic Sans MS', 15), bg='pink')
        btn4 = Button(mood_tag_win, image=neutral, width=50, height=50, command=lambda: save_mood('neutral'))
        lbl5 = Label(mood_tag_win, text='SAD', font=('Comic Sans MS', 15), bg='pink')
        btn5 = Button(mood_tag_win, image=sad, width=50, height=50, command=lambda: save_mood('sad'))
        btn6 = Button(mood_tag_win, text="SAVE", font=('Comic Sans MS', 20, 'bold'), command=lambda: save_mood)

        back = Button(mood_tag_win, text='BACK', font=('Comic Sans Ms', 20, 'bold'), command=lambda: mood_tag_win.destroy())
        back.place(relx=0.55, rely=0.75)

        lbl2.place(relx=0.31, rely=0.12) # angry
        lbl1.place(relx=0.447, rely=0.55) # happy
        lbl3.place(relx=0.685, rely=0.55) # excited
        lbl4.place(relx=0.157, rely=0.55) # neutral
        lbl5.place(relx=0.585, rely=0.12) # sad

        btn2.place(relx=0.32, rely=0.2)
        btn1.place(relx=0.45, rely=0.4)
        btn3.place(relx=0.7, rely=0.4)
        btn4.place(relx=0.18, rely=0.4)
        btn5.place(relx=0.58, rely=0.2)
        btn6.place(relx=0.3, rely=0.75)

        mood_tag_win.mainloop()

    mood_log_win = tkinter.Toplevel()
    mood_log_win.title('moodlog')
    mood_log_win.geometry(win_size)
    mood_log_win.configure(bg='lightblue')

    but1 = Button(mood_log_win, text='MOOD RATING', bg='pink', font=('Comic Sans MS',20),
                  command=lambda: moodrating(mood_log_win))
    but1.place(relx=0.3, rely=0.28)
    but2 = Button(mood_log_win, text='EMOTION TAGS', bg='pink', font=('Comic Sans MS',20),
                  command=lambda: moodtag(mood_log_win))
    but2.place(relx=0.3, rely=0.48)

def edit_entry():
    last_clk = None
    curr_time = 0

    def edit_file(event):
        nonlocal last_clk, curr_time
        curr_time = event.time
        if last_clk is not None:
            if curr_time - last_clk < 300:
                return
        last_clk = curr_time

        if 'DailyReflection' in entries.get(entries.curselection()):
            daily_reflect('editfile', entries.get(entries.curselection()))
            last_clk = None
            curr_time = 0

        elif 'EventNote' in entries.get(entries.curselection()):
            event_note('editfile', entries.get(entries.curselection()))
            last_clk = None
            curr_time = 0


    def del_file(event):
        nonlocal last_clk
        last_clk = event.time
        file = entries.get(entries.curselection()).strip('\n')
        with open("file_list.txt", 'r') as f:
            item = f.readlines()
            for j in item:
                if j.strip('\n') == file:
                    item.remove(j)
                    break
        with open("file_list.txt", 'w+') as f1:
            f1.writelines(item)
            f1.seek(0)
            entries.delete(0, END)
            for i in f1.readlines():
                entries.insert(0, i)
            os.remove(f"file/{file}")

    edit_window = Tk()
    edit_window.title("Edit and Delete")
    edit_window.geometry(win_size)
    edit_window.configure(bg='yellow2')

    entries = Listbox(edit_window, width=40, font=('Comic Sans MS', 15))
    edit_lbl = Label(edit_window, text='CLICK ON AN ITEM TO EDIT', font=('Comic Sans MS', 15), background='aquamarine3')
    del_lbl = Label(edit_window, text='DOUBLE CLICK ON AN ITEM TO DELETE', font=('Comic Sans MS', 15), background='aquamarine3')
    back = Button(edit_window, text='BACK', font=('Comic Sans Ms', 20),
                  background='lightgreen', command=lambda: edit_window.destroy())
    entries.bind("<<ListboxSelect>>", edit_file)
    entries.bind("<Double-1>", del_file)
    with open("file_list.txt", 'r') as f:
        lst = f.readlines()
    for i in lst:
        entries.insert(0, i)

    entries.place(relx=0.5, rely=0.5, anchor='center')
    edit_lbl.place(relx=0.3, rely=0.05)
    del_lbl.place(relx=0.25, rely=0.12)
    back.place(relx=0.43, rely=0.83)

    edit_window.mainloop()

def filter_entry():
    global search_window
    if optionmenu == 1:
        entry_type_menu.destroy()

    options = ['Filter by type',
               'Filter by date']

    clicked = StringVar()
    entry_menu = OptionMenu(search_window, clicked, *options)
    entry_menu.place(relx=0.73, rely=0.22)
    entry_menu.configure(bg='lightgreen')

    clicked.trace_add("write", lambda *args: on_select(clicked.get(), entry_menu))


def on_select(option, entry_menu):
    global optionmenu, entry_type_menu, entries, calflag

    entry_menu.destroy()
    optionmenu = 1
    options = ['Daily Reflection', 'Event Note', 'Mood log', 'BookMark']
    clicked = StringVar()
    entry_type_menu = OptionMenu(search_window, clicked, *options)
    entry_type_menu.configure(bg='lightpink')
    clicked.trace_add("write", lambda *args: entrytype(clicked.get()))

    if option == 'Filter by type':
        if calflag==1:
            cal.destroy()
        entries.delete(0, END)
        entry_type_menu.place(relx=0.73, rely=0.22)
        optionmenu = 1
    elif option == 'Filter by mood':
        pass
    elif option == 'Filter by date':
        calflag = 1
        filter_date()


def entrytype(option_type):
    if option_type == 'Daily Reflection':
        diary_mng = backend.DiaryManager()
        reflect = diary_mng.filter_entries(type_ent='Daily Reflection')
        entries.delete(0, END)
        for i in reflect:
            entries.insert(0, i)

    elif option_type == 'Event Note':
        diary_mng = backend.DiaryManager()
        event = diary_mng.filter_entries(type_ent='Event Note')
        entries.delete(0, END)
        for i in event:
            entries.insert(0, i)

    elif option_type == 'Mood log':
        mood = backend.MoodLog.filter(type_ent='Mood Log')
        entries.delete(0, END)
        for i in mood:
            entries.insert(0, i)

    elif option_type == 'BookMark':
        entries.delete(0, END)
        with open("bookmark_list.txt",'r') as f:
            for i in f.readlines():
                entries.insert(0, i.strip('\n'))


def filter_date():
    fdate = None
    sdate = None

    def showdate(event):
        nonlocal fdate, sdate
        if fdate is None:
            fdate = cal.get_date()
        elif sdate is None and fdate is not None:
            sdate = cal.get_date()

        diary_mng = backend.DiaryManager()
        filter_by_date = diary_mng.filter_entries(start_date=fdate, end_date=sdate)
        entries.delete(0, END)
        for i in filter_by_date:
            entries.insert(0, i)

        if fdate and sdate:
            fdate = sdate = None

    cal.bind("<<CalendarSelected>>", showdate)
    cal.place(relx=0.73, rely=0.25)


def search():
    global search_window, entries, cal

    def hintclr(event):
        search_lbl.delete(0, END)

    def hint(event):
        search_lbl.insert(0, "SEARCH")

    def search_file(event):
        diary_mng = backend.DiaryManager()
        a = diary_mng.search_entries(search_lbl.get())
        entries.delete(0, END)

        for i in a:
            entries.insert(0, i)

    def lst_file(event):
        entries.delete(0, END)
        with open("file_list.txt", 'r') as file:
            files = file.readlines()
            for i in files:
                entries.insert(0, i)

    def sort_file(event):
        if 'DailyReflection' in entries.get(entries.curselection()):
            daily_reflect('file', entries.get(entries.curselection()))

        elif 'EventNote' in entries.get(entries.curselection()):
            event_note('file', entries.get(entries.curselection()))

    search_window = Toplevel()
    search_window.title("SEARCH AND FILTER")
    search_window.geometry(win_size)
    search_window.configure(bg='yellow')

    filter_image = PhotoImage(file='filter_img.png')
    search_lbl = Entry(search_window, width=40, foreground='grey', font=('Comic Sans MS', 15))
    search_lbl.insert(0, "SEARCH")
    search_lbl.bind("<FocusIn>", hintclr)
    search_lbl.bind("<FocusOut>", hint)
    search_lbl.bind("<KeyRelease>", lambda event: search_file(event))
    search_lbl.bind("<Leave>", lst_file)
    cal = Calendar(search_window, date_pattern='yyyy-mm-dd', selectmode='day',
                   date=dt.date.today(),
                   font=('Comic Sans MS', 6))
    filter_btn = Button(search_window, image=filter_image, width=25, height=25, command=filter_entry)
    entries = Listbox(search_window, width=40, font=('Comic Sans MS', 15))
    back = Button(search_window, text='BACK', font=('Comic Sans Ms', 20),
                  background='lightblue', command=lambda: search_window.destroy())
    entries.bind("<<ListboxSelect>>", sort_file)
    diary_mng = backend.DiaryManager()
    a = diary_mng.search_entries()
    for i in a:
        entries.insert(0, i)

    search_lbl.place(relx=0.08, rely=0.15)
    filter_btn.place(relx=0.73, rely=0.15)
    entries.place(relx=0.08, rely=0.23)
    back.place(relx=0.4, rely=0.83)

    search_window.mainloop()

from backend import *

def sum_win():
    def summary(type=''):
        color1 = randint(10, 250) / 255
        color2 = randint(0, 255) / 255
        color3 = randint(0, 255) / 255

        if type == 'week':
            fig1, ax = plt.subplots(1, 2, figsize=(8, 6))
            ax[0].set_title("Weekly Event Summary", color='blue', fontsize='18')
            ax[0].set_xlabel('Weekly Event', color='red', fontsize='15')
            ax[0].set_ylabel("Count", color='green', fontsize='15')
            ax[0].bar(plot_events_week_x, plot_events_week_y, color=(color1, color2, color3))

            ax[1].set_title("Weekly Reflections Summary", color='blue', fontsize='17')
            ax[1].set_xlabel("Weekly Reflections", color='red', fontsize='15')
            ax[1].set_ylabel("Count", color='green', fontsize='15')
            ax[1].bar(plot_daily_reflection_week_x, plot_daily_reflection_week_y, color=(color3, color1, color2))

            for a in ax.flat:
                plt.setp(a.get_xticklabels(), rotation=45, ha="right")

            fig1.tight_layout()

            fig2, ax = plt.subplots((mood_log_counter_week + 1) // 2, 2, figsize=(10, 10))
            fig2.suptitle("MOOD TRACKER", fontsize=19, weight='bold')
            ax = ax.flatten()

            for i in range(mood_log_counter_week):
                labels = ['Angry', 'Sad', 'Neutral', 'Happy', 'Excited']
                colors = ['red', 'skyblue', '#47B39C', '#FFC154', '#EC6B56']
                size1 = [size_week[i][j] for j in range(len(size_week[i])) if size_week[i][j] != 0]
                filtered_labels = [labels[j] for j in range(len(size_week[i])) if size_week[i][j] != 0]
                ax[i].pie(size1, labels=filtered_labels, colors=colors, autopct='%0.1f%%', startangle=140)
                ax[i].set_aspect("equal")
                ax[i].set_title(plot_events_week_x[i], color='darkblue', fontsize='13')

            if mood_log_counter_week % 2 != 0:
                ax[-1].remove()
            fig2.tight_layout()
            plt.show()

        if type == 'month':
            fig1, ax = plt.subplots(1, 2, figsize=(8, 6))
            plt.xticks(fontsize=10)
            ax[0].set_title("monthly event summary", color='blue', fontsize='18')
            ax[0].set_xlabel("monthy event", color='red', fontsize='15')
            ax[0].set_ylabel("count", color='green', fontsize='15')
            ax[0].bar(plot_events_month_x, plot_events_month_y, color=(color2, color3, color1))
            ax[1].set_title("monthly reflections summary", color='blue', fontsize='17')
            plt.xticks(fontsize=10)
            ax[1].set_xlabel("monthly reflections", color='red', fontsize='15')
            ax[1].set_ylabel("count", color='green', fontsize='15')
            ax[1].bar(plot_daily_reflection_month_x, plot_daily_reflection_month_y, color=(color1, color3, color2))

            for a in ax.flat:
                plt.setp(a.get_xticklabels(), rotation=45, ha="right")
            fig1.tight_layout()

            fig2, ax = plt.subplots((mood_log_counter_month + 1) // 2, 2, figsize=(10, 8))
            fig2.suptitle("MOOD TRACKER", fontsize=20, weight='bold')
            ax = ax.flatten()
            for i in range(mood_log_counter_month):
                labels = ['angry', 'sad', 'neutral', 'happy', 'excited']
                colors = ['red', 'skyblue', '#47B39C', '#FFC154', '#EC6B56']

                size1 = [size_month[i][j] for j in range(len(size_month[i])) if size_month[i][j] != 0]
                filtered_labels = [labels[j] for j in range(len(size_month[i])) if size_month[i][j] != 0]
                ax[i].pie(size1, labels=filtered_labels, colors=colors, autopct='%0.1f%%', startangle=140)
                ax[i].set_aspect("equal")
                ax[i].set_title(plot_events_month_x[i], color='darkblue', fontsize='13')
            if mood_log_counter_week % 2 != 0:
                ax[-1].remove()
            fig2.tight_layout()
            plt.show()

    summary_win = Tk()
    summary_win.config(bg='darkorange')
    summary_win.geometry("750x500")
    summary_win.title("Personal Diary Management")
    time_period = Label(summary_win, text="SUMMARY", font=('Comic Sans MS', 25), fg ="black",
                        bg='darkorange', padx=10, pady=30)
    time_period.place(relx=0.38, rely=0.05)

    s = Button(summary_win, text="WEEKLY", font=('Comic Sans MS', 20), bg="linen", padx=15, pady=10,
               command=lambda: summary("week"))
    d = Button(summary_win, text="MONTHLY", font=('Comic Sans MS', 20), bg="linen", padx=15, pady=10,
               command=lambda: summary("month"))
    back = Button(summary_win, text='BACK', font=('Comic Sans Ms', 20),
                  background='aquamarine3', command=lambda: summary_win.destroy())

    s.place(relx=0.18, rely=0.4)
    d.place(relx=0.57, rely=0.4)
    back.place(relx=0.43, rely=0.74)

    summary_win.mainloop()


def register_win():
    global username, passcode, register_window, flag

    def checkbtn():
        global pass_show
        if pass_show:
            passcode.config(show='')
            pass_show = False
        else:
            passcode.config(show='*')
            pass_show = True

    register_window = Tk()
    register_window.title("REGISTER")
    register_window.geometry(win_size)

    data_frame = Frame(register_window)
    user = Label(data_frame, text='Enter Username', font=('Comic Sans MS', 15))
    password = Label(data_frame, text='Enter password', font=('Comic Sans MS', 15))

    if flag == 1:
        username = Entry(data_frame, justify='center', width=50)
        username.insert(0, username_chk.get())
        passcode = Entry(data_frame, justify='center', width=50, show='*')
    else:
        username = Entry(data_frame, justify='center', width=50)
        passcode = Entry(data_frame, justify='center', width=50, show='*')
    show_pass = Checkbutton(register_window, text='Show password', font=('Comic Sans MS', 15),
                            relief='raised', bg='aquamarine3', border='2.0',
                            command=checkbtn)
    submit = Button(register_window, text='SUBMIT', font=('Comic Sans Ms', 20, 'bold'),
                    background='aquamarine3', command=create_user)
    back = Button(register_window, text='BACK', font=('Comic Sans Ms', 20, 'bold'),
                  background='aquamarine3', command=lambda: register_window.destroy())

    data_frame.place(relx=0.5, rely=0.25, anchor='center')
    user.pack()
    username.pack(pady=20, fill='x')
    password.pack()
    passcode.pack(pady=20, fill='x')
    show_pass.place(relx=0.38, rely=0.43)
    submit.place(relx=0.4, rely=0.55)
    back.place(relx=0.43, rely=0.74)

    register_window.mainloop()

def create_user():
    global user_name, pwd, register_window, flag
    user_name = username.get()
    pwd = passcode.get()
    l = []
    if flag == 1:
        with open("login.csv", "r") as read:
            reader = csv.reader(read)
            for i in reader:
                if user_name in i:
                    i[1] = pwd
                l.append(i)
        with open("login.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for line in l:
                writer.writerow(line)

    else:
        with open("login.csv", "a+", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user_name, pwd])

    username.delete(0, END)
    passcode.delete(0, END)
    flag = 0

    register_window.destroy()

bg_frame = Frame(root)
btn_frame = Frame(root)
btn_frame1 = Frame(root)

bookmark = PhotoImage(file='bookmark - Copy.png')
bg = PhotoImage(file='diary.png')
label_bg = Label(bg_frame, image=bg)
login = Button(root, width=10, height=1, text='LOGIN', font=('Comic Sans Ms', 15, 'bold'),
               background='linen',fg ='black',command=login_win)
register = Button(root, width=10, height=1, text='REGISTER', font=('Comic Sans MS', 15, 'bold'),
                  background='linen',fg='black', command=register_win)
exit = Button(root, width=5, height=1, text='EXIT', font=('Comic Sans MS', 15, 'bold'),
                  background='lightsalmon', command=lambda: root.destroy())

bg_frame.place(relx=0.5, rely=0.36, anchor='center')
label_bg.pack(pady='10')
btn_frame.place(relx=0.37, rely=0.85, anchor='center')
btn_frame1.place(relx=0.63, rely=0.85, anchor='center')
register.place(relx=0.3, rely=0.66)
login.place(relx=0.5215, rely=0.66)
exit.place(relx=0.45, rely=0.80)

root.mainloop()
