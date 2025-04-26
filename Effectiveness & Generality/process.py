import json
import os
result_list=[] 
tut=[]
script_dir = os.path.dirname(os.path.abspath(__file__))

def process_pmp(input_pmp_path):
    try:
        with open(input_pmp_path, 'r',encoding='cp850') as file:
            for line in file:
                if '(' in line and ')' in line:
                    func_name, args = line.split('(', 1)
                    if func_name=='force':
                        continue
                    args = args.rstrip(')\n')
                    args=args.split(',')
                    for i in range(0,len(args)):
                        if 'char_t*)' not in args[i]:
                            args[i]='num'
                    args=str(args)
                    tut.append(str([func_name,args]))
                    if(func_name in func_pmp_dict.keys()):
                        if args in func_pmp_dict[func_name]:
                            pass
                        else:
                            func_pmp_dict[func_name].append(args)
                    elif len(func_name) > 2 and func_name != 'timeGetTime':
                        func_pmp_dict[func_name]=[args]
            
    except FileNotFoundError:
        print(f"File not found: {input_pmp_path}")
def process_vmforce(input_vmforce_path):
    try:
        for root, dirs, files in os.walk(input_vmforce_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='cp850') as file:
                    func_vmforce_dict = dict()
                    for line in file:
                        if '(' in line and ')' in line:
                            func_name, args = line.split('(', 1)
                            if func_name == 'force':
                                continue
                            args = args.rstrip(')\n')
                            args = args.split(',')
                            for i in range(len(args)):
                                if 'char_t*)' not in args[i]:
                                    args[i] = 'num'
                            args = str(args)
                            if func_name in func_vmforce_dict.keys():  
                                if args in func_vmforce_dict[func_name]:  
                                    pass
                                else:
                                    func_vmforce_dict[func_name].append(args)
                            elif len(func_name) > 2 and func_name != 'timeGetTime':  
                                func_vmforce_dict[func_name] = [args]  
                    func_vmforce_dicts[file_name]=func_pmp_dict
    except FileNotFoundError:
        print(f"File not found: {input_vmforce_path}")
    
    return func_vmforce_dicts
def process_cuckoo(input_cuckoo_path):
    try:
        with open(input_cuckoo_path, 'r') as json_file:
            data = json.load(json_file)
        data = data['behavior']['apistats']
        data = next(iter(data.values()))
        for item in data:
            api_cuckoo_names.add(item)
    except Exception as e:
        print(f"error when processing {input_cuckoo_path}: {e}")

def compare():
    func_pmp_compare_set=set(func_pmp_dict.keys())
    func_diff_pmp_cuckoo=func_pmp_compare_set.difference(api_cuckoo_names)

    result.write("hidden api:"+str(len(func_diff_pmp_cuckoo))+"\n")
    sum=0
    for i in func_diff_pmp_cuckoo:
        result.write(i+'\n')
        sum+=len(func_pmp_dict[i])
    result.write("--------------------------------------\n")

    for key,value in func_vmforce_dicts.items():
        result.write(key+'\n')
        func_vmforce_compare_set=set(value.keys())
        func_diff_vmforce_cuckoo=func_vmforce_compare_set.difference(api_cuckoo_names)
        result.write("hidden api :"+str(len(func_diff_vmforce_cuckoo))+'\n')
        for i in func_diff_pmp_cuckoo:
            result.write(i+'\n')
        result.write("--------------------------------------\n")

for i in [1, 2, 3, 4, 5, 6]:
    vmforce_lines = []
    result = open(os.path.join(script_dir, f'./rq2-{i}_result.txt'), 'w')
    func_pmp_set = set()
    func_pmp_dict = dict()
    func_vmforce_dicts = dict()
    func_pmp_compare_set = set()
    api_cuckoo_names = set()
    cuckoo_path = os.path.join(script_dir, f'./rq2-{i}/logs/cuckoo/report.json')
    pmp_path = os.path.join(script_dir, f'./rq2-{i}/logs/pmp/stap_log.txt')
    vmforce_path = os.path.join(script_dir, f'./rq2-{i}/logs/VMForce')
    process_cuckoo(cuckoo_path)
    process_pmp(pmp_path)
    process_vmforce(vmforce_path)
    compare()

    