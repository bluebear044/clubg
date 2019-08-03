#!/usr/bin/python
# -*- coding: utf-8  -*-
import config

import os
import unittest
from mock import patch, Mock, MagicMock
from soup import Soup

class SoupTest(unittest.TestCase):

	reqUrlHtml_base_three_item = '<div class="reserve_ban_con"><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015618"><img src="https://image.bandai.co.kr/plan/image/20190801_mg_heavyarms_ew_1020x160_ko_20190801170112.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] MG 건담 헤비암즈 EW (이겔 장비)</span><br/><span>기간 : 2019/08/01 ~ 2019/08/06</span><p class="release_time">출고연월 : 2019/12</p></div></a></div><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015619"><img src="https://image.bandai.co.kr/plan/image/20190709_mg_f91_harrison_1020x160_ko_20190724160916.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] MG 건담 F91 Ver.2.0 해리슨 전용기</span><br/><span>기간 : 2019/07/24 ~ 2019/08/11</span><p class="release_time">출고연월 : 2019/11</p></div></a></div><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015615"><img src="https://image.bandai.co.kr/plan/image/20190709_hg_second_v_1020x160_ko_20190724154729.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] HG 세컨드 V</span><br/><span>기간 : 2019/07/24 ~ 2019/08/11</span><p class="release_time">출고연월 : 2019/11</p></div></a></div></div>'
	reqUrlHtml_sub_one_item = '<div class="reserve_ban_con"><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015619"><img src="https://image.bandai.co.kr/plan/image/20190709_mg_f91_harrison_1020x160_ko_20190724160916.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] MG 건담 F91 Ver.2.0 해리슨 전용기</span><br/><span>기간 : 2019/07/24 ~ 2019/08/11</span><p class="release_time">출고연월 : 2019/11</p></div></a></div><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015615"><img src="https://image.bandai.co.kr/plan/image/20190709_hg_second_v_1020x160_ko_20190724154729.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] HG 세컨드 V</span><br/><span>기간 : 2019/07/24 ~ 2019/08/11</span><p class="release_time">출고연월 : 2019/11</p></div></a></div></div>'
	reqUrlHtml_add_new_item = '<div class="reserve_ban_con"><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=008784"><img src="https://image.bandai.co.kr/plan/image/pc_20190724155351.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] MG 풀 아머 건담 (블루 컬러 Ver.) [재판]</span><br/><span>기간 : 2019/07/24 ~ 2019/08/11</span><p class="release_time">출고연월 : 2019/12</p></div></a></div><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015618"><img src="https://image.bandai.co.kr/plan/image/20190801_mg_heavyarms_ew_1020x160_ko_20190801170112.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] MG 건담 헤비암즈 EW (이겔 장비)</span><br/><span>기간 : 2019/08/01 ~ 2019/08/06</span><p class="release_time">출고연월 : 2019/12</p></div></a></div><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015619"><img src="https://image.bandai.co.kr/plan/image/20190709_mg_f91_harrison_1020x160_ko_20190724160916.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] MG 건담 F91 Ver.2.0 해리슨 전용기</span><br/><span>기간 : 2019/07/24 ~ 2019/08/11</span><p class="release_time">출고연월 : 2019/11</p></div></a></div><div class="reserve_ban"><a href="/display/goods.do?method=goods&goods_code=015615"><img src="https://image.bandai.co.kr/plan/image/20190709_hg_second_v_1020x160_ko_20190724154729.jpg" alt="" width="1020px" height="160px"/><div class="reserve_ban_txt"><span>[클럽G] HG 세컨드 V</span><br/><span>기간 : 2019/07/24 ~ 2019/08/11</span><p class="release_time">출고연월 : 2019/11</p></div></a></div></div>'
	reqUrlHtml_empty = ''

	def setUp(self):
		#File Backup
		fName = os.path.join(config.PRJ_CONFIG['path'], "data.txt")
		if os.path.exists(fName):
			os.rename(fName, ''.join([config.PRJ_CONFIG['path'], "data.bak"]))

	def tearDown(self):

		fName = os.path.join(config.PRJ_CONFIG['path'], "data.txt")
		if os.path.exists(fName):
			os.remove(fName)

		#File Restore
		fName = os.path.join(config.PRJ_CONFIG['path'], "data.bak")
		if os.path.exists(fName):
			os.rename(fName, ''.join([config.PRJ_CONFIG['path'], "data.txt"]))

	def test_soup_first_crawling(self):
		obj = Soup()
		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_base_three_item)
		obj.sendEmail = MagicMock()		
		result = obj.main()
		self.assertTrue(result > 0)
	
	def test_soup_normal_crawling(self):
		obj = Soup()
		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_base_three_item)
		obj.sendEmail = MagicMock()		
		
		#Request N times
		result = obj.main()
		result = obj.main()
		result = obj.main()

		self.assertTrue(result == 0)

	def test_soup_crawling_detect_differnce_sub_item(self):
		obj = Soup()
		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_base_three_item)
		obj.sendEmail = MagicMock()		
		result = obj.main()

		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_sub_one_item)
		result = obj.main()

		self.assertTrue(result > 0)

	def test_soup_crawling_detect_differnce_new_item(self):
		obj = Soup()
		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_base_three_item)
		obj.sendEmail = MagicMock()		
		result = obj.main()

		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_add_new_item)
		result = obj.main()

		self.assertTrue(result > 0)

	def test_soup_crawling_meet_empty_response(self):
		obj = Soup()
		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_base_three_item)
		obj.sendEmail = MagicMock()		
		result = obj.main()

		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_empty)
		result = obj.main()

		self.assertTrue(result == 0)

	def test_soup_crawling_meet_empty_file(self):
		obj = Soup()
		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_empty)
		obj.sendEmail = MagicMock()		
		result = obj.main()

		obj.reqUrl = MagicMock(return_value=self.reqUrlHtml_base_three_item)
		result = obj.main()

		self.assertTrue(result > 0)


if __name__ == '__main__':  
	unittest.main()