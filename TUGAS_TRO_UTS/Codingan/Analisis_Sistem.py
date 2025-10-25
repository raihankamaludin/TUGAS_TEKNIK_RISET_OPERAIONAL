import numpy as np
from scipy.optimize import linprog

# Nama gudang dan toko
warehouses = ['Bandung', 'Bekasi']
stores = ['Cimahi', 'Bogor', 'Cirebon', 'Depok', 'Karawang', 'Dummy']

# Biaya per unit (Dummy = 0.01)
cost = np.array([
    [4, 3, 5, 2, 2, 0.01],
    [2, 1, 1, 4, 3, 0.01]
])

# Supply & Demand (+ dummy)
supply = np.array([90, 120])
demand = np.array([40, 50, 45, 30, 25, 20])  # total 210 = total supply

# Flatten biaya
c = cost.flatten()

# Constraint supply
A_eq = []
for i in range(len(supply)):
    row = [0]*len(c)
    row[i*len(demand):(i+1)*len(demand)] = [1]*len(demand)
    A_eq.append(row)

# Constraint demand
for j in range(len(demand)):
    row = [0]*len(c)
    for i in range(len(supply)):
        row[i*len(demand)+j] = 1
    A_eq.append(row)

b_eq = np.concatenate([supply, demand])

# Bounds variabel >=0
x_bounds = [(0, None)]*len(c)

# Jalankan linprog
res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=x_bounds, method='highs')

# Output
if res.success:
    allocation = res.x.reshape(len(supply), len(demand))
    
    # Tabel rapi
    print("{:<10}".format("Gudang/Toko"), end="")
    for store in stores[:-1]:
        print("{:>10}".format(store), end="")
    print()
    
    for i, wh in enumerate(warehouses):
        print("{:<10}".format(wh), end="")
        for j in range(len(stores)-1):
            print("{:>10}".format(int(allocation[i,j])), end="")
        print()
    
    total_cost = np.sum(allocation[:,:-1]*cost[:,:-1])
    print(f"\nTotal Biaya Minimum: {total_cost:.2f}")
else:
    print("Solver gagal:", res.message)






