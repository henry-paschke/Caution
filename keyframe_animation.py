import game_object_editor
import utility
import copy

class Keyframe_animation:
    def __init__(self, object, serialized_list, intervals):
        self.object = object
        self.keyframe_list = []
        for i in range(len(serialized_list)):
            self.keyframe_list.append(game_object_editor.create_keyframe_from_serialized(serialized_list[i], intervals[i]))
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

    def change_animation(self, id_number, serialized_data, interval):
        self.keyframe_list[id_number] = game_object_editor.create_keyframe_from_serialized(serialized_data, interval)
    
    def add_frame(self, serialized_data, length):
        self.keyframe_list.append(game_object_editor.create_keyframe_from_serialized(serialized_data, length))

    def reset_keyframe_list(self, keyframe_list, intervals):
        self.keyframe_list.clear()
        for i in range(len(keyframe_list)):
            self.keyframe_list.append(game_object_editor.create_keyframe_from_serialized(keyframe_list[i], intervals[i]))
    
    def switch_animation(self, animation_data):
        self.keyframe_list = animation_data.keyframe_list
        self.frame = 0
        self.elapsed = 0
        self.object.set_keyframe(self.keyframe_list[self.frame])


def create_animation(fp, go):
    data = utility.read_from_json(fp)
    keyframes = data["frames"]
    intervals = data["times"]

    go.read_serialized_data(keyframes[0])

    return Keyframe_animation(go, keyframes, intervals)