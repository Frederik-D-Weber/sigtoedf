import sys
import struct
import codecs
from itertools import repeat
import os
import numpy
from datetime import time, date, datetime, timedelta
from os.path import splitext
from math import floor
import pandas as pd
from collections import namedtuple
from datetime import datetime
import pyedflib
import math

from datetime import date
from datetime import datetime

class Event:
    ET_SAVESKIPEVENT = 1
    ET_SYSTEMEVENT = 2
    ET_USEREVENT = 3
    ET_DIGINPEVENT = 4
    ET_RECORDEREVENT = 5
    ET_RESPIRATIONEVENTS = 6
    ET_SATURATIONEVENTS = 7
    ET_ECGEVENTS = 8
    ET_EMGEVENTS = 9
    ET_EEG_DELTAEVENTS = 10
    ET_EEG_SPINDLEEVENTS = 11
    ET_EEG_ALPHAEVENTS = 12
    ET_EOGEVENTS = 13
    ET_EEG_THETAEVENTS = 14
    ET_EEG_BETAEVENTS = 15
    ET_AROUSALEVENTS = 16
    ET_SOUNDEVENTS = 17
    ET_BODYPOSITIONEVENTS = 18
    ET_CPAPEVENTS = 19

    ET_DICT = {ET_SAVESKIPEVENT: "ET_SAVESKIPEVENT",
               ET_SYSTEMEVENT: "ET_SYSTEMEVENT",
               ET_USEREVENT: "ET_USEREVENT",
               ET_DIGINPEVENT: "ET_DIGINPEVENT",
               ET_RECORDEREVENT: "ET_RECORDEREVENT",
               ET_RESPIRATIONEVENTS: "ET_RESPIRATIONEVENTS",
               ET_SATURATIONEVENTS: "ET_SATURATIONEVENTS",
               ET_ECGEVENTS: "ET_ECGEVENTS",
               ET_EMGEVENTS: "ET_EMGEVENTS",
               ET_EEG_DELTAEVENTS: "ET_EEG_DELTAEVENTS",
               ET_EEG_SPINDLEEVENTS: "ET_EEG_SPINDLEEVENTS",
               ET_EEG_ALPHAEVENTS: "ET_EEG_ALPHAEVENTS",
               ET_EOGEVENTS: "ET_EOGEVENTS",
               ET_EEG_THETAEVENTS: "ET_EEG_THETAEVENTS",
               ET_EEG_BETAEVENTS: "ET_EEG_BETAEVENTS",
               ET_AROUSALEVENTS: "ET_AROUSALEVENTS",
               ET_SOUNDEVENTS: "ET_SOUNDEVENTS",
               ET_BODYPOSITIONEVENTS: "ET_BODYPOSITIONEVENTS",
               ET_CPAPEVENTS: "ET_CPAPEVENTS"}

    ST_ANALYSIS = 'A'
    ST_MONTAGECHANGE = 'M'
    ST_DIG_LOW_FILTER_INC = 'L'
    ST_DIG_LOW_FILTER_DEF = 'M'
    ST_DIG_LOW_FILTER_DEC = 'l'
    ST_DIG_HIGH_FILTER_INC = 'H'
    ST_DIG_HIGH_FILTER_DEF = 'I'
    ST_DIG_HIGH_FILTER_DEC = 'h'
    ST_SENSITIVITY_INC = 'S'
    ST_SENSITIVITY_DEF = 'T'
    ST_SENSITIVITY_DEC = 's'
    ST_LOW_FILTER_INC = 'L'
    ST_LOW_FILTER_DEF = 'M'
    ST_LOW_FILTER_DEC = 'l'
    ST_HIGH_FILTER_INC = 'H'
    ST_HIGH_FILTER_DEF = 'I'
    ST_HIGH_FILTER_DEC = 'h'
    ST_VIDEO_ON = 'V'
    ST_VIDEO_OFF = 'v'
    ST_VIDEO_ON_WHILE_MEASURING = 'Z'
    ST_VIDEO_OFF_WHILE_MEASURING = 'z'
    ST_STIMULUS_ON = 'X'
    ST_STIMULUS_OFF = 'x'
    ST_NONCLASSIFIEDAPNEA = 'A'
    ST_CENTRALAPNEA = 'C'
    ST_OBSTRUCTIVEAPNEA = 'O'
    ST_MIXEDAPNEA = 'M'
    ST_NONCLASSIFIEDHYPOPNEA = 'H'
    ST_CENTRALHYPOPNEA = 'D'
    ST_OBSTRUCTIVEHYPOPNEA = 'Q'
    ST_MIXEDHYPOPNEA = 'W'
    ST_NEUTRAL = 'N'
    ST_PARADOXYCALAPNEA = 'P'
    ST_PARADOXYCALHYPOPNEA = 'S'
    ST_PERIODICALBREATHING = 'R'
    ST_INVALIDFORRESPIRATIONS1 = 'I'
    ST_INVALIDFORRESPIRATIONS2 = 'J'
    ST_DIPSATURATION = 'D'
    ST_HYPOXYCALSATURATION = 'H'
    ST_INVALIDFORSATURATIONS1 = 'I'
    ST_INVALIDFORSATURATIONS2 = 'J'
    ST_TACHY = 'T'
    ST_BRADY = 'B'
    ST_INVALIDFORECGS1 = 'I'
    ST_INVALIDFORECGS2 = 'J'
    ST_MOVEMENT = 'M'
    ST_LEFTLEGMOVEMENT = 'L'
    ST_RIGHTLEGMOVEMENT = 'R'
    ST_INVALIDFOREMGS1 = 'I'
    ST_INVALIDFOREMGS2 = 'J'
    ST_K_COMPLEX = 'K'
    ST_INVALIDFOREEG_DELTAS1 = 'I'
    ST_INVALIDFOREEG_DELTAS2 = 'J'
    ST_SPINDLE = 'S'
    ST_INVALIDFOREEG_SPINDLES1 = 'I'
    ST_INVALIDFOREEG_SPINDLES2 = 'J'
    ST_ALPHA = 'A'
    ST_INVALIDFOREEG_ALPHAS1 = 'I'
    ST_INVALIDFOREEG_ALPHAS2 = 'J'
    ST_REM = 'R'
    ST_SEM = 'S'
    ST_BLINK = 'B'
    ST_INVALIDFOREOGREMS1 = 'I'
    ST_INVALIDFOREOGREMS2 = 'J'
    ST_INVALIDFOREOGSEMS1 = 'M'
    ST_INVALIDFOREOGSEMS2 = 'N'
    ST_THETA = 'T'
    ST_INVALIDFOREEG_THETAS1 = 'I'
    ST_INVALIDFOREEG_THETAS2 = 'J'
    ST_BETA = 'B'
    ST_INVALIDFOREEG_BETAS1 = 'I'
    ST_INVALIDFOREEG_BETAS2 = 'J'
    ST_AROUSAL = 'A'
    ST_INVALIDFORAROUSALS1 = 'I'
    ST_INVALIDFORAROUSALS2 = 'J'
    ST_SNORING = 'S'
    ST_PERIODICAL_SNORING = 'P'
    ST_INVALIDFORSOUNDS1 = 'I'
    ST_INVALIDFORSOUNDS2 = 'J'
    ST_LEFTSIDE = 'L'
    ST_RIGHTSIDE = 'R'
    ST_BACK = 'A'
    ST_BELLY = 'B'
    ST_STANDINGUP = 'U'
    ST_HEADDOWN = 'D'
    ST_INVALIDFORBODYPOSITIONS1 = 'I'
    ST_INVALIDFORBODYPOSITIONS2 = 'J'
    ST_CPAP = 'C'
    ST_INVALIDFORCPAPS1 = 'I'
    ST_INVALIDFORCPAPS2 = 'J'

    ST_DICT = {(ET_SYSTEMEVENT, ST_ANALYSIS): "ST_ANALYSIS",
               (ET_SYSTEMEVENT, ST_MONTAGECHANGE): "ST_MONTAGECHANGE",
               (ET_SYSTEMEVENT, ST_DIG_LOW_FILTER_INC): "ST_DIG_LOW_FILTER_INC",
               (ET_SYSTEMEVENT, ST_DIG_LOW_FILTER_DEF): "ST_DIG_LOW_FILTER_DEF",
               (ET_SYSTEMEVENT, ST_DIG_LOW_FILTER_DEC): "ST_DIG_LOW_FILTER_DEC",
               (ET_SYSTEMEVENT, ST_DIG_HIGH_FILTER_INC): "ST_DIG_HIGH_FILTER_INC",
               (ET_SYSTEMEVENT, ST_DIG_HIGH_FILTER_DEF): "ST_DIG_HIGH_FILTER_DEF",
               (ET_SYSTEMEVENT, ST_DIG_HIGH_FILTER_DEC): "ST_DIG_HIGH_FILTER_DEC",
               (ET_RECORDEREVENT, ST_SENSITIVITY_INC): "ST_SENSITIVITY_INC",
               (ET_RECORDEREVENT, ST_SENSITIVITY_DEF): "ST_SENSITIVITY_DEF",
               (ET_RECORDEREVENT, ST_SENSITIVITY_DEC): "ST_SENSITIVITY_DEC",
               (ET_RECORDEREVENT, ST_LOW_FILTER_INC): "ST_LOW_FILTER_INC",
               (ET_RECORDEREVENT, ST_LOW_FILTER_DEF): "ST_LOW_FILTER_DEF",
               (ET_RECORDEREVENT, ST_LOW_FILTER_DEC): "ST_LOW_FILTER_DEC",
               (ET_RECORDEREVENT, ST_HIGH_FILTER_INC): "ST_HIGH_FILTER_INC",
               (ET_RECORDEREVENT, ST_HIGH_FILTER_DEF): "ST_HIGH_FILTER_DEF",
               (ET_RECORDEREVENT, ST_HIGH_FILTER_DEC): "ST_HIGH_FILTER_DEC",
               (ET_RECORDEREVENT, ST_VIDEO_ON): "ST_VIDEO_ON",
               (ET_RECORDEREVENT, ST_VIDEO_OFF): "ST_VIDEO_OFF",
               (ET_RECORDEREVENT, ST_VIDEO_ON_WHILE_MEASURING): "ST_VIDEO_ON_WHILE_MEASURING",
               (ET_RECORDEREVENT, ST_VIDEO_OFF_WHILE_MEASURING): "ST_VIDEO_OFF_WHILE_MEASURING",
               (ET_RECORDEREVENT, ST_STIMULUS_ON): "ST_STIMULUS_ON",
               (ET_RECORDEREVENT, ST_STIMULUS_OFF): "ST_STIMULUS_OFF",
               (ET_RESPIRATIONEVENTS, ST_NONCLASSIFIEDAPNEA): "ST_NONCLASSIFIEDAPNEA",
               (ET_RESPIRATIONEVENTS, ST_CENTRALAPNEA): "ST_CENTRALAPNEA",
               (ET_RESPIRATIONEVENTS, ST_OBSTRUCTIVEAPNEA): "ST_OBSTRUCTIVEAPNEA",
               (ET_RESPIRATIONEVENTS, ST_MIXEDAPNEA): "ST_MIXEDAPNEA",
               (ET_RESPIRATIONEVENTS, ST_NONCLASSIFIEDHYPOPNEA): "ST_NONCLASSIFIEDHYPOPNEA",
               (ET_RESPIRATIONEVENTS, ST_CENTRALHYPOPNEA): "ST_CENTRALHYPOPNEA",
               (ET_RESPIRATIONEVENTS, ST_OBSTRUCTIVEHYPOPNEA): "ST_OBSTRUCTIVEHYPOPNEA",
               (ET_RESPIRATIONEVENTS, ST_MIXEDHYPOPNEA): "ST_MIXEDHYPOPNEA",
               (ET_RESPIRATIONEVENTS, ST_NEUTRAL): "ST_NEUTRAL",
               (ET_RESPIRATIONEVENTS, ST_PARADOXYCALAPNEA): "ST_PARADOXYCALAPNEA",
               (ET_RESPIRATIONEVENTS, ST_PARADOXYCALHYPOPNEA): "ST_PARADOXYCALHYPOPNEA",
               (ET_RESPIRATIONEVENTS, ST_PERIODICALBREATHING): "ST_PERIODICALBREATHING",
               (ET_RESPIRATIONEVENTS, ST_INVALIDFORRESPIRATIONS1): "ST_INVALIDFORRESPIRATIONS1",
               (ET_RESPIRATIONEVENTS, ST_INVALIDFORRESPIRATIONS2): "ST_INVALIDFORRESPIRATIONS2",
               (ET_SATURATIONEVENTS, ST_DIPSATURATION): "ST_DIPSATURATION",
               (ET_SATURATIONEVENTS, ST_HYPOXYCALSATURATION): "ST_HYPOXYCALSATURATION",
               (ET_SATURATIONEVENTS, ST_INVALIDFORSATURATIONS1): "ST_INVALIDFORSATURATIONS1",
               (ET_SATURATIONEVENTS, ST_INVALIDFORSATURATIONS2): "ST_INVALIDFORSATURATIONS2",
               (ET_ECGEVENTS, ST_TACHY): "ST_TACHY",
               (ET_ECGEVENTS, ST_BRADY): "ST_BRADY",
               (ET_ECGEVENTS, ST_INVALIDFORECGS1): "ST_INVALIDFORECGS1",
               (ET_ECGEVENTS, ST_INVALIDFORECGS2): "ST_INVALIDFORECGS2",
               (ET_EMGEVENTS, ST_MOVEMENT): "ST_MOVEMENT",
               (ET_EMGEVENTS, ST_LEFTLEGMOVEMENT): "ST_LEFTLEGMOVEMENT",
               (ET_EMGEVENTS, ST_RIGHTLEGMOVEMENT): "ST_RIGHTLEGMOVEMENT",
               (ET_EMGEVENTS, ST_INVALIDFOREMGS1): "ST_INVALIDFOREMGS1",
               (ET_EMGEVENTS, ST_INVALIDFOREMGS2): "ST_INVALIDFOREMGS2",
               (ET_EEG_DELTAEVENTS, ST_K_COMPLEX): "ST_K_COMPLEX",
               (ET_EEG_DELTAEVENTS, ST_INVALIDFOREEG_DELTAS1): "ST_INVALIDFOREEG_DELTAS1",
               (ET_EEG_DELTAEVENTS, ST_INVALIDFOREEG_DELTAS2): "ST_INVALIDFOREEG_DELTAS2",
               (ET_EEG_SPINDLEEVENTS, ST_SPINDLE): "ST_SPINDLE",
               (ET_EEG_SPINDLEEVENTS, ST_INVALIDFOREEG_SPINDLES1): "ST_INVALIDFOREEG_SPINDLES1",
               (ET_EEG_SPINDLEEVENTS, ST_INVALIDFOREEG_SPINDLES2): "ST_INVALIDFOREEG_SPINDLES2",
               (ET_EEG_ALPHAEVENTS, ST_ALPHA): "ST_ALPHA",
               (ET_EEG_ALPHAEVENTS, ST_INVALIDFOREEG_ALPHAS1): "ST_INVALIDFOREEG_ALPHAS1",
               (ET_EEG_ALPHAEVENTS, ST_INVALIDFOREEG_ALPHAS2): "ST_INVALIDFOREEG_ALPHAS2",
               (ET_EOGEVENTS, ST_REM): "ST_REM",
               (ET_EOGEVENTS, ST_SEM): "ST_SEM",
               (ET_EOGEVENTS, ST_BLINK): "ST_BLINK",
               (ET_EOGEVENTS, ST_INVALIDFOREOGREMS1): "ST_INVALIDFOREOGREMS1",
               (ET_EOGEVENTS, ST_INVALIDFOREOGREMS2): "ST_INVALIDFOREOGREMS2",
               (ET_EOGEVENTS, ST_INVALIDFOREOGSEMS1): "ST_INVALIDFOREOGSEMS1",
               (ET_EOGEVENTS, ST_INVALIDFOREOGSEMS2): "ST_INVALIDFOREOGSEMS2",
               (ET_EEG_THETAEVENTS, ST_THETA): "ST_THETA",
               (ET_EEG_THETAEVENTS, ST_INVALIDFOREEG_THETAS1): "ST_INVALIDFOREEG_THETAS1",
               (ET_EEG_THETAEVENTS, ST_INVALIDFOREEG_THETAS2): "ST_INVALIDFOREEG_THETAS2",
               (ET_EEG_BETAEVENTS, ST_BETA): "ST_BETA",
               (ET_EEG_BETAEVENTS, ST_INVALIDFOREEG_BETAS1): "ST_INVALIDFOREEG_BETAS1",
               (ET_EEG_BETAEVENTS, ST_INVALIDFOREEG_BETAS2): "ST_INVALIDFOREEG_BETAS2",
               (ET_AROUSALEVENTS, ST_AROUSAL): "ST_AROUSAL",
               (ET_AROUSALEVENTS, ST_INVALIDFORAROUSALS1): "ST_INVALIDFORAROUSALS1",
               (ET_AROUSALEVENTS, ST_INVALIDFORAROUSALS2): "ST_INVALIDFORAROUSALS2",
               (ET_SOUNDEVENTS, ST_SNORING): "ST_SNORING",
               (ET_SOUNDEVENTS, ST_PERIODICAL_SNORING): "ST_PERIODICAL_SNORING",
               (ET_SOUNDEVENTS, ST_INVALIDFORSOUNDS1): "ST_INVALIDFORSOUNDS1",
               (ET_SOUNDEVENTS, ST_INVALIDFORSOUNDS2): "ST_INVALIDFORSOUNDS2",
               (ET_BODYPOSITIONEVENTS, ST_LEFTSIDE): "ST_LEFTSIDE",
               (ET_BODYPOSITIONEVENTS, ST_RIGHTSIDE): "ST_RIGHTSIDE",
               (ET_BODYPOSITIONEVENTS, ST_BACK): "ST_BACK",
               (ET_BODYPOSITIONEVENTS, ST_BELLY): "ST_BELLY",
               (ET_BODYPOSITIONEVENTS, ST_STANDINGUP): "ST_STANDINGUP",
               (ET_BODYPOSITIONEVENTS, ST_HEADDOWN): "ST_HEADDOWN",
               (ET_BODYPOSITIONEVENTS, ST_INVALIDFORBODYPOSITIONS1): "ST_INVALIDFORBODYPOSITIONS1",
               (ET_BODYPOSITIONEVENTS, ST_INVALIDFORBODYPOSITIONS2): "ST_INVALIDFORBODYPOSITIONS2",
               (ET_CPAPEVENTS, ST_CPAP): "ST_CPAP",
               (ET_CPAPEVENTS, ST_INVALIDFORCPAPS1): "ST_INVALIDFORCPAPS1",
               (ET_CPAPEVENTS, ST_INVALIDFORCPAPS2): "ST_INVALIDFORCPAPS2"}

    def __init__(self, ev_type=0, sub_type=' ', page=0, page_time=0.0, time=0, duration=0, duration_in_ms=0, channels=0,
                 info=0):
        self.ev_type = ev_type
        self.sub_type = sub_type
        self.page = page
        self.page_time = page_time
        self.time = time
        self.duration = duration
        self.duration_in_ms = duration_in_ms
        self.end_time = time + duration_in_ms
        self.channels = channels
        self.info = info


def read_events(sf, offset, size, nevents=10240):
    sf.seek(offset)
    int16 = struct.Struct("<h")
    tcount = int16.unpack(sf.read(int16.size))[0]
    events = []
    evstruct = struct.Struct("<hB6I")
    currsize = int16.size + tcount*evstruct.size
    if currsize > size:
        pass
    for i in range(nevents):
        bts = sf.read(evstruct.size)
        if i < tcount:
            evd = evstruct.unpack(bts)
            events.append(
                Event(evd[0], chr(evd[1]), evd[2] >> 16, (evd[2] & 0x0000ffff) / 1000.0, evd[3], evd[4], evd[5],
                      evd[6], evd[7]))
    return events


class EventDesc:
    DT_MEASURE = 0
    DT_EXTERNAL = 1
    DT_SCAN = 2

    DT_DICT = {DT_MEASURE: "DT_MEASURE", DT_EXTERNAL: "DT_EXTERNAL", DT_SCAN: "DT_SCAN"}

    def __init__(self, desc="", label="", d_type=0, value=0):
        self.desc = desc
        self.label = label
        self.d_type = d_type
        self.value = value


def read_event_descs(sf):
    types = []
    ssize = 32
    int16 = struct.Struct("<h")
    tcount = int16.unpack(sf.read(int16.size))[0]
    ds = "".join(repeat("20s", ssize))
    ls = "".join(repeat("6s", ssize))
    ts = "<%dh" % ssize
    vs = "<%dh" % ssize
    dstruct = struct.Struct(ds)
    descs = dstruct.unpack(sf.read(dstruct.size))
    lstruct = struct.Struct(ls)
    labels = lstruct.unpack(sf.read(lstruct.size))
    tstruct = struct.Struct(ts)
    dtypes = tstruct.unpack(sf.read(tstruct.size))
    vstruct = struct.Struct(vs)
    values = vstruct.unpack(sf.read(vstruct.size))
    for i in range(tcount):
        types.append(EventDesc(string_trim_to_0(descs[i]), string_trim_to_0(labels[i]), dtypes[i], values[i]))
    return types


def get_codes_4_label(evds, label):
    return set(((chr(x.value)) for x in evds if x.label == label))


def get_selected_events(evlist, evtypes, evcode):
    return [x for x in evlist if (x.ev_type in evtypes) and (x.sub_type in evcode)]


def get_selected_events_4_types(evlist, evtypes):
    return [x for x in evlist if x.ev_type in evtypes]


class RecordingEvent:
    def __init__(self, start_page, end_page, start_time, end_time):
        self.start_page = start_page
        self.end_page = end_page
        self.start_time = start_time
        self.end_time = end_time


def find_recording_event(page, events):
    return next((x for x in events if (page >= x.start_page) and (page <= x.end_page)), None)



class SignalFile:
    def __init__(self):
        self.header = SignalHeader()
        self.data_table = DataTable()
        self.measurement = Measurement()
        self.recorder_info = RecorderMontageInfo()
        self.events = []
        self.events_desc = []
        self.store_events = 0
        self.signal_pages = []
        self.signal_data = []


def read_signal_file(file_name, read_signal_data):
    file_size = os.path.getsize(file_name)
    sf = open(file_name, 'rb')
    #sf = codecs.open(file_name, 'rb', encoding='utf-8')
    signal = SignalFile()
    try:
        signal.header = read_signal_header(sf)
        signal.data_table = read_data_table(sf)
        signal.measurement = read_measurement(sf, signal.data_table.measurement_info.offset, signal.data_table.measurement_info.size)
        signal.recorder_info = read_recorder_info(sf, signal.data_table.recorder_montage_info.offset,
                                                  signal.data_table.recorder_montage_info.size)
        signal.events = read_events(sf, signal.data_table.events_info.offset, signal.data_table.events_info.size, 2048)

        signal.events_desc = read_event_descs(sf)
        store_events_list = get_selected_events_4_types(signal.events, [Event.ET_SAVESKIPEVENT])
        signal.store_events = len(store_events_list)
        spages = read_signal_pages(sf, read_signal_data, file_size, signal.data_table.signal_info.offset, signal.data_table.signal_info.size, 30,
                                   signal.recorder_info.numberOfChannelsUsed, signal.recorder_info.channels)
        signal.signal_pages = spages[0]
        signal.signal_data = spages[1]
    finally:
        sf.close()
    return signal


class Block:
    def __init__(self, offset=0, size=0, header_size=0):
        self.offset = offset
        self.size = size
        self.header_size = header_size


class DataTable:
    def __init__(self):
        self.measurement_info = Block()
        self.recorder_montage_info = Block()
        self.events_info = Block()
        self.notes_info = Block()
        self.impedance_info = Block()
        self.display_montages_info = Block()
        self.stimulator_info = Block()
        self.signal_info = Block()


def read_data_table(sf):
    sf.seek((struct.Struct("<2l2h")).size)
    data_table = DataTable()
    dt_struct = struct.Struct("<17l")
    dt = dt_struct.unpack(sf.read(dt_struct.size))
    data_table.measurement_info = Block(dt[0], dt[1])
    data_table.recorder_montage_info = Block(dt[2], dt[3])
    data_table.events_info = Block(dt[4], dt[5])
    data_table.notes_info = Block(dt[6], dt[7])
    data_table.impedance_info = Block(dt[8], dt[9])
    data_table.display_montages_info = Block(dt[10], dt[11])
    data_table.stimulator_info = Block(dt[12], dt[13])
    data_table.signal_info = Block(dt[14], dt[15], dt[16])
    return data_table


class SignalHeader:
    PROGRAM_ID = 0x41545353
    SIGNAL_ID = 0x47495352
    SIGNAL_DUMMY_ID = 0x53464445

    def __init__(self, program_id=0, signal_id=0, version_id=0, read_only=0):
        self.program_id = program_id
        self.signal_id = signal_id
        self.version_id = version_id
        self.read_only = read_only

    def check_program_id(self):
        return self.program_id == SignalHeader.PROGRAM_ID

    def check_signal_id(self):
        return self.signal_id in (SignalHeader.SIGNAL_ID, SignalHeader.SIGNAL_DUMMY_ID)

    def check_header(self):
        return self.check_program_id() and self.check_signal_id()


def read_signal_header(sf):
    sf.seek(0)
    hs = struct.Struct("<2l2h")
    hb = hs.unpack(sf.read(hs.size))
    return SignalHeader(hb[0], hb[1], hb[2], hb[3])


class Measurement:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.street = ""
        self.zip_code = ""
        self.city = ""
        self.state = ""
        self.country = ""
        self.birthday = date(1900, 1, 1)
        self.sex = ""
        self.start_date = date(1900, 1, 1)
        self.start_hour = time(0, 0, 0)
        self.room = ""
        self.doctor = ""
        self.technician = ""
        self.class_code = ""
        self.clin_info = ""
        self.backup_flag = ""
        self.status_flags = 0
        self.archive_flag = ""
        self.vcr_timing_correction = 0
        self.referring_doctor_name = ""
        self.referring_doctor_code = ""
        self.weight = 0
        self.height = 0
        self.weight_unit = 0
        self.height_unit = 0
        self.protocol = ""
        self.maximum_voltage = 0
        self.maximum_amplitude = 0


def read_measurement(sf, offset, size):
    def sexc(x):
        return {
            1: 'M',
            0: 'F'}.get(x)

    sf.seek(offset)
    meas_struct = struct.Struct("<17s33s33s17s33s33s33slh2l9s33s33s9s1963s1sh1sd33s33s4h33s2h")
    if meas_struct.size > size:
        pass
    ms = meas_struct.unpack(sf.read(meas_struct.size))
    measurement = Measurement()
    measurement.id = string_trim_to_0(ms[0])
    measurement.name = string_trim_to_0(ms[1])
    measurement.street = string_trim_to_0(ms[2])
    measurement.zip_code = string_trim_to_0(ms[3])
    measurement.city = string_trim_to_0(ms[4])
    measurement.state = string_trim_to_0(ms[5])
    measurement.country = string_trim_to_0(ms[6])
    measurement.birthday = decode_date(ms[7])
    measurement.sex = sexc(ms[8])
    measurement.start_date = decode_date(ms[9])
    measurement.start_hour = decode_time(ms[10])
    measurement.room = string_trim_to_0(ms[11])
    measurement.doctor = string_trim_to_0(ms[12])
    measurement.technician = string_trim_to_0(ms[13])
    measurement.class_code = string_trim_to_0(ms[14])
    measurement.clin_info = string_trim_to_0(ms[15])
    measurement.backup_flag = string_trim_to_0(ms[16])
    measurement.status_flags = ms[17]
    measurement.archive_flag = string_trim_to_0(ms[18])
    measurement.vcr_timing_correction = ms[19]
    measurement.referring_doctor_name = string_trim_to_0(ms[20])
    measurement.referring_doctor_code = string_trim_to_0(ms[21])
    measurement.weight = ms[22] / 10
    measurement.height = ms[23] / 100
    measurement.weight_unit = ms[24]
    measurement.height_unit = ms[25]
    measurement.protocol = string_trim_to_0(ms[26])
    measurement.maximum_voltage = ms[27]
    measurement.maximum_amplitude = ms[28]
    td_age = measurement.start_date - measurement.birthday
    measurement.age = td_age.days / 365.25

    return measurement


def create_fmt_strings(cl):
    return ['%'+str(cl.field_size[i])+(('.'+str(cl.field_decimal[i])) if cl.field_decimal[i]>0 else '')+cl.field_type[i] for i in range(len(cl.field_name))]


def create_title_fmts(cl):
    return ['%'+str(cl.field_size[i])+'s' for i in range(len(cl.field_name))]


def create_table_title(cl):
    return ('|'+'|'.join(create_title_fmts(cl))+'|') % tuple(cl.field_name)


def create_row_breaker(cl):
    return ('|'+'|'.join(create_title_fmts(cl))+'|') % tuple(['-'*x for x in cl.field_size])


def create_row(cl, data_tuple):
    return ('|'+'|'.join(create_fmt_strings(cl))+'|') % data_tuple


class RecorderChannel:
    field_name = ['Samp.', 'Type', 'Subtype', 'Desc', 'Sens', 'LF', 'HF', 'Delay', 'Unit', 'ArLv', 'Cal Type', 'Cal Fct.', 'Cal Off.', 'B.Size']
    field_type = ['d', 's', 's', 's', 'f', 'f', 'f', 'd', 's', 'd', 'd', 'f', 'f', 'd']
    field_size = [5, 8, 8, 8, 6, 6, 6, 5, 5, 5, 8, 10, 8, 6]
    field_decimal = [0, 0, 0, 0, 1, 3, 1, 0, 0, 0, 0, 8, 1, 0]

    def __init__(self, sampling_rate, signal_type, signal_sub_type, channel_desc, sensitivity_index, low_filter_index, high_filter_index, delay,
                 unit, artefact_level, cal_type, cal_factor, cal_offset, save_buffer_size):
        self.sampling_rate = sampling_rate
        self.signal_type = signal_type
        self.signal_sub_type = signal_sub_type
        self.channel_desc = channel_desc
        self.sensitivity_index = sensitivity_index
        self.low_filter_index = low_filter_index
        self.high_filter_index = high_filter_index
        self.delay = delay
        self.unit = unit
        self.artefact_level = artefact_level
        self.cal_type = cal_type
        self.cal_factor = cal_factor
        self.cal_offset = cal_offset
        self.save_buffer_size = save_buffer_size

    def create_data_tuple(self,sensitivity=None, low_filter=None, high_filter=None):
        return (self.sampling_rate, self.signal_type, self.signal_sub_type, self.channel_desc,
                sensitivity[self.sensitivity_index] if sensitivity is not None else self.sensitivity_index,
                low_filter[self.low_filter_index] if low_filter is not None else self.low_filter_index,
                high_filter[self.high_filter_index] if high_filter is not None else self.high_filter_index, self.delay,
                self.unit, self.artefact_level, self.cal_type, self.cal_factor, self.cal_offset, self.save_buffer_size)


class RecorderMontageInfo:
    def __init__(self):
        self.name = ""
        self.nRecChannels = 0
        self.invertedACChannels = 0
        self.maximumVoltage = 0
        self.normalVoltage = 0
        self.calibrationSignal = 0
        self.calibrationScale = 0
        self.videoControl = 0
        self.nSensitivities = 0
        self.nLowFilters = 0
        self.nHighFilters = 0
        self.sensitivity = []
        self.lowFilter = []
        self.highFilter = []
        self.montageName = ""
        self.numberOfChannelsUsed = 0
        self.globalSens = 0
        self.epochLengthInSamples = 0
        self.highestRate = 0
        self.channels = []
        self.parameter = 0
        self.displayMontageName = ""
        self.dispCh = []
        self.dispChScale = []
        self.electrode = []
        self.lead = []
        self.gain = []
        self.offset = []
        self.nChannelsOnDisplay = 0
        self.sampleMap = []
        self.dummy = []


def read_recorder_info(sf, offset, size):
    sf.seek(offset)
    recorder_struct = struct.Struct("<33s2b5h3H")
    if recorder_struct.size > size:
        pass
    rs = recorder_struct.unpack(sf.read(recorder_struct.size))

    recorder_info = RecorderMontageInfo()
    recorder_info.name = string_trim_to_0(rs[0])
    recorder_info.nRecChannels = rs[1]
    recorder_info.invertedACChannels = rs[2]
    recorder_info.maximumVoltage = rs[3]
    recorder_info.normalVoltage = rs[4]
    recorder_info.calibrationSignal = rs[5]
    recorder_info.calibrationScale = rs[6]
    recorder_info.videoControl = rs[7]
    recorder_info.nSensitivities = rs[8]
    recorder_info.nLowFilters = rs[9]
    recorder_info.nHighFilters = rs[10]

    recorder_struct = struct.Struct("20f")
    recorder_info.sensitivity = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_info.lowFilter = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_info.highFilter = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<33s2bhH")
    rs = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_info.montageName = string_trim_to_0(rs[0])
    recorder_info.numberOfChannelsUsed = rs[1]
    recorder_info.globalSens = rs[2]
    recorder_info.epochLengthInSamples = rs[3]
    recorder_info.highestRate = rs[4]

    recorder_struct = struct.Struct("<32H")
    sampling_rate = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct(32 * "9s")
    signal_type = [string_trim_to_0(x) for x in recorder_struct.unpack(sf.read(recorder_struct.size))]
    recorder_struct = struct.Struct(32 * "9s")
    signal_sub_type = [string_trim_to_0(x) for x in recorder_struct.unpack(sf.read(recorder_struct.size))]
    recorder_struct = struct.Struct(32 * "13s")
    channel_desc = [string_trim_to_0(x) for x in recorder_struct.unpack(sf.read(recorder_struct.size))]
    recorder_struct = struct.Struct("<32H")
    sensitivity_index = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<32H")
    low_filter_index = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<32H")
    high_filter_index = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<32H")
    delay = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct(32 * "5s")
    unit = [string_trim_to_0(x) for x in recorder_struct.unpack(sf.read(recorder_struct.size))]
    recorder_struct = struct.Struct("<32h")
    artefact_level = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<32h")
    cal_type = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<32f")
    cal_factor = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<32f")
    cal_offset = recorder_struct.unpack(sf.read(recorder_struct.size))
    recorder_struct = struct.Struct("<32H")
    save_buffer_size = recorder_struct.unpack(sf.read(recorder_struct.size))

    for i in range(32):
        rc = RecorderChannel(sampling_rate[i], signal_type[i], signal_sub_type[i], channel_desc[i], sensitivity_index[i],
                             low_filter_index[i], high_filter_index[i], delay[i], unit[i], artefact_level[i], cal_type[i], cal_factor[i],
                             cal_offset[i], save_buffer_size[i])
        recorder_info.channels.append(rc)

    return recorder_info


class SignalPage:
    def __init__(self):
        self.filling = 0
        self.time = time(0, 0, 0)


def eof(f):
    return f.tell() == os.fstat(f.fileno()).st_size


def read_signal_pages(sf, read_signal_data, file_size, offset, page_size, epoch_length, channels_used, channels):
    header_length = 6
    num_pages = int((file_size-offset)/page_size)
    pages=[None]*num_pages
    signals = [numpy.zeros(channels[i].save_buffer_size*num_pages) if read_signal_data else [] for i in range(channels_used)]
    current_offset = offset
    header_struct = struct.Struct("<Hl")
    stop = False
    sf.seek(current_offset)
    curr_page = -1
    while not stop and (not eof(sf)):
        curr_page += 1
        rs = header_struct.unpack(sf.read(header_struct.size))
        page = SignalPage()
        page.filling = rs[0]
        page.time = decode_time(rs[1])
        pages[curr_page]=page
        if page.filling != 0:
            stop = True
        else:
            data_size = page_size - header_length
        if not stop:
            current_offset += page_size
            if read_signal_data:
                for i in range(channels_used):
                    buffer_struct = struct.Struct(channels[i].save_buffer_size * "h")
                    b = buffer_struct.unpack(sf.read(buffer_struct.size))
                    start_index=curr_page*channels[i].save_buffer_size
                    numpy.put(signals[i], numpy.arange(start_index,start_index+channels[i].save_buffer_size), b)
            else:
                sf.seek(current_offset)
    if read_signal_data:
        for i in range(channels_used):
            signals[i] = signals[i] * channels[i].cal_factor + channels[i].cal_offset
    return pages, signals

def string_trim_to_0(s):
    s = list(s)
    for i in range(len(s)):
 #       if (ord(s[i]) < 1) or (ord(s[i]) > 128):
        if (ord(s[i]) < 1) or (ord(s[i]) >= 249):
            s[i] = u' '
        else:
            s[i] = unichr(ord(s[i]))
    #return u"".join(s).strip().decode("ASCII")
    return u"".join(s).strip()


def decode_time(tm):
    h = tm // (60 * 60 * 1000)
    m = (tm // (60 * 1000)) % 60
    s = (tm // 1000) % 60
    ms = tm % 1000
    return time(h if 0 <= h <= 23 else h - 24, m, s, ms * 1000)


def decode_time_seconds(tm):
    h = tm // (60 * 60 * 1000)
    m = (tm // (60 * 1000)) % 60
    s = (tm // 1000) % 60
    return time(h if 0 <= h <= 23 else h - 24, m, s, 0)


def time_to_time_seconds(tm):
    return tm.replace(microsecond=0)


def add_seconds_to_time(timeval, secs_to_add):
    return (datetime.combine(date(1, 1, 1), timeval) + timedelta(seconds=secs_to_add)).time()


def ms_to_events_seconds(ms):
    return floor(ms / 1000)


def decode_date(dt):
    y = dt // (31 * 12)
    m = (dt // 31) % 12
    if m == 0:
        m = 12
        y -= 1
    d = dt % 31
    if d == 0:
        d = 31
        m -= 1
    if y <= 0:
        return date(1900, 1, 1)
    return date(y, m, d)


def date_2_remlogic_date(c):
    return str(c.day) + '/' + str(c.month) + '/' + str(c.year)


def make_brainlab_filenames(fn):
    basename = splitext(fn)[0]
    return "".join([basename, ".sig"]), "".join([basename, ".tbl"])



class AnalyzeFile:
    def __init__(self):
        self.header = AnalyzeHeader()
        self.inventory = []
        self.stage_defs = {}
        self.events = []
        self.registration_events = []
        self.stage_defs = {}
        self.stages = []
        self.events_desc = []
        self.sleep_stg_vals = []
        self.sleep_stg_rem_vals = []
        self.sleep_stg_non_rem_vals = []
        self.first_sleep_stage = None
        self.last_sleep_stage = None
        self.sleep_period_time_hrs = 0
        self.sleep_period_time = 0
        self.sleep_stages = []
        self.sleep_time = 0
        self.sleep_time_hrs = 0
        self.sleep_wake_time = 0
        self.sleep_wake_time_hrs = 0
        self.sleep_n1_time = 0
        self.sleep_n1_time_hrs = 0
        self.sleep_n2_time = 0
        self.sleep_n2_time_hrs = 0
        self.sleep_n3_time = 0
        self.sleep_n3_time_hrs = 0
        self.sleep_rem_time = 0
        self.sleep_rem_time_hrs = 0
        self.respiratory_events = []
        self.saturation_events = []
        self.arousal_events = []
        self.rdi = 0
        self.odi = 0
        self.ai = 0


def read_analyze_file(file_name):
    af = AnalyzeFile()
    sf = open(file_name, 'rb')
    try:
        af.header = read_analyze_header(sf)
        af.inventory = read_file_inventory(sf)
        stage_block = None
        event_block = None
        for inv in af.inventory:
            if inv.item_id == InventoryItem.ID_STAGES:
                stage_block = inv
            if inv.item_id == InventoryItem.ID_EVENTS:
                event_block = inv
        stgs = read_stages(sf, stage_block.offset, stage_block.size)
        af.stage_defs = read_stage_types(sf)

        af.events = read_events(sf, event_block.offset, event_block.size)
        af.registration_events = []
        for ev in get_selected_events_4_types(af.events, [Event.ET_SAVESKIPEVENT]):
            af.registration_events.append(
                RecordingEvent(ev.page, ev.page + int(ms_to_events_seconds(ev.duration_in_ms) / 30) - 1,
                               decode_time_seconds(ev.time), decode_time_seconds(ev.end_time)))

        af.stages = transform_stages(stgs, af.stage_defs, af.registration_events)

        af.events_desc = read_event_descs(sf)
        af.sleep_stg_vals = get_sleep_values(af.stage_defs)
        af.sleep_stg_rem_vals = get_rem_values(af.stage_defs)
        af.sleep_stg_non_rem_vals = get_non_rem_values(af.stage_defs)
        af.first_sleep_stage = find_first_sleep_epoch(af.stages, af.sleep_stg_non_rem_vals, af.sleep_stg_vals)
        af.last_sleep_stage = find_last_sleep_epoch(af.stages, af.sleep_stg_vals)
        if (af.last_sleep_stage >= af.first_sleep_stage) and (af.first_sleep_stage != 0):
            af.sleep_period_time = (af.last_sleep_stage - af.first_sleep_stage) * 30
        af.sleep_period_time_hrs = af.sleep_period_time / (60 * 60)
        af.sleep_stages = [x for x in af.stages if (x.val in af.sleep_stg_vals)]
        af.sleep_time = len(af.sleep_stages) * 30
        af.sleep_time_hrs = af.sleep_time / (60 * 60)
        af.sleep_wake_time = len([x for x in af.stages if (
            (x.label == "W") and (x.no > af.first_sleep_stage) and (x.no <= af.last_sleep_stage))]) * 30
        af.sleep_wake_time_hrs = af.sleep_wake_time / (60 * 60)
        af.sleep_n1_time = len([x for x in af.stages if x.label == "N1"]) * 30
        af.sleep_n1_time_hrs = af.sleep_n1_time / (60 * 60)
        af.sleep_n2_time = len([x for x in af.stages if x.label == "N2"]) * 30
        af.sleep_n2_time_hrs = af.sleep_n2_time / (60 * 60)
        af.sleep_n3_time = len([x for x in af.stages if x.label == "N3"]) * 30
        af.sleep_n3_time_hrs = af.sleep_n3_time / (60 * 60)
        af.sleep_rem_time = len([x for x in af.stages if x.label == "R"]) * 30
        af.sleep_rem_time_hrs = af.sleep_rem_time / (60 * 60)
        resp_subtypes = [Event.ST_NONCLASSIFIEDAPNEA, Event.ST_CENTRALAPNEA, Event.ST_OBSTRUCTIVEAPNEA,
                         Event.ST_MIXEDAPNEA, Event.ST_NONCLASSIFIEDHYPOPNEA, Event.ST_CENTRALHYPOPNEA,
                         Event.ST_OBSTRUCTIVEHYPOPNEA, Event.ST_MIXEDHYPOPNEA, Event.ST_NEUTRAL,
                         Event.ST_PARADOXYCALAPNEA, Event.ST_PARADOXYCALHYPOPNEA, Event.ST_PERIODICALBREATHING]
        af.respiratory_events = get_selected_events(af.events, [Event.ET_RESPIRATIONEVENTS], resp_subtypes)
        af.saturation_events = get_selected_events(af.events, [Event.ET_SATURATIONEVENTS],
                                                   [Event.ST_DIPSATURATION])
        af.arousal_events = get_selected_events(af.events, [Event.ET_AROUSALEVENTS], [Event.ST_AROUSAL])
        if af.sleep_time_hrs != 0:
            af.rdi = len(af.respiratory_events) / af.sleep_time_hrs
            af.odi = len(af.saturation_events) / af.sleep_time_hrs
            af.ai = len(af.arousal_events) / af.sleep_time_hrs
    finally:
        sf.close()
    return af


def find_first_sleep_epoch(stages, sleep_stg_nrem_vals, sleep_stg_vals):
    scount = len(stages)
    for i in range(scount):
        if len(sleep_stg_nrem_vals) < 2:
            if stages[i].val in sleep_stg_vals:
                return i + 1
        else:
            if i > 0:
                if stages[i].val in sleep_stg_nrem_vals[1:]:
                    return i + 1
    return 0


def find_last_sleep_epoch(stages, sleep_stg_vals):
    scount = len(stages)
    last_stage = 0
    for i in range(scount):
        if stages[i].val in sleep_stg_vals:
            last_stage = i
    if last_stage > 0:
        return last_stage + 1
    return 0


class AnalyzeHeader:
    PROGRAM_ID = 0x41545353
    TABLE_ID = 0x534C4254

    def __init__(self, program_id=0, table_id=0, version_id=0):
        self.program_id = program_id
        self.table_id = table_id
        self.version_id = version_id

    def check_program_id(self):
        return self.program_id == AnalyzeHeader.PROGRAM_ID

    def check_table_id(self):
        return self.table_id == AnalyzeHeader.TABLE_ID

    def check_header(self):
        return self.check_program_id() and self.check_table_id()


def read_analyze_header(sf):
    sf.seek(0)
    header_struct = struct.Struct("<2lh")
    hb = header_struct.unpack(sf.read(header_struct.size))
    return AnalyzeHeader(hb[0], hb[1], hb[2])


class InventoryItem:
    ID_INVALID = 0x0000  # unused or invalid
    ID_SELECTEDPAGES = 0x0100  # Selected Pages
    ID_STAGES = 0x0200  # Stages
    ID_CALCULATEDSTAGES = 0x0210  # Calculated Stages
    ID_CALCSTAGESPARAMETERS = 0x0220  # Calculated Stages parameters
    ID_EVENTS = 0x0300  # Events
    ID_NOTES = 0x0400  # Notes
    ID_ECGPARAMETERS = 0x0500  # ECG parameters
    ID_ECGRATE = 0x0510  # ECG rate
    ID_ECGWAVE = 0x0520  # ECG wave
    ID_ECGRHYTHM = 0x0530  # ECG rhythm
    ID_RESPIRATIONPARAMETERS = 0x0600  # Respiration parameters
    ID_THORAXOLDHISTOGRAM = 0x0610  # Thorax histogram old
    ID_ABDOMENOLDHISTOGRAM = 0x0611  # Abdomen histogram old
    ID_FLOWOLDHISTOGRAM = 0x0612  # Flow histogram old
    ID_THORAXHISTOGRAM = 0x0615  # Thorax histogram
    ID_ABDOMENHISTOGRAM = 0x0616  # Abdomen histogram
    ID_FLOWHISTOGRAM = 0x0617  # Flow histogram
    ID_RESPIRATIONRATE = 0x0620  # Respiration rate
    ID_SATURATIONPARAMETERS = 0x0700  # Saturation parameters
    ID_SATURATIONRATE = 0x0710  # Saturation rate
    ID_SATURATIONSIGNAL = 0x0720  # Saturation signal
    ID_EMGPARAMETERS = 0x0800  # EMG parameters
    ID_EMGCHINSIGNAL = 0x0810  # EMG chin signal
    ID_EMGTIBIALSIGNAL_01 = 0x0820  # EMG tibial signal 1
    ID_EMGTIBIALSIGNAL_02 = 0x0821  # EMG tibial signal 2
    ID_EMGTIBIALSIGNAL_03 = 0x0822  # EMG tibial signal 3
    ID_EMGTIBIALSIGNAL_04 = 0x0823  # EMG tibial signal 4
    ID_EMGTIBIALSIGNAL_05 = 0x0824  # EMG tibial signal 5
    ID_EMGTIBIALSIGNAL_06 = 0x0825  # EMG tibial signal 6
    ID_EMGTIBIALSIGNAL_07 = 0x0826  # EMG tibial signal 7
    ID_EMGTIBIALSIGNAL_08 = 0x0827  # EMG tibial signal 8
    ID_EMGTIBIALSIGNAL_09 = 0x0828  # EMG tibial signal 9
    ID_EMGTIBIALSIGNAL_10 = 0x0829  # EMG tibial signal 10
    ID_EMGTIBIALSIGNAL_11 = 0x082a  # EMG tibial signal 11
    ID_EMGTIBIALSIGNAL_12 = 0x082b  # EMG tibial signal 12
    ID_EMGTIBIALSIGNAL_13 = 0x082c  # EMG tibial signal 13
    ID_EMGTIBIALSIGNAL_14 = 0x082d  # EMG tibial signal 14
    ID_EMGTIBIALSIGNAL_15 = 0x082e  # EMG tibial signal 15
    ID_EMGTIBIALSIGNAL_16 = 0x082f  # EMG tibial signal 16
    ID_EMGTIBIALSIGNAL_17 = 0x0830  # EMG tibial signal 17
    ID_EMGTIBIALSIGNAL_18 = 0x0831  # EMG tibial signal 18
    ID_EMGTIBIALSIGNAL_19 = 0x0832  # EMG tibial signal 19
    ID_EMGTIBIALSIGNAL_20 = 0x0833  # EMG tibial signal 20
    ID_EMGTIBIALSIGNAL_21 = 0x0834  # EMG tibial signal 21
    ID_EMGTIBIALSIGNAL_22 = 0x0835  # EMG tibial signal 22
    ID_EMGTIBIALSIGNAL_23 = 0x0836  # EMG tibial signal 23
    ID_EMGTIBIALSIGNAL_24 = 0x0837  # EMG tibial signal 24
    ID_EMGTIBIALSIGNAL_25 = 0x0838  # EMG tibial signal 25
    ID_EMGTIBIALSIGNAL_26 = 0x0839  # EMG tibial signal 26
    ID_EMGTIBIALSIGNAL_27 = 0x083a  # EMG tibial signal 27
    ID_EMGTIBIALSIGNAL_28 = 0x083b  # EMG tibial signal 28
    ID_EMGTIBIALSIGNAL_29 = 0x083c  # EMG tibial signal 29
    ID_EMGTIBIALSIGNAL_30 = 0x083d  # EMG tibial signal 30
    ID_EMGTIBIALSIGNAL_31 = 0x083e  # EMG tibial signal 31
    ID_EMGTIBIALSIGNAL_32 = 0x083f  # EMG tibial signal 32
    ID_EEGDELTAPARAMETERS = 0x0900  # EEG Delta parameters
    ID_EEGDELTAHISTOGRAM_01 = 0x0910  # EEG Delta Histogram channel 1
    ID_EEGDELTAHISTOGRAM_02 = 0x0911  # EEG Delta Histogram channel 2
    ID_EEGDELTAHISTOGRAM_03 = 0x0912  # EEG Delta Histogram channel 3
    ID_EEGDELTAHISTOGRAM_04 = 0x0913  # EEG Delta Histogram channel 4
    ID_EEGDELTAHISTOGRAM_05 = 0x0914  # EEG Delta Histogram channel 5
    ID_EEGDELTAHISTOGRAM_06 = 0x0915  # EEG Delta Histogram channel 6
    ID_EEGDELTAHISTOGRAM_07 = 0x0916  # EEG Delta Histogram channel 7
    ID_EEGDELTAHISTOGRAM_08 = 0x0917  # EEG Delta Histogram channel 8
    ID_EEGDELTAHISTOGRAM_09 = 0x0918  # EEG Delta Histogram channel 9
    ID_EEGDELTAHISTOGRAM_10 = 0x0919  # EEG Delta Histogram channel 10
    ID_EEGDELTAHISTOGRAM_11 = 0x091a  # EEG Delta Histogram channel 11
    ID_EEGDELTAHISTOGRAM_12 = 0x091b  # EEG Delta Histogram channel 12
    ID_EEGDELTAHISTOGRAM_13 = 0x091c  # EEG Delta Histogram channel 13
    ID_EEGDELTAHISTOGRAM_14 = 0x091d  # EEG Delta Histogram channel 14
    ID_EEGDELTAHISTOGRAM_15 = 0x091e  # EEG Delta Histogram channel 15
    ID_EEGDELTAHISTOGRAM_16 = 0x091f  # EEG Delta Histogram channel 16
    ID_EEGDELTAHISTOGRAM_17 = 0x0920  # EEG Delta Histogram channel 17
    ID_EEGDELTAHISTOGRAM_18 = 0x0921  # EEG Delta Histogram channel 18
    ID_EEGDELTAHISTOGRAM_19 = 0x0922  # EEG Delta Histogram channel 19
    ID_EEGDELTAHISTOGRAM_20 = 0x0923  # EEG Delta Histogram channel 20
    ID_EEGDELTAHISTOGRAM_21 = 0x0924  # EEG Delta Histogram channel 21
    ID_EEGDELTAHISTOGRAM_22 = 0x0925  # EEG Delta Histogram channel 22
    ID_EEGDELTAHISTOGRAM_23 = 0x0926  # EEG Delta Histogram channel 23
    ID_EEGDELTAHISTOGRAM_24 = 0x0927  # EEG Delta Histogram channel 24
    ID_EEGDELTAHISTOGRAM_25 = 0x0928  # EEG Delta Histogram channel 25
    ID_EEGDELTAHISTOGRAM_26 = 0x0929  # EEG Delta Histogram channel 26
    ID_EEGDELTAHISTOGRAM_27 = 0x092a  # EEG Delta Histogram channel 27
    ID_EEGDELTAHISTOGRAM_28 = 0x092b  # EEG Delta Histogram channel 28
    ID_EEGDELTAHISTOGRAM_29 = 0x092c  # EEG Delta Histogram channel 29
    ID_EEGDELTAHISTOGRAM_30 = 0x092d  # EEG Delta Histogram channel 30
    ID_EEGDELTAHISTOGRAM_31 = 0x092e  # EEG Delta Histogram channel 31
    ID_EEGDELTAHISTOGRAM_32 = 0x092f  # EEG Delta Histogram channel 32
    ID_EEGDELTAPERCENTAGE_01 = 0x0930  # EEG Delta Percentage channel 1
    ID_EEGDELTAPERCENTAGE_02 = 0x0931  # EEG Delta Percentage channel 2
    ID_EEGDELTAPERCENTAGE_03 = 0x0932  # EEG Delta Percentage channel 3
    ID_EEGDELTAPERCENTAGE_04 = 0x0933  # EEG Delta Percentage channel 4
    ID_EEGDELTAPERCENTAGE_05 = 0x0934  # EEG Delta Percentage channel 5
    ID_EEGDELTAPERCENTAGE_06 = 0x0935  # EEG Delta Percentage channel 6
    ID_EEGDELTAPERCENTAGE_07 = 0x0936  # EEG Delta Percentage channel 7
    ID_EEGDELTAPERCENTAGE_08 = 0x0937  # EEG Delta Percentage channel 8
    ID_EEGDELTAPERCENTAGE_09 = 0x0938  # EEG Delta Percentage channel 9
    ID_EEGDELTAPERCENTAGE_10 = 0x0939  # EEG Delta Percentage channel 10
    ID_EEGDELTAPERCENTAGE_11 = 0x093a  # EEG Delta Percentage channel 11
    ID_EEGDELTAPERCENTAGE_12 = 0x093b  # EEG Delta Percentage channel 12
    ID_EEGDELTAPERCENTAGE_13 = 0x093c  # EEG Delta Percentage channel 13
    ID_EEGDELTAPERCENTAGE_14 = 0x093d  # EEG Delta Percentage channel 14
    ID_EEGDELTAPERCENTAGE_15 = 0x093e  # EEG Delta Percentage channel 15
    ID_EEGDELTAPERCENTAGE_16 = 0x093f  # EEG Delta Percentage channel 16
    ID_EEGDELTAPERCENTAGE_17 = 0x0940  # EEG Delta Percentage channel 17
    ID_EEGDELTAPERCENTAGE_18 = 0x0941  # EEG Delta Percentage channel 18
    ID_EEGDELTAPERCENTAGE_19 = 0x0942  # EEG Delta Percentage channel 19
    ID_EEGDELTAPERCENTAGE_20 = 0x0943  # EEG Delta Percentage channel 20
    ID_EEGDELTAPERCENTAGE_21 = 0x0944  # EEG Delta Percentage channel 21
    ID_EEGDELTAPERCENTAGE_22 = 0x0945  # EEG Delta Percentage channel 22
    ID_EEGDELTAPERCENTAGE_23 = 0x0946  # EEG Delta Percentage channel 23
    ID_EEGDELTAPERCENTAGE_24 = 0x0947  # EEG Delta Percentage channel 24
    ID_EEGDELTAPERCENTAGE_25 = 0x0948  # EEG Delta Percentage channel 25
    ID_EEGDELTAPERCENTAGE_26 = 0x0949  # EEG Delta Percentage channel 26
    ID_EEGDELTAPERCENTAGE_27 = 0x094a  # EEG Delta Percentage channel 27
    ID_EEGDELTAPERCENTAGE_28 = 0x094b  # EEG Delta Percentage channel 28
    ID_EEGDELTAPERCENTAGE_29 = 0x094c  # EEG Delta Percentage channel 29
    ID_EEGDELTAPERCENTAGE_30 = 0x094d  # EEG Delta Percentage channel 30
    ID_EEGDELTAPERCENTAGE_31 = 0x094e  # EEG Delta Percentage channel 31
    ID_EEGDELTAPERCENTAGE_32 = 0x094f  # EEG Delta Percentage channel 32
    ID_EEGDELTACOUNT_01 = 0x0950  # EEG Delta Count channel 1
    ID_EEGDELTACOUNT_02 = 0x0951  # EEG Delta Count channel 2
    ID_EEGDELTACOUNT_03 = 0x0952  # EEG Delta Count channel 3
    ID_EEGDELTACOUNT_04 = 0x0953  # EEG Delta Count channel 4
    ID_EEGDELTACOUNT_05 = 0x0954  # EEG Delta Count channel 5
    ID_EEGDELTACOUNT_06 = 0x0955  # EEG Delta Count channel 6
    ID_EEGDELTACOUNT_07 = 0x0956  # EEG Delta Count channel 7
    ID_EEGDELTACOUNT_08 = 0x0957  # EEG Delta Count channel 8
    ID_EEGDELTACOUNT_09 = 0x0958  # EEG Delta Count channel 9
    ID_EEGDELTACOUNT_10 = 0x0959  # EEG Delta Count channel 10
    ID_EEGDELTACOUNT_11 = 0x095a  # EEG Delta Count channel 11
    ID_EEGDELTACOUNT_12 = 0x095b  # EEG Delta Count channel 12
    ID_EEGDELTACOUNT_13 = 0x095c  # EEG Delta Count channel 13
    ID_EEGDELTACOUNT_14 = 0x095d  # EEG Delta Count channel 14
    ID_EEGDELTACOUNT_15 = 0x095e  # EEG Delta Count channel 15
    ID_EEGDELTACOUNT_16 = 0x095f  # EEG Delta Count channel 16
    ID_EEGDELTACOUNT_17 = 0x0960  # EEG Delta Count channel 17
    ID_EEGDELTACOUNT_18 = 0x0961  # EEG Delta Count channel 18
    ID_EEGDELTACOUNT_19 = 0x0962  # EEG Delta Count channel 19
    ID_EEGDELTACOUNT_20 = 0x0963  # EEG Delta Count channel 20
    ID_EEGDELTACOUNT_21 = 0x0964  # EEG Delta Count channel 21
    ID_EEGDELTACOUNT_22 = 0x0965  # EEG Delta Count channel 22
    ID_EEGDELTACOUNT_23 = 0x0966  # EEG Delta Count channel 23
    ID_EEGDELTACOUNT_24 = 0x0967  # EEG Delta Count channel 24
    ID_EEGDELTACOUNT_25 = 0x0968  # EEG Delta Count channel 25
    ID_EEGDELTACOUNT_26 = 0x0969  # EEG Delta Count channel 26
    ID_EEGDELTACOUNT_27 = 0x096a  # EEG Delta Count channel 27
    ID_EEGDELTACOUNT_28 = 0x096b  # EEG Delta Count channel 28
    ID_EEGDELTACOUNT_29 = 0x096c  # EEG Delta Count channel 29
    ID_EEGDELTACOUNT_30 = 0x096d  # EEG Delta Count channel 30
    ID_EEGDELTACOUNT_31 = 0x096e  # EEG Delta Count channel 31
    ID_EEGDELTACOUNT_32 = 0x096f  # EEG Delta Count channel 32
    ID_EEGSPINDLEPARAMETERS = 0x0a00  # EEG Spindle parameters
    ID_EEGSPINDLEHISTOGRAM_01 = 0x0a10  # EEG Spindle Histogram channel 1
    ID_EEGSPINDLEHISTOGRAM_02 = 0x0a11  # EEG Spindle Histogram channel 2
    ID_EEGSPINDLEHISTOGRAM_03 = 0x0a12  # EEG Spindle Histogram channel 3
    ID_EEGSPINDLEHISTOGRAM_04 = 0x0a13  # EEG Spindle Histogram channel 4
    ID_EEGSPINDLEHISTOGRAM_05 = 0x0a14  # EEG Spindle Histogram channel 5
    ID_EEGSPINDLEHISTOGRAM_06 = 0x0a15  # EEG Spindle Histogram channel 6
    ID_EEGSPINDLEHISTOGRAM_07 = 0x0a16  # EEG Spindle Histogram channel 7
    ID_EEGSPINDLEHISTOGRAM_08 = 0x0a17  # EEG Spindle Histogram channel 8
    ID_EEGSPINDLEHISTOGRAM_09 = 0x0a18  # EEG Spindle Histogram channel 9
    ID_EEGSPINDLEHISTOGRAM_10 = 0x0a19  # EEG Spindle Histogram channel 10
    ID_EEGSPINDLEHISTOGRAM_11 = 0x0a1a  # EEG Spindle Histogram channel 11
    ID_EEGSPINDLEHISTOGRAM_12 = 0x0a1b  # EEG Spindle Histogram channel 12
    ID_EEGSPINDLEHISTOGRAM_13 = 0x0a1c  # EEG Spindle Histogram channel 13
    ID_EEGSPINDLEHISTOGRAM_14 = 0x0a1d  # EEG Spindle Histogram channel 14
    ID_EEGSPINDLEHISTOGRAM_15 = 0x0a1e  # EEG Spindle Histogram channel 15
    ID_EEGSPINDLEHISTOGRAM_16 = 0x0a1f  # EEG Spindle Histogram channel 16
    ID_EEGSPINDLEHISTOGRAM_17 = 0x0a20  # EEG Spindle Histogram channel 17
    ID_EEGSPINDLEHISTOGRAM_18 = 0x0a21  # EEG Spindle Histogram channel 18
    ID_EEGSPINDLEHISTOGRAM_19 = 0x0a22  # EEG Spindle Histogram channel 19
    ID_EEGSPINDLEHISTOGRAM_20 = 0x0a23  # EEG Spindle Histogram channel 20
    ID_EEGSPINDLEHISTOGRAM_21 = 0x0a24  # EEG Spindle Histogram channel 21
    ID_EEGSPINDLEHISTOGRAM_22 = 0x0a25  # EEG Spindle Histogram channel 22
    ID_EEGSPINDLEHISTOGRAM_23 = 0x0a26  # EEG Spindle Histogram channel 23
    ID_EEGSPINDLEHISTOGRAM_24 = 0x0a27  # EEG Spindle Histogram channel 24
    ID_EEGSPINDLEHISTOGRAM_25 = 0x0a28  # EEG Spindle Histogram channel 25
    ID_EEGSPINDLEHISTOGRAM_26 = 0x0a29  # EEG Spindle Histogram channel 26
    ID_EEGSPINDLEHISTOGRAM_27 = 0x0a2a  # EEG Spindle Histogram channel 27
    ID_EEGSPINDLEHISTOGRAM_28 = 0x0a2b  # EEG Spindle Histogram channel 28
    ID_EEGSPINDLEHISTOGRAM_29 = 0x0a2c  # EEG Spindle Histogram channel 29
    ID_EEGSPINDLEHISTOGRAM_30 = 0x0a2d  # EEG Spindle Histogram channel 30
    ID_EEGSPINDLEHISTOGRAM_31 = 0x0a2e  # EEG Spindle Histogram channel 31
    ID_EEGSPINDLEHISTOGRAM_32 = 0x0a2f  # EEG Spindle Histogram channel 32
    ID_EEGALPHAOLDPARAMETERS = 0x0b00  # EEG Alpha old-style parameters
    ID_EEGALPHASIGNAL_01 = 0x0b10  # EEG Alpha Histogram channel 1
    ID_EEGALPHASIGNAL_02 = 0x0b11  # EEG Alpha Histogram channel 2
    ID_EEGALPHASIGNAL_03 = 0x0b12  # EEG Alpha Histogram channel 3
    ID_EEGALPHASIGNAL_04 = 0x0b13  # EEG Alpha Histogram channel 4
    ID_EEGALPHASIGNAL_05 = 0x0b14  # EEG Alpha Histogram channel 5
    ID_EEGALPHASIGNAL_06 = 0x0b15  # EEG Alpha Histogram channel 6
    ID_EEGALPHASIGNAL_07 = 0x0b16  # EEG Alpha Histogram channel 7
    ID_EEGALPHASIGNAL_08 = 0x0b17  # EEG Alpha Histogram channel 8
    ID_EEGALPHASIGNAL_09 = 0x0b18  # EEG Alpha Histogram channel 9
    ID_EEGALPHASIGNAL_10 = 0x0b19  # EEG Alpha Histogram channel 10
    ID_EEGALPHASIGNAL_11 = 0x0b1a  # EEG Alpha Histogram channel 11
    ID_EEGALPHASIGNAL_12 = 0x0b1b  # EEG Alpha Histogram channel 12
    ID_EEGALPHASIGNAL_13 = 0x0b1c  # EEG Alpha Histogram channel 13
    ID_EEGALPHASIGNAL_14 = 0x0b1d  # EEG Alpha Histogram channel 14
    ID_EEGALPHASIGNAL_15 = 0x0b1e  # EEG Alpha Histogram channel 15
    ID_EEGALPHASIGNAL_16 = 0x0b1f  # EEG Alpha Histogram channel 16
    ID_EEGALPHASIGNAL_17 = 0x0b20  # EEG Alpha Histogram channel 17
    ID_EEGALPHASIGNAL_18 = 0x0b21  # EEG Alpha Histogram channel 18
    ID_EEGALPHASIGNAL_19 = 0x0b22  # EEG Alpha Histogram channel 19
    ID_EEGALPHASIGNAL_20 = 0x0b23  # EEG Alpha Histogram channel 20
    ID_EEGALPHASIGNAL_21 = 0x0b24  # EEG Alpha Histogram channel 21
    ID_EEGALPHASIGNAL_22 = 0x0b25  # EEG Alpha Histogram channel 22
    ID_EEGALPHASIGNAL_23 = 0x0b26  # EEG Alpha Histogram channel 23
    ID_EEGALPHASIGNAL_24 = 0x0b27  # EEG Alpha Histogram channel 24
    ID_EEGALPHASIGNAL_25 = 0x0b28  # EEG Alpha Histogram channel 25
    ID_EEGALPHASIGNAL_26 = 0x0b29  # EEG Alpha Histogram channel 26
    ID_EEGALPHASIGNAL_27 = 0x0b2a  # EEG Alpha Histogram channel 27
    ID_EEGALPHASIGNAL_28 = 0x0b2b  # EEG Alpha Histogram channel 28
    ID_EEGALPHASIGNAL_29 = 0x0b2c  # EEG Alpha Histogram channel 29
    ID_EEGALPHASIGNAL_30 = 0x0b2d  # EEG Alpha Histogram channel 30
    ID_EEGALPHASIGNAL_31 = 0x0b2e  # EEG Alpha Histogram channel 31
    ID_EEGALPHASIGNAL_32 = 0x0b2f  # EEG Alpha Histogram channel 32
    ID_EEGALPHAPARAMETERS = 0x0b80  # EEG Alpha parameters
    ID_EEGALPHAHISTOGRAM_01 = 0x0b90  # EEG Alpha Histogram channel 1
    ID_EEGALPHAHISTOGRAM_02 = 0x0b91  # EEG Alpha Histogram channel 2
    ID_EEGALPHAHISTOGRAM_03 = 0x0b92  # EEG Alpha Histogram channel 3
    ID_EEGALPHAHISTOGRAM_04 = 0x0b93  # EEG Alpha Histogram channel 4
    ID_EEGALPHAHISTOGRAM_05 = 0x0b94  # EEG Alpha Histogram channel 5
    ID_EEGALPHAHISTOGRAM_06 = 0x0b95  # EEG Alpha Histogram channel 6
    ID_EEGALPHAHISTOGRAM_07 = 0x0b96  # EEG Alpha Histogram channel 7
    ID_EEGALPHAHISTOGRAM_08 = 0x0b97  # EEG Alpha Histogram channel 8
    ID_EEGALPHAHISTOGRAM_09 = 0x0b98  # EEG Alpha Histogram channel 9
    ID_EEGALPHAHISTOGRAM_10 = 0x0b99  # EEG Alpha Histogram channel 10
    ID_EEGALPHAHISTOGRAM_11 = 0x0b9a  # EEG Alpha Histogram channel 11
    ID_EEGALPHAHISTOGRAM_12 = 0x0b9b  # EEG Alpha Histogram channel 12
    ID_EEGALPHAHISTOGRAM_13 = 0x0b9c  # EEG Alpha Histogram channel 13
    ID_EEGALPHAHISTOGRAM_14 = 0x0b9d  # EEG Alpha Histogram channel 14
    ID_EEGALPHAHISTOGRAM_15 = 0x0b9e  # EEG Alpha Histogram channel 15
    ID_EEGALPHAHISTOGRAM_16 = 0x0b9f  # EEG Alpha Histogram channel 16
    ID_EEGALPHAHISTOGRAM_17 = 0x0ba0  # EEG Alpha Histogram channel 17
    ID_EEGALPHAHISTOGRAM_18 = 0x0ba1  # EEG Alpha Histogram channel 18
    ID_EEGALPHAHISTOGRAM_19 = 0x0ba2  # EEG Alpha Histogram channel 19
    ID_EEGALPHAHISTOGRAM_20 = 0x0ba3  # EEG Alpha Histogram channel 20
    ID_EEGALPHAHISTOGRAM_21 = 0x0ba4  # EEG Alpha Histogram channel 21
    ID_EEGALPHAHISTOGRAM_22 = 0x0ba5  # EEG Alpha Histogram channel 22
    ID_EEGALPHAHISTOGRAM_23 = 0x0ba6  # EEG Alpha Histogram channel 23
    ID_EEGALPHAHISTOGRAM_24 = 0x0ba7  # EEG Alpha Histogram channel 24
    ID_EEGALPHAHISTOGRAM_25 = 0x0ba8  # EEG Alpha Histogram channel 25
    ID_EEGALPHAHISTOGRAM_26 = 0x0ba9  # EEG Alpha Histogram channel 26
    ID_EEGALPHAHISTOGRAM_27 = 0x0baa  # EEG Alpha Histogram channel 27
    ID_EEGALPHAHISTOGRAM_28 = 0x0bab  # EEG Alpha Histogram channel 28
    ID_EEGALPHAHISTOGRAM_29 = 0x0bac  # EEG Alpha Histogram channel 29
    ID_EEGALPHAHISTOGRAM_30 = 0x0bad  # EEG Alpha Histogram channel 30
    ID_EEGALPHAHISTOGRAM_31 = 0x0bae  # EEG Alpha Histogram channel 31
    ID_EEGALPHAHISTOGRAM_32 = 0x0baf  # EEG Alpha Histogram channel 32
    ID_EEGALPHAPERCENTAGE_01 = 0x0bb0  # EEG Alpha Percentage channel 1
    ID_EEGALPHAPERCENTAGE_02 = 0x0bb1  # EEG Alpha Percentage channel 2
    ID_EEGALPHAPERCENTAGE_03 = 0x0bb2  # EEG Alpha Percentage channel 3
    ID_EEGALPHAPERCENTAGE_04 = 0x0bb3  # EEG Alpha Percentage channel 4
    ID_EEGALPHAPERCENTAGE_05 = 0x0bb4  # EEG Alpha Percentage channel 5
    ID_EEGALPHAPERCENTAGE_06 = 0x0bb5  # EEG Alpha Percentage channel 6
    ID_EEGALPHAPERCENTAGE_07 = 0x0bb6  # EEG Alpha Percentage channel 7
    ID_EEGALPHAPERCENTAGE_08 = 0x0bb7  # EEG Alpha Percentage channel 8
    ID_EEGALPHAPERCENTAGE_09 = 0x0bb8  # EEG Alpha Percentage channel 9
    ID_EEGALPHAPERCENTAGE_10 = 0x0bb9  # EEG Alpha Percentage channel 10
    ID_EEGALPHAPERCENTAGE_11 = 0x0bba  # EEG Alpha Percentage channel 11
    ID_EEGALPHAPERCENTAGE_12 = 0x0bbb  # EEG Alpha Percentage channel 12
    ID_EEGALPHAPERCENTAGE_13 = 0x0bbc  # EEG Alpha Percentage channel 13
    ID_EEGALPHAPERCENTAGE_14 = 0x0bbd  # EEG Alpha Percentage channel 14
    ID_EEGALPHAPERCENTAGE_15 = 0x0bbe  # EEG Alpha Percentage channel 15
    ID_EEGALPHAPERCENTAGE_16 = 0x0bbf  # EEG Alpha Percentage channel 16
    ID_EEGALPHAPERCENTAGE_17 = 0x0bc0  # EEG Alpha Percentage channel 17
    ID_EEGALPHAPERCENTAGE_18 = 0x0bc1  # EEG Alpha Percentage channel 18
    ID_EEGALPHAPERCENTAGE_19 = 0x0bc2  # EEG Alpha Percentage channel 19
    ID_EEGALPHAPERCENTAGE_20 = 0x0bc3  # EEG Alpha Percentage channel 20
    ID_EEGALPHAPERCENTAGE_21 = 0x0bc4  # EEG Alpha Percentage channel 21
    ID_EEGALPHAPERCENTAGE_22 = 0x0bc5  # EEG Alpha Percentage channel 22
    ID_EEGALPHAPERCENTAGE_23 = 0x0bc6  # EEG Alpha Percentage channel 23
    ID_EEGALPHAPERCENTAGE_24 = 0x0bc7  # EEG Alpha Percentage channel 24
    ID_EEGALPHAPERCENTAGE_25 = 0x0bc8  # EEG Alpha Percentage channel 25
    ID_EEGALPHAPERCENTAGE_26 = 0x0bc9  # EEG Alpha Percentage channel 26
    ID_EEGALPHAPERCENTAGE_27 = 0x0bca  # EEG Alpha Percentage channel 27
    ID_EEGALPHAPERCENTAGE_28 = 0x0bcb  # EEG Alpha Percentage channel 28
    ID_EEGALPHAPERCENTAGE_29 = 0x0bcc  # EEG Alpha Percentage channel 29
    ID_EEGALPHAPERCENTAGE_30 = 0x0bcd  # EEG Alpha Percentage channel 30
    ID_EEGALPHAPERCENTAGE_31 = 0x0bce  # EEG Alpha Percentage channel 31
    ID_EEGALPHAPERCENTAGE_32 = 0x0bcf  # EEG Alpha Percentage channel 32
    ID_EOGPARAMETERS = 0x0c00  # EOG parameters
    ID_EOGREMHISTOGRAM_01 = 0x0c10  # EOG REM Histogram channel 1
    ID_EOGREMHISTOGRAM_02 = 0x0c11  # EOG REM Histogram channel 2
    ID_EOGREMCOUNT_01 = 0x0c30  # EOG REM Count channel 1
    ID_EOGREMCOUNT_02 = 0x0c31  # EOG REM Count channel 2
    ID_EOGSEMHISTOGRAM = 0x0c50  # EOG SEM Histogram
    ID_EOGSEMCOUNT = 0x0c70  # EOG SEM Count
    ID_EOGBLINKCOUNT_01 = 0x0c90  # EOG Blink Count channel 1
    ID_EOGBLINKCOUNT_02 = 0x0c91  # EOG Blink Count channel 2
    ID_EEGTHETAPARAMETERS = 0x0d00  # EEG Theta parameters
    ID_EEGTHETASIGNAL_01 = 0x0d10  # EEG Theta Histogram channel 1
    ID_EEGTHETASIGNAL_02 = 0x0d11  # EEG Theta Histogram channel 2
    ID_EEGTHETASIGNAL_03 = 0x0d12  # EEG Theta Histogram channel 3
    ID_EEGTHETASIGNAL_04 = 0x0d13  # EEG Theta Histogram channel 4
    ID_EEGTHETASIGNAL_05 = 0x0d14  # EEG Theta Histogram channel 5
    ID_EEGTHETASIGNAL_06 = 0x0d15  # EEG Theta Histogram channel 6
    ID_EEGTHETASIGNAL_07 = 0x0d16  # EEG Theta Histogram channel 7
    ID_EEGTHETASIGNAL_08 = 0x0d17  # EEG Theta Histogram channel 8
    ID_EEGTHETASIGNAL_09 = 0x0d18  # EEG Theta Histogram channel 9
    ID_EEGTHETASIGNAL_10 = 0x0d19  # EEG Theta Histogram channel 10
    ID_EEGTHETASIGNAL_11 = 0x0d1a  # EEG Theta Histogram channel 11
    ID_EEGTHETASIGNAL_12 = 0x0d1b  # EEG Theta Histogram channel 12
    ID_EEGTHETASIGNAL_13 = 0x0d1c  # EEG Theta Histogram channel 13
    ID_EEGTHETASIGNAL_14 = 0x0d1d  # EEG Theta Histogram channel 14
    ID_EEGTHETASIGNAL_15 = 0x0d1e  # EEG Theta Histogram channel 15
    ID_EEGTHETASIGNAL_16 = 0x0d1f  # EEG Theta Histogram channel 16
    ID_EEGTHETASIGNAL_17 = 0x0d20  # EEG Theta Histogram channel 17
    ID_EEGTHETASIGNAL_18 = 0x0d21  # EEG Theta Histogram channel 18
    ID_EEGTHETASIGNAL_19 = 0x0d22  # EEG Theta Histogram channel 19
    ID_EEGTHETASIGNAL_20 = 0x0d23  # EEG Theta Histogram channel 20
    ID_EEGTHETASIGNAL_21 = 0x0d24  # EEG Theta Histogram channel 21
    ID_EEGTHETASIGNAL_22 = 0x0d25  # EEG Theta Histogram channel 22
    ID_EEGTHETASIGNAL_23 = 0x0d26  # EEG Theta Histogram channel 23
    ID_EEGTHETASIGNAL_24 = 0x0d27  # EEG Theta Histogram channel 24
    ID_EEGTHETASIGNAL_25 = 0x0d28  # EEG Theta Histogram channel 25
    ID_EEGTHETASIGNAL_26 = 0x0d29  # EEG Theta Histogram channel 26
    ID_EEGTHETASIGNAL_27 = 0x0d2a  # EEG Theta Histogram channel 27
    ID_EEGTHETASIGNAL_28 = 0x0d2b  # EEG Theta Histogram channel 28
    ID_EEGTHETASIGNAL_29 = 0x0d2c  # EEG Theta Histogram channel 29
    ID_EEGTHETASIGNAL_30 = 0x0d2d  # EEG Theta Histogram channel 30
    ID_EEGTHETASIGNAL_31 = 0x0d2e  # EEG Theta Histogram channel 31
    ID_EEGTHETASIGNAL_32 = 0x0d2f  # EEG Theta Histogram channel 32
    ID_EEGBETAPARAMETERS = 0x0e00  # EEG Beta parameters
    ID_EEGBETASIGNAL_01 = 0x0e10  # EEG Beta Histogram channel 1
    ID_EEGBETASIGNAL_02 = 0x0e11  # EEG Beta Histogram channel 2
    ID_EEGBETASIGNAL_03 = 0x0e12  # EEG Beta Histogram channel 3
    ID_EEGBETASIGNAL_04 = 0x0e13  # EEG Beta Histogram channel 4
    ID_EEGBETASIGNAL_05 = 0x0e14  # EEG Beta Histogram channel 5
    ID_EEGBETASIGNAL_06 = 0x0e15  # EEG Beta Histogram channel 6
    ID_EEGBETASIGNAL_07 = 0x0e16  # EEG Beta Histogram channel 7
    ID_EEGBETASIGNAL_08 = 0x0e17  # EEG Beta Histogram channel 8
    ID_EEGBETASIGNAL_09 = 0x0e18  # EEG Beta Histogram channel 9
    ID_EEGBETASIGNAL_10 = 0x0e19  # EEG Beta Histogram channel 10
    ID_EEGBETASIGNAL_11 = 0x0e1a  # EEG Beta Histogram channel 11
    ID_EEGBETASIGNAL_12 = 0x0e1b  # EEG Beta Histogram channel 12
    ID_EEGBETASIGNAL_13 = 0x0e1c  # EEG Beta Histogram channel 13
    ID_EEGBETASIGNAL_14 = 0x0e1d  # EEG Beta Histogram channel 14
    ID_EEGBETASIGNAL_15 = 0x0e1e  # EEG Beta Histogram channel 15
    ID_EEGBETASIGNAL_16 = 0x0e1f  # EEG Beta Histogram channel 16
    ID_EEGBETASIGNAL_17 = 0x0e20  # EEG Beta Histogram channel 17
    ID_EEGBETASIGNAL_18 = 0x0e21  # EEG Beta Histogram channel 18
    ID_EEGBETASIGNAL_19 = 0x0e22  # EEG Beta Histogram channel 19
    ID_EEGBETASIGNAL_20 = 0x0e23  # EEG Beta Histogram channel 20
    ID_EEGBETASIGNAL_21 = 0x0e24  # EEG Beta Histogram channel 21
    ID_EEGBETASIGNAL_22 = 0x0e25  # EEG Beta Histogram channel 22
    ID_EEGBETASIGNAL_23 = 0x0e26  # EEG Beta Histogram channel 23
    ID_EEGBETASIGNAL_24 = 0x0e27  # EEG Beta Histogram channel 24
    ID_EEGBETASIGNAL_25 = 0x0e28  # EEG Beta Histogram channel 25
    ID_EEGBETASIGNAL_26 = 0x0e29  # EEG Beta Histogram channel 26
    ID_EEGBETASIGNAL_27 = 0x0e2a  # EEG Beta Histogram channel 27
    ID_EEGBETASIGNAL_28 = 0x0e2b  # EEG Beta Histogram channel 28
    ID_EEGBETASIGNAL_29 = 0x0e2c  # EEG Beta Histogram channel 29
    ID_EEGBETASIGNAL_30 = 0x0e2d  # EEG Beta Histogram channel 30
    ID_EEGBETASIGNAL_31 = 0x0e2e  # EEG Beta Histogram channel 31
    ID_EEGBETASIGNAL_32 = 0x0e2f  # EEG Beta Histogram channel 32
    ID_BODYPOSPARAMETERS = 0x0f00  # Body position parameters
    ID_SOUNDPARAMETERS = 0x1000  # Sound parameters
    ID_SOUND = 0x1010  # Sound signal
    ID_CPAPPRESSUREPARAMETERS = 0x1100  # CPAPparameters
    ID_CPAPPRESSUREVALUES = 0x1110  # CPAP page values

    ID_DICT = {ID_INVALID: "ID_INVALID",
               ID_SELECTEDPAGES: "ID_SELECTEDPAGES",
               ID_STAGES: "ID_STAGES",
               ID_CALCULATEDSTAGES: "ID_CALCULATEDSTAGES",
               ID_CALCSTAGESPARAMETERS: "ID_CALCSTAGESPARAMETERS",
               ID_EVENTS: "ID_EVENTS",
               ID_NOTES: "ID_NOTES",
               ID_ECGPARAMETERS: "ID_ECGPARAMETERS",
               ID_ECGRATE: "ID_ECGRATE",
               ID_ECGWAVE: "ID_ECGWAVE",
               ID_ECGRHYTHM: "ID_ECGRHYTHM",
               ID_RESPIRATIONPARAMETERS: "ID_RESPIRATIONPARAMETERS",
               ID_THORAXOLDHISTOGRAM: "ID_THORAXOLDHISTOGRAM",
               ID_ABDOMENOLDHISTOGRAM: "ID_ABDOMENOLDHISTOGRAM",
               ID_FLOWOLDHISTOGRAM: "ID_FLOWOLDHISTOGRAM",
               ID_THORAXHISTOGRAM: "ID_THORAXHISTOGRAM",
               ID_ABDOMENHISTOGRAM: "ID_ABDOMENHISTOGRAM",
               ID_FLOWHISTOGRAM: "ID_FLOWHISTOGRAM",
               ID_RESPIRATIONRATE: "ID_RESPIRATIONRATE",
               ID_SATURATIONPARAMETERS: "ID_SATURATIONPARAMETERS",
               ID_SATURATIONRATE: "ID_SATURATIONRATE",
               ID_SATURATIONSIGNAL: "ID_SATURATIONSIGNAL",
               ID_EMGPARAMETERS: "ID_EMGPARAMETERS",
               ID_EMGCHINSIGNAL: "ID_EMGCHINSIGNAL",
               ID_EMGTIBIALSIGNAL_01: "ID_EMGTIBIALSIGNAL_01",
               ID_EMGTIBIALSIGNAL_02: "ID_EMGTIBIALSIGNAL_02",
               ID_EMGTIBIALSIGNAL_03: "ID_EMGTIBIALSIGNAL_03",
               ID_EMGTIBIALSIGNAL_04: "ID_EMGTIBIALSIGNAL_04",
               ID_EMGTIBIALSIGNAL_05: "ID_EMGTIBIALSIGNAL_05",
               ID_EMGTIBIALSIGNAL_06: "ID_EMGTIBIALSIGNAL_06",
               ID_EMGTIBIALSIGNAL_07: "ID_EMGTIBIALSIGNAL_07",
               ID_EMGTIBIALSIGNAL_08: "ID_EMGTIBIALSIGNAL_08",
               ID_EMGTIBIALSIGNAL_09: "ID_EMGTIBIALSIGNAL_09",
               ID_EMGTIBIALSIGNAL_10: "ID_EMGTIBIALSIGNAL_10",
               ID_EMGTIBIALSIGNAL_11: "ID_EMGTIBIALSIGNAL_11",
               ID_EMGTIBIALSIGNAL_12: "ID_EMGTIBIALSIGNAL_12",
               ID_EMGTIBIALSIGNAL_13: "ID_EMGTIBIALSIGNAL_13",
               ID_EMGTIBIALSIGNAL_14: "ID_EMGTIBIALSIGNAL_14",
               ID_EMGTIBIALSIGNAL_15: "ID_EMGTIBIALSIGNAL_15",
               ID_EMGTIBIALSIGNAL_16: "ID_EMGTIBIALSIGNAL_16",
               ID_EMGTIBIALSIGNAL_17: "ID_EMGTIBIALSIGNAL_17",
               ID_EMGTIBIALSIGNAL_18: "ID_EMGTIBIALSIGNAL_18",
               ID_EMGTIBIALSIGNAL_19: "ID_EMGTIBIALSIGNAL_19",
               ID_EMGTIBIALSIGNAL_20: "ID_EMGTIBIALSIGNAL_20",
               ID_EMGTIBIALSIGNAL_21: "ID_EMGTIBIALSIGNAL_21",
               ID_EMGTIBIALSIGNAL_22: "ID_EMGTIBIALSIGNAL_22",
               ID_EMGTIBIALSIGNAL_23: "ID_EMGTIBIALSIGNAL_23",
               ID_EMGTIBIALSIGNAL_24: "ID_EMGTIBIALSIGNAL_24",
               ID_EMGTIBIALSIGNAL_25: "ID_EMGTIBIALSIGNAL_25",
               ID_EMGTIBIALSIGNAL_26: "ID_EMGTIBIALSIGNAL_26",
               ID_EMGTIBIALSIGNAL_27: "ID_EMGTIBIALSIGNAL_27",
               ID_EMGTIBIALSIGNAL_28: "ID_EMGTIBIALSIGNAL_28",
               ID_EMGTIBIALSIGNAL_29: "ID_EMGTIBIALSIGNAL_29",
               ID_EMGTIBIALSIGNAL_30: "ID_EMGTIBIALSIGNAL_30",
               ID_EMGTIBIALSIGNAL_31: "ID_EMGTIBIALSIGNAL_31",
               ID_EMGTIBIALSIGNAL_32: "ID_EMGTIBIALSIGNAL_32",
               ID_EEGDELTAPARAMETERS: "ID_EEGDELTAPARAMETERS",
               ID_EEGDELTAHISTOGRAM_01: "ID_EEGDELTAHISTOGRAM_01",
               ID_EEGDELTAHISTOGRAM_02: "ID_EEGDELTAHISTOGRAM_02",
               ID_EEGDELTAHISTOGRAM_03: "ID_EEGDELTAHISTOGRAM_03",
               ID_EEGDELTAHISTOGRAM_04: "ID_EEGDELTAHISTOGRAM_04",
               ID_EEGDELTAHISTOGRAM_05: "ID_EEGDELTAHISTOGRAM_05",
               ID_EEGDELTAHISTOGRAM_06: "ID_EEGDELTAHISTOGRAM_06",
               ID_EEGDELTAHISTOGRAM_07: "ID_EEGDELTAHISTOGRAM_07",
               ID_EEGDELTAHISTOGRAM_08: "ID_EEGDELTAHISTOGRAM_08",
               ID_EEGDELTAHISTOGRAM_09: "ID_EEGDELTAHISTOGRAM_09",
               ID_EEGDELTAHISTOGRAM_10: "ID_EEGDELTAHISTOGRAM_10",
               ID_EEGDELTAHISTOGRAM_11: "ID_EEGDELTAHISTOGRAM_11",
               ID_EEGDELTAHISTOGRAM_12: "ID_EEGDELTAHISTOGRAM_12",
               ID_EEGDELTAHISTOGRAM_13: "ID_EEGDELTAHISTOGRAM_13",
               ID_EEGDELTAHISTOGRAM_14: "ID_EEGDELTAHISTOGRAM_14",
               ID_EEGDELTAHISTOGRAM_15: "ID_EEGDELTAHISTOGRAM_15",
               ID_EEGDELTAHISTOGRAM_16: "ID_EEGDELTAHISTOGRAM_16",
               ID_EEGDELTAHISTOGRAM_17: "ID_EEGDELTAHISTOGRAM_17",
               ID_EEGDELTAHISTOGRAM_18: "ID_EEGDELTAHISTOGRAM_18",
               ID_EEGDELTAHISTOGRAM_19: "ID_EEGDELTAHISTOGRAM_19",
               ID_EEGDELTAHISTOGRAM_20: "ID_EEGDELTAHISTOGRAM_20",
               ID_EEGDELTAHISTOGRAM_21: "ID_EEGDELTAHISTOGRAM_21",
               ID_EEGDELTAHISTOGRAM_22: "ID_EEGDELTAHISTOGRAM_22",
               ID_EEGDELTAHISTOGRAM_23: "ID_EEGDELTAHISTOGRAM_23",
               ID_EEGDELTAHISTOGRAM_24: "ID_EEGDELTAHISTOGRAM_24",
               ID_EEGDELTAHISTOGRAM_25: "ID_EEGDELTAHISTOGRAM_25",
               ID_EEGDELTAHISTOGRAM_26: "ID_EEGDELTAHISTOGRAM_26",
               ID_EEGDELTAHISTOGRAM_27: "ID_EEGDELTAHISTOGRAM_27",
               ID_EEGDELTAHISTOGRAM_28: "ID_EEGDELTAHISTOGRAM_28",
               ID_EEGDELTAHISTOGRAM_29: "ID_EEGDELTAHISTOGRAM_29",
               ID_EEGDELTAHISTOGRAM_30: "ID_EEGDELTAHISTOGRAM_30",
               ID_EEGDELTAHISTOGRAM_31: "ID_EEGDELTAHISTOGRAM_31",
               ID_EEGDELTAHISTOGRAM_32: "ID_EEGDELTAHISTOGRAM_32",
               ID_EEGDELTAPERCENTAGE_01: "ID_EEGDELTAPERCENTAGE_01",
               ID_EEGDELTAPERCENTAGE_02: "ID_EEGDELTAPERCENTAGE_02",
               ID_EEGDELTAPERCENTAGE_03: "ID_EEGDELTAPERCENTAGE_03",
               ID_EEGDELTAPERCENTAGE_04: "ID_EEGDELTAPERCENTAGE_04",
               ID_EEGDELTAPERCENTAGE_05: "ID_EEGDELTAPERCENTAGE_05",
               ID_EEGDELTAPERCENTAGE_06: "ID_EEGDELTAPERCENTAGE_06",
               ID_EEGDELTAPERCENTAGE_07: "ID_EEGDELTAPERCENTAGE_07",
               ID_EEGDELTAPERCENTAGE_08: "ID_EEGDELTAPERCENTAGE_08",
               ID_EEGDELTAPERCENTAGE_09: "ID_EEGDELTAPERCENTAGE_09",
               ID_EEGDELTAPERCENTAGE_10: "ID_EEGDELTAPERCENTAGE_10",
               ID_EEGDELTAPERCENTAGE_11: "ID_EEGDELTAPERCENTAGE_11",
               ID_EEGDELTAPERCENTAGE_12: "ID_EEGDELTAPERCENTAGE_12",
               ID_EEGDELTAPERCENTAGE_13: "ID_EEGDELTAPERCENTAGE_13",
               ID_EEGDELTAPERCENTAGE_14: "ID_EEGDELTAPERCENTAGE_14",
               ID_EEGDELTAPERCENTAGE_15: "ID_EEGDELTAPERCENTAGE_15",
               ID_EEGDELTAPERCENTAGE_16: "ID_EEGDELTAPERCENTAGE_16",
               ID_EEGDELTAPERCENTAGE_17: "ID_EEGDELTAPERCENTAGE_17",
               ID_EEGDELTAPERCENTAGE_18: "ID_EEGDELTAPERCENTAGE_18",
               ID_EEGDELTAPERCENTAGE_19: "ID_EEGDELTAPERCENTAGE_19",
               ID_EEGDELTAPERCENTAGE_20: "ID_EEGDELTAPERCENTAGE_20",
               ID_EEGDELTAPERCENTAGE_21: "ID_EEGDELTAPERCENTAGE_21",
               ID_EEGDELTAPERCENTAGE_22: "ID_EEGDELTAPERCENTAGE_22",
               ID_EEGDELTAPERCENTAGE_23: "ID_EEGDELTAPERCENTAGE_23",
               ID_EEGDELTAPERCENTAGE_24: "ID_EEGDELTAPERCENTAGE_24",
               ID_EEGDELTAPERCENTAGE_25: "ID_EEGDELTAPERCENTAGE_25",
               ID_EEGDELTAPERCENTAGE_26: "ID_EEGDELTAPERCENTAGE_26",
               ID_EEGDELTAPERCENTAGE_27: "ID_EEGDELTAPERCENTAGE_27",
               ID_EEGDELTAPERCENTAGE_28: "ID_EEGDELTAPERCENTAGE_28",
               ID_EEGDELTAPERCENTAGE_29: "ID_EEGDELTAPERCENTAGE_29",
               ID_EEGDELTAPERCENTAGE_30: "ID_EEGDELTAPERCENTAGE_30",
               ID_EEGDELTAPERCENTAGE_31: "ID_EEGDELTAPERCENTAGE_31",
               ID_EEGDELTAPERCENTAGE_32: "ID_EEGDELTAPERCENTAGE_32",
               ID_EEGDELTACOUNT_01: "ID_EEGDELTACOUNT_01",
               ID_EEGDELTACOUNT_02: "ID_EEGDELTACOUNT_02",
               ID_EEGDELTACOUNT_03: "ID_EEGDELTACOUNT_03",
               ID_EEGDELTACOUNT_04: "ID_EEGDELTACOUNT_04",
               ID_EEGDELTACOUNT_05: "ID_EEGDELTACOUNT_05",
               ID_EEGDELTACOUNT_06: "ID_EEGDELTACOUNT_06",
               ID_EEGDELTACOUNT_07: "ID_EEGDELTACOUNT_07",
               ID_EEGDELTACOUNT_08: "ID_EEGDELTACOUNT_08",
               ID_EEGDELTACOUNT_09: "ID_EEGDELTACOUNT_09",
               ID_EEGDELTACOUNT_10: "ID_EEGDELTACOUNT_10",
               ID_EEGDELTACOUNT_11: "ID_EEGDELTACOUNT_11",
               ID_EEGDELTACOUNT_12: "ID_EEGDELTACOUNT_12",
               ID_EEGDELTACOUNT_13: "ID_EEGDELTACOUNT_13",
               ID_EEGDELTACOUNT_14: "ID_EEGDELTACOUNT_14",
               ID_EEGDELTACOUNT_15: "ID_EEGDELTACOUNT_15",
               ID_EEGDELTACOUNT_16: "ID_EEGDELTACOUNT_16",
               ID_EEGDELTACOUNT_17: "ID_EEGDELTACOUNT_17",
               ID_EEGDELTACOUNT_18: "ID_EEGDELTACOUNT_18",
               ID_EEGDELTACOUNT_19: "ID_EEGDELTACOUNT_19",
               ID_EEGDELTACOUNT_20: "ID_EEGDELTACOUNT_20",
               ID_EEGDELTACOUNT_21: "ID_EEGDELTACOUNT_21",
               ID_EEGDELTACOUNT_22: "ID_EEGDELTACOUNT_22",
               ID_EEGDELTACOUNT_23: "ID_EEGDELTACOUNT_23",
               ID_EEGDELTACOUNT_24: "ID_EEGDELTACOUNT_24",
               ID_EEGDELTACOUNT_25: "ID_EEGDELTACOUNT_25",
               ID_EEGDELTACOUNT_26: "ID_EEGDELTACOUNT_26",
               ID_EEGDELTACOUNT_27: "ID_EEGDELTACOUNT_27",
               ID_EEGDELTACOUNT_28: "ID_EEGDELTACOUNT_28",
               ID_EEGDELTACOUNT_29: "ID_EEGDELTACOUNT_29",
               ID_EEGDELTACOUNT_30: "ID_EEGDELTACOUNT_30",
               ID_EEGDELTACOUNT_31: "ID_EEGDELTACOUNT_31",
               ID_EEGDELTACOUNT_32: "ID_EEGDELTACOUNT_32",
               ID_EEGSPINDLEPARAMETERS: "ID_EEGSPINDLEPARAMETERS",
               ID_EEGSPINDLEHISTOGRAM_01: "ID_EEGSPINDLEHISTOGRAM_01",
               ID_EEGSPINDLEHISTOGRAM_02: "ID_EEGSPINDLEHISTOGRAM_02",
               ID_EEGSPINDLEHISTOGRAM_03: "ID_EEGSPINDLEHISTOGRAM_03",
               ID_EEGSPINDLEHISTOGRAM_04: "ID_EEGSPINDLEHISTOGRAM_04",
               ID_EEGSPINDLEHISTOGRAM_05: "ID_EEGSPINDLEHISTOGRAM_05",
               ID_EEGSPINDLEHISTOGRAM_06: "ID_EEGSPINDLEHISTOGRAM_06",
               ID_EEGSPINDLEHISTOGRAM_07: "ID_EEGSPINDLEHISTOGRAM_07",
               ID_EEGSPINDLEHISTOGRAM_08: "ID_EEGSPINDLEHISTOGRAM_08",
               ID_EEGSPINDLEHISTOGRAM_09: "ID_EEGSPINDLEHISTOGRAM_09",
               ID_EEGSPINDLEHISTOGRAM_10: "ID_EEGSPINDLEHISTOGRAM_10",
               ID_EEGSPINDLEHISTOGRAM_11: "ID_EEGSPINDLEHISTOGRAM_11",
               ID_EEGSPINDLEHISTOGRAM_12: "ID_EEGSPINDLEHISTOGRAM_12",
               ID_EEGSPINDLEHISTOGRAM_13: "ID_EEGSPINDLEHISTOGRAM_13",
               ID_EEGSPINDLEHISTOGRAM_14: "ID_EEGSPINDLEHISTOGRAM_14",
               ID_EEGSPINDLEHISTOGRAM_15: "ID_EEGSPINDLEHISTOGRAM_15",
               ID_EEGSPINDLEHISTOGRAM_16: "ID_EEGSPINDLEHISTOGRAM_16",
               ID_EEGSPINDLEHISTOGRAM_17: "ID_EEGSPINDLEHISTOGRAM_17",
               ID_EEGSPINDLEHISTOGRAM_18: "ID_EEGSPINDLEHISTOGRAM_18",
               ID_EEGSPINDLEHISTOGRAM_19: "ID_EEGSPINDLEHISTOGRAM_19",
               ID_EEGSPINDLEHISTOGRAM_20: "ID_EEGSPINDLEHISTOGRAM_20",
               ID_EEGSPINDLEHISTOGRAM_21: "ID_EEGSPINDLEHISTOGRAM_21",
               ID_EEGSPINDLEHISTOGRAM_22: "ID_EEGSPINDLEHISTOGRAM_22",
               ID_EEGSPINDLEHISTOGRAM_23: "ID_EEGSPINDLEHISTOGRAM_23",
               ID_EEGSPINDLEHISTOGRAM_24: "ID_EEGSPINDLEHISTOGRAM_24",
               ID_EEGSPINDLEHISTOGRAM_25: "ID_EEGSPINDLEHISTOGRAM_25",
               ID_EEGSPINDLEHISTOGRAM_26: "ID_EEGSPINDLEHISTOGRAM_26",
               ID_EEGSPINDLEHISTOGRAM_27: "ID_EEGSPINDLEHISTOGRAM_27",
               ID_EEGSPINDLEHISTOGRAM_28: "ID_EEGSPINDLEHISTOGRAM_28",
               ID_EEGSPINDLEHISTOGRAM_29: "ID_EEGSPINDLEHISTOGRAM_29",
               ID_EEGSPINDLEHISTOGRAM_30: "ID_EEGSPINDLEHISTOGRAM_30",
               ID_EEGSPINDLEHISTOGRAM_31: "ID_EEGSPINDLEHISTOGRAM_31",
               ID_EEGSPINDLEHISTOGRAM_32: "ID_EEGSPINDLEHISTOGRAM_32",
               ID_EEGALPHAOLDPARAMETERS: "ID_EEGALPHAOLDPARAMETERS",
               ID_EEGALPHASIGNAL_01: "ID_EEGALPHASIGNAL_01",
               ID_EEGALPHASIGNAL_02: "ID_EEGALPHASIGNAL_02",
               ID_EEGALPHASIGNAL_03: "ID_EEGALPHASIGNAL_03",
               ID_EEGALPHASIGNAL_04: "ID_EEGALPHASIGNAL_04",
               ID_EEGALPHASIGNAL_05: "ID_EEGALPHASIGNAL_05",
               ID_EEGALPHASIGNAL_06: "ID_EEGALPHASIGNAL_06",
               ID_EEGALPHASIGNAL_07: "ID_EEGALPHASIGNAL_07",
               ID_EEGALPHASIGNAL_08: "ID_EEGALPHASIGNAL_08",
               ID_EEGALPHASIGNAL_09: "ID_EEGALPHASIGNAL_09",
               ID_EEGALPHASIGNAL_10: "ID_EEGALPHASIGNAL_10",
               ID_EEGALPHASIGNAL_11: "ID_EEGALPHASIGNAL_11",
               ID_EEGALPHASIGNAL_12: "ID_EEGALPHASIGNAL_12",
               ID_EEGALPHASIGNAL_13: "ID_EEGALPHASIGNAL_13",
               ID_EEGALPHASIGNAL_14: "ID_EEGALPHASIGNAL_14",
               ID_EEGALPHASIGNAL_15: "ID_EEGALPHASIGNAL_15",
               ID_EEGALPHASIGNAL_16: "ID_EEGALPHASIGNAL_16",
               ID_EEGALPHASIGNAL_17: "ID_EEGALPHASIGNAL_17",
               ID_EEGALPHASIGNAL_18: "ID_EEGALPHASIGNAL_18",
               ID_EEGALPHASIGNAL_19: "ID_EEGALPHASIGNAL_19",
               ID_EEGALPHASIGNAL_20: "ID_EEGALPHASIGNAL_20",
               ID_EEGALPHASIGNAL_21: "ID_EEGALPHASIGNAL_21",
               ID_EEGALPHASIGNAL_22: "ID_EEGALPHASIGNAL_22",
               ID_EEGALPHASIGNAL_23: "ID_EEGALPHASIGNAL_23",
               ID_EEGALPHASIGNAL_24: "ID_EEGALPHASIGNAL_24",
               ID_EEGALPHASIGNAL_25: "ID_EEGALPHASIGNAL_25",
               ID_EEGALPHASIGNAL_26: "ID_EEGALPHASIGNAL_26",
               ID_EEGALPHASIGNAL_27: "ID_EEGALPHASIGNAL_27",
               ID_EEGALPHASIGNAL_28: "ID_EEGALPHASIGNAL_28",
               ID_EEGALPHASIGNAL_29: "ID_EEGALPHASIGNAL_29",
               ID_EEGALPHASIGNAL_30: "ID_EEGALPHASIGNAL_30",
               ID_EEGALPHASIGNAL_31: "ID_EEGALPHASIGNAL_31",
               ID_EEGALPHASIGNAL_32: "ID_EEGALPHASIGNAL_32",
               ID_EEGALPHAPARAMETERS: "ID_EEGALPHAPARAMETERS",
               ID_EEGALPHAHISTOGRAM_01: "ID_EEGALPHAHISTOGRAM_01",
               ID_EEGALPHAHISTOGRAM_02: "ID_EEGALPHAHISTOGRAM_02",
               ID_EEGALPHAHISTOGRAM_03: "ID_EEGALPHAHISTOGRAM_03",
               ID_EEGALPHAHISTOGRAM_04: "ID_EEGALPHAHISTOGRAM_04",
               ID_EEGALPHAHISTOGRAM_05: "ID_EEGALPHAHISTOGRAM_05",
               ID_EEGALPHAHISTOGRAM_06: "ID_EEGALPHAHISTOGRAM_06",
               ID_EEGALPHAHISTOGRAM_07: "ID_EEGALPHAHISTOGRAM_07",
               ID_EEGALPHAHISTOGRAM_08: "ID_EEGALPHAHISTOGRAM_08",
               ID_EEGALPHAHISTOGRAM_09: "ID_EEGALPHAHISTOGRAM_09",
               ID_EEGALPHAHISTOGRAM_10: "ID_EEGALPHAHISTOGRAM_10",
               ID_EEGALPHAHISTOGRAM_11: "ID_EEGALPHAHISTOGRAM_11",
               ID_EEGALPHAHISTOGRAM_12: "ID_EEGALPHAHISTOGRAM_12",
               ID_EEGALPHAHISTOGRAM_13: "ID_EEGALPHAHISTOGRAM_13",
               ID_EEGALPHAHISTOGRAM_14: "ID_EEGALPHAHISTOGRAM_14",
               ID_EEGALPHAHISTOGRAM_15: "ID_EEGALPHAHISTOGRAM_15",
               ID_EEGALPHAHISTOGRAM_16: "ID_EEGALPHAHISTOGRAM_16",
               ID_EEGALPHAHISTOGRAM_17: "ID_EEGALPHAHISTOGRAM_17",
               ID_EEGALPHAHISTOGRAM_18: "ID_EEGALPHAHISTOGRAM_18",
               ID_EEGALPHAHISTOGRAM_19: "ID_EEGALPHAHISTOGRAM_19",
               ID_EEGALPHAHISTOGRAM_20: "ID_EEGALPHAHISTOGRAM_20",
               ID_EEGALPHAHISTOGRAM_21: "ID_EEGALPHAHISTOGRAM_21",
               ID_EEGALPHAHISTOGRAM_22: "ID_EEGALPHAHISTOGRAM_22",
               ID_EEGALPHAHISTOGRAM_23: "ID_EEGALPHAHISTOGRAM_23",
               ID_EEGALPHAHISTOGRAM_24: "ID_EEGALPHAHISTOGRAM_24",
               ID_EEGALPHAHISTOGRAM_25: "ID_EEGALPHAHISTOGRAM_25",
               ID_EEGALPHAHISTOGRAM_26: "ID_EEGALPHAHISTOGRAM_26",
               ID_EEGALPHAHISTOGRAM_27: "ID_EEGALPHAHISTOGRAM_27",
               ID_EEGALPHAHISTOGRAM_28: "ID_EEGALPHAHISTOGRAM_28",
               ID_EEGALPHAHISTOGRAM_29: "ID_EEGALPHAHISTOGRAM_29",
               ID_EEGALPHAHISTOGRAM_30: "ID_EEGALPHAHISTOGRAM_30",
               ID_EEGALPHAHISTOGRAM_31: "ID_EEGALPHAHISTOGRAM_31",
               ID_EEGALPHAHISTOGRAM_32: "ID_EEGALPHAHISTOGRAM_32",
               ID_EEGALPHAPERCENTAGE_01: "ID_EEGALPHAPERCENTAGE_01",
               ID_EEGALPHAPERCENTAGE_02: "ID_EEGALPHAPERCENTAGE_02",
               ID_EEGALPHAPERCENTAGE_03: "ID_EEGALPHAPERCENTAGE_03",
               ID_EEGALPHAPERCENTAGE_04: "ID_EEGALPHAPERCENTAGE_04",
               ID_EEGALPHAPERCENTAGE_05: "ID_EEGALPHAPERCENTAGE_05",
               ID_EEGALPHAPERCENTAGE_06: "ID_EEGALPHAPERCENTAGE_06",
               ID_EEGALPHAPERCENTAGE_07: "ID_EEGALPHAPERCENTAGE_07",
               ID_EEGALPHAPERCENTAGE_08: "ID_EEGALPHAPERCENTAGE_08",
               ID_EEGALPHAPERCENTAGE_09: "ID_EEGALPHAPERCENTAGE_09",
               ID_EEGALPHAPERCENTAGE_10: "ID_EEGALPHAPERCENTAGE_10",
               ID_EEGALPHAPERCENTAGE_11: "ID_EEGALPHAPERCENTAGE_11",
               ID_EEGALPHAPERCENTAGE_12: "ID_EEGALPHAPERCENTAGE_12",
               ID_EEGALPHAPERCENTAGE_13: "ID_EEGALPHAPERCENTAGE_13",
               ID_EEGALPHAPERCENTAGE_14: "ID_EEGALPHAPERCENTAGE_14",
               ID_EEGALPHAPERCENTAGE_15: "ID_EEGALPHAPERCENTAGE_15",
               ID_EEGALPHAPERCENTAGE_16: "ID_EEGALPHAPERCENTAGE_16",
               ID_EEGALPHAPERCENTAGE_17: "ID_EEGALPHAPERCENTAGE_17",
               ID_EEGALPHAPERCENTAGE_18: "ID_EEGALPHAPERCENTAGE_18",
               ID_EEGALPHAPERCENTAGE_19: "ID_EEGALPHAPERCENTAGE_19",
               ID_EEGALPHAPERCENTAGE_20: "ID_EEGALPHAPERCENTAGE_20",
               ID_EEGALPHAPERCENTAGE_21: "ID_EEGALPHAPERCENTAGE_21",
               ID_EEGALPHAPERCENTAGE_22: "ID_EEGALPHAPERCENTAGE_22",
               ID_EEGALPHAPERCENTAGE_23: "ID_EEGALPHAPERCENTAGE_23",
               ID_EEGALPHAPERCENTAGE_24: "ID_EEGALPHAPERCENTAGE_24",
               ID_EEGALPHAPERCENTAGE_25: "ID_EEGALPHAPERCENTAGE_25",
               ID_EEGALPHAPERCENTAGE_26: "ID_EEGALPHAPERCENTAGE_26",
               ID_EEGALPHAPERCENTAGE_27: "ID_EEGALPHAPERCENTAGE_27",
               ID_EEGALPHAPERCENTAGE_28: "ID_EEGALPHAPERCENTAGE_28",
               ID_EEGALPHAPERCENTAGE_29: "ID_EEGALPHAPERCENTAGE_29",
               ID_EEGALPHAPERCENTAGE_30: "ID_EEGALPHAPERCENTAGE_30",
               ID_EEGALPHAPERCENTAGE_31: "ID_EEGALPHAPERCENTAGE_31",
               ID_EEGALPHAPERCENTAGE_32: "ID_EEGALPHAPERCENTAGE_32",
               ID_EOGPARAMETERS: "ID_EOGPARAMETERS",
               ID_EOGREMHISTOGRAM_01: "ID_EOGREMHISTOGRAM_01",
               ID_EOGREMHISTOGRAM_02: "ID_EOGREMHISTOGRAM_02",
               ID_EOGREMCOUNT_01: "ID_EOGREMCOUNT_01",
               ID_EOGREMCOUNT_02: "ID_EOGREMCOUNT_02",
               ID_EOGSEMHISTOGRAM: "ID_EOGSEMHISTOGRAM",
               ID_EOGSEMCOUNT: "ID_EOGSEMCOUNT",
               ID_EOGBLINKCOUNT_01: "ID_EOGBLINKCOUNT_01",
               ID_EOGBLINKCOUNT_02: "ID_EOGBLINKCOUNT_02",
               ID_EEGTHETAPARAMETERS: "ID_EEGTHETAPARAMETERS",
               ID_EEGTHETASIGNAL_01: "ID_EEGTHETASIGNAL_01",
               ID_EEGTHETASIGNAL_02: "ID_EEGTHETASIGNAL_02",
               ID_EEGTHETASIGNAL_03: "ID_EEGTHETASIGNAL_03",
               ID_EEGTHETASIGNAL_04: "ID_EEGTHETASIGNAL_04",
               ID_EEGTHETASIGNAL_05: "ID_EEGTHETASIGNAL_05",
               ID_EEGTHETASIGNAL_06: "ID_EEGTHETASIGNAL_06",
               ID_EEGTHETASIGNAL_07: "ID_EEGTHETASIGNAL_07",
               ID_EEGTHETASIGNAL_08: "ID_EEGTHETASIGNAL_08",
               ID_EEGTHETASIGNAL_09: "ID_EEGTHETASIGNAL_09",
               ID_EEGTHETASIGNAL_10: "ID_EEGTHETASIGNAL_10",
               ID_EEGTHETASIGNAL_11: "ID_EEGTHETASIGNAL_11",
               ID_EEGTHETASIGNAL_12: "ID_EEGTHETASIGNAL_12",
               ID_EEGTHETASIGNAL_13: "ID_EEGTHETASIGNAL_13",
               ID_EEGTHETASIGNAL_14: "ID_EEGTHETASIGNAL_14",
               ID_EEGTHETASIGNAL_15: "ID_EEGTHETASIGNAL_15",
               ID_EEGTHETASIGNAL_16: "ID_EEGTHETASIGNAL_16",
               ID_EEGTHETASIGNAL_17: "ID_EEGTHETASIGNAL_17",
               ID_EEGTHETASIGNAL_18: "ID_EEGTHETASIGNAL_18",
               ID_EEGTHETASIGNAL_19: "ID_EEGTHETASIGNAL_19",
               ID_EEGTHETASIGNAL_20: "ID_EEGTHETASIGNAL_20",
               ID_EEGTHETASIGNAL_21: "ID_EEGTHETASIGNAL_21",
               ID_EEGTHETASIGNAL_22: "ID_EEGTHETASIGNAL_22",
               ID_EEGTHETASIGNAL_23: "ID_EEGTHETASIGNAL_23",
               ID_EEGTHETASIGNAL_24: "ID_EEGTHETASIGNAL_24",
               ID_EEGTHETASIGNAL_25: "ID_EEGTHETASIGNAL_25",
               ID_EEGTHETASIGNAL_26: "ID_EEGTHETASIGNAL_26",
               ID_EEGTHETASIGNAL_27: "ID_EEGTHETASIGNAL_27",
               ID_EEGTHETASIGNAL_28: "ID_EEGTHETASIGNAL_28",
               ID_EEGTHETASIGNAL_29: "ID_EEGTHETASIGNAL_29",
               ID_EEGTHETASIGNAL_30: "ID_EEGTHETASIGNAL_30",
               ID_EEGTHETASIGNAL_31: "ID_EEGTHETASIGNAL_31",
               ID_EEGTHETASIGNAL_32: "ID_EEGTHETASIGNAL_32",
               ID_EEGBETAPARAMETERS: "ID_EEGBETAPARAMETERS",
               ID_EEGBETASIGNAL_01: "ID_EEGBETASIGNAL_01",
               ID_EEGBETASIGNAL_02: "ID_EEGBETASIGNAL_02",
               ID_EEGBETASIGNAL_03: "ID_EEGBETASIGNAL_03",
               ID_EEGBETASIGNAL_04: "ID_EEGBETASIGNAL_04",
               ID_EEGBETASIGNAL_05: "ID_EEGBETASIGNAL_05",
               ID_EEGBETASIGNAL_06: "ID_EEGBETASIGNAL_06",
               ID_EEGBETASIGNAL_07: "ID_EEGBETASIGNAL_07",
               ID_EEGBETASIGNAL_08: "ID_EEGBETASIGNAL_08",
               ID_EEGBETASIGNAL_09: "ID_EEGBETASIGNAL_09",
               ID_EEGBETASIGNAL_10: "ID_EEGBETASIGNAL_10",
               ID_EEGBETASIGNAL_11: "ID_EEGBETASIGNAL_11",
               ID_EEGBETASIGNAL_12: "ID_EEGBETASIGNAL_12",
               ID_EEGBETASIGNAL_13: "ID_EEGBETASIGNAL_13",
               ID_EEGBETASIGNAL_14: "ID_EEGBETASIGNAL_14",
               ID_EEGBETASIGNAL_15: "ID_EEGBETASIGNAL_15",
               ID_EEGBETASIGNAL_16: "ID_EEGBETASIGNAL_16",
               ID_EEGBETASIGNAL_17: "ID_EEGBETASIGNAL_17",
               ID_EEGBETASIGNAL_18: "ID_EEGBETASIGNAL_18",
               ID_EEGBETASIGNAL_19: "ID_EEGBETASIGNAL_19",
               ID_EEGBETASIGNAL_20: "ID_EEGBETASIGNAL_20",
               ID_EEGBETASIGNAL_21: "ID_EEGBETASIGNAL_21",
               ID_EEGBETASIGNAL_22: "ID_EEGBETASIGNAL_22",
               ID_EEGBETASIGNAL_23: "ID_EEGBETASIGNAL_23",
               ID_EEGBETASIGNAL_24: "ID_EEGBETASIGNAL_24",
               ID_EEGBETASIGNAL_25: "ID_EEGBETASIGNAL_25",
               ID_EEGBETASIGNAL_26: "ID_EEGBETASIGNAL_26",
               ID_EEGBETASIGNAL_27: "ID_EEGBETASIGNAL_27",
               ID_EEGBETASIGNAL_28: "ID_EEGBETASIGNAL_28",
               ID_EEGBETASIGNAL_29: "ID_EEGBETASIGNAL_29",
               ID_EEGBETASIGNAL_30: "ID_EEGBETASIGNAL_30",
               ID_EEGBETASIGNAL_31: "ID_EEGBETASIGNAL_31",
               ID_EEGBETASIGNAL_32: "ID_EEGBETASIGNAL_32",
               ID_BODYPOSPARAMETERS: "ID_BODYPOSPARAMETERS",
               ID_SOUNDPARAMETERS: "ID_SOUNDPARAMETERS",
               ID_SOUND: "ID_SOUND",
               ID_CPAPPRESSUREPARAMETERS: "ID_CPAPPRESSUREPARAMETERS",
               ID_CPAPPRESSUREVALUES: "ID_CPAPPRESSUREVALUES"}

    def __init__(self, item_id=0, offset=0, size=0):
        self.item_id = item_id
        self.offset = offset
        self.size = size


def read_file_inventory(sf):
    sf.seek(10)
    inventory = []
    append = inventory.append
    inv_struct = struct.Struct("<hlL")
    for i in range(1, 129):
        ib = inv_struct.unpack(sf.read(inv_struct.size))
        append(InventoryItem(ib[0], ib[1], ib[2]))
    return inventory


class StageType:
    def __init__(self, desc="", label="", value=0, value_type=0):
        self.desc = desc
        self.label = label
        self.value = value
        self.value_type = value_type


def decode_stage_type(val, stage_defs):
    if val in stage_defs:
        return stage_defs[val]
    return StageType("INVALID", "INVALID", 0, 0)


def read_stage_types(sf):
    types = {}
    ssize = 12
    int16 = struct.Struct("<h")
    tcount = int16.unpack(sf.read(int16.size))[0]

    ds = "".join(repeat("20s", ssize))
    ls = "".join(repeat("6s", ssize))
    vs = "<%dh" % ssize

    dstruct = struct.Struct(ds)
    descs = dstruct.unpack(sf.read(dstruct.size))
    lstruct = struct.Struct(ls)
    labels = lstruct.unpack(sf.read(lstruct.size))
    vstruct = struct.Struct(vs)
    values = vstruct.unpack(sf.read(vstruct.size))
    for i in range(tcount):
        valbytes = values[i].to_bytes(2, byteorder='big')
        val = valbytes[1]
        valtype = valbytes[0]
        types[val] = StageType(string_trim_to_0(descs[i]), string_trim_to_0(labels[i]), val, valtype)
    return types


class Stage:
    def __init__(self, no, time, val, label, val_type):
        self.no = no
        self.time = time
        self.val = val
        self.label = label
        self.val_type = val_type


def get_wake_values(stage_defs):
    return [x.value for x in stage_defs.values() if (x.value_type == 1)]


def get_sleep_values(stage_defs):
    return [x.value for x in stage_defs.values() if (x.value_type in [2, 3])]


def get_rem_values(stage_defs):
    return [x.value for x in stage_defs.values() if (x.value_type == 2)]


def get_non_rem_values(stage_defs):
    return [x.value for x in stage_defs.values() if (x.value_type == 3)]


def read_stages(sf, offset, size):
    sf.seek(offset)
    int16 = struct.Struct("<h")
    tcount = int16.unpack(sf.read(int16.size))[0]
    currsize = int16.size + tcount
    if currsize > size:
        pass
    stgs = sf.read(tcount)
    return stgs


LBL_DICT = {"INVALID": "INVALID", "Wake": "W", "MT": "MT", "S 1": "N1", "S 2": "N2", "S 3": "N3", "S 4": "N4",
            "REM": "R"}


def transform_stages(stgs, stage_defs, recording_events):
    stages = []
    append = stages.append
    j = 0
    for i in stgs:
        j += 1
        stgdef = decode_stage_type(i, stage_defs)
        recording_event = find_recording_event(j, recording_events)
        if recording_event is not None:
            tm = add_seconds_to_time(recording_event.start_time, (j - recording_event.start_page) * 30)
            append(Stage(j, tm, i, LBL_DICT[stgdef.label], stgdef.value_type))
    return stages


def find_page_in_stages(page, stages):
    return next((x for x in stages if (x.no == page)), None)


####### EDF ###########

_DEFAULT_DATE_FORMAT = "%d.%m.%y"
_DEFAULT_TIME_FORMAT = "%H.%M.%S"


def _encode_date(dtstr):
    return datetime.strptime(dtstr, _DEFAULT_DATE_FORMAT).date()


def _encode_time(tmstr):
    return datetime.strptime(tmstr, _DEFAULT_TIME_FORMAT).time()


def _string_trim0(s):
    ns = "".join([x if 32 <= ord(x) <= 126 else '' for x in s])
    return ns


StructDesc = namedtuple('StructDesc', 'fname ln type encoding input_f output_f')


def _prepare_float_string(sd, f):
    int_f = int(f)
    len_int_f = len(str(int_f))
    decimals = sd.ln - 1 - len_int_f
    return ('{' + ':<{}.{}f'.format(sd.ln, decimals) + '}').format(f).encode(sd.encoding)


def _prepare_int_string(sd, d):
    return ('{' + ':<{}d'.format(sd.ln) + '}').format(d).encode(sd.encoding)


def _prepare_time_string(sd, tm):
    return ('{' + ':<{}'.format(sd.ln) + '}').format(tm.strftime(_DEFAULT_TIME_FORMAT)[:sd.ln]).encode(sd.encoding)


def _prepare_date_string(sd, dt):
    return ('{' + ':<{}'.format(sd.ln) + '}').format(dt.strftime(_DEFAULT_DATE_FORMAT)[:sd.ln]).encode(sd.encoding)


def _prepare_string(sd, st):
    return ('{' + ':<{}'.format(sd.ln) + '}').format(st.strip()[:sd.ln]).encode(sd.encoding)


_HEADER_STRUCTURE = [StructDesc('version', 8, 's', 'ASCII', _string_trim0, _prepare_string),
                     StructDesc('patient_id', 80, 's', 'LATIN2', _string_trim0, _prepare_string),
                     StructDesc('record_id', 80, 's', 'LATIN2', _string_trim0, _prepare_string),
                     StructDesc('start_date', 8, 's', 'ASCII', _encode_date, _prepare_date_string),
                     StructDesc('start_time', 8, 's', 'ASCII', _encode_time, _prepare_time_string),
                     StructDesc('bytes_in_header', 8, 's', 'ASCII', int, _prepare_int_string),
                     StructDesc('reserved', 44, 's', 'ASCII', _string_trim0, _prepare_string),
                     StructDesc('records_in_file', 8, 's', 'ASCII', int, _prepare_int_string),
                     StructDesc('record_duration', 8, 's', 'ASCII', int, _prepare_int_string),
                     StructDesc('signals_in_file', 4, 's', 'ASCII', int, _prepare_int_string)]

_HEADER_FIELD_NAMES = ['version', 'patient_id', 'record_id', 'start_date', 'start_time', 'bytes_in_header',
                       'reserved', 'records_in_file', 'record_duration', 'signals_in_file', 'signal_defs']

_HEADER_SD_STRUCTURE = [StructDesc('label', 16, 's', 'ASCII', _string_trim0, _prepare_string),
                        StructDesc('transducer', 80, 's', 'ASCII', _string_trim0, _prepare_string),
                        StructDesc('dimension', 8, 's', 'ASCII', _string_trim0, _prepare_string),
                        StructDesc('phys_min', 8, 's', 'ASCII', float, _prepare_float_string),
                        StructDesc('phys_max', 8, 's', 'ASCII', float, _prepare_float_string),
                        StructDesc('dig_min', 8, 's', 'ASCII', int, _prepare_int_string),
                        StructDesc('dig_max', 8, 's', 'ASCII', int, _prepare_int_string),
                        StructDesc('filter', 80, 's', 'ASCII', _string_trim0, _prepare_string),
                        StructDesc('samples', 8, 's', 'ASCII', int, _prepare_int_string),
                        StructDesc('reserved', 32, 's', 'ASCII', _string_trim0, _prepare_string)]

_SD_FIELD_NAMES = [x.fname for x in _HEADER_SD_STRUCTURE]

SignalDefinition = namedtuple('SignalDefinition', _SD_FIELD_NAMES)

SignalReadInfo = namedtuple('SignalReadInfo', ['index', 'index_in_file', 'start_position', 'struct_def', 'samples'])


def _extract_field(sf, hds):
    hs = struct.Struct(str(hds.ln) + hds.type)
    hb = hs.unpack(sf.read(hs.size))
    try:
        s = hb[0].decode(hds.encoding).strip()
    except:
        print("Erorr in field {} decoding (probably wrong {} character): {}".format(hds.fname, hds.encoding, hb[0]))
        s = hds.fname
    if hds[3] is not None:
        try:
            value = hds.input_f.__call__(s)
        except:
            print("Erorr in processing field {}: {}".format(hds.fname, hb[0]))
            value = None
    else:
        value = s
    return value


def _extract_composed_field(sf, hds, ln):
    hs = struct.Struct(ln * (str(hds.ln) + hds.type))
    hb = hs.unpack(sf.read(hs.size))
    try:
        s = [x.decode(hds.encoding).strip() for x in hb]
    except:
        print("Erorr in field {} decoding : {}".format(hds.fname, hds.encoding))
        s = ln * (hds.fname if hds.input_f is None else '0')
    if hds.input_f is not None:
        try:
            values = [hds.input_f.__call__(x) for x in s]
        except:
            print("Erorr in processing field {}".format(hds.fname))
            values = None
    else:
        values = s
    return values


class Header(namedtuple('Header', _HEADER_FIELD_NAMES)):
    def duration(self):
        return self.records_in_file * self.record_duration

    def to_bytes(self):
        sdict = {x.fname: [] for x in _HEADER_SD_STRUCTURE}
        for s in self.signal_defs:
            sd = s._asdict()
            for sg in _HEADER_SD_STRUCTURE:
                ss = struct.Struct(str(sg.ln) + sg.type)
                sdict[sg.fname].append(ss.pack(sg.output_f.__call__(sg, sd[sg.fname])))

        sb = b''.join([x for x in [b''.join(sdict[y.fname]) for y in _HEADER_SD_STRUCTURE]])
        header_len = 256 + len(sb)
        hs = struct.Struct(''.join([str(x.ln) + x.type for x in _HEADER_STRUCTURE]))
        hdict = self._asdict()
        if hdict['bytes_in_header'] != header_len:
            hdict['bytes_in_header'] = header_len
        hb = hs.pack(*[x.output_f.__call__(x, hdict[x.fname]) for x in _HEADER_STRUCTURE])
        return b''.join([hb, sb])

    def find_signal_index(self, signal_label):
        labels = [x.label for x in self.signal_defs]
        return labels.index(signal_label) if signal_label in labels else None


def create_header_from_stream(sf):
    dheader = {}
    for hds in _HEADER_STRUCTURE:
        value = _extract_field(sf, hds)
        dheader[hds[0]] = value

    signals_in_file = dheader['signals_in_file']
    dsignals = {}
    for hds in _HEADER_SD_STRUCTURE:
        values = _extract_composed_field(sf, hds, signals_in_file)
        dsignals[hds[0]] = values

    signal_defs = [SignalDefinition(**{x[0]: dsignals[x[0]][i] for x in _HEADER_SD_STRUCTURE}) for i in
                   range(0, signals_in_file)]
    dheader['signal_defs'] = signal_defs
    return Header(**dheader)


def create_header_from_file(file_name):
    with open(file_name, mode='rb') as ifile:
        instance = create_header_from_stream(ifile)
    return instance


class EdfFile(object):
    def __init__(self, header, integers=False):
        self.filename = None
        self._integers = integers
        self._data_start = 0
        self._nrecords = 0
        self._signal_infos = []
        self._record_size = 0
        self.header = header

    def _prepare_to_read(self, sf, signals_to_read):
        sf.seek(0, 2)
        file_size = sf.tell()
        self._data_start = 256 + 256 * self.header.signals_in_file
        self._record_size = sum([x.samples for x in self.header.signal_defs]) * 2
        estimated_records = (file_size - self._data_start) / self._record_size
        self._nrecords = self.header.records_in_file if self.header.records_in_file != -1 else estimated_records
        if estimated_records < self._nrecords:
            print("Estimated records number (%d) lower than stored records (%d)" % (estimated_records, self._nrecords))
            print("Assuming %d" % estimated_records)
            self._nrecords = estimated_records
        before = 0
        orig_start_positions = []
        for s in self.header.signal_defs:
            orig_start_positions.append(before)
            before += s.samples * 2
        sigs = [x for x in (signals_to_read if signals_to_read is not None else range(0, self.header.signals_in_file))]
        for i, s in enumerate(sigs):
            st = struct.Struct("%dh" % self.header.signal_defs[s].samples)
            self._signal_infos.append(
                SignalReadInfo(i, s, orig_start_positions[s], st, self.header.signal_defs[s].samples))

    @staticmethod
    def _read_signal_record(sf, s, record_start):
        sf.seek(record_start + s.start_position)
        ssize = s.struct_def.size
        rbytes = sf.read(ssize)
        rbytes_len = len(rbytes)
        if rbytes_len < ssize:
            rbytes = rbytes + bytes(ssize - rbytes_len)
        return s.struct_def.unpack(rbytes)

    def _read_record(self, sf, r, signals):
        record_start = self._data_start + r * self._record_size
        for s in self._signal_infos:
            buf = self._read_signal_record(sf, s, record_start)
            start_pos = r * s.samples
            signals[s.index].put(range(start_pos, start_pos + len(buf)), buf, mode='clip')

    def read_signals(self, sf, signals_to_read=None):
        self._prepare_to_read(sf, signals_to_read)
        # npsignals = len(self._signal_infos)*[numpy.array([], dtype=int)]
        npsignals = []
        for s in self._signal_infos:
            npsignals.append(numpy.zeros(self._nrecords * s.samples, dtype=int))
        for r in range(0, self._nrecords):
            self._read_record(sf, r, npsignals)
        if not self._integers:
            for s in self._signal_infos:
                dig_min = self.header.signal_defs[s.index_in_file].dig_min
                dig_max = self.header.signal_defs[s.index_in_file].dig_max
                phys_min = self.header.signal_defs[s.index_in_file].phys_min
                phys_max = self.header.signal_defs[s.index_in_file].phys_max
                phys_dig = (phys_max - phys_min) / (dig_max - dig_min)
                npsignals[s.index] = (npsignals[s.index] - dig_min) * phys_dig + phys_min
        return npsignals

    def find_signal_index(self, signal_label):
        return self.header.find_signal_index(signal_label)

    def __eq__(self, other):
        return self.header == other.header if other is not None else False


class EdfData(EdfFile):
    def __init__(self, header, signals):
        super(EdfData, self).__init__(header)
        self.signals = signals
        if header.signals_in_file != len(signals):
            raise BaseException("Signals lenght different from no. signals in header")

    def _create_record_block(self, rec, signals_to_write):
        record_data = []
        for i in range(len(self.header.signal_defs)):
            start_index = rec * self.header.signal_defs[i].samples
            sig_data = signals_to_write[i][start_index:start_index + self.header.signal_defs[i].samples]
            if self._integers:
                buf = b''.join(struct.pack("<h", x) for x in sig_data)
            else:
                buf = b''.join(
                    (struct.pack("<h", int(x) if -32768.0 <= x <= 32767.0 else -32768 if x <= -32768.0 else 32767)
                     for x in sig_data))
            record_data.append(buf)
        return b''.join(record_data)

    def _signals_to_stream(self, sf):
        signals_to_write = self._prepare_signals_to_write()
        for i in range(self.header.records_in_file):
            rb = self._create_record_block(i, signals_to_write)
            sf.write(rb)

    def _signals_to_bytes(self):
        record_data = []
        signals_to_write = self._prepare_signals_to_write()
        for i in range(self.header.records_in_file):
            rb = self._create_record_block(i, signals_to_write)
            record_data.append(rb)
        return b''.join(record_data)

    def _prepare_signals_to_write(self):
        if self._integers:
            signals_to_write = self.signals
        else:
            signals_to_write = []
            for i in range(len(self.header.signal_defs)):
                dig_min = self.header.signal_defs[i].dig_min
                dig_max = self.header.signal_defs[i].dig_max
                phys_min = self.header.signal_defs[i].phys_min
                phys_max = self.header.signal_defs[i].phys_max
                dig_phys = (dig_max - dig_min) / (phys_max - phys_min)
                new_signal = (self.signals[i] - phys_min) * dig_phys + dig_min
                signals_to_write.append(numpy.rint(new_signal))
        return signals_to_write

    def to_bytes(self):
        return b''.join([self.header.to_bytes(), self._signals_to_bytes()])

    def signal_to_timeserie(self, signum, relative=False):
        signal_length = len(self.signals[signum])
        signal_frequency = (self.header.signal_defs[signum].samples / self.header.record_duration)
        if relative:
            signal_start = 0.0
            index_range = pd.timedelta_range(signal_start, periods=signal_length,
                                             freq=str(int(1000 / signal_frequency)) + 'ms')
        else:
            signal_start = datetime.combine(self.header.start_date, self.header.start_time)
            index_range = pd.date_range(signal_start, periods=signal_length,
                                        freq=str(int(1000 / signal_frequency)) + 'ms')
        return pd.Series(self.signals[signum], index=index_range)

    def signal_sampf(self, signum):
        return self.header.signal_defs[signum].samples / self.header.record_duration

    def __eq__(self, other):
        return (self.header == other.header and len(self.signals) == len(other.signals)) if other is not None else False

    def write_to_stream(self, sf):
        sf.write(self.header.to_bytes())
        self._signals_to_stream(sf)

    def write_to_file(self, file_name):
        with open(file_name, mode='wb') as ofile:
            self.write_to_stream(ofile)


def calculate_header_size(ns):
    return 256 * ns * 256


def create_from_stream(file_stream, signals_to_read=None, integers=False):
    header = create_header_from_stream(file_stream)
    edf2read = EdfFile(header, integers)
    signals = edf2read.read_signals(file_stream, signals_to_read)
    if signals_to_read is not None:
        hdict = header._asdict()
        sif = len(signals_to_read)
        hdict['signals_in_file'] = sif
        hdict['signal_defs'] = [header.signal_defs[x] for x in signals_to_read]
        hdict['bytes_in_header'] = calculate_header_size(sif)
        header = Header(**hdict)
    return EdfData(header, signals)


def create_from_file(file_name, signals_to_read=None, integers=False):
    with open(file_name, mode='rb') as ifile:
        instance = create_from_stream(ifile, signals_to_read, integers)
    if instance is not None:
        instance.filename = file_name
    return instance


####### EDF END #######

def _calculate_records_num(signal, smpls):
    r = int(round(signal.size/smpls))
    return r if (r*smpls) >= signal.size else r+1

def edfWriteAnnotation(edfWriter, onset_in_seconds, duration_in_seconds, description, str_format='utf-8'):
    edfWriter.writeAnnotation(onset_in_seconds, duration_in_seconds, description, str_format)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('expecting path to a sigfile as the only argument')
        exit(0)

    input_name = sys.argv[1]
    sf = read_signal_file(input_name,False)


    fevent = codecs.open(input_name + '_info' + '.txt', 'w',encoding='utf-8')

    fevent.write('HEADER INFO:' + '\n')
    ##### HEADER ############
    fevent.write('headerversion: ' + str(hex(sf.header.version_id)) + '\n')
    fevent.write('data offset: ' + str(hex(sf.data_table.measurement_info.offset)) + '\n')
    fevent.write('data size: ' + str(sf.data_table.measurement_info.size) + '\n')

    fevent.write("%20s\t%s\n" % ("ID:", sf.measurement.id))
    fevent.write("%20s\t%s\n" % ("Name:", sf.measurement.name))
    fevent.write("%20s\t%s\n" % ("Start hour:", sf.measurement.start_hour))
    fevent.write("%20s\t%s\n" % ("Street:", sf.measurement.street))
    fevent.write("%20s\t%s\n" % ("City:", sf.measurement.city))
    fevent.write("%20s\t%s\n" % ("Zip code:", sf.measurement.zip_code))

    fevent.write("%20s\t%s\n" % ("Sex:", sf.measurement.sex))
    fevent.write("%20s\t%s\n" % ("Doctor:", sf.measurement.doctor))
    fevent.write("%20s\t%s\n" % ("Technician:", sf.measurement.technician))
    fevent.write("%20s\t%s\n" % ("Start date:", sf.measurement.start_date))
    fevent.write("%20s\t%s\n" % ("Birth date:", sf.measurement.birthday))
    fevent.write("%20s\t%s\n" % ("Age:", sf.measurement.age))
    fevent.write("%20s\t%s\n" % ("Protocol:", sf.measurement.protocol))
    fevent.write("%20s\t%s\n" % ("Clinical info:", sf.measurement.clin_info))
    fevent.write("%20s\t%s\n" % ("Ref. doctor name:", sf.measurement.referring_doctor_name))
    fevent.write("%20s\t%s\n" % ("Ref. doctor code:", sf.measurement.referring_doctor_code))

    fevent.write("====================" + '\n')
    fevent.write("%20s\t%s\n" % ("Recorder name:", sf.recorder_info.name))
    fevent.write("%20s\t%d\n" % ("No rec. channels:", sf.recorder_info.nRecChannels))
    fevent.write("%20s\t%d\n" % ("Inverted AC channels:", sf.recorder_info.invertedACChannels))
    fevent.write("%20s\t%d\n" % ("Max voltage:", sf.recorder_info.maximumVoltage))
    fevent.write("%20s\t%d\n" % ("Normal voltage:", sf.recorder_info.normalVoltage))
    fevent.write("%20s\t%d\n" % ("Calibration signal:", sf.recorder_info.calibrationSignal))
    fevent.write("%20s\t%d\n" % ("Calibration scale:", sf.recorder_info.calibrationScale))
    fevent.write("%20s\t%d\n" % ("Video control:", sf.recorder_info.videoControl))
    fevent.write("%20s\t%d\n" % ("No sensitivities:", sf.recorder_info.nSensitivities))
    fevent.write("%20s\t%d\n" % ("No low filters:", sf.recorder_info.nLowFilters))
    fevent.write("%20s\t%d\n" % ("No high filters:", sf.recorder_info.nHighFilters))
    fevent.write("%20s\n" % ("Sensitivities:", ))
    for i in range(sf.recorder_info.nSensitivities):
        fevent.write("%20d:\t%f\n" % (i, sf.recorder_info.sensitivity[i]))

    fevent.write("%20s\n" % ("Low filters:", ))
    for i in range(sf.recorder_info.nLowFilters):
        fevent.write("%20d:\t%f\n" % (i, sf.recorder_info.lowFilter[i]))
    fevent.write("%20s\n" % ("High filters:", ))
    for i in range(sf.recorder_info.nHighFilters):
        fevent.write("%20d:\t%f\n" % (i, sf.recorder_info.highFilter[i]))
    fevent.write("%20s\t%s\n" % ("Montage name:", sf.recorder_info.montageName))
    fevent.write("%20s\t%d\n" % ("No channels used:", sf.recorder_info.numberOfChannelsUsed))
    fevent.write("%20s\t%d\n" % ("Global sensitivity:", sf.recorder_info.globalSens))
    fevent.write("%20s\t%d\n" % ("Epoch length:", sf.recorder_info.epochLengthInSamples))
    fevent.write("%20s\t%d\n" % ("Highest rate:", sf.recorder_info.highestRate))

    fevent.write(create_row_breaker(RecorderChannel) + '\n')
    fevent.write(create_table_title(RecorderChannel) + '\n')
    fevent.write(create_row_breaker(RecorderChannel) + '\n')

    for rc in sf.recorder_info.channels:
        fevent.write(create_row(RecorderChannel, rc.create_data_tuple(sf.recorder_info.sensitivity, sf.recorder_info.lowFilter, sf.recorder_info.highFilter)))
    fevent.write("%20s\t%d\n" % ("Page buffor size:", sum([x.save_buffer_size for x in sf.recorder_info.channels])))



    fevent.write("====================" + '\n')
    fevent.write("%20s\t%s\n" % ("Signal table offset:", sf.data_table.signal_info.offset))
    fevent.write("%20s\t%s\n" % ("First page size:", sf.data_table.signal_info.size))
    fevent.write("%20s\t%s\n" % ("Page header size:", sf.data_table.signal_info.header_size))


    fevent.write("====================" + '\n')
    fevent.write("Events" + '\n')
    for evt in sf.events:
        st = Event.ST_DICT.get((evt.ev_type, evt.sub_type))
        fevent.write(str(Event.ET_DICT.get(evt.ev_type)) + ',' +
                     str((st if st is not None else evt.sub_type)) + ',' +
                     str(evt.page) + ',' +
                     str(evt.page_time) + ',' +
                     str(decode_time(evt.time).isoformat()) + ',' +
                     str(evt.duration) + ',' +
                     str(evt.duration_in_ms) + ',' +
                     str(hex(evt.channels)) + ',' +
                     str(evt.info) + ',' +
                     str((evt.page-1)*sf.recorder_info.epochLengthInSamples/float(sf.recorder_info.highestRate) + evt.page_time) + '\n')

    fevent.write("====================" + '\n')
    fevent.write("Events defs:" + '\n')
    for evd in sf.events_desc:
        fevent.write(evd.label + ',' +
                     evd.desc + ',' +
                     str(EventDesc.DT_DICT.get(evd.d_type)) + ',' +
                     str(evd.value) + '\n')

    # print("====================")
    # print("Signal Pages:")
    # i = 0
    # for page in sf.signal_pages:
    #     print(i,page.filling, page.time)
    #     i += 1
    fevent.close()
    ##### DATA ############
    epoch_length = 1

    #dest_dir = sys.argv[2]
    #signal_name = sys.argv[3]
    meas_id = os.path.splitext(os.path.split(input_name)[1])[0]
    print('Processing conversion of edf for: {}'.format(input_name))

    #dest_path = meas_id+'.EDF'

    #fnames = make_brainlab_filenames(input_name)
    #sf = read_signal_file(fnames[0], True)
    print('Reading: {}'.format(input_name))
    sf = read_signal_file(input_name, True)
    #ch_index = 0
    # for ch_index in range(sf.signal_data.__len__()):
    #     # ch_index=-1
    #     # i=0
    #     # for c in sf.recorder_info.channels:
    #     #     if c.signal_type == signal_name:
    #     #         ch_index=i
    #     #         break
    #     #     else:
    #     #         i+=1
    #     if ch_index <0:
    #         #print(" Channel {} no found. Skipping!".format(signal_name))
    #         print(" Channel {} no found. Skipping!")
    #     else:
    #         dest_path = input_name + '_ch' + str(ch_index+1)
    #         if os.path.exists(dest_path):
    #             print(" !!!! File exists in dest dir ({}). Skipping!".format(dest_path))
    #         ch = sf.recorder_info.channels[ch_index]
    #         print(" Channel {} found, Description: {} Subtype: {} Sampling: {}. Saving to {}".format(ch.signal_type, ch.channel_desc, ch.signal_sub_type, ch.sampling_rate, dest_path))
    #         samples = epoch_length*ch.sampling_rate
    #         ch_signal = sf.signal_data[ch_index]*100
    #
    #         signal_defs = [SignalDefinition(ch.signal_type.encode(), ch.signal_sub_type.encode(), "uV", -2560.0, 2560.0, -32767, 32767, "", samples,'')]
    #         version = "0"
    #         patient_id = "Id:"+sf.measurement.id+" Name:"+sf.measurement.name+" Birthdate:"+sf.measurement.birthday.strftime("%d-%b-%Y").upper()
    #         record_id = "Id:"+meas_id+" Startdate:"+ sf.measurement.start_date.strftime("%d-%b-%Y").upper()+" Protocol:"+sf.measurement.protocol
    #         start_date = sf.measurement.start_date
    #         start_time = sf.signal_pages[0].time
    #         header_bytes = 0
    #         records = _calculate_records_num(ch_signal, samples)
    #         if ch_signal.size < (records*samples):
    #             ch_signal = numpy.append(ch_signal, numpy.zeros((records*samples)-ch_signal.size))
    #
    #         record_duration = epoch_length
    #         signals_no = 1
    #         header = Header(version, patient_id.encode(), record_id.encode(), start_date, start_time, header_bytes, "", records, record_duration, signals_no, signal_defs)
    #         edf_file = EdfData(header, [ch_signal])
    #         print('Writing: {}'.format(dest_path+'.EDF'))
    #         edf_file.write_to_file(dest_path+'.EDF')


            ####### EDF 2 ########

    dest_path = input_name

    #EDF_format_extention = ".edf"
    #EDF_format_filetype = pyedflib.FILETYPE_EDFPLUS
    # temp_filterStringFileIndicator = "_prefiltered"
    # temp_filterStringHeader = 'HP ' + str(self.prefilterEDF_hp) + ' Hz'
    EDF_format_extention = ".bdf"
    EDF_format_filetype = pyedflib.FILETYPE_BDFPLUS
    temp_filterStringFileIndicator = "_not_refiltered"

    nChannels = sf.signal_data.__len__()
    exportFileName = dest_path + temp_filterStringFileIndicator + EDF_format_extention
    edfWriter = pyedflib.EdfWriter(exportFileName, nChannels,
                                   file_type=EDF_format_filetype)

    """
     Only when the number of annotations you want to write is more than the number of seconds of the duration of the recording, you can use this function to increase the storage space for annotations */
    /* Minimum is 1, maximum is 64 */
    """
    nEvents = sf.events.__len__()
    nSecondsRecording = sf.signal_pages.__len__()*sf.recorder_info.epochLengthInSamples/float(sf.recorder_info.highestRate)
    edfAnnotationChannels = int(math.ceil(nEvents/nSecondsRecording))
    edfWriter.set_number_of_annotation_signals(edfAnnotationChannels)  # 7*60 = 420 annotations per minute on average
    version = "0"
    patient_id = "Id:" + sf.measurement.id + " Name:" + sf.measurement.name + " Birthdate:" + sf.measurement.birthday.strftime("%d-%b-%Y").upper()
    record_id = "Id:" + meas_id + " Startdate:" + sf.measurement.start_date.strftime("%d-%b-%Y").upper() + " Protocol:" + sf.measurement.protocol
    start_date = sf.measurement.start_date
    start_time = sf.signal_pages[0].time
    header_bytes = 0
    edfWriter.setTechnician('')
    edfWriter.setRecordingAdditional(" Protocol:" + sf.measurement.protocol)
    edfWriter.setPatientName(sf.measurement.name)
    edfWriter.setPatientCode(sf.measurement.id)
    edfWriter.setPatientAdditional(meas_id)
    edfWriter.setAdmincode('')
    edfWriter.setEquipment(sf.recorder_info.name)
    edfWriter.setGender(sf.measurement.sex == 'M')
    # edfWriter.setBirthdate(datetime.date(2000, 1, 1))
    edfWriter.setBirthdate(sf.measurement.birthday)
    # sf.measurement.birthday.strftime("%d-%b-%Y").upper()
    dt = datetime.combine(sf.measurement.start_date, sf.measurement.start_hour)
    edfWriter.setStartdatetime(dt)
    edfWriteAnnotation(edfWriter, 0, -1, u"signal_start")


    chFactor = 100

    for ch_index in range(nChannels):

        recinf = sf.recorder_info.channels[ch_index]
        temp_filterStringHeader = 'HP ' + str(sf.recorder_info.highFilter[recinf.high_filter_index]) + ' ' + 'LP ' + str(sf.recorder_info.lowFilter[recinf.low_filter_index])

        ch = sf.recorder_info.channels[ch_index]
        samples = epoch_length * ch.sampling_rate
        #chInvert = 1
        #if recinf.cal_factor < 0:
        #    chInvert = -1
        ch_signal = sf.signal_data[ch_index] * chFactor
        #records = _calculate_records_num(ch_signal, samples)
        #if ch_signal.size < (records * samples):
        #    ch_signal = numpy.append(ch_signal, numpy.zeros((records * samples) - ch_signal.size))



        if EDF_format_extention == ".edf":
            #EDF_Physical_max_microVolt = int(max(math.ceil(max(abs(ch_signal)) * chFactor), 1))
            #if (EDF_Physical_max_microVolt % 2) != 1:
            #    EDF_Physical_max_microVolt += 1
            #EDF_Physical_mim_microVolt = -EDF_Physical_max_microVolt
            EDF_Physical_max_microVolt = 3277
            EDF_Physical_min_microVolt = -EDF_Physical_max_microVolt
            channel_info = {'label': 'ch', 'dimension': recinf.unit, 'sample_rate': int(round(ch.sampling_rate)),
                            'physical_max': EDF_Physical_max_microVolt, 'physical_min': EDF_Physical_min_microVolt,
                            'digital_max': 32767, 'digital_min': -32767,
                            'prefilter': temp_filterStringHeader, 'transducer': 'none'}

        if EDF_format_extention == ".bdf":
            EDF_Physical_max_microVolt = 187500
            EDF_Physical_min_microVolt = -EDF_Physical_max_microVolt
            channel_info = {'label': 'ch', 'dimension': recinf.unit, 'sample_rate': int(round(ch.sampling_rate)),
                            'physical_max': EDF_Physical_min_microVolt, 'physical_min': EDF_Physical_min_microVolt,
                            'digital_max': 8388607, 'digital_min': -8388607,
                            'prefilter': temp_filterStringHeader, 'transducer': 'none'}

        edfWriter.setSignalHeader(ch_index, channel_info.copy())

        #chName = ch.signal_type  # ch.channel_desc, ch.signal_sub_type
        chType = ch.signal_type
        chName = ch.channel_desc  # ch.channel_desc, ch.signal_sub_type
        iEnd = chName.find(' ')
        if iEnd < 0:
            iEnd = chName.__len__()
        chName = chName[0:iEnd]
        chName = chType + '-' + chName
        chName = chName.replace(' ','_')
        chName = chName.replace('---,','')

        edfWriter.setLabel(ch_index, chName)

    ch = sf.recorder_info.channels[0]
    nBlocks = int(math.ceil(float(sf.signal_data[0].__len__())/ch.sampling_rate))
    for iBlock in range(nBlocks):
        for ch_index in range(nChannels):
            recinf = sf.recorder_info.channels[ch_index]
            #chInvert = 1
            #if recinf.cal_factor < 0:
            #    chInvert = -1
            ch = sf.recorder_info.channels[ch_index]
            iBeg = iBlock*ch.sampling_rate
            iEnd = (iBlock+1)*ch.sampling_rate
            #samples = epoch_length * ch.sampling_rate
            ch_signal = sf.signal_data[ch_index][iBeg:iEnd] * chFactor
            #records = _calculate_records_num(ch_signal, samples)
            #if ch_signal.size < (ch.sampling_rate * samples):
             #   ch_signal = numpy.append(ch_signal, numpy.zeros((records * samples) - ch_signal.size))
            ch_signal[ch_signal > EDF_Physical_max_microVolt] = EDF_Physical_max_microVolt
            ch_signal[ch_signal < EDF_Physical_min_microVolt] = EDF_Physical_min_microVolt
            edfWriter.writePhysicalSamples(ch_signal)
            ####### EDF 2 end ####

    for evt in sf.events:
        st = Event.ST_DICT.get((evt.ev_type, evt.sub_type))
        eventName = Event.ET_DICT.get(evt.ev_type) + '_' + (st if st is not None else evt.sub_type)
        second = (evt.page - 1) * sf.recorder_info.epochLengthInSamples / float(sf.recorder_info.highestRate) + evt.page_time
        duration = -1
        edfWriteAnnotation(edfWriter, second, duration, eventName.encode("utf-8"))

    print('------ Writing of file ' + exportFileName + ' finished! --------')