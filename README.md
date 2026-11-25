# bazaarche — جلسه اول دوره پیشرفته Django

نسخه مستقل آموزشی پایان جلسه اول؛ Python 3.12+ و Django 5.2، SQLite برای اجرای ساده. PostgreSQL، Sites، Multi-Tenancy و DRF عمداً به جلسات بعد موکول شده‌اند.

## اجرا

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

یا با pip در محیط مجازی: `pip install -r requirements.txt` و سپس دستورات manage.py بدون `uv run`.

مرورگر: http://127.0.0.1:8000/products/ و پنل مدیریت: http://127.0.0.1:8000/admin/ . برای ایجاد و ویرایش محصول با superuser وارد شوید. صفحه جزئیات دارای فرم محاسبه قیمت است؛ محاسبه قیمت موجودی را تغییر نمی‌دهد.

## معماری

`View → Form → Service → Repository → ORM` برای محاسبه قیمت؛ CRUD ساده با ModelForm و Generic CBV. قرارداد Protocol و DTO امکان تست PricingService بدون دیتابیس را فراهم می‌کنند. QuerySet سفارشی برای فیلترهای قابل ترکیب، مدل abstract برای timestamp، Middleware برای شناسه و زمان درخواست و Context Processor بدون query برای اطلاعات مشترک قالب‌ها.

قاعده نمونه: سبد با مبلغ حداقل ۱۰۰۰ دلار، ۱۰ درصد تخفیف دارد. این یک انتخاب آموزشی است. InventoryService با update شرطی موجودی را کم می‌کند؛ ثبت سفارش و رزرو موجودی هنوز پیاده نشده‌اند. فرم ویرایش عمومی موجودی را تغییر نمی‌دهد؛ پنل مدیریت فقط برای استفاده آموزشی است.

## تست و بررسی

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py test
```

تست‌های pricing، queryset، inventory، permissions و middleware در apps/shop/tests قرار دارند. تنظیمات DEBUG و کلید پیش‌فرض فقط برای توسعه محلی هستند؛ این نسخه برای استقرار production نیست.

## مسیر مطالعه

۱. core/models.py و shop/models.py و querysets.py
۲. dto.py، contracts.py، repositories.py و services.py
۳. forms.py، core/mixins.py، views.py و urls.py
۴. core/middleware.py و context_processors.py و templates
۵. tests و seed_demo
