import subprocess
import time

#This is the main tts object. If you want to make a new tts querry, create a new one of these.
class AudioClip:    
    def __init__(self, text, speed=1, voice="awb"):
        self.text = text
        self.voice = voice
        self.speed = speed

    #This function will output a .wav file of the given audio clip.
    def export(self, outFileName):
        with open(outFileName, 'w') as file:
            subprocess.run(['mimic3', '--remote', '--voice', ('en_US/cmu-arctic_low#' + self.voice), ('"' + self.text + '"'), '--length-scale', str(self.speed)], stdout=file)

    #Will play the audio for the clip.
    def play(self):
        subprocess.run(['mimic3', '--remote', '--voice', ('en_US/cmu-arctic_low#' + self.voice), ('"' + self.text + '"'), '--length-scale', str(self.speed)])



# A temporary method to test the tts.
def main():
    #Creating the tts generation server.
    server = subprocess.Popen(['mimic3-server'])
    time.sleep(5)

    #Playing test clips.
    clip1 = AudioClip("Testing a new sentance.", 0.8)
    clip1.play()

    clip1.text = "This is a different, but still awesome, sentance."
    clip1.play()


    #Killing the server before exiting.
    server.kill()

if __name__ == "__main__":
    main()