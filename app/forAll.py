class forAll:
    def __init__(self):
        self.null()

    def set_(self, events):
        self.mouse_up = [False, []]
        self.key_up = [False, []]

        for event in events:
            if event.type == 2: # KeyDown
                self.key_down[0] = True
                self.key_down[1].append([event.key, event])

            elif event.type == 3: # KeyUp
                for i in range(len(self.key_down[1])):
                    if self.key_down[1][i][0] == event.key:
                        del self.key_down[1][i]
                        break
                if self.key_down[1] == []:
                    self.key_down[0] = False
                self.key_up[0] = True
                self.key_up[1].append([event.key, event])

            elif event.type == 5: # MouseButtonDown
                self.mouse_down[0] = True
                self.mouse_down[1].append(event.button)

            elif event.type == 6: # MouseButtonUp
                for i in range(len(self.mouse_down[1])):
                    if self.mouse_down[1][i] == event.button:
                        del self.mouse_down[1][i]
                        break
                if self.mouse_down[1] == []:
                    self.mouse_down[0] = False
                self.mouse_up[0] = True
                self.mouse_up[1].append(event.button)

            elif event.type == 12: # Quit
                return True

        return False
    
    def null(self):
        self.mouse_down = [False, []]
        self.key_down = [False, []]

        self.mouse_up = [False, []]
        self.key_up = [False, []]

    def get_mouse(self):
        if self.mouse_down[0] == False and self.mouse_up[0] == False:
            return False, False
        elif self.mouse_down[0] == False:
            return False, self.mouse_up[1]
        elif self.mouse_up[0] == False:
            return self.mouse_down[1], False
        else:
            return self.mouse_down[1], self.mouse_up[1]
        
    def get_keys(self):
        if self.key_down[0] == False and self.key_up[0] == False:
            return False, False
        elif self.key_down[0] == False:
            return False, self.key_up[1]
        elif self.key_up[0] == False:
            return self.key_down[1], False
        else:
            return self.key_down[1], self.key_up[1]
            