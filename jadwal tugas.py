import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class Task:
    def __init__(self, name, deadline, difficulty_rate, duration, schedule_date=None):
        self.name = name
        self.deadline = deadline
        self.difficulty_rate = difficulty_rate
        self.duration = duration
        self.schedule_date = schedule_date

def schedule_tasks(tasks):
    tasks.sort(key=lambda x: (x.deadline, -x.difficulty_rate, -x.duration))

    current_date = datetime.datetime.now()

    tasks_today = []

    for task in tasks:
        max_schedule_date = task.deadline - datetime.timedelta(days=3)

        if current_date > task.deadline:
            task.schedule_date = "Deadline telah lewat"
        elif current_date <= max_schedule_date or current_date <= task.deadline:
            if current_date == task.deadline:
                if task.duration > tasks_today[0].duration:
                    tasks_today = [task]
                    task.schedule_date = current_date
                elif task.duration == tasks_today[0].duration and task.difficulty_rate > tasks_today[0].difficulty_rate:
                    tasks_today = [task]
                    task.schedule_date = current_date
            else:
                task.schedule_date = current_date
                tasks_today = [task]

        else:
            task.schedule_date = max_schedule_date

        current_date += datetime.timedelta(days=1)

    return tasks

def update_schedule():
    scheduled_tasks = schedule_tasks(tasks)
    result_table.delete(*result_table.get_children())

    for task in scheduled_tasks:
        if task.schedule_date == "Deadline telah lewat":
            status = task.schedule_date
            scheduled_date = ""
        else:
            status = task.deadline.strftime('%Y-%m-%d')
            scheduled_date = task.schedule_date.strftime('%Y-%m-%d')

        values = (task.name, scheduled_date, status, task.difficulty_rate, task.duration)
        result_table.insert("", "end", values=values)

        # Menandai baris yang memiliki deadline lewat dengan warna merah
        if task.schedule_date == "Deadline telah lewat":
            result_table.tag_configure('red_tag', background='red')
            result_table.tag_add('red_tag', 'end-1c', 'end')

def add_new_task():
    try:
        name = entry_name.get()
        deadline_str = entry_deadline.get()
        deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d')
        difficulty_rate = int(entry_difficulty_rate.get())
        duration = int(entry_duration.get())

        task = Task(name, deadline, difficulty_rate, duration)
        tasks.append(task)

        update_schedule()

        # Reset isian formulir
        entry_name.delete(0, tk.END)
        entry_deadline.delete(0, tk.END)
        entry_difficulty_rate.delete(0, tk.END)
        entry_duration.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")

# Buat GUI
root = tk.Tk()
root.title("Jadwal Tugas")
root.configure(bg='#d1cfe2')  # Warna latar belakang UI (biru muda)

# Label dan Entry untuk input tugas
label_name = tk.Label(root, text="Nama Tugas:", bg='#d1cfe2')  # Warna latar belakang Label
entry_name = tk.Entry(root, bg='#d1cfe2')  # Warna latar belakang Entry

label_deadline = tk.Label(root, text="Deadline (format YYYY-MM-DD):", bg='#d1cfe2')
entry_deadline = tk.Entry(root, bg='#d1cfe2')

label_difficulty_rate = tk.Label(root, text="Rate Kesulitan (1-10):", bg='#d1cfe2')
entry_difficulty_rate = tk.Entry(root, bg='#d1cfe2')

label_duration = tk.Label(root, text="Lama Pengerjaan (dalam menit):", bg='#d1cfe2')
entry_duration = tk.Entry(root, bg='#d1cfe2')

new_task_button = tk.Button(root, text="Tambah Tugas Baru", command=add_new_task, bg='#9cadce', fg='white')  # Warna latar belakang dan teks Button

# Tabel untuk menampilkan hasil jadwal
result_table = ttk.Treeview(root, columns=("Nama Tugas", "Tanggal Pengerjaan", "Deadline", "Rate Kesulitan", "Durasi"), show='headings', selectmode='browse')
result_table.heading("Nama Tugas", text="Nama Tugas")
result_table.heading("Tanggal Pengerjaan", text="Tanggal Pengerjaan")
result_table.heading("Deadline", text="Deadline")
result_table.heading("Rate Kesulitan", text="Rate Kesulitan")
result_table.heading("Durasi", text="Durasi (menit)")
result_table["displaycolumns"] = (0, 1, 2, 3, 4)  # Menentukan kolom yang akan ditampilkan

result_table.pack()

# Tampilkan GUI
label_name.pack()
entry_name.pack()
label_deadline.pack()
entry_deadline.pack()
label_difficulty_rate.pack()
entry_difficulty_rate.pack()
label_duration.pack()
entry_duration.pack()
new_task_button.pack()

tasks = []  # List untuk menyimpan tugas

# Inisialisasi jadwal awal
update_schedule()

root.mainloop()
