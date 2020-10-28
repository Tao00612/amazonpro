import random


def cookies_list():
	cookies_lists = [
		'session-id=459-6793643-9024842; i18n-prefs=CNY; ubid-acbcn=460-2861381-0690269; session-id-time=2082729601l; session-token=K9jvSDvFcyR1w/LfT7RcWixEch9Djf/JAUjFuubalV6yls0yv2Lk9k4mvZd0AZ7ObsL+pJrUtjGNLIYeOjimhT8VaNPrHPrikI3i+vYKMU4N9fgAf35NGVuIWksh1TchRG2JP914EMOFkTGB38f7KLDdYFB3JXWr2gSX/73KVhTnTfgivYY+zquNs9xTRKKYLIgr1RKtQPEXdHH/3IaJT4OR5LViC9vP9piVHvMazrc2pcc1RHDLog==; csm-hit=tb:KR7QNEWZ9SZ9D5P0HH09+s-KR7QNEWZ9SZ9D5P0HH09|1603804118397&t:1603804118397&adb:adblk_no',

	]

	return cookies_lists


def get_cookies_dict():
	cookie = cookies_list()
	cookie = random.choice(cookie)
	cookie_dict = {
		c.split('=')[0].strip(): c.split('=')[-1].strip()
		for c in cookie.split(';')
	}
	return cookie_dict
