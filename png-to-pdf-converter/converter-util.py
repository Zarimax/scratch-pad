from PIL import Image

number_of_pages = 22
imagelist = []

for i in range(1, number_of_pages + 1):
    image_path = f"C:\\Users\\Black Beast\\Desktop\\p{i}.png"
    print(f"... adding {image_path}")
    image = Image.open(image_path)
    imagelist.append(image.convert('RGB'))

imagelist[0].save(r'C:\Users\Black Beast\Desktop\merged_result.pdf',save_all=True, append_images=imagelist[1:])
