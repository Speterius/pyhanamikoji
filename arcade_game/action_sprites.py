import arcade


class ActionSprite(arcade.Sprite):

    actions_path = 'C:\\Users\\PSere\\Desktop\\hanamikoji_game_assets\\actions\\'

    HIGHLIGHT_COLOR = arcade.color.WHITE
    HIGHLIGHT_WIDTH = 2
    SCALE = 0.2

    def __init__(self, action: str, center_x: float, center_y: float, action_function):
        arcade.Sprite.__init__(self, filename=self.actions_path+action+'.png',
                               center_x=center_x, center_y=center_y, scale=self.SCALE)

        # These booleans control clickability, texture display and selection:
        self._enabled: bool = False
        self._used: bool = False
        self.pressed: bool = False
        self.selected: bool = False

        # These are the disabled and flipped textures: KEEP ORDER
        self.append_texture(arcade.load_texture(file_name=self.actions_path+action+'_disabled.png', scale=self.SCALE))
        self.append_texture(arcade.load_texture(file_name=self.actions_path+action+'_used.png', scale=self.SCALE))

        self.action_function = action_function
        self.enabled = True

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        self.set_texture(int(not value))

    @property
    def used(self):
        return self._used

    @used.setter
    def used(self, value: bool):
        self._used = value

        if self._used:
            self.set_texture(2)
        else:
            self.set_texture(int(not self.enabled))

    def is_click_inside(self, x, y):
        if x > self.right:
            return False
        if x < self.left:
            return False
        if y > self.top:
            return False
        if y < self.bottom:
            return False
        return True

    def mouse_press(self, x, y):
        if self.is_click_inside(x, y) and self.enabled:
            self.pressed = True

    def mouse_release(self):
        if self.pressed:
            self.pressed = False
            self.selected = not self.selected
            self.action_function()

    def draw(self):
        super().draw()

        if self.selected:
            arcade.draw_lrtb_rectangle_outline(self.left, self.right, self.top, self.bottom,
                                               color=self.HIGHLIGHT_COLOR, border_width=self.HIGHLIGHT_WIDTH)


class ActionSpriteManager:

    action_library = ('secret', 'burn', 'gift', 'comp')

    ACTION_HEIGHT = 60
    ACTION_SPACING = 120

    def __init__(self, parent_window: arcade.Window):
        self.parent_window = parent_window
        self.actions = {'p1': [], 'p2': []}
        self.action_indeces = {}
        N = len(self.action_library)
        for idx, a in enumerate(self.action_library):
            self.actions['p1'].append(ActionSprite(action=a, action_function=self.foo,
                                                   center_x=self.parent_window.width/2 + (idx - (N-1)/2)
                                                            * self.ACTION_SPACING,
                                                   center_y=self.ACTION_HEIGHT))

            self.actions['p2'].append(ActionSprite(action=a, action_function=self.foo,
                                                   center_x=self.parent_window.width/2 + (idx - (N-1)/2)
                                                            * self.ACTION_SPACING,
                                                   center_y=self.parent_window.height - self.ACTION_HEIGHT))

            self.action_indeces[idx] = a

        self.p1_used = []
        self.p2_used = []

    def update_usage(self):

        for idx, act_sprite in enumerate(self.player_actions()):
            if self.action_indeces[idx] in self.p1_used:
                act_sprite.used = True

        for idx, act_sprite in enumerate(self.opponent_actions()):
            if self.action_indeces[idx] in self.p2_used:
                act_sprite.used = True

    def p1_use_action(self, act_str: str):
        self.p1_used.append(act_str)

    def p2_use_action(self, act_str: str):
        self.p2_used.append(act_str)

    def player_actions(self):
        for act in self.actions['p1']:
            yield act

    def opponent_actions(self):
        for act in self.actions['p2']:
            yield act

    def foo(self):
        pass

    def get_selected_actions(self):
        return [act for act in self.actions['p1'] if act.selected]

    def all_actions(self):
        for k, v in self.actions.items():
            for action in v:
                yield action

    def draw(self):
        for action in self.all_actions():
            action.draw()

    def mouse_press(self, x, y):
        for c in self.all_actions():
            c.mouse_press(x, y)

    def mouse_release(self):
        for c in self.all_actions():
            c.mouse_release()
