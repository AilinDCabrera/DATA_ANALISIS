import numpy as np

def walsh_test(data, alpha=0.05):
    """
    Walsh's Test for Large Sample Sizes
    
    Parameters:
    - data: Array-like object containing the data
    - alpha: Significance level
    
    Returns:
    - outliers: Array containing the indices of the outliers
    """
    n = len(data)
        
    if n <= 60:
        print("Sample size is too small. Walsh's test should not be applied.")
    elif n <= 220:
        alpha = 0.10
        
    c = int(np.ceil(np.sqrt(2 * n)))
    b2 = 1/alpha
    b = np.sqrt(b2)
    a = (1+b*np.sqrt((c-b2)/(c-1)))/(c-b2-1)
        
    # Step 1: Check if the r smallest points are outliers
    for i in range(n):
        k = i + c
        if data[i] - (1 + a) * data[i + 1] + a * data[k] < 0:
            outliers_small.append(i)
        elif data[i] - (1 + a) * data[i + 1] + a * data[k] >= 0:
            if i > 0:
                thrs_outlier_small =  data[i - 1]
            else:
                thrs_outlier_small =  None
            break
        
    # Step 2: Check if the r largest points are outliers
    for i in range(n,0, -1): 
        k = i + c
        if data[n+1-i] - (1 + a) * data[n - i] + a * data[n +1- k] <= 0:
            if i < n:
                thrs_outlier_large = data[i + 1]
            elif i == n:
                thrs_outlier_large = None
            break
        
    # Step 3: Combine small and large thrs
    outliers = {"thrs_small":thrs_outlier_small, "thrs_large": thrs_outlier_large}
    
    return outliers

# Example usage:
# data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]  # Sample data
# outliers = walsh_test(data)
# print("Indices of outliers:", outliers)
# print("Outliers:", [data[i] for i in outliers])
