def get_current_state(self):
    try:
        logger_payment_state.info(json.dumps(self.state, ensure_ascii=False))
    except:
        logger_payment_state.info(self.state)

    if not isinstance(self.state, dict):
        return {'result':False, 'content': u'Текущее состояние экземпляра не является словарем'}
    if not 'result' in self.state:
        return {'result':False, 'content': u'Текущее состояние экземпляра не содержит ОБЯЗАТЕЛЬНЫЙ признак "result"'}
    return self.state

class Payment(object):
    def __new__(cls, card_typeClass, point_typeClass, params=None):
        if not isinstance(params, dict):
            return {'result':False, 'content': u'Эклемпляр платежа должен быть в формате словаря'}
        if not set(['card_num', 'num_ta', 'summ']) <= set(params.keys()):
            return {'result':False, 'content': u'Эклемпляр платежа должен ОБЯЗАТЕЛЬНО включать номер карты, номер точки продажи, сумму платежа'}

        return type('Payment', (card_typeClass, point_typeClass), {
            'params':params, 'get_current_state':get_current_state, 'get_check_number':get_check_number, 'wd':settings.WD, 'state':{'last_command':'', 'result':False, 'content':'Операция на выполнена', 'data':{}}
            })()

p = Payment(card_typeClass, point_typeClass, request['params'])
