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

    @staticmethod
    def none_checker(param_list):
        if None in param_list:
            raise NoneKeywordException


class ActionState(State):
    """queue管理用のstate

    """
    def __init__(self, user_id, cloth_type, img_path, processing, action):
        State.__init__(self, user_id)
        param_list = [user_id, cloth_type, img_path, processing, action]
        ActionState.none_checker(param_list)
        self.user_id = user_id
        self.cloth_type = cloth_type
        self.img_path = img_path
        self.processing = processing
        self.action = action

    def to_dict(self):
        return {u'user_id': self.user_id,
                u'cloth_type': self.cloth_type,
                u'img_path': self.img_path,
                u'processing': self.processing,
                u'action': self.action}


class ResultState(State):
    """push_message用のstate

    """
    def __init__(self, user_id, message, error_type):
        State.__init__(self, user_id)
        param_list = [user_id, message, error_type]
        ResultState.none_checker(param_list)
        self.user_id = user_id
        self.message = message
        self.error_type = error_type

    def to_dict(self):
        return {u'user_id': self.user_id,
                u'message': self.message,
                u'error_type': self.error_type}


class NoneKeywordException(Exception):
    pass
