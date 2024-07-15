# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import rtmidi
import tkinter as tk
from tkinter import filedialog as open_file
from tkinter.filedialog import asksaveasfile as save_as
import json

DEBUG = False

midi_out = rtmidi.MidiOut()
midi_in = rtmidi.MidiIn()
midi_in.ignore_types(sysex=False)
midi_k = rtmidi.MidiIn()
available_out_ports = midi_out.get_ports()
available_in_ports = midi_in.get_ports()

if DEBUG:
    print(available_out_ports)
    print(available_in_ports)

global m_ch
m_ch = 2

global p_c_ch
p_c_ch = 15

#in_port = ''
for x in range(0, len(available_in_ports)):
    if 'S-1' in available_in_ports[x]:
        in_port = x
        break

#in_port = ''
for x in range(0, len(available_in_ports)):
    if 'Akai' in available_in_ports[x]:
        midi_k_port = x
        break

#out_port = ''
for x in range(0, len(available_out_ports)):
    if 'S-1' in available_out_ports[x]:
        out_port = x
        break


# if in_port == '' or out_port == '':
#     exit()
print(in_port, out_port)
if available_out_ports:
    midi_out.open_port(out_port)

if available_in_ports:
    midi_in.open_port(in_port)

else:
    midi_out.open_virtual_port("My virtual output")
    midi_in.open_virtual_port("My virtual input")

midi_k.open_port(midi_k_port)


def handle_input(event, data=None):
    message, deltatime = event
    cc = int(message[0])
    com = int(message[1])
    value = message[2]

    if DEBUG:
        print('cc', cc, 'com', com, 'value', value)

    if cc - m_ch == 176:
        index_name = int(w_com.index(com))
        widget[index_name].set(value)
        try:
            widget_label[com]['text'] = extra_data[com][value]
        except:
            widget_label[com]['text'] = value

        if extra_data[com] != '':
            cmd_label['text'] = w_name[index_name] + ': ' + str(extra_data[com][value])
        else:
            cmd_label['text'] = w_name[index_name] + ': ' + str(value)

def handle_midi_k_input(event, data=None):
    message, deltatime = event
    cc = int(message[0])
    com = int(message[1])
    value = message[2]


    midi_out.send_message([0x90 + m_ch, com, value])

def midi_in_message():
    midi_in.set_callback(handle_input)

def midi_k_message():
    midi_k.set_callback(handle_midi_k_input)


midi_in_message()
midi_k_message()


def get_all_widget_value():
    for x in range(0, len_widget):
        try:
            full_name = str(widget[x].cget("label"))
            p = full_name.find('.')
            name = full_name[-((len(full_name) - p - 1)):]
            com = int(full_name[0:p])
            value = int(widget[x].get())
            control[x][0] = full_name
            control[x][1] = com
            control[x][2] = value
            try:
                widget_label[com]['text'] = extra_data[com][value]
            except:
                widget_label[com]['text'] = value
            if DEBUG:
                print('name', name, 'com', com, 'value', value)
        except:
            pass


def select_pattern(event):
    bank = int(program_change1.get())
    number = int(program_change2.get())

    value = ((bank - 1) * 16) + number

    midi_out.send_message([0xC0 + p_c_ch, value - 1])
    if DEBUG:
        print('Event:', event)
        print('value', value)
        print('p_c_ch: ', p_c_ch)
        print('Pattern: ', bank, '-', number, '-', value)
    program_change_label['text'] = 'Pattern: ' + str(bank) + '-' + str(number)


def select_program_change_ch(event):
    global p_c_ch
    p_c_ch = int(program_change_ch.get()) - 1
    if DEBUG:
        print('p_c_ch: ', p_c_ch)


def select_midi_ch(event):
    global m_ch
    m_ch = int(midi_ch.get()) - 1
    if DEBUG:
        print('m_ch: ', m_ch)


def update_value(event):
    w = event.widget
    if DEBUG:
        print('Event:', event)
    if isinstance(w, tk.Scale):
        # print(repr(w))

        full_name = str(w.cget("label"))
        p = full_name.find('.')
        name = full_name[-((len(full_name) - p - 1)):]
        com = int(full_name[0:p])
        value = int(w.get())
        try:
            widget_label[com]['text'] = extra_data[com][value]
        except:
            widget_label[com]['text'] = value

        if DEBUG:
            print('name', name, 'com', com, 'value', value)
        if extra_data[com] != '':
            cmd_label['text'] = name + ': ' + str(extra_data[com][value])

        else:
            cmd_label['text'] = name + ': ' + str(value)
        midi_out.send_message([0xB0 + m_ch, com, value])


def press_note(event):
    w = event.widget
    print(w)
    if isinstance(w, tk.Button):
        print(repr(w))

        name = w.cget("text")
        value = int(w_value[w_name.index(name)])
        print('name', name, 'value', value)
        com = int(w_com[w_name.index(name)])
        print('name', name, 'com', com, value, 'value')

        midi_out.send_message([0x90 + m_ch, com, value])


def release_note(event):
    w = event.widget
    if isinstance(w, tk.Button):
        print(repr(w))

        name = w.cget("text")
        value = int(w_value[w_name.index(name)])
        com = int(w_com[w_name.index(name)])
        print('name', name, 'com', com, value, 'value')

        midi_out.send_message([0x80 + m_ch, com, value])


def click_button(event):
    w = event.widget
    if isinstance(w, tk.Button):
        print(repr(w))

        name = w.cget("text")
        value = int(w_value[w_name.index(name)])
        com = int(w_com[w_name.index(name)])
        print('name', name, 'com', com, value, 'value')

        midi_out.send_message([0xB0 + m_ch, com, value])


def init_patch():
    for x in range(0, len_widget):
        try:
            w_name[x] = str(control[x][0])
            w_com[x] = control[x][1]
            w_value[x] = control[x][2]
            widget[x].set(w_value[x])
            try:
                widget_label[w_com[x]]['text'] = extra_data[w_com[x]][w_value[x]]
            except:
                widget_label[w_com[x]]['text'] = w_value[x]

            if DEBUG:
                print('com' + ' ' + str(w_com[x]) + 'value' + ' ' + str(w_value[x]))
        except:
            pass


    for x in range(0, len_controls):
        if x in w_com:
            try:

                if DEBUG:
                    print('com' + ' ' + str(w_com[w_com.index(x)]) + 'value' + ' ' + str(w_value[w_com.index(x)]))

                midi_out.send_message([0xB0 + m_ch, w_com[w_com.index(x)], w_value[w_com.index(x)]])
            except:
                pass
    cmd_label['text'] = '--------'


def update_control():
    for x in range(1, len_controls):
        if w_type[x] == 0 or w_type[x] == 3:
            control[x][4] = widget[x]['state']
        else:
            control[x][4] = widget[x].get()


def load_default():
    global control
    global filehandle
    with open('default.ptc', 'r') as file:
        control = json.load(file)
    info_label['text'] = 'default'
    init_patch()
    filehandle = ""


def save_patch_def():
    global filehandle
    get_all_widget_value()
    with open('default.ptc', 'w') as filehandle:
        json.dump(control, filehandle)
        info_label['text'] = 'Patch saved as default'
    filehandle = ""


def save_patch_as():
    global filehandle
    get_all_widget_value()
    filehandle = save_as(defaultextension='.ptc')
    if filehandle != None:
        json.dump(control, filehandle)
        info_label['text'] = filehandle.name.split("/")[-1]
        filehandle = filehandle.name


def save_patch():
    get_all_widget_value()
    try:

        if filehandle != "":
            with open(filehandle, 'w') as f:
                json.dump(control, f)
                info_label['text'] = 'Patch saved'
                info_label['text'] = filehandle.split("/")[-1]
        else:
            save_patch_as()

    except:
        save_patch_as()


def load_patch():
    global filehandle
    filehandle = open_file.askopenfilename(defaultextension='.ptc')
    if filehandle != '':
        global control
        control = []
        with open(filehandle, 'r') as file:
            control = json.load(file)

        init_patch()
        f = filehandle.split("/")[-1]
        info_label['text'] = f


# gui settings
fg_color = 'white'
bg_color = '#151b24'
tc_color = 'darkgray'
abg_color = 'gray'
t_color = 'dark gray'
hbc_color = '#353535'
hc_color = 'yellow'
bg_info_label = '#0f1626'
fg_info_label = '#4f6fb9'
bg_label_color = 'orange'
fg_label_color = 'black'
w_l_bg = bg_color
w_l_fg = 'lime'
font_label = '{Digital-7 Italic} 20 {}'

len_controls = 127
widget = [0] * 55
len_widget = len(widget)
widget_label = [0] * 255

extra_data = [''] * 255

extra_data[3] = ['8_1', '6_1', '8_1T', '4_1', '3_1', '4_1T', '2_1', '1D', '2_1T', '1_1', '2D', '1T', '1_2', '4D', '2T',
                 '1_4', '8_D', '4T', '1_8', '16D', '8T', '1_16', '32D', '16T', '1_32', '64D', '32T', '1_64', '128D',
                 '64T', '128']
extra_data[10] = ['L=63', 'L=62', 'L=61', 'L=60', 'L=59', 'L=58', 'L=57', 'L=56', 'L=55', 'L=54', 'L=53', 'L=52',
                  'L=51', 'L=50', 'L=49', 'L=48', 'L=47', 'L=46', 'L=45', 'L=44', 'L=43', 'L=42', 'L=41', 'L=40',
                  'L=39', 'L=38', 'L=37', 'L=36', 'L=35', 'L=34', 'L=33', 'L=32', 'L=31', 'L=30', 'L=29', 'L=28',
                  'L=27', 'L=26', 'L=25', 'L=24', 'L=23', 'L=22', 'L=21', 'L=20', 'L=19', 'L=18', 'L=17', 'L=16',
                  'L=15', 'L=14', 'L=13', 'L=12', 'L=11', 'L=10', 'L=9', 'L=8', 'L=7', 'L=6', 'L=5', 'L=4', 'L=3',
                  'L=2', 'L=1',
                  'L=R',
                  'R=1', 'R=2', 'R=3', 'R=4', 'R=5', 'R=6', 'R=7', 'R=8', 'R=9', 'R=10', 'R=11', 'R=12', 'R=13', 'R=14',
                  'R=15', 'R=16', 'R=17', 'R=18', 'R=19', 'R=20', 'R=21', 'R=22', 'R=23', 'R=24', 'R=25', 'R=26',
                  'R=27', 'R=28', 'R=29', 'R=30', 'R=31', 'R=32', 'R=33', 'R=34', 'R=35', 'R=36', 'R=37', 'R=38',
                  'R=39', 'R=40', 'R=41', 'R=42', 'R=43', 'R=44', 'R=45', 'R=46', 'R=47', 'R=48', 'R=49', 'R=50',
                  'R=51', 'R=52', 'R=53', 'R=54', 'R=55', 'R=56', 'R=57', 'R=58', 'R=59', 'R=60', 'R=61', 'R=62',
                  'R=63', 'R=64']
extra_data[12] = ['R. SAW', 'D. SAW', 'TRIANGLE', 'SQUARE', 'RANDOM', 'NOISE']
extra_data[14] = ["64'", "32'", "16'", "8'", "4'", "2'"]
extra_data[16] = ['ENU', 'NAN', ' LFO']
extra_data[22] = ['-2OA', '-2OC', '-1OC']
extra_data[28] = ['GATE', 'ENU']
extra_data[29] = ['LFO', 'GATE', 'TRIG']
extra_data[31] = ['OFF', 'ON', 'AUTO']
extra_data[78] = ['PINK', 'WHITE']
extra_data[79] = ['NORM', 'FAST']
extra_data[80] = ['MONO', 'UNI', 'POLY', 'CHD']
extra_data[81] = ['OFF', 'ON']
extra_data[82] = ['OFF', 'ON']
extra_data[83] = ['OFF', 'ON']
extra_data[90] = ['128', '64T', '128D', '1_64', '32T', '64D', '1_32', '16T', '32D', '1_16', '8T', '16D', '1_8', '4T',
                  '8D', '1_4']
extra_data[93] = ['OFF', '1', '2', '3', '4']
extra_data[105] = ['OFF', 'ON']
extra_data[106] = ['OFF', 'ON']
extra_data[107] = ['OFF', 'STEP', 'SLPE']

global control
control = []

rows, cols = len_widget, 5
for i in range(rows):
    col = []
    for j in range(cols):
        col.append(0)
    control.append(col)

current_value = [0] * len_widget

# build ui
root = tk.Tk()
root.title('Synth X Explorer')
frame1 = tk.Frame(root)
frame1.configure(height=820, width=1420)
frame_extra2 = tk.Frame(frame1)
frame_extra2.configure(
    height=130,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=560)
label11 = tk.Label(frame_extra2)
label11.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='EXTRA2')
label11.place(anchor="nw", height=15)
widget[0] = tk.Scale(frame_extra2)
current_value[0] = tk.IntVar()
widget[0].configure(
    from_=127,
    label='27.FILT BEND S',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[0].place(anchor="nw", x=10, y=20)
widget[0].bind("<ButtonRelease>", update_value)
widget[0].bind("<B1-Motion>", update_value)
widget_label[27] = tk.Label(frame_extra2)
widget_label[27].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[27].place(anchor="nw", x=30, y=60)
######
widget[1] = tk.Scale(frame_extra2)
current_value[1] = tk.IntVar()
widget[1].configure(
    from_=1,
    label='28.AMP ENV M',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[1].place(anchor="nw", x=150, y=20)
widget[1].bind("<ButtonRelease>", update_value)
widget[1].bind("<B1-Motion>", update_value)
widget_label[28] = tk.Label(frame_extra2)
widget_label[28].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[28].place(anchor="nw", x=170, y=60)
######
widget[2] = tk.Scale(frame_extra2)
current_value[2] = tk.IntVar()
widget[2].configure(
    from_=2,
    label='29.ENV TR MODE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[2].place(anchor="nw", x=290, y=20)
widget[2].bind("<ButtonRelease>", update_value)
widget[2].bind("<B1-Motion>", update_value)
widget_label[29] = tk.Label(frame_extra2)
widget_label[29].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[29].place(anchor="nw", x=310, y=60)
######
# widget[3] = tk.Scale(frame_extra2)
# current_value[3] = tk.IntVar()
# widget[3].configure(
#     from_=127,
#     label='26.FILT_KEYB_F',
#     orient="vertical",
#     to=0,
#     variable=current_value,
#     activebackground=abg_color,
#     troughcolor=t_color,
#     foreground=fg_color,
#     highlightthickness=0,
#     showvalue=0,
#     background=bg_color)
# widget[3].place(anchor="nw", x=430, y=20)
# widget[3].bind("<ButtonRelease>", update_value)
# widget[3].bind("<B1-Motion>", update_value)
# widget_label[26] = tk.Label(frame_extra2)
# widget_label[26].configure(
#     background=w_l_bg,
#     foreground=w_l_fg,
#     borderwidth=0,
#     text='')
# widget_label[26].place(anchor="nw", x=450, y=60)
frame_extra2.place(anchor="nw", bordermode="outside", x=140, y=560)
frame_extra2.grid_propagate(0)
frame_efx = tk.Frame(frame1)
frame_efx.configure(
    height=130,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=720)
######
label6 = tk.Label(frame_efx)
label6.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='EFX')
label6.place(anchor="nw", height=15)
widget[4] = tk.Scale(frame_efx)
current_value[4] = tk.IntVar()
widget[4].configure(
    from_=127,
    label='92.DELAY LEVEL',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[4].place(anchor="nw", x=10, y=20)
widget[4].bind("<ButtonRelease>", update_value)
widget[4].bind("<B1-Motion>", update_value)
widget_label[92] = tk.Label(frame_efx)
widget_label[92].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[92].place(anchor="nw", x=30, y=60)
widget[5] = tk.Scale(frame_efx)
current_value[5] = tk.IntVar()
widget[5].configure(
    from_=15,
    label='90.DELAY TIME',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[5].place(anchor="nw", x=150, y=20)
widget[5].bind("<ButtonRelease>", update_value)
widget[5].bind("<B1-Motion>", update_value)
widget_label[90] = tk.Label(frame_efx)
widget_label[90].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[90].place(anchor="nw", x=170, y=60)
widget[6] = tk.Scale(frame_efx)
current_value[6] = tk.IntVar()
widget[6].configure(
    from_=127,
    label='91.REVERB LEVEL',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[6].place(anchor="nw", x=290, y=20)
widget[6].bind("<ButtonRelease>", update_value)
widget[6].bind("<B1-Motion>", update_value)
widget_label[91] = tk.Label(frame_efx)
widget_label[91].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[91].place(anchor="nw", x=310, y=60)
widget[7] = tk.Scale(frame_efx)
current_value[7] = tk.IntVar()
widget[7].configure(
    from_=127,
    label='89.REVERB TIME',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[7].place(anchor="nw", x=430, y=20)
widget[7].bind("<ButtonRelease>", update_value)
widget[7].bind("<B1-Motion>", update_value)
widget_label[89] = tk.Label(frame_efx)
widget_label[89].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[89].place(anchor="nw", x=450, y=60)
widget[8] = tk.Scale(frame_efx)
current_value[8] = tk.IntVar()
widget[8].configure(
    from_=4,
    label='93.CHORUS',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[8].place(anchor="nw", x=570, y=20)
widget[8].bind("<ButtonRelease>", update_value)
widget[8].bind("<B1-Motion>", update_value)
widget_label[93] = tk.Label(frame_efx)
widget_label[93].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[93].place(anchor="nw", x=590, y=60)
######
frame_efx.place(anchor="nw", bordermode="outside", x=700, y=560)
frame_efx.grid_propagate(0)
frame_controller = tk.Frame(frame1)
frame_controller.configure(
    height=780,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=140)
label7 = tk.Label(frame_controller)
label7.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    state="normal",
    takefocus=True,
    text='CONTROLLER')
label7.place(anchor="nw", height=15)
widget[9] = tk.Scale(frame_controller)
current_value[9] = tk.IntVar()
widget[9].configure(
    from_=127,
    label='1.MOD WHEEL',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[9].place(anchor="nw", x=10, y=150)
widget[9].bind("<ButtonRelease>", update_value)
widget[9].bind("<B1-Motion>", update_value)
widget_label[1] = tk.Label(frame_controller)
widget_label[1].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[1].place(anchor="nw", x=30, y=190)
widget[10] = tk.Scale(frame_controller)
current_value[10] = tk.IntVar()
widget[10].configure(
    from_=127,
    label='65.PORTAM',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[10].place(anchor="nw", x=10, y=410)
widget[10].bind("<ButtonRelease>", update_value)
widget[10].bind("<B1-Motion>", update_value)
widget_label[65] = tk.Label(frame_controller)
widget_label[65].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[65].place(anchor="nw", x=30, y=450)
widget[11] = tk.Scale(frame_controller)
current_value[11] = tk.IntVar()
widget[11].configure(
    from_=0,
    label='10.PAN',
    orient="horizontal",
    to=127,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[11].place(anchor="nw", x=10, y=25)
widget[11].bind("<ButtonRelease>", update_value)
widget[11].bind("<B1-Motion>", update_value)
widget_label[10] = tk.Label(frame_controller)
widget_label[10].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[10].place(anchor="nw", x=10, y=70)
widget[12] = tk.Scale(frame_controller)
current_value[12] = tk.IntVar()
widget[12].configure(
    from_=127,
    label='11.EXP PEDAL',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[12].place(anchor="nw", x=10, y=280)
widget[12].bind("<ButtonRelease>", update_value)
widget[12].bind("<B1-Motion>", update_value)
widget_label[11] = tk.Label(frame_controller)
widget_label[11].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[11].place(anchor="nw", x=30, y=320)
widget[13] = tk.Scale(frame_controller)
current_value[13] = tk.IntVar()
widget[13].configure(
    from_=127,
    label='64.DAMP P',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[13].place(anchor="nw", x=10, y=540)
widget[13].bind("<ButtonRelease>", update_value)
widget[13].bind("<B1-Motion>", update_value)
widget_label[64] = tk.Label(frame_controller)
widget_label[64].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[64].place(anchor="nw", x=30, y=580)
######
frame_controller.place(anchor="nw", bordermode="outside", x=0, y=40)
frame_controller.grid_propagate(0)
frame_filter = tk.Frame(frame1)
frame_filter.configure(
    height=130,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=700)
label4 = tk.Label(frame_filter)
label4.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='FILTER')
label4.place(anchor="nw", height=15)
widget[14] = tk.Scale(frame_filter)
current_value[14] = tk.IntVar()
widget[14].configure(
    from_=127,
    label='74.FREQ',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[14].place(anchor="nw", x=10, y=20)
widget[14].bind("<ButtonRelease>", update_value)
widget[14].bind("<B1-Motion>", update_value)
widget_label[74] = tk.Label(frame_filter)
widget_label[74].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[74].place(anchor="nw", x=30, y=60)
widget[15] = tk.Scale(frame_filter)
current_value[15] = tk.IntVar()
widget[15].configure(
    from_=127,
    label='71.RESON',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[15].place(anchor="nw", x=150, y=20)
widget[15].bind("<ButtonRelease>", update_value)
widget[15].bind("<B1-Motion>", update_value)
widget_label[71] = tk.Label(frame_filter)
widget_label[71].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[71].place(anchor="nw", x=170, y=60)
widget[16] = tk.Scale(frame_filter)
current_value[16] = tk.IntVar()
widget[16].configure(
    from_=127,
    label='25.LFO',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[16].place(anchor="nw", x=290, y=20)
widget[16].bind("<ButtonRelease>", update_value)
widget[16].bind("<B1-Motion>", update_value)
widget_label[25] = tk.Label(frame_filter)
widget_label[25].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[25].place(anchor="nw", x=310, y=60)
widget[17] = tk.Scale(frame_filter)
current_value[17] = tk.IntVar()
widget[17].configure(
    from_=127,
    label='24.ENVELOPE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[17].place(anchor="nw", x=430, y=20)
widget[17].bind("<ButtonRelease>", update_value)
widget[17].bind("<B1-Motion>", update_value)
widget_label[24] = tk.Label(frame_filter)
widget_label[24].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[24].place(anchor="nw", x=450, y=60)
widget[18] = tk.Scale(frame_filter)
current_value[18] = tk.IntVar()
widget[18].configure(
    from_=127,
    label='26.FILT KEYB F',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[18].place(anchor="nw", x=570, y=20)
widget[18].bind("<ButtonRelease>", update_value)
widget[18].bind("<B1-Motion>", update_value)
widget_label[26] = tk.Label(frame_filter)
widget_label[26].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[26].place(anchor="nw", x=590, y=60)
frame_filter.place(anchor="nw", bordermode="outside", x=140, y=300)
frame_filter.grid_propagate(0)
######
Label = tk.Frame(frame1)
Label.configure(
    height=35,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=1420)
info_label = tk.Label(Label)
info_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label, font=font_label,
                     text='--------')
info_label.place(anchor="nw", width=280, height=25, x=0, y=5)

cmd_label = tk.Label(Label)
cmd_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label, font=font_label,
                    text='--------')
cmd_label.place(anchor="nw", width=280, height=25, x=860, y=5)

program_change_label = tk.Label(Label)
program_change_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label,
                               font=font_label, text='--------')
program_change_label.place(anchor="nw", width=140, height=25, x=425, y=5)

program_change1 = tk.StringVar(value='03')
values = [
    '01',
    '02',
    '03',
    '04']

optionmenu1 = tk.OptionMenu(
    Label, program_change1, *values, command=select_pattern)
optionmenu1.place(anchor="nw", width=50, height=25, x=575, y=5)

program_change2 = tk.StringVar(value='01')
values = [
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '09',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16']

optionmenu2 = tk.OptionMenu(
    Label, program_change2, *values, command=select_pattern)
optionmenu2.place(anchor="nw", width=50, height=25, x=630, y=5)

program_change_ch_label = tk.Label(Label)
program_change_ch_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label,
                                  font=font_label, text='P.C. CH:')
program_change_ch_label.place(anchor="nw", width=140, height=25, x=1110, y=5)
program_change_ch = tk.StringVar(value='15')
values = [
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '09',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16']

option_program_change_ch = tk.OptionMenu(
    Label, program_change_ch, *values, command=select_program_change_ch)
option_program_change_ch.place(anchor="nw", width=50, height=25, x=1200, y=5)

midi_ch_label = tk.Label(Label)
midi_ch_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label, font=font_label,
                        text='MIDI CH:')
midi_ch_label.place(anchor="nw", width=70, height=25, x=1270, y=5)
midi_ch = tk.StringVar(value='03')
values = [
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '09',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16']

option_midi_ch = tk.OptionMenu(
    Label, midi_ch, *values, command=select_midi_ch)
option_midi_ch.place(anchor="nw", width=50, height=25, x=1360, y=5)

button2 = tk.Button(Label)
button2.configure(justify="left", text='Load', command=load_patch)
button2.place(anchor="nw", width=50, x=240, y=5)
button3 = tk.Button(Label)
button3.configure(text='Save', command=save_patch)
button3.place(anchor="nw", width=50, x=290, y=5)
button4 = tk.Button(Label)
button4.configure(justify="left", text='Save as', command=save_patch_as)
button4.place(anchor="nw", width=50, x=340, y=5)
button5 = tk.Button(Label)
button5.configure(text='Initialize', command=load_default)
button5.place(anchor="nw", width=80, x=690, y=5)
button6 = tk.Button(Label)
button6.configure(state="normal", text='Make default', command=save_patch_def)
button6.place(anchor="nw", width=80, x=770, y=5)
Label.place(anchor="nw", x=0, y=5)
######
frame_lfo = tk.Frame(frame1)
frame_lfo.configure(
    height=260,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=320)
label2 = tk.Label(frame_lfo)
label2.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    state="normal", text='LFO')
label2.place(anchor="nw", height=15)
######
widget[19] = tk.Scale(frame_lfo)
current_value[19] = tk.IntVar()
widget[19].configure(
    from_=30,
    label='3.LFO RATE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[19].place(anchor="nw", relx=0.0, x=10, y=20)
widget[19].bind("<ButtonRelease>", update_value)
widget[19].bind("<B1-Motion>", update_value)
widget_label[3] = tk.Label(frame_lfo)
widget_label[3].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[3].place(anchor="nw", x=30, y=60)
######
widget[20] = tk.Scale(frame_lfo)
current_value[20] = tk.IntVar()
widget[20].configure(
    from_=5,
    label='12.WAVE FORM',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[20].place(anchor="nw", x=10, y=150)
widget[20].bind("<ButtonRelease>", update_value)
widget[20].bind("<B1-Motion>", update_value)
widget_label[12] = tk.Label(frame_lfo)
widget_label[12].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[12].place(anchor="nw", x=30, y=190)
######
widget[21] = tk.Scale(frame_lfo)
current_value[21] = tk.IntVar()
widget[21].configure(
    from_=1,
    label='79.LFO MODE',
    orient="vertical",
    state="normal",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[21].place(anchor="nw", relx=0.0, x=150, y=20)
widget[21].bind("<ButtonRelease>", update_value)
widget[21].bind("<B1-Motion>", update_value)
widget_label[79] = tk.Label(frame_lfo)
widget_label[79].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[79].place(anchor="nw", x=170, y=60)
widget[22] = tk.Scale(frame_lfo)
current_value[22] = tk.IntVar()
widget[22].configure(
    from_=1,
    label='106.LFO SYNC',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[22].place(anchor="nw", x=150, y=150)
widget[22].bind("<ButtonRelease>", update_value)
widget[22].bind("<B1-Motion>", update_value)
widget_label[106] = tk.Label(frame_lfo)
widget_label[106].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[106].place(anchor="nw", x=170, y=190)
frame_lfo.place(anchor="nw", bordermode="outside", x=140, y=40)
frame_lfo.grid_propagate(0)
######
frame_oscillator = tk.Frame(frame1)
frame_oscillator.configure(
    height=260,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=1000)
label3 = tk.Label(frame_oscillator)
label3.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    state="normal",
    text='OSCILLATOR')
label3.place(anchor="nw", height=15)
######
widget[23] = tk.Scale(frame_oscillator)
current_value[23] = tk.IntVar()
widget[23].configure(
    from_=5,
    label='14.OSC RANGE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[23].place(anchor="nw", x=10, y=20)
widget[23].bind("<ButtonRelease>", update_value)
widget[23].bind("<B1-Motion>", update_value)
widget_label[14] = tk.Label(frame_oscillator)
widget_label[14].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[14].place(anchor="nw", x=30, y=60)
widget[24] = tk.Scale(frame_oscillator)
current_value[24] = tk.IntVar()
widget[24].configure(
    from_=127,
    label='13.OSC LFO',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[24].place(anchor="nw", x=10, y=150)
widget[24].bind("<ButtonRelease>", update_value)
widget[24].bind("<B1-Motion>", update_value)
widget_label[13] = tk.Label(frame_oscillator)
widget_label[13].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[13].place(anchor="nw", x=30, y=190)
widget[25] = tk.Scale(frame_oscillator)
current_value[25] = tk.IntVar()
widget[25].configure(
    from_=127,
    label='76.FINE TUNE',  # todo fix range must show -100 +100
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[25].place(anchor="nw", x=150, y=20)
widget[25].bind("<ButtonRelease>", update_value)
widget[25].bind("<B1-Motion>", update_value)
widget_label[76] = tk.Label(frame_oscillator)
widget_label[76].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[76].place(anchor="nw", x=170, y=60)
widget[26] = tk.Scale(frame_oscillator)
current_value[26] = tk.IntVar()
widget[26].configure(
    from_=100,
    label='103.OSC CHOP',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[26].place(anchor="nw", x=150, y=150)
widget[26].bind("<ButtonRelease>", update_value)
widget[26].bind("<B1-Motion>", update_value)
widget_label[103] = tk.Label(frame_oscillator)
widget_label[103].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[103].place(anchor="nw", x=170, y=190)
widget[27] = tk.Scale(frame_oscillator)
current_value[27] = tk.IntVar()
widget[27].configure(
    from_=127,
    label='19.SQUARE W L',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[27].place(anchor="nw", x=290, y=20)
widget[27].bind("<ButtonRelease>", update_value)
widget[27].bind("<B1-Motion>", update_value)
widget_label[19] = tk.Label(frame_oscillator)
widget_label[19].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[19].place(anchor="nw", x=310, y=60)
widget[28] = tk.Scale(frame_oscillator)
current_value[28] = tk.IntVar()
widget[28].configure(
    from_=127,
    label='20.SAWT W L',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[28].place(anchor="nw", x=290, y=150)
widget[28].bind("<ButtonRelease>", update_value)
widget[28].bind("<B1-Motion>", update_value)
widget_label[20] = tk.Label(frame_oscillator)
widget_label[20].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[20].place(anchor="nw", x=310, y=190)
widget[29] = tk.Scale(frame_oscillator)
current_value[29] = tk.IntVar()
widget[29].configure(
    from_=127,
    label='15.OSC PWIDTH',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[29].place(anchor="nw", x=430, y=20)
widget[29].bind("<ButtonRelease>", update_value)
widget[29].bind("<B1-Motion>", update_value)
widget_label[15] = tk.Label(frame_oscillator)
widget_label[15].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[15].place(anchor="nw", x=450, y=60)
widget[30] = tk.Scale(frame_oscillator)
current_value[30] = tk.IntVar()
widget[30].configure(
    from_=2,
    label='107.OSC DW SW',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[30].place(anchor="nw", x=430, y=150)
widget[30].bind("<ButtonRelease>", update_value)
widget[30].bind("<B1-Motion>", update_value)
widget_label[107] = tk.Label(frame_oscillator)
widget_label[107].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[107].place(anchor="nw", x=450, y=190)
widget[31] = tk.Scale(frame_oscillator)
current_value[31] = tk.IntVar()
widget[31].configure(
    from_=127,
    label='102.OSC DRAW M',
    orient="vertical",
    to=3,  # To test it!
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[31].place(anchor="nw", x=570, y=20)
widget[31].bind("<ButtonRelease>", update_value)
widget[31].bind("<B1-Motion>", update_value)
widget_label[102] = tk.Label(frame_oscillator)
widget_label[102].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[102].place(anchor="nw", x=590, y=60)
widget[32] = tk.Scale(frame_oscillator)
current_value[32] = tk.IntVar()
widget[32].configure(
    from_=127,
    label='23.OSC NOISE L',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[32].place(anchor="nw", x=570, y=150)
widget[32].bind("<ButtonRelease>", update_value)
widget[32].bind("<B1-Motion>", update_value)
widget_label[23] = tk.Label(frame_oscillator)
widget_label[23].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[23].place(anchor="nw", x=590, y=190)
widget[33] = tk.Scale(frame_oscillator)
current_value[33] = tk.IntVar()
widget[33].configure(
    from_=1,
    label='78.NOISE MODE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[33].place(anchor="nw", x=710, y=150)
widget[33].bind("<ButtonRelease>", update_value)
widget[33].bind("<B1-Motion>", update_value)
widget_label[78] = tk.Label(frame_oscillator)
widget_label[78].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[78].place(anchor="nw", x=730, y=190)
widget[34] = tk.Scale(frame_oscillator)
current_value[34] = tk.IntVar()
widget[34].configure(
    from_=127,
    label='21.OSC S-LEVEL',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[34].place(anchor="nw", x=710, y=20)
widget[34].bind("<ButtonRelease>", update_value)
widget[34].bind("<B1-Motion>", update_value)
widget_label[21] = tk.Label(frame_oscillator)
widget_label[21].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[21].place(anchor="nw", x=730, y=60)
widget[35] = tk.Scale(frame_oscillator)
current_value[35] = tk.IntVar()
widget[35].configure(
    from_=127,
    label='104.OSC CHOP C',
    orient="vertical",
    to=3,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[35].place(anchor="nw", x=850, y=20)
widget[35].bind("<ButtonRelease>", update_value)
widget[35].bind("<B1-Motion>", update_value)
widget_label[104] = tk.Label(frame_oscillator)
widget_label[104].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[104].place(anchor="nw", x=870, y=60)
######
frame_oscillator.place(anchor="nw", bordermode="outside", x=420, y=40)
frame_oscillator.grid_propagate(0)
frame_envelope = tk.Frame(frame1)
frame_envelope.configure(
    height=130,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=580)
label5 = tk.Label(frame_envelope)
label5.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='ENVELOPE')
label5.place(anchor="nw", height=15)
widget[36] = tk.Scale(frame_envelope)
current_value[36] = tk.IntVar()
widget[36].configure(
    from_=127,
    label='73.ATTACK',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[36].place(anchor="nw", x=10, y=20)
widget[36].bind("<ButtonRelease>", update_value)
widget[36].bind("<B1-Motion>", update_value)
widget_label[73] = tk.Label(frame_envelope)
widget_label[73].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[73].place(anchor="nw", x=30, y=60)
widget[37] = tk.Scale(frame_envelope)
current_value[37] = tk.IntVar()
widget[37].configure(
    from_=127,
    label='75.DECAY',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[37].place(anchor="nw", x=150, y=20)
widget[37].bind("<ButtonRelease>", update_value)
widget[37].bind("<B1-Motion>", update_value)
widget_label[75] = tk.Label(frame_envelope)
widget_label[75].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[75].place(anchor="nw", x=170, y=60)
widget[38] = tk.Scale(frame_envelope)
current_value[38] = tk.IntVar()
widget[38].configure(
    from_=127,
    label='30.SUSTAIN',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[38].place(anchor="nw", x=290, y=20)
widget[38].bind("<ButtonRelease>", update_value)
widget[38].bind("<B1-Motion>", update_value)
widget_label[30] = tk.Label(frame_envelope)
widget_label[30].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[30].place(anchor="nw", x=310, y=60)
widget[39] = tk.Scale(frame_envelope)
current_value[39] = tk.IntVar()
widget[39].configure(
    from_=127,
    label='72.RELEASE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[39].place(anchor="nw", x=430, y=20)
widget[39].bind("<ButtonRelease>", update_value)
widget[39].bind("<B1-Motion>", update_value)
widget_label[72] = tk.Label(frame_envelope)
widget_label[72].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[72].place(anchor="nw", x=450, y=60)
frame_envelope.place(anchor="nw", bordermode="outside", x=840, y=300)
######
frame_extra1 = tk.Frame(frame1)
frame_extra1.configure(
    height=130,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=1280)
label10 = tk.Label(frame_extra1)
label10.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='EXTRA1')
label10.place(anchor="nw", height=15)
widget[40] = tk.Scale(frame_extra1)
current_value[40] = tk.IntVar()
widget[40].configure(
    from_=2,
    label='16.OSC PWM S ',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[40].place(anchor="nw", x=10, y=20)
widget[40].bind("<ButtonRelease>", update_value)
widget[40].bind("<B1-Motion>", update_value)
widget_label[16] = tk.Label(frame_extra1)
widget_label[16].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[16].place(anchor="nw", x=30, y=60)
widget[41] = tk.Scale(frame_extra1)
current_value[41] = tk.IntVar()
widget[41].configure(
    from_=127,
    label='17.LFO MOD D',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[41].place(anchor="nw", x=150, y=20)
widget[41].bind("<ButtonRelease>", update_value)
widget[41].bind("<B1-Motion>", update_value)
widget_label[17] = tk.Label(frame_extra1)
widget_label[17].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[17].place(anchor="nw", x=170, y=60)
widget[42] = tk.Scale(frame_extra1)
current_value[42] = tk.IntVar()
widget[42].configure(
    from_=120,
    label='18.OSC BEND S',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[42].place(anchor="nw", x=290, y=20)
widget[42].bind("<ButtonRelease>", update_value)
widget[42].bind("<B1-Motion>", update_value)
widget_label[18] = tk.Label(frame_extra1)
widget_label[18].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[18].place(anchor="nw", x=310, y=60)
widget[43] = tk.Scale(frame_extra1)
current_value[43] = tk.IntVar()
widget[43].configure(
    from_=2,
    label='22.OSC S-TYPE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[43].place(anchor="nw", x=430, y=20)
widget[43].bind("<ButtonRelease>", update_value)
widget[43].bind("<B1-Motion>", update_value)
widget_label[22] = tk.Label(frame_extra1)
widget_label[22].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[22].place(anchor="nw", x=450, y=60)
widget[44] = tk.Scale(frame_extra1)
current_value[44] = tk.IntVar()
widget[44].configure(
    from_=3,
    label='80.POLY MODE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[44].place(anchor="nw", x=570, y=20)
widget[44].bind("<ButtonRelease>", update_value)
widget[44].bind("<B1-Motion>", update_value)
widget_label[80] = tk.Label(frame_extra1)
widget_label[80].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[80].place(anchor="nw", x=590, y=60)
widget[45] = tk.Scale(frame_extra1)
current_value[45] = tk.IntVar()
widget[45].configure(
    from_=2,
    label='31.PORT MODE',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[45].place(anchor="nw", x=710, y=20)
widget[45].bind("<ButtonRelease>", update_value)
widget[45].bind("<B1-Motion>", update_value)
widget_label[31] = tk.Label(frame_extra1)
widget_label[31].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[31].place(anchor="nw", x=730, y=60)
widget[46] = tk.Scale(frame_extra1)
current_value[46] = tk.IntVar()
widget[46].configure(
    from_=127,
    label='5.PORT TIME',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[46].place(anchor="nw", x=850, y=20)
widget[46].bind("<ButtonRelease>", update_value)
widget[46].bind("<B1-Motion>", update_value)
widget_label[5] = tk.Label(frame_extra1)
widget_label[5].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[5].place(anchor="nw", x=880, y=60)
widget[47] = tk.Scale(frame_extra1)
current_value[47] = tk.IntVar()
widget[47].configure(
    from_=1,
    label='105.LFO KEY T',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[47].place(anchor="nw", x=990, y=20)
widget[47].bind("<ButtonRelease>", update_value)
widget[47].bind("<B1-Motion>", update_value)
widget_label[105] = tk.Label(frame_extra1)
widget_label[105].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[105].place(anchor="nw", x=1010, y=60)
widget[48] = tk.Scale(frame_extra1)
current_value[48] = tk.IntVar()
widget[48].configure(
    from_=1,
    label='77.TRANSP SW',  # todo fix range must show -60 +60
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[48].place(anchor="nw", x=1130, y=20)
widget[48].bind("<ButtonRelease>", update_value)
widget[48].bind("<B1-Motion>", update_value)
widget_label[77] = tk.Label(frame_extra1)
widget_label[77].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[77].place(anchor="nw", x=1150, y=60)
######
frame_extra1.place(anchor="nw", bordermode="outside", x=140, y=430)
frame_extra1.grid_propagate(0)
frame_extra3 = tk.Frame(frame1)
frame_extra3.configure(
    height=130,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=1280)
label8 = tk.Label(frame_extra3)
label8.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='EXTRA3')
label8.place(anchor="nw", height=15)
######
widget[49] = tk.Scale(frame_extra3)
current_value[49] = tk.IntVar()
widget[49].configure(
    from_=1,
    label='81.CHORD V2 SW',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[49].place(anchor="nw", x=10, y=20)
widget[49].bind("<ButtonRelease>", update_value)
widget[49].bind("<B1-Motion>", update_value)
widget_label[81] = tk.Label(frame_extra3)
widget_label[81].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[81].place(anchor="nw", x=30, y=60)
widget[50] = tk.Scale(frame_extra3)
current_value[50] = tk.IntVar()
widget[50].configure(
    from_=1,
    label='82.CHORD V3 SW',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[50].place(anchor="nw", x=150, y=20)
widget[50].bind("<ButtonRelease>", update_value)
widget[50].bind("<B1-Motion>", update_value)
widget_label[82] = tk.Label(frame_extra3)
widget_label[82].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[82].place(anchor="nw", x=180, y=60)
widget[51] = tk.Scale(frame_extra3)
current_value[51] = tk.IntVar()
widget[51].configure(
    from_=1,
    label='83.CHORD V4 SW',
    orient="vertical",
    to=0,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[51].place(anchor="nw", x=290, y=20)
widget[51].bind("<ButtonRelease>", update_value)
widget[51].bind("<B1-Motion>", update_value)
widget_label[83] = tk.Label(frame_extra3)
widget_label[83].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[83].place(anchor="nw", x=310, y=60)
widget[52] = tk.Scale(frame_extra3)
current_value[52] = tk.IntVar()
widget[52].configure(
    from_=76,
    label='85.CHORD V2 KS',  # todo value should show -12 +12
    orient="vertical",
    to=52,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[52].place(anchor="nw", x=430, y=20)
widget[52].bind("<ButtonRelease>", update_value)
widget[52].bind("<B1-Motion>", update_value)
widget_label[85] = tk.Label(frame_extra3)
widget_label[85].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[85].place(anchor="nw", x=450, y=60)
widget[53] = tk.Scale(frame_extra3)
current_value[53] = tk.IntVar()
widget[53].configure(
    from_=76,
    label='86.CHORD V3 KS',
    orient="vertical",
    to=52,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[53].place(anchor="nw", x=570, y=20)
widget[53].bind("<ButtonRelease>", update_value)
widget[53].bind("<B1-Motion>", update_value)
widget_label[86] = tk.Label(frame_extra3)
widget_label[86].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[86].place(anchor="nw", x=590, y=60)
widget[54] = tk.Scale(frame_extra3)
current_value[54] = tk.IntVar()
widget[54].configure(
    from_=76,
    label='87.CHORD V4 KS',
    orient="vertical",
    to=52,
    variable=current_value,
    activebackground=abg_color,
    troughcolor=t_color,
    foreground=fg_color,
    highlightthickness=0,
    showvalue=0,
    background=bg_color)
widget[54].place(anchor="nw", x=710, y=20)
widget[54].bind("<ButtonRelease>", update_value)
widget[54].bind("<B1-Motion>", update_value)
widget_label[87] = tk.Label(frame_extra3)
widget_label[87].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[87].place(anchor="nw", x=730, y=60)
frame_extra3.place(anchor="nw", bordermode="outside", x=140, y=690)
frame_extra3.grid_propagate(0)
frame1.pack(side="top")

get_all_widget_value()

w_name = [0] * len_widget
w_type = [0] * len_widget
w_com = [0] * len_widget
w_value = [0] * len_widget

for x in range(0, len_widget):
    w_name[x] = str(control[x][0])
    w_com[x] = control[x][1]
    w_value[x] = control[x][2]

load_default()
select_pattern(None)

root.mainloop()
