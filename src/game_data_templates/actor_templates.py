from src.const import GameConstants as const

MOVING_PLATFORM_TEMPLATE = {
    const.X_COORD: None, # should be set in level editor
    const.Y_COORD: None,
    const.VELOCITY: 0,
    const.VERTICAL_VELOCITY: 0,
    const.DIRECTION: 1,
    const.COUNTER: 0,
    const.PATH: [], # also set in level editor, list of positions
}

def moving_platform_update_function(self):
    if (self.STATE[const.X_COORD], self.state[const.Y_COORD]) == self.STATE[const.PATH][self.STATE[const.COUNTER]]:
        self.STATE[const.COUNTER] = self.STATE[const.COUNTER] 

    X, Y = self.STATE[const.X_COORD], self.state[const.Y_COORD]
    X_, Y_ = self.STATE[const.PATH][self.STATE[const.COUNTER]]
    self.STATE[const.X_COORD] += X_ - X / Y_ - Y
    self.STATE[const.Y_COORD] += Y_ - Y / X_ - X 

