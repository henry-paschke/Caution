import game_object

class Keyframe_animation:
    def __init__(self, object, serialized_list, interval):
        self.object = object
        self.keyframe_list = []
        for e in serialized_list:
            self.keyframe_list.append(game_object.create_keyframe_from_serialized(e, interval))
        self.elapsed = 0
        self.frame = 0
        object.set_keyframe(self.keyframe_list[self.frame])


    def update(self, elapsed):
        self.elapsed += elapsed
        if self.elapsed > self.keyframe_list[self.frame][0].time:
            self.frame += 1
            self.elapsed = 0
            if (self.frame >= len(self.keyframe_list)):
                self.frame = 0
            self.object.set_keyframe(self.keyframe_list[self.frame])
