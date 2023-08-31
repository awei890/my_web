from PIL import Image


class Image_process():
    '''该类用于处理图片到合适比例，一些特殊情况，如 图片1（1000x300）-> 图片2（240x360） 可能无法进行处理或处理结果不行(不会进行拉伸，而是白布替代)'''

    def __init__(self, img_url, fix=240 / 360, width=560):
        '''
        :param img_url: 图片路径
        :param fix: 图片需要调整的比例（宽/高）
        :param width: 输出图片的宽
        '''
        self.img = Image.open(img_url).convert("RGB")
        self.fix = fix
        self.width = width
        self.size = self.img.size

        # 以width宽度为目标进行同比缩放
        self.resize()

        # 保存
        self.img.save(img_url)
        self.size = self.img.size
        # 根据比例裁剪图片
        self.fix_image()
        self.img.save(img_url)

    def resize(self):
        # 以width宽度为目标进行同比缩放 scale为缩放、扩大百分比
        scale = self.width / self.size[0]
        y = self.size[1] * scale
        self.img = self.img.resize((self.width, int(y)))

    def fix_image(self):
        # 用于裁剪出合适比例的图片

        # 图片的高比目标比例的高大
        if self.size[1] > self.width / self.fix:
            print("剪切处理")
            img_crop = self.img.crop((0, int((self.size[1] - self.width / self.fix) / 2), self.width,
                                      int((self.size[1] - self.width / self.fix) / 2 + self.width / self.fix)))
            self.img = img_crop

        # 图片的高比目标比例的高小
        else:
            print("白色背景填充")
            img_background = Image.new(mode="RGB", size=(self.width, int(self.width / self.fix)), color="white")
            img_background.paste(self.img, (0, int((img_background.size[1] - self.img.size[1]) / 2)))
            self.img = img_background
