import client

class Main():
    def __init__(self):
        self.client = client.Client()
        self.client.main() 

if __name__ == "__main__":
    main = Main()