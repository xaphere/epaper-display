from waveshare_epd import epd2in13bc
from PIL import Image


class Display:
    def __init__(self) -> None:
        self.epd = epd2in13bc.EPD()
        self.drawing = False

    def size(self):
        return self.epd.height, self.epd.width

    def draw_image(self, black, red):
        self.drawing = True
        try:
            self.epd.init()
            #self.epd.Clear()

            self.epd.display(self.epd.getbuffer(
                black), self.epd.getbuffer(red))
            self.epd.sleep()
            self.drawing = False
        except Exception:
            self.drawing = False
            epd2in13bc.epdconfig.module_exit()

    def get_clear_image(self):
        return Image.new('1', (self.epd.height, self.epd.width), 255)

    def Busy(self):
        return self.drawing