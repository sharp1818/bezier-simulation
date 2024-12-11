import cv2
import numpy as np
import time

width, height = 900, 600
canvas = np.zeros((height, width, 3), dtype=np.uint8)
positions = []
fade_duration = 5

def bezier_curve(points, num_points=100):
    n = len(points) - 1
    bezier_points = []
    for t in np.linspace(0, 1, num_points):
        x = sum((np.math.comb(n, i) * (1 - t) ** (n - i) * t ** i * points[i][0])for i in range(n + 1))
        y = sum((np.math.comb(n, i) * (1 - t) ** (n - i) * t ** i * points[i][1])for i in range(n + 1))
        bezier_points.append((int(x), int(y)))
    return bezier_points

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        current_time = time.time()
        positions.append(((x, y), current_time))

cv2.namedWindow("Mouse Tracker")
cv2.setMouseCallback("Mouse Tracker", mouse_callback)

while True:
    canvas[:] = (0, 0, 0)
    current_time = time.time()
    recent_positions = [(pos, t) for pos, t in positions if current_time - t <= fade_duration]

    for i in range(1, len(recent_positions)):
        cv2.line(canvas, recent_positions[i - 1][0], recent_positions[i][0], (0, 255, 0), 2)

    if len(recent_positions) > 2:
        bezier_points = bezier_curve([pos for pos, _ in recent_positions])
        for i in range(len(bezier_points) - 1):
            cv2.line(canvas, bezier_points[i], bezier_points[i + 1], (255, 0, 0), 2)

    cv2.putText(canvas, "Curva de Bezier", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(canvas, "Movimiento del mouse", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    positions = recent_positions
    cv2.imshow("Mouse Tracker", canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
