from src.const import GameConstants as const

PLAYER_STATE_TEMPLATE = {
    const.X_COORD: 0,
    const.Y_COORD: 0,
    const.VELOCITY: 0,
    const.VERTICAL_VELOCITY: 0,
    const.STATE: const.IDLE,
    const.DIRECTION: 1,
    const.MOVE: 0,
    const.JUMP: 0,
    const.DIVE: 0,
    const.FRAME: 0,
    const.LANDING_FRAME: 2,
    const.JUMP_SQUAT_FRAME: 2,
    const.BONKLF: 5,
    const.DSTARTF: 3,
    const.DIVESTR: 20,
    const.DIVELJSTR: -12,
    const.SPEED: 10,
    const.TRACTION: 2,
    const.JUMP_SPEED: -24,
    const.AIR: 12,
    const.DRIFT: 2,
    const.KICKFLIPSTR: -30,
    const.KICKFLIPLIMIT: -18,
}
