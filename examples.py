from predictor import *
import time

'''
#col-vgk game 3 5/24/26
print("COL @ VGK - West Final Game 3")
print("3rd period start")
print(poisson_predictor("COL", "VGK", 20, 3, 3))
print("Hertl goal 8:21")
print(poisson_predictor("COL", "VGK", 11.6, 3, 4))
print("Howden Goal 19:01")
print(poisson_predictor("COL", "VGK", 1, 3, 5))
'''

'''
#first live test: car-mtl game 3 5/25/26
#bug with tie probability (1-result) & OT
run_live()
print("Fanduel data: ")
car_fd = 162
mtl_fd = 126
print("CAR: " + str((car_fd)/(car_fd+100)))
print("MTL: " + str(100/(mtl_fd+100)))
'''

#car @ vgk scf game 6 6/14/26
game_id = pick_game()
while True:
    run_live(game_id)
    odds = get_odds("CAR", "VGK")
    print("Fanduel data: " )
    print("CAR: " + str(odds[0]))
    print("VGK: " + str(odds[1]))
    time.sleep(180)