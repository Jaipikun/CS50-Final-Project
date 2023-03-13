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
        sys.exit("Error while calculating wave")


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
        sys.exit("Error while calculating wave")

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
        sys.exit("Error while calculating wave")

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
        sys.exit("Error while calculating wave")

#####################################
#       Combine audio files         #
#####################################

def combine(file1_path,file2_path):
    audio_params_1 = []
    audio_params_2 = []
    data_1 = []
    data_2 = []
    with wave.open(file1_path,'rb') as file1:
        audio_params_1 = file1.getparams()
        data_1 = file1.readframes(audio_params_1[3])
        with open("data.txt",'w') as data:
            data.write(str(data_1))

    with wave.open(file2_path,'rb') as file2:
        audio_params_2 = file2.getparams()
        data_2 = file2.readframes(audio_params_2[3])

    for i in range(len(audio_params_1)):
        if audio_params_1[i]!=audio_params_2[i]:
            return "Incompatible audio files"
    convert_from_16bit(data_1)
    max_1 = max(data_1)
    max_2 = max(data_2)


    new_data = []


    for i in range(len(data_1)):
        new_data.append(((data_1[i]/max_1)+(data_2[i]/max_2))*0.5)
        

    generate_wav_file(new_data,audio_params_1,"Combined_Audio")

    return "Files combined successfully!"





#####################################
#   Additional / helper functions   #
#####################################

def convert_to_16bit(data):
    try:
        _16bit_val = []
        for i in range(0,len(data)):
            data[i]*=32767.0 # scaling values to 16 bit by multiplying it by max amplitude
            data[i]=round(data[i])
            _16bit_val.append( struct.pack('<h', data[i]))
        return _16bit_val
    except TypeError:
        sys.exit("Error while converting data")


def convert_from_16bit(data):
    #try:
        converted = []
        for i in data:
            converted.append(struct.unpack("<h",i))
        print(converted[0])
        return converted

    #except TypeError:
        sys.exit("Error while converting data")


def generate_wav_file(data,audio_params,name):
    try:
        with wave.open(name+".wav",'wb') as audio:
            audio.setparams(audio_params)
            data = convert_to_16bit(data)
            for i in data:
                audio.writeframesraw(i)
    except wave.Error:
        sys.exit("Something wrong with .wav file")


def sign(value):
    try:
        if value>0:
            return 1
        if value<0:
            return -1
        return 0
    except TypeError:
        sys.exit("Nan")


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
    
    elif len(sys.argv) == 3:
        file_path1 = sys.argv[1]
        file_path2 = sys.argv[2]
        combine(file_path1,file_path2)

    else:
        sys.exit("Incorrect amount of arguments")

    return 0



if __name__ == "__main__":
    main()