# استخدام نظام Ubuntu كقاعدة
FROM ubuntu:latest  

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app  

# نسخ ملف Power BI إلى داخل الحاوية
COPY TP3.pbix /app/  

# التحقق من أن الملف موجود عند تشغيل الحاوية
CMD ["ls", "-l", "/app"]
 
