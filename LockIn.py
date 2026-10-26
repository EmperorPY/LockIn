# Import customtkinter — a modern wrapper around tkinter with nicer widgets
import customtkinter as ctk
# Import random so we can pick a random motivational quote
import random

# Set the whole app to dark mode (dark background, light text)
ctk.set_appearance_mode("dark")

# Create the main application window
root = ctk.CTk()
# Set the window title bar text
root.title("LockIn")

# ---- Full screen minus task bar ----
# Ask Windows (or whatever OS) how wide the screen is, in pixels
screen_width = root.winfo_screenwidth()
# Ask how tall the screen is, in pixels
screen_height = root.winfo_screenheight()
# We subtract this so the window doesn't hide behind the OS taskbar
task_bar_height = 60
# Place the window: full width, height minus taskbar, at position (0,0) = top-left
root.geometry(f"{screen_width}x{screen_height - task_bar_height}+0+0")

# ---- Timer state ----
# Work phase lasts 25 minutes = 1500 seconds
WORK_SECONDS = 25 * 60
# Rest phase lasts 5 minutes = 300 seconds
REST_SECONDS = 5 * 60
# How many seconds are left in the current countdown; starts at 25:00
remaining = WORK_SECONDS
# Which phase we're in right now: "work" or "rest"; starts as work
phase = "work"
# Whether the timer is currently counting down
running = False
# The ID returned by root.after() so we can cancel the pending tick when pausing/resetting
after_id = None

# ---- Grid: let content fill the whole window ----
# Column 0 = the timer side (left); weight=1 means it grows when the window grows
root.grid_columnconfigure(0, weight=1)
# Column 1 = the motivation side (right); also grows equally
root.grid_columnconfigure(1, weight=1)
# Row 0 = title row; weight=0 means it stays at its natural (fixed) height
root.grid_rowconfigure(0, weight=0)
# Row 1 = the big center block; weight=1 = takes all leftover vertical space
root.grid_rowconfigure(1, weight=1)
# Row 2 = footer row; fixed height
root.grid_rowconfigure(2, weight=0)

# ---- Title ----
# The big "LockIn" heading at the very top
title = ctk.CTkLabel(root, text="LockIn", font=("Helvetica", 70, "bold"))
# Put it in row 0, column 0, with some top/bottom padding
title.grid(row=0, column=0, pady=(30, 10))

# ---- Center block (holds everything else) ----
# An invisible container that holds all the timer widgets (its background is see-through)
center = ctk.CTkFrame(root, fg_color="transparent")
# Place it in row 1, column 0, and let it stretch in all directions
center.grid(row=1, column=0, sticky="nsew")
# Make its single column stretch to fill its width
center.grid_columnconfigure(0, weight=1)
# Give all 5 rows equal stretch weight so things space out vertically
for r in range(5):
    center.grid_rowconfigure(r, weight=1)

# A short descriptive paragraph about what the app does
description = ctk.CTkLabel(
    center,
    text=("LockIn is a clean, distraction-free desktop study timer. "
          "It uses the proven Pomodoro technique (25 minutes of focused work "
          "followed by a 5-minute break) to help you build concentration and avoid burnout."),
    wraplength=700,           # wrap long text at 700 pixels
    font=("Helvetica", 20),
)
# Place it in row 0 of the center frame
description.grid(row=0, column=0, pady=10)

# A label that says "Work Time" or "Rest Time" depending on the current phase
time_type = ctk.CTkLabel(center, text="Work Time", font=("Helvetica", 40))
# Row 1 of the center frame
time_type.grid(row=1, column=0, pady=10)

# The huge countdown display; starts at 25:00
time_display = ctk.CTkLabel(center, text="25:00", font=("Helvetica", 120, "bold"))
# Row 2 of the center frame
time_display.grid(row=2, column=0, pady=10)

# A frame to hold the Start and Reset buttons side-by-side
button_frame = ctk.CTkFrame(center, fg_color="transparent")
# Row 3 of the center frame
button_frame.grid(row=3, column=0, pady=20)

# The Start/Pause/Resume button — clicking it toggles the timer
start_button = ctk.CTkButton(button_frame, text="Start", width=160, height=50, text_color="black", hover_color="green", fg_color="white",
                             font=("Helvetica", 20), command=lambda: toggle())
# Pack it on the left side of the button frame
start_button.pack(side="left", padx=10)

# The Reset button — clicking it stops the timer and resets to 25:00 work
reset_button = ctk.CTkButton(button_frame, text="Reset", width=160, height=50, fg_color = "white", text_color="black", hover_color="red",
                             font=("Helvetica", 20), command=lambda: reset())
# Pack it on the left side too (after Start, so it appears on the right)
reset_button.pack(side="left", padx=10)


def fmt(seconds):
    """Format seconds as MM:SS."""
    # // is integer division → gives minutes; % gives leftover seconds
    # :02d pads with a leading zero so "5" becomes "05"
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def tick():
    """One second has passed — update the countdown."""
    # These variables are declared global because we reassign them here
    global remaining, phase, after_id
    # Subtract one second from the countdown
    remaining -= 1
    # If the countdown has reached zero (or gone below), switch phases
    if remaining <= 0:
        if phase == "work":
            # Work just ended → switch to rest
            phase = "rest"
            remaining = REST_SECONDS
            # Change the "Work Time" label to "Rest Time" and make it green
            time_type.configure(text="Rest Time", text_color="green")
        else:
            # Rest just ended → switch back to work
            phase = "work"
            remaining = WORK_SECONDS
            # Change the label back to "Work Time" and make it white
            time_type.configure(text="Work Time", text_color="white")
    # Update the on-screen countdown text
    time_display.configure(text=fmt(remaining))
    # Schedule the next tick one second from now — but only if still running
    if running:
        after_id = root.after(1000, tick)


def toggle():
    """Start/pause the timer."""
    # Declare globals because we reassign them
    global running, after_id
    if running:
        # We're currently running → PAUSE
        running = False
        # Cancel the scheduled next tick so it doesn't fire after we paused
        if after_id is not None:
            root.after_cancel(after_id)
            after_id = None
        # Change button label from "Pause" to "Resume"
        start_button.configure(text="Resume")
    else:
        # We're paused → START or RESUME
        running = True
        # Change button label from "Start"/"Resume" to "Pause"
        start_button.configure(text="Pause")
        # Schedule the first tick in 1 second (recursion handles the rest)
        after_id = root.after(1000, tick)


def reset():
    """Stop and reset to the beginning of a work phase."""
    # Declare globals because we reassign them
    global running, phase, remaining, after_id
    # Stop the timer
    running = False
    # Cancel any pending tick so it doesn't fire later
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None
    # Go back to the work phase
    phase = "work"
    # Reset the countdown to 25:00
    remaining = WORK_SECONDS
    # Reset the phase label to "Work Time" with white text
    time_type.configure(text="Work Time", text_color="white")
    # Update the big countdown display
    time_display.configure(text=fmt(remaining))
    # Change the Start button text back to "Start"
    start_button.configure(text="Start")


# ---- Footer ----
# A small gray motivational tagline at the bottom of the window
footer = ctk.CTkLabel(root, text="Focus. Break. Repeat.",
                      font=("Helvetica", 16), text_color="gray")
# Place it in the footer row (row 2)
footer.grid(row=2, column=0, pady=20)

# The right-side frame that holds the "Motivate Me!" section.
# It has a white border, very rounded corners (90px), a set width, and a huge height.
motivate_frame = ctk.CTkFrame(root, border_width=2, corner_radius=90, width=400, height=1000, border_color="white")
# Prevent its children from shrinking it (keeps the fixed 400×1000 size)
motivate_frame.propagate(False)
# Place it in row 1, column 1 (the right-side grid cell)
motivate_frame.grid(row=1, column=1, pady=20)

# A "Tired?" heading inside the motivation frame
motivative_label = ctk.CTkLabel(motivate_frame, text="Tired?", font=("Helvetica", 40))
# Pack it at the top of the frame
motivative_label.pack(pady=10)


# The big list of motivational quotes. One is picked at random when the button is clicked.
motive = [
    "You don't have to be great to start, but you have to start to be great.",
    "Small progress is still progress.",
    "The expert in anything was once a beginner.",
    "Focus on being productive instead of busy.",
    "Discipline beats motivation.",
    "One page at a time.",
    "Your future self is watching you right now through your actions.",
    "Study while others are sleeping; work while others are loafing.",
    "Don't stop when you're tired. Stop when you're done.",
    "The pain of studying is temporary; the pain of ignorance lasts forever.",
    "Every hour you study is an hour invested in yourself.",
    "Success is the sum of small efforts repeated day in and day out.",
    "You are one study session away from a better grade.",
    "Don't wish it were easier. Wish you were better.",
    "The difference between ordinary and extraordinary is that little extra.",
    "A little progress each day adds up to big results.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don't stop when you're tired. Stop when you're done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
    "Little things make big days.",
    "It's going to be hard, but hard does not mean impossible.",
    "Don't wait for opportunity. Create it.",
    "Sometimes we're tested not to show our weaknesses, but to discover our strengths.",
    "The key to success is to focus on goals, not obstacles.",
    "Dream it. Believe it. Build it.",
    "Study smarter, not harder.",
    "Your only limit is you.",
    "The secret of getting ahead is getting started.",
    "Quality is not an act, it is a habit.",
    "You don't need to be perfect. You just need to try.",
    "Every accomplishment starts with the decision to try.",
    "The future depends on what you do today.",
    "Learning never exhausts the mind.",
    "An investment in knowledge pays the best interest.",
    "Education is the most powerful weapon you can use to change the world.",
    "The beautiful thing about learning is that no one can take it away from you.",
    "Study hard, dream big.",
    "Knowledge is power.",
    "Learning is a treasure that will follow its owner everywhere.",
    "The more you learn, the more you earn.",
    "Develop a passion for learning. If you do, you will never cease to grow.",
    "Education is not preparation for life; education is life itself.",
    "The mind is not a vessel to be filled, but a fire to be kindled.",
    "Live as if you were to die tomorrow. Learn as if you were to live forever.",
    "The only way to do great work is to love what you do.",
    "Your attitude determines your direction.",
    "Believe you can and you're halfway there.",
    "The best way to predict your future is to create it.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "It always seems impossible until it's done.",
    "Don't watch the clock; do what it does. Keep going.",
    "The secret to getting ahead is getting started.",
    "You are braver than you believe, stronger than you seem, and smarter than you think.",
    "What you get by achieving your goals is not as important as what you become by achieving your goals.",
    "The only person you are destined to become is the person you decide to be.",
    "Go confidently in the direction of your dreams.",
    "You have within you right now, everything you need to deal with whatever the world can throw at you.",
    "Act as if what you do makes a difference. It does.",
    "The harder you work, the luckier you get.",
    "Success usually comes to those who are too busy to be looking for it.",
    "Opportunities don't happen. You create them.",
    "Don't be afraid to give up the good to go for the great.",
    "I find that the harder I work, the more luck I seem to have.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "The way to get started is to quit talking and begin doing.",
    "If you really look closely, most overnight successes took a long time.",
    "The road to success and the road to failure are almost exactly the same.",
    "Success is not how high you have climbed, but how you make a positive difference.",
    "Try not to become a person of success, but rather try to become a person of value.",
    "Don't let yesterday take up too much of today.",
    "You learn more from failure than from success.",
    "It's not whether you get knocked down, it's whether you get up.",
    "If you are working on something that you really care about, you don't have to be pushed.",
    "People who are crazy enough to think they can change the world are the ones who do.",
    "Failure will never overtake me if my determination to succeed is strong enough.",
    "Entrepreneurs are great at dealing with uncertainty and also very good at minimizing risk.",
    "We may encounter many defeats but we must not be defeated.",
    "Knowing is not enough; we must apply. Wishing is not enough; we must do.",
    "Imagine your life is perfect in every respect; what would it look like?",
    "We generate fears while we sit. We overcome them by action.",
    "Whether you think you can or think you can't, you're right.",
    "Security is mostly a superstition. Life is either a daring adventure or nothing.",
    "The man who has confidence in himself gains the confidence of others.",
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Creativity is intelligence having fun.",
    "What you lack in talent can be made up with desire, hustle and giving 110% all the time.",
    "Do what you can with all you have, wherever you are.",
    "You are never too old to set another goal or to dream a new dream.",
    "To see what is right and not do it is a lack of courage.",
    "Reading is to the mind what exercise is to the body.",
    "The journey of a thousand miles begins with one step.",
    "Learning is not attained by chance; it must be sought with ardor and attended with diligence.",
    "The more that you read, the more things you will know.",
    "Study the past if you would define the future.",
    "Education is the passport to the future, for tomorrow belongs to those who prepare for it today.",
    "The expert in anything was once a beginner.",
    "Every master was once a disaster.",
    "Knowledge will bring you the opportunity to make a difference.",
    "There are no shortcuts to any place worth going.",
    "Success is the result of perfection, hard work, learning from failure, loyalty, and persistence.",
    "The only place where success comes before work is in the dictionary.",
    "There are no secrets to success. It is the result of preparation, hard work, and learning from failure.",
    "I never dreamed about success. I worked for it.",
    "Opportunities are usually disguised as hard work, so most people don't recognize them.",
    "The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack of will.",
    "Success is peace of mind which is a direct result of self-satisfaction in knowing you did your best.",
    "The starting point of all achievement is desire.",
    "Success is not the key to happiness. Happiness is the key to success.",
    "If you love what you are doing, you will be successful.",
    "The only way to do great work is to love what you do.",
    "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.",
    "The people who are crazy enough to think they can change the world are the ones who do.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Our greatest glory is not in never falling, but in rising every time we fall.",
    "Perseverance is not a long race; it is many short races one after the other.",
    "The will to succeed is important, but what's more important is the will to prepare.",
    "The successful warrior is the average man, with laser-like focus.",
    "Success is the sum of small efforts, repeated day in and day out.",
    "There is no substitute for hard work.",
    "The only thing standing between you and your goal is the story you keep telling yourself.",
    "Don't let what you cannot do interfere with what you can do.",
    "The best preparation for tomorrow is doing your best today.",
    "You don't have to see the whole staircase, just take the first step.",
    "The secret of change is to focus all of your energy not on fighting the old, but on building the new.",
    "It's not about having time. It's about making time.",
    "The difference between try and triumph is a little umph.",
    "If you want to lift yourself up, lift up someone else.",
    "Do what you have always done and you'll get what you have always got.",
    "You don't get what you wish for. You get what you work for.",
    "A goal without a plan is just a wish.",
    "Motivation gets you going, but discipline keeps you growing.",
    "Nothing will work unless you do.",
    "A river cuts through rock not because of its power, but because of its persistence.",
    "You don't have to be extreme, just consistent.",
    "The best way to get things done is to simply begin.",
    "It's not about perfect. It's about effort.",
    "When you feel like quitting, think about why you started.",
    "Your speed doesn't matter, forward is forward.",
    "Focus on the journey, not the destination.",
    "You are capable of more than you know.",
    "Every study session counts.",
    "One day or day one. You decide.",
    "Don't count the days. Make the days count.",
    "The more you practice, the better you get.",
    "You didn't come this far to only come this far.",
    "The difference between who you are and who you want to be is what you do.",
    "Study with purpose, not just with pressure.",
    "Discipline is choosing between what you want now and what you want most.",
    "Your only competition is who you were yesterday.",
    "Growth begins at the end of your comfort zone.",
    "Every page you read is a step closer to success.",
    "You've survived every hard day so far. You'll survive this one too.",
    "Showing up is half the battle.",
    "Don't minimize your progress. You're doing better than you think.",
    "Be proud of yourself for showing up today.",
    "The best students aren't always the smartest; they're the most consistent.",
    "One chapter at a time, one problem at a time.",
    "You are building your future with every hour you study.",
    "There's no elevator to success. You have to take the stairs.",
    "You don't need more time. You need more focus.",
    "Study like your dreams depend on it — because they do.",
    "Your effort today is your advantage tomorrow.",
    "You are not behind. You are exactly where you need to be.",
    "Progress over perfection.",
    "If it matters to you, you'll find a way. If not, you'll find an excuse.",
    "The only bad study session is the one you didn't have.",
    "Start where you are. Use what you have. Do what you can.",
    "One focused hour beats five distracted ones.",
    "Turn your 'I have to' into 'I get to.'",
    "The work you put in when no one is watching will show when everyone is.",
    "Hard work beats talent when talent doesn't work hard.",
    "You will never always be motivated. You must learn to be disciplined.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "A small step every day leads to big results.",
    "Each session is another brick in your future.",
    "Your best is enough, as long as you give it.",
    "Be the person you want to be, starting right now.",
    "Even the smallest progress counts. Keep going.",
]

# The "Motivate Me!" button. When clicked, it updates phrase_label with a random quote.
motivate_button = ctk.CTkButton(motivate_frame, text="Motivate Me!", text_color="black", command=lambda: phrase_label.configure(text=random.choice(motive), text_color="cyan", font=("Arial", 15), wraplength=300,), fg_color="white", hover_color="cyan")
# Pack the button inside the motivation frame
motivate_button.pack(pady=10)

# A label that will display the chosen quote. Starts empty until the button is clicked.
phrase_label = ctk.CTkLabel(motivate_frame, text="")
# Pack it so it's actually visible on screen (this is essential!)
phrase_label.pack()

# Start the app's main event loop — keeps the window open and responsive
root.mainloop()