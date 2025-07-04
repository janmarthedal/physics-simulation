import time
import numpy as np
import skfem as fem
from skfem.helpers import dot, grad
from skfem.io.meshio import from_meshio
from mesh.meshio import to_meshio
from mesh.generate import rect2d


@fem.BilinearForm
def a(u, v, _):
    return dot(grad(u), grad(v))


@fem.LinearForm
def lf(v, w):
    x, y = w.x  # global coordinates
    f = np.sin(np.pi * x) * np.sin(np.pi * y)
    return f * v


# mesh = Mesh.load("rect.vtu")
mesh = rect2d(1.0, 1.0, 90, 90, addz=False)

t1 = time.time()
mesh = from_meshio(to_meshio(mesh))
t2 = time.time()

Vh = fem.Basis(mesh, fem.ElementTriP1())

t3 = time.time()
A = a.assemble(Vh)
t4 = time.time()
b = lf.assemble(Vh)
t5 = time.time()
D = Vh.get_dofs()
cond = fem.condense(A, b, D=D)
x = fem.solve(*cond)

print(f"A size: {A.shape}")
# print(f"Condensed: {cond}")
print(f"x: {x}")
print(f"Time from_meshio: {t2 - t1}")
print(f"Time basis: {t3 - t2}")
print(f"Time A: {t4 - t3}")
print(f"Time b: {t5 - t4}")

np.set_printoptions(linewidth=200, precision=4)

if A.shape[1] < 0:
    print(A.toarray())
    print(b)
