
if event.type == KEYDOWN and event.key == K_w:
    up = True
    start = time()
    move = True
if event.type == KEYDOWN and event.key == K_s:
    down = True
    start = time()
    move = True
if event.type == KEYDOWN and event.key == K_a:
    left = True
    start = time()
    move = True
if event.type == KEYDOWN and event.key == K_d:
    right = True
    start = time()
    move = True
if event.type == KEYDOWN and event.key == K_e:
    attack = True
    start = time()
    move = True
if event.type == KEYUP and event.key == K_w:
    up = False
    auto_repeat = False
if event.type == KEYUP and event.key == K_s:
    down = False
    auto_repeat = False
if event.type == KEYUP and event.key == K_a:
    left = False
    auto_repeat = False
if event.type == KEYUP and event.key == K_d:
    right = False
    auto_repeat = False
if event.type == KEYUP and event.key == K_e:
    attack = False
    auto_repeat = False