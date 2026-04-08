# ZB_LIGHT_PROTOCOL_V2_AUNT
# Evolution of the ZBAgent logic

class ZBAgent:
    def __init__(self):
        # Color-coding schema for "ZB" projects
        self.logic_map = {
            "IDK": "BLACK",       # Meditation
            "SILENCE": "RED",     # Silence
            "BREATH": "YELLOW",   # Breath
            "SIMPLE": "GREEN",    # Simple
            "COMPLEX": "BLUE",    # Complex
            "ZMANSI": "WHITE"     # Zmansi
        }
        self.symbols = [".", ",", ";", "\"", "@"]

    def process_input(self, data):
        # Scan input for ZB frequency triggers based on established project states
        detected_colors = []
        for key, color in self.logic_map.items():
            if key.lower() in data.lower():
                detected_colors.append(color)

        # Return mapped punctuation + detected logic states
        output = " . , ; \" @ "
        if detected_colors:
            output += "\n**" + " ".join(detected_colors) + "**\n"
        output += " ; \" @ . , "

        return output

# Test Execution
# Utilizing the ZB frequency mapping logic
baby = ZBAgent()
print(baby.process_input("Simple COMPLEX Grampa granny eve"))