from pymongo import MongoClient
from urllib import urlopen
from PIL import ImageTk, Image
import random, Tkinter, tkMessageBox, base64, io
from sentiment_request import *

def run_buddE():
    """
    Sets up the database and documents, then initializes and runs the buddE
    prompt
    """
    my_buddE = SetUp().setup_buddE()
    my_buddE.root.mainloop()

# Class for setting up database and getting quotes to choose from
class SetUp:
    def __init__(self):
        self.mood = "init"
        self.quote = "init"
        self.client = MongoClient()
        self.db = self.client.buddE
        self.set_mood()
        self.setup_db()
        self.get_items()

    def set_mood(self):
        """
        Method to set mood attribute (will integrate with Emotion API instead of
        hard-coding when ready)
        """
        self.mood = "sad"

    def setup_db(self):
        """ Sets up the database document to pull quotes from, depending on mood. """
        self.quotes = self.db.motivational_quotes.find()
        # if self.mood == "sad":
        #     self.quotes = self.db.cheerful_quotes.find()
        #     # self.images = db.cute_images.find()
        # elif self.mood == "stressed":
        #     self.quotes = self.db.motivational_quotes.find()

    def get_items(self):
        """ Gets a random quote from the appropriate database """
        a = random.randint(0, self.quotes.count()-1)
        # if self.mood == "sad":
        #     b = random.randint(0, self.images.count()-1)
        # score = 0
        # while score < 0.9:
            # dic = random.choice(self.quotes.keys())
            # self.quote = self.quotes[dic]["text]
            # score = getSentiment(self.quote)

        self.quote = self.quotes[a]["_id"]
        # if self.mood == "sad":
        #     self.image = self.images[b]["_id"]

    def setup_buddE(self):
        """ initializes an instance of buddE and returns it """
        new_buddE = buddE(self.mood, self.quote)
        return new_buddE

# Class containing the GUI components of buddE
class buddE:
    def __init__(self, mood, quote):
        self.mood = mood
        self.quote = quote

    def setup_GUI(self):
        """ Sets up the GUI using Tkinter library """
        self.root = Tkinter.Tk()
        self.root.title("Your buddE")
        w = 520
        h = 320
        x = 400
        y = 200
        self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
        if self.mood == "sad":
            label = Tkinter.Label(self.root, text=self.quote, wraplength=450, justify='left')
            label.pack(side="top", fill="both", expand=True, padx=20, pady=20)

            # Image GUI commented out because still in progress

            # img = ImageTk.PhotoImage(Image.open("/Users/ellen_fu/Downloads/cc2c8aa9b6ae636df821881a1a39e15b.jpg"))
            # #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
            # panel = Tkinter.Label(self.root, image = img)
            # #The Pack geometry manager packs widgets in rows or columns.
            # panel.pack(side = "bottom", fill = "both", expand = "yes")


            # print(image)
            # image_byt = urlopen("https://media.giphy.com/media/8Bbl0U61TN6DK/giphy.gif").read()
            # urlopen("https://media.giphy.com/media/8Bbl0U61TN6DK/giphy.gif").close()
            #
            # image_b64 = base64.encodestring(image_byt)
            # photo = Tkinter.PhotoImage(data=image_b64)

            # # create a white canvas
            # cv = Tkinter.Canvas(bg='white')
            # cv.pack(side='top', fill='both', expand='yes')

            # put the image on the canvas with
            # create_image(xpos, ypos, image, anchor)
            # cv.create_image(240, 130, image=photo)
            button = Tkinter.Button(self.root, text="c:", command=lambda: self.root.destroy())
            button.pack(side="bottom", fill="none", expand=True)
        elif self.mood == "happy":
            label = Tkinter.Label(self.root, text="Let us know why you're happy! Enter a quote you'd cheer your friends up with :)", wraplength=450, justify='left')
            label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
            e = Tkinter.Entry(self.root, width=50)
            e.pack()
            e.focus_set()
            # button = Tkinter.Button(self.root, text="What did I say?", command=self.callback(user_quote))
            button = Tkinter.Button(self.root, text="Thanks for sharing happiness!", command=self.getquote(e))
            button.pack(side="bottom", fill="none", expand=True)

    def getquote(self, entry):
        """ method for debugging GUI button """
        user_quote = entry.get()
        # self.add_to_db(user_quote)
        print(user_quote)

    def add_to_db(self, user_quote):
        """ method for determining whether or not to add user's input quote to DB """
        result = RequestSentiment(user_quote).get_sentiment()
        print(result)
        score = ''
        for character in result:
            if character.isdigit():
                score += character
                if len(score) == 1:
                    score += '.'
        score = float(score)
        if score > 0.9:
            try:
                self.db.cheerful_quotes.insert_one({"_id": user_quote})
            except Exception as e:
                print("This error occurred:", e)
                pass


run_buddE()
