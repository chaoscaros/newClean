"""
cron: 50 59 * * * *
new Env('财富岛兑换红包');
"""
import os
import re
import time
import json
import datetime
import requests
import random
import string

ql_auth_path = '/ql/config/auth.json'
# ql_auth_path = r'D:\Docker\ql\config\auth.json'
ql_url = 'http://localhost:5700'


def __get_token() -> str or None:
    with open(ql_auth_path, 'r', encoding='utf-8') as f:
        j_data = json.load(f)
    return j_data.get('token')


def __get__headers() -> dict:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + __get_token()
    }
    return headers


# 查询环境变量
def get_envs(name: str = None) -> list:
    params = {
        't': int(time.time() * 1000)
    }
    if name is not None:
        params['searchValue'] = name
    res = requests.get(ql_url + '/api/envs', headers=__get__headers(), params=params)
    j_data = res.json()
    if j_data['code'] == 200:
        return j_data['data']
    return []


# 新增环境变量
def post_envs(name: str, value: str, remarks: str = None) -> list:
    params = {
        't': int(time.time() * 1000)
    }
    data = [{
        'name': name,
        'value': value
    }]
    if remarks is not None:
        data[0]['remarks'] = remarks
    res = requests.post(ql_url + '/api/envs', headers=__get__headers(), params=params, json=data)
    j_data = res.json()
    if j_data['code'] == 200:
        return j_data['data']
    return []


# 修改环境变量
def put_envs(_id: str, name: str, value: str, remarks: str = None) -> bool:
    params = {
        't': int(time.time() * 1000)
    }
    data = {
        'name': name,
        'value': value,
        '_id': _id
    }
    if remarks is not None:
        data['remarks'] = remarks
    res = requests.put(ql_url + '/api/envs', headers=__get__headers(), params=params, json=data)
    j_data = res.json()
    if j_data['code'] == 200:
        return True
    return False


# 禁用环境变量
def disable_env(_id: str) -> bool:
    params = {
        't': int(time.time() * 1000)
    }
    data = [_id]
    res = requests.put(ql_url + '/api/envs/disable', headers=__get__headers(), params=params, json=data)
    j_data = res.json()
    if j_data['code'] == 200:
        return True
    return False


# 启用环境变量
def enable_env(_id: str) -> bool:
    params = {
        't': int(time.time() * 1000)
    }
    data = [_id]
    res = requests.put(ql_url + '/api/envs/enable', headers=__get__headers(), params=params, json=data)
    j_data = res.json()
    if j_data['code'] == 200:
        return True
    return False
# 随机生成数字与小写字母字符串
def get_random_str(rdm_leg: int = 8, status: bool = False):
    random_str = ''
    base_str = string.octdigits
    if status:
        base_str = base_str + string.ascii_lowercase
    length = len(base_str) - 1
    for i in range(rdm_leg):
        random_str += base_str[random.randint(0, length)]
    return random_str

# 默认配置(看不懂代码也勿动)
cfd_start_time = -0.15
cfd_offset_time = 0.01
myCookie = ""

# 基础配置勿动
# cfd_url = "https://m.jingxi.com/jxbfd/user/ExchangePrize?strZone=jxbfd&dwType=3&dwLvl=1&ddwPaperMoney=100000&strPoolName=jxcfd2_exchange_hb_202205&sceneval=2&g_login_type=1"
# cfd_url = "https://m.jingxi.com/jxbfd/user/ExchangePrize?_imbfd=FA56B0A1AF372BBAE3F33091F156FEB34F657A4B48966B17F54B7D0972D7B0314E610F2165A90511E681893527E53D3BC771955830B8A547D93A3385D3E610B7&strZone=jxbfd&bizCode=jxbfd&source=jxbfd&dwEnv=7&_cfd_t=1653998618328&ptag=7155.9.47&dwType=3&dwLvl=1&ddwPaperMoney=100000&strPoolName=jxcfd2_exchange_hb_202205&strPgtimestamp=1653998618260&strPhoneID=205a305d21fe7b50&strPgUUNum=e2595104ed3993798c9801dcf855ac04&_stk=_cfd_t%2C_imbfd%2CbizCode%2CddwPaperMoney%2CdwEnv%2CdwLvl%2CdwType%2Cptag%2Csource%2CstrPgUUNum%2CstrPgtimestamp%2CstrPhoneID%2CstrPoolName%2CstrZone&_ste=1&h5st=20220531200338329%3B3254222980533141%3B92a36%3Btk02w84451b8e18nZesSESvA3VSBSL%2F834YoPese4xuS%2B6l2xKmldGDpBh0AG041CTgbvpYyjBpoKVpZD%2F9nbKGkJm0w%3Ba0458c422c0d4c9f7020f93762258f1454f3a99fecc0063c73f82ba150148af7%3B3.1%3B1653998618329%3B62f4d401ae05799f14989d31956d3c5fcc829ed37fcdeed4a441c9247af14f05a5599b1932ed9018725b7f152a59a65a8ee3994f819b044bd6195b18bc929c667b2aa4d4086fa7da328843ece58e7b44adcb19efab73f0427565754effca6ae69ce8f653a12f7385e6cae10cdbf7eaeb0b6ee6fa63c3ab39191ecb62d5c97a401a69fabee939c710365424101d90e5dd&_=1653998618342&sceneval=2&g_login_type=1&callback=jsonpCBKM&g_ty=ls&appCode=msd1188198"
# cfd_url = "https://m.jingxi.com/jxbfd/user/ExchangePrize?_imbfd=3EDC6B02C1D48E976D35A4AAE8793D04BA18FFEA02E77A06EDB0A8590B76B5245549AE5636875494D14EECDBDF08B8BF93B5FDC5185B1FB8A6CB6080D1324245&strZone=jxbfd&bizCode=jxbfd&source=jxbfd&dwEnv=7&_cfd_t=1654074396012&ptag=7155.9.47&dwType=3&dwLvl=1&ddwPaperMoney=100000&strPoolName=jxcfd2_exchange_hb_202205&strPgtimestamp=1654074395995&strPhoneID=e5b777e6987529fb&strPgUUNum=e69ed458524f7d4dc0dc169e665e08c3&_stk=_cfd_t%2C_imbfd%2CbizCode%2CddwPaperMoney%2CdwEnv%2CdwLvl%2CdwType%2Cptag%2Csource%2CstrPgUUNum%2CstrPgtimestamp%2CstrPhoneID%2CstrPoolName%2CstrZone&_ste=1&h5st=20220601170636013%3B3784488396145427%3B92a36%3Btk02w9d9e1c5718nVKJm6igHgV778OS2%2F8xVpsqXUxjW8yOqcRRx2lGBXSLa8UlUG9W9nQqMyePYs4bXnMrwV38cxjJU%3Bbdc81178a3a26795dfe4b7b963d804d81aa962aa7e34db32bd3861b0fe04d450%3B3.1%3B1654074396013%3B62f4d401ae05799f14989d31956d3c5fc5d6217cd2fca8359fcce631cf05de92958f0abfb52587bcc5772d578a1272340faf98edddc83bd91e9f366ecc516291ccc1225cff0b678f25b36176ca90685a008f323bd85492d68b5e5c8f3e3315415211e27605faa1fae66ca67b6d67cc1b&_=1654074396020&sceneval=2&g_login_type=1&callback=jsonpCBKII&g_ty=ls&appCode=msd1188198"
cfd_url="https://m.jingxi.com/jxbfd/user/ExchangePrize?strZone=jxbfd&bizCode=jxbfd&source=jxbfd&dwEnv=7&_cfd_t=1655249372974&ptag=138631.77.28&dwType=3&dwLvl=15&ddwPaperMoney=100000&strPoolName=jxcfd2_exchange_hb_202205&strPgtimestamp=1655249372937&strPhoneID=205a305d21fe7b50&strPgUUNum=a1c00859bb44dd61bab2be8affad6825&_stk=_cfd_t%2C_imbfd%2CbizCode%2CddwPaperMoney%2CdwEnv%2CdwLvl%2CdwType%2Cptag%2Csource%2CstrPgUUNum%2CstrPgtimestamp%2CstrPhoneID%2CstrPoolName%2CstrZone&_ste=1&h5st=20220615072932975%3B3254222980533141%3B92a36%3Btk02w84751b4618nG0GiIAQFZzjzCpnCyvXH%2B6pJR%2B6461oPGnSFObURYqn7JbZW86nKf0DLs3yyunuuIEULj8e%2B08Kc%3Bf6e59c94b314b470c15e9fd40ec3864c3fb9528c055bb261cd8d2ac08d6d8ed2%3B3.1%3B1655249372975%3B62f4d401ae05799f14989d31956d3c5fcc829ed37fcdeed4a441c9247af14f05a5599b1932ed9018725b7f152a59a65a8ee3994f819b044bd6195b18bc929c667b2aa4d4086fa7da328843ece58e7b44adcb19efab73f0427565754effca6ae69ce8f653a12f7385e6cae10cdbf7eaeb0b6ee6fa63c3ab39191ecb62d5c97a401a69fabee939c710365424101d90e5dd&_=1655249372981&sceneval=2&g_login_type=1&callback=jsonpCBKNN&g_ty=ls&appCode=msd1188198"
pattern_pin = re.compile(r'pt_pin=([\w\W]*?);')
pattern_data = re.compile(r'\(([\w\W]*?)\)')


# 获取下个整点和时间戳
def get_date() -> str and int:
    # 当前时间
    now_time = datetime.datetime.now()
    # 把根据当前时间计算下一个整点时间戳
    integer_time = (now_time + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:00:00")
    time_array = time.strptime(integer_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return integer_time, time_stamp


# 获取要执行兑换的cookie
def get_cookie():
    ck_list = []
    pin = "null"
    cookie = None
    cookies = get_envs("CFD_COOKIE")
    for ck in cookies:
        if ck.get('status') == 0:
            ck_list.append(ck)
    if len(ck_list) >= 1:
        cookie = ck_list[0]
        re_list = pattern_pin.search(cookie.get('value'))
        if re_list is not None:
            pin = re_list.group(1)
        print('共配置{}条CK,已载入用户[{}]'.format(len(ck_list), pin))
    else:
        print('共配置{}条CK,请添加环境变量,或查看环境变量状态'.format(len(ck_list)))
    return pin, cookie


# 获取配置参数
def get_config():
    start_dist = {}
    start_times = get_envs("CFD_START_TIME")
    if len(start_times) >= 1:
        start_dist = start_times[0]
        start_time = float(start_dist.get('value'))
        print('从环境变量中载入时间变量[{}]'.format(start_time))
    else:
        start_time = cfd_start_time
        u_data = post_envs('CFD_START_TIME', str(start_time), '财富岛兑换时间配置,自动生成,勿动')
        if len(u_data) == 1:
            start_dist = u_data[0]
        print('从默认配置中载入时间变量[{}]'.format(start_time))
    return start_time, start_dist


# 抢购红包请求函数
def cfd_qq(def_start_time):
    # 进行时间等待,然后发送请求
    end_time = time.time()
    while end_time < def_start_time:
        end_time = time.time()
    # 记录请求时间,发送请求
    t1 = time.time()
    d1 = datetime.datetime.now().strftime("%H:%M:%S.%f")
    res = requests.get(cfd_url, headers=headers)
    print(res.text)
    t2 = time.time()
    # 正则对结果进行提取
    # re_list = pattern_data.search(res.text)
    # 进行json转换
    # data = json.loads(re_list.group(1))
    data = json.loads(res.text)
    msg = data['sErrMsg']
    # 根据返回值判断
    if data['iRet'] == 0:
        # 抢到了
        msg = "可能抢到了"
        # put_envs(u_cookie.get('_id'), u_cookie.get('name'), u_cookie.get('value'), msg)
        # disable_env(u_cookie.get('_id'))
    elif data['iRet'] == 2016:
        # 需要减
        start_time = float(u_start_time) - float(cfd_offset_time)
        put_envs(u_start_dist.get('_id'), u_start_dist.get('name'), str(start_time)[:8])
    elif data['iRet'] == 2013:
        # 需要加
        start_time = float(u_start_time) + float(cfd_offset_time)
        put_envs(u_start_dist.get('_id'), u_start_dist.get('name'), str(start_time)[:8])
    elif data['iRet'] == 1014:
        # URL过期
        pass
    elif data['iRet'] == 2007:
        # 财富值不够
        put_envs(u_cookie.get('_id'), u_cookie.get('name'), u_cookie.get('value'), msg)
        disable_env(u_cookie.get('_id'))
    elif data['iRet'] == 9999:
        # 账号过期
        put_envs(u_cookie.get('_id'), u_cookie.get('name'), u_cookie.get('value'), msg)
        disable_env(u_cookie.get('_id'))
    print("实际发送[{}]\n耗时[{:.3f}]\n用户[{}]\n结果[{}]".format(d1, (t2 - t1), u_pin, msg))


if __name__ == '__main__':
    print("- 程序初始化")
    print("脚本进入时间[{}]".format(datetime.datetime.now().strftime("%H:%M:%S.%f")))
    # 从环境变量获取url,不存在则从配置获取
    u_url = os.getenv("CFD_URL", cfd_url)
    # 获取cookie等参数
    u_pin, u_cookie = get_cookie()
    # 获取时间等参数
    u_start_time, u_start_dist = get_config()
    # 预计下个整点为
    u_integer_time, u_time_stamp = get_date()
    print("抢购整点[{}]".format(u_integer_time))
    print("- 初始化结束\n")

    print("- 主逻辑程序进入")
    UA = "jdpingou;iPhone;5.11.0;15.1.1;{};network/wifi;model/iPhone13,2;appBuild/100755;ADID/;supportApplePay/1;hasUPPay/0;pushNoticeIsOpen/1;hasOCPay/0;supportBestPay/0;session/22;pap/JA2019_3111789;brand/apple;supportJDSHWK/1;Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148".format(
        get_random_str(45, True))
    if u_cookie is None:
        print("未读取到CFD_COOKIE,程序结束")
    else:
        headers = {
            "Host": "m.jingxi.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
            'Cookie': u_cookie['value'],
            "User-Agent": UA,
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Referer": "https://st.jingxi.com/",
            "Accept-Encoding": "gzip, deflate, br"
        }
        u_start_sleep = float(u_time_stamp) + float(u_start_time)
        print("预计发送时间为[{}]".format(datetime.datetime.fromtimestamp(u_start_sleep).strftime("%H:%M:%S.%f")))
        if u_start_sleep - time.time() > 300:
            print("离整点时间大于5分钟,强制立即执行")
            cfd_qq(0)
        else:
            cfd_qq(u_start_sleep)
    print("- 主逻辑程序结束")
