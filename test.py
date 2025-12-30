from database.transaction_model import TransactionModel
from datetime import date

if __name__=="__main__":

    # init model
    transaction_model = TransactionModel()

    # define params:
    transaction_type = "Income"
    category = "Shopping"
    amount = 234
    transaction_date = date.today()

    new_transaction = transaction_model.add_new_transaction(
        transaction_type=transaction_type,
        category=category,
        amount=amount,
        transaction_date=transaction_date,
        description= None # or skip pass
    )
    print(f"New transaction created!! {new_transaction}")

    # test delete
    result = transaction_model.delete_transaction(transaction_id=new_transaction)
    print(f"Delete Success: {result} record")