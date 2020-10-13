# ToyMoney
Make and use toy-money easily with REST API.
The money said below is not-real money.

## Features
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

## API endpoints
Users
- users/create POST
- users/assets GET
- users/assets/use POST
- users/money GET
- users/transactions GET
- users/transactions/create POST
- users/ranking GET
- users/<user_id:int> GET
- users/admin/list GET (Admin only)
- users/admin/<user_id:int> GET (Admin only)
- users/admin/<user_id:int> PUT (Admin only)
- users/admin/<user_id:int> DELETE (Admin only)

Transactions
- transactions GET (Admin only)

Machine
- machines/list GET
- machines/create POST (Admin only)
- machines/<machine_id:int> GET
- machines/<machine_id:int> PUT (Admin only)
- machines/<machine_id:int> DELETE  (Admin only)
- machines/<machine_id:int>/<product_id>/buy POST  
※自販機名も商品リストもPUTで指定できる  
※内部的にユーザーIDも作成して管理する  

Product
- products/list GET
- products/create POST (Admin only)
- products/<product_id:int> GET
- products/<product_id:int> PUT (Admin only)
- products/<product_id:int> DELETE (Admin only) 
- products/<product_id>/buy POST
※自販機に関係なく直接購入もできる

Airdrop
- airdrops/list GET
- airdrops/list_with_status GET
- airdrops/create POST (Admin only)
- airdrops/<airdrop_id:int>/status GET
- airdrops/<airdrop_id:int>/claim POST
- airdrops/<airdrop_id:int> GET
- airdrops/<airdrop_id:int> PUT (Admin only)
- airdrops/<airdrop_id:int> DELETE (Admin only) 
