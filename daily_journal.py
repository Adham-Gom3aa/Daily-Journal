from collections import Counter
import customtkinter as tk
import mysql.connector as mysql
from tkinter import messagebox
import calendar
import datetime
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

font = ("Arial", 16)

class Database:
    def __init__(self):
        self.mydb = mysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="daily_journal",
            autocommit=True
        )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS daily_journal")
        self.mycursor.execute('''CREATE table IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY
                        , username VARCHAR(255) UNIQUE
                        , password VARCHAR(255),year_rate TEXT, year_moods TEXT, year_sleep TEXT,year_dream TEXT,notes TEXT)''')

    def get_user_info(self, username, password):
        if username == "" or password == "":
            messagebox.showerror("Error", 'Please enter username and password!')
            return False

        try:
            self.mycursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                                  (username, password))
            result = self.mycursor.fetchall()
            if not result:
                messagebox.showerror("Error", 'invalid username or password!')
                return False

            elif username in result[0] and password in result[0]:
                messagebox.showinfo('logged in', 'login successful')
                self.username = username
                self.password = password
                return True

        except:
            messagebox.showerror("Error", 'invalid username or password!')
            return False

        return True

    def set_user_info(self, username, password):
        if username == "" or password == "":
            messagebox.showerror("Error", 'Please enter username and password!')
            return False

        try:
            self.mycursor.execute('INSERT INTO users (username,password) VALUES (%s,%s)', (username, password))
            if not hasattr(self, 'username'):
                self.username = username
                self.password = password

        except:
            messagebox.showerror("Error", 'this Username is already used!')
            return False

        messagebox.showinfo('Signed up', 'Sign up Successful')
        return True

    def set_year_rate(self, rate, username):
        self.rate_file = json.dumps(rate)
        self.mycursor.execute('UPDATE users SET year_rate = %s WHERE username = %s', (self.rate_file, username))

    def get_year_rate(self):
        try:
            self.mycursor.execute('SELECT year_rate FROM users WHERE username = %s', (self.username,))
            result = self.mycursor.fetchone()
            if result and result[0]:
                return json.loads(result[0])

        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")

        return [['gray' for _ in range(31)] for _ in range(12)]

    def set_year_moods(self, moods, username):
        self.moods_file = json.dumps(moods)
        self.mycursor.execute('UPDATE users SET year_moods = %s WHERE username = %s', (self.moods_file, username))

    def get_year_moods(self):
        try:
            self.mycursor.execute('SELECT year_moods FROM users WHERE username = %s', (self.username,))
            result = self.mycursor.fetchone()
            if result and result[0]:
                return json.loads(result[0])

        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")

        return [['gray' for _ in range(31)] for _ in range(12)]

    def set_year_sleep(self, sleep, username):
        self.sleep_file = json.dumps(sleep)
        self.mycursor.execute('UPDATE users SET year_sleep = %s WHERE username = %s', (self.sleep_file, username))

    def get_year_sleep(self):
        try:
            self.mycursor.execute('SELECT year_sleep FROM users WHERE username = %s', (self.username,))
            result = self.mycursor.fetchone()
            if result and result[0]:
                return json.loads(result[0])

        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")

        return [['gray' for _ in range(31)] for _ in range(12)]

    def set_year_dream(self, dream, username):
        self.dream_file = json.dumps(dream)
        self.mycursor.execute('UPDATE users SET year_dream = %s WHERE username = %s', (self.dream_file, username))

    def get_year_dream(self):
        try:
            self.mycursor.execute('SELECT year_dream FROM users WHERE username = %s', (self.username,))
            result = self.mycursor.fetchone()
            if result and result[0]:
                return json.loads(result[0])

        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")

        return [['gray' for _ in range(31)] for _ in range(12)]

    def set_notes(self, notes, username):
        self.Notes_file = json.dumps(notes)
        self.mycursor.execute('UPDATE users SET notes = %s WHERE username = %s', (self.Notes_file, username))

    def get_notes(self):
        try:
            self.mycursor.execute('SELECT notes FROM users WHERE username = %s', (self.username,))
            result = self.mycursor.fetchone()
            if result and result[0]:
                return json.loads(result[0])

        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {str(err)}")


class GuiJournal:
    def __init__(self):
        self.db = Database()
        self.root = tk.CTk()
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.title('Daily Journal')
        self.page2 = tk.CTkFrame(self.root, fg_color='#091a21', bg_color='#091a21')
        self.table = tk.CTkFrame(self.page2, fg_color='#14232b', border_width=3, border_color='white')
        self.title = tk.CTkLabel(self.table, text='Rate\n 2024', font=('Tahoma', 25, 'bold'), bg_color='#323d42',
                                 text_color='white', width=100, height=50)
        self.frame = tk.CTkFrame(self.page2, fg_color='#091a21')
        self.nextB = tk.CTkButton(self.frame, text='Next', command=self.Mood_table,
                                  font=('Tahoma', 20, 'bold'), width=150, fg_color='#33576e', text_color='white')
        self.backB = tk.CTkButton(self.frame, text='Back', command=lambda: [self.login_page(), self.page2.pack_forget()],
                                  font=('Tahoma', 20, 'bold'), width=150, fg_color='#33576e', text_color='white')
        self.colors = tk.CTkComboBox(self.page2, font=('Tahoma', 20, 'bold'), width=110, state='readonly')
        self.notes = {}
        self.month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
                           8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

        self.day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday',
                         6: 'Sunday'}

        self.note_label = tk.CTkLabel(self.root, text="", fg_color="lightyellow",corner_radius=10,anchor='w')
        self.p2 = False
        self.p3 = False
        self.p4 = False
        self.p5 = False
        self.login_page()
        self.root.mainloop()

    def login_page(self):
        self.page1 = tk.CTkFrame(self.root)
        self.root.geometry("400x400")
        self.page1.configure(fg_color="lightgray")
        self.root.title("Daily Journal")
        self.label = tk.CTkLabel(self.page1, text="Daily Journal", font=("Arial", 50, "bold"), text_color='white')
        self.label.pack(pady=20)
        self.label_username = tk.CTkLabel(self.page1, text="Username", font=font, text_color='white')
        self.label_username.pack(pady=5)
        self.entry_username = tk.CTkEntry(self.page1, font=font, text_color='white', fg_color="lightblue")
        self.entry_username.pack(pady=10)
        self.label_password = tk.CTkLabel(self.page1, text="Password", font=font, text_color='white')
        self.label_password.pack(pady=5)
        self.entry_password = tk.CTkEntry(self.page1, font=font, text_color='white', fg_color="lightblue", show="*")
        self.entry_password.pack(pady=10)

        frame1 = tk.CTkFrame(self.page1, fg_color="lightgray")
        self.login_button = tk.CTkButton(frame1, text="Login", command=self.login, font=font, text_color='white',
                                         fg_color="gray", width=80)
        self.login_button.grid(row=0, column=0, pady=10, padx=10)
        self.signup_button = tk.CTkButton(frame1, text="Sign Up", command=self.signup, font=font, text_color='white',
                                          fg_color="gray", width=80)
        self.signup_button.grid(row=0, column=1, pady=10, padx=10)

        frame1.pack(pady=20)
        self.page1.pack(fill='both', expand=True)

    def mainPage(self):
        self.Bs = [['' for _ in range(31)] for _ in range(12)]
        self.root.geometry("1250x650")
        months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        days = [str(i) for i in range(1, 32)]

        for i in range(len(months)):
            label = tk.CTkLabel(self.table, text=months[i], font=('Tahoma', 20, 'bold'), bg_color='#33576e',
                                text_color='white')
            if i == 11:
                label.grid(row=i + 1, column=0, sticky='news', padx=(5, 0), pady=(0, 5))
            else:
                label.grid(row=i + 1, column=0, sticky='news', padx=(5, 0))

        for j in range(len(days)):
            label = tk.CTkLabel(self.table, text=days[j], font=('Tahoma', 15, 'bold'), bg_color='#33576e',
                                text_color='white')
            if j == 30:
                label.grid(row=0, column=j + 1, sticky='news', padx=(0, 5), pady=(5, 0))
            else:
                label.grid(row=0, column=j + 1, ipadx=5, sticky='news', pady=(5, 0))

        self.title.grid(row=0, column=0, columnspan=1, ipadx=5, ipady=5, sticky='news', padx=(5, 0), pady=(5, 0))
        for i in range(len(months)):
            for j in range(len(days)):
                b = tk.CTkButton(self.table, text='', font=('Tahoma', 10), command=lambda x=i, y=j: self.selected(x, y),
                                 width=25, height=25, border_width=1, fg_color=self.year_colors[i][j],
                                 border_color='white')
                b.grid(row=i + 1, column=j + 1, columnspan=1, pady=5, padx=5, sticky='news')

                if (j + 1 > datetime.datetime.now().day and i + 1 >= datetime.datetime.now().month) or i + 1 > datetime.datetime.now().month:
                    b.configure(state='disabled', fg_color='#454545')

                if j + 1 > int(calendar.monthrange(2024, i + 1)[1]):
                    b.configure(state='disabled', fg_color='black')

                b.bind("<Enter>", lambda event, d=f"{j + 1}/{i + 1}": self.show_note(event, d, self.note_label))
                b.bind("<Leave>", lambda event: self.hide_note(self.note_label))
                self.Bs[i][j] = b
                self.year_colors[i][j] = b.cget('fg_color')

        self.nextB.grid(row=0, column=1, pady=20, padx=20)
        self.backB.grid(row=0, column=0, pady=20, padx=20)
        self.table.pack(pady=20)
        self.colors.pack()
        self.frame.pack()
        self.page2.pack(fill='both', expand=True)

    def Rate_table(self):
        self.p3 = False
        self.p4 = False
        self.p5 = False
        self.p2 = True
        self.title.configure(text='Rate\n 2024 ')
        self.colors_options = {'1 Star': '#1d2a62', '2 Stars': '#87aece', '3 Stars': '#f5f3d8', '4 Stars': '#afd06e',
                               '5 Stars': '#437118'}

        self.root.geometry("1250x650")

        if self.db.get_year_rate():
            self.year_colors = self.db.get_year_rate()
        if self.db.get_notes():
            self.notes = self.db.get_notes()

        for i in range(12):
            for j in range(31):
                if (j + 1 > datetime.datetime.now().day and i + 1 >= datetime.datetime.now().month) or i + 1 > datetime.datetime.now().month:
                    self.year_colors[i][j] = '#454545'
                elif (j + 1 == datetime.datetime.now().day and i + 1 == datetime.datetime.now().month):
                    self.year_colors[i][j] = 'gray'

                if j + 1 > int(calendar.monthrange(2024, i + 1)[1]):
                    self.year_colors[i][j] = 'black'

        self.colors.configure(values=['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'])
        self.nextB.configure(command=self.Mood_table)
        self.colors.set('')
        self.backB.configure(command=lambda: [self.login_page(), self.page2.pack_forget()])

        if hasattr(self, 'Bs'):
            for i in range(12):
                for j in range(31):
                    self.Bs[i][j].configure(fg_color=self.year_colors[i][j])

    def Mood_table(self):
        self.p4 = False
        self.p5 = False
        self.p3 = True
        self.p2 = False
        self.title.configure(text='2024\nMoods ')
        self.colors_options = {'Depressed': '#ff69b4', 'Sad': '#ffb4b4', 'Neutral': '#fcf6bd', 'Happy': '#ffdc5e',
                               'Excited': '#ff9900'}

        if self.db.get_year_moods():
            self.year_colors = self.db.get_year_moods()

        for i in range(12):
            for j in range(31):
                if (j + 1 > datetime.datetime.now().day and i + 1 >= datetime.datetime.now().month) or i + 1 > datetime.datetime.now().month:
                    self.year_colors[i][j] = '#454545'
                elif (j + 1 == datetime.datetime.now().day and i + 1 == datetime.datetime.now().month):
                    self.year_colors[i][j] = 'gray'

                if j + 1 > int(calendar.monthrange(2024, i + 1)[1]):
                    self.year_colors[i][j] = 'black'

        self.colors.configure(values=['Depressed', 'Sad', 'Neutral', 'Happy', 'Excited'])
        self.colors.set('')
        self.nextB.configure(command=self.Sleep_table)
        self.backB.configure(command=self.Rate_table)

        for i in range(12):
            for j in range(31):
                self.Bs[i][j].configure(fg_color=self.year_colors[i][j])

    def Sleep_table(self):
        self.p4 = True
        self.p5 = False
        self.p3 = False
        self.p2 = False
        self.title.configure(text='2024\nSleep ')
        self.colors_options = {'1-2 Hours': '#D4B0FF', '3-5 Hours': '#C8A2C8', '6-8 Hours': '#9B59B6',
                               '9-11 Hours': '#6A0DAD', '12+ Hours': '#3D0C6B'}

        if self.db.get_year_sleep():
            self.year_colors = self.db.get_year_sleep()

        for i in range(12):
            for j in range(31):
                if (j + 1 > datetime.datetime.now().day and i + 1 >= datetime.datetime.now().month) or i + 1 > datetime.datetime.now().month:
                    self.year_colors[i][j] = '#454545'
                elif (j + 1 == datetime.datetime.now().day and i + 1 == datetime.datetime.now().month):
                    self.year_colors[i][j] = 'gray'

                if j + 1 > int(calendar.monthrange(2024, i + 1)[1]):
                    self.year_colors[i][j] = 'black'

        self.colors.configure(values=['1-2 Hours', '3-5 Hours', '6-8 Hours', '9-11 Hours', '12+ Hours'])
        self.colors.set('')
        self.nextB.configure(command=self.Dream_table)
        self.backB.configure(command=self.Mood_table)

        for i in range(12):
            for j in range(31):
                self.Bs[i][j].configure(fg_color=self.year_colors[i][j])

    def Dream_table(self):
        self.colors_options = {'can\'t remember': '#E7E6F7', 'Happy': '#FDC5F5', 'Sad': '#A6E3E9', 'Weird': '#FFB347',
                               'Scary': '#4B4453'}

        self.p4 = False
        self.p5 = True
        self.p3 = False
        self.p2 = False
        self.title.configure(text='2024\nDream')

        if self.db.get_year_dream():
            self.year_colors = self.db.get_year_dream()

        for i in range(12):
            for j in range(31):
                if (j + 1 > datetime.datetime.now().day and i + 1 >= datetime.datetime.now().month) or i + 1 > datetime.datetime.now().month:
                    self.year_colors[i][j] = '#454545'
                elif (j + 1 == datetime.datetime.now().day and i + 1 == datetime.datetime.now().month):
                    self.year_colors[i][j] = 'gray'

                if j + 1 > int(calendar.monthrange(2024, i + 1)[1]):
                    self.year_colors[i][j] = 'black'

        self.colors.configure(values=['can\'t remember', 'Happy', 'Sad', 'Weird', 'Scary'])
        self.colors.set('')

        for i in range(12):
            for j in range(31):
                self.Bs[i][j].configure(fg_color=self.year_colors[i][j])

        self.nextB.configure(command=self.stats_rate)
        self.backB.configure(command=self.Sleep_table)

    def chart_data(self, category_data, category_dict, color_map):
        for i in range(len(category_data)):
            for j in range(len(category_data[0])):
                color = category_data[i][j]
                if color in color_map:
                    category_dict[color_map[color]] += 1

    def streak_counter(self, category_data, color):
        streak_count = [1, (), ()]
        strk = []

        for i in range(len(category_data)):
            for j in range(len(category_data[0])):
                temp = category_data[i][j]

                if j == len(category_data[0]) - 1:
                    if temp == category_data[i][j - 1] and temp == color:
                        streak_count[0] += 1
                        if streak_count[1] == ():
                            streak_count[1] = (i, j)
                if j + 1 <= len(category_data[0]) - 1:
                    if temp == category_data[i][j + 1] and temp == color:
                        streak_count[0] += 1
                        if streak_count[1] == ():
                            streak_count[1] = (i, j)
                    else:
                        streak_count[2] = (i, j)
                        strk.append(streak_count)
                        if len(strk) >= 2:
                            if strk[1][0] >= strk[0][0]:
                                strk.pop(0)
                            else:
                                strk.pop(1)
                        streak_count = [1, (), ()]

        if strk[0][1] == ():
            if any(color in i for i in category_data):
                for i in range(len(category_data)):
                    for j in range(len(category_data[0])):
                        if category_data[i][j] == color:
                            return [1, (i, j), (i, j)]
            return [0, (-1, -1), (-1, -1)]

        return strk[0]

    def week_avg(self, category_data, dict):
        weeks_avg = []
        week = 0
        count = 0

        for i in range(len(category_data)):
            for j in range(len(category_data[0])):
                if category_data[i][j] == 'black' or category_data[i][j] == 'gray' or category_data[i][j] == '#454545':
                    continue

                date = datetime.datetime(2024, i + 1, j + 1)
                r = category_data[i][j]

                if date.weekday() == 5 and count != 0:
                    if '#E7E6F7' in dict.keys():
                        weeks_avg.append(f'{week}')
                    else:
                        weeks_avg.append(f'{week / count:.1f}')
                    week = 0
                    count = 0

                    if r in dict.keys():
                        week += dict[r]
                        count += 1
                else:
                    if r in dict.keys():
                        week += dict[r]
                        count += 1

        if not weeks_avg:
            return ['0']
        return weeks_avg

    def day_avg(self, category_data, dict):
        days = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        final_day = {'Monday': '0', 'Tuesday': '0', 'Wednesday': '0', 'Thursday': '0', 'Friday': '0',
                     'Saturday': '0', 'Sunday': '0'}

        for i in range(len(category_data)):
            for j in range(len(category_data[0])):
                if category_data[i][j] == 'black' or category_data[i][j] == 'gray' or category_data[i][j] == '#454545':
                    continue

                r = category_data[i][j]
                date = datetime.datetime(2024, i + 1, j + 1)

                if r in dict.keys():
                    days[date.weekday()] += dict[r]
                    count[date.weekday()] += 1

        for i in days:
            if count[i] != 0:
                final_day[self.day_dict[i]] = f'{days[i] / count[i]:.1f}'

        return final_day

    def day_count(self):
        category_data = self.db.get_year_dream()
        map = {
            '#FDC5F5': 'Happy',
            '#A6E3E9': 'Sad',
            '#FFB347': 'Weird',
            '#4B4453': 'Scary'
        }

        final_day = {'Monday': '0', 'Tuesday': '0', 'Wednesday': '0', 'Thursday': '0', 'Friday': '0',
                     'Saturday': '0', 'Sunday': '0'}
        count = {0: {'Happy': 0, 'Sad': 0, 'Weird': 0, 'Scary': 0},
                 1: {'Happy': 0, 'Sad': 0, 'Weird': 0, 'Scary': 0},
                 2: {'Happy': 0, 'Sad': 0, 'Weird': 0, 'Scary': 0},
                 3: {'Happy': 0, 'Sad': 0, 'Weird': 0, 'Scary': 0},
                 4: {'Happy': 0, 'Sad': 0, 'Weird': 0, 'Scary': 0},
                 5: {'Happy': 0, 'Sad': 0, 'Weird': 0, 'Scary': 0},
                 6: {'Happy': 0, 'Sad': 0, 'Weird': 0, 'Scary': 0}}

        for i in range(len(category_data)):
            for j in range(len(category_data[0])):
                if category_data[i][j] == 'black' or category_data[i][j] == 'gray' or category_data[i][j] == '#454545':
                    continue

                date = datetime.datetime(2024, i + 1, j + 1)
                if category_data[i][j] in map.keys():
                    count[date.weekday()][map[category_data[i][j]]] += 1

        days = []
        for i in count:
            days.append(max(count[i], key=count[i].get))

        for i, j in enumerate(final_day):
            final_day[j] = days[i]

        return final_day

    def month_Count(self, category_data, month):
        dream_map = {
            '#FDC5F5': 'Happy',
            '#A6E3E9': 'Sad',
            '#FFB347': 'Weird',
            '#4B4453': 'Scary'
        }
        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                  'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        skip_items = ['#454545', 'black', 'gray', '#E7E6F7']

        filtered_list = [item for item in category_data[months[month] - 1] if item not in skip_items]
        if not filtered_list:
            return 'No data to display'
        rating = Counter(filtered_list)
        final = f'{month} : Mostly {dream_map[rating.most_common(1)[0][0]]} Dreams'

        return final

    def month_avg(self, category_data, dict):
        months_avg = []
        month = 0
        temp = 0
        count = 0

        for i in range(len(category_data)):
            for j in range(len(category_data[0])):
                r = category_data[i][j]
                if r == '#E7E6F7':
                    continue

                if i == temp and r in dict.keys():
                    month += dict[r]
                    count += 1
                else:
                    if count != 0:
                        months_avg.append(f'{month / count:.1f}')
                    month = 0
                    count = 0
                    temp = i

        if not months_avg:
            return ['0']
        return months_avg

    def draw_pie_chart(self, ax, data, colors, title):
        if sum(data.values()) == 0:
            ax.text(0.5, 0.5, 'No data to display', horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes, fontsize=12)
            return

        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90, colors=colors,
               textprops={'fontsize': 10, 'color': 'black'})
        ax.axis('equal')
        ax.set_title(title)

    def add_note(self, date):
        input_dialog = tk.CTkInputDialog(text=f"Add a note for {date}:", title="Add Note")

        note = input_dialog.get_input()
        if note:
            if date in self.notes:
                existing_dream = self.notes[date].split('Dream:\n', 1)[-1]
                self.notes[date] = f'Note:\n{note}\nDream:\n{existing_dream}'
            else:
                self.notes[date] = f'Note:\n{note}\nDream:\n'

    def add_dream(self, date):
        input_dialog = tk.CTkInputDialog(text=f"Add a dream for {date}:", title="Add Dream")

        dream = input_dialog.get_input()
        if dream:
            if date in self.notes:
                existing_note = self.notes[date].split('Note:\n', 1)[-1].split('\nDream:\n')[0]
                self.notes[date] = f'Note:\n{existing_note}\nDream:\n{dream}'
            else:
                self.notes[date] = f'Note:\n\nDream:\n{dream}'

    def show_note(self, event, date, note_label):
        if date in self.notes:
            note_label.configure(text=self.notes[date])
            note_label.place(x=event.x_root - 50, y=event.y_root - 50)

    def hide_note(self, note_label):
        note_label.place_forget()

    def update_week(self, event, data):
        weeks = self.week_avg(data, self.rate_dict)
        selected_week = int(self.l2.get())
        self.week.configure(text=f"Week {selected_week}: {weeks[selected_week - 1]} Stars")

        if '#ff69b4' in self.rate_dict.keys():
            if float(weeks[selected_week - 1]) <= 1:
                self.week.configure(text=f"Week {selected_week}  : Depressed \nAverage Rate: {weeks[selected_week - 1]}")
            elif float(weeks[selected_week - 1]) <= 2:
                self.week.configure(text=f"Week {selected_week}  : Mildly Depressed \nAverage Rate: {weeks[selected_week - 1]}")
            elif float(weeks[selected_week - 1]) <= 3:
                self.week.configure(text=f"Week {selected_week}  : Neutral \nAverage Rate: {weeks[selected_week - 1]}")
            elif float(weeks[selected_week - 1]) <= 4:
                self.week.configure(text=f"Week {selected_week}  : Happy \nAverage Rate: {weeks[selected_week - 1]}")
            elif float(weeks[selected_week - 1]) <= 5:
                self.week.configure(text=f"Week {selected_week}  : Very Happy \nAverage Rate: {weeks[selected_week - 1]}")

        if '#D4B0FF' in self.rate_dict.keys():
            if float(weeks[selected_week - 1]) >= 12:
                self.week.configure(text=f"Week {selected_week}  : Woke up late \nAverage Sleep: {weeks[selected_week - 1]} Hours")
            elif float(weeks[selected_week - 1]) >= 10:
                self.week.configure(text=f"Week {selected_week}  : Slept a lot \nAverage Sleep: {weeks[selected_week - 1]} Hours")
            elif float(weeks[selected_week - 1]) >= 7:
                self.week.configure(text=f"Week {selected_week}  : Slept well \nAverage Sleep: {weeks[selected_week - 1]} Hours")
            elif float(weeks[selected_week - 1]) >= 4:
                self.week.configure(text=f"Week {selected_week}  : Slept a bit \nAverage Sleep: {weeks[selected_week - 1]} Hours")
            elif float(weeks[selected_week - 1]) >= 1.5:
                self.week.configure(text=f"Week {selected_week}  : Sleepy \nAverage Sleep: {weeks[selected_week - 1]} Hours")

        if "#E7E6F7" in self.rate_dict.keys():
            if float(weeks[selected_week - 1]) == 1:
                self.week.configure(text=f"Week {selected_week}  : {weeks[selected_week - 1]} Time")
            else:
                self.week.configure(text=f"Week {selected_week}  : {weeks[selected_week - 1]} Times")

    def update_month(self, event, data):
        months = self.month_avg(data, self.rate_dict)
        selected_month = self.l3.get()
        map = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
               'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

        self.month.configure(text=f"{selected_month}  : {months[map[selected_month] - 1]} Stars")

        if '#ff69b4' in self.rate_dict.keys():
            if float(months[map[selected_month] - 1]) <= 1:
                self.month.configure(text=f"{selected_month}  : Depressed \nAverage Rate: {months[map[selected_month] - 1]}")
            elif float(months[map[selected_month] - 1]) <= 2:
                self.month.configure(text=f"{selected_month}  : Mildly Depressed \nAverage Rate: {months[map[selected_month] - 1]}")
            elif float(months[map[selected_month] - 1]) <= 3:
                self.month.configure(text=f"{selected_month}  : Neutral \nAverage Rate: {months[map[selected_month] - 1]}")
            elif float(months[map[selected_month] - 1]) <= 4:
                self.month.configure(text=f"{selected_month}  : Happy \nAverage Rate: {months[map[selected_month] - 1]}")
            elif float(months[map[selected_month] - 1]) <= 5:
                self.month.configure(text=f"{selected_month}  : Very Happy \nAverage Rate: {months[map[selected_month] - 1]}")

        if '#D4B0FF' in self.rate_dict.keys():
            if float(months[map[selected_month] - 1]) >= 12:
                self.month.configure(text=f"{selected_month}  : Woke up late \nAverage Sleep: {months[map[selected_month] - 1]} Hours")
            elif float(months[map[selected_month] - 1]) >= 10:
                self.month.configure(text=f"{selected_month}  : Slept a lot \nAverage Sleep: {months[map[selected_month] - 1]} Hours")
            elif float(months[map[selected_month] - 1]) >= 7:
                self.month.configure(text=f"{selected_month}  : Slept well \nAverage Sleep: {months[map[selected_month] - 1]} Hours")
            elif float(months[map[selected_month] - 1]) >= 4:
                self.month.configure(text=f"{selected_month}  : Slept a bit \nAverage Sleep: {months[map[selected_month] - 1]} Hours")
            elif float(months[map[selected_month] - 1]) >= 1.5:
                self.month.configure(text=f"{selected_month}  : Sleepy \nAverage Sleep: {months[map[selected_month] - 1]} Hours")

        if '#FDC5F5' in self.rate_dict.keys():
            Text = self.month_Count(data, selected_month)
            self.month.configure(text=Text)

    def update_streak(self, event, rate_map, data):
        selected_color = rate_map[self.l1.get()]
        long, start, end = self.streak_counter(data, selected_color)
        self.strk_5.configure(
            text=f"Longest {self.l1.get()} Streak: {long} days from {start[1] + 1}/{start[0] + 1}  to  {end[1] + 1}/{end[0] + 1}"
        )

    def update_day(self, event, data):
        day_avg = self.day_avg(data, self.rate_dict)
        selected_day = self.l4.get()
        self.day_rate.configure(text=f"{selected_day}  : {day_avg[selected_day]} Stars")

        if '#ff69b4' in self.rate_dict.keys():
            if float(day_avg[selected_day]) <= 1:
                self.day_rate.configure(text=f"{selected_day}  :Depressed \nAverage Rate: {day_avg[selected_day]}")
            elif float(day_avg[selected_day]) <= 2:
                self.day_rate.configure(text=f"{selected_day}  : Mildly Depressed \nAverage Rate: {day_avg[selected_day]}")
            elif float(day_avg[selected_day]) <= 3:
                self.day_rate.configure(text=f"{selected_day}  : Neutral \nAverage Rate: {day_avg[selected_day]}")
            elif float(day_avg[selected_day]) <= 4:
                self.day_rate.configure(text=f"{selected_day}  : Happy \nAverage Rate: {day_avg[selected_day]}")
            elif float(day_avg[selected_day]) <= 5:
                self.day_rate.configure(text=f"{selected_day}  : Very Happy \nAverage Rate: {day_avg[selected_day]}")

        if '#D4B0FF' in self.rate_dict.keys():
            if float(day_avg[selected_day]) >= 12:
                self.day_rate.configure(text=f"{selected_day}  : Woke up late \nAverage Sleep: {day_avg[selected_day]} Hours")
            elif float(day_avg[selected_day]) >= 10:
                self.day_rate.configure(text=f"{selected_day}  : Slept a lot \nAverage Sleep: {day_avg[selected_day]} Hours")
            elif float(day_avg[selected_day]) >= 7:
                self.day_rate.configure(text=f"{selected_day}  : Slept well \nAverage Sleep: {day_avg[selected_day]} Hours")
            elif float(day_avg[selected_day]) >= 4:
                self.day_rate.configure(text=f"{selected_day}  : Slept a bit \nAverage Sleep: {day_avg[selected_day]} Hours")
            elif float(day_avg[selected_day]) >= 1.5:
                self.day_rate.configure(text=f"{selected_day}  : Sleepy \nAverage Sleep: {day_avg[selected_day]} Hours")

        if '#FDC5F5' in self.rate_dict.keys():
            days = self.day_count()
            self.day_rate.configure(text=f"Your dreams for {selected_day} are {days[selected_day]}")

    def stats_rate(self):
        self.page2.pack_forget()
        self.stats = tk.CTkFrame(self.root)
        self.stats.configure(fg_color='#f7e8d5', bg_color='#f7e8d5')
        self.root.title("Statistics")

        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#23556b')

        rate_map = {
            '#1d2a62': '1 Star',
            '#87aece': '2 Stars',
            '#f5f3d8': '3 Stars',
            '#afd06e': '4 Stars',
            '#437118': '5 Stars'
        }

        self.rate_dict = {'#1d2a62': 1, '#87aece': 2, '#f5f3d8': 3, '#afd06e': 4, '#437118': 5}
        Rates = {key: 0 for key in rate_map.values()}

        a = self.db.get_year_rate()
        self.chart_data(a, Rates, rate_map)
        self.draw_pie_chart(ax, Rates, rate_map.keys(), 'Rates')

        f = tk.CTkFrame(self.stats, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f2 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f3 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')

        self.nextS = tk.CTkButton(f2, text='Next', fg_color='#454545', font=('Tahoma', 20, 'bold'), width=150,
                                  command=lambda: self.stats_moods())
        self.backS = tk.CTkButton(f2, text='Back', fg_color='#454545', font=('Tahoma', 20, 'bold'), width=150,
                                  command=lambda: [self.stats.pack_forget(), self.mainPage()])

        self.nextS.grid(row=0, column=1, pady=20, padx=20)
        self.backS.grid(row=0, column=0, pady=20, padx=20)

        long, start, end = self.streak_counter(a, '#437118')
        weeks = self.week_avg(a, self.rate_dict)
        values = [str(i + 1) for i in range(len(weeks))]

        temp = {'1 Star': '#1d2a62', '2 Stars': '#87aece', '3 Stars': '#f5f3d8', '4 Stars': '#afd06e', '5 Stars': '#437118'}

        self.l1 = tk.CTkComboBox(f3, values=['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                                 font=('Tahoma', 25, 'bold'),
                                 command=lambda event, t=temp, data=a: self.update_streak(event, t, data),
                                 state='readonly')

        self.l1.grid(row=0, column=0, pady=(200, 10), padx=10)

        self.l2 = tk.CTkComboBox(f3, values=values, font=('Tahoma', 25, 'bold'),
                                 command=lambda event, data=a: self.update_week(event, data),
                                 state='readonly')

        self.l2.grid(row=1, column=0, pady=10, padx=10)

        month = self.month_avg(a, self.rate_dict)
        values = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

        days = self.day_avg(a, self.rate_dict)

        self.l3 = tk.CTkComboBox(f3, values=values[:len(month)], font=('Tahoma', 20, 'bold'),
                                 command=lambda event, data=a: self.update_month(event, data),
                                 state='readonly')

        self.l3.grid(row=2, column=0, pady=10, padx=10)

        self.l4 = tk.CTkComboBox(f3,
                                 values=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                 font=('Tahoma', 20, 'bold'),
                                 command=lambda event, data=a: self.update_day(event, data),
                                 state='readonly')

        self.l4.grid(row=3, column=0, pady=10, padx=10)

        self.day_rate = tk.CTkLabel(f3,
                                    text=f"The best day is {max(days, key=days.get)} : {max(days.values())} Stars\nThe worst day is {min(days, key=days.get)} : {min(days.values())} Stars",
                                    text_color='#454545', font=('Tahoma', 15))

        self.day_rate.grid(row=3, column=1, pady=10, padx=10)

        self.month = tk.CTkLabel(f3,
                                 text=f"The best Month is {self.month_dict[month.index(max(month)) + 1]} : {max(month)} Stars\nThe worst Month is {self.month_dict[month.index(min(month)) + 1]} : {min(month)} Stars",
                                 text_color='#454545', font=('Tahoma', 15,))

        self.month.grid(row=2, column=1, pady=10, padx=10)

        self.strk_5 = tk.CTkLabel(f3,
                                  text=f"Longest 5 Star Streak: {long} days from {start[1] + 1}/{start[0] + 1}  to  {end[1] + 1}/{end[0] + 1}",
                                  text_color='#454545', font=('Tahoma', 15,))

        self.week = tk.CTkLabel(f3,
                                text=f"The best Week is Week {weeks.index(max(weeks)) + 1} : {max(weeks)} Stars\nThe worst Week is Week {weeks.index(min(weeks)) + 1} : {min(weeks)} Stars",
                                text_color='#454545', font=('Tahoma', 15,))

        self.week.grid(row=1, column=1, pady=10, padx=10)

        sidebar = tk.CTkFrame(self.stats, fg_color='#23556b', bg_color='#23556b')
        self.strk_5.grid(row=0, column=1, pady=(200, 10), padx=10)

        chart_canvas = FigureCanvasTkAgg(fig, sidebar)
        chart_canvas.get_tk_widget().pack(side=tk.LEFT)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        f2.pack(side=tk.BOTTOM)
        f3.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        chart_canvas.draw()
        self.stats.pack(fill=tk.BOTH, expand=True)

    def stats_moods(self):
        self.stats.pack_forget()
        self.page2.pack_forget()
        self.stats = tk.CTkFrame(self.root)
        self.stats.configure(fg_color='#f7e8d5', bg_color='#f7e8d5')

        self.root.title("Statistics")
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#23556b')

        mood_map = {
            '#ff69b4': 'Depressed',
            '#ffb4b4': 'Sad',
            '#fcf6bd': 'Neutral',
            '#ffdc5e': 'Happy',
            '#ff9900': 'Excited'}

        self.rate_dict = {'#ff69b4': 1, '#ffb4b4': 2, '#fcf6bd': 3, '#ffdc5e': 4, '#ff9900': 5}

        temp = {'Depressed': '#ff69b4', 'Sad': '#ffb4b4', 'Neutral': '#fcf6bd', 'Happy': '#ffdc5e',
                'Excited': '#ff9900'}

        Moods = {key: 0 for key in mood_map.values()}
        b = self.db.get_year_moods()

        self.chart_data(b, Moods, mood_map)
        self.draw_pie_chart(ax, Moods, mood_map.keys(), 'Moods')

        f = tk.CTkFrame(self.stats, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f2 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f3 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')

        long, start, end = self.streak_counter(b, '#ff9900')
        self.l1 = tk.CTkComboBox(f3, values=['Depressed', 'Sad', 'Neutral', 'Happy', 'Excited'],
                                 font=('Tahoma', 25, 'bold'),
                                 command=lambda event, t=temp, data=b: self.update_streak(event, t, data),
                                 state='readonly')

        self.l1.grid(row=0, column=0, pady=(200, 10), padx=10)

        self.strk_5 = tk.CTkLabel(f3,
                                  text=f"Longest Excited Streak: {long} days from {start[1] + 1}/{start[0] + 1}  to  {end[1] + 1}/{end[0] + 1}",
                                  text_color='#454545', font=('Tahoma', 15,))

        self.strk_5.grid(row=0, column=1, pady=(200, 10), padx=10)

        weeks = self.week_avg(b, self.rate_dict)
        values = [str(i + 1) for i in range(len(weeks))]

        self.l2 = tk.CTkComboBox(f3, values=values, font=('Tahoma', 25, 'bold'),
                                 command=lambda event, data=b: self.update_week(event, data), state='readonly')

        self.l2.grid(row=1, column=0, pady=10, padx=10)

        self.week = tk.CTkLabel(f3,
                                text=f"The best Week is Week {weeks.index(max(weeks)) + 1} : Average Rate: {max(weeks)}\nThe worst Week is Week {weeks.index(min(weeks)) + 1} : Average Rate: {min(weeks)}",
                                text_color='#454545', font=('Tahoma', 15,))

        self.week.grid(row=1, column=1, pady=10, padx=10)

        month = self.month_avg(b, self.rate_dict)

        values = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

        self.l3 = tk.CTkComboBox(f3, values=values[:len(month)], font=('Tahoma', 20, 'bold'),
                                 command=lambda event, data=b: self.update_month(event, data), state='readonly')

        self.l3.grid(row=2, column=0, pady=10, padx=10)

        self.month = tk.CTkLabel(f3,
                                 text=f"The best Month is {self.month_dict[month.index(max(month)) + 1]} : Average Rate: {max(month)}\nThe worst Month is {self.month_dict[month.index(min(month)) + 1]} : Average Rate: {min(month)}",
                                 text_color='#454545', font=('Tahoma', 15,))

        self.month.grid(row=2, column=1, pady=10, padx=10)

        days = self.day_avg(b, self.rate_dict)
        self.l4 = tk.CTkComboBox(f3,
                                 values=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                 font=('Tahoma', 20, 'bold'),
                                 command=lambda event, data=b: self.update_day(event, data), state='readonly')

        self.l4.grid(row=3, column=0, pady=10, padx=10)

        self.day_rate = tk.CTkLabel(f3,
                                    text=f"The best day is {max(days, key=days.get)} : Average Rate: {max(days.values())}\nThe worst day is {min(days, key=days.get)} : Average Rate: {min(days.values())}",
                                    text_color='#454545', font=('Tahoma', 15,))

        self.day_rate.grid(row=3, column=1, pady=10, padx=10)

        self.nextS = tk.CTkButton(f2, text='Next', fg_color='#454545', font=('Tahoma', 20, 'bold'), width=150
                                  , command=lambda: self.stats_sleep())
        self.backS = tk.CTkButton(f2, text='Back', fg_color='#454545', font=('Tahoma', 20, 'bold'), width=150
                                  , command=lambda: [self.stats.pack_forget(), self.stats_rate()])

        self.nextS.grid(row=0, column=1, pady=20, padx=20)
        self.backS.grid(row=0, column=0, pady=20, padx=20)

        sidebar = tk.CTkFrame(self.stats, fg_color='#23556b', bg_color='#23556b')
        chart_canvas = FigureCanvasTkAgg(fig, sidebar)
        chart_canvas.get_tk_widget().pack(side=tk.LEFT)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        f2.pack(side=tk.BOTTOM)
        f3.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        chart_canvas.draw()
        self.stats.pack(fill=tk.BOTH, expand=True)

    def stats_sleep(self):
        self.stats.pack_forget()
        self.page2.pack_forget()
        self.stats = tk.CTkFrame(self.root)
        self.stats.configure(fg_color='#f7e8d5', bg_color='#f7e8d5')

        self.root.title("Statistics")
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#23556b')

        sleep_map = {
            '#D4B0FF': '1-2 Hours',
            '#C8A2C8': '3-5 Hours',
            '#9B59B6': '6-8 Hours',
            '#6A0DAD': '9-11 Hours',
            '#3D0C6B': '12+ Hours'
        }

        Sleep = {key: 0 for key in sleep_map.values()}
        self.rate_dict = {'#D4B0FF': 1.5, '#C8A2C8': 4, '#9B59B6': 7, '#6A0DAD': 10, '#3D0C6B': 12}

        temp = {'1-2 Hours': '#D4B0FF', '3-5 Hours': '#C8A2C8', '6-8 Hours': '#9B59B6',
                '9-11 Hours': '#6A0DAD', '12+ Hours': '#3D0C6B'}

        c = self.db.get_year_sleep()
        self.chart_data(c, Sleep, sleep_map)
        self.draw_pie_chart(ax, Sleep, sleep_map.keys(), 'Sleep')

        f = tk.CTkFrame(self.stats, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f2 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f3 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')

        long, start, end = self.streak_counter(c, '#3D0C6B')
        self.l1 = tk.CTkComboBox(f3, values=['1-2 Hours', '3-5 Hours', '6-8 Hours', '9-11 Hours', '12+ Hours'],
                                 font=('Tahoma', 25, 'bold'),
                                 command=lambda event, t=temp, data=c: self.update_streak(event, t, data),
                                 state='readonly')

        self.l1.grid(row=0, column=0, pady=(200, 10), padx=10)

        self.strk_5 = tk.CTkLabel(f3,
                                  text=f"Longest 12+ Hours Streak: {long} days from {start[1] + 1}/{start[0] + 1}  to  {end[1] + 1}/{end[0] + 1}",
                                  text_color='#454545', font=('Tahoma', 15,))

        self.strk_5.grid(row=0, column=1, pady=(200, 10), padx=10)

        weeks = self.week_avg(c, self.rate_dict)
        values = [str(i + 1) for i in range(len(weeks))]

        self.l2 = tk.CTkComboBox(f3, values=values, font=('Tahoma', 25, 'bold'),
                                 command=lambda event, data=c: self.update_week(event, data),
                                 state='readonly')

        self.l2.grid(row=1, column=0, pady=10, padx=10)

        self.week = tk.CTkLabel(f3,
                                text=f"The best Week is Week {weeks.index(max(weeks)) + 1} : Average Sleep: {max(weeks)} Hours\nThe worst Week is Week {weeks.index(min(weeks)) + 1} : Average Sleep: {min(weeks)} Hours",
                                text_color='#454545', font=('Tahoma', 15,))

        self.week.grid(row=1, column=1, pady=10, padx=10)

        month = self.month_avg(c, self.rate_dict)

        values = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

        self.l3 = tk.CTkComboBox(f3, values=values[:len(month)], font=('Tahoma', 20, 'bold'),
                                           command=lambda event, data=c: self.update_month(event, data),
                                           state='readonly')

        self.l3.grid(row=2, column=0, pady=10, padx=10)

        self.month = tk.CTkLabel(f3,
                                 text=f"The best Month is {self.month_dict[month.index(max(month)) + 1]} : Average Sleep: {max(month)} Hours\nThe worst Month is {self.month_dict[month.index(min(month)) + 1]} : Average Sleep: {min(month)} Hours",
                                 text_color='#454545', font=('Tahoma', 15,))

        self.month.grid(row=2, column=1, pady=10, padx=10)

        days = self.day_avg(c, self.rate_dict)
        self.l4 = tk.CTkComboBox(f3,
                                 values=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                 font=('Tahoma', 20, 'bold'),
                                 command=lambda event, data=c: self.update_day(event, data), state='readonly')

        self.l4.grid(row=3, column=0, pady=10, padx=10)

        self.day_rate = tk.CTkLabel(f3,
                                    text=f"The best day is {max(days, key=days.get)} : Average Sleep: {max(days.values())} Hours\nThe worst day is {min(days, key=days.get)} : Average Sleep: {min(days.values())} Hours",
                                    text_color='#454545', font=('Tahoma', 15,))

        self.day_rate.grid(row=3, column=1, pady=10, padx=10)

        self.nextS = tk.CTkButton(f2, text='Next', fg_color='#454545', font=('Tahoma', 20, 'bold'), width=150,
                                  command=lambda: self.stats_dreams())
        self.backS = tk.CTkButton(f2, text='Back', fg_color='#454545', font=('Tahoma', 20, 'bold'), width=150,
                                  command=lambda: self.stats_moods())

        self.nextS.grid(row=0, column=1, pady=20, padx=20)
        self.backS.grid(row=0, column=0, pady=20, padx=20)

        sidebar = tk.CTkFrame(self.stats, fg_color='#23556b', bg_color='#23556b')
        chart_canvas = FigureCanvasTkAgg(fig, sidebar)
        chart_canvas.get_tk_widget().pack(side=tk.LEFT)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        f2.pack(side=tk.BOTTOM)
        f3.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        chart_canvas.draw()
        self.stats.pack(fill=tk.BOTH, expand=True)

    def stats_dreams(self):
        self.stats.pack_forget()
        self.page2.pack_forget()
        self.stats = tk.CTkFrame(self.root)
        self.stats.configure(fg_color='#f7e8d5', bg_color='#f7e8d5')

        self.root.title("Statistics")
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.patch.set_facecolor('#23556b')

        dream_map = {
            '#E7E6F7': 'can\'t remember',
            '#FDC5F5': 'Happy',
            '#A6E3E9': 'Sad',
            '#FFB347': 'Weird',
            '#4B4453': 'Scary'
        }

        self.rate_dict = {'#E7E6F7':0, '#FDC5F5': 1, '#A6E3E9': 1, '#FFB347': 1, '#4B4453': 1}

        Dream = {key: 0 for key in dream_map.values()}
        d = self.db.get_year_dream()

        self.chart_data(d, Dream, dream_map)
        self.draw_pie_chart(ax, Dream, dream_map.keys(), 'Dreams')

        temp = {'can\'t remember': '#E7E6F7', 'Happy': '#FDC5F5', 'Sad': '#A6E3E9', 'Weird': '#FFB347',
                'Scary': '#4B4453'}

        f = tk.CTkFrame(self.stats, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f2 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')
        f3 = tk.CTkFrame(f, fg_color='#f7e8d5', bg_color='#f7e8d5')

        long, start, end = self.streak_counter(d, '#4B4453')

        self.l1 = tk.CTkComboBox(f3, values=['can\'t remember', 'Happy', 'Sad', 'Weird', 'Scary'],
                                 font=('Tahoma', 25, 'bold'),
                                 command=lambda event, t=temp, data=d: self.update_streak(event, t, data),
                                 state='readonly')

        self.l1.grid(row=0, column=0, pady=(200, 10), padx=10)

        self.strk_5 = tk.CTkLabel(f3,
                                  text=f"Longest Scary Streak: {long} days from {start[1] + 1}/{start[0] + 1}  to  {end[1] + 1}/{end[0] + 1}",
                                  text_color='#454545', font=('Tahoma', 15,))

        self.strk_5.grid(row=0, column=1, pady=(200, 10), padx=10)

        weeks = self.week_avg(d, self.rate_dict)
        values = [str(i + 1) for i in range(len(weeks))]

        self.l2 = tk.CTkComboBox(f3, values=values, font=('Tahoma', 25, 'bold'),
                                 command=lambda event, data=d: self.update_week(event, data),
                                 state='readonly')

        self.l2.grid(row=1, column=0, pady=10, padx=10)

        self.week = tk.CTkLabel(f3,text=f"You had the most dreams in Week {weeks.index(max(weeks))} "
                                        f": {max(weeks)} Times\nYou had the least dreams in Week {weeks.index(min(weeks))} : {min(weeks)} Times",
                                text_color='#454545', font=('Tahoma', 15,))

        self.week.grid(row=1, column=1, pady=10, padx=10)

        month = self.month_avg(d, self.rate_dict)

        values = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

        self.l3 = tk.CTkComboBox(f3, values=values[:len(month)], font=('Tahoma', 20, 'bold'),
                                 command=lambda event, data=d: self.update_month(event, data),
                                 state='readonly')

        self.l3.grid(row=2, column=0, pady=10, padx=10)

        text=self.month_Count(d,'January')

        self.month = tk.CTkLabel(f3,text=text,text_color='#454545', font=('Tahoma', 15,))

        self.month.grid(row=2, column=1, pady=10, padx=10)

        days = self.day_count()

        self.l4 = tk.CTkComboBox(f3,
                                 values=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                 font=('Tahoma', 20, 'bold'),
                                 command=lambda event, data=d: self.update_day(event, data), state='readonly')

        self.l4.grid(row=3, column=0, pady=10, padx=10)

        self.day_rate = tk.CTkLabel(f3, text=f"Your dreams for Monday are {days['Monday']}",
                                    text_color='#454545', font=('Tahoma', 15,))

        self.day_rate.grid(row=3, column=1, pady=10, padx=10)


        self.backS = tk.CTkButton(f2, text='Back', fg_color='#454545', font=('Tahoma', 20, 'bold'), width=150,
                                  command=lambda: [self.stats_sleep()])


        self.backS.pack(side=tk.BOTTOM, pady=20)

        sidebar = tk.CTkFrame(self.stats, fg_color='#23556b', bg_color='#23556b')
        chart_canvas = FigureCanvasTkAgg(fig, sidebar)
        chart_canvas.get_tk_widget().pack(side=tk.LEFT)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        f.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        f2.pack(side=tk.BOTTOM)
        f3.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        chart_canvas.draw()
        self.stats.pack(fill=tk.BOTH, expand=True)

    def selected(self, x, y):
        if y != 0:
            if self.year_colors[x][y - 1] == 'gray':
                messagebox.showerror("Error", "Please select a color for the previous cells first")
                return

        elif y == 0 and x != 0:
            if self.year_colors[x - 1][-1] == 'gray':
                messagebox.showerror("Error", "Please select a color for the previous cells first")
                return

            if self.year_colors[x - 1][-1] == 'black':
                for i in range(len(self.year_colors[x - 1])):
                    if self.year_colors[x - 1][i] == 'black':
                        if self.year_colors[x - 1][i - 1] == 'gray':
                            messagebox.showerror("Error", "Please select a color for the previous cells first")
                            return

        self.Bs[x][y].configure(fg_color=self.colors_options[self.colors.get()])
        self.year_colors[x][y] = self.colors_options[self.colors.get()]

        if self.p2:
            self.add_note(f"{y + 1}/{x + 1}")
            self.db.set_notes(self.notes, self.db.username)
            self.db.set_year_rate(self.year_colors, self.db.username)
        elif self.p3:
            self.db.set_year_moods(self.year_colors, self.db.username)
        elif self.p4:
            self.db.set_year_sleep(self.year_colors, self.db.username)
        elif self.p5:
            self.add_dream(f"{y + 1}/{x + 1}")
            self.db.set_notes(self.notes, self.db.username)
            self.db.set_year_dream(self.year_colors, self.db.username)

    def login(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        if self.db.get_user_info(self.username, self.password):
            self.page1.pack_forget()
            self.Rate_table()
            self.mainPage()

    def signup(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        if self.db.set_user_info(self.username, self.password):
            self.page1.pack_forget()
            self.Rate_table()
            self.mainPage()


GuiJournal()
