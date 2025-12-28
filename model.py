from ultralytics import YOLO
if __name__ == "__main__":
    model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)
    model.train(
        # เปลี่ยน Path ตรงนี้ให้เป็นที่อยู่ไฟล์ data.yaml ของคุณ
        data=r'C:\Users\hp\Desktop\study\dataset\data.yaml', 
        
        epochs=100,       # จำนวนรอบ (แนะนำ 50-100 รอบ)
        imgsz=640,       # ขนาดภาพ
        save_period=10,
        # --- โซนแก้ Error Memory เต็ม ---
        batch=24,         # ใส่ 8 พอครับ (ถ้ายังเต็มให้ลดเหลือ 4)
        device=0,        # ใช้การ์ดจอ RTX 5050
        name='TheForgeV1' # ชื่อโปรเจกต์ (จำชื่อนี้ไว้นะ)
    )