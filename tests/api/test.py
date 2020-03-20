import requests

# SCHEMA_BASE_URL = os.path.join(BASE_DIR, 'schema')
class Test:
    def test_ressult(self):
        '''

        :return:
        '''
        response1 = requests.get(
            url='https://search.develop.tekoapis.net/api/search?channel=vnshop_online&terminal=vnshop_app&q=bàn&_limit=1&responses=products,filters&filters=brands,sellerCategories&_page=1&publishStatus=true&price_gte=1&saleStatuses_ne=ngung_kinh_doanh,hang_dat_truoc')
        result1 = response1.json()
        response2 = requests.get(
            url='https://listing.develop.tekoapis.net/api/search?channel=vnshop_online&terminal=vnshop_app&q=bàn&_limit=1&responses=products,filters&filters=brands,sellerCategories&_page=1&publishStatus=true&price_gte=1&saleStatuses_ne=ngung_kinh_doanh,hang_dat_truoc')
        result2 = response2.json()
        assert result1 == result2

    def call_api(self, q):
        params = {
            'channel': 'vnshop_online',
            'terminal': 'vnshop_app',
            'q': q,
            '_limit': 100,
            '_page': 1,
        }
        return requests.get(url='http://search.stage.tekoapis.net/api/search', params=params)

    def test_search(self):
        # key = ["Ghế", "Bình", "Ca", "Cốc", "Cửa", "Dép", "giường", "lồng", "nước rửa tay", "nến", "quần", "son", "sữa",
        #        "tủ", "váy", "vệ sinh", "balo", "bia", "bánh", "bút bi", "bút chì", "kính mắt", "lịch bàn", "móc treo",
        #        "nồi", "sách", "túi", "xà bông", "xà phòng", "bột giặt", "đèn", "đồng hồ", "kem dưỡng da", "xịt khoáng",
        #        "nước hoa hồng", "quạt", "chăn", "gối"]
        key = [ "quạt", "chăn", "gối"]
        # key = ["nước hoa hồng"]
        for q in key:
            print(q)
            response = self.call_api(q)
            result = response.json()
            for i in range(len(result['result']['products'])):

                if q in (result['result']['products'][i]['name']):
                    pass
                elif q in (result['result']['products'][i]['categories'][0]['name']):
                    pass
                elif q in (result['result']['products'][i]['attributeSet']['name']):
                    pass
                else:
                    print("fail")
                    print(result['result']['products'][i]['sku'])
                    print(result['result']['products'][i]['name'])
                    print(result['result']['products'][i]['categories'][0]['name'])
                    print(result['result']['products'][i]['attributeSet']['name'])
                    print("------------------")



            # for j in range(len(result['result']['products'])):
            #     if q in (result['result']['products'][j]['name']):
            #         print("pass")
            #     elif q in (result['result']['products'][j]['categories'][0]['name']):
            #         print("pass")
            #     elif q in (result['result']['products'][j]['attributeSet']['name']):
            #         print("pass")
            #     else:
            #         print("fail")

