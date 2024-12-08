# Extract GPS Information from Images

This Python script extracts GPS information from image files using the Pillow library. It reads the EXIF data from an image and formats the latitude and longitude into a readable string.

## Requirements

To run this script, you need to have the following installed:

- Python 3.x
- Pillow library

## Installation and Setup

Follow these steps to set up the environment and run the script:

1. **Clone the repository**  
   First, clone the repository to your local machine:
   ```bash
   git clone https://github.com/fufin228/Extract-GPS-Information-from-Images
   ```

2. **Navigate to the project directory**  
   Change to the project directory:
   ```bash
   cd Extract-GPS-Information-from-Images
   ```

3. **Create a virtual environment**  
   Create a virtual environment to avoid installing packages system-wide:
   ```bash
   python3 -m venv myenv
   ```

4. **Activate the virtual environment**  
   To activate the virtual environment, run:
   ```bash
   source myenv/bin/activate
   ```

5. **Install the required dependencies**  
   Now that your virtual environment is active, install the required libraries by running:
   ```bash
   pip install -r requirements.txt
   ```

   If there is no \`requirements.txt\` file in the repository, you can manually install the required libraries:
   ```bash
   pip install pillow tkintermapview
   ```

6. **Run the script**  
   Now you can run the script:
   ```bash
   python3 window.py
   ```

## Usage

1. Download your image file and place it in the same directory as the script.
2. Rename the image file to \`photo.jpg\` or change the filename in the code to match your image.
3. Run the script using Python:
   ```bash
   python3 window.py
   ```

## How It Works

- The script opens an image file and retrieves its EXIF data.
- It checks if the GPS information is present.
- If GPS data is found, it extracts and formats the latitude and longitude into a string and prints it. If no GPS information is available, it will print a message indicating this.

### Example Output

When the script successfully extracts GPS data, it will output something like:

```
40°26'46.00\" N, 74°0'21.00\" W
```

If there is no GPS information, you will see:

```
GPS information not found.
```

### Main Features

- The script utilizes the Pillow library to handle image files and extract EXIF data.
- It focuses on GPS information, ensuring only essential details are extracted and presented clearly.

## License

This project is licensed under the MIT License.
