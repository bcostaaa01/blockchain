with open('demo.txt', mode='r') as f:
    file_content = f.readlines()
    for line in file_content:
        print(line)
    print(file_content)
