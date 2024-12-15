from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PayAPI:
    direct_url: str  = field(metadata={"required": True, "description": "跳转支付API"})
    request_url: str = field(metadata={"required": True, "description": "接口支付API"})
    action_url: str = field(metadata={"required": True, "description": "接口操作API"})


@dataclass
class BasicParams:
    pid: str = field(metadata={"required": True, "description": "商户ID"})
    key: str = field(metadata={"required": True, "description": "商户密钥"})
    return_url: str = field(metadata={"required": True, "description": "回调地址，用于接收支付结果通知"})
    notify_url: str = field(metadata={"required": True, "description": "回调地址，用于接收支付结果通知"})
    default_paytype: str = field(metadata={"required": True, "description": "默认支付方式"})
    return_with_base64: bool = field(default=False, metadata={"required": False, "description": "是否返回带base64数据编码的url参数"})
    notify_with_base64: bool = field(default=False, metadata={"required": False, "description": "是否返回带base64数据编码的url参数"})


@dataclass
class PayParams:
    name: str = field(metadata={"required": True, "description": "商品名称，不超过100字"})
    money: str = field(metadata={"required": True, "description": "订单金额，最多保留两位小数"})
    type: str = field(metadata={"required": True, "description": "支付方式：alipay 或 wxpay"})
    out_trade_no: str = field(metadata={"required": True, "description": "订单编号，每个商品不可重复"})
    cid: Optional[str] = field(default='', metadata={"required": False, "description": "支付渠道ID，如果不填则随机使用某一支付渠道"})
    param: Optional[str] = field(default='', metadata={"required": False, "description": "附加内容，会通过notify_url原样返回"})


@dataclass
class PayAPIParams:
    name: str = field(metadata={"required": True, "description": "商品名称，不超过100字"})
    money: str = field(metadata={"required": True, "description": "订单金额，最多保留两位小数"})
    type: str = field(metadata={"required": True, "description": "支付方式：alipay 或 wxpay"})
    out_trade_no: str = field(metadata={"required": True, "description": "订单编号，每个商品不可重复"})
    clientip: str = field(metadata={"required": True, "description": "客户端IP"})
    device: str = field(default='pc', metadata={"required": False, "description": "客户端设备类型，pc或mobile"})
    cid: Optional[str] = field(default='', metadata={"required": False, "description": "支付渠道ID，如果不填则随机使用某一支付渠道"})
    param: Optional[str] = field(default='', metadata={"required": False, "description": "附加内容，会通过notify_url原样返回"})
    

@dataclass
class PayResult:
    code: int = field(metadata={"required": True, "description": "状态码"})
    msg: str = field(metadata={"required": True, "description": "状态信息"})
    trade_no: str = field(default='', metadata={"required": False, "description": "订单编号"})
    O_id: str = field(default='', metadata={"required": False, "description": "商户订单号"})
    payurl: str = field(default='', metadata={"required": False, "description": "支付链接"})
    payurl2: str = field(default='', metadata={"required": False, "description": "支付链接"})
    qrcode: str = field(default='', metadata={"required": False, "description": "二维码链接"})
    img: str = field(default='', metadata={"required": False, "description": "二维码图片"})


@dataclass
class SignResult:
    sign: str = field(metadata={"required": True, "description": "签名结果"})
    sign_type: str = field(metadata={"required": True, "description": "签名类型"})
    urlparams: str = field(metadata={"required": True, "description": "签名后的参数"})


@dataclass
class QueryResult:
    code: int = field(metadata={"required": True, "description": "状态码"})
    msg: str = field(metadata={"required": True, "description": "状态信息"})
    trade_no: str = field(default='', metadata={"required": False, "description": "易支付订单号"})
    out_trade_no: str = field(default='', metadata={"required": False, "description": "商户订单号"})
    type: str = field(default='', metadata={"required": False, "description": "支付方式"})
    pid: str = field(default='', metadata={"required": False, "description": "商户ID"})
    addtime: str = field(default='', metadata={"required": False, "description": "创建订单时间"})
    endtime: str = field(default='', metadata={"required": False, "description": "完成交易时间"})
    name: str = field(default='', metadata={"required": False, "description": "商品名称"})
    money: str = field(default='', metadata={"required": False, "description": "商品金额"})
    status: int = field(default='', metadata={"required": False, "description": "支付状态"})
    param: str = field(default='', metadata={"required": False, "description": "业务扩展参数"})
    buyer: str = field(default='', metadata={"required": False, "description": "支付者账号"})
    

@dataclass
class RefundResult:
    code: int = field(metadata={"required": True, "description": "状态码"})
    msg: str = field(metadata={"required": True, "description": "状态信息"})