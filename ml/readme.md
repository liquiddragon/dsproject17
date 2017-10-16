# Learning and Inference code

## TODO:

* I think we should generate a Python list of all data files for easy loading and manipulation
* Load data files and interpolate their values in a meaningful way
* For data that ends before 2015, extrapolate the data to reach 2015 if possible
  * Another option is to use 3 years lag for data sets that end earlier (this should be OK)
* Create a numpy array with feature rows in the following way:
  * Use years 1970 - 2000 as the years used for training features **X**
  * Use GDP increase between the year in X and year X+15 as **Y** value
  * Introduce 5-10 year time lag for features where it is possible
* Train! :)
  * For GDP, we can use normalized GDP as one of the features in **X**
  * For **Y** we should treat the GDP in **X** as *1* and **Y** should be equal to the fraction of the the GDP in **X**
  * For example, if GDP grew *10%* in 15 years between **X** and **Y**, the value of **Y** should be *1.10*, conversely,
  if GDP decreased *10%* the value in **Y** should be *0.90*. Would that make sense?