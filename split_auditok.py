from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for, dataset
import sys
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
def split(filename='g1238-20181214-081712-1544750232.37681.wav'):
    sr, samples = wavfile.read(filename=filename, mmap=True)
    #print(len(samples))
    plt.plot(samples)
    asource = ADSFactory.ads(filename=filename, record=False)
    validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold=50)
    # Default analysis window is 10 ms (float(asource.get_block_size()) / asource.get_sampling_rate())
    # min_length=20 : minimum length of a valid audio activity is 20 * 10 == 200 ms
    # max_length=400 :  maximum length of a valid audio activity is 400 * 10 == 4000 ms == 4 seconds
    # max_continuous_silence=30 : maximum length of a tolerated  silence within a valid audio activity is 30 * 10 == 300 ms 
    tokenizer = StreamTokenizer(validator=validator, min_length=100, max_length=500, max_continuous_silence=50)
    asource.open()
    tokens = tokenizer.tokenize(asource)
    stack=[]
    sum=[]
    for i,t in enumerate(tokens):
        #print("Token [{0}] starts at {1} and ends at {2}".format(i+1, t[1], t[2]))
        stack.append([t[1]*80, t[2]*80])
        sum.append((t[2]*80 - t[1]*80)/8000)
        wavfile.write('token_'+str(i)+'.wav',sr,samples[t[1]*80:t[2]*80]) #write to file
    asource.close()
    print(sum)
    return stack

split()