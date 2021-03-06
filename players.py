from pygame import *
import blocks
import enemies
import pyganim
import pygame_menu
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

MOVE_SPEED_NINJA = 10
MOVE_SPEED_STRIKER = 5
BULLET_SPEED = 8
WIDTH = 32
HEIGHT = 48
WIDTH_BULLET = 20
SHOOT_LENGTH = 100
JUMP_POWER_NINJA = 10
JUMP_POWER_STRIKER = 7
GRAVITY = 0.35
COLOR_NINJA = "#888888"
COLOR_STRIKER = "#FF0000"
COLOR_BULLET = "#424200"
ANIMATION_DELAY = 300
asset_url1 = resource_path('sprites/player/ninja_walk1.png')
asset_url2 = resource_path('sprites/player/ninja_walk2.png')
ANIMATION_NINJA_RIGHT = [(asset_url1),
                        (asset_url2)]
asset_url1 = resource_path('sprites/player/ninja_walk1_left.png')
asset_url2 = resource_path('sprites/player/ninja_walk2_left.png')
ANIMATION_NINJA_LEFT = [(asset_url1),
                        (asset_url2)]
asset_url = resource_path('sprites/player/ninja_jump.png')
ANIMATION_NINJA_JUMP = [(asset_url, 1)]
asset_url = resource_path('sprites/player/ninja_stand.png')
ANIMATION_NINJA_STAY = [(asset_url, 1)]
asset_url = resource_path('sprites/player/ninja_onwall.png')
ANIMATION_NINJA_ONWALL = [(asset_url, 1)]
asset_url = resource_path('sprites/player/ninja_jump_left.png')
ANIMATION_NINJA_JUMP_L = [(asset_url, 1)]
asset_url = resource_path('sprites/player/ninja_onwall_left.png')
ANIMATION_NINJA_ONWALL_L = [(asset_url, 1)]

asset_url = resource_path('sprites/player/striker_stand.png')
ANIMATION_STRIKER_STAY = [(asset_url, 1)]

asset_url1 = resource_path('sprites/player/striker_walk1.png')
asset_url2 = resource_path('sprites/player/striker_walk2.png')
asset_url3 = resource_path('sprites/player/striker_walk3.png')
ANIMATION_STRIKER_RIGHT = [(asset_url1),
            (asset_url2),
            (asset_url3)]
asset_url1 = resource_path('sprites/player/striker_walk1_left.png')
asset_url2 = resource_path('sprites/player/striker_walk2_left.png')
asset_url3 = resource_path('sprites/player/striker_walk3_left.png')
ANIMATION_STRIKER_LEFT = [(asset_url1),
            (asset_url2),
            (asset_url3)]
class Ninja(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onWall = False
        self.onWallOne = False
        self.startX = x
        self.startY = y
        self.flipped = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR_NINJA))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.onGroundArray = [False, False, False, False, False]
        self.reallyOnGround = False
        self.image.set_colorkey(Color(COLOR_NINJA))

        boltAnim = []
        for anim in ANIMATION_NINJA_RIGHT:
           boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in ANIMATION_NINJA_LEFT:
           boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_NINJA_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))


        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_NINJA_JUMP)
        self.boltAnimJump.play()

        self.boltAnimWall= pyganim.PygAnimation(ANIMATION_NINJA_ONWALL)
        self.boltAnimWall.play()

        self.boltAnimJumpL= pyganim.PygAnimation(ANIMATION_NINJA_JUMP_L)
        self.boltAnimJumpL.play()

        self.boltAnimWallL= pyganim.PygAnimation(ANIMATION_NINJA_ONWALL_L)
        self.boltAnimWallL.play()

    def update(self, left, right, up, platforms, entities, bullets, delta, sounds):
        self.onGroundArray.pop(0)
        self.onGroundArray.insert(4, self.onGround)
        self.reallyOnGround = False
        for i in range(0,4):
            if self.onGroundArray[i]:
                self.reallyOnGround = True
        if up:
            if self.onGround or self.onWall:
                self.yvel = -JUMP_POWER_NINJA
                sounds[0].play()
            self.onWall = False
        if left and not self.onWall:
            self.xvel += -MOVE_SPEED_NINJA * delta
            self.flipped = True
            self.image.fill(Color(COLOR_NINJA))
            self.boltAnimLeft.blit(self.image, (0, 0))
        if right and not self.onWall:
            self.xvel += MOVE_SPEED_NINJA * delta
            self.flipped = False
            self.image.fill(Color(COLOR_NINJA))
            self.boltAnimRight.blit(self.image, (0, 0))
        if not(left or right):
            self.xvel = 0
            self.image.fill(Color(COLOR_NINJA))
            self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += GRAVITY
        if not self.reallyOnGround:
            self.image.fill(Color(COLOR_NINJA))
            if self.flipped:
                self.boltAnimJumpL.blit(self.image, (0, 0))
            else:
                self.boltAnimJump.blit(self.image, (0, 0))
        if self.onWall:
            self.yvel = 0
            self.onWallOne = True
            self.image.fill(Color(COLOR_NINJA))
            if self.flipped:
                self.boltAnimWallL.blit(self.image, (0, 0))
            else:
                self.boltAnimWall.blit(self.image, (0, 0))
        if self.onGround:
            self.yvel += GRAVITY
            self.onWallOne = False
        self.onGround = False
        if self.rect.x < 32 or self.rect.y > 5000:
            self.death(sounds)
        if self.xvel > MOVE_SPEED_NINJA:
            self.xvel = MOVE_SPEED_NINJA
        if self.xvel < -MOVE_SPEED_NINJA:
            self.xvel = -MOVE_SPEED_NINJA
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, entities, bullets, sounds)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, entities, bullets, sounds)


    def collide(self, xvel, yvel, platforms, entities, bullets, sounds):
        for b in platforms:
            if sprite.collide_rect(self,b):
                if isinstance(b, blocks.Block):
                    if xvel > 0:
                        self.rect.right = b.rect.left
                        if (not self.onWallOne) and (not self.reallyOnGround):
                            self.onWall = True
                    if xvel < 0:
                        self.rect.left = b.rect.right
                        if (not self.onWallOne) and (not self.reallyOnGround):
                            self.onWall = True
                    if yvel > 0:
                        self.rect.bottom = b.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = b.rect.bottom
                        self.yvel = 0
                if isinstance(b, blocks.DeathBlock) or isinstance(b, enemies.Enemy):
                    self.death(sounds)
                if isinstance(b, Bullet):
                    self.death(sounds)
                    platforms.remove(b)
                    entities.remove(b)
                    bullets.remove(b)
                if isinstance(b, blocks.Teleport_in):
                    for i in platforms:
                        if isinstance(i, blocks.Teleport_out):
                            sounds[1].play()
                            self.teleporting(i.startX,i.startY)
    def death(self,sounds):
        sounds[2].play()
        time.wait(500)
        self.xvel = 0
        self.yvel = 0
        self.teleporting(self.startX, self.startY)


    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY



class Striker(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.startX = x
        self.startY = y
        self.flipped = False
        self.image = Surface((WIDTH,HEIGHT))
        self.image.fill(Color(COLOR_STRIKER))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(Color(COLOR_STRIKER))

        boltAnim = []
        for anim in ANIMATION_STRIKER_RIGHT:
           boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in ANIMATION_STRIKER_LEFT:
           boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STRIKER_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

    def update(self, left, right, up, platforms, delta, sounds):
        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER_STRIKER
        if left:
            self.xvel += -MOVE_SPEED_STRIKER * delta
            self.flipped = True
            self.image.fill(Color(COLOR_STRIKER))
            self.boltAnimLeft.blit(self.image, (0, 0))
        if right:
            self.xvel += MOVE_SPEED_STRIKER * delta
            self.flipped = False
            self.image.fill(Color(COLOR_STRIKER))
            self.boltAnimRight.blit(self.image, (0, 0))
        if not(left or right):
            self.xvel = 0
            self.image.fill(Color(COLOR_STRIKER))
            self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        if self.xvel > MOVE_SPEED_STRIKER:
            self.xvel = MOVE_SPEED_STRIKER
        if self.xvel < -MOVE_SPEED_STRIKER:
            self.xvel = -MOVE_SPEED_STRIKER
        if self.rect.x < 32 or self.rect.y > 5000:
            self.death(sounds)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, sounds)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, sounds)

    def collide(self, xvel, yvel, platforms, sounds):
        for b in platforms:
            if sprite.collide_rect(self,b):
                if isinstance(b, blocks.Block):
                    if xvel > 0:
                        self.rect.right = b.rect.left
                    if xvel < 0:
                        self.rect.left = b.rect.right
                    if yvel > 0:
                        self.rect.bottom = b.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = b.rect.bottom
                        self.yvel = 0
                if isinstance(b, blocks.DeathBlock) or isinstance(b, enemies.Enemy):
                    self.death(sounds)
                if isinstance(b, blocks.Teleport_in):
                    for i in platforms:
                        if isinstance(i, blocks.Teleport_out):
                            sounds[1].play()
                            self.teleporting(i.startX,i.startY)
    def death(self, sounds):
        sounds[2].play()
        time.wait(500)
        self.xvel = 0
        self.yvel = 0
        self.teleporting(self.startX, self.startY)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY


class Bullet(sprite.Sprite):
    def __init__(self, x, y, flipped):
        sprite.Sprite.__init__(self)
        self.xvel = BULLET_SPEED
        self.onGround = False
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH_BULLET,WIDTH_BULLET))
        self.flip = flipped
        if self.flip:
            asset_url = resource_path("sprites/bullet2.png")
            self.image = image.load(asset_url).convert_alpha()
        if not self.flip:
            asset_url = resource_path("sprites/bullet1.png")
            self.image = image.load(asset_url).convert_alpha()
        self.rect = Rect(x, y, WIDTH_BULLET, WIDTH_BULLET)


    def update(self, platforms, entities, monsters, sounds):
        if self.flip:
            self.rect.x -= self.xvel
        if not self.flip:
            self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, entities, monsters, sounds)


    def collide(self, xvel, yvel, platforms, entities, monsters, sounds):
        for b in platforms:
            if sprite.collide_rect(self,b):
                if isinstance(b, enemies.Enemy):
                    sounds[3].play()
                    platforms.remove(b)
                    entities.remove(b)
                    monsters.remove(b)
