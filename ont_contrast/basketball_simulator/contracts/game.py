from boa.interop.System.Runtime import *
from boa.interop.System.Storage import *
from boa.builtins import *

# -------------------------------------------
# GAME SETTINGS
# -------------------------------------------
denominator = 100

west_sf_name = "James"
west_pf_name = "Durant"
west_c_name = "Davis"
west_pg_name = "Curry"
west_sg_name = "Harden"

west_sf_off_skill = 95
west_pf_off_skill = 92
west_c_off_skill = 88
west_pg_off_skill = 90
west_sg_off_skill = 90

west_sf_def_skill = 88
west_pf_def_skill = 88
west_c_def_skill = 90
west_pg_def_skill = 78
west_sg_def_skill = 80

east_sf_name = "Leonard"
east_pf_name = "Antetokounmpo"
east_c_name = "Embiid"
east_pg_name = "Wall"
east_sg_name = "Oladipo"

east_sf_off_skill = 97
east_pf_off_skill = 88
east_c_off_skill = 88
east_pg_off_skill = 92
east_sg_off_skill = 90

east_sf_def_skill = 93
east_pf_def_skill = 94
east_c_def_skill = 89
east_pg_def_skill = 88
east_sg_def_skill = 88

ctx = GetContext()


def main(op, args):
    if op is 'init':
        return init(args[0])

    if op is 'next_round':
        return next_round(args[0])

    if op is 'get_scores':
        return get_scores()

    if op is 'random_int_from_zero':
        return random_int_from_zero(args[0], args[1])

    if op is 'shoot':
        shoot(args[0], args[1], args[2], args[3])
        return True

    if op is 'pass_ball':
        pass_ball(args[0], args[1], args[2])
        return True

    if op is 'pick_ball_holder':
        pick_ball_holder(args[0], args[1])
        return True

    if op is 'jump_ball':
        jump_ball()
        return True

    if op is 'rand_player':
        return rand_player(args[0])

    if op is 'get_team_scores':
        return get_team_scores()

    if op is 'get_curr_time':
        return get_curr_time()

    return False


def init(seed):
    """
    init the game
    :return:
    """
    Put(ctx, 'seed', seed)
    Put(ctx, 'time', 180)
    Put(ctx, 'west_score', 0)
    Put(ctx, 'east_score', 0)

    # 体能可以影响球员状态
    # Put(ctx, concat(west_sf_name, '_stamina'), 100)
    # Put(ctx, concat(west_pf_name, '_stamina'), 100)
    # Put(ctx, concat(west_c_name, '_stamina'), 100)
    # Put(ctx, concat(west_pg_name, '_stamina'), 100)
    # Put(ctx, concat(west_sg_name, '_stamina'), 100)
    #
    # Put(ctx, concat(east_sf_name, '_stamina'), 100)
    # Put(ctx, concat(east_pf_name, '_stamina'), 100)
    # Put(ctx, concat(east_c_name, '_stamina'), 100)
    # Put(ctx, concat(east_pg_name, '_stamina'), 100)
    # Put(ctx, concat(east_sg_name, '_stamina'), 100)

    Put(ctx, concat(west_sf_name, '_off_skill'), west_sf_off_skill)
    Put(ctx, concat(west_pf_name, '_off_skill'), west_pf_off_skill)
    Put(ctx, concat(west_c_name, '_off_skill'), west_c_off_skill)
    Put(ctx, concat(west_pg_name, '_off_skill'), west_pg_off_skill)
    Put(ctx, concat(west_sg_name, '_off_skill'), west_sg_off_skill)

    Put(ctx, concat(east_sf_name, '_off_skill'), east_sf_off_skill)
    Put(ctx, concat(east_pf_name, '_off_skill'), east_pf_off_skill)
    Put(ctx, concat(east_c_name, '_off_skill'), east_c_off_skill)
    Put(ctx, concat(east_pg_name, '_off_skill'), east_pg_off_skill)
    Put(ctx, concat(east_sg_name, '_off_skill'), east_sg_off_skill)

    Put(ctx, concat(west_sf_name, '_def_skill'), west_sf_def_skill)
    Put(ctx, concat(west_pf_name, '_def_skill'), west_pf_def_skill)
    Put(ctx, concat(west_c_name, '_def_skill'), west_c_def_skill)
    Put(ctx, concat(west_pg_name, '_def_skill'), west_pg_def_skill)
    Put(ctx, concat(west_sg_name, '_def_skill'), west_sg_def_skill)

    Put(ctx, concat(east_sf_name, '_def_skill'), east_sf_def_skill)
    Put(ctx, concat(east_pf_name, '_def_skill'), east_pf_def_skill)
    Put(ctx, concat(east_c_name, '_def_skill'), east_c_def_skill)
    Put(ctx, concat(east_pg_name, '_def_skill'), east_pg_def_skill)
    Put(ctx, concat(east_sg_name, '_def_skill'), east_sg_def_skill)

    # 人盯人防守，后面可以加上挡拆后换人之类复杂的逻辑
    Put(ctx, concat(west_sf_name, '_def'), east_sf_name)
    Put(ctx, concat(west_pf_name, '_def'), east_pf_name)
    Put(ctx, concat(west_c_name, '_def'), east_c_name)
    Put(ctx, concat(west_pg_name, '_def'), east_pg_name)
    Put(ctx, concat(west_sg_name, '_def'), east_sg_name)

    Put(ctx, concat(east_sf_name, '_def'), west_sf_name)
    Put(ctx, concat(east_pf_name, '_def'), west_pf_name)
    Put(ctx, concat(east_c_name, '_def'), west_c_name)
    Put(ctx, concat(east_pg_name, '_def'), west_pg_name)
    Put(ctx, concat(east_sg_name, '_def'), west_sg_name)

    # 数据, for now just score
    Put(ctx, concat(west_sf_name, '_score'), 0)
    Put(ctx, concat(west_pf_name, '_score'), 0)
    Put(ctx, concat(west_c_name, '_score'), 0)
    Put(ctx, concat(west_pg_name, '_score'), 0)
    Put(ctx, concat(west_sg_name, '_score'), 0)

    Put(ctx, 'has_ball', None)

    Notify('game start')
    return True


def next_round(seed):
    """
    每次都涉及交换球权，重置24秒; 每4-8秒做一次选择：进攻，传球；时间不足则强制进攻
    :return:
    """
    Put(ctx, 'seed', seed)
    jump_ball() # 2 events
    time_per_round = 24
    team = Get(ctx, 'has_ball')

    while time_per_round > 0: # 可多次传球，投篮只有一次
        holder = Get(ctx, 'ball_holder')
        curr_time = Get(ctx, 'time')
        rand = random_int_from_zero(5, seed) + 4
        time_per_round -= rand

        if time_per_round < 0:
            curr_time -= time_per_round + rand
        else:
            curr_time -= rand

        if curr_time <= 0:
            Notify('end')
            Delete(ctx, 'has_ball')
            break

        Put(ctx, 'time', curr_time)
        def_player = Get(ctx, concat(holder, '_def'))
        if time_per_round <= 0:
            shoot(holder, def_player, time_per_round, team)
            break
        else:
            choice = random_int_from_zero(2, seed)
            if choice == 0:
                shoot(holder, def_player, time_per_round, team)
                break
            else:
                pass_ball(holder, def_player, team)

    if team == 'west':
        team = 'east'
    else:
        team = 'west'
    Put(ctx, 'has_ball', team)
    Notify(concat('Now is ', team))
    pick_ball_holder(team, False)


def shoot(off_player, def_player, seconds, team):
    off_skill = Get(ctx, concat(off_player, '_off_skill'))
    def_skill = Get(ctx, concat(def_player, '_def_skill'))
    limit = random_int_from_zero(80, Get(ctx, 'seed'))
    point = random_int_from_zero(2, Get(ctx, 'seed')) + 2

    def_rate = random_int_from_zero(20, Get(ctx, 'seed')) + 40
    hit_rate = off_skill - int((def_skill * def_rate) / denominator)
    curr_time = Get(ctx, 'time')
    if hit_rate >= limit:
        score = Get(ctx, concat(off_player, '_score'))
        score += point
        Put(ctx, concat(off_player, '_score'), score)

        team_score = Get(ctx, concat(team, '_score'))
        team_score += point
        Put(ctx, concat(team, '_score'), team_score)

        if seconds > 3:
            if point == 3:
                Notify(concat(concat(off_player, ' get the 3-point shot '), concat(def_player, ' can\'t stop him')))
            else:
                Notify(concat(off_player, ' make the shot'))
        else:
            if curr_time >= 10:
                Notify(concat("OMG!!! Countdown Shot by ", off_player))
            else:
                Notify(concat(concat("He got it!!!! ", off_player), '\'s shot!'))
    else:
        if hit_rate < 60:
            Notify(concat(concat(off_player, ' shoot and '), concat('Great D by ', def_player)))
        else:
            Notify(concat(def_player, ' stop him'))


def pass_ball(holder, def_player, team):
    rand = random_int_from_zero(5, Get(ctx, 'seed'))
    if team == 'west':
        if rand == 0:
            next_player = west_sf_name
        elif rand == 1:
            next_player = west_pf_name
        elif rand == 2:
            next_player = west_c_name
        elif rand == 3:
            next_player = west_pg_name
        else:
            next_player = west_sg_name
    else:
        if rand == 0:
            next_player = east_sf_name
        elif rand == 1:
            next_player = east_pf_name
        elif rand == 2:
            next_player = east_c_name
        elif rand == 3:
            next_player = east_pg_name
        else:
            next_player = east_sg_name

    if next_player == holder:
        pick = random_int_from_zero(3, Get(ctx, 'seed'))
        if pick == 0:
            Notify(concat(holder, ' dribble and organize the attack'))
        elif pick == 1:
            Notify(concat(holder, ' Fancy dribble! Show TIME'))
        else:
            Notify(concat(concat('Great D by ', def_player), concat(' almost lose the ball ', holder)))
    else:
        Notify(concat(concat(holder, ' pass to '), next_player))
        Put(ctx, 'ball_holder', next_player)


def get_scores():
    return [[Get(ctx, concat(west_sf_name, '_score')), Get(ctx, concat(west_pf_name, '_score')),
             Get(ctx, concat(west_c_name, '_score')), Get(ctx, concat(west_pg_name, '_score')),
             Get(ctx, concat(west_sg_name, '_score'))],
            [Get(ctx, concat(east_sf_name, '_score')), Get(ctx, concat(east_pf_name, '_score')),
             Get(ctx, concat(east_c_name, '_score')), Get(ctx, concat(east_pg_name, '_score')),
             Get(ctx, concat(east_sg_name, '_score'))]]


def get_curr_time():
    return Get(ctx, 'time')


def get_team_scores():
    ws = Get(ctx, 'west_score')
    es = Get(ctx, 'east_score')
    return [ws, es]


def pick_ball_holder(team, is_first):
    player = rand_player(team)
    Put(ctx, 'ball_holder', player)
    if is_first:
        Notify(concat(player, ' holding the ball and pushing'))
    else:
        Notify(concat(player, ' get the ball'))


def jump_ball():
    if Get(ctx, 'has_ball') is not None:
        return False
    res = random_int_from_zero(2, Get(ctx, 'seed'))
    if res == 1:
        team = 'west'
        Put(ctx, 'has_ball', team)
    else:
        team = 'east'
        Put(ctx, 'has_ball', team)
    Notify(concat("JUMP BALL!! Game start and ", concat(team, " get the ball")))
    pick_ball_holder(team, True)
    return team


def rand_player(team):
    rand = random_int_from_zero(5, Get(ctx, 'seed'))

    if team == 'west':
        if rand == 0:
            return west_sf_name
        elif rand == 1:
            return west_pf_name
        elif rand == 2:
            return west_c_name
        elif rand == 3:
            return west_pg_name
        else:
            return west_sg_name
    else:
        if rand == 0:
            return east_sf_name
        elif rand == 1:
            return east_pf_name
        elif rand == 2:
            return east_c_name
        elif rand == 3:
            return east_pg_name
        else:
            return east_sg_name


def random_int_from_zero(num, seed):
    """
    my code is so ugly...
    the fake random number generator
    the return number is including in [0, num)
    :param seed:
    :param num:
    :return:
    """
    # time = GetTime()
    val = seed
    h = val # hash(val)
    # seed = GetTime() % 100
    rand = h % num # 先不用hash了，貌似有点问题
    return rand