import requests
import random
import re

from PIL import Image


def mostRecentImg(imgs:str):
    mostRecent = imgs[0].split('-')
    for per in imgs[1:]:
        splits = per.split('-')
        if splits[0] > mostRecent[0]: # year
            mostRecent = splits
        elif splits[1] > mostRecent[1]: # month
            mostRecent = splits
        elif splits[2] > mostRecent[2]: # day
            mostRecent = splits
        elif splits[3] > mostRecent[3]:  # hour
            mostRecent = splits
        elif splits[4] > mostRecent[4]:  # minute
            mostRecent = splits
        elif splits[5] > mostRecent[5]:  # second
            mostRecent = splits
    full = '-'.join(mostRecent)
    return full


def getAddrFromIP(ip:str) -> dict:
    url = "https://www.ip138.com/iplookup.asp?ip={}&action=2".format(ip)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36'
    }

    # 获取响应
    response = requests.get(url=url, headers=headers)
    response.encoding = "gb2312"

    html = response.text

    info = dict()
    for match in re.finditer('"(prov|city|ct)":"(.*?)"', html):
        divide = match.group().split(":")
        info["{}".format(divide[0].strip('"'))] = divide[1].strip('"')
    return info

def RandomEmail(emailType=None, rang=None):
    __emailtype = ["@qq.com", "@163.com", "@126.com", "@189.com", "@gmail.com"]
    # 如果没有指定邮箱类型，默认在 __emailtype中随机一个
    if emailType == None:
        __randomEmail = random.choice(__emailtype)
    else:
        __randomEmail = emailType
    # 如果没有指定邮箱长度，默认在4-10之间随机
    if rang == None:
        __rang = random.randint(6, 10)
    else:
        __rang = int(rang)
    __Number = "0123456789qbcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPWRSTUVWXYZ"
    __randomNumber = "".join(random.choice(__Number) for i in range(__rang))
    _email = __randomNumber + __randomEmail
    return _email

# pytorch模型
import torch as t
import torchvision as tv

device = t.device("cpu")
img_size = 256
normalize = tv.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
transform = tv.transforms.Compose(
    [tv.transforms.Resize([img_size, img_size]), tv.transforms.CenterCrop([img_size, img_size]),
     tv.transforms.ToTensor(), normalize])

Apple = ['[Apple_scab]', '[Black_rot]', '[Cedar_apple_rust]', '[healthy]']
Cherry = ['[Powdery_mildew]', '[healthy]']
Corn = ['[Cercospora_leaf_spot] [Gray_leaf_spot]', '[Common_rust]', '[Northern_Leaf_Blight]', '[healthy]']
Grape = ['[Black_rot]', '[Esca_Black_Measles]', '[Leaf_blight]', '[healthy]']
Peach = ['[Bacterial_spot]', '[healthy]']
Pepper = ['[Bacterial_spot]', '[healthy]']
Potato = ['[Early_blight]', '[Late_blight]', '[healthy]']
Tomato = ['[Target_Spot]', '[YellowLeaf_Curl_Virus]', '[Bacterial_spot]', '[Early_blight]', '[healthy]', '[Late_blight]', '[Leaf_Mold]', '[Septoria_leaf_spot]', '[Spider_mites]']
classname = ["apple", "cherry", "corn", "grape", "peach", "pepper", "potato", "tomato"]
classes = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
en2ch = {"Apple [Apple_scab]": "苹果 黑星病", "Apple [Black_rot]": "苹果 黑腐病", "Apple [Cedar_apple_rust]": "苹果 胶锈菌瘿", "Apple [healthy]": "苹果 健康",

         "Cherry [Powdery_mildew]": "樱桃 白粉病", "Cherry [healthy]": "樱桃 健康",

         "Corn [Cercospora_leaf_spot] [Gray_leaf_spot]": "玉米 叶斑病 灰斑病", "Corn [Common_rust]": "玉米 锈病", "Corn [Northern_Leaf_Blight]": "玉米 大斑病", "Corn [healthy]": "玉米 健康",

         "Grape [Black_rot]": "葡萄 黑腐病", "Grape [Esca_Black_Measles]": "葡萄 伊斯卡黑色麻疹", "Grape [Leaf_blight]": "葡萄 叶疫病", "Grape [healthy]": "葡萄 健康",

         "Peach [Bacterial_spot]": "桃子 细菌性斑点病", "Peach [healthy]": "桃子 健康",

         "Pepper [Bacterial_spot]": "胡椒 细菌性斑点病", "Pepper [healthy]": "胡椒 健康",

         "Potato [Early_blight]": "土豆 早疫病", "Potato [healthy]": "土豆 健康", "Potato [Late_blight]": "土豆 晚疫病",

         'Tomato [Target_Spot]': "西红柿 靶斑病", 'Tomato [YellowLeaf_Curl_Virus]': "西红柿 黄化曲叶病毒",
         'Tomato [Bacterial_spot]': "西红柿 细菌性斑点病", 'Tomato [Early_blight]': "西红柿 早疫病",
         'Tomato [healthy]': "西红柿 健康", 'Tomato [Late_blight]': "西红柿 晚疫病",
         'Tomato [Leaf_Mold]': "西红柿 叶霉病", 'Tomato [Septoria_leaf_spot]': "西红柿 针壳孢叶斑病",
         'Tomato [Spider_mites]': "西红柿 蜘蛛螨",

         "apple [apple scab]": "苹果 [苹果黑星病]",
         "apple [black rot]": "苹果 [黑腐病]",
         "apple [cedar apple rust]": "苹果 [雪松苹果锈病]",
         "apple [healthy]": "苹果 [健康]",
         "blueberry [healthy]": "蓝莓 [健康]",
         "cherry [including sour] [powdery mildew]": "樱桃 [含酸][白粉病]",
         "cherry [including sour] [healthy]": "樱桃 [包括酸的][健康的]",
         "corn [maize cercospora leaf spot] [gray leaf spot]": "玉米 [玉米褐斑病叶斑病][灰斑病]",
         "corn [maize common rust]": "玉米 [玉米普通锈病]",
         "corn [maize northern leaf blight]": "玉米 [玉米北叶枯病]",
         "corn [healthy]": "玉米 [健康]",
         "grape [black rot]": "葡萄 [黑腐病]",
         "grape [esca black measles]": "葡萄 [埃斯卡黑麻疹]",
         "grape [leaf blight] [isariopsis leaf spot]": "葡萄 [叶枯病][狭叶草叶斑病]",
         "grape [healthy]": "葡萄 [健康]",
         "orange [haunglongbing citrus greening]": "柑桔 [鬼龙槟榔]",
         "peach [bacterial spot]": "桃子 [细菌性斑点病]",
         "peach [healthy]": "桃子 [健康]",
         "bellpepper [bacterial spot]": "灯笼椒 [细菌性斑点病]",
         "bellpepper [healthy]": "灯笼椒 [健康]",
         "potato [early blight]": "土豆 [早疫病]",
         "potato [late blight]": "土豆 [晚疫病]",
         "potato [healthy]": "土豆 [健康]",
         "raspberry [healthy]": "覆盆子 [健康]",
         "soybean [healthy]": "大豆 [健康]",
         "squash [powdery mildew]": "南瓜 [白粉病]",
         "strawberry [leaf scorch]": "草莓 [叶子枯萎]",
         "strawberry [healthy]": "草莓 [健康]",
         "tomato [bacterial spot]": "番茄 [细菌性斑点病]",
         "tomato [early blight]": "番茄 [早疫病]",
         "tomato [late blight]": "番茄 [晚疫病]",
         "tomato [leaf mold]": "番茄 [霉菌]",
         "tomato [septoria leaf spot]": "番茄 [斑疹叶]",
         "tomato [spider mites] [two spotted spider mite]": "番茄 [蜘蛛螨][两斑蜘蛛螨]",
         "tomato [target spot]": "番茄 [靶斑病]",
         "tomato [yellow leaf curl virus]": "番茄 [黄曲叶病毒]",
         "tomato [mosaic virus]": "番茄 [花叶病毒]",
         "tomato [healthy]": "番茄 [健康]"
         }


def infer(model, image_PIL, isShowSoftmax=False):
    t.no_grad()

    image_tensor = transform(image_PIL)
    # 以下语句等效于 img = torch.unsqueeze(image_tensor, 0)
    image_tensor.unsqueeze_(0)
    # 没有这句话会报错
    image_tensor = image_tensor.to(device)
    out = model(image_tensor)
    # 得到预测结果，并且从大到小排序
    _, indices = t.sort(out, descending=True)

    # 返回每个预测值的百分数
    percentage = t.nn.functional.softmax(out, dim=1)[0] * 100

    # 是否显示每个分类的预测值
    item = indices[0]
    if isShowSoftmax:
        for idx in item:
            ss = percentage[idx]
            value = ss.item()
            name = classes[idx]
            # print('名称：', name, '预测值：', value)

    # 预测最大值
    _, predicted = t.max(out.data, 1)
    maxPredicted = classes[predicted.item()]
    maxAccuracy = percentage[item[0]].item()
    return int(maxPredicted)-1, maxAccuracy

model_Apple = t.load('static/models/applemodel.pkl', map_location=device)
model_Apple = model_Apple.to(device)
model_Apple.eval()
model_Cherry = t.load('static/models/cherrymodel.pkl', map_location=device)
model_Cherry = model_Cherry.to(device)
model_Cherry.eval()
model_Corn = t.load('static/models/cornmodel.pkl', map_location=device)
model_Corn = model_Corn.to(device)
model_Corn.eval()
model_Grape = t.load('static/models/grapemodel.pkl', map_location=device)
model_Grape = model_Grape.to(device)
model_Grape.eval()
model_Peach = t.load('static/models/peachmodel.pkl', map_location=device)
model_Peach = model_Peach.to(device)
model_Peach.eval()
model_Pepper = t.load('static/models/peppermodel.pkl', map_location=device)
model_Pepper = model_Pepper.to(device)
model_Pepper.eval()
model_Potato = t.load('static/models/potatomodel.pkl', map_location=device)
model_Potato = model_Potato.to(device)
model_Potato.eval()
model_Tomato = t.load('static/models/tomatomodel.pkl', map_location=device)
model_Tomato = model_Tomato.to(device)
model_Tomato.eval()


def infer_special(value, image):
    print("预测{}".format(value))
    condition, val = infer(eval("model_{}".format(value)), image, True)
    condition = eval("{}[condition]".format(value))
    val = str(float(val) / 100)[:9]
    ch = en2ch[' '.join([value, condition])]
    return {'prediction': {'species': ch.split(' ')[0], 'condition': ' '.join(ch.split(' ')[1:]), 'value': val}, 'conditionen': condition}


import datetime
from sqlalchemy import and_, or_
from flask import render_template
from detectweb.models.predict import Predict
week, month, year, tenyear = 7, 30, 360, 3600
delta = {"week": 1, "month": 1, "year": 30, "tenyear": 360}


def getStatistics(timeline, type_, all_of_same_city, time_now, current_user):
    assign_timeline = {"week": -1, "month": -1, "year": -1, "tenyear": -1}
    assign_type = {"allkinds": -1, "apple": -1, "cherry": -1, "corn": -1, "grape": -1,
                   "peach": -1, "pepper": -1, "potato": -1, "tomato": -1}
    if timeline not in assign_timeline.keys() or type_ not in assign_type.keys():
        return render_template('404.html')
    alltimes = []
    # 最近一周数据
    predicts_certain_time = eval("all_of_same_city.filter(and_((Predict.predict_time >= time_now - datetime.timedelta(days={})), Predict.predict_time <= time_now))".format(timeline))
    if type_ != "allkinds":
        predicts_certain_time = eval("predicts_certain_time.filter(or_(Predict.predict_result.like('{}%'), Predict.predict_result.like('{}%')))".format(type_, type_.capitalize()))

    alltimes.append(predicts_certain_time.count())
    last_time = predicts_certain_time
    for i in range(eval(timeline)-delta[timeline], 0, -delta[timeline]):
        this_time = last_time.filter(and_((Predict.predict_time >= time_now - datetime.timedelta(days=i)), Predict.predict_time <= time_now))
        last_time = this_time
        alltimes.append(this_time.count())
    assign_timeline[timeline] = alltimes
    assign_type[type_] = 1
    return render_template(
        'dashboard.html',
        assign_timeline=assign_timeline,
        assign_type=assign_type,
        timeline=timeline,
        type_=type_,
        user=current_user)

# def init_model(value):
#     exec("model_{} = t.load('static/models/{}model.pkl', map_location=device)".format(value, value.lower()))
#     exec("model_{} = model_{}.to(device)".format(value, value))
#     eval("model_{}.eval()".format(value))
#     return eval("model_{}".format(value))

# def delete_model(model):
#     try:
#         del model
#         return True
#     except:
#         return False

# from memory_profiler import profile
# @profile
# def infer_special(value, image):
#     model = init_model(value)
#     print("预测{}".format(value))
#     condition, val = infer(model, image, True)
#     condition = eval("{}[condition]".format(value))
#     val = str(float(val) / 100)[:9]
#     del model
#     return {'prediction': {'species': value, 'condition': condition, 'value': val}}

