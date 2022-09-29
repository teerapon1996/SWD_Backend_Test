
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
def process(num):
    units = ("", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า")
    tens = ("", "สิบ", "ยี่สิบ", "สามสิบ", "สี่สิบ", "ห้าสิบ","หกสิบ","เจ็ดสิบ","แปดสิบ","เก้าสิบ")
    # Return msg หากเลขที่ Input มาน้อยกว่า 0
    if num < 0:
        return "ตัวเลขต้องมากกว่าหรือเท่ากับ 0"
    
    if num < 10:
        return units[int(num % 10)]
    
    if num < 100:
        # ถ้าเลขหลักสิบลงท้ายด้วย 1 เช่น 31 tens[num // 10] จะเป็นเลขจำนวนเต็มคิอ 3 ไป map tuple "tens" คือ สามสิบ + กับ String 'เอ็ด' = สามสิบเอ็ด
        if num % 10 == 1:
            return tens[num // 10] + 'เอ็ด'
        # หากหลักสิบและเป็นเลขที่ลงท้ายด้วย 2-9 จะ Map หา Tuple 'units' ปกติ
        else :
            return  tens[num // 10] + units[int(num % 10)] 
    # process() Function ไปใช้อีกครั้งและโยนเลขที่หารได้เศษเป็น Parameter ไปทำงาน Function อีกรอบ
    if num<1000:
        return units[num // 100]  +"ร้อย" +process(int(num % 100))

    if num<10000: 
        return  process(num // 1000) + "พัน" + process(int(num % 1000))

    if num<100000: 
        return  process(num // 10000) + "หมื่น" + process(int(num % 10000))

    if num<1000000: 
        return  process(num // 100000) + "แสน" + process(int(num % 100000))

    if num < 10000000:    
        return process(num // 1000000) + "ล้าน" + process(int(num % 1000000))
    else:
        return "กรอกเลขได้ไม่เกิน 10 ล้าน"

input_number = 0
# Infinite input number
while True:
    try:
        input_number = int(input('Enter your number : '))
        result = process(int(input_number))
    except ValueError:
        print('Invalid number.')
        continue
    print('Convert Number to Thai Text : ' + result )