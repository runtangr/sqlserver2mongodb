from unittest import TestCase

from src.main.python.Application.Information.DxtInformationJxNewsImage import jxNewsImage


class TestJxNewsImage(TestCase):
    def setUp(self):
        self.jxNewsImage = jxNewsImage()

    def test_CreateSyncInfo(self):
        self.fail()

    def test_jxNewsImagePort(self):
        self.jxNewsImage.jxNewsImagePort()

    def test_jxNewsImageMC(self):
        self.fail()

    def test_DealData(self):
        self.fail()

    def test_Save(self):
        self.fail()
