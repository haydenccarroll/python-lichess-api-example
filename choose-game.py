import berserk
import dotenv
import os
import chess.svg
import tkinter as tk
from PIL import Image, ImageTk



dotenv.load_dotenv()
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

def on_click(event):
    dotenv_file = dotenv.find_dotenv()
    os.environ['GAME_ID'] = event
    dotenv.set_key(dotenv_file, "GAME_ID", os.environ['GAME_ID'])


session = berserk.TokenSession(AUTH_TOKEN)
client = berserk.Client(session=session)
game_list = berserk.clients.Games(session).get_ongoing()
gameImages = []
window = tk.Tk()
NUM_GAMES_PER_ROW = 3
IMG_SIZE = 250
window.geometry(f'{IMG_SIZE*NUM_GAMES_PER_ROW}x{IMG_SIZE*NUM_GAMES_PER_ROW}')

for game in game_list:
    fen = game["fen"]
    gameId = game["gameId"]
    print(gameId)
    is_flipped = True if game["color"] == "black" else False
    board = chess.Board(fen)
    svg = chess.svg.board(board, flipped=is_flipped)

    with open("temp.svg", 'w') as file:
        file.write(svg)
    os.system(f"inkscape --without-gui temp.svg -w {IMG_SIZE} -h {IMG_SIZE} -o temp.png")
    img = Image.open('temp.png')
    pimg = ImageTk.PhotoImage(img)
    gameImages.append((pimg, img, gameId))

size = (IMG_SIZE*NUM_GAMES_PER_ROW, IMG_SIZE*NUM_GAMES_PER_ROW)

frames = [tk.Button() for _ in gameImages]
for index, (pimg, img, gameId) in enumerate(gameImages):
    frame = tk.Canvas(window, width=IMG_SIZE, height=IMG_SIZE)
    l = tk.Label(frame, text=f"Game #{index+1}")
    l.grid()
    b = tk.Button(frame, image=pimg, command=lambda gameId=gameId: on_click(gameId))
    b.image = pimg
    b.grid()
    
    b.command = lambda gameId=gameId: on_click(gameId)
    frame.grid(column=index % NUM_GAMES_PER_ROW, row=index // NUM_GAMES_PER_ROW)


window.mainloop()