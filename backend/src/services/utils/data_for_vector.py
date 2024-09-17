import json 
import os
import re

data_dir = '/hdd-6tb/nghiavm/DATN/gen_instruction/data/instructions_new.jsonl'

save_data = '/hdd-6tb/nghiavm/DATN/data_extract/data_haui/'
with open(data_dir, 'r', encoding='utf-8') as file_data_dir:
    for line in file_data_dir:
        segment = json.loads(line)
        name = segment['Instruction']

        # Xử lý ký tự không hợp lệ
        name = re.sub(r'[\\/*?:"<>|]', '', name)  # Loại bỏ ký tự không hợp lệ cho hệ điều hành
        name = name.replace('/', '_')
        # name = name.replace('?','')
        # name = name.replace('!','')
        # name = name.replace('/','_')
        name = name.replace('.','')
        name = name.replace("'",'')
        name = name.replace('"','')
        name = name.replace(',','')
        
        if len(name) > 250:
            name_new = name[:160]
            filename = os.path.join(save_data, f'{name}.txt')
        else: 
            filename = os.path.join(save_data, f'{name}.txt')
        
        # Ghi dữ liệu vào tệp
        try:
            with open(filename, 'w', encoding='utf-8') as file_txt:
                file_txt.write(segment['Input'] + '\n=======\n' + segment['Output'])
        except:
            print('==== len : ',len(filename))