# import os
# from home.models import Thing
#
# from neostore import settings
#
#
# def cleanup():
#     # 1. Удаляем объекты с amount <= 0
#     things_to_delete = Thing.objects.filter(amount__lte=0)  # используем filter вместо цикла
#     for thing in things_to_delete:
#         # Перед удалением объекта, удаляем его фото
#         if thing.photo:
#             photo_path = os.path.join(settings.MEDIA_ROOT, thing.photo.name)
#             if os.path.exists(photo_path):
#                 os.remove(photo_path)
#                 print(f"Удалено фото: {thing.photo.name}")
#         thing.delete()
#         print(f"Удален объект: {thing.id}")
#
#     # 2. Чистка осиротевших фото (которые в папке, но не в БД)
#     media_root = settings.MEDIA_ROOT
#     photos_path = os.path.join(media_root, 'things')
#
#     used_photos = set()
#     for thing in Thing.objects.exclude(photo=''):
#         used_photos.add(thing.photo.name)
#
#     for filename in os.listdir(photos_path):
#         if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
#             relative_path = f'things/{filename}'
#             file_path = os.path.join(photos_path, filename)
#             if relative_path not in used_photos:
#                 os.remove(file_path)
