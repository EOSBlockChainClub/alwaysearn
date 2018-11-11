import requests
import json
import traceback
import pprint
import pyeosio

with open('config.json', 'r') as f:
    config = json.load(f)
    TELEGRAM_API_KEY = config['telegram']

class EncryptRecorder(object):
    def __init__(self):
        self.client = EosClient(
                api_endpoint="http://etos.ciceron.xyz:8888", 
                wallet_endpoint="http://etos.ciceron.xyz:8900"
                )   

    def getUpdates(self, last_update_id=0):
        api_get_updates = 'https://api.telegram.org/bot{}/getUpdates'.format(TELEGRAM_API_KEY)
        payloads = {'offset': last_update_id}
        resp = requests.post(api_get_updates, data=payloads)
        res = resp.json()
        msg_list = res.get('result')
        return msg_list

    def read_last_update_id(self):
        with open('updateid_translation.txt', 'r') as f:
            last_update_id = f.read()
        return last_update_id

    def write_last_update_id(self, last_update_id):
        with open('updateid_translation.txt', 'w') as f:
            f.write(str(last_update_id))
        return

    def bidrecord(self, name, str_name, website, price):
        txBuilder = TransactionBuilder(self.client)

        try:
            self.client.wallet_unlock('PW5JhMP6LxXqKNtRjZC28sNGdTHjUCxcztRankRPsZRrTzBu84WsT')
        except:
            pass

        param = { 
                  "action": "addbid",
                  "code": "bryanrhee",
                  "args": {
                      "name": name,
                      "strname": str_name,
                      "website": website,
                      "price": "{} LCT".format(price)
                  }   
                }
        print("JSON to Bin")
        bin_param = self.client.chain_abi_json_to_bin(param)
        print(bin_param)
        act = Action("bryanrhee", "recorddata", "bryanrhee", "active", bin_param['binargs'])
        print("Sign")
        ready_tx, chain_id =  txBuilder.build_sign_transaction_request([act])
        signed_transaction = self.client.wallet_sign_transaction(ready_tx, ['EOS4xei1fKyvZaf4j4L886PKBNjigecy32ehru2DcSH9MLNuQtuTt'], chain_id)
        pprint.pprint(signed_transaction)
        print("Push")

        try:
            ret = self.client.chain_push_transaction(signed_transaction)
            print(ret)
        except:
            traceback.print_exc()

        print("Complete")

    def getBiddingStatus(self):
        # Get table
        rows = self.client.chain_get_table_rows("bryanrhee", "bryanrhee", "bidder", True, 10) 
        pprint.pprint(rows)
        return rows['rows']

    def getCurrPrice(self):
        # Get table
        rows = self.client.chain_get_table_rows("bryanrhee", "bryanrhee", "minprice", True, 10) 
        pprint.pprint(rows)
        if len(rows['rows']) < 1:
            return None

        token_price = rows['rows'][0]['price']
        return token_price

    def main(self):
        last_id = self.read_last_update_id()
        msg_list = self.getUpdates(last_id)

        # Ready
        for unit_chat in msg_list:
            last_id = unit_chat.get('update_id')
            unit_msg = unit_chat.get('message')

            if unit_msg is None:
                continue

            from_obj = unit_msg.get('from')
            if from_obj is not None:
                user = from_obj.get('username')
            else:
                continue

            text = unit_msg.get('text')
            photo = unit_msg.get('photo')
            if text is None:
                continue

            if text == '/price_koen':
                token_price = self.getCurrPrice()
                cur_fiat = 10
                unit_token_price = 


            elif text == '/bidstatus':
                pass

            elif text == '/bid':
                pass

            elif photo is not None:

                text = 'File uploaded'
                pass

            print("User: {} | Text: {}".format(user, text))

        self.write_last_update_id(int(last_id)+1)


if __name__ == "__main__":
    rec = EncryptRecorder()

    while True:
        rec.main()
