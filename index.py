import cv2
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
import speech_recognition as sr
import numpy as np

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the desired female voice ID (replace with the actual ID from the list)
desired_female_voice_id = 'address of voice zira '
engine.setProperty('voice', desired_female_voice_id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("Sorry, sir ?")
        return "None"
    return query

def send_email(receiver_email, subject, body):
    sender_email = "your_email@gmail.com"
    password = "your_password"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{body}")
    server.quit()

def get_weather(city):
    api_key = "your_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_info = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather_info} with a temperature of {temp} degrees Celsius."
    else:
        return "Sorry, I couldn't fetch the weather information right now."

def get_battery_percentage():
    if os.name == 'nt':  # Windows
        import psutil
        battery = psutil.sensors_battery()
        if battery is not None:
            return f"Battery: {battery.percent}%"
        else:
            return "Battery info not available"
    else:
        return "Battery info not supported on this OS"

def overlay_text(frame, text, position, font_size=20, color=(255, 255, 255)):
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def play_video():
    global video_source, video_panel, root, update_frame_flag
    video_path = r''         #video of addres play on the background after run the jarvis
    video_source = cv2.VideoCapture(video_path)
    update_frame_flag = True

    if not video_source.isOpened():
        print("Error: Unable to open video file.")
        return

    def update_frame():
        if update_frame_flag:
            ret, frame = video_source.read()
            if ret:
                now = datetime.datetime.now()
                time_str = now.strftime("%H:%M:%S")
                date_str = now.strftime("%Y-%m-%d")
                battery_str = get_battery_percentage()
                frame = overlay_text(frame, f"Time: {time_str}", (10, 10))
                frame = overlay_text(frame, f"Date: {date_str}", (10, 40))
                frame = overlay_text(frame, battery_str, (10, 70))
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(img)
                video_panel.config(image=img)
                video_panel.image = img
            else:
                video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)
            root.after(10, update_frame)

    update_frame()
    
def assistant():
    speak("Hello! I'm Lara. How can I assist you today?")
    while True:
        query = listen().lower()

        if query == "none":
            continue

        response = ""
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)
                speak("Thank you! How else can I assist you today?")
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Too many results for {query}. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak(f"Sorry, I couldn't find any information for {query}.")
            continue


        if "hello" in query:
            response = "Hi there! How can I help?"
        elif "hai lara good morning" in query:
            response = "Good morning, sir!"
        elif "good morning" in query:
            response = "Good morning!"
        elif "love you" in query:
            response = "I love you too!"
        elif "can you hear me" in query:
            response = "Yes, sir."
        elif "who are you" in query:
            response = "I'm Lara, your personal assistant!"
        elif "how are you" in query:
            response = "I'm doing great, thank you!"
        elif "thank you" in query:
            response = "You're welcome! Feel free to ask if you need anything else."

        # music
        elif 'play music' in query:
            music_dir = r'D:\II\AI/PROJECT\music'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found in the directory.")
        elif 'play video' in query:
            video_dir = r'D:\II\AI\PROJECT\video'
            videos = os.listdir(video_dir)
            if videos:
                os.startfile(os.path.join(video_dir, videos[0]))
            else:
                speak("No video files found in the directory.")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            response = "Opening YouTube."

        elif 'open code' in query:
            codePath = "C:\\Users\\Haris\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif "what time is it" in query or "time" in query:
            time = datetime.datetime.now().strftime("%H:%M")
            response = f"It's {time} right now."
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            response = "Opening Google."
        elif "search for" in query:
            search_query = query.replace("search for", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            response = f"Searching for {search_query}."
        elif "send email" in query:
            try:
                speak("What should I say in the email?")
                email_body = listen()
                speak("Who is the receiver?")
                receiver_email = input("Receiver's Email: ")
                send_email(receiver_email, "Subject", email_body)
                response = "Email has been sent successfully!"
            except Exception as e:
                print(e)
                response = "Sorry, I couldn't send the email. Please try again."
        elif "weather in" in query:
            city = query.split("weather in")[1].strip()
            response = get_weather(city)
        elif "exit" in query or "bye" in query or "close" in query or "band ho ja" in query:
            response = "Goodbye! Have a great day!"
            speak(response)
            break
        else:
            response = "I'm sorry, I didn't understand that. Can you please repeat or ask something else?"

        speak(response)

def start_assistant():
    global update_frame_flag
    update_frame_flag = False
    assistant()

    
def show_gui():
    global root, video_panel

    # Initialize the GUI
    root = tk.Tk()
    root.title("Python Voice Assistant")
    root.attributes('-fullscreen', True)
    root.configure(bg="black")

    # Create and pack the video panel
    video_panel = tk.Label(root)
    video_panel.pack(fill=tk.BOTH, expand=True)

    # Start playing the video
    play_video()

    # Create a frame for the buttons
    button_frame = tk.Frame(root, bg=root.cget("bg"))
    button_frame.place(relx=1.0, rely=0.0, anchor=tk.NE, x=-10, y=10)  # Place frame at the top-right corner

    # Add the "Exit" button
    btn_exit = tk.Button(button_frame, text="Exit", command=root.quit, font=("Arial", 16), fg="red", activebackground="#b71c1c", activeforeground="white")
    btn_exit.pack()

    # Call the assistant function after a short delay
    root.after(1000, assistant)  # 1000 ms delay to ensure the GUI is fully rendered before starting the assistant

    # Start the GUI event loop
    root.mainloop()
if __name__ == "__main__":
    show_gui()

