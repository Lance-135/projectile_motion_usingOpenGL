import math



x0 = 0
y0 = 0
u = 60
g = 9.8
dt = 0.01
angle = 45
rad_angle = math.radians(angle)
v_x = u * math.cos(rad_angle)
v_y = u * math.sin(rad_angle)

def calcPoints(x0, y0, g, dt, v_x, v_y):
    points = []
    while y0>=0: 
        x0 += v_x*dt
        y0 += v_y*dt
        v_y -= g*dt
        points.append((x0, y0))
    return points

print(calcPoints(x0, y0, g, dt, v_x, v_y))