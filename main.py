# (c) 2023 Antonio Rivera
# This code is licensed under GNU General Public license (see LICENSE.txt for details)

import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from scale import major_scales, minor_scales
from fret import fretboard, notes_array, Fret

#
# (0,0) (0,1) (0,2) (0,3) (0,4) (0,5) (0,6)
# (1,0) (1,1)       (1,3) (1,4) (1,5)
#
# c     d     e     f     g     a     b
# c#    d#          f#    g#    a#
#

key_selected = "n/a"
quality_selected = "n/a"
scale_selected = "n/a"
name = "n/a and n/a"
major = False
image_path = "images/Fretboard.png"
current_image_label = None
current_image = None


def key_selector(key_name):
    # this gets called whenever a key is selected
    # each button's commands calls this method with the key as the argument
    # at the end of the method, there's a check to see if a quality has been selected
    # if so then shows screen 2 and shows the key and the quality
    global key_selected
    global quality_selected
    key_selected = key_name
    if quality_selected != "n/a":
        update_name()
        show_screen2()


def quality_selector(option):
    # this gets called whenever a quality is selected
    # each button's commands calls this method with the quality as the argument
    # If the quality is major then the global var "major" is set to true, false otherwise
    # at the end of the method, there's a check to see if a key has been selected
    # if so then shows screen 2 and shows the key and the quality
    global quality_selected
    global key_selected
    global major
    selected_qual_var.set(option)
    quality_selected = option
    if option == "Major":
        major = True
    else:
        major = False

    if key_selected != "n/a":
        update_name()
        show_screen2()


def scale_selector(scale, index):
    # this gets called whenever a scale is selected
    # each button's commands calls this method with the scale name as the argument
    # modifies the global scale_selected variable
    # prints the scale select and the key with scale
    global scale_selected, current_image
    scale_var.set(scale)
    scale_selected = scale
    if major:
        temp_scale = major_scales[index]
    else:
        temp_scale = minor_scales[index]

    clear_fretboard()

    fill_out_board(temp_scale)
    current_image = draw_on_fretboard()
    show_image(current_image)



def get_notes_in_scale(scale):
    starting_note_index = 0
    for i, note in enumerate(notes_array):
        if note.note == key_selected:
            starting_note_index = i
            break
    cur_note_index = starting_note_index

    notes = [notes_array[starting_note_index]]


    count = 1
    for i, interval in enumerate(scale.intervals):
        cur_note_index = cur_note_index + interval
        if cur_note_index >= 12:
            cur_note_index = cur_note_index - 12
        if notes_array[cur_note_index] == notes[0]:
            break
        if cur_note_index < 12:
            notes.append(notes_array[cur_note_index])
        print(notes[count].note)
        count = count + 1
    return notes


# TODO fix the bug that currently makes the open fret apart of the scale ( not phrased correctly)
#  #do this by checking if the fret is in the scale after reaching 24th fret
def fill_out_board(scale):
    clear_fretboard()
    fret_marker = 0

    for x in fretboard:
        cur_fret = 0
        cur_interval = 0
        prev_interval = 0
        for i, fret in enumerate(x.string_frets):
            if fret.note != key_selected:
                continue
            else:
                fret_marker = i
                cur_fret = i
                fret.visible = True
                fret.root_check = True
                cur_fret = cur_fret + scale.intervals[cur_interval]
                prev_interval = cur_interval
                cur_interval = cur_interval + 1
                break

        condition = True

        while condition:
            if cur_fret == fret_marker:
                condition = False
            if cur_interval >= len(scale.intervals):
                cur_interval = 0
            if cur_fret >= len(x.string_frets):
                cur_fret = cur_fret - 24
                continue

            cur_fret_obj = x.string_frets[cur_fret]
            if cur_fret_obj.note == key_selected:
                cur_fret_obj.root_check = True
            cur_fret_obj.visible = True

            if cur_fret == 24:
                cur_fret = 0
                continue

            else:
                cur_fret = cur_fret + scale.intervals[cur_interval]

            prev_interval = cur_interval
            cur_interval = cur_interval + 1


def draw_on_fretboard():
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    font_path = "fonts/Marlboro.ttf"
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    first_fret_position = 20
    fret_spacing = 40
    bottom_string_position = 225
    string_distance = 40
    circle_radius = 17

    for x, strings in enumerate(fretboard):
        for y in range(25):
            fret_position = (first_fret_position + y * fret_spacing)
            string_position = (bottom_string_position - x * string_distance)
            cur_fret = fretboard[x].string_frets[y]
            if cur_fret.visible:
                circle_center = (fret_position, string_position)

                if cur_fret.root_check:
                    draw.ellipse(
                        (circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                         circle_center[0] + circle_radius, circle_center[1] + circle_radius),
                        fill='red', outline='red', width=2
                    )
                else:
                    draw.ellipse(
                        (circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                         circle_center[0] + circle_radius, circle_center[1] + circle_radius),
                        fill='black', outline='black', width=2
                    )

                text_size = draw.textsize(cur_fret.note, font=font)
                text_position = (circle_center[0] - text_size[0] / 2, circle_center[1] - text_size[1] / 2)

                draw.text(text_position, cur_fret.note, fill='white', font=font)

    return image


def show_image(image):
    global current_image_label, current_image

    if current_image_label:
        current_image_label.pack_forget()
    if current_image:
        current_image = None

    root.geometry("1300x400")
    photo = ImageTk.PhotoImage(image)

    current_image_label = tk.Label(root, image=photo)
    current_image_label.image = photo
    current_image_label.pack()

    current_image = photo


def clear_fretboard():
    for x in fretboard:
        for fret in x.string_frets:
            fret.visible = False
            fret.root_check = False


def update_name():
    # displays the key and quality selected on the second screen
    global key_selected
    global quality_selected
    k_q.set(f"{key_selected} {quality_selected}")


def back_button():
    # once the back button is pressed, this method gets called
    # it resets the global key and quality variables
    # ends by showing screen 1 and hiding screen 2

    global key_selected, quality_selected, current_image_label, current_image
    key_selected = "n/a"
    quality_selected = "n/a"
    show_screen1()
    clear_fretboard()
    current_image_label.pack_forget()
    current_image = None



def show_screen1():
    # shows screen1 and hides screen2, including the back button
    # shows the quality menu when the first frame is up
    # shrinks the window since there isn't a lot to be displayed
    root.geometry("300x150")
    screen1_frame.pack()
    screen2_frame.pack_forget()
    back_frame.pack_forget()
    show_quality_menu()


def show_screen2():
    # shows screen2 and hides screen1, and displays the back button
    # shows the scale menu when the first frame is up
    # also resizes the page to accommodate the fretboard display
    root.geometry("650x350")
    screen2_frame.pack()
    screen1_frame.pack_forget()
    back_frame.pack(side="left", anchor="nw", expand=False)
    show_scale()


def show_quality_menu():
    # clears the quality menu and adds the options again
    # this is to prevent duplicates of the options to appear whenever the method is called
    menu.delete(0, tk.END)
    selected_qual_var.set("Major or Minor")
    menu.add_command(label="Major", command=lambda: quality_selector("Major"))
    menu.add_command(label="Minor", command=lambda: quality_selector("Minor"))


def show_scale():
    # clears the scale menu
    # depending on the global major var, display the major or minor scales
    scale_menu.delete(0, tk.END)
    scale_var.set("Choose a Scale")
    if major:
        show_major()
    else:
        show_minor()


def show_major():
    # adds the major scales to the scale menu
    scale_menu.add_command(label="Major Scale/Ionian", command=lambda: scale_selector("Major Scale/Ionian", 0))
    scale_menu.add_command(label="Major Pentatonic", command=lambda: scale_selector("Major Pentatonic", 1))
    scale_menu.add_command(label="Harmonic Major", command=lambda: scale_selector("Harmonic Major", 2))
    scale_menu.add_command(label="Major Bebop", command=lambda: scale_selector("Major Bebop", 3))
    scale_menu.add_command(label="Major Blues", command=lambda: scale_selector("Major Blues", 4))
    scale_menu.add_command(label="Mixolydian", command=lambda: scale_selector("Mixolydian", 5))
    scale_menu.add_command(label="Lydian", command=lambda: scale_selector("Lydian", 6))


def show_minor():
    # adds the minor scales to the scale menu
    scale_menu.add_command(label="Minor Scale/Aeolian", command=lambda: scale_selector("Minor Scale/Aeolian", 0))
    scale_menu.add_command(label="Minor Pentatonic", command=lambda: scale_selector("Minor Pentatonic", 1))
    scale_menu.add_command(label="Harmonic Minor", command=lambda: scale_selector("Harmonic Minor", 2))
    scale_menu.add_command(label="Melodic Minor", command=lambda: scale_selector("Melodic Minor", 3))
    scale_menu.add_command(label="Minor Bebop", command=lambda: scale_selector("Minor Bebop", 4))
    scale_menu.add_command(label="Minor Blues", command=lambda: scale_selector("Minor Blues", 5))
    scale_menu.add_command(label="Dorian", command=lambda: scale_selector("Dorian", 6))
    scale_menu.add_command(label="Phrygian", command=lambda: scale_selector("Phrygian", 7))
    scale_menu.add_command(label="Locrian", command=lambda: scale_selector("Locrian", 8))


root = tk.Tk()
root.title("Guitar Scales Visualizer")

# Screen 1 where you select the Key and Quality
screen1_frame = tk.Frame(master=root)
screen1_frame.pack()

# Screen 2 where you select mode or specific scale
screen2_frame = tk.Frame(master=root)
screen2_frame.pack()

# Displays the title of the application
title_frame = tk.Frame(screen1_frame)
title_frame.pack(sid="top")

title = tk.Label(title_frame, text="Guitar Scales!")
title.pack(fill="none", expand=False)

# A menu for the quality of the key
menu_frame = tk.Frame(screen1_frame)
selected_qual_var = tk.StringVar()
selected_qual_var.set("Select a Quality")
quality_menu = tk.Menubutton(menu_frame, textvariable=selected_qual_var, relief=tk.RAISED)
quality_menu.pack(anchor="n", padx=5, pady=10)
menu = tk.Menu(quality_menu, tearoff=0)
quality_menu.config(menu=menu)
menu_frame.pack()

# the next frames are for the buttons to select a key
# btn_frame contains two frames within it: top and bottom
# top will have the non-sharped/flatted keys and the bottom will

btn_frame = tk.Frame(screen1_frame)
btn_frame.pack()

btn_top_frame = tk.Frame(btn_frame)
btn_top_frame.pack()

btn_btm_frame = tk.Frame(btn_frame)
btn_btm_frame.pack()

btn_frame.grid_rowconfigure(0, weight=1)
btn_frame.grid_columnconfigure(0, weight=1)

# Creating an array to house the different keys so that I can use two for loops
# This is in place of manually inserting all 12 keys
keys = ['C', "D", "E", "F", "G", "A", "B"]
key_sharps = ['C#/D♭', 'D#/E♭', "F#/G♭", "G#/A♭", "A#/B♭"]

# for loop for the top row
count = 0
for i in keys:
    btn = tk.Button(btn_top_frame, text=i, command=lambda key_name=i: key_selector(key_name))
    row = 0
    column = count
    btn.grid(row=row, column=column)
    count += 1

# for loop for creating the bottom row of buttons
count = 0
for i in key_sharps:
    btn = tk.Button(btn_btm_frame, text=i, command=lambda key_name=i: key_selector(key_name))
    row = 1
    column = count
    btn.grid(row=row, column=column)
    count += 1

# a button to return to the previous menu and wipes the selected key and quality
back_frame = tk.Frame()
back_frame.pack(side="top", anchor="nw", expand=False)

back = tk.Button(back_frame, text="Return", command=back_button)
back.pack(side="top", anchor="nw", padx=5, pady=5)

# Displays the Key and Quality on the second page
second_title_frame = tk.Frame(screen2_frame)
name_var = tk.StringVar()
k_q = tk.StringVar()

title_2 = tk.Label(second_title_frame, textvariable=k_q)
title_2.pack()
second_title_frame.pack(side="top")

# Create a Frame for the major scales
frame_scale = tk.Frame(screen2_frame)
frame_scale.pack()

scale_var = tk.StringVar()
scale_var.set("Choose a Scale")

scale_menubut = tk.Menubutton(frame_scale, textvariable=scale_var)
scale_menubut.pack()
scale_menu = tk.Menu(scale_menubut)
scale_menubut.config(menu=scale_menu)
scale_menubut.pack()

# show Screen 1 that also hides screen 2
show_screen1()
root.mainloop()

