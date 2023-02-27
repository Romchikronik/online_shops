from django.test import TestCase

# Create your tests here.
# qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

# def save(self, *args, **kwargs):
#
#     value = self.title
#     self.slug = slugify(value, allow_unicode=True)
#     super().save(*args, **kwargs)
#
#     # вызываем метод save родительской модели
#     super(OnlineShop, self).save(*args, **kwargs)
#
#     # создаем QR-код по ссылке на страницу товара
#     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
#     url = settings.BASE_URL + reverse('online_shop_detail', args=[self.slug, self.pk]) # формируем ссылку на страницу товара
#     qr.add_data(url)
#     qr.make(fit=True)
#
#     # сохраняем QR-код в модель товара
#     img = qr.make_image(fill_color="black", back_color="white")
#     img_io = BytesIO()
#     img.save(img_io, format='JPEG')
#     self.qr_code.save(str(self.slug) + '.jpg', ContentFile(img_io.getvalue()), save=True)