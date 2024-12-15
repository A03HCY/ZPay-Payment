from dataclasses import dataclass
import re
import hashlib

def browser_info(user_agent):
    # 定义正则表达式模式，包括更多浏览器
    browser_patterns = {
        'Chrome': r'Chrome/([\d\.]+)',
        'Firefox': r'Firefox/([\d\.]+)',
        'Safari': r'Version/([\d\.]+).*Safari',
        'Edge': r'Edg/([\d\.]+)|Edge/([\d\.]+)',
        'Opera': r'Opera/([\d\.]+)|OPR/([\d\.]+)',
        'Internet Explorer': r'MSIE ([\d\.]+)|Trident.*rv:([\d\.]+)',
        'Samsung Internet': r'SamsungBrowser/([\d\.]+)',
        'Vivaldi': r'Vivaldi/([\d\.]+)',
        'Brave': r'Brave/([\d\.]+)',
        'UC Browser': r'UCWEB/([\d\.]+)',
        'QQ Browser': r'QQ/([\d\.]+)',
        'Puffin': r'Puffin/([\d\.]+)',
        'Yandex Browser': r'YaBrowser/([\d\.]+)',
        'Konqueror': r'Konqueror/([\d\.]+)',
        'Netscape': r'Netscape/([\d\.]+)',
        'Flock': r'Flock/([\d\.]+)',
        'Maxthon': r'Maxthon/([\d\.]+)',
        'SeaMonkey': r'SeaMonkey/([\d\.]+)',
        'Iceweasel': r'Iceweasel/([\d\.]+)',
        'Midori': r'Midori/([\d\.]+)',
        'Pale Moon': r'PaleMoon/([\d\.]+)',
        'Epic': r'Epic/([\d\.]+)',
        'Tizen Browser': r'Tizen/([\d\.]+)'
    }

    for browser, pattern in browser_patterns.items():
        match = re.search(pattern, user_agent)
        if match:
            version = match.group(1) if match.group(1) else match.group(2) if len(match.groups()) > 1 else ''
            return f"{browser} {version}"
    
    return "Unknown Browser"

def os_info(user_agent):
    os_patterns = {
        'Windows': r'Windows NT ([\d\.]+)',
        'Mac OS': r'Macintosh; Intel Mac OS X ([\d_]+)',
        'Linux': r'Linux',
        'Ubuntu': r'Ubuntu',
        'Android': r'Android ([\d\.]+)',
        'iOS': r'iPhone OS ([\d_]+)',
        'iPad': r'iPad; CPU OS ([\d_]+)',
        'BlackBerry': r'BlackBerry',
        'Chrome OS': r'CrOS',
        'FreeBSD': r'FreeBSD',
        'NetBSD': r'NetBSD',
        'OpenBSD': r'OpenBSD',
        'Tizen': r'Tizen'
    }

    for os_name, pattern in os_patterns.items():
        match = re.search(pattern, user_agent)
        if match:
            version = match.group(1).replace('_', '.') if len(match.groups()) > 0 else ''
            return f"{os_name} {version}".strip()
    
    return "Unknown OS"

def device_type(user_agent):
    mobile_keywords = [
        'Mobile', 'Android', 'iPhone', 'iPad', 'iPod', 'Windows Phone', 
        'BlackBerry', 'Opera Mini', 'Opera Mobi', 'IEMobile', 'webOS',
        'Kindle', 'Nexus', 'Silk', 'PlayBook', 'Fennec'
    ]
    pc_keywords = [
        'Windows', 'Macintosh', 'Linux', 'X11', 'Ubuntu', 'CrOS', 
        'FreeBSD', 'NetBSD', 'OpenBSD'
    ]
    tablet_keywords = [
        'iPad', 'Android', 'Tablet', 'Kindle', 'Nexus',
        'PlayBook', 'Surface'
    ]
    bot_keywords = [
        'bot', 'crawl', 'spider', 'checker', 'archive', 'wget', 'curl'
    ]
    user_agent = user_agent.lower()  # 将用户代理字符串转换为小写以便匹配

    if any(keyword.lower() in user_agent for keyword in bot_keywords):
        return 'bot'  # 如果是爬虫，返回'bot'
    
    if any(keyword.lower() in user_agent for keyword in mobile_keywords):
        if any(keyword.lower() in user_agent for keyword in tablet_keywords):
            return 'tablet'  # 返回tablet类型
        return 'mobile'
    
    elif any(keyword.lower() in user_agent for keyword in pc_keywords):
        return 'pc'
    
    return 'other'

@dataclass
class UserAgent:
    user_agent: str
    device: str = None
    os: str = None
    browser: str = None
    hashinfo: str = None

    def __post_init__(self):
        self.device = device_type(self.user_agent)
        self.os = os_info(self.user_agent)
        self.browser = browser_info(self.user_agent)
        self.hashinfo = hashlib.md5(self.user_agent.encode('utf-8')).hexdigest().lower()