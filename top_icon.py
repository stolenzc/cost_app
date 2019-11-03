import base64


# 将icon.ico文件转换为icon.py文件
with open("icon.py","a") as f:
    f.write('class Icon(object):\n')
    f.write('\tdef __init__(self):\n')
    f.write("\t\tself.img='")
with open("icon.ico","rb") as i:
    b64str = base64.b64encode(i.read())
    with open("icon.py","ab+") as f:
        f.write(b64str)
with open("icon.py","a") as f:
    f.write("'")

# from icon import Icon
# with open('tmp.ico','wb') as tmp:
#     tmp.write(base64.b64decode(Icon().img))
# root.iconbitmap('tmp.ico')
# os.remove('tmp.ico')
