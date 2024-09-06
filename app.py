# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import tkinter as tk
from tkinter import filedialog as open_file
from tkinter.filedialog import asksaveasfile as save_as

import rtmidi

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

# len_widget = 127
# widget = [0] * len_widget

# widget_label = [0] * len_widget

len_controls = 127
control = [[]] * 255
widget = [0] * 255
len_widget = len(widget)
widget_label = [0] * 255
current_value = [0] * len_widget


extra_data = [''] * 255


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

DEBUG = True

midi_out = rtmidi.MidiOut()
midi_in = rtmidi.MidiIn()
midi_in.ignore_types(sysex=False)
midi_k = rtmidi.MidiIn()
available_out_ports = midi_out.get_ports()
available_in_ports = midi_in.get_ports()
available_out_ports.append("None")
available_in_ports.append("None")
available_k_ports = available_in_ports

print(available_out_ports)
print(available_in_ports)

def save_conf():
    with open('config.cfg', 'w') as file:
        json.dump(conf, file)

def load_conf():
    global conf
    global m_ch
    global p_c_ch
    global midi_in_port
    global midi_out_port
    global midi_k_port
    try:
        with open('config.cfg', 'r') as file:
            conf = json.load(file)
        m_ch = conf['m_ch']
        p_c_ch = conf['p_c_ch']
        midi_in_port = conf['midi_in_port']
        midi_out_port = conf['midi_out_port']
        midi_k_port = conf['midi_k_port']

    except:

        conf = {}
        conf["m_ch"] = 2
        m_ch = conf["m_ch"]
        conf["p_c_ch"] = 15
        p_c_ch = conf["p_c_ch"]
        conf["midi_in_port"] = len(available_in_ports) - 1
        midi_in_port = conf["midi_in_port"]
        conf["midi_out_port"] = len(available_out_ports) - 1
        midi_out_port = conf["midi_out_port"]
        conf["midi_k_port"] = len(available_k_ports) - 1
        midi_k_port = conf["midi_k_port"]
        save_conf()

load_conf()

try:
    midi_in.open_port(midi_in_port)
    midi_out.open_port(midi_out_port)
    midi_k.open_port(midi_k_port)
except:
    print('Open Midi ports failed')
m_k_ch = 0

def handle_input(event, data=None):
    message, deltatime = event
    cc = int(message[0])
    com = int(message[1])
    value = message[2]

    if DEBUG:
        print('cc', cc, 'com', com, 'value', value)

    if cc - m_ch == 176:
        control_name = control[com][0]
        widget[com].set(value)


        if extra_data[com]:
            widget_label[com]['text'] = extra_data[com][value]
            cmd_label['text'] = control_name + ': ' + str(extra_data[com][value])


        else:
            widget_label[com]['text'] = value
            cmd_label['text'] = control_name + ': ' + str(value)


def handle_midi_k_input(event, data=None):
    message, deltatime = event
    cc = int(message[0])
    com = int(message[1])
    value = message[2]

    if DEBUG:
        print('cc', cc, 'com', com, 'value', value)

    if cc - m_ch == 176:
        control_name = control[com][0]
        widget[com].set(value)

        if extra_data[com]:
            widget_label[com]['text'] = extra_data[com][value]
            cmd_label['text'] = control_name + ': ' + str(extra_data[com][value])


        else:
            widget_label[com]['text'] = value
            cmd_label['text'] = control_name + ': ' + str(value)


    midi_out.send_message([cc + m_ch, com, value])

def midi_in_message():
    midi_in.set_callback(handle_input)

def midi_k_message():
    midi_k.set_callback(handle_midi_k_input)


midi_in_message()
midi_k_message()


def get_all_widget_value():
    for x in range(0, len(control)):
        try:
            value = int(widget[x].get())
            control[x][2] = value
            if DEBUG:
                print('get_all_widget_value', 'x', x, value)
        except:
            pass

def set_all_widget_value():

    for x in range(0,len(control)):

        if control[x]:

            com = int(control[x][1])
            value = int(control[x][2])

            widget[com].set(value)

            if com == 3:
                if control[106][2] == 1:
                    widget[3].configure(from_=30)
                else:
                    widget[3].configure(from_=128)
            try:
                widget_label[com]['text'] = extra_data[com][value]
            except:
                widget_label[com]['text'] = value


            if DEBUG:
                print('set_all_widget_value',com, value)
            midi_out.send_message([0xB0 + m_ch, com, value])




def update_value(event):    #20240905   100%
    w = event.widget
    if isinstance(w, tk.Scale):
        full_name = str(w.cget("label"))
        p = full_name.find('.')
        name = full_name[-((len(full_name) - p - 1)):]
        com = int(full_name[0:p])
        value = int(w.get())
        control[com][2] = value

        if DEBUG:
            print('name', name, 'com', com, 'value', value, 'extra data', extra_data[com])

        if com == 106 and value == 1:
            extra_data[3] = ['8_1', '6_1', '8_1T', '4_1', '3_1', '4_1T', '2_1', '1D', '2_1T', '1_1', '2D', '1T', '1_2',
                                 '4D', '2T', '1_4', '8_D', '4T', '1_8', '16D', '8T', '1_16', '32D', '16T', '1_32', '64D',
                                 '32T', '1_64', '128D', '64T', '128']
            widget[3].configure(from_ = 30)
        if com == 106 and value == 0:
                extra_data[3] = ''
                widget[3].configure(from_ = 128)
        try:
            widget_label[com]['text'] = extra_data[com][value]
        except:
            widget_label[com]['text'] = value

        try:
            cmd_label['text'] = name + ': ' + str(extra_data[com][value])

        except:
            cmd_label['text'] = name + ': ' + str(value)
        midi_out.send_message([0xB0 + m_ch, com, value])

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
    conf["p_c_ch"] = p_c_ch
    save_conf()
    if DEBUG:
        print('p_c_ch: ', p_c_ch)

def select_midi_ch(event):
    global m_ch
    m_ch = int(midi_ch.get()) - 1
    conf["m_ch"] = m_ch
    save_conf()
    if DEBUG:
        print('m_ch: ', m_ch)
def select_midi_in_d(event):
    try:
        midi_in_port = midi_in_d.get()
        midi_in_port = available_in_ports.index(midi_in_port)
        midi_in.close_port()
        midi_in.open_port(midi_in_port)
        midi_in_d.set(available_in_ports[midi_in_port])
        midi_in_message()
        conf["midi_in_port"] = midi_in_port
        save_conf()

    except:
        midi_in_d.set(available_in_ports[available_in_ports.index('None')])
        conf["midi_in_port"] = available_in_ports.index('None')
        save_conf()

def select_midi_out_d(event):
    try:
        midi_out_port = midi_out_d.get()
        midi_out_port = available_out_ports.index(midi_out_port)
        midi_out.close_port()
        midi_out.open_port(midi_out_port)
        midi_out_d.set(available_out_ports[midi_out_port])
        conf["midi_out_port"] = midi_out_port
        save_conf()
    except:
        midi_out_d.set(available_out_ports[available_out_ports.index('None')])
        conf["midi_out_port"] = available_out_ports.index('None')
        save_conf()

def select_midi_k_d(event):
    try:
        midi_k_port = midi_k_d.get()
        midi_k_port = available_k_ports.index(midi_k_port)
        midi_k.close_port()
        midi_k.open_port(midi_k_port)
        midi_k_d.set(available_k_ports[midi_k_port])
        midi_k_message()
        conf["midi_k_port"] = midi_k_port
        save_conf()
    except:
        midi_k_d.set(available_k_ports[available_k_ports.index('None')])
        conf["midi_k_port"] = available_k_ports.index('None')
        save_conf()

def press_note(event):
    w = event.widget
    if isinstance(w, tk.Button):

        name = w.cget("text")
        value = int(w_value[w_name.index(name)])
        com = int(w_com[w_name.index(name)])
        if DEBUG:
            print('name', name, 'com', com, value, 'value')

        midi_out.send_message([0x90 + m_ch, com, value])

def release_note(event):
    w = event.widget
    if isinstance(w, tk.Button):
        name = w.cget("text")
        value = int(w_value[w_name.index(name)])
        com = int(w_com[w_name.index(name)])
        if DEBUG:
            print('name', name, 'com', com, value, 'value')

        midi_out.send_message([0x80 + m_ch, com, value])

def click_button(event):
    w = event.widget
    if isinstance(w, tk.Button):
        name = w.cget("text")
        value = int(w_value[w_name.index(name)])
        com = int(w_com[w_name.index(name)])
        if DEBUG:
            print('name', name, 'com', com, value, 'value')

        midi_out.send_message([0xB0 + m_ch, com, value])

def update_control():
    for x in range(1, len(control)):
        try:
            if w_type[x] == 0 or w_type[x] == 3:
                control[x][4] = widget[x]['state']
            else:
                control[x][4] = widget[x].get()
        except:
            pass
def read_var(file, var_name):
    for a in file:
        if var_name + '\t= ' in a:
            var_val = int(a.replace(var_name + '\t= ', ''))
            return var_val
def read_step_note(file):
    step_note = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]] * 64
    var_names = ['NOTE1', 'VELO1', 'LENG1', 'NOTE2', 'VELO2', 'LENG2', 'NOTE3', 'VELO3', 'LENG3', 'NOTE4', 'VELO4',
                 'LENG4', 'SUBSTEP', 'PROB']
    for a in file:
        if 'STEP_NOTE' in a:
            for s in range(0, len(step_note)):
                for v in range(0, len(var_names)):
                    var_name = var_names[v]
                    var_pos = a.find(var_name + '=')
                    var_val_len = len(var_name) + 1
                    val = 0
                    i = 0
                    while -1:

                        var_val = a[var_pos + var_val_len: var_pos + var_val_len + i]
                        var_val = var_val
                        val = a[var_pos + var_val_len + i: var_pos + var_val_len + i + 1]
                        if val == ' ' or val == '':
                            break

                        i = i + 1
                    if '\n' in var_val:
                        var_val = var_val.replace('\n', '')
                    step_note[s][v] = int(var_val)
    if DEBUG:
        print(step_note)
    return step_note
def read_step_motion(file):
    step_motion = [[1, 2, 3, 4, 5, 6, 7, 8, 9]] * 512
    var_names = ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'PB']
    for a in file:
        if 'STEP_MOTION' in a:
            for s in range(0, len(step_motion)):
                for v in range(0, len(var_names)):
                    var_name = var_names[v]
                    var_pos = a.find(var_name + '=')
                    var_val_len = len(var_name) + 1
                    val = 0
                    i = 0
                    while -1:

                        var_val = a[var_pos + var_val_len: var_pos + var_val_len + i]
                        var_val = var_val
                        val = a[var_pos + var_val_len + i: var_pos + var_val_len + i + 1]
                        if val == ' ' or val == '':
                            break

                        i = i + 1
                    if '\n' in var_val:
                        var_val = var_val.replace('\n', '')
                    step_motion[s][v] = int(var_val)

    return step_motion

with open('TEST.PRM', 'r') as file:
    LENG = int(read_var(file,'LENG') / 2)
    SCALE = int(read_var(file, 'SCALE') / 2)
    TRANSPOSE = int(read_var(file, 'TRANSPOSE') / 2)
    LEVEL = int(read_var(file, 'LEVEL') / 2)
    TEMPO = int(read_var(file, 'TEMPO') / 2)
    SHUFFLE = int(read_var(file, 'SHUFFLE') / 2)
    ARP_TYPE = int(read_var(file, 'ARP_TYPE') / 2)
    ARP_RATE = int(read_var(file, 'ARP_RATE') / 2)
    MOTION_CC1 = int(read_var(file, 'MOTION_CC1') / 2)
    MOTION_CC2 = int(read_var(file, 'MOTION_CC2') / 2)
    MOTION_CC3 = int(read_var(file, 'MOTION_CC3') / 2)
    MOTION_CC4 = int(read_var(file, 'MOTION_CC4') / 2)
    MOTION_CC5 = int(read_var(file, 'MOTION_CC5') / 2)
    MOTION_CC6 = int(read_var(file, 'MOTION_CC6') / 2)
    MOTION_CC7 = int(read_var(file, 'MOTION_CC7') / 2)
    MOTION_CC8 = int(read_var(file, 'MOTION_CC8') / 2)
    LFO_RATE = int(read_var(file, 'LFO_RATE') / 2)
    LFO_WAVE_FORM = int(read_var(file, 'LFO_WAVE_FORM') / 2)
    VCO_MOD_DEPTH = int(read_var(file, 'VCO_MOD_DEPTH') / 2)
    VCO_RANGE = int(read_var(file, 'VCO_RANGE') / 2)
    VCO_PULSE_WIDTH = int(read_var(file, 'VCO_PULSE_WIDTH') / 2)
    VCO_PWM_SOURCE = int(read_var(file, 'VCO_PWM_SOURCE') / 2)
    VCO_PWM_LEVEL = int(read_var(file, 'VCO_PWM_LEVEL') / 2)
    VCO_SAW_LEVEL = int(read_var(file, 'VCO_SAW_LEVEL') / 2)
    VCO_SUB_LEVEL = int(read_var(file, 'VCO_SUB_LEVEL') / 2)
    VCO_SUB_TYPE = int(read_var(file, 'VCO_SUB_TYPE') / 2)
    VCO_NOISE_LEVEL = int(read_var(file, 'VCO_NOISE_LEVEL') / 2)
    VCF_CUTOFF = int(read_var(file, 'VCF_CUTOFF') / 2)
    VCF_RESONANCE = int(read_var(file, 'VCF_RESONANCE') / 2)
    VCF_ENV_DEPTH = int(read_var(file, 'VCF_ENV_DEPTH') / 2)
    VCF_MOD_DEPTH = int(read_var(file, 'VCF_MOD_DEPTH') / 2)
    VCF_KEY_FOLLOW = int(read_var(file, 'VCF_KEY_FOLLOW') / 2)
    VCA_ENV_MODE = int(read_var(file, 'VCA_ENV_MODE') / 2)
    ENV_TRG_MODE = int(read_var(file, 'ENV_TRG_MODE') / 2)
    ENV_ATTACK = int(read_var(file, 'ENV_ATTACK') / 2)
    ENV_DECAY = int(read_var(file, 'ENV_DECAY') / 2)
    ENV_SUSTAIN = int(read_var(file, 'ENV_SUSTAIN') / 2)
    ENV_RELEASE = int(read_var(file, 'ENV_RELEASE') / 2)
    ASSIGN_MODE = int(read_var(file, 'ASSIGN_MODE') / 2)
    CHORD_VOICE2_SW = int(read_var(file, 'CHORD_VOICE2_SW') / 2)
    CHORD_VOICE3_SW = int(read_var(file, 'CHORD_VOICE3_SW') / 2)
    CHORD_VOICE4_SW = int(read_var(file, 'CHORD_VOICE4_SW') / 2)
    CHORD_VOICE2_KEY_SHIFT = int(read_var(file, 'CHORD_VOICE2_KEY_SHIFT') / 2)
    CHORD_VOICE3_KEY_SHIFT = int(read_var(file, 'CHORD_VOICE3_KEY_SHIFT') / 2)
    CHORD_VOICE4_KEY_SHIFT = int(read_var(file, 'CHORD_VOICE4_KEY_SHIFT') / 2)
    VCO_BEND_SENS = int(read_var(file, 'VCO_BEND_SENS') / 2)
    VCF_BEND_SENS = int(read_var(file, 'VCF_BEND_SENS') / 2)
    LFO_MOD_DEPTH = int(read_var(file, 'LFO_MOD_DEPTH') / 2)
    PORTAMENTO_MODE = int(read_var(file, 'PORTAMENTO_MODE') / 2)
    PORTAMENTO_TIME = int(read_var(file, 'PORTAMENTO_TIME') / 2)
    NOISE_MODE = int(read_var(file, 'NOISE_MODE') / 2)
    LFO_MODE = int(read_var(file, 'LFO_MODE') / 2)
    FINE_TUNE = int(read_var(file, 'FINE_TUNE') / 2)
    TEMPO_SYNC = int(read_var(file, 'TEMPO_SYNC') / 2)
    CHORUS = int(read_var(file, 'CHORUS') / 2)
    DELAY_LEVEL = int(read_var(file, 'DELAY_LEVEL') / 2)
    DELAY_TIME = int(read_var(file, 'DELAY_TIME') / 2)
    DELAY_TEMPO = int(read_var(file, 'DELAY_TEMPO') / 2)
    DELAY_FEEDBACK = int(read_var(file, 'DELAY_FEEDBACK') / 2)
    DELAY_LOW_CUT = int(read_var(file, 'DELAY_LOW_CUT') / 2)
    DELAY_HIGH_CUT = int(read_var(file, 'DELAY_HIGH_CUT') / 2)
    DELAY_SW = int(read_var(file, 'DELAY_SW') / 2)
    REVERB_TYPE = int(read_var(file, 'REVERB_TYPE') / 2)
    REVERB_TIME = int(read_var(file, 'REVERB_TIME') / 2)
    REVERB_LEVEL = int(read_var(file, 'REVERB_LEVEL') / 2)
    REVERB_PRE_DELAY = int(read_var(file, 'REVERB_PRE_DELAY') / 2)
    REVERB_LOW_CUT = int(read_var(file, 'REVERB_LOW_CUT') / 2)
    REVERB_HIGH_CUT = int(read_var(file, 'REVERB_HIGH_CUT') / 2)
    REVERB_DENSITY = int(read_var(file, 'REVERB_DENSITY') / 2)
    OSC_DRAW_SW = int(read_var(file, 'OSC_DRAW_SW') / 2)
    OSC_DRAW_MULT = int(read_var(file, 'OSC_DRAW_MULT') / 2)
    OSC_DRAW_P1 = int(read_var(file, 'OSC_DRAW_P1') / 2)
    OSC_DRAW_P2 = int(read_var(file, 'OSC_DRAW_P2') / 2)
    OSC_DRAW_P3 = int(read_var(file, 'OSC_DRAW_P3') / 2)
    OSC_DRAW_P4 = int(read_var(file, 'OSC_DRAW_P4') / 2)
    OSC_DRAW_P5 = int(read_var(file, 'OSC_DRAW_P5') / 2)
    OSC_DRAW_P6 = int(read_var(file, 'OSC_DRAW_P6') / 2)
    OSC_DRAW_P7 = int(read_var(file, 'OSC_DRAW_P7') / 2)
    OSC_DRAW_P8 = int(read_var(file, 'OSC_DRAW_P8') / 2)
    OSC_CHOP_TYPE = int(read_var(file, 'OSC_CHOP_TYPE') / 2)
    OSC_CHOP_OVERTONE = int(read_var(file, 'OSC_CHOP_OVERTONE') / 2)
    OSC_CHOP_COMB_TYPE = int(read_var(file, 'OSC_CHOP_COMB_TYPE') / 2)
    OSC_CHOP_COMB = int(read_var(file, 'OSC_CHOP_COMB') / 2)
    OSC_CHOP_PWM = int(read_var(file, 'OSC_CHOP_PWM') / 2)
    OSC_CHOP_SAW = int(read_var(file, 'OSC_CHOP_SAW') / 2)
    OSC_CHOP_SUB = int(read_var(file, 'OSC_CHOP_SUB') / 2)
    OSC_CHOP_NOISE = int(read_var(file, 'OSC_CHOP_NOISE') / 2)
    RISER_MODE = int(read_var(file, 'RISER_MODE') / 2)
    RISER_SW = int(read_var(file, 'RISER_SW') / 2)
    RISER_CTRL = int(read_var(file, 'RISER_CTRL') / 2)
    RISER_BEAT = int(read_var(file, 'RISER_BEAT') / 2)
    RISER_RESO = int(read_var(file, 'RISER_RESO') / 2)
    RISER_LEVEL = int(read_var(file, 'RISER_LEVEL') / 2)
    DM_ASSIGN_X = int(read_var(file, 'DM_ASSIGN_X') / 2)
    DM_ASSIGN_Y = int(read_var(file, 'DM_ASSIGN_Y') / 2)
    DM_ASSIGN_TAP = int(read_var(file, 'DM_ASSIGN_TAP') / 2)
    DM_ASSIGN_FF = int(read_var(file, 'DM_ASSIGN_FF') / 2)
    DM_SENS_X = int(read_var(file, 'DM_SENS_X') / 2)
    DM_SENS_Y = int(read_var(file, 'DM_SENS_Y') / 2)
    LFO_KEY_TRIG = int(read_var(file, 'LFO_KEY_TRIG') / 2)
    LFO_SYNC = int(read_var(file, 'LFO_SYNC') / 2)
    RISER_SHAPE = int(read_var(file, 'RISER_SHAPE') / 2)
    PRM1 = int(read_var(file, 'PRM1') / 2)
    PRM2 = int(read_var(file, 'PRM2') / 2)
    PRM3 = int(read_var(file, 'PRM3') / 2)
    PRM4 = int(read_var(file, 'PRM4') / 2)
    PRM5 = int(read_var(file, 'PRM5') / 2)
    PRM6 = int(read_var(file, 'PRM6') / 2)
    PRM7 = int(read_var(file, 'PRM7') / 2)
    PRM8 = int(read_var(file, 'PRM8') / 2)
    PRM9 = int(read_var(file, 'PRM9') / 2)
    PRM10 = int(read_var(file, 'PRM10') / 2)
    PRM11 = int(read_var(file, 'PRM11') / 2)


    control1 = [["27.FILT BEND S", 27, VCF_BEND_SENS, 0, 0],
               ["28.AMP ENV M", 28, VCA_ENV_MODE, 0, 0],
               ["29.ENV TR MODE", 29, ENV_TRG_MODE, 0, 0],
               ["26.FILT_KEYB_F", 26, 0, 0, 0],
               ["92.DELAY LEVEL", 92, DELAY_LEVEL, 0, 0],
               ["90.DELAY TIME", 90, DELAY_TIME, 0, 0],
               ["91.REVERB LEVEL", 91, REVERB_LEVEL, 0, 0],
               ["89.REVERB TIME", 89, REVERB_TIME, 0, 0],
               ["93.CHORUS", 93, CHORUS, 0, 0],
               ["1.MOD WHEEL", 1, 0, 0, 0],
               ["65.PORTAM", 65, 0, 0, 0],
               ["10.PAN", 10, 63, 0, 0],
               ["11.EXP PEDAL", 11, 127, 0, 0],
               ["64.DAMP P", 64, 0, 0, 0],
               ["74.FREQ", 74, VCF_CUTOFF, 0, 0],
               ["71.RESON", 71, VCF_RESONANCE, 0, 0],
               ["25.LFO", 25, VCF_MOD_DEPTH, 0, 0],
               ["24.ENVELOPE", 24, VCF_ENV_DEPTH, 0, 0],
               ["26.FILT KEYB F", 26, VCF_KEY_FOLLOW, 0, 0],
               ["3.LFO RATE", 3, LFO_RATE, 0, 0],
               ["12.WAVE FORM", 12, LFO_WAVE_FORM, 0, 0],
               ["79.LFO MODE", 79, LFO_MODE, 0, 0],
               ["106.LFO SYNC", 106, LFO_SYNC, 0, 0],
               ["14.OSC RANGE", 14, VCO_RANGE, 0, 0],
               ["13.OSC LFO", 13, VCO_MOD_DEPTH, 0, 0],
               ["76.FINE TUNE", 76, FINE_TUNE, 0, 0],
               ["103.OSC CHOP", 103, OSC_CHOP_OVERTONE, 0, 0],
               ["19.SQUARE W L", 19, VCO_PWM_LEVEL, 0, 0],
               ["20.SAWT W L", 20, VCO_SAW_LEVEL, 0, 0],
               ["15.OSC PWIDTH", 15, VCO_PULSE_WIDTH, 0, 0],
               ["107.OSC DW SW", 107, OSC_DRAW_SW, 0, 0],
               ["102.OSC DRAW M", 102, OSC_DRAW_MULT, 0, 0],
               ["23.OSC NOISE L", 23, VCO_NOISE_LEVEL, 0, 0],
               ["78.NOISE MODE", 78, NOISE_MODE, 0, 0],
               ["21.OSC S-LEVEL", 21, VCO_SUB_LEVEL, 0, 0],
               ["104.OSC CHOP C", 104, OSC_CHOP_COMB, 0, 0],
               ["73.ATTACK", 73, ENV_ATTACK, 0, 0],
               ["75.DECAY", 75, ENV_DECAY, 0, 0],
               ["30.SUSTAIN", 30, ENV_SUSTAIN, 0, 0],
               ["72.RELEASE", 72, ENV_RELEASE, 0, 0],
               ["16.OSC PWM S ", 16, VCO_PWM_SOURCE, 0, 0],
               ["17.LFO MOD D", 17, LFO_MOD_DEPTH, 0, 0],
               ["18.OSC BEND S", 18, VCO_BEND_SENS, 0, 0],
               ["22.OSC S-TYPE", 22, VCO_SUB_TYPE, 0, 0],
               ["80.POLY MODE", 80, 2, 0, 0],
               ["31.PORT MODE", 31, PORTAMENTO_MODE, 0, 0],
               ["5.PORT TIME", 5, PORTAMENTO_TIME, 0, 0],
               ["105.LFO KEY T", 105, LFO_KEY_TRIG, 0, 0],
               ["77.TRANSP SW", 77, TRANSPOSE, 0, 0],
               ["81.CHORD V2 SW", 81, CHORD_VOICE2_SW, 0, 0],
               ["82.CHORD V3 SW", 82, CHORD_VOICE3_SW, 0, 0],
               ["83.CHORD V4 SW", 83, CHORD_VOICE4_SW, 0, 0],
               ["85.CHORD V2 KS", 85, CHORD_VOICE2_KEY_SHIFT, 0, 0],
               ["86.CHORD V3 KS", 86, CHORD_VOICE3_KEY_SHIFT, 0, 0],
               ["87.CHORD V4 KS", 87, CHORD_VOICE4_KEY_SHIFT, 0, 0]]

with open('TEST.PRM', 'r') as file:
    STEP_NOTE = read_step_note(file)

with open('TEST.PRM', 'r') as file:
    STEP_MOTION = read_step_motion(file)
def load_default():
    global control
    global filehandle

    try:
        with open('default.ptc', 'r') as file:
            control = json.load(file)
    # control = [["27.FILT BEND S", 27, VCF_BEND_SENS, 0, 0],
    #            ["28.AMP ENV M", 28, VCA_ENV_MODE, 0, 0],
    #            ["29.ENV TR MODE", 29, ENV_TRG_MODE, 0, 0],
    #            ["26.FILT_KEYB_F", 26, 0, 0, 0],
    #            ["92.DELAY LEVEL", 92, DELAY_LEVEL, 0, 0],
    #            ["90.DELAY TIME", 90, DELAY_TIME, 0, 0],
    #            ["91.REVERB LEVEL", 91, REVERB_LEVEL, 0, 0],
    #            ["89.REVERB TIME", 89, REVERB_TIME, 0, 0],
    #            ["93.CHORUS", 93, CHORUS, 0, 0],
    #            ["1.MOD WHEEL", 1, 0, 0, 0],
    #            ["65.PORTAM", 65, 0, 0, 0],
    #            ["10.PAN", 10, 63, 0, 0],
    #            ["11.EXP PEDAL", 11, 127, 0, 0],
    #            ["64.DAMP P", 64, 0, 0, 0],
    #            ["74.FREQ", 74, VCF_CUTOFF, 0, 0],
    #            ["71.RESON", 71, VCF_RESONANCE, 0, 0],
    #            ["25.LFO", 25, VCF_MOD_DEPTH, 0, 0],
    #            ["24.ENVELOPE", 24, VCF_ENV_DEPTH, 0, 0],
    #            ["26.FILT KEYB F", 26, VCF_KEY_FOLLOW, 0, 0],
    #            ["3.LFO RATE", 3, LFO_RATE, 0, 0],
    #            ["12.WAVE FORM", 12, LFO_WAVE_FORM, 0, 0],
    #            ["79.LFO MODE", 79, LFO_MODE, 0, 0],
    #            ["106.LFO SYNC", 106, LFO_SYNC, 0, 0],
    #            ["14.OSC RANGE", 14, VCO_RANGE, 0, 0],
    #            ["13.OSC LFO", 13, VCO_MOD_DEPTH, 0, 0],
    #            ["76.FINE TUNE", 76, FINE_TUNE, 0, 0],
    #            ["103.OSC CHOP", 103, OSC_CHOP_OVERTONE, 0, 0],
    #            ["19.SQUARE W L", 19, VCO_PWM_LEVEL, 0, 0],
    #            ["20.SAWT W L", 20, VCO_SAW_LEVEL, 0, 0],
    #            ["15.OSC PWIDTH", 15, VCO_PULSE_WIDTH, 0, 0],
    #            ["107.OSC DW SW", 107, OSC_DRAW_SW, 0, 0],
    #            ["102.OSC DRAW M", 102, OSC_DRAW_MULT, 0, 0],
    #            ["23.OSC NOISE L", 23, VCO_NOISE_LEVEL, 0, 0],
    #            ["78.NOISE MODE", 78, NOISE_MODE, 0, 0],
    #            ["21.OSC S-LEVEL", 21, VCO_SUB_LEVEL, 0, 0],
    #            ["104.OSC CHOP C", 104, OSC_CHOP_COMB, 0, 0],
    #            ["73.ATTACK", 73, ENV_ATTACK, 0, 0],
    #            ["75.DECAY", 75, ENV_DECAY, 0, 0],
    #            ["30.SUSTAIN", 30, ENV_SUSTAIN, 0, 0],
    #            ["72.RELEASE", 72, ENV_RELEASE, 0, 0],
    #            ["16.OSC PWM S ", 16, VCO_PWM_SOURCE, 0, 0],
    #            ["17.LFO MOD D", 17, LFO_MOD_DEPTH, 0, 0],
    #            ["18.OSC BEND S", 18, VCO_BEND_SENS, 0, 0],
    #            ["22.OSC S-TYPE", 22, VCO_SUB_TYPE, 0, 0],
    #            ["80.POLY MODE", 80, 2, 0, 0],
    #            ["31.PORT MODE", 31, PORTAMENTO_MODE, 0, 0],
    #            ["5.PORT TIME", 5, PORTAMENTO_TIME, 0, 0],
    #            ["105.LFO KEY T", 105, LFO_KEY_TRIG, 0, 0],
    #            ["77.TRANSP SW", 77, TRANSPOSE, 0, 0],
    #            ["81.CHORD V2 SW", 81, CHORD_VOICE2_SW, 0, 0],
    #            ["82.CHORD V3 SW", 82, CHORD_VOICE3_SW, 0, 0],
    #            ["83.CHORD V4 SW", 83, CHORD_VOICE4_SW, 0, 0],
    #            ["85.CHORD V2 KS", 85, CHORD_VOICE2_KEY_SHIFT, 0, 0],
    #            ["86.CHORD V3 KS", 86, CHORD_VOICE3_KEY_SHIFT, 0, 0],
    #            ["87.CHORD V4 KS", 87, CHORD_VOICE4_KEY_SHIFT, 0, 0]]
    except:
        def_patch = [["1.MOD WHEEL", 1, 0, 0, 0],
                   ["3.LFO RATE", 3, 3, 0, 0],
                   ["5.PORT TIME", 5, 0, 0, 0],
                   ["10.PAN", 10, 63, 0, 0],
                   ["11.EXP PEDAL", 11, 127, 0, 0],
                   ["12.WAVE FORM", 12, 3, 0, 0],
                   ["13.OSC LFO", 13, 127, 0, 0],
                   ["14.OSC RANGE", 14, 3, 0, 0],
                   ["15.OSC PWIDTH", 15, 88, 0, 0],
                   ["16.OSC PWM S ", 16, 0, 0, 0],
                   ["17.LFO MOD D", 17, 0, 0, 0],
                   ["18.OSC BEND S", 18, 0, 0, 0],
                   ["19.SQUARE W L", 19, 30, 0, 0],
                   ["20.SAWT W L", 20, 0, 0, 0],
                   ["21.OSC S-LEVEL", 21, 17, 0, 0],
                   ["22.OSC S-TYPE", 22, 0, 0, 0],
                   ["23.OSC NOISE L", 23, 0, 0, 0],
                   ["24.ENVELOPE", 24, 0, 0, 0],
                   ["25.LFO", 25, 0, 0, 0],
                   ["26.FILT_KEYB_F", 26, 0, 0, 0],
                   ["27.FILT BEND S", 27, 0, 0, 0],
                   ["28.AMP ENV M", 28, 0, 0, 0],
                   ["29.ENV TR MODE", 29, 0, 0, 0],
                   ["30.SUSTAIN", 30, 92, 0, 0],
                   ["31.PORT MODE", 31, 0, 0, 0],
                   ["64.DAMP P", 64, 0, 0, 0],
                   ["65.PORTAM", 65, 0, 0, 0],
                   ["71.RESON", 71, 86, 0, 0],
                   ["72.RELEASE", 72, 50, 0, 0],
                   ["73.ATTACK", 73, 0, 0, 0],
                   ["74.FREQ", 74, 86, 0, 0],
                   ["75.DECAY", 75, 127, 0, 0],
                   ["76.FINE TUNE", 76, 69, 0, 0],
                   ["77.TRANSP SW", 77, 0, 0, 0],
                   ["78.NOISE MODE", 78, 1, 0, 0],
                   ["79.LFO MODE", 79, 0, 0, 0],
                   ["80.POLY MODE", 80, 2, 0, 0],
                   ["81.CHORD V2 SW", 81, 0, 0, 0],
                   ["82.CHORD V3 SW", 82, 0, 0, 0],
                   ["83.CHORD V4 SW", 83, 0, 0, 0],
                   ["85.CHORD V2 KS", 85, 52, 0, 0],
                   ["86.CHORD V3 KS", 86, 52, 0, 0],
                   ["87.CHORD V4 KS", 87, 52, 0, 0],
                   ["89.REVERB TIME", 89, 103, 0, 0],
                   ["90.DELAY TIME", 90, 12, 0, 0],
                   ["91.REVERB LEVEL", 91, 103, 0, 0],
                   ["92.DELAY LEVEL", 92, 105, 0, 0],
                   ["93.CHORUS", 93, 2, 0, 0],
                   ["102.OSC DRAW M", 102, 105, 0, 0],
                   ["103.OSC CHOP", 103, 60, 0, 0],
                   ["104.OSC CHOP C", 104, 103, 0, 0],
                   ["105.LFO KEY T", 105, 0, 0, 0],
                   ["106.LFO SYNC", 106, 0, 0, 0],
                   ["107.OSC DW SW", 107, 0, 0, 0]]

        for x in range(0, len(control)):
            for xx in range(0, len(def_patch)):
                try:
                    if def_patch[xx][1] == x:
                        control[x] = def_patch[xx]
                except:
                    pass


    global w_name
    global w_type
    global w_com
    global w_value
    w_name = [0] * len(control)
    w_type = [0] * len(control)
    w_com = [0] * len(control)
    w_value = [0] * len(control)

    info_label['text'] = 'default'
    set_all_widget_value()
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
        with open(filehandle, 'r') as file:
            control = json.load(file)
        set_all_widget_value()
        f = filehandle.split("/")[-1]
        info_label['text'] = f


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
widget[27] = tk.Scale(frame_extra2)
current_value[27] = tk.IntVar()
widget[27].configure(
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
widget[27].place(anchor="nw", x=10, y=20)
widget[27].bind("<ButtonRelease>", update_value)
widget[27].bind("<B1-Motion>", update_value)
widget_label[27] = tk.Label(frame_extra2)
widget_label[27].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[27].place(anchor="nw", x=30, y=60)
######
widget[28] = tk.Scale(frame_extra2)
current_value[28] = tk.IntVar()
widget[28].configure(
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
widget[28].place(anchor="nw", x=150, y=20)
widget[28].bind("<ButtonRelease>", update_value)
widget[28].bind("<B1-Motion>", update_value)
widget_label[28] = tk.Label(frame_extra2)
widget_label[28].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[28].place(anchor="nw", x=170, y=60)
######
widget[29] = tk.Scale(frame_extra2)
current_value[29] = tk.IntVar()
widget[29].configure(
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
widget[29].place(anchor="nw", x=290, y=20)
widget[29].bind("<ButtonRelease>", update_value)
widget[29].bind("<B1-Motion>", update_value)
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
widget[92] = tk.Scale(frame_efx)
current_value[92] = tk.IntVar()
widget[92].configure(
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
widget[92].place(anchor="nw", x=10, y=20)
widget[92].bind("<ButtonRelease>", update_value)
widget[92].bind("<B1-Motion>", update_value)
widget_label[92] = tk.Label(frame_efx)
widget_label[92].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[92].place(anchor="nw", x=30, y=60)
widget[90] = tk.Scale(frame_efx)
current_value[90] = tk.IntVar()
widget[90].configure(
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
widget[90].place(anchor="nw", x=150, y=20)
widget[90].bind("<ButtonRelease>", update_value)
widget[90].bind("<B1-Motion>", update_value)
widget_label[90] = tk.Label(frame_efx)
widget_label[90].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[90].place(anchor="nw", x=170, y=60)
widget[91] = tk.Scale(frame_efx)
current_value[91] = tk.IntVar()
widget[91].configure(
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
widget[91].place(anchor="nw", x=290, y=20)
widget[91].bind("<ButtonRelease>", update_value)
widget[91].bind("<B1-Motion>", update_value)
widget_label[91] = tk.Label(frame_efx)
widget_label[91].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[91].place(anchor="nw", x=310, y=60)
widget[89] = tk.Scale(frame_efx)
current_value[89] = tk.IntVar()
widget[89].configure(
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
widget[89].place(anchor="nw", x=430, y=20)
widget[89].bind("<ButtonRelease>", update_value)
widget[89].bind("<B1-Motion>", update_value)
widget_label[89] = tk.Label(frame_efx)
widget_label[89].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[89].place(anchor="nw", x=450, y=60)
widget[93] = tk.Scale(frame_efx)
current_value[93] = tk.IntVar()
widget[93].configure(
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
widget[93].place(anchor="nw", x=570, y=20)
widget[93].bind("<ButtonRelease>", update_value)
widget[93].bind("<B1-Motion>", update_value)
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
widget[1] = tk.Scale(frame_controller)
current_value[1] = tk.IntVar()
widget[1].configure(
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
widget[1].place(anchor="nw", x=10, y=150)
widget[1].bind("<ButtonRelease>", update_value)
widget[1].bind("<B1-Motion>", update_value)
widget_label[1] = tk.Label(frame_controller)
widget_label[1].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[1].place(anchor="nw", x=30, y=190)
widget[65] = tk.Scale(frame_controller)
current_value[65] = tk.IntVar()
widget[65].configure(
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
widget[65].place(anchor="nw", x=10, y=410)
widget[65].bind("<ButtonRelease>", update_value)
widget[65].bind("<B1-Motion>", update_value)
widget_label[65] = tk.Label(frame_controller)
widget_label[65].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[65].place(anchor="nw", x=30, y=450)
widget[10] = tk.Scale(frame_controller)
current_value[10] = tk.IntVar()
widget[10].configure(
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
widget[10].place(anchor="nw", x=10, y=25)
widget[10].bind("<ButtonRelease>", update_value)
widget[10].bind("<B1-Motion>", update_value)
widget_label[10] = tk.Label(frame_controller)
widget_label[10].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[10].place(anchor="nw", x=10, y=70)
widget[11] = tk.Scale(frame_controller)
current_value[11] = tk.IntVar()
widget[11].configure(
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
widget[11].place(anchor="nw", x=10, y=280)
widget[11].bind("<ButtonRelease>", update_value)
widget[11].bind("<B1-Motion>", update_value)
widget_label[11] = tk.Label(frame_controller)
widget_label[11].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[11].place(anchor="nw", x=30, y=320)
widget[64] = tk.Scale(frame_controller)
current_value[64] = tk.IntVar()
widget[64].configure(
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
widget[64].place(anchor="nw", x=10, y=540)
widget[64].bind("<ButtonRelease>", update_value)
widget[64].bind("<B1-Motion>", update_value)
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
widget[74] = tk.Scale(frame_filter)
current_value[74] = tk.IntVar()
widget[74].configure(
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
widget[74].place(anchor="nw", x=10, y=20)
widget[74].bind("<ButtonRelease>", update_value)
widget[74].bind("<B1-Motion>", update_value)
widget_label[74] = tk.Label(frame_filter)
widget_label[74].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[74].place(anchor="nw", x=30, y=60)
widget[71] = tk.Scale(frame_filter)
current_value[71] = tk.IntVar()
widget[71].configure(
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
widget[71].place(anchor="nw", x=150, y=20)
widget[71].bind("<ButtonRelease>", update_value)
widget[71].bind("<B1-Motion>", update_value)
widget_label[71] = tk.Label(frame_filter)
widget_label[71].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[71].place(anchor="nw", x=170, y=60)
widget[25] = tk.Scale(frame_filter)
current_value[25] = tk.IntVar()
widget[25].configure(
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
widget[25].place(anchor="nw", x=290, y=20)
widget[25].bind("<ButtonRelease>", update_value)
widget[25].bind("<B1-Motion>", update_value)
widget_label[25] = tk.Label(frame_filter)
widget_label[25].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[25].place(anchor="nw", x=310, y=60)
widget[24] = tk.Scale(frame_filter)
current_value[24] = tk.IntVar()
widget[24].configure(
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
widget[24].place(anchor="nw", x=430, y=20)
widget[24].bind("<ButtonRelease>", update_value)
widget[24].bind("<B1-Motion>", update_value)
widget_label[24] = tk.Label(frame_filter)
widget_label[24].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[24].place(anchor="nw", x=450, y=60)
widget[26] = tk.Scale(frame_filter)
current_value[26] = tk.IntVar()
widget[26].configure(
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
widget[26].place(anchor="nw", x=570, y=20)
widget[26].bind("<ButtonRelease>", update_value)
widget[26].bind("<B1-Motion>", update_value)
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
widget[3] = tk.Scale(frame_lfo)
current_value[3] = tk.IntVar()
widget[3].configure(
    from_=len(extra_data[3]),
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
widget[3].place(anchor="nw", relx=0.0, x=10, y=20)
widget[3].bind("<ButtonRelease>", update_value)
widget[3].bind("<B1-Motion>", update_value)
widget_label[3] = tk.Label(frame_lfo)
widget_label[3].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[3].place(anchor="nw", x=30, y=60)
######
widget[12] = tk.Scale(frame_lfo)
current_value[12] = tk.IntVar()
widget[12].configure(
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
widget[12].place(anchor="nw", x=10, y=150)
widget[12].bind("<ButtonRelease>", update_value)
widget[12].bind("<B1-Motion>", update_value)
widget_label[12] = tk.Label(frame_lfo)
widget_label[12].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[12].place(anchor="nw", x=30, y=190)
######
widget[79] = tk.Scale(frame_lfo)
current_value[79] = tk.IntVar()
widget[79].configure(
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
widget[79].place(anchor="nw", relx=0.0, x=150, y=20)
widget[79].bind("<ButtonRelease>", update_value)
widget[79].bind("<B1-Motion>", update_value)
widget_label[79] = tk.Label(frame_lfo)
widget_label[79].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[79].place(anchor="nw", x=170, y=60)
widget[106] = tk.Scale(frame_lfo)
current_value[106] = tk.IntVar()
widget[106].configure(
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
widget[106].place(anchor="nw", x=150, y=150)
widget[106].bind("<ButtonRelease>", update_value)
widget[106].bind("<B1-Motion>", update_value)
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
widget[14] = tk.Scale(frame_oscillator)
current_value[14] = tk.IntVar()
widget[14].configure(
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
widget[14].place(anchor="nw", x=10, y=20)
widget[14].bind("<ButtonRelease>", update_value)
widget[14].bind("<B1-Motion>", update_value)
widget_label[14] = tk.Label(frame_oscillator)
widget_label[14].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[14].place(anchor="nw", x=30, y=60)
widget[13] = tk.Scale(frame_oscillator)
current_value[13] = tk.IntVar()
widget[13].configure(
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
widget[13].place(anchor="nw", x=10, y=150)
widget[13].bind("<ButtonRelease>", update_value)
widget[13].bind("<B1-Motion>", update_value)
widget_label[13] = tk.Label(frame_oscillator)
widget_label[13].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[13].place(anchor="nw", x=30, y=190)
widget[76] = tk.Scale(frame_oscillator)
current_value[76] = tk.IntVar()
widget[76].configure(
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
widget[76].place(anchor="nw", x=150, y=20)
widget[76].bind("<ButtonRelease>", update_value)
widget[76].bind("<B1-Motion>", update_value)
widget_label[76] = tk.Label(frame_oscillator)
widget_label[76].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[76].place(anchor="nw", x=170, y=60)
widget[103] = tk.Scale(frame_oscillator)
current_value[103] = tk.IntVar()
widget[103].configure(
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
widget[103].place(anchor="nw", x=150, y=150)
widget[103].bind("<ButtonRelease>", update_value)
widget[103].bind("<B1-Motion>", update_value)
widget_label[103] = tk.Label(frame_oscillator)
widget_label[103].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[103].place(anchor="nw", x=170, y=190)
widget[19] = tk.Scale(frame_oscillator)
current_value[19] = tk.IntVar()
widget[19].configure(
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
widget[19].place(anchor="nw", x=290, y=20)
widget[19].bind("<ButtonRelease>", update_value)
widget[19].bind("<B1-Motion>", update_value)
widget_label[19] = tk.Label(frame_oscillator)
widget_label[19].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[19].place(anchor="nw", x=310, y=60)
widget[20] = tk.Scale(frame_oscillator)
current_value[20] = tk.IntVar()
widget[20].configure(
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
widget[20].place(anchor="nw", x=290, y=150)
widget[20].bind("<ButtonRelease>", update_value)
widget[20].bind("<B1-Motion>", update_value)
widget_label[20] = tk.Label(frame_oscillator)
widget_label[20].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[20].place(anchor="nw", x=310, y=190)
widget[15] = tk.Scale(frame_oscillator)
current_value[15] = tk.IntVar()
widget[15].configure(
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
widget[15].place(anchor="nw", x=430, y=20)
widget[15].bind("<ButtonRelease>", update_value)
widget[15].bind("<B1-Motion>", update_value)
widget_label[15] = tk.Label(frame_oscillator)
widget_label[15].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[15].place(anchor="nw", x=450, y=60)
widget[107] = tk.Scale(frame_oscillator)
current_value[107] = tk.IntVar()
widget[107].configure(
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
widget[107].place(anchor="nw", x=430, y=150)
widget[107].bind("<ButtonRelease>", update_value)
widget[107].bind("<B1-Motion>", update_value)
widget_label[107] = tk.Label(frame_oscillator)
widget_label[107].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[107].place(anchor="nw", x=450, y=190)
widget[102] = tk.Scale(frame_oscillator)
current_value[102] = tk.IntVar()
widget[102].configure(
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
widget[102].place(anchor="nw", x=570, y=20)
widget[102].bind("<ButtonRelease>", update_value)
widget[102].bind("<B1-Motion>", update_value)
widget_label[102] = tk.Label(frame_oscillator)
widget_label[102].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[102].place(anchor="nw", x=590, y=60)
widget[23] = tk.Scale(frame_oscillator)
current_value[23] = tk.IntVar()
widget[23].configure(
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
widget[23].place(anchor="nw", x=570, y=150)
widget[23].bind("<ButtonRelease>", update_value)
widget[23].bind("<B1-Motion>", update_value)
widget_label[23] = tk.Label(frame_oscillator)
widget_label[23].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[23].place(anchor="nw", x=590, y=190)
widget[78] = tk.Scale(frame_oscillator)
current_value[78] = tk.IntVar()
widget[78].configure(
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
widget[78].place(anchor="nw", x=710, y=150)
widget[78].bind("<ButtonRelease>", update_value)
widget[78].bind("<B1-Motion>", update_value)
widget_label[78] = tk.Label(frame_oscillator)
widget_label[78].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[78].place(anchor="nw", x=730, y=190)
widget[21] = tk.Scale(frame_oscillator)
current_value[21] = tk.IntVar()
widget[21].configure(
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
widget[21].place(anchor="nw", x=710, y=20)
widget[21].bind("<ButtonRelease>", update_value)
widget[21].bind("<B1-Motion>", update_value)
widget_label[21] = tk.Label(frame_oscillator)
widget_label[21].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[21].place(anchor="nw", x=730, y=60)
widget[104] = tk.Scale(frame_oscillator)
current_value[104] = tk.IntVar()
widget[104].configure(
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
widget[104].place(anchor="nw", x=850, y=20)
widget[104].bind("<ButtonRelease>", update_value)
widget[104].bind("<B1-Motion>", update_value)
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
widget[73] = tk.Scale(frame_envelope)
current_value[73] = tk.IntVar()
widget[73].configure(
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
widget[73].place(anchor="nw", x=10, y=20)
widget[73].bind("<ButtonRelease>", update_value)
widget[73].bind("<B1-Motion>", update_value)
widget_label[73] = tk.Label(frame_envelope)
widget_label[73].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[73].place(anchor="nw", x=30, y=60)
widget[75] = tk.Scale(frame_envelope)
current_value[75] = tk.IntVar()
widget[75].configure(
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
widget[75].place(anchor="nw", x=150, y=20)
widget[75].bind("<ButtonRelease>", update_value)
widget[75].bind("<B1-Motion>", update_value)
widget_label[75] = tk.Label(frame_envelope)
widget_label[75].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[75].place(anchor="nw", x=170, y=60)
widget[30] = tk.Scale(frame_envelope)
current_value[30] = tk.IntVar()
widget[30].configure(
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
widget[30].place(anchor="nw", x=290, y=20)
widget[30].bind("<ButtonRelease>", update_value)
widget[30].bind("<B1-Motion>", update_value)
widget_label[30] = tk.Label(frame_envelope)
widget_label[30].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[30].place(anchor="nw", x=310, y=60)
widget[72] = tk.Scale(frame_envelope)
current_value[72] = tk.IntVar()
widget[72].configure(
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
widget[72].place(anchor="nw", x=430, y=20)
widget[72].bind("<ButtonRelease>", update_value)
widget[72].bind("<B1-Motion>", update_value)
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
widget[16] = tk.Scale(frame_extra1)
current_value[16] = tk.IntVar()
widget[16].configure(
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
widget[16].place(anchor="nw", x=10, y=20)
widget[16].bind("<ButtonRelease>", update_value)
widget[16].bind("<B1-Motion>", update_value)
widget_label[16] = tk.Label(frame_extra1)
widget_label[16].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[16].place(anchor="nw", x=30, y=60)
widget[17] = tk.Scale(frame_extra1)
current_value[17] = tk.IntVar()
widget[17].configure(
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
widget[17].place(anchor="nw", x=150, y=20)
widget[17].bind("<ButtonRelease>", update_value)
widget[17].bind("<B1-Motion>", update_value)
widget_label[17] = tk.Label(frame_extra1)
widget_label[17].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[17].place(anchor="nw", x=170, y=60)
widget[18] = tk.Scale(frame_extra1)
current_value[18] = tk.IntVar()
widget[18].configure(
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
widget[18].place(anchor="nw", x=290, y=20)
widget[18].bind("<ButtonRelease>", update_value)
widget[18].bind("<B1-Motion>", update_value)
widget_label[18] = tk.Label(frame_extra1)
widget_label[18].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[18].place(anchor="nw", x=310, y=60)
widget[22] = tk.Scale(frame_extra1)
current_value[22] = tk.IntVar()
widget[22].configure(
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
widget[22].place(anchor="nw", x=430, y=20)
widget[22].bind("<ButtonRelease>", update_value)
widget[22].bind("<B1-Motion>", update_value)
widget_label[22] = tk.Label(frame_extra1)
widget_label[22].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[22].place(anchor="nw", x=450, y=60)
widget[80] = tk.Scale(frame_extra1)
current_value[80] = tk.IntVar()
widget[80].configure(
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
widget[80].place(anchor="nw", x=570, y=20)
widget[80].bind("<ButtonRelease>", update_value)
widget[80].bind("<B1-Motion>", update_value)
widget_label[80] = tk.Label(frame_extra1)
widget_label[80].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[80].place(anchor="nw", x=590, y=60)
widget[31] = tk.Scale(frame_extra1)
current_value[31] = tk.IntVar()
widget[31].configure(
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
widget[31].place(anchor="nw", x=710, y=20)
widget[31].bind("<ButtonRelease>", update_value)
widget[31].bind("<B1-Motion>", update_value)
widget_label[31] = tk.Label(frame_extra1)
widget_label[31].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[31].place(anchor="nw", x=730, y=60)
widget[5] = tk.Scale(frame_extra1)
current_value[5] = tk.IntVar()
widget[5].configure(
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
widget[5].place(anchor="nw", x=850, y=20)
widget[5].bind("<ButtonRelease>", update_value)
widget[5].bind("<B1-Motion>", update_value)
widget_label[5] = tk.Label(frame_extra1)
widget_label[5].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[5].place(anchor="nw", x=880, y=60)
widget[105] = tk.Scale(frame_extra1)
current_value[105] = tk.IntVar()
widget[105].configure(
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
widget[105].place(anchor="nw", x=990, y=20)
widget[105].bind("<ButtonRelease>", update_value)
widget[105].bind("<B1-Motion>", update_value)
widget_label[105] = tk.Label(frame_extra1)
widget_label[105].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[105].place(anchor="nw", x=1010, y=60)
widget[77] = tk.Scale(frame_extra1)
current_value[77] = tk.IntVar()
widget[77].configure(
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
widget[77].place(anchor="nw", x=1130, y=20)
widget[77].bind("<ButtonRelease>", update_value)
widget[77].bind("<B1-Motion>", update_value)
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
    width=840)
label8 = tk.Label(frame_extra3)
label8.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='EXTRA3')
label8.place(anchor="nw", height=15)
######
widget[81] = tk.Scale(frame_extra3)
current_value[81] = tk.IntVar()
widget[81].configure(
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
widget[81].place(anchor="nw", x=10, y=20)
widget[81].bind("<ButtonRelease>", update_value)
widget[81].bind("<B1-Motion>", update_value)
widget_label[81] = tk.Label(frame_extra3)
widget_label[81].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[81].place(anchor="nw", x=30, y=60)
widget[82] = tk.Scale(frame_extra3)
current_value[82] = tk.IntVar()
widget[82].configure(
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
widget[82].place(anchor="nw", x=150, y=20)
widget[82].bind("<ButtonRelease>", update_value)
widget[82].bind("<B1-Motion>", update_value)
widget_label[82] = tk.Label(frame_extra3)
widget_label[82].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[82].place(anchor="nw", x=180, y=60)
widget[83] = tk.Scale(frame_extra3)
current_value[83] = tk.IntVar()
widget[83].configure(
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
widget[83].place(anchor="nw", x=290, y=20)
widget[83].bind("<ButtonRelease>", update_value)
widget[83].bind("<B1-Motion>", update_value)
widget_label[83] = tk.Label(frame_extra3)
widget_label[83].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[83].place(anchor="nw", x=310, y=60)
widget[85] = tk.Scale(frame_extra3)
current_value[85] = tk.IntVar()
widget[85].configure(
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
widget[85].place(anchor="nw", x=430, y=20)
widget[85].bind("<ButtonRelease>", update_value)
widget[85].bind("<B1-Motion>", update_value)
widget_label[85] = tk.Label(frame_extra3)
widget_label[85].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[85].place(anchor="nw", x=450, y=60)
widget[86] = tk.Scale(frame_extra3)
current_value[86] = tk.IntVar()
widget[86].configure(
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
widget[86].place(anchor="nw", x=570, y=20)
widget[86].bind("<ButtonRelease>", update_value)
widget[86].bind("<B1-Motion>", update_value)
widget_label[86] = tk.Label(frame_extra3)
widget_label[86].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[86].place(anchor="nw", x=590, y=60)
widget[87] = tk.Scale(frame_extra3)
current_value[87] = tk.IntVar()
widget[87].configure(
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
widget[87].place(anchor="nw", x=710, y=20)
widget[87].bind("<ButtonRelease>", update_value)
widget[87].bind("<B1-Motion>", update_value)
widget_label[87] = tk.Label(frame_extra3)
widget_label[87].configure(
    background=w_l_bg,
    foreground=w_l_fg,
    borderwidth=0,
    text='')
widget_label[87].place(anchor="nw", x=730, y=60)
frame_extra3.place(anchor="nw", bordermode="outside", x=140, y=690)
frame_extra3.grid_propagate(0)
######
frame_midi = tk.Frame(frame1)
frame_midi.configure(
    height=130,
    background=bg_color,
    highlightbackground=hbc_color,
    highlightthickness=1,
    width=580)
label8 = tk.Label(frame_midi)
label8.configure(
    foreground=fg_label_color,
    background=bg_label_color,
    relief="flat",
    state="normal",
    text='MIDI')
label8.place(anchor="nw", height=15)
######
program_change_ch_label = tk.Label(frame_midi)
program_change_ch_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label,
                                  font=font_label, text='Prog. C. CH:')
program_change_ch_label.place(anchor="nw", width=140, height=25, x=5, y=18)
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
    frame_midi, program_change_ch, *values, command=select_program_change_ch)
option_program_change_ch.place(anchor="nw", width=50, height=25, x=140, y=18)

midi_ch_label = tk.Label(frame_midi)
midi_ch_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label, font=font_label,
                        text='MIDI CH:')
midi_ch_label.place(anchor="nw", width=140, height=25, x=230, y=18)
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
    frame_midi, midi_ch, *values, command=select_midi_ch)
option_midi_ch.place(anchor="nw", width=50, height=25, x=365, y=18)


midi_in_d_label = tk.Label(frame_midi)
midi_in_d_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label,
                                  font=font_label, text='MIDI IN DEV:')
midi_in_d_label.place(anchor="nw", width=140, height=25, x=5, y=45)
midi_in_d = tk.StringVar(value=available_in_ports[int(midi_in_port)])
values = available_in_ports

option_midi_in_d = tk.OptionMenu(
    frame_midi, midi_in_d, *values, command=select_midi_in_d)
option_midi_in_d.place(anchor="nw", width=275, height=25, x=140, y=45)

midi_out_d_label = tk.Label(frame_midi)
midi_out_d_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label,
                                  font=font_label, text='MIDI OUT DEV:')
midi_out_d_label.place(anchor="nw", width=140, height=25, x=5, y=72)
midi_out_d = tk.StringVar(value=available_out_ports[int(midi_out_port)])
values = available_out_ports

option_midi_out_d = tk.OptionMenu(
    frame_midi, midi_out_d, *values, command=select_midi_out_d)
option_midi_out_d.place(anchor="nw", width=275, height=25, x=140, y=72)

midi_k_d_label = tk.Label(frame_midi)
midi_k_d_label.configure(anchor="w", justify="left", background=bg_info_label, foreground=fg_info_label,
                                  font=font_label, text='MIDI KEYB.:')
midi_k_d_label.place(anchor="nw", width=140, height=25, x=5, y=99)
midi_k_d = tk.StringVar(value=available_k_ports[int(midi_k_port)])
values = available_k_ports
option_midi_k_d = tk.OptionMenu(
    frame_midi, midi_k_d, *values, command=select_midi_k_d)
option_midi_k_d.place(anchor="nw", width=275, height=25, x=140, y=99)





frame_midi.place(anchor="nw", bordermode="outside", x=980, y=690)
frame_midi.grid_propagate(0)




frame1.pack(side="top")







load_default()
select_pattern(None)

root.mainloop()
