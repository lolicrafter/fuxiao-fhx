import json
import pytesseract
import pyautogui
import time, os
import pyperclip
from PIL import Image, ImageDraw, ImageFont
from pytesseract import Output
from cnocr import CnOcr
from position import mouse_position
from notice import send_notification

cand_alphabet = [
    "山风鸟",
    "破空者",
    "风舞姬",
    "流萤",
    "夏雨临",
    "夜裔",
    "泽斯托尔-1",
    "泽斯托尔-16",
    "美祢",
    "墨汐",
    "泽斯托尔-22",
    "禾栎",
    "美由纪",
    "羽露草",
    "诗炉雪",
    "探索者",
    "通讯员",
    "禾椛",
    "知枫",
    "萝斯",
    "春柚",
    "枪之先驱",
    "幻想曲",
    "祥瑞御免",
    "知栀",
    "果蒲",
    "铁臂",
    "果荻",
    "知梓",
    "知柏",
    "佐栴",
    "萨罗蒙",
    "莫妮卡",
    "哈曼",
    "火焰女神",
    "海伦",
    "金之谜团",
    "木田神",
    "玉瑞",
    "多多",
    "若川",
    "山淀",
    "仙黛",
    "云雀",
    "雷鸟",
    "海鹰飞艇",
    "琥珀",
    "上游之民",
    "忠诚伯爵",
    "莱茵",
    "大河流",
    "洋平",
    "洋宁",
    "空流",
    "奈亚",
    "阿列苏莎",
    "希露·菲利德",
    "伊希斯",
    "不死鸟",
    "红叶",
    "弥犰",
    "雾都",
    "若犹",
    "若排",
    "美食",
    "弥獌",
    "库恩锡",
    "魔女塔",
    "亚田子",
    "管风琴",
    "珀菈",
    "诺弗科",
    "纱芙可",
    "普里斯特",
    "坎格娜",
    "巨人",
    "云鸱",
    "木星",
    "鹁鸽",
    "阿尔戈斯",
    "木枭",
    "云鸢",
    "幽冥",
    "惊灵",
    "剑卫士",
    "神罗圣女",
    "青雀",
    "北之女王",
    "洛特尼",
    "微妮特",
    "乌鳌",
    "奈雅纪",
    "乌螯",
    "无津",
    "巨湾",
    "黄金",
    "银之藏",
    "抢先者",
    "红衣公爵",
    "尼尔薰",
    "花园",
    "印苏",
    "红雀",
    "沃斯派蒂",
    "尤莉娅·西撒",
    "卡米萝·本索",
    "安娜·希斯塔",
    "德拉蔻·尤克尔",
    "芮托莉欧",
    "伊莉欧·星语",
    "纯白女王",
    "空鲤",
    "彻尔",
    "锥鳗",
    "洄鲟",
    "杜萦·科尔克",
    "赛茵赫斯",
    "黑桧",
    "金泽",
    "灰夫人",
    "空之罗宾",
    "飞艇伯爵",
    "追击方舟",
    "约柯敦",
    "闪灵",
    "荷涅特",
    "善战",
    "鹤寿",
    "白鹬",
    "仙鹤",
    "蓝女士",
    "耶格尔",
    "苍蛟",
    "虹龙",
    "山凤"
]

ocr = CnOcr()  # 所有参数都使用默认值

# 配置pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'


def capture_screen():
    image = pyautogui.screenshot()
    return image


def load_card_names(filename):
    with open(filename, 'r', 8, 'utf-8') as file:
        card_data = json.load(file)
    return card_data['shipName']


def ocr_image_with_position(image_path):
    # CnOcr.set_cand_alphabet(cand_alphabet)
    resized_shape = [2000, 3200]
    # det_kwargs中resized_shape使用(1920,860)
    output = ocr.ocr(image_path, resized_shape=resized_shape, min_box_size=6)
    # 准备一个列表来存储OCR结果
    ocr_results = []

    # 遍历output字典的每一项
    for i in output:
        text = i['text'].strip()
        score: float = i['score']
        # 将NumPy数组转换为列表
        position = i['position'].flatten().tolist()
        # 确保文本非空
        if text and score > 0.5:
            ocr_results.append({'text': text, 'score': score, 'position': position})

    return ocr_results


def find_matching_text_and_position(ocr_results, card_names):
    matching_results = []
    for ocr_result in ocr_results:
        for card in card_names:
            if ocr_result['text'] == card['harmony']:
                matching_results.append((ocr_result['text'], ocr_result['position'], card['originName']))
                break  # 假设每个harmony名称只匹配一次
    return matching_results


def draw_text_on_image(image_path, text, position):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    points = [(x, y) for x, y in zip(position[::2], position[1::2])]
    draw.polygon(points, (255, 0, 0))  # 绘制红色矩形框

    # # 使用默认字体和字体大小
    # font = ImageFont.load_default()
    # text_width = 44
    # text_height = 33
    # # 计算新文本的位置
    # new_position = (
    #     position[0],  # 左边距
    #     position[1] + position[3] + text_height  # 顶部偏移加上原高度再加新文本高度
    # )
    # draw.text(new_position,
    #           text, (255, 255, 255))
    image.save(text + 'modified_card_image.jpg')


def press_key(message):
    pyperclip.copy(message)  # 复制该行
    pyautogui.hotkey("alt", "space")
    time.sleep(2)
    pyautogui.hotkey("ctrl", "v")  # 粘贴
    time.sleep(1)
    pyautogui.hotkey("esc")
    # pyautogui.hotkey("esc")  # 粘贴
    # time.sleep(1)

# 移动鼠标并发送通知
def move_and_notice(title, position):
    print('move_and_notice', title)
    pyautogui.moveTo(position[0], position[1])
    press_key(title)
    # send_notification(title, title)
    time.sleep(0.5)


def handle_ship():
    time.sleep(2)  # 等待5秒，确保截屏成功
    card_names = load_card_names('shipName.json')
    # 截屏并保存为harmony.jpg
    capture_screen().save('harmony1.jpg')
    ocr_results = ocr_image_with_position('./harmony1.jpg')
    matching_results = find_matching_text_and_position(ocr_results, card_names)

    print(matching_results)
    for match in matching_results:
        original_name, position = match[2], match[1]
        print(original_name, position)
        # draw_text_on_image('./harmony1.jpg', original_name, position)
        # modified_image.show()  # 显示修改后的图像
        move_and_notice(original_name, position)


# 主程序
if __name__ == '__main__':
    # mouse_position()
    handle_ship()
    # send_notification('test', 'message')
