from flask import Flask, request, jsonify
import api
import time
from user_agent import *
from dataclasses import asdict

payment = api.Payment.load(api.BasicParams(
        pid='2024121412492711',
        key='7IUnBovq3tfraXCppZH0RkFEiqrdUMKm',
        notify_url='https://api.z-pay.cn/api/callback',
        return_url='https://z-pay.cn',
        default_paytype='wxpay'
    )).set_api(api.PayAPI(
        direct_url='https://z-pay.cn/submit.php',
        request_url='https://zpayz.cn/mapi.php',
        action_url='https://z-pay.cn/api.php'
    ))

app = Flask(__name__)


@app.route('/api/payment/pay_redirect')
def pay_redirect():
    ua = UserAgent(request.headers.get('User-Agent'))
    data = payment.pay_redirect(api.PayParams(
        name = 'PaymentTest',
        money = '0.01',
        type = 'wxpay',
        out_trade_no = str(time.time()).replace('.', '')
    ))
    return jsonify({
        'url': data,
        'info': {
            'os': ua.os,
            'device': ua.device,
            'browser': ua.browser,
            'hash': ua.hashinfo
        }
    })


@app.route('/api/payment/pay_api')
def pay_api():
    ua = UserAgent(request.headers.get('User-Agent'))
    data = payment.pay_api(api.PayAPIParams(
        name='Test',
        money='5.05',
        type='wxpay',
        out_trade_no=str(time.time()).replace('.', ''),
        clientip=request.remote_addr,
        device=ua.device
    ))
    return jsonify({
        'url': asdict(data),
        'info': {
            'os': ua.os,
            'device': ua.device,
            'browser': ua.browser,
            'hash': ua.hashinfo
        }
    })


app.run(host='0.0.0.0', port=1030, debug=True)