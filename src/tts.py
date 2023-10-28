import subprocess

class AudioClip:    
    def __init__(self, text, speed=1, voice="awb"):
        self.text = text
        self.voice = voice
        self.speed = speed

    #This function will output a .wav file of the given audio clip.
    def export(self, outFileName):
        with open(outFileName, 'w') as file:
            subprocess.run(['mimic3', ('"' + self.text + '"'), '--voice', ('en_US/cmu-arctic_low#' + self.voice), '--length-scale', str(self.speed)], stdout=file)

    #Will play the audio for the clip.
    def play(self):
        subprocess.run(['mimic3', ('"' + self.text + '"'), '--voice', ('en_US/cmu-arctic_low#' + self.voice), '--length-scale', str(self.speed)])

       
clip1 = AudioClip("Testing a new sentance.", 0.8)
clip1.export("test.wav");
