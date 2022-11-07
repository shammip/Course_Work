#include <iostream>
#include <vector>
#include <fstream>
#include <cmath>
using namespace std;

//***************************************************************************************************//
//                                DO NOT MODIFY THE SECTION BELOW                                    //
//***************************************************************************************************//

// Pixel structure
struct Pixel
{
    // Red, green, blue color values
    int red;
    int green;
    int blue;
};

/**
 * Gets an integer from a binary stream.
 * Helper function for read_image()
 * @param stream the stream
 * @param offset the offset at which to read the integer
 * @param bytes  the number of bytes to read
 * @return the integer starting at the given offset
 */ 
int get_int(fstream& stream, int offset, int bytes)
{
    stream.seekg(offset);
    int result = 0;
    int base = 1;
    for (int i = 0; i < bytes; i++)
    {   
        result = result + stream.get() * base;
        base = base * 256;
    }
    return result;
}

/**
 * Reads the BMP image specified and returns the resulting image as a vector
 * @param filename BMP image filename
 * @return the image as a vector of vector of Pixels
 */
vector<vector<Pixel>> read_image(string filename)
{
    // Open the binary file
    fstream stream;
    stream.open(filename, ios::in | ios::binary);

    // Get the image properties
    int file_size = get_int(stream, 2, 4);
    int start = get_int(stream, 10, 4);
    int width = get_int(stream, 18, 4);
    int height = get_int(stream, 22, 4);
    int bits_per_pixel = get_int(stream, 28, 2);

    // Scan lines must occupy multiples of four bytes
    int scanline_size = width * (bits_per_pixel / 8);
    int padding = 0;
    if (scanline_size % 4 != 0)
    {
        padding = 4 - scanline_size % 4;
    }

    // Return empty vector if this is not a valid image
    if (file_size != start + (scanline_size + padding) * height)
    {
        return {};
    }

    // Create a vector the size of the input image
    vector<vector<Pixel>> image(height, vector<Pixel> (width));

    int pos = start;
    // For each row, starting from the last row to the first
    // Note: BMP files store pixels from bottom to top
    for (int i = height - 1; i >= 0; i--)
    {
        // For each column
        for (int j = 0; j < width; j++)
        {
            // Go to the pixel position
            stream.seekg(pos);

            // Save the pixel values to the image vector
            // Note: BMP files store pixels in blue, green, red order
            image[i][j].blue = stream.get();
            image[i][j].green = stream.get();
            image[i][j].red = stream.get();

            // We are ignoring the alpha channel if there is one

            // Advance the position to the next pixel
            pos = pos + (bits_per_pixel / 8);
        }

        // Skip the padding at the end of each row
        stream.seekg(padding, ios::cur);
        pos = pos + padding;
    }

    // Close the stream and return the image vector
    stream.close();
    return image;
}

/**
 * Sets a value to the char array starting at the offset using the size
 * specified by the bytes.
 * This is a helper function for write_image()
 * @param arr    Array to set values for
 * @param offset Starting index offset
 * @param bytes  Number of bytes to set
 * @param value  Value to set
 * @return nothing
 */
void set_bytes(unsigned char arr[], int offset, int bytes, int value)
{
    for (int i = 0; i < bytes; i++)
    {
        arr[offset+i] = (unsigned char)(value>>(i*8));
    }
}

/**
 * Write the input image to a BMP file name specified
 * @param filename The BMP file name to save the image to
 * @param image    The input image to save
 * @return True if successful and false otherwise
 */
bool write_image(string filename, const vector<vector<Pixel>>& image)
{
    // Get the image width and height in pixels
    int width_pixels = image[0].size();
    int height_pixels = image.size();

    // Calculate the width in bytes incorporating padding (4 byte alignment)
    int width_bytes = width_pixels * 3;
    int padding_bytes = 0;
    padding_bytes = (4 - width_bytes % 4) % 4;
    width_bytes = width_bytes + padding_bytes;

    // Pixel array size in bytes, including padding
    int array_bytes = width_bytes * height_pixels;

    // Open a file stream for writing to a binary file
    fstream stream;
    stream.open(filename, ios::out | ios::binary);

    // If there was a problem opening the file, return false
    if (!stream.is_open())
    {
        return false;
    }

    // Create the BMP and DIB Headers
    const int BMP_HEADER_SIZE = 14;
    const int DIB_HEADER_SIZE = 40;
    unsigned char bmp_header[BMP_HEADER_SIZE] = {0};
    unsigned char dib_header[DIB_HEADER_SIZE] = {0};

    // BMP Header
    set_bytes(bmp_header,  0, 1, 'B');              // ID field
    set_bytes(bmp_header,  1, 1, 'M');              // ID field
    set_bytes(bmp_header,  2, 4, BMP_HEADER_SIZE+DIB_HEADER_SIZE+array_bytes); // Size of BMP file
    set_bytes(bmp_header,  6, 2, 0);                // Reserved
    set_bytes(bmp_header,  8, 2, 0);                // Reserved
    set_bytes(bmp_header, 10, 4, BMP_HEADER_SIZE+DIB_HEADER_SIZE); // Pixel array offset

    // DIB Header
    set_bytes(dib_header,  0, 4, DIB_HEADER_SIZE);  // DIB header size
    set_bytes(dib_header,  4, 4, width_pixels);     // Width of bitmap in pixels
    set_bytes(dib_header,  8, 4, height_pixels);    // Height of bitmap in pixels
    set_bytes(dib_header, 12, 2, 1);                // Number of color planes
    set_bytes(dib_header, 14, 2, 24);               // Number of bits per pixel
    set_bytes(dib_header, 16, 4, 0);                // Compression method (0=BI_RGB)
    set_bytes(dib_header, 20, 4, array_bytes);      // Size of raw bitmap data (including padding)                     
    set_bytes(dib_header, 24, 4, 2835);             // Print resolution of image (2835 pixels/meter)
    set_bytes(dib_header, 28, 4, 2835);             // Print resolution of image (2835 pixels/meter)
    set_bytes(dib_header, 32, 4, 0);                // Number of colors in palette
    set_bytes(dib_header, 36, 4, 0);                // Number of important colors

    // Write the BMP and DIB Headers to the file
    stream.write((char*)bmp_header, sizeof(bmp_header));
    stream.write((char*)dib_header, sizeof(dib_header));

    // Initialize pixel and padding
    unsigned char pixel[3] = {0};
    unsigned char padding[3] = {0};

    // Pixel Array (Left to right, bottom to top, with padding)
    for (int h = height_pixels - 1; h >= 0; h--)
    {
        for (int w = 0; w < width_pixels; w++)
        {
            // Write the pixel (Blue, Green, Red)
            pixel[0] = image[h][w].blue;
            pixel[1] = image[h][w].green;
            pixel[2] = image[h][w].red;
            stream.write((char*)pixel, 3);
        }
        // Write the padding bytes
        stream.write((char *)padding, padding_bytes);
    }

    // Close the stream and return true
    stream.close();
    return true;
}

//***************************************************************************************************//
//                                DO NOT MODIFY THE SECTION ABOVE                                    //
//***************************************************************************************************//

//Process 1: Vignette effect (darkens corners)
vector<vector<Pixel>> process_1(const vector<vector<Pixel>>& image) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image that is the same size as the input image
    vector<vector<Pixel>> new_image(num_rows, vector<Pixel> (num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Compute math operations that will be used to create the new colors 
            double distance = sqrt(pow(col-num_columns/2,2) + pow(row-num_rows/2,2));
            double scaling_factor = (num_rows - distance) / num_rows;
            //Assign new color values to the pixels 
            new_image[row][col].red = red_color*scaling_factor;
            new_image[row][col].green = green_color*scaling_factor;
            new_image[row][col].blue = blue_color*scaling_factor;   
        }
    }
    //Return the new image
    return new_image;
}

//Process 2: Clarendon effect (darks darker and lights lighter) using a scaling factor
vector<vector<Pixel>> process_2(const vector<vector<Pixel>>& image, double scaling_factor) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image that is the same size as the input image
    vector<vector<Pixel>> new_image(num_rows, vector<Pixel> (num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Compute the average of the colors
            int average_value = (red_color + green_color + blue_color)/3;
            //Create new color variables 
            int new_red_color, new_green_color, new_blue_color; 
            //If the pixel is light, make it lighter            
            if (average_value >= 170) {
                new_red_color = int(255-(255-red_color)*scaling_factor);
                new_green_color = int(255-(255-green_color)*scaling_factor);
                new_blue_color = int(255-(255-blue_color)*scaling_factor);
            } 
            //If the pixel is dark, make it darker
            else if (average_value < 90){
                new_red_color = red_color * scaling_factor; 
                new_green_color = green_color * scaling_factor;
                new_blue_color = blue_color * scaling_factor;
            }
            else {
                new_red_color = red_color; 
                new_green_color = green_color;
                new_blue_color = blue_color;                
            }
            //Assign new color values to the pixels 
            new_image[row][col].red = new_red_color;
            new_image[row][col].green = new_green_color;
            new_image[row][col].blue = new_blue_color;   
        }
    }
    //Return the new image
    return new_image;    
}

//Process 3: Grayscale
vector<vector<Pixel>> process_3(const vector<vector<Pixel>>& image) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image that is the same size as the input image
    vector<vector<Pixel>> new_image(num_rows, vector<Pixel> (num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Compute the average of the colors to get the gray value
            int gray_value = (red_color + green_color + blue_color)/3;
            //Assign gray value to each pixel's color 
            new_image[row][col].red = gray_value;
            new_image[row][col].green = gray_value;
            new_image[row][col].blue = gray_value;
        }
    }
    //Return the new image
    return new_image; 
}

//Process 4: 90 degree clockwise rotation
vector<vector<Pixel>> process_4(const vector<vector<Pixel>>& image) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image with size of rows and columns switched
    vector<vector<Pixel>> new_image(num_columns, vector<Pixel> (num_rows));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Assign color value to each rotated pixel
            new_image[col][(num_rows-1)-row].red = red_color;
            new_image[col][(num_rows-1)-row].green = green_color;
            new_image[col][(num_rows-1)-row].blue = blue_color;
        }
    }
    //Return the new image
    return new_image; 
}

//Process 5: Multiples of 90 degree clockwise rotation
vector<vector<Pixel>> process_5(const vector<vector<Pixel>>& image, int number) {    
    //Compute the angle, which is a multiple of 90 degrees
    int angle = int(number * 90);
    //If angle mod 90 is not 0, angle is not a multiple of 90 degrees
    if (angle%90 != 0) {
        cout << "The angle has to be a multiple of 90 degrees.";
    } 
    //If angle mod 360 is 0, image doesn't rotate or rotates by 360 degrees
    else if (angle%360 == 0) {
        return image; 
    }
    //If angle mod 360 is 90, image rotates by 90 degrees 
    else if (angle%360 == 90) {
        return process_4(image); 
    }
    //If angle mod 360 is 180, image rotates by 180 degrees
    else if (angle%360 == 180) {
        return process_4(process_4(image));
    }
    //If angle mod 360 is 270, image rotates by 270 degrees
    else {
        return process_4(process_4(process_4(image)));
    }
    //Function requires a return value, but it won't reach this point
    return image;
}

//Process 6: Enlarge image
vector<vector<Pixel>> process_6(const vector<vector<Pixel>>& image, int x_scale, int y_scale) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create 2D vector of new image, same size as x and y scale multiplied by image size
    vector<vector<Pixel>> new_image(y_scale*num_rows, vector<Pixel> (x_scale*num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < int(y_scale*num_rows); row++) {
        //Create a for loop for each column
        for (int col = 0; col < int(x_scale*num_columns); col++) {
            //Get the color value for each pixel 
            int red_color = image[int(row/y_scale)][int(col/x_scale)].red;
            int green_color = image[int(row/y_scale)][int(col/x_scale)].green;
            int blue_color = image[int(row/y_scale)][int(col/x_scale)].blue;
            //Assign new color values to the pixels 
            new_image[row][col].red = red_color;
            new_image[row][col].green = green_color;
            new_image[row][col].blue = blue_color;
        }
    }
    //Return the new image
    return new_image;
}

//Process 7: High contrast (black and white)
vector<vector<Pixel>> process_7(const vector<vector<Pixel>>& image) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image that is the same size as the input image
    vector<vector<Pixel>> new_image(num_rows, vector<Pixel> (num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Compute the average of the colors to get the gray value
            int gray_value = (red_color + green_color + blue_color)/3;
            //Create new color variables 
            int new_red_color, new_green_color, new_blue_color; 
            //Pixel becomes white if gray value is greater than 127.5
            if (gray_value >= 255/2) {
                new_red_color = 255;
                new_green_color = 255;
                new_blue_color = 255;
            }
            //Pixel becomes black if gray value is less than 127.5
            else {
                new_red_color = 0;
                new_green_color = 0;
                new_blue_color = 0; 
            }
            //Assign new color values to the pixels 
            new_image[row][col].red = new_red_color;
            new_image[row][col].green = new_green_color;
            new_image[row][col].blue = new_blue_color;
        }
    }
    //Return the new image
    return new_image;
}

//Process 8: Lighten by a scaling factor
vector<vector<Pixel>> process_8(const vector<vector<Pixel>>& image, double scaling_factor) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image that is the same size as the input image
    vector<vector<Pixel>> new_image(num_rows, vector<Pixel> (num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Compute mathematics to lighten colors by a scaling factor 
            int new_red_color = int(255-(255-red_color)*scaling_factor);
            int new_green_color = int(255-(255-green_color)*scaling_factor);
            int new_blue_color = int(255-(255-blue_color)*scaling_factor);
            //Assign new color values to the pixels 
            new_image[row][col].red = new_red_color;
            new_image[row][col].green = new_green_color;
            new_image[row][col].blue = new_blue_color;
        }
    }
    //Return the new image
    return new_image;
}

//Process 9: Darken by a scaling factor 
vector<vector<Pixel>> process_9(const vector<vector<Pixel>>& image, double scaling_factor) {  
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image that is the same size as the input image
    vector<vector<Pixel>> new_image(num_rows, vector<Pixel> (num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Compute mathematics to lighten colors by a scaling factor 
            int new_red_color = red_color*scaling_factor;
            int new_green_color = green_color*scaling_factor;
            int new_blue_color = blue_color*scaling_factor;
            //Assign new color values to the pixels 
            new_image[row][col].red = new_red_color;
            new_image[row][col].green = new_green_color;
            new_image[row][col].blue = new_blue_color;
        }
    }
    //Return the new image
    return new_image;
}

//Process 10: Create black, white, red, green, or blue color image
vector<vector<Pixel>> process_10(const vector<vector<Pixel>>& image) {
    //Get the height and width of image
    int num_rows = image.size(); //height
    int num_columns = image[0].size(); //width
    //Create a 2D vector of new image that is the same size as the input image
    vector<vector<Pixel>> new_image(num_rows, vector<Pixel> (num_columns));
    //Create a for loop for each row 
    for (int row = 0; row < num_rows; row++) {
        //Create a for loop for each column
        for (int col = 0; col < num_columns; col++) {
            //Get the color value for each pixel 
            int red_color = image[row][col].red;
            int green_color = image[row][col].green;
            int blue_color = image[row][col].blue;
            //Compute the max_color value 
            int max_color = max(red_color, green_color); 
            max_color = max(max_color, blue_color); 
            //Create new color variables 
            int new_red_color, new_green_color, new_blue_color; 
            //Compute if pixel is light, then it becomes white
            if (red_color + green_color + blue_color >= 550) {
                new_red_color = 255; 
                new_green_color = 255; 
                new_blue_color = 255; 
            }
            //Compute if pixel is dark, then it becomes black 
            else if (red_color + green_color + blue_color <= 150) {
                new_red_color = 0; 
                new_green_color = 0; 
                new_blue_color = 0; 
            }
            //If red appears more in pixel, pixel becomes red
            else if (max_color == red_color) {
                new_red_color = 255; 
                new_green_color = 0; 
                new_blue_color = 0; 
            }
            //If green appears more in pixel, pixel becomes green
            else if (max_color == green_color) {
                new_red_color = 0; 
                new_green_color = 255; 
                new_blue_color = 0; 
            }
            //Pixels becomes blue
            else {
                new_red_color = 0; 
                new_green_color = 0; 
                new_blue_color = 255; 
            }
            //Assign new color values to the pixels 
            new_image[row][col].red = new_red_color;
            new_image[row][col].green = new_green_color;
            new_image[row][col].blue = new_blue_color;
        }
    }
    //Return the new image
    return new_image;
}

//Main function of the program
int main() {
    //Declare variables
    string file_input, file_output, selection, application, extension; 
    int number_of_rotations, x_scale, y_scale;
    double scaling_factor; 
    vector<vector<Pixel>> image, new_image; 
    
    //Program title 
    cout << "\nImage Processing Application\n";
    cout << "----------------------------";
    
    //Loop while image vector is empty so input file name is invalid
    do {
        //User is prompted to enter image's file name
        cout << "\nEnter input BMP file name: ";
        cin >> file_input; 

        //Read image into 2D vector
        image = read_image(file_input);
        
        //If image vector is empty then wrong file name was input
        if (image.empty() == true) {
        cout << "\nInvalid file name.\n"; 
        }
    }
    while (image.empty() == true);
    
    //Loop while user wants to keep processing images 
    do {
        //Loop while user wants to change file name
        do{
            //Selection menu offered to user 
            cout << "\nSELECTION MENU:";
            cout << "\n0) Change file - current: " + file_input;
            cout << "\n1) Vignette";
            cout << "\n2) Clarendon";
            cout << "\n3) Grayscale";
            cout << "\n4) Rotate 90 degrees";
            cout << "\n5) Rotate multiple 90 degrees";
            cout << "\n6) Enlarge";
            cout << "\n7) High contrast";
            cout << "\n8) Lighten";
            cout << "\n9) Darken";
            cout << "\n10) Black, white, red, green, blue";
            cout << "\nQ) Quit\n";
            
            //Take user input about selection 
            cout << "\nEnter menu selection: ";
            cin >> selection; 
            
            //If user wants to change file name
            if (selection == "0") {
                cout << "\nOption selected: Change file" << endl;
                
                //Loop while input file name is invalid
                do {
                    //User is prompted to enter image's file name
                    cout << "\nEnter input BMP file name: ";
                    cin >> file_input; 

                    //Read image into 2D vector
                    image = read_image(file_input);

                    //If image vector is empty then wrong file name was input
                    if (image.empty() == true) {
                        cout << "\nInvalid file name.\n"; 
                    }
                }
                while (image.empty() == true);
                cout << "\nChange file successfully applied." << endl;
            }
        }
        while (selection == "0");

        //If selection is 1, apply vignette
        if (selection == "1") {
            cout << "\nOption selected: Vignette" << endl;
            application = "\nVignette";
            new_image = process_1(image);
        }
        //If selection is 2, apply clarendon
        else if (selection == "2") {
            cout << "\nOption selected: Clarendon" << endl;
            application = "\nClarendon";
            cout << "\nEnter the scaling factor: ";
            cin >> scaling_factor;
            new_image = process_2(image, scaling_factor);
        }
        //If selection is 3, apply grayscale
        else if (selection == "3") {
            cout << "\nOption selected: Grayscale" << endl;
            application = "\nGrayscale";
            new_image = process_3(image);
        }
        //If selection is 4, apply rotate 90 degrees
        else if (selection == "4") {
            cout << "\nOption selected: Rotate 90 degrees" << endl;
            application = "\nRotate 90 degrees";
            new_image = process_4(image);
        }
        //If selection is 5, apply rotate multiple 90 degrees
        else if (selection == "5") {
            cout << "\nOption selected: Rotate multiple 90 degrees" << endl;
            application = "\nRotate multiple 90 degrees"; 
            cout << "\nEnter the number of rotations: ";
            cin >> number_of_rotations;
            new_image = process_5(image, number_of_rotations);
        }
        //If selection is 6, apply enlarge
        else if (selection == "6") {
            cout << "\nOption selected: Enlarge" << endl;
            application = "\nEnlarge";
            cout << "\nEnter the x scale to enlarge image by: ";
            cin >> x_scale;
            cout << "\nEnter the y scale to enlarge image by: ";
            cin >> y_scale;
            new_image = process_6(image, x_scale, y_scale);
        }
        //If selection is 7, apply high contrast
        else if (selection == "7") {
            cout << "\nOption selected: High Contrast" << endl;
            application = "\nHigh contrast";
            new_image = process_7(image);
        }
        //If selection is 8, apply lighten
        else if (selection == "8") {
            cout << "\nOption selected: Lighten" << endl;
            application = "\nLighten";
            cout << "\nEnter the scaling factor: ";
            cin >> scaling_factor;
            new_image = process_8(image, scaling_factor);
        }
        //If selection is 9, apply darken
        else if (selection == "9") {
            cout << "\nOption selected: Darken" << endl;
            application = "\nDarken";
            cout << "\nEnter the scaling factor: ";
            cin >> scaling_factor;
            new_image = process_9(image, scaling_factor);
        }
        //If selection is 10, apply black, white, red, green, blue
        else if (selection == "10") {
            cout << "\nOption selected: Black, white, red, green, blue" << endl;
            application = "\nBlack, white, red, green, blue";
            new_image = process_10(image);
        }
        //If selection is Q, quit the program
        else if (selection == "Q") {
            cout << "\nThank you for using the Image Processing Application!\n" << endl;
            exit(0);
        }
        //If invalid selection is input
        else {
            cout << "\nInvalid selection.\n";
        }
        
        //If selection is between 1 to 10
        if (selection == "1" || selection == "2" || selection == "3" || selection == "4" ||
            selection == "5" || selection == "6" || selection == "7" || selection == "8" ||
            selection == "9" || selection == "10") {
            
            //Loop while output file name is invalid
            do {
                //Prompt user to enter output file name
                cout << "\nEnter output BMP file name: "; 
                cin >> file_output;
                
                //If length of output file name is less than 5
                if (file_output.length() < 5) {
                    cout << "\nPlease enter a file name with extension: .bmp\n";
                }
                //If length of output file name is equal to or greater than 5
                else {
                    //Assign output file name's extension to variable extension 
                    extension = file_output.substr(file_output.length()-4,4);
                    //If extension is not equal to .bmp
                    if (extension != ".bmp") {
                        cout << "\nPlease enter a file name with extension: .bmp\n";
                    }
                    //If output file name is same as input file name
                    if (file_input == file_output) {
                        cout << "\nPlease enter an output file name, different from input file name.\n";
                    }
                }
            }
            while (file_input == file_output || extension != ".bmp" || file_output.length() < 5);

            //Write the new image into a new file
            bool success = write_image(file_output, new_image);

            //If new_image was successfully input to file_output
            if (success == 1) { 
                cout << application + " successfully applied." << endl;
            }
            //If new_image was not successfully input to file_output
            else {
                cout << application + " failed." << endl;
            }
        }
    }
    while (true); 
    return 0;
}//end of main()
