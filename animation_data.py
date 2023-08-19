import utility
import game_object

class Animation_data:
    def __init__(self, path):
        data = utility.read_from_json(path)
        self.keyframes = data["frames"]
        self.intervals = data["times"]
        self.keyframe_list = []
        for i in range(len(self.keyframes)):
            self.keyframe_list.append(game_object.create_keyframe_from_serialized(self.keyframes[i], self.intervals[i]))