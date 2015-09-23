
"""
Whether or not city links should be enabled.

This is used to check if moves are valid.

If True, player moves are checked for validity. This is done using `drac_links.py`
If False, any player can move from any location to any other location.
"""
links = True

"""
The mode to run drac in.

Valid settings are:
    'plays', 'turns', 'interactive', 'networked', 'pygame', 'ai_mode'
    'p',     't',     'i',           'n',         'g'     , 'ai'

    If 'p' or 'plays'         ; drac simply cycles through all moves, printing outcomes.

    If 't' or 'turns'         ; drac enters turn-by-turn mode. A console is available.

    If 'i' or 'interactive'   ; drac enters interactive mode, allowing turns to be entered.

    If 'n' or 'networked'     ; drac enters server-client mode.

    If 'g' or 'pygame'        ; drac uses pygame to provide a visual representation of the game.

    If ai' or 'ai_mode' ; drac enters AI mode, calling ./ai/hunter(_NAME).py and ./ai/dracula.py
                                                             if _NAME is present, use it instead of hunter.py
"""
mode  = 'p'

"""
Whether the current user is the client or the server.

If True, drac acts a client and connects to IP specified below.
If False, drac acts as a server and handles connections to the port below.
"""
networked_i_am_client = True

"""
The server IP to connect to when running in client mode.
"""
networked_server_ip   = '0.0.0.0'

"""
The server port to connect to when running in client mode.
AND
The port to listen on when running in server mode.
"""
networked_server_port = 36666