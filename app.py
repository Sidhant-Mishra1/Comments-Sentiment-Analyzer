import tkinter as tk
from tkinter import ttk
import threading
from youtube_comment import *  # Make sure this is correctly imported
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller

        # Centering the contents of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a label for instructions
        label = tk.Label(self, text="Enter the site link", font=("Arial", 25))
        label.grid(column=0, row=0, pady=20, padx=20, sticky="n")

        # Create an entry field for user input
        self.ip_entry = tk.Entry(self, width=50, font=("Arial", 20))
        self.ip_entry.grid(column=0, row=1, pady=10, padx=20, sticky="n")

        # Create an Enter button
        enter_button = tk.Button(self, text="Enter", font=("Arial", 15), command=self.go_to_second_page)
        enter_button.grid(column=0, row=2, pady=20, padx=20)

        # Loading label
        self.loading_label = tk.Label(self, text="Processing...", font=("Arial", 15), fg="blue")
        self.loading_label.grid(column=0, row=3, pady=20, padx=20)
        self.loading_label.grid_forget()  # Hide initially

    def go_to_second_page(self):
        self.loading_label.grid()  # Show loading label

        # Start a thread to handle the data processing
        threading.Thread(target=self.process_data, daemon=True).start()
    
    def process_data(self):
        ip_address = self.ip_entry.get()
        val = main(ip_address)
        self.after(0, self.handle_result, val)  # Update GUI after processing is done

    def handle_result(self, val):
        self.loading_label.grid_forget()  # Hide loading label
        if val == "Invalid YouTube URL":
            self.controller.show_frame(ThirdPage)
        else:
            self.controller.set_dict(val)
            self.controller.show_frame(SecondPage)

        
class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller

        # Centering the contents of the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a label to display the invalid link message
        label = tk.Label(self, text="The entered link is Invalid!", font=("Arial", 20), fg="red")
        label.grid(column=0, row=0, pady=20, padx=20, sticky="n")

        # Create a button to navigate back to the first page
        enter_button = tk.Button(self, text="First Page", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        enter_button.grid(column=0, row=1, pady=20, padx=20)

        # Optional: You might want to center the button horizontally
        # self.grid_columnconfigure(0, weight=1)


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)  # Label row
        self.grid_rowconfigure(1, weight=10)  # Graphs row
        self.grid_rowconfigure(2, weight=1)  # Button row
        self.grid_columnconfigure(0, weight=1)  # Center column

        # Label to display messages
        self.label = tk.Label(self, text="", font=("Arial", 14))
        self.label.grid(column=0, row=0, pady=10, sticky="n")

        # Create a figure and a grid layout for plotting
        self.figure = plt.Figure(figsize=(12, 6), dpi=100)
        self.ax_bar = self.figure.add_subplot(121)  # Bar graph subplot
        self.ax_pie = self.figure.add_subplot(122)  # Pie chart subplot
        
        # Create canvas for matplotlib
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        
        # Back button
        back_button = tk.Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        back_button.grid(column=0, row=2, pady=20, padx=20, sticky="s")

    def update_label(self):
        val = self.controller.get_dict()
        self.update_bar_graph(val)
        self.update_pie_chart(val)
        self.canvas.draw()  # Redraw the canvas
    
    def update_bar_graph(self, prediction_dict):
        categories = ['Positive', 'Neutral', 'Sarcastic', 'Negative']
        values = [prediction_dict['Positive'], 
                  prediction_dict['Neutral'], prediction_dict['Sarcastic'], 
                  prediction_dict['Negative']]
        colors = ['#05FF36', '#87F0FF', '#FF6E0F', '#FF0000']
        
        self.ax_bar.clear()
        bars = self.ax_bar.bar(categories, values, color=colors)
        
        for bar in bars:
            height = bar.get_height()
            self.ax_bar.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', 
                             ha='center', va='bottom', fontsize=10)
        
        self.ax_bar.set_title('Comment Stats (Bar Graph)')
        self.ax_bar.set_xlabel('Sentiment')
        self.ax_bar.set_ylabel('No. of comments')
    
    def update_pie_chart(self, prediction_dict):
        labels = ['Positive', 'Neutral', 'Sarcastic', 'Negative']
        sizes = [prediction_dict['Positive'], 
                  prediction_dict['Neutral'], prediction_dict['Sarcastic'], 
                  prediction_dict['Negative']]
        colors = ['#05FF36', '#87F0FF', '#FF6E0F', '#FF0000']
        explode = (0, 0, 0, 0)  # explode the 1st slice

        self.ax_pie.clear()
        self.ax_pie.pie(sizes, explode=explode, labels=labels, colors=colors,
                        autopct='%1.1f%%', shadow=True, startangle=140)
        self.ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.geometry("1100x600")
        
        #  Creating a window
        window = tk.Frame(self)
        window.pack(fill='both', expand=True)
        
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.dict = {}  # Initialize the dict variable
        
        for F in (FirstPage, SecondPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(FirstPage)
    
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if isinstance(frame, SecondPage):
            frame.update_label()  # Update the label when showing the SecondPage

    def set_dict(self, dict):
        self.dict = dict

    def get_dict(self):
        return self.dict

app = Application()
app.title("Comment-Sentiment Analyzer")
app.maxsize(1920,1080)
app.mainloop()
