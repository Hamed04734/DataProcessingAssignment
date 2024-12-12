class InMemoryDB:
    def __init__(self):
        self.db = {}  # Stores the primary state of the database
        self.temp = {}  # Temporary storage for changes during a transaction
        self.transaction = False  # Indicates if a transaction is currently active

    def get(self, key):
        """
Retrieves the value for the given key from the main database. If the key does not exist, returns None.
    This method can be used regardless of whether a transaction is active.
        """
        return self.db.get(key, None)

    def put(self, key, val):
        """
        adds a new key-value pair to the temporary transaction storage or updates the value
        of an existing key. 
        Raises an exception if no transaction is in progress.
        """
        if not self.transaction:
            raise Exception("Transaction is not in progress")
        self.temp[key] = val

    def begin_transaction(self):
        """
    Initializes a transaction. Prevents starting another transaction if one is already active.
     During a transaction, changes are stored in a temporary buffer and only
        applied to the main database upon commit.
        """
        if self.transaction:
            raise Exception("Cannot have more than one open transaction")
        self.transaction = True

    def commit(self):
        """ Finalizes the active transaction by merging the temporary changes 
         Clears the transaction state and temporary buffer after committing.
        """
        if not self.transaction:
            raise Exception("No open transaction")
        self.transaction = False
        self.db.update(self.temp)
        self.temp.clear()

    def rollback(self):
        """
        Cancels all changes made during the active transaction, restoring the database
        to its previous state. Clears the transaction state and temporary buffer.
        """
        if not self.transaction:
            raise Exception("No ongoing transaction")
        self.transaction = False
        self.temp.clear()


def main():
    transaction = InMemoryDB()

    print("Welcome, this is an in-memory database with transaction support!")
    print("Type 'QUIT' to leave the database. Type 'HELP' for all available commands.")

    cont = True

    while cont:
        try:
            user_input = input(">>> ").strip()

            if user_input == "BEGIN TRANSACTION":
                transaction.begin_transaction()

            elif user_input == "GET":
                key = input("What key do you want to get? ").strip()
                print(transaction.get(key))

            elif user_input == "PUT":
                key = input("Key: ").strip()
                value = int(input("Value: ").strip())
                transaction.put(key, value)

            elif user_input == "COMMIT":
                transaction.commit()

            elif user_input == "ROLLBACK":
                transaction.rollback()

            elif user_input == "HELP":
                print("All Commands:")
                print("BEGIN TRANSACTION")
                print("GET")
                print("PUT")
                print("COMMIT")
                print("ROLLBACK")
                print("QUIT")

            elif user_input == "QUIT":
                cont = False

            else:
                print("Unknown command. Type 'HELP' for a list of commands.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
