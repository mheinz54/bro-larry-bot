from datetime import datetime


class HeartSanctifier:
    def __init__(self):
        self.heart = ["Worldly Distractions"]
        self.presence_of_god = False
        self.last_reset = None

    def empty_heart(self):
        self.heart.clear()
        return "🧹 Heart emptied of distractions."

    def invite_god(self):
        if not self.heart:
            self.presence_of_god = True
            return "🕊️ God invited into the heart."
        else:
            return "⚠️ Heart not ready—please surrender first."

    def allow_god_to_act(self):
        if self.presence_of_god:
            return "✨ God moves freely within the soul."
        else:
            return "🚫 Access restricted—deepen surrender."

    def surrender(self):
        return self.empty_heart() + "\n" + self.invite_god() + "\n" + self.allow_god_to_act()

    def reset_heart(self):
        """Reset the heart to its initial state"""
        self.heart = ["Worldly Distractions"]
        self.presence_of_god = False
        self.last_reset = datetime.now()
