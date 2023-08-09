class bot_entry_point:
    def interaction(self, input_message: str) -> str:
        # You can add additional logic here if needed
        return 'Success'

# This allows the class to be used as a standalone script or as an imported module.
if __name__ == '__main__':
    bot = bot_entry_point()
    message = input("Enter a message: ")
    print(bot.interaction(message))
