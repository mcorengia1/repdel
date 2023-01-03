import cv2
import numpy as np
import os


class Preferences:
    def __init__(self, subFolders, confirmation) -> None:
        self.subFolders = subFolders
        self.confirmation = confirmation


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


def GetPreferences():
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

    return Preferences(subFolders, confirmation)


print("\nWelcome to RepDel, a tool for removing duplicates images\n")

userPreferences = GetPreferences()
imagesRoutes = ()
routesAux = []

# Routes setup
# Get all the files routes in the subfolders
if userPreferences.subFolders == "y":
    for (path, dir_names, files_names) in os.walk(
        os.path.dirname(os.path.realpath(__file__))
    ):
        for fileName in files_names:
            routesAux.append(path + "\\" + fileName)

# Get all the files routes in this folder
else:
    for fileName in os.listdir():
        routesAux.append(os.path.dirname(
            os.path.realpath(__file__)) + "\\" + fileName)

routes = tuple(routesAux)

for i in range(0, len(routes)):
    try:
        img1 = cv2.imread(routes[i])
    except:
        print('Image already removed')

    else:
        # if a write 'if img1' a bug appears
        if img1 is not None:

            for j in range(i+1, len(routes)):
                try:
                    img2 = cv2.imread(routes[j])
                except:
                    print('Image already removed')

                else:
                    if img2 is not None:

                        # They could be duplicates
                        if img1.shape == img2.shape:
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
                                print("######################\nRepeated images found at \n" +
                                      routes[i] + '\nand\n' + routes[j] + '\n######################')

                                # resize the images and show both
                                img1 = ResizeWithAspectRatio(img1, 400)
                                img2 = ResizeWithAspectRatio(img2, 400)

                                # combine both images and show
                                vis = np.concatenate((img1, img2), axis=1)
                                cv2.imshow("comparation", vis)
                                cv2.setWindowProperty(
                                    'comparation', cv2.WND_PROP_TOPMOST, 1)

                                key = 0
                                while key != 49 and key != 50 and key != 51:
                                    print(
                                        "1. Remove the first img\n2. Remove the second img\n3. Keep both\n")

                                    key = cv2.waitKey(0)
                                    if key == 49:
                                        # number 1 on windows
                                        os.remove(routes[i])

                                    elif key == 50:
                                        # number 2 on windows
                                        os.remove(routes[j])

                                    elif key == 51:
                                        # number 3 on windows
                                        continue
                                    else:
                                        cv2.destroyAllWindows()
                                        cv2.imshow('comparation', vis)


                                cv2.destroyAllWindows()
