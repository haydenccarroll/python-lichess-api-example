import berserk
import dotenv

dotenv_file = dotenv.find_dotenv()
AUTH_TOKEN = dotenv.get_key(dotenv_file, "AUTH_TOKEN")
GAME_ID = dotenv.get_key(dotenv_file, "GAME_ID")
USERNAME = dotenv.get_key(dotenv_file, "USERNAME")

session = berserk.TokenSession(AUTH_TOKEN)
client = berserk.Client(session=session)
game_state = berserk.clients.Board(session).stream_game_state(GAME_ID)

am_i_white = False
is_it_my_turn = False
for x in game_state:
    if x['type'] == 'gameFull': #special api request
        print(x)
        moves = x['state']['moves'].split(' ')
        status = x['state']['status']
        try:
            if x['white']['name'] == USERNAME:
                am_i_white = True
        except KeyError:
            pass
        try:
            if x['state']['wdraw'] == True and not am_i_white:
                print("White offered a draw. Please accept/decline on the app.")
        except KeyError:
            pass
        try:
            if x['state']['bdraw'] == True and am_i_white:
                print("Black offered a draw. Please accept/decline on the app.")
        except KeyError:
            pass

        
    elif x['type'] == 'chatLine': #offers a draw potentially
        if x['room'] == 'player' and x['username'] == 'lichess' and x['text'].endswith("offers a draw"):
            if not is_it_my_turn:
                print("Player offered a draw. Accept/Decline on the app.")

    else: # normal move
        moves = x['moves'].split(' ')
    moves = [x for x in moves if x != '']
    is_it_my_turn = True if ((len(moves) + int(am_i_white)) % 2 == 1) else False
    if len(moves) > 0:
        print("move:", moves[-1])
    print(moves)
    print("status:", status)
    print("Is it my turn:", "Yes" if is_it_my_turn else "No")

    if status == "mate": # mate occured
        if is_it_my_turn:
            print("you lost...")
        else:
            print("you won!!!")
        break
    if status == "resign":
        if (x['winner'] == 'white' and am_i_white) or x['winner'] == 'black' and not am_i_white:
            print("you won!!!")
        else:
            print("you lost...")
    if status == "draw":
        print('you drew')    


    if is_it_my_turn: # it is my turn
        while True:
            move = print("Please enter a move to play: ")
            # try:
            #     berserk.clients.Board(session).make_move(GAME_ID, move)
            # except berserk.exceptions.ResponseError:
            #     print("That move was illegal. try again")
            #     continue
            break
