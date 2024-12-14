from data import *
import requests
import hashlib
import base64
import json


def params_to_dict(params: str) -> dict:
    params = params.split('&')
    params_dict = {}
    for param in params:
        param = param.split('=')
        params_dict[param[0]] = param[1]
    return params_dict


class Payment:
    def __init__(self, pid: str='', key: str='', default_paytype: str = 'alipay'):
        '''
        pid: 商户ID
        key: 商户密钥
        default_paytype: 默认支付方式，默认为支付宝
        '''
        self.pid = pid
        self.key = key
        self.default_paytype = default_paytype
        self.return_url = ''
        self.notify_url = ''
        self.default_api = PayAPI('', '', '')
    
    @property
    def everyth_set_ok(self) -> bool:
        return self.pid != '' and self.key != '' and self.default_paytype in ['alipay', 'wxpay'] and self.return_url != '' and self.notify_url != ''
    
    def load(self, data: BasicParams):
        self.pid = data.pid
        self.key = data.key
        self.default_paytype = data.default_paytype
        self.set_return_url(data.return_url, data.return_with_base64)
        self.set_notify_url(data.notify_url, data.notify_with_base64)
        return self
    
    def set_api(self, api: PayAPI):
        self.default_api = api
        return self

    def set_return_url(self, return_url: str, with_base64: bool = False):
        self.return_url = return_url.split('?')[0]
        if with_base64:
            self.return_url += '/{data}' if not return_url.endswith('/') else '{data}'
        
    def set_notify_url(self, notify_url: str, with_base64: bool = False):
        self.notify_url = notify_url.split('?')[0]
        if with_base64:
            self.notify_url += '/{data}' if not notify_url.endswith('/') else '{data}'
    
    def base64(self, url:str, data:dict, with_params:bool=False) -> str:
        basedata = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')
        if '{data}' in url:
            return url.format(data=basedata)
        if with_params:
            return url + '?data=' + basedata
        return url

    def sign(self, data: PayParams|PayAPIParams) -> SignResult:
        '''
        对参数进行签名
        '''
        # 将数据进行排序并构建待签名字符串
        if not self.everyth_set_ok:
            raise Exception('Basic 参数不完整')
        # 检查参数
        params = {k: v for k, v in data.__dict__.items() if v is not None and v.strip() != ''}
        params.pop('sign', None)
        params.pop('sign_type', None)
        params.pop('pid', None)
        params['pid'] = self.pid
        if params.get('type', '') not in ['alipay', 'wxpay']:
            params['type'] = self.default_paytype
        # 设置回调地址
        params['return_url'] = self.base64(self.return_url, params)
        params['notify_url'] = self.base64(self.notify_url, params)
        # 对参数进行排序，生成待签名字符串
        sorted_params = sorted(params.items())
        url_string = '&'.join([f"{k}={v}" for k, v in sorted_params])
        sign_string = url_string + self.key  # 添加商户密钥
        sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest().lower()
        final = url_string + '&sign=' + sign  # 添加签名
        final = final + '&sign_type=MD5'  # 添加签名类型
        return SignResult(sign=sign, sign_type='MD5', urlparams=final)
    
    def pay_redirect(self, info:PayParams) -> str:
        '''
        生成支付跳转链接
        '''
        sign = self.sign(info)
        url = self.default_api.direct_url + '?' + sign.urlparams
        return url
    
    def pay_api(self, info:PayAPIParams) -> PayResult:
        '''
        调用支付接口
        '''
        data = params_to_dict(self.sign(info))
        response = requests.post(self.default_api.request_url, data=data)
        result = PayResult(**response.json())
        return result
    
    def query_order(self, out_trade_no: str=None) -> QueryResult:
        '''
        查询订单
        '''
        params = {
            'act': 'order',
            'pid': self.pid,
            'key': self.key,
        }
        if out_trade_no is not None:
            params['out_trade_no'] = out_trade_no
        response = requests.get(self.default_api.action_url, params=params)
        result = QueryResult(**response.json())
        return result
    
    def refund(self, trade_no: str) -> RefundResult:
        '''
        退款
        '''
        info = self.query_order(trade_no)
        if info.status == 'error':
            return info
        data = {
            'pid': self.pid,
            'key': self.key,
            'trade_no': trade_no,
            'money': info.money,
        }
        response = requests.post(self.default_api.action_url, data=data, params={
            'act': 'refund'
        })
        return RefundResult(**response.json())
    

DefultPayAPI = PayAPI(
    direct_url='https://z-pay.cn/submit.php',
    request_url='https://zpayz.cn/mapi.php',
    action_url='https://z-pay.cn/api.php'
)


test = Payment('2024121412492711', '7IUnBovq3tfraXCppZH0RkFEiqrdUMKm')
test.set_notify_url('https://api.z-pay.cn/api/callback')
test.set_return_url('https://z-pay.cn')
test.set_api(DefultPayAPI)

print(test.refund('1E8cX2lcWonV9S5E0vwv'))