import numpy as np

# Function to recursively calculate the max difference in a sublist
def max_difference_calc(arr_temp, difference = -1):
  if not arr_temp:
    return difference
  
  else:
    max_value, index_max = max(arr_temp), np.argmax(arr_temp)

    if (index_max > 0) and (max_value - min(arr_temp[:index_max])) > (difference + 1):
      difference = max_value - min(arr_temp[:index_max])

    return max_difference_calc(arr_temp[index_max+1:], difference)


# keep this function call here 
print(max_difference_calc(input()))

# Example input: [14,20,4,12,5,11]