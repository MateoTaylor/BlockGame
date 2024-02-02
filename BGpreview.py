'''elif self.blocks[0].rect.bottom + self.bottom > 479: #collisions for bottom side
                for b in self.blocks:
                    if mouseposreal[1] > 449:
                        b.pos.y = 420 + ((self.block_positions[self.blocks.index(b)][1]))
                    else: b.pos.y = CELL_SIZE*round(mouseposreal[1]/CELL_SIZE) + (self.block_positions[self.blocks.index(b)][1])
            

elif self.blocks[0].rect.bottom + self.bottom > 479: #collisions for bottom side
                for b in self.blocks:
                    if mouseposreal[1] > 419:
                        b.pos.y = 420 + ((self.block_positions[self.blocks.index(b)][1]))
                    else: b.pos.y = mouseposreal[1] + (self.block_positions[self.blocks.index(b)][1])
                    '''

class birds:
    def __init__(self):
        self.y = [1,2,3]
        x = self.y.copy()
        x[0] = 0
        print(self.y)

birds()
