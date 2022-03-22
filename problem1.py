from math import exp

def LogitRegression(arr):

  # code goes here
  x, y = arr[0], arr[1]
  a, b = arr[2], arr[3]
  # Assuming learning rate = 1
  L = 1

  # Calculating the prediction
  y_pred = 1 / (1 + exp(-b + -a*x))

  # Calculating derivatives
  D_a = x * exp(-a*x - b) / (1 + exp(-a*x -b))**2
  D_b = exp(-a*x - b) / (1 + exp(-a*x -b))**2

  D_La = -y * D_a / y_pred + (1 - y) * D_a / (1-y_pred)
  D_Lb = -y * D_b / y_pred + (1 - y) * D_b / (1-y_pred)

  # Update a and b
  a1 = a + D_La
  b1 = b + D_Lb

  return '{:.3f}, {:.3f}'.format(a1, b1)

# keep this function call here 
print(LogitRegression(input()))

# Example of test Input = [1, 1, 1, 1]

