from datetime import timedelta, datetime
# import datetime
import os
import csv

class DiaryEntry:
    def __init__(self, date: str, content: str, filename: str = None):
        self.date = date
        self.content = content
        self.filename = filename  # to ensure each entry knows which file it belongs to or should be saved to + easier to perform operations w/out needing to pass filename seperately

class DiaryManager(DiaryEntry):
    def __init__(self, date=None, content=None):
        super().__init__(date, content)
        # self.entries = []

    def add_entry(self, entry: DiaryEntry):
        if isinstance(entry, DiaryEntry):
            # self.entries.append(entry)
            # if entry.filename:

            if os.path.exists(f"file/{entry.filename}"):  # ensures you are editing an existing file w a defined filename (that isnt blank or None)
                print("File exists")
                with open(entry.filename, 'w') as f:
                    f.writelines([entry.date + '\n', 'DiaryEntry\n', entry.content])

                def convert_txt_to_csv(txt_file, csv_file):
                    with open(txt_file, 'r') as txt:
                        with open(f"{csv_file}.csv", 'w', newline='') as csv_f:
                            var = txt.readlines()
                            csv_writer = csv.writer(csv_f)
                            csv_writer.writerow([var[0].strip('\n'), var[1].strip('\n'), var[2].strip('\n')])

                convert_txt_to_csv(f"{entry.filename}", f"{entry.filename}")
                # with open("file_list.txt", 'r') as f:
                #     file_list = f.readlines()
                #     for i in file_list:
                #         if entry.filename == i.strip('\n'):
                #             break

            else:
                with open(entry.filename, 'w') as f:
                    f.writelines([entry.date + '\n', 'DiaryEntry\n', entry.content])
                with open("file_list.txt", 'a') as f:
                    f.write(entry.filename + '\n')

                    def convert_txt_to_csv(txt_file, csv_file):
                        with open(txt_file, 'r') as txt:
                            with open(f"{csv_file}.csv", 'w', newline='') as csv_f:
                                var = txt.readlines()
                                csv_writer = csv.writer(csv_f)
                                csv_writer.writerow([var[0].strip('\n'), var[1].strip('\n'), var[2].strip('\n')])

                    convert_txt_to_csv(f"{entry.filename}", f"{entry.filename}")
                    #     f.seek(0)
                    #     file_list = f.readlines()
                    #     for i in file_list:
                    #         if entry.filename == i.strip('\n'):
                    #             break
                    #     else:


            os.replace(f"{entry.filename}", f"file/{entry.filename}")
            os.replace(f"{entry.filename}.csv", f"csv_files/{entry.filename}.csv")

    def search_entries(self, keyword=None):
        results = []
        with open("file_list.txt", 'r') as f:
            lst = f.readlines()
        if keyword is not None:
            for entry in lst:
                if keyword.lower() in entry.lower():
                    results.append(entry)
        else:
            for entry in lst:
                results.append(entry)
        # for entry in self.entries:
        #     if keyword.lower() in entry.content.lower():
        #         results.append(entry)
        return results

    def filter_entries(self, start_date=None, end_date=None, type_ent=None, mood=None):
        filtered_entries = []  # self.entries
        # Filter by date range if both start and end dates are provided
        with open("file_list.txt", 'r') as f:
            file_list = f.readlines()
            if start_date:
                # start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                filtered_entries = [name for name in file_list if name.split()[0] >= start_date]

            if end_date:
                # end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                filtered_entries = [name for name in file_list if name.split()[0] <= end_date]

            # Filter by tags if provided
            # if mood:
            #     filtered_entries = [entry for entry in filtered_entries if any(tag in entry.tags for tag in tags)]
            #
            # # Filter by keyword in content if provided
            if type_ent == 'Daily Reflection':
                filtered_entries = [name for name in file_list if name.split()[2] == 'DailyReflection']
            elif type_ent == 'Event Note':
                filtered_entries = [name for name in file_list if name.split()[2] == 'EventNote']

        return filtered_entries

    def summarize(self):
        pass


def folder_path(folder):  # Loop through each file present in the folder
    txt_files = []
    for i in folder.readlines():
        txt_files.append(i.strip('\n'))
    return txt_files


def txt_open(file):  # To separate and return all the dates from the files
    dates = []
    for i in file:
        dates.append(i.split()[0])  # Assuming the date is in the first column

    return dates


def min_date(list_Dates):  # To get the min of all dates
    valid_dates = []
    for date in list_Dates:
        try:
            valid_dates.append(datetime.strptime(date, '%Y-%m-%d').date())
        except ValueError:
            continue
    earliest_date = min(valid_dates)
    return earliest_date


def max_date(list_Dates):  # To get the max of all dates
    valid_dates = []
    for date in list_Dates:
        try:
            valid_dates.append(datetime.strptime(date, '%Y-%m-%d').date())
        except ValueError:
            continue
    last_date = max(valid_dates)
    return last_date


def add_1month(earliest_date):  # To keep adding one month and create a file with all the dates between start and end date
    end_date = earliest_date + timedelta(days=30)
    global temp_file_month
    temp_file_month = []
    for i in files:
        log_date = i.split()[0]
        # print(log_date)
        log_date = datetime.strptime(log_date, "%Y-%m-%d").date()

        if early_date_month <= log_date < end_date:
            temp_file_month.append(i)
    return end_date


def add_1week(earliest_date):  # To keep adding a week and create a file with all the data between start and end date
    end_date = earliest_date + timedelta(days=7)
    global temp_file_week
    temp_file_week = []
    for i in files:
        log_date = i.split()[0]
        # print(log_date)
        log_date = datetime.strptime(log_date, "%Y-%m-%d").date()

        if early_date_week <= log_date < end_date:
            temp_file_week.append(i)
    return end_date


def average_mood_rating(type, file):  # Stores the average of the mood rating present in the file 'data' into the file 'report'
    global mood_log_counter_week, mood_log_counter_month
    s_week = []
    s_month = []
    if type == 'week':
        mood_log_counter_week += 1
    else:
        mood_log_counter_month += 1

    mood_log_list = []
    for i in file:
        try:
            if i.split()[2] == 'MoodLog':
                with open(f"file/{i}", 'r') as f:
                    line = f.readlines()
                    mood_log_list.append(int(line[3]))  # Adjust if mood is in another position
                    # print(mood_log_list)
        except FileNotFoundError:
            pass

    if type == "week":
        s_week.extend([mood_log_list.count(1), mood_log_list.count(2), mood_log_list.count(3), mood_log_list.count(4),
                       mood_log_list.count(5)])
        size_week.append(s_week)
        # print(size_week)
    else:
        s_month.extend([mood_log_list.count(1), mood_log_list.count(2), mood_log_list.count(3), mood_log_list.count(4),
                        mood_log_list.count(5)])
        size_month.append(s_month)


def no_of_events(type, file, counter):  # Stores the number of unique events from the file 'data' into the file 'report'
    no_of_events_set = set()
    for i in file:
        if i.split()[2] == 'EventNote':
            with open(f"file/{i}", 'r') as f:
                c = tuple(f.readlines()[2].strip('\n'),)
                no_of_events_set.add(c)
    events_count = len(no_of_events_set)
    if type == 'week':
        plot_events_week_x.append(f"last {counter} {type}")
        plot_events_week_y.append(events_count)
    else:
        plot_events_month_x.append(f"last {counter} {type}")
        plot_events_month_y.append(events_count)


def no_of_reflections(type, file,counter):  # Stores the number of unique daily_reflections from the file 'data' into the file 'report'
    no_of_reflections_set = set()
    for i in file:
        if i.split()[2] == 'DailyReflection':
            with open(f"file/{i}", 'r') as f:
                c = tuple(f.readlines()[2].strip('\n'),)
                no_of_reflections_set.add(c)
    events_count = len(no_of_reflections_set)
    if type == 'week':
        plot_daily_reflection_week_x.append(f"last {counter} {type}")
        plot_daily_reflection_week_y.append(events_count)
    else:
        plot_daily_reflection_month_x.append(f"last {counter} {type}")
        plot_daily_reflection_month_y.append(events_count)


# Example code to test everything
with open("file_list.txt", 'r') as f:
    files = folder_path(f)  # Files contains all the .txt files from the folder

temp_file_week = []
temp_file_month = []

all_dates = txt_open(files)  # This list contains all the dates
early_date_week = early_date_month = min_date(all_dates)

early_date_week_buffer = early_date_month_buffer = early_date_week

last_date = max_date(all_dates)

end_date_week = end_date_month = early_date_week

plot_daily_reflection_week_x = []
plot_daily_reflection_week_y = []

plot_daily_reflection_month_x = []
plot_daily_reflection_month_y = []

plot_events_week_x = []
plot_events_week_y = []

plot_events_month_x = []
plot_events_month_y = []

mood_log_counter_week = 0
mood_log_counter_month = 0
size_week = []
size_month = []

c = 1  # Counter for which week or month we are right now
while (end_date_week <= last_date):
    end_date_week = add_1week(early_date_week_buffer)

    average_mood_rating('week', temp_file_week)
    no_of_events('week', temp_file_week, c)
    no_of_reflections('week', temp_file_week, c)

    early_date_week_buffer = end_date_week

    c += 1

d = 1  # Counter for month
while (end_date_month <= last_date):
    end_date_month = add_1month(early_date_month_buffer)

    average_mood_rating("month", temp_file_month)
    no_of_events("month", temp_file_month, d)
    no_of_reflections("month", temp_file_month, d)

    early_date_month_buffer = end_date_month

    d += 1


class MoodLog(DiaryEntry):
    def __init__(self, date=None, content=None, filename='', mood_rating=None):
        # self.date = datetime.date(datetime.today()).isoformat()
        # self.filename = filename
        if os.path.exists(f"file/{filename}"):  # ensures you are editing an existing file w a defined filename (that isnt blank or None)
            print("File exists")
        else:
            with open("file_list.txt", 'a') as f:
                f.write(filename+'\n')
        with open(filename, "w") as f:
            self.mood_rating = mood_rating
            self.emotion_tags = content
            k = None
            if content == "sad":
                k = 2
            elif content == 'happy':
                k = 4
            elif content == 'excited':
                k = 5
            elif content == 'angry':
                k = 1
            elif content == 'neutral':
                k = 3
            f.write(date[:10] + '\n' + 'MOOD EMOTION\n' + content + '\n' + str(k))

        os.replace(f"{filename}", f"file/{filename}")

    def filter(type_ent=None):
        filtered_entries = []

        with open("file_list.txt", 'r') as f:
            file_list = f.readlines()

        if type_ent == 'Mood Log':
            filtered_entries = [name for name in file_list if name.split()[2] == 'MoodLog']

        return filtered_entries
