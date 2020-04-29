"""
test for getimage
"""

import getImages
image_urls = getImages.get_image_urls('bing', 10, 'レジ')
getImages.save_images(image_urls,'image_directory')