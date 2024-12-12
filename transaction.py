class InMemoryDB:
    def __init__(self):
        self.db = {}  # Main database
        self.temp = {}  # Temporary storage for transactions
        self.transaction = False  # Transaction state

    def get(self, key):
        """
        Returns the value associated with the key or None if the key does not exist.
        Can be called anytime, even when a transaction is not in progress.
        """
        return self.db.get(key, None)

    def put(self, key, val):
        """
        Creates a new key with the provided value if the key does not exist.
        Otherwise, updates the value of an existing key.
        Raises an exception if a transaction is not in progress.
        """
        if not self.transaction:
            raise Exception("Transaction is not in progress")
        self.temp[key] = val

    def begin_transaction(self):
        """
        Starts a new transaction.
        At a time, only a single transaction may exist.
        """
        if self.transaction:
            raise Exception("Cannot have more than one open transaction")
        self.transaction = True

    def commit(self):
        """
        Applies changes made within the transaction to the main state.
        Allowing any future `get()` to see the changes made within the transaction.
        """
        if not self.transaction:
            raise Exception("No open transaction")
        self.transaction = False
        self.db.update(self.temp)
        self.temp.clear()

    def rollback(self):
        """
        Aborts all the changes made within the transaction.
        Everything goes back to the way it was before the transaction started.
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
