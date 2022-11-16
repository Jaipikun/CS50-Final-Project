import sys
import wave
import math
import struct

#########################
#       sys args        #
#########################
# 1 - wave type:        #
#       a) sine         #
#       b) square       #
#       c) triangle     #
#       d) sawtooth     #
# 2 - frequency         #
# 3 - output file name  #
#########################

###########################
#   Audio output config   #
###########################

duration = 2     # in seconds

num_channels = 2
sample_width = 4
samplerate = 44100
num_frames = 2*samplerate
amplitude = 1

######################
#   Wave type dict   #
######################

Types = {
    "SINE" : 1,
    "SQUARE" : 2,
    "TRIANGLE" : 3,
    "SAWTOOTH" : 4
}

###########################
#      Main functions     #
###########################


#############
# sine wave #
#############

def calculate_sine_wave(frequency,amplitude,audio_params):
    try:
        if amplitude < 0.0:
            amplitude = 0.0
        if amplitude > 1.0:
            amplitude = 1        
              
        values = []

        for i in range(0,audio_params[2]*4*duration):
            t = float(i)/float(audio_params[2])
            values.append(float(amplitude)*math.sin(2.0*math.pi*float(frequency)*t))



        return values

    except ValueError:
        sys.exit("Error")


###############
# square wave #
###############

def calculate_square_wave(frequency,amplitude,audio_params):
    try:
        if amplitude < 0.0:
            amplitude = 0.0
        if amplitude > 1.0:
            amplitude = 1       

        values = []
        for i in range(0,audio_params[2]*4*duration):
            values.append(sign(float(amplitude)*math.sin(2.0*math.pi*float(frequency)*float(i)/float(audio_params[2]))))

        return values

    except ValueError:
        sys.exit("Error")

#################
# Triangle wave #
#################


def calculate_triangle_wave(frequency,amplitude,audio_params):
    try:
        if amplitude < 0.0:
            amplitude = 0.0
        if amplitude > 1.0:
            amplitude = 1       

        values = []
        for i in range(0,audio_params[2]*4*duration):
            t = float(i)/float(audio_params[2])
            values.append(4.0*frequency*(t-pow(2*frequency,-1)*math.floor(2*t*frequency+0.5))*pow(-1,math.floor(2*t*frequency+0.5)))

        return values

    except ValueError:
        sys.exit("Error")

#################
# Sawtooth wave #
#################


def calculate_sawtooth_wave(frequency,amplitude,audio_params):
    try:
        if amplitude < 0.0:
            amplitude = 0.0
        if amplitude > 1.0:
            amplitude = 1       

        values = []
        for i in range(0,audio_params[2]*4*duration):
            t = float(i)/float(audio_params[2])
            values.append(2*(t*frequency-math.floor(0.5+t*frequency)))

        return values

    except ValueError:
        sys.exit("Error")

#####################################
#   Additional / helper functions   #
#####################################

def convert_to_16bit(data):
    _16bit_val = []

    for i in range(0,len(data)):
        data[i]*=32767.0 # scaling values to 16 bit by multiplying it by max amplitude
        data[i]=round(data[i])
        _16bit_val.append( struct.pack('<h', data[i]))
    return _16bit_val


def generate_wav_file(data,audio_params,name):
    with wave.open(name+".wav",'wb') as audio:
        audio.setparams(audio_params)
        data = convert_to_16bit(data)
        for i in data:
            audio.writeframesraw(i)


def sign(value):
    if value>0:
        return 1
    if value<0:
        return -1
    return 0


###########################
#          Main           #
###########################

def main():
    if len(sys.argv) == 4:


        try:
            if float(sys.argv[2])<0:
                sys.exit("Incorrect frequency")

            frequency = float(sys.argv[2])/4.0
        except (ValueError,TypeError):
            sys.exit("Incorrect frequency")

        try:
            wave_type = int(Types[sys.argv[1].upper()])
        except KeyError:
            sys.exit("Wrong wave type")

        audio_params = [num_channels,sample_width,samplerate,num_frames,'NONE','not compressed']

        if wave_type == 1:
            data = calculate_sine_wave(frequency,amplitude,audio_params)


        if wave_type == 2:
            data = calculate_square_wave(frequency,amplitude,audio_params)


        if wave_type == 3:
            data = calculate_triangle_wave(frequency,amplitude,audio_params)


        if wave_type == 4:
            data = calculate_sawtooth_wave(frequency,amplitude,audio_params)


        generate_wav_file(data,audio_params,sys.argv[3])
    else:
        sys.exit("Incorrect amount of arguments")
    return 0



if __name__ == "__main__":
    main()