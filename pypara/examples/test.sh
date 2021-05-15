pypara -p example1.py
# use ruuning function from example1.py with given generator
pypara -p example1.py -g "1 2 3"
# use generator from example1.py with given running command
pypara -p example1.py -r "echo cmd{f}"
# Pass argument to generator in example2.py
pypara -p example2.py --run "echo cmd{f}" --count 3
# With pipe
echo "0 1 2" | pypara -g - --run "echo cmd{f}"
# Change spliting character
pypara -g "0_1_2" --run "echo cmd{f}" --splitby "_"
# Example for process lock
pypara -p example3.py 
pypara -p example3.py --lock
