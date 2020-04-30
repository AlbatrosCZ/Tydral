class forAll:
    def __init__(self):
        self.null()

    def set_(self, events):
        self.mouse_up = [False, []]
        self.key_up = [False, []]

        if self.mouse_down[0]:
            for i in self.mouse_down[2].keys():
                if self.mouse_down[2][i] == 0:
                    self.mouse_down[2][i] = 1

        for event in events:
            if event.type == 2: # KeyDown
                self.key_down[0] = True
                self.key_down[1].append([event.key, event, 0])

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
                self.mouse_down[2][event.button] = 0

            elif event.type == 6: # MouseButtonUp
                for i in range(len(self.mouse_down[1])):
                    if self.mouse_down[1][i] == event.button:
                        del self.mouse_down[1][i]
                        self.mouse_down[2][event.button] = -1
                        break
                if self.mouse_down[1] == []:
                    self.mouse_down[0] = False
                self.mouse_up[0] = True
                self.mouse_up[1].append(event.button)

            elif event.type == 12: # Quit
                return True

        if self.key_down[0]:
            for i in range(len(self.key_down[1])):
                self.key_down[1][i][2] += 1

        
        return False
    
    def null(self):
        self.mouse_down = [False, [], {}]
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
            
    def is_in(self, key):
        if type(key) == str:
            for i in self.key_down[1]:
                if i[1].unicode == key:
                    return True, i[2]
        elif type(key) == int:
            for i in self.key_down[1]:
                if i[0] == key:
                    return True, i[2]
        return False, 0