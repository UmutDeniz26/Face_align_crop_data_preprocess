import os

def main(dataset_path, output_file):

    # Veri setinin bulunduğu dizin  -> dataset_path
    # Çıktı dosyasının adı  -> output_file

    counter = 0
    n = 0
    #print(os.listdir("./Elif/YoutubeFace/aligned_images_DB2"))

    # Dosya açma işlemi
    with open(output_file, 'w') as file:
        #file.write('personname_klasor_img\n')
        # Ana dizindeki klasörleri listele
        for person_name in os.listdir(dataset_path):
            person_path = os.path.join(dataset_path, person_name)

            # Klasörleri kontrol et ve içerisindeki dosyaları listele
            if os.path.isdir(person_path):
            # file.write(f'{person_name}')

                # Person'a ait tüm alt klasörlerdeki görselleri listele
                person_images = []

                for subfolder_name in os.listdir(person_path):
                    subfolder_path = os.path.join(person_path, subfolder_name)

                    if os.path.isdir(subfolder_path):
                        # Alt klasördeki dosyaları listele
                        for image_file in os.listdir(subfolder_path):
                            person_number = f'{counter:05d}'
                            img_number = f'{n:06d}'

                            person_images.append(f'\t {person_number}_{subfolder_name}_{img_number}')
                            n += 1

                # Person'a ait tüm görselleri tek bir satırda listeleyerek yaz
                file.write('\n'.join(person_images))
                file.write('\n')

                counter += 1

    # Bilgileri içeren txt dosyası oluşturuldu
    print(f'Liste oluşturuldu ve {output_file} adında kaydedildi.')

if __name__ == "__main__":
    main(dataset_path="./Elif/YoutubeFace/YoutubeFace",
         output_file='./Elif/YoutubeFace/new.txt')
