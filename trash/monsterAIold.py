else:
    if self.tick == 4:
        self.tick = 0
        vision = self.vision

        diff_x = player.x - self.x
        diff_y = player.y - self.y
        d_x_zo = int(diff_x == 0)
        d_y_zo = int(diff_y == 0)
        toward_p_x = diff_x if diff_x == 0 else diff_x / abs(diff_x)
        toward_p_y = diff_y if diff_y == 0 else diff_y / abs(diff_y)
        further_x = int(0 <= (abs(diff_x) - abs(diff_y)))
        further_y = int(0 <= (abs(diff_y) - abs(diff_x)))
        sees_p_x = int(0 <= (vision - abs(diff_x)))
        sees_p_y = int(0 <= (vision - abs(diff_y)))
        atck_p_x = d_x_zo * int((diff_x * self.dirn_x) >= 0) * sees_p_x
        atck_p_y = d_y_zo * int((diff_y * self.dirn_y) >= 0) * sees_p_y

        if (atck_p_x or atck_p_y) and self.proj_count > 0:
            self.shoot_projectile('Arrow', all_sprite, projectiles,
                                  one_square)
        elif sees_p_x or sees_p_y:
            self.movx = one_square * further_x * toward_p_x
            self.movy = one_square * further_y * toward_p_y
        else:
            self.movx = one_square * random.randint(-1, 1)
            self.movy = one_square * random.randint(-1, 1)

        # if self.movy and self.movx:
        #     rand = random.randint(0, 1)
        #     self.movx *= rand
        #     self.movy *= abs(rand - 1)

        if self.movx:
            self.dirn_x = self.movx / abs(self.movx)
        if self.movy:
            self.dirn_y = self.movy / abs(self.movy)

        self.rect.right += self.movx
        self.collide(self.movx, 0, world)
        self.rect.top += self.movy
        self.collide(0, self.movy, world)

        self.x, self.y = self.rect.topleft
        self.contact = False

self.tick += 1