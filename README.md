# ToyMoney
Make and use toy-money easily with REST API.
The money said below is not-real money.

Features:
- User can have a wallet.
- User can give their money to otherone with message.
- User can get transaction histories.
- User can buy products from machines.
- User can list their bought products.
- User can watch their money ranking.
- Admin can make a machine sells products.
- Admin can make an airdrop that gives money per specified time.
- Admin can set transaction fee.
- Admin can get all transaction history.
- Admin can control user's wallet.

API Map:

User
- wallets GET
- wallets POST
- wallets/properties GET
- wallets/transactions GET
- wallets/transactions/create POST
- wallets/ranking GET
- wallets/list GET (Admin only)
- wallets/<wallets_id> GET (Admin only)
- wallets/<wallets_id> PUT (Admin only)
- wallets/<wallets_id> DELETE (Admin only)
- transactions GET (Admin only)
- transactions/fee GET (Admin only)
- transactions/fee PUT (Admin only)

Machine
- machines GET
- machines POST (Admin only)
- machines/<machine_id:int> GET
- machines/<machine_id:int> PUT (Admin only)
- machines/<machine_id:int> DELETE  (Admin only)
- machines/<machine_id:int>/<product_id>/buy POST
※自販機名も商品リストもPUTで指定できる
※内部的にユーザーIDも作成して管理する

Product
- products GET
- products POST (Admin only)
- products/<product_id:int> GET
- products/<product_id:int> PUT (Admin only)
- products/<product_id:int> DELETE (Admin only)
※商品は自販機に後で個別に設定する

Airdrop
- airdrops GET
- airdrops POST (Admin only)
- airdrops/<airdrop_id:int> GET
- airdrops/<airdrop_id:int> PUT
- airdrops/<airdrop_id:int>/claim POST
