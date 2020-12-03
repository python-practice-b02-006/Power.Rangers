from modules import vectors

class Field():

    def __init__(self, B, E):
         self.B = vectors.Vector(B[0], B[1], B[2])
         self.E = vectors.Vector(E[0], E[1], E[2])

    def calculate_force(self, bullets):
        local = bullets
        for body in local:
            body.force = 0 * body.force
                    
            body.force = body.force + body.m_c * body.vel @ self.E 
            body.force = body.force - body.m_c * self.B
                
            body.force = body.force + body.e_c * body.vel @ self.B 
            body.force = body.force + body.e_c * self.E
            
        return local

if __name__ == "__main__":
    print("This module is not for direct call!")


