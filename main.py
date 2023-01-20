import tkinter as tk
import tkinter.ttk as ttk
import funcs_cards as funcs
from PIL import Image, ImageTk
import time
from datetime import datetime

#  beginning of the game
def start():   
    global cards_on_field, count, clicks, btn, window, frame_btns, frame_cards, all_cards, start_time

    count = 0
    all_cards = []
    cards_on_field = []
    clicks = []
    btn = None
    all_cards = funcs.new_cards()

    # destroy all widgets (labels and buttons) from previous screen
    for widget in frame_cards.winfo_children():
        widget.destroy()
    for widget in frame_btns.winfo_children():
        widget.destroy()

    btn_more = ttk.Button(master=frame_btns, text='More cards', command=more_card, width=12, style='My.TButton', name='more')
    btn_more.grid(row=0, column=0, padx=5, pady=5)

    btn_end = ttk.Button(master=frame_btns, text='End the game', command=end_game, width=15, style='My.TButton')
    btn_end.grid(row=0, column=1, padx=5, pady=5)

    btn_help = ttk.Button(master=frame_btns, text='Help', name='help', command=help_find, width=8, style='My.TButton', )
    btn_help.grid(row=0, column=2, padx=5, pady=5)

    lbl_count = ttk.Label(text=f'Score: {count}', master=frame_btns)
    lbl_count.config(font=("Courier", 20))
    lbl_count.grid(row=0, column=3, padx=5, pady=5)

    # creating and laying out cards
    for i in range(3):
        for j in range(4):
            card = all_cards.pop()
            create_card_button(card, i, j)

    start_time = datetime.now()   # start point for timer


def help_find():
    """function to find and emphasize set on the screen"""

    result = funcs.find_set(cards_on_field)   # set of 3 set cards
    if result:  # if set exist
        for bttn in frame_cards.winfo_children():
            if bttn.card in result:
                bttn.config(background='green')  # made green background for one card
                break
    else:   # if set doesn't exist
        if len(cards_on_field) == 12:    #  if it is posssible to give more cards
            more_card()
        else:   # if it is not posssible to give more cards
            end_game()


def create_card_button(card, i, j, add=1):
    """Create new button and put it on the screen. If needed - add to cards_on_field list"""
    img = Image.open(card.pict)
    img = img.resize((140, 200))
    img = ImageTk.PhotoImage(img)
    btn = tk.Button(image=img, master=frame_cards, padx=5, pady=5, width=146, height=206, background='white')
    btn.image = img
    btn.card = card
    btn.i = i
    btn.j = j
    btn.bind('<Button-1>', lambda event, btn=btn: click(event, btn))
    btn.grid(row=i, column=j, padx=5, pady=5)
    if add:
        cards_on_field.append(card)
    return




def click(event, button):
    """Handle click on card button"""
    global clicks, count, all_cards
    if button:
        if button in clicks:  # if there is a re-click
            clicks.remove(button)
            button.config(background='white')
        else:
            time.sleep(.1)
            button.config(background='black')   # change bg color
            button.update()
            time.sleep(.1)
            
            clicks.append(button)

            if len(clicks) == 3:   # if a third card was chosen
                time.sleep(.1)
                result = funcs.check_set(*(i.card for i in clicks))
                for bttn in frame_cards.winfo_children():
                    bttn.config(background='white')
                if result:  #  if set
                    count += 1

                    lbl_count = ttk.Label(text=f'Score: {count}', master=frame_btns)
                    lbl_count.config(font=("Courier", 20))
                    lbl_count.grid(row=0, column=3, padx=5, pady=5)
                    

                    if all_cards:  # if there are other cards 
                        if len(cards_on_field) == 12:  #  if there are 12 cards on the screen

                            for bttn in clicks:
                                cards_on_field.remove(bttn.card)
                                bttn.destroy()
                                card = all_cards.pop()
                                create_card_button(card, bttn.i, bttn.j)
                            assert len(frame_cards.winfo_children()) == 12

                        else:   # if number of cards on the screen > 12
                            btn_more = ttk.Button(master=frame_btns, text='More cards', command=more_card, width=15, style='My.TButton', name='more')
                            btn_more.grid(row=0, column=0, padx=5, pady=5)
                            decrease_column(4)
                            assert len(frame_cards.winfo_children()) == 12

                    else:  # if there is no more card to spread
                        j = max((a.j for a in frame_cards.winfo_children()))
                        decrease_column(j)
    
                clicks = []


def decrease_column(col):
    """Remove 3 cards from the screen, decrease number of columns"""
    global clicks, cards_on_field, frame_cards
    
    it = filter(lambda a: a.j != col, clicks)   # cards that are in the SET and not at the last column
    for bttn in frame_cards.winfo_children():
        if bttn.j == col and bttn not in clicks:   # if card not in the SET and at the last column, move it to the empty place on the screen
            old_bttn = next(it)
            create_card_button(bttn.card, old_bttn.i, old_bttn.j, add=0)

    for bttn in clicks:
        cards_on_field.remove(bttn.card)   # remove SET cards from the list with cards on the field
    for widget in frame_cards.winfo_children():
        if widget in clicks or widget.j == col:
            widget.destroy()   # destroy buttons with SET cards


def end_game():
    """Creating screen for the end of the game"""
    for widget in frame_cards.winfo_children():
        widget.destroy()
    for widget in frame_btns.winfo_children():
        widget.destroy()
    

    lbl_end = ttk.Label(text='End of the game!', master=frame_cards)
    lbl_end.config(font=("Courier", 50))

    lbl_score = ttk.Label(text=f'Your score: {count}', master=frame_cards)
    lbl_score.config(font=("Courier", 30))

    t = datetime.now() - start_time
    t_sec = t.seconds % 60
    t_min = (t.seconds // 60) % 60
    t_hour = t_min // 60
    lbl_time = ttk.Label(text=f'Your time: {t_hour}:{t_min}:{t_sec}', master=frame_cards)
    lbl_time.config(font=("Courier", 30))

    btn_start = ttk.Button(text='Start New Game', master=frame_btns, style='My.TButton', command=start, width=20, padding=5)
    btn_start.pack(pady=5)

    lbl_end.grid(row=0, column=0, padx=10, pady=10)
    lbl_score.grid(row=1, column=0, padx=10, pady=10)
    lbl_time.grid(row=2, column=0, padx=10, pady=10)



def more_card():
    """Spread more 3 more cards at the 4th column"""
    if funcs.find_set(cards_on_field):   # if there is a SET on the screen, just emphasize it 
        help_find()
    else:
        if all_cards:
            time.sleep(.1)
            for i in range(3):
                card = all_cards.pop()
                create_card_button(card, i, 4)
            frame_btns.children['more'].destroy()
        else:   # if there are no more cards and no SET - finish the game
            end_game()



def main():
    """First appearance, hello screen"""
    global  window, frame_cards, frame_btns
    window = tk.Tk()
    window.title('SET')
    window.geometry('900x780+50+0')

    frame_cards = ttk.Frame(master=window)
    frame_cards.pack(padx=10, pady=10)

    frame_btns = ttk.Frame(master=window)
    frame_btns.pack(padx=10, pady=10)
    
    s = ttk.Style()
    s.configure('My.TButton', font=("Courier", 20))

    lbl_start = ttk.Label(text='Welcome to the SET game!', master=frame_cards)
    lbl_start.config(font=("Courier", 40))
    lbl_start.grid(row=0, column=0, padx=10, pady=50)

    lbl_rules = ttk.Label(text='\tThe object of the game is to identify a SET of 3 cards of 12 cards placed faced up on the screen. Each card has 4 features: color, shape, number, and shading.\n\n\tA SET consist of 3 cards in which each of the cards features, looked at one-by-one, are the same on each card, or, are different on each card. All of the features must separaley satisfy this rile. In other words: shape must ve either the same on all 3 cards, or different on each of the 3 cards; color must be either the same of all 3 cards, or different on each of the 3, etc.', master=frame_cards, wraplength=700)
    lbl_rules.config(font=("Courier", 15))
    lbl_rules.grid(row=1, column=0, padx=10, pady=10)

    
    btn_start = ttk.Button(text='Start Game', master=frame_btns, style='My.TButton', command=start, width=17, padding=5)
    btn_start.pack(pady=5)


    window.mainloop()


if __name__ == '__main__':
    main()