# coding=utf-8


class State:
    def __init__(self, user_id):
        pass
    # 抽象メソッド書きたかった.....
    # def to_dict(self):
    #     return
    #
    # def to_json(self):
    #     return
    processing_state = {'done': 'done',
                        'empty': 'empty',
                        'busy': 'busy'
                        }


class ActionState(State):
    """queue管理用のstate

    """
    def __init__(self, user_id, cloth_type, img_path, processing, next_action):
        State.__init__(self, user_id)
        self.user_id = user_id
        self.cloth_type = cloth_type
        self.img_path = img_path
        self.processing = processing
        self.next_action = next_action

    def to_dict(self):
        return {'user_id': self.user_id,
                'cloth_type': self.cloth_type,
                'img_path': self.img_path,
                'processing': self.processing,
                "next_action": self.next_action}


class ResultState(State):
    """push_message用のstate

    """
    def __init__(self, user_id, message, error_type):
        State.__init__(self, user_id)
        self.user_id = user_id
        self.message = message
        self.error_type = error_type

    def to_dict(self):
        return {'user_id': self.user_id, 'message': self.message, 'error_type': self.error_type}
