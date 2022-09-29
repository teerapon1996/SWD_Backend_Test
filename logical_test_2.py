
"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""

def process(num):
    num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),(50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
    roman = ''
    while num > 0: #วนจนกว่าตัวเลข input ที่รับมาจะเหลือ 0
        for i, r in num_map: #Map tuple of list
            while num >= i: #ค้นหาตัวเลขที่เข้าเงื่อนไข >=
                roman += r #ตัวอักษร Roman ที่ Map ได้บันทึกในตัวแปร 'roman' และเลขที่เหลือต่อท้ายไปเรื่อยๆ
                num -= i #ตัวแปรที่ input - num ที่ Map ได้ 
    return roman

while True:
    try:
        input_number = int(input("Enter your number : " ))
        result = process(int(input_number))
    except ValueError:
        print('Invalid number.')
        continue
    print('Convert Number to Roman is : : ' + result )

