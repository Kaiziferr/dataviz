def identify_classes(path: str)->list[str]:
    """
    Identify the class labels available in an image dataset.

    This function inspects the dataset directory structure and extracts
    the class names based on the folder organization. Each subdirectory
    inside the provided path is considered a separate class, assuming that
    the images are organized following a standard supervised learning
    directory structure:

        dataset/
        ├── class_1/
        │   ├── image_1.jpg
        │   └── image_2.jpg
        ├── class_2/
        │   ├── image_3.jpg
        │   └── image_4.jpg

    Parameters
    ----------
    path : str
        Path to the root directory containing the image dataset. Each
        subfolder within this directory represents an image class.

    Returns
    -------
    list[str]
        A sorted list containing the detected class names.

    Notes
    -----
    The function assumes that the dataset follows a folder-based labeling
    convention 

    Examples
    --------
    >>> identify_classes(Path("data/images"))
    ['cat', 'dog', 'horse']
    """

    class_names = sorted(
            [
                folder.name for folder in path.iterdir()
                if folder.is_dir()
            ]
        )
    return class_names



def count_images_per_class(path: Path, class_names: list[str]) -> dict[str, int]:
    """
    Count the number of images available for each class in an image dataset.

    This function scans the dataset directory and counts the number of image
    files contained in each class subdirectory. The function assumes that the
    dataset follows a folder-based organization where each class is represented
    by a separate directory.

        dataset/
        ├── cat/
        │   ├── image_1.jpg
        │   ├── image_2.jpg
        │   └── ...
        ├── dog/
        │   ├── image_3.jpg
        │   └── ...

    Parameters
    ----------
    path : Path
        Path to the root directory containing the image dataset.

    class_names : list[str]
        List of class names to inspect. Each class name must correspond
        to a subdirectory inside the dataset root directory.

    Returns
    -------
    dict[str, int]
        A dictionary where the keys are the class names and the values
        are the corresponding number of images found in each class.

    Raises
    ------
    FileNotFoundError
        If the dataset root directory or one of the class directories
        does not exist.

    NotADirectoryError
        If the provided dataset path is not a directory.

    Notes
    -----
    This function assumes that every class is stored in its own folder.
    All files contained inside each class directory are counted.

    Examples
    --------
    >>> count_images_per_class(Path("data/images"), ["cat", "dog"])
    {'cat': 1250, 'dog': 980}
    """

    if not path.exists():
        raise FileNotFoundError(f"Dataset path '{path}' does not exist.")

    if not path.is_dir():
        raise NotADirectoryError(f"'{path}' is not a directory.")

    image_counts = {}

    for class_name in class_names:
        class_path = path / class_name

        if not class_path.exists():
            raise FileNotFoundError(
                f"Class directory '{class_path}' does not exist."
            )

        if not class_path.is_dir():
            raise NotADirectoryError(
                f"'{class_path}' is not a directory."
            )

        image_counts[class_name] = sum(
            file.is_file() for file in class_path.iterdir()
        )

    return image_counts


def show_random_images(class_path: Path, n_images: int = 5) -> None:
    """
    Display a random sample of images from a dataset class.

    This function randomly selects a specified number of images from a
    class directory and displays them in a single row using Matplotlib.

    Parameters
    ----------
    class_path : Path
        Path to the directory containing the images of a single class.

    n_images : int, default=5
        Number of images to randomly sample and display.

    Returns
    -------
    None
        Displays the selected images using Matplotlib.

    Raises
    ------
    FileNotFoundError
        If the specified class directory does not exist.

    NotADirectoryError
        If the provided path is not a directory.

    ValueError
        If ``n_images`` is greater than the number of available images
        in the class directory.

    Notes
    -----
    Images are selected without replacement using ``random.sample()``.
    The function assumes that all files inside the directory are valid
    image files supported by Matplotlib.

    Examples
    --------
    >>> show_random_images(Path("dataset/cats"), n_images=5)
    """

    if not class_path.exists():
        raise FileNotFoundError(
            f"Class directory '{class_path}' does not exist."
        )

    if not class_path.is_dir():
        raise NotADirectoryError(
            f"'{class_path}' is not a directory."
        )

    image_paths = [img for img in class_path.iterdir() if img.is_file()]

    if len(image_paths) < n_images:
        raise ValueError(
            f"Requested {n_images} images, but only "
            f"{len(image_paths)} are available in '{class_path.name}'."
        )

    selected = random.sample(image_paths, n_images)

    plt.figure(figsize=(3 * n_images, 4))

    for i, image_path in enumerate(selected):
        image = plt.imread(image_path)
        plt.subplot(1, n_images, i + 1)
        plt.imshow(image)
        plt.axis("off")

    plt.suptitle(class_path.name, fontsize=15)
    plt.tight_layout()
    plt.show()




def extract_image_metadata(image_path: Path) -> dict:
    """
    Extract image metadata without fully loading the image into memory.

    This function inspects an image file and extracts metadata useful for
    exploratory data analysis (EDA). It relies on Pillow's lazy loading,
    meaning that only the image header and metadata are read without
    decoding the full pixel array.

    Parameters
    ----------
    image_path : Path
        Path to the image file.

    Returns
    -------
    dict
        Dictionary containing the extracted image metadata.

    Raises
    ------
    FileNotFoundError
        If the image file does not exist.

    ValueError
        If the image cannot be identified or opened.

    Notes
    -----
    This function does not load the image pixels into memory. Therefore,
    statistics based on pixel values (mean, histogram, brightness,
    entropy, etc.) are not computed.

    Examples
    --------
    >>> extract_image_metadata(Path("cat_001.jpg"))

    """

    if not image_path.exists():
        raise FileNotFoundError(f"Image '{image_path}' does not exist.")

    metadata = {
        "filename": image_path.name,
        "extension": image_path.suffix.lower(),
        "file_size_bytes": image_path.stat().st_size,
        "file_size_mb": round(image_path.stat().st_size / (1024 ** 2), 3)
    }

    try:

        with Image.open(image_path) as img:

            width, height = img.size

            metadata.update({

                "format": img.format,
                "width": width,
                "height": height,
                "resolution": width * height,
                "aspect_ratio": round(width / height, 3),
                "orientation": (
                    "Landscape"
                    if width > height
                    else "Portrait"
                    if height > width
                    else "Square"
                ),
                "mode": img.mode,
                "channels": len(img.getbands()),
                "bands": img.getbands(),
                "bits_per_channel": 8,
                "dpi": img.info.get("dpi"),
                "compression": img.info.get("compression"),
                "has_transparency": (
                    "A" in img.getbands()
                    or "transparency" in img.info
                ),
                "is_animated": getattr(img, "is_animated", False),
                "n_frames": getattr(img, "n_frames", 1)
            })

            exif = {}

            if hasattr(img, "getexif"):

                raw_exif = img.getexif()

                if raw_exif:

                    exif = {
                        TAGS.get(tag, tag): value
                        for tag, value in raw_exif.items()
                    }

            metadata["exif"] = exif

        return metadata

    except Exception as e:
        raise ValueError(
            f"Unable to extract metadata from '{image_path}'."
        ) from e
