from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
import uuid
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Хранилище для общих счетов
shared_accounts = {}

class SharedAccount(Resource):
    def post(self):
        data = request.get_json()

        owner = data.get('owner')
        card_ids = data.get('cardIds')

        if not owner or not isinstance(card_ids, list) or not card_ids:
            return {'error': 'Invalid request data'}, 400

        account_id = str(uuid.uuid4())
        new_account = {
            'accountId': account_id,
            'owner': owner,
            'cardIds': card_ids,
            'balance': 0,  # Инициализация баланса
            'creationDate': datetime.utcnow().isoformat()
        }

        shared_accounts[account_id] = new_account
        return new_account, 201

    def get(self, account_id):
        account = shared_accounts.get(account_id)

        if not account:
            return {'error': 'Shared account not found'}, 404

        return account, 200

    def delete(self, account_id):
        if account_id not in shared_accounts:
            return {'error': 'Shared account not found'}, 404

        del shared_accounts[account_id]
        return '', 204

    def put(self, account_id):
        account = shared_accounts.get(account_id)

        if not account:
            return {'error': 'Shared account not found'}, 404

        data = request.get_json()
        amount = data.get('amount', 0)

        if amount <= 0:
            return {'error': 'Amount must be positive'}, 400

        account['balance'] += amount
        return {'accountId': account_id, 'newBalance': account['balance']}, 200

# Настройка маршрутов
api.add_resource(SharedAccount, '/shared-accounts', '/shared-accounts/<string:account_id>')

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True, port=3000)
