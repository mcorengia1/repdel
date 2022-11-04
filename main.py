# include subfolders
# confirm Button

# list all the photos
# compare all the entre ellas a ver si son iguales
# si son iguales confirm button para eliminar

# imports
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


class Preferences:
    def __init__(self, subFolders, confirmation) -> None:
        self.subFolders = subFolders
        self.confirmation = confirmation


print("\nWelcome to RepDel, a tool for removing duplicates images\n")

subFolders = "x"
confirmation = "x"

while subFolders != "y" and subFolders != "n":
    subFolders = input(
        "Do you want to analice the subfolders of this directoty too? (y/n)"
    )
while confirmation != "y" and confirmation != "n":
    confirmation = input(
        "Do you want to see a confirmation button before deleting an image? (y/n)"
    )

userPreferences = Preferences(subFolders, confirmation)
imagesRoutes = ()
routesAux = []

if userPreferences.subFolders == "y":
    for (path, dir_names, files_names) in os.walk(
        os.path.dirname(os.path.realpath(__file__))
    ):
        print(f"Path = {path}, Name = {dir_names}, File = {files_names}")

        for fileName in files_names:
            routesAux.append(path + "\\" + fileName)

else:
    for fileName in os.listdir():
        print(f"fileName = {fileName}")
        routesAux.append(os.path.dirname(os.path.realpath(__file__)) + "\\" + fileName)

routes = tuple(routesAux)

for i in range(0, len(routes)):
    img1 = cv2.imread(routes[i])

    # if a write 'if img1' a bug appears
    if img1 is not None:

        for j in range(i, len(routes)):
            img2 = cv2.imread(routes[j])

            if img2 is not None:

                if img1.shape == img2.shape:
                    # They could be duplicates
                    diff = cv2.subtract(img1, img2)
                    (
                        b,
                        g,
                        r,
                    ) = cv2.split(diff)

                    if (
                        cv2.countNonZero(b) == 0
                        and cv2.countNonZero(g) == 0
                        and cv2.countNonZero(r) == 0
                    ):
                        print("Repeated images found")
                        # resize the images and show both
                        img1 = ResizeWithAspectRatio(img1, 400)
                        img2 = ResizeWithAspectRatio(img2, 400)

                        # combine both images and show
                        vis = np.concatenate((img1, img2), axis=1)
                        cv2.imshow("comparation", vis)

                        remove_img = 0
                        while remove_img != 1 and remove_img != 2 and remove_img != 9:
                            remove_img = input(
                                "1. Remove the first img\n2. Remove the second img\n3. Keep both\n"
                            )

