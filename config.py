import os
import base64
import dotenv

dotenv.load_dotenv('.env')

server_error_codes = ["<Response [500]>", "<Response [501]>", "<Response [502]>", "<Response [503]>",
                      "<Response [504]>", "<Response [520]>", "<Response [521]>", "<Response [522]>",
                      "<Response [523]>", "<Response [524]>"]

area_codes = ['13', '14', '15', '16', '17', '18', '21', '22', '23', '25', '29', '33', '44']

company_id = os.environ['company_id']

auth = base64.b64encode(bytes(f'{company_id}:{os.environ["api_key"]}'.encode("UTF-8")))

url_update_access_tokens_a1 = "https://vats.a1.by/crm-api/open-api/v1/auth/tokens"
