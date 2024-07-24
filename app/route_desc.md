# Service and Route Description

<div style="text-align:center"><h3>English Description</h3></div>

1. **Borrow Status Section**:
   This section is responsible for managing the status of borrowing requests. CRUD operations are implemented for it, but it is not needed during project execution as all states will be saved.

2. **User Borrow Section**:
   This section allows a customer to request to borrow a book. The conditions for borrowing the book are reviewed, and if the user meets the requirements, the request is registered. The customer can then receive the book from the library employee.

3. **Sell Section**:
   The selling section is where a customer can purchase a book. If they have sufficient inventory and the conditions for selling the book are met, the book is sold to them. They can receive the book from the library specialist.

4. **Management Section**:
   This section has various subcategories accessible only by employees. It includes functionalities such as listing available books for sale, income reporting from book borrowing and sales categorized by type, listing books borrowed by each user with search filters for book name, category name, number of times borrowed, and available books for borrowing. It also provides the service of receiving lists of fines based on days and number of fines incurred, with sorting capabilities. Additionally, functionalities for delivering requested books and recording deliveries to customers by specialists, as well as receiving borrowed books from customers and delivering them to the library, are designed.

5. **Categories Section**:
   This section is designed for managing categories, with CRUD operations implemented for it.

6. **Books Section**:
   This section is designed for managing books, with CRUD operations implemented for it.

7. **Users Section**:
   In this section, only the service for recharging a user's account is implemented, which can only be done by an employee.


<div style="text-align:center"><h3>توضیحات فارسی</h3></div>

1. بخش borrow status: این بخش وضعیت درخواست های قرض گرفتن را به عهده دارد که برای آن عملیات CRUD نوشته شده است و نیازی به استفاده از آن نیست چون هنگام اجرای پروژه تمامی حالات ذخیره خواهد شد.

2. بخش user borrow: بخشی است که مشتری میتواند درخواست قرض کردن کتابی را بدهد و شرایط دریافت کتاب بررسی میشود و در صورتی که واجد شرایط باشد درخواستش ثبت شده و میتواند کتاب را از کارمند کتابخانه تحویل بگیرد.

3. قسمت sell: بخش خرید، بخشی است که مشتری میتواند کتاب را بخرد و در صورتی که موجودی کافی داشته باشد و شرایط فروش کتاب نیز محیا باشد کتاب به ایشان فروخته میشود که میتواند آن را از کارشناس تحویل بگیرد.

4. بخش management: این بخش دارای زیر مجموعه های مختلفی است که فقط کارمند میتواند به آن دسترسی داشته باشد و قابلیت لیست کتاب های موجود براش فروش، گزارش گیری درآمد حاصل از قرض دادن و فروش کتاب به تفکیک دسته بندی، لیست کتاب های قرض گرفته شده توسط هر کاربر با فیلتر جستجوی نام کتاب، نام دسته بندی، تعداد بار قرض گرفته شده و تعداد کتاب های موجود برای قرض دادن است و همچنین سرویس دریافت لیست جریمه ها بر اساس روز و تعداد جریمه های انجام شده با قابلیت مرتب کردن و همچنین تحویل کتاب درخواست شده و ثبت تحویل به مشتری توسط کارشناس و همچنین دریافت کتاب قرض گرفته شده از مشتری و تحویل آن به کتابخانه نیز طراحی شده است.

5. بخش categories: این بخش برای مدیریت دسته بندی ها طراحی شده و عملیات CRUD نیز برای آن نوشته شده است.

6. بخش Books: این بخش برای مدیریت کتاب ها طراحی شده و عملیات CRUD نیز برای آن نوشته شده است

7. بخش users: در این بخش فقط سرویس شارژ کردن حساب کاربر نوشته شده است که فقط کارمند میتواند حساب کاربر را شارژ نماید.