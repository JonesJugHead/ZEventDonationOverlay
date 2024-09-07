import tkinter as tk
from tkinter.font import Font
import requests
import time

class TransparentOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.7)  # Set transparency level (0.0 to 1.0)
        self.root.attributes('-topmost', True)  # Keep the window on top
        self.root.overrideredirect(True)  # Remove window decorations

        # Define a monospaced font
        self.font = Font(family="Courier", size=14)
        
        self.label = tk.Label(self.root, text="Dons: 0€", font=self.font, fg='white', bg='black')
        self.label.pack()

        self.current_amount = 0.0
        self.target_amount = 0.0

        self.update_donation()

    def fetch_donation_amount(self):
        try:
            response = requests.get('https://zevent.fr/api/')
            if response.status_code == 200:
                data = response.json()
                return float(data["donationAmount"]["number"])
            else:
                return self.current_amount  # If there's an error, return the current amount
        except Exception as e:
            return self.current_amount  # If there's an error, return the current amount

    def format_amount(self, amount):
        return "{:,.2f}€".format(amount).replace(",", " ").replace(".", ",")

    def animate_donation(self):
        if self.current_amount < self.target_amount:
            step = (self.target_amount - self.current_amount) / 20  # Adjust the divisor for speed
            self.current_amount += step
            self.label.config(text=self.format_amount(self.current_amount))
            self.root.after(50, self.animate_donation)  # Adjust the interval for smoothness
        else:
            self.current_amount = self.target_amount
            self.label.config(text=self.format_amount(self.current_amount))

    def update_donation(self):
        self.target_amount = self.fetch_donation_amount()
        self.animate_donation()
        self.root.after(5000, self.update_donation)  # Update every 5 seconds

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    overlay = TransparentOverlay()
    overlay.run()
